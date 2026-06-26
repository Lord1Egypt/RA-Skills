#!/usr/bin/env python3
"""A股IPO周报 - 微信友好版（周三~下周二自动周期）

⚠️ 架构对称依赖：本脚本从 akshare 拉取 IPO 数据自包含生成，不读 LLM 写的中间文件，
   无 LLM 写入依赖。教训来源：v2.0.5→v2.0.7 修复链（其他 send 脚本因 LLM 不写
   中间文件推旧版）。详见 SKILL.md Changelog v2.0.7。
"""
import re, os
import pandas as pd
from datetime import datetime, timedelta, timezone
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _send_lib import wx  # noqa: E402  # 推送共用库（v3.2.3 迁移）

# ── 配置加载（白名单读取外部配置，路径可通过 ENV_FILE 系列变量覆盖）──────────────
_REQUIRED_KEYS = ["WECOM_WEBHOOK_KEY", "IWENCAI_API_KEY"]
for _p in (
    os.environ.get("ENV_FILE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env")),
    os.environ.get("ENV_FILE_FALLBACK", "/workspace/.env"),
):
    if not os.path.exists(_p):
        continue
    try:
        for _line in open(_p):
            _line = _line.strip()
            if not _line or _line.startswith("#") or "=" not in _line: continue
            _k, _v = _line.split("=", 1)
            _k = _k.strip()
            if _k in _REQUIRED_KEYS and _k not in os.environ:
                os.environ[_k] = _v.strip().strip('"').strip("'")
    except (OSError, UnicodeDecodeError):
        continue

# ── 北京时间 & IPO周期计算 ───────────────────────────────
_TZ = timedelta(hours=8)

def now_bj():
    return datetime.now(timezone.utc).astimezone(timezone(_TZ))

def get_ipo_report_period(ref_date=None):
    """周期：本周一~本周五（固定5天）"""
    if ref_date is None:
        ref_date = now_bj()
    monday = ref_date - timedelta(days=ref_date.weekday())
    friday = monday + timedelta(days=4)
    return monday, friday, monday.strftime("%m月%d日"), friday.strftime("%m月%d日")

# ── 防并发原子锁（PID + TTL 智能锁）──────────────────
_LOCK_FILE = "/tmp/a_stock_ipo.lock"
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lock import lock as _smart_lock, unlock as _smart_unlock

def _acquire_lock():
    """PID+TTL 智能锁；返回 True=获取成功, False=已被占。"""
    return _smart_lock(_LOCK_FILE, owner=__file__)

def _release_lock():
    _smart_unlock(_LOCK_FILE)

# ── 防重：按「执行日期+周期末日期」去重，同一周期只发送一次 ──
_STATE_FILE = "/workspace/scripts/.ipo_report_sent"

def _mark_sent_for_period(period_key):
    """记录今日执行的周期标识（YYYYMMDD），用于去重"""
    with open(_STATE_FILE, "w") as f:
        f.write(f"{NOW.strftime('%Y%m%d')}|{period_key}")

def _already_sent_for_period(period_key):
    """今日已运行过相同周期则跳过（不同周期正常发送）"""
    if not os.path.exists(_STATE_FILE):
        return False
    content = open(_STATE_FILE).read().strip()
    if not content:
        return False
    parts = content.split("|")
    if len(parts) != 2:
        return False  # 格式异常，视为未发送过
    sent_date, sent_period = parts
    today = NOW.strftime("%Y%m%d")
    if sent_date != today:
        return False  # 新的一天，清洗旧记录
    return sent_period == period_key

# ── 周期计算（需要先引入 now_bj）──────────────────────────
NOW = now_bj()

# ── 原子锁：在周期计算之前就拦截并发 ──────────────────────
if not _acquire_lock():
    sys.exit(0)
_period_start_dt, _period_end_dt, REPORT_START, PERIOD_END_STR = get_ipo_report_period(NOW)
# 周期唯一标识：用于文件命名（YYYYMMDD = 周期末日期）
_PERIOD_KEY = _period_end_dt.strftime("%Y%m%d")  # e.g. "20260424"

# ── 兜底检查：周期距今不超过3周，超出则视为异常拒绝发送 ──
_days_old = (NOW.date() - _period_end_dt.date()).days
if _days_old > 21:
    print(f"[IPO周报] ⚠️ 周期 {_period_start_dt.date()}～{_period_end_dt.date()} 距今 {_days_old} 天（>{21}天），疑似数据异常，拒绝发送！")
    _release_lock(); sys.exit(1)

if _already_sent_for_period(_PERIOD_KEY):
    print(f"[IPO周报] 今日（{NOW.strftime('%Y%m%d')}）已运行过相同周期({_PERIOD_KEY})，跳过")
    _release_lock(); sys.exit(0)
# 周期：本周一 ～ 本周五
PERIOD_START = _period_start_dt
PERIOD_END   = _period_end_dt
# 下周上会计划截止日：本期周五 + 7天 = 下下周五
_w = NOW.weekday()
_days_to_next_fri = (11 - _w) % 7 + 7   # 距下下周五的天数
THIS_WEEK_END = (_period_end_dt + timedelta(days=3)).strftime("%m/%d")   # 下周周期截止日（下周一）
NEXT_WEEK_END = (_period_end_dt + timedelta(days=7)).strftime("%m/%d")   # 下下周周期截止日（下周五）
QUEUE_DATE    = _period_end_dt.strftime("%Y年%m月%d日")

# ── Webhook 由 _send_lib.wx 提供（v3.2.3 迁移：删 24 行重复实现）──

def shname(name, n=12):
    return name[:n] + ".." if len(name) > n else name

def sdate(dt):
    return str(dt)[5:7] + "/" + str(dt)[8:10]

def board_alias(b):
    return {"上交所科创板": "科创板", "深交所创业板": "创业板",
            "深交所主板": "深主板", "上交所主板": "沪主板",
            "北交所": "北交所"}.get(b, b)

# ── 首日涨幅（akshare 同花顺）──────────────────────────────
def fmt_price(v):
    if pd.isna(v): return "N/A"
    return f"{v:.2f}元"

# ── 数据拉取（AKShare）─────────────────────────────────────
# 注意：akshare 调用在 __main__ 中执行（锁之后），见下方 _collect_ipo_data()
import akshare as ak  # 模块级导入（延迟到 __main__ 调用时实际使用）


def _collect_ipo_data(period_start, period_end, period_end_dt):
    """
    在原子锁之后执行所有 akshare 数据拉取。
    返回 dict: {review, ths_df, queue, recent_r, next_r, recent_l, reg_up, recent_up}
    """
    import akshare as _ak
    import pandas as pd
    from datetime import timedelta

    pstart_str = period_start.strftime("%Y-%m-%d")
    pend_str = period_end.strftime("%Y-%m-%d")

    pstart_ts = pd.Timestamp(pstart_str)
    pend_ts = pd.Timestamp(pend_str)
    next_start_ts = (pd.Timestamp(period_end_dt) + timedelta(days=3)).tz_localize(None)
    next_end_ts = (pd.Timestamp(period_end_dt) + timedelta(days=7)).tz_localize(None)

    review = _ak.stock_ipo_review_em()
    review["上会日期"] = pd.to_datetime(review["上会日期"], errors="coerce").dt.tz_localize(None)
    recent_r = review.loc[review["上会日期"].between(pstart_ts, pend_ts)].dropna(subset=["上会日期"]).sort_values("上会日期")
    next_r = review.loc[review["上会日期"].between(next_start_ts, next_end_ts)].dropna(subset=["上会日期"]).sort_values("上会日期")

    ths_df = _ak.stock_xgsr_ths()
    ths_df["上市_dt"] = pd.to_datetime(ths_df["上市日期"], errors="coerce")
    recent_l = ths_df[ths_df["上市_dt"].between(pd.Timestamp(pstart_str), pd.Timestamp(pend_str))].sort_values("上市_dt")

    queue = _ak.stock_ipo_declare_em()
    queue["更新日期"] = pd.to_datetime(queue["更新日期"], errors="coerce").dt.tz_localize(None)
    recent_up = queue[queue["更新日期"].between(pd.Timestamp(pstart_str), pd.Timestamp(pend_str))]
    reg_up = recent_up[recent_up["最新状态"].isin(["注册", "核准"])].dropna(subset=["企业名称"])

    # ── 5板块排队情况（修复 v2.0.8：补 queue_detail/queue_status_detail/source_date 字段）──
    boards_map = [
        ('科创板', _ak.stock_register_kcb, {'已问询', '已受理', '上市委会议通过', '中止(财报更新)', '提交注册'}),
        ('创业板', _ak.stock_register_cyb, {'已问询', '已受理', '上市委会议通过', '中止'}),
        ('北交所', _ak.stock_register_bj, {'已问询', '已受理', '上市委会议通过', '上市委会议暂缓', '中止'}),
        ('沪主板', _ak.stock_register_sh, {'已问询', '已受理', '上市委会议暂缓'}),
        ('深主板', _ak.stock_register_sz, {'已问询', '中止', '中止审查'}),
    ]
    all_full = []
    for name, fn, _ in boards_map:
        df = fn().copy()
        df["更新日期"] = pd.to_datetime(df["更新日期"], errors="coerce").dt.tz_localize(None)
        df["板块"] = name
        all_full.append(df[["企业名称", "最新状态", "板块", "更新日期"]])
    all_full = pd.concat(all_full, ignore_index=True)
    all_full = all_full.loc[:, ~all_full.columns.duplicated()]

    # 数据新鲜度（取全市场最大更新日期作 source_date）
    source_date = all_full["更新日期"].max().strftime("%Y年%m月%d日")
    print(f"[排队] 数据更新日期: {source_date}")

    # 180 天内的有效记录（去掉时区避免 tz-naive/tz-aware 比较错误）
    PASSED_CUTOFF = (pd.Timestamp(period_end_dt) - pd.DateOffset(days=180)).tz_localize(None)
    recent_q = all_full[all_full["更新日期"] >= PASSED_CUTOFF].copy()

    # 在会 vs 终止 分类
    CATS = {
        '排队中': {'已问询','已受理','上市委会议通过','上市委会议暂缓','中止','中止审查','中止(财报更新)',
                   '提交注册','已收到注册申请材料','已上发审会,暂缓表决','已上发审会，暂缓表决',
                   '预先披露更新','已反馈'},
        '已终止': {'终止','终止注册','撤回','不予注册','审核不通过','未在规定时限内回复'},
    }
    def _cat(s):
        for cat, sts in CATS.items():
            if s in sts: return cat
        return '其他'
    recent_q['分类'] = recent_q['最新状态'].map(_cat)

    # pivot → queue_detail
    pivot = recent_q.pivot_table(index="板块", columns="分类", values="最新状态",
                                 aggfunc="count", fill_value=0, observed=True)
    pivot["全市场"] = pivot.sum(axis=1)
    order = ["科创板", "创业板", "北交所", "沪主板", "深主板"]
    pivot = pivot.reindex(order)
    if "已终止" in pivot.columns:
        pivot.drop(columns="已终止", inplace=True)
    queue_detail = pivot.to_dict("index")
    print(f"[排队] queue_detail: { {b: dict(queue_detail[b]) for b in order} }")

    # 状态细项 → queue_status_detail
    detail_status = ['已问询','已受理','上市委会议通过','上市委会议暂缓',
                     '中止','中止审查','中止(财报更新)',
                     '提交注册','已收到注册申请材料',
                     '已上发审会,暂缓表决','已上发审会，暂缓表决','预先披露更新','已反馈']
    queue_status_detail = {}
    for b in order:
        sub = recent_q[(recent_q['板块']==b) & (recent_q['最新状态'].isin(detail_status))]
        vc = sub['最新状态'].value_counts()
        queue_status_detail[b] = {k: int(v) for k, v in vc.items()}
    print(f"[排队] queue_status_detail: {queue_status_detail}")

    return dict(review=review, ths_df=ths_df, queue=queue,
                recent_r=recent_r, next_r=next_r, recent_l=recent_l,
                reg_up=reg_up, recent_up=recent_up,
                queue_detail=queue_detail, queue_status_detail=queue_status_detail,
                source_date=source_date)


def _fetch_queue_from_web(lines):
    """
    调东方财富注册制审核接口 stock_register_* 系列，取各板块实时排队数。
    直接追加 lines（不返回值）；PERIOD_START/_pend 等从 globals 读取。

    各板块在审口径（穷举验证，匹配凤凰网周报官方数字）：
      科创板：已问询 + 已受理 + 上市委会议通过 + 中止(财报更新) + 提交注册  → 精确命中41
      创业板：已问询 + 已受理 + 上市委会议通过 + 中止                       → 精确命中39
      北交所：已问询 + 已受理 + 上市委会议通过 + 上市委会议暂缓 + 中止        → 152（官方174，AKShare数据滞后约22家）
      沪主板：已问询 + 已受理 + 上市委会议暂缓                               → 18（官方17，差+1）
      深主板：已问询 + 中止 + 中止审查                                        → 精确命中16

    来源：东方财富/证监会公示，数据每日更新。
    """
    import akshare as ak, pandas as pd

    boards_map = [
        ('科创板', ak.stock_register_kcb,
         {'已问询', '已受理', '上市委会议通过', '中止(财报更新)', '提交注册'}),
        ('创业板', ak.stock_register_cyb,
         {'已问询', '已受理', '上市委会议通过', '中止'}),
        ('北交所', ak.stock_register_bj,
         {'已问询', '已受理', '上市委会议通过', '上市委会议暂缓', '中止'}),
        ('沪主板', ak.stock_register_sh,
         {'已问询', '已受理', '上市委会议暂缓'}),
        ('深主板', ak.stock_register_sz,
         {'已问询', '中止', '中止审查'}),
    ]
    boards = {}
    for name, fn, in_status in boards_map:
        df = fn()
        active = df[df['最新状态'].isin(in_status)]
        boards[name] = len(active)
        max_dt = df['更新日期'].max().strftime('%Y-%m-%d')
        print(f"[排队] {name}: {len(active)}家在审（更新至{max_dt}）")

    total = sum(boards.values())
    src = f"东方财富/证监会公示（各板块实时，验证口径）"
    print(f"[排队] 全市场{total}家: {boards}  来源:{src}")

    # ── 返回完整状态分布（供报告展示）────────────────────
    CATS = {
        # 在会排队（含预披露/反馈）：问询+受理+中止+提交注册+暂缓+预披露+已反馈（180天内更新）
        '排队中': {'已问询','已受理','上市委会议通过','上市委会议暂缓','中止','中止审查','中止(财报更新)',
                   '提交注册','已收到注册申请材料','已上发审会,暂缓表决','已上发审会，暂缓表决',
                   '预先披露更新','已反馈'},
        '已终止': {'终止','终止注册','撤回','不予注册','审核不通过','未在规定时限内回复'},
    }
    def _cat(s):
        for cat, sts in CATS.items():
            if s in sts: return cat
        return '其他'

    # 全量数据含更新日期（用于时间过滤）
    all_full = []
    for name, fn, _ in boards_map:
        df = fn().copy()
        df["更新日期"] = pd.to_datetime(df["更新日期"], errors="coerce")
        df["板块"] = name
        all_full.append(df[["企业名称","最新状态","板块","更新日期"]])
    all_full = pd.concat(all_full, ignore_index=True)
    all_full = all_full.loc[:, ~all_full.columns.duplicated()]

    PASSED_CUTOFF = pd.Timestamp("today") - pd.DateOffset(days=180)

    # 透视表：仅统计180天内有更新的记录
    recent = all_full[all_full["更新日期"] >= PASSED_CUTOFF].copy()
    recent["分类"] = recent["最新状态"].map(_cat)
    pivot = recent.pivot_table(index="板块", columns="分类", values="最新状态", aggfunc="count", fill_value=0, observed=True)
    pivot["全市场"] = pivot.sum(axis=1)
    order = ["科创板", "创业板", "北交所", "沪主板", "深主板"]
    pivot = pivot.reindex(order)
    # 剔除已终止列（历史数据不代表当前状态）
    if "已终止" in pivot.columns:
        pivot.drop(columns="已终止", inplace=True)
    queue_detail = pivot.to_dict("index")

    print(f"[排队] 完整分布: { {b: dict(queue_detail[b]) for b in order} }")
    # 同时返回细项（各状态×各板块，180天内）
    detail_status = ['已问询','已受理','上市委会议通过','上市委会议暂缓',
                     '中止','中止审查','中止(财报更新)',
                     '提交注册','已收到注册申请材料',
                     '已上发审会,暂缓表决','已上发审会，暂缓表决','预先披露更新','已反馈']
    # 用 value_counts 代替 pivot_table，避免列分组器维度问题
    detail_dict = {}
    for b in order:
        sub = recent[(recent['板块']==b) & (recent['最新状态'].isin(detail_status))]
        vc = sub['最新状态'].value_counts()
        detail_dict[b] = {k: int(v) for k, v in vc.items()}

    max_dt_str = max_dt.replace('-', '年', 1).replace('-', '月') + '日'  # '2026-04-30' → '2026年04月30日'
    lines += ["━━━━━━━━━━", f"📊 一、排队情况（截止{max_dt_str}）", ""]
    lines.append(f"全市场共{total}家：{boards}")
    lines.append("")
# ── 组装报告（由 __main__ 调用）───────────────────────────────
def build_report_lines(data, period_start_str, period_end_str):
    import pandas as pd
    lines = [f"📋 A股IPO周报 {period_start_str}～{period_end_str}", ""]
    qd = data.get('queue_detail', {})
    sd = data.get('queue_status_detail', {})
    source_date = data.get('source_date', 'N/A')
    recent_r = data.get('recent_r')
    recent_up = data.get('recent_up')
    recent_l = data.get('recent_l')
    next_r = data.get('next_r')

    _order = ['科创板', '创业板', '北交所', '沪主板', '深主板']
    if qd:
        # 汇总
        total_all = sum(v.get('全市场', 0) for v in qd.values())
        total_wenxun = sum(sd.get(b, {}).get('已问询', 0) for b in _order)
        total_guohui = sum(
            sd.get(b, {}).get('上市委会议通过', 0) + sd.get(b, {}).get('上市委会议暂缓', 0)
            for b in _order)
        total_zijian = sum(sd.get(b, {}).get('提交注册', 0) for b in _order)
        lines += ["━━━━━━━━━━", f"📊 一、排队情况（截止{source_date}）", ""]
        lines.append(f"全市场共{total_all}家：问询{total_wenxun}家 | "
                     f"已过会待发行{total_guohui}家 | 提交注册{total_zijian}家")
        lines.append("")
        for b in _order:
            bd_data = qd.get(b, {})
            bd_total = bd_data.get('排队中', 0)
            bd_sd = sd.get(b, {})
            parts = []
            for st_key, disp in [('已受理','已受理'), ('已问询','问询'),
                                  ('上市委会议通过','过会'), ('上市委会议暂缓','过会'),
                                  ('中止','中止'), ('中止审查','中止'),
                                  ('中止(财报更新)','中止'),
                                  ('提交注册','提交注册')]:
                cnt = bd_sd.get(st_key, 0)
                if cnt > 0:
                    parts.append(f"{disp}{cnt}")
            detail_str = " | ".join(parts) if parts else f"共{bd_total}家"
            lines.append(f"【{b}】{bd_total}家  {detail_str}")
    else:
        lines += ["━━━━━━━━━━", "📊 一、排队情况（数据获取失败）", ""]
        lines.append("  ⚠️ 数据暂缺")

    passed_r = recent_r[recent_r["审核状态"] == "上会通过"]
    pending_r = recent_r[recent_r["审核状态"] == "未上会"]
    failed_r = recent_r[recent_r["审核状态"].isin(["上会未通过", "取消审核"])]
    lines += ["", "━━━━━━━━━━", f"📋 二、本周期上会（{period_start_str}～{period_end_str}）", ""]

    if len(passed_r) > 0:
        lines.append(f"✅ 通过：{len(passed_r)}家")
        for _, r in passed_r.iterrows():
            lines.append(f"  · {shname(r.get('企业名称', r.get('股票简称','?')))} | "
                         f"{board_alias(r.get('上市板块',''))} | {sdate(r['上会日期'])}")
    else:
        lines.append("  本周期无上会记录")

    if len(pending_r) > 0:
        lines.append(f"🔄 待审：{len(pending_r)}家")
        for _, r in pending_r.iterrows():
            lines.append(f"  · {shname(r.get('企业名称', r.get('股票简称','?')))} | "
                         f"{board_alias(r.get('上市板块',''))} | {sdate(r['上会日期'])}")

    if len(failed_r) > 0:
        lines.append(f"❌ 否决：{len(failed_r)}家")
        for _, r in failed_r.iterrows():
            lines.append(f"  · {shname(r.get('企业名称', r.get('股票简称','?')))} | "
                         f"{board_alias(r.get('上市板块',''))}")

    reg_up2 = recent_up[recent_up["最新状态"].isin(["注册", "核准"])].dropna(subset=["企业名称"])
    lines += ["", "━━━━━━━━━━", f"📋 三、本周期获批（{period_start_str}～{period_end_str}）", ""]
    if len(reg_up2) > 0:
        lines.append(f"📄 获发行批文：{len(reg_up2)}家")
        for _, r in reg_up2.iterrows():
            lines.append(f"  · {shname(r.get('企业名称',''))} | "
                         f"{board_alias(r.get('拟上市地点',''))} | "
                         f"{str(r['更新日期'])[:10]}")
    else:
        lines.append("  （暂无数据）")

    term_up = recent_up[recent_up["最新状态"].isin(["终止"])].dropna(subset=["企业名称"])
    lines += ["", "━━━━━━━━━━", f"📋 四、本周期终止/撤回（{period_start_str}～{period_end_str}）", ""]
    if len(term_up) > 0:
        for _, r in term_up.iterrows():
            lines.append(f"  · {shname(r.get('企业名称',''))} | "
                         f"{board_alias(r.get('拟上市地点',''))}")
    else:
        lines.append("  本周期无终止撤回记录")

    lines += ["", "━━━━━━━━━━", f"📋 五、下周期上会计划（{THIS_WEEK_END}～{NEXT_WEEK_END}）", ""]
    if len(next_r) > 0:
        for _, r in next_r.iterrows():
            lines.append(f"  · {shname(r.get('企业名称', r.get('股票简称','?')))} | "
                         f"{board_alias(r.get('上市板块',''))} | "
                         f"计划{sdate(r['上会日期'])}")
    else:
        lines.append("  ⚠️ 近期暂无上会安排（数据更新存在滞后，以证监会官网为准）")

    lines += ["", "━━━━━━━━━━", f"📋 六、本周期新股上市（{period_start_str}～{period_end_str}）", ""]
    if len(recent_l) > 0:
        for _, r in recent_l.iterrows():
            cd = str(r.get("股票代码", ""))
            nm = r.get("股票简称", "?")
            dt = sdate(r["上市_dt"]) if pd.notna(r.get("上市_dt")) else "?"
            gain = f"{r['首日涨跌幅']:.2f}%" if pd.notna(r.get("首日涨跌幅")) else "无数据"
            pr = fmt_price(r.get("发行价"))
            lines.append(f"  · {nm}（{cd}）| 上市:{dt} | 发行:{pr} | 涨幅:{gain}")
    else:
        lines.append("  （无）")

    lines += ["", "━━━━━━━━━━",
              f"📌 数据来源：{source_date}",
              "⚠️ 仅供参考，不构成投资建议。"]
    return lines


if __name__ == "__main__":
    # 数据拉取（在原子锁之后执行）
    import argparse as _argparse
    import akshare as _ak
    import pandas as pd
    from datetime import timedelta

    # ── CLI 参数：--ref-date 用来回溯跑历史周报（默认今天） ──
    _cli = _argparse.ArgumentParser(description="A股IPO周报")
    _cli.add_argument('--ref-date', default=None,
                     help='回溯日期 YYYY-MM-DD（默认今天）')
    _cli_args = _cli.parse_args()
    if _cli_args.ref_date:
        # 覆盖 NOW + 重新计算周期变量（保持与 cron 触发时一致的逻辑）
        from datetime import datetime as _dt, timezone as _tz
        NOW = _dt.fromisoformat(_cli_args.ref_date).replace(tzinfo=_tz(_TZ))
        _period_start_dt, _period_end_dt, REPORT_START, PERIOD_END_STR = get_ipo_report_period(NOW)
        _PERIOD_KEY = _period_end_dt.strftime("%Y%m%d")
        _days_old = (NOW.date() - _period_end_dt.date()).days
        print(f"[IPO周报] [CLI] ref_date={_cli_args.ref_date} → 周期 {_period_start_dt.date()}～{_period_end_dt.date()}（距今 {_days_old} 天）")
        if _days_old > 21:
            print(f"[IPO周报] ⚠️ 周期距今 > 21 天，拒绝发送！")
            _release_lock(); sys.exit(1)
        if _already_sent_for_period(_PERIOD_KEY):
            print(f"[IPO周报] 周期({_PERIOD_KEY})已发过，跳过")
            _release_lock(); sys.exit(0)
        # 同步更新所有下游用到的模块级变量
        PERIOD_START = _period_start_dt
        PERIOD_END   = _period_end_dt
        THIS_WEEK_END = (_period_end_dt + timedelta(days=3)).strftime("%m/%d")
        NEXT_WEEK_END = (_period_end_dt + timedelta(days=7)).strftime("%m/%d")
        QUEUE_DATE    = _period_end_dt.strftime("%Y年%m月%d日")

    pstart_str = _period_start_dt.strftime("%Y-%m-%d")
    pend_str = _period_end_dt.strftime("%Y-%m-%d")

    # 收集数据
    data = _collect_ipo_data(_period_start_dt, _period_end_dt, _period_end_dt)
    lines = build_report_lines(data, pstart_str, pend_str)

    try:
        import os
        print(f"[TS] 第一步：收集数据...")
        report = "\n".join(lines)
        if report:
            print(f"[TS] 第二步：保存Markdown报告...")
            _dir = "/workspace/projects/A股报告系统/reports"
            os.makedirs(_dir, exist_ok=True)
            _path = os.path.join(_dir, f"IPO周报_{_PERIOD_KEY}.md")
            with open(_path, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"  已保存: {_path}")
            print("\n" + "="*60)
            print(report)
            print("="*60)
            print(f"[TS] 第三步：推送...")
            err2 = wx(report)
            print("\n" + ("✅ 已推送" if err2 == 0 else f"❌ err={err2}"))
            # ── 发送成功后才标记，避免发送失败却仍去重 ──
            if err2 == 0:
                _mark_sent_for_period(_PERIOD_KEY)
                print(f"[去重] 已记录执行日期+周期: {NOW.strftime('%Y%m%d')}|{_PERIOD_KEY}")
    finally:
        _release_lock()
