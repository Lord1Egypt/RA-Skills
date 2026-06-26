#!/usr/bin/env python3
"""财经周末要闻推送脚本 - 支持从历史收盘小结提取情绪轨迹数据
第一步（LLM）：搜新闻 + 生成报告，写入 /tmp/weekend_news_content.txt
第二步（Python）：读取文件 → 保存MD → 打印
第三步（Python）：推送
"""
import sys, os, subprocess, json, re
from pathlib import Path
from datetime import datetime, timedelta, timezone

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
            if not _line or _line.startswith("#") or "=" not in _line:
                continue
            _k, _v = _line.split("=", 1)
            _k = _k.strip()
            if _k in _REQUIRED_KEYS and _k not in os.environ:
                os.environ[_k] = _v.strip().strip('"').strip("'")
    except (OSError, UnicodeDecodeError):
        continue

# ── 防重复运行锁（PID + TTL 智能锁）──────────────────
_LOCK_FILE = "/tmp/a_stock_weekend.lock"
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lock import lock as _smart_lock, unlock as _smart_unlock

def _acquire_lock():
    if not _smart_lock(_LOCK_FILE, owner=__file__):
        _sys.exit(0)

def _release_lock():
    _smart_unlock(_LOCK_FILE)

# ── 共用推送库（v3.1.1 抽取）────────────────────────────────────
from _send_lib import get_webhook_url, wx, notify_failure  # noqa: E402

_TZ = timezone(timedelta(hours=8))
TS = datetime.now(_TZ).strftime("%Y%m%d_%H%M")
content_file = '/tmp/weekend_news_content.txt'
REPORTS_DIR = Path("/workspace/projects/A股报告系统/reports")

# ── v3.4 数据驱动: 从 /tmp/_weekend_5d.json 读取 5d 7 字段 (替代 v3.3 自抽) ──
WEEKEND_DATA_JSON = '/tmp/_weekend_5d.json'
WEEKEND_FIELDS = ['综合评分', 'IF基差', '两融(亿)', '两融占比%', 'PE', 'PE分位%', 'ERP%']


def _load_5d_data() -> dict:
    """从 /tmp/_weekend_5d.json 读 5d 7 字段; 缺字段时调 dispatcher 兜底

    返回 {date_str: {field: value or None}}
    """
    import sys as _s
    _s.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from skill_dispatcher import extract_5d_data, get_prev_n_trade_dates, WEEKEND_FIELD_PATTERNS

    data = {}
    dates = []
    if os.path.exists(WEEKEND_DATA_JSON):
        try:
            with open(WEEKEND_DATA_JSON, encoding='utf-8') as f:
                data = json.load(f)
            dates = sorted(data.keys())
            print(f"[{TS}] ✓ v3.4 json 已读 ({len(dates)} 天)")
        except Exception as e:
            print(f"[{TS}] ⚠ v3.4 json 解析失败: {e}, 走兜底")
            data = {}
            dates = []

    if not data or not dates:
        print(f"[{TS}] 🔄 兜底: 调 dispatcher.extract_5d_data 拉数据")
        dates = get_prev_n_trade_dates(5)
        data = extract_5d_data(str(REPORTS_DIR), dates)
        # 写回 json, 下次直接读
        with open(WEEKEND_DATA_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[{TS}] ✓ 兜底完成, 写回 {WEEKEND_DATA_JSON}")
        return data

    # 完整性检查: 任一日期任一字段为 None → 走兜底
    missing = [(d, f) for d in dates for f in WEEKEND_FIELD_PATTERNS
               if data.get(d, {}).get(f) is None]
    if missing:
        miss_str = '、'.join([f'{d}/{f}' for d, f in missing[:5]])
        print(f"[{TS}] ⚠ 缺字段 ({len(missing)}): {miss_str}{'...' if len(missing)>5 else ''}")
        print(f"[{TS}] 🔄 兜底: 调 dispatcher.extract_5d_data 重抽")
        dates = get_prev_n_trade_dates(5)
        data = extract_5d_data(str(REPORTS_DIR), dates)
        with open(WEEKEND_DATA_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[{TS}] ✓ 兜底完成, 写回 {WEEKEND_DATA_JSON}")
    else:
        print(f"[{TS}] ✓ 7 字段全部完整 ({len(dates)} 天 × {len(WEEKEND_FIELD_PATTERNS)} 字段)")

    return data


def _render_lines(data: dict) -> dict:
    """5d json → 7 行渲染文字 (注入段用)

    7 行: 量化情绪打分 / 涨停家数趋势 / 两融余额(亿) / 两融占比% / 沪深300PE / PE分位% / IF基差 / ERP%
    """
    dates = sorted(data.keys())
    if not dates:
        return {}

    wd_names = ['一', '二', '三', '四', '五', '六', '日']

    def _wd(d):
        from datetime import datetime as _dt
        return f"周{wd_names[_dt.strptime(d, '%Y%m%d').weekday()]}"

    def _fmt_score(d):
        v = data[d].get('综合评分')
        return f"{_wd(d)}{v if v else '？'}分"

    def _fmt_pe(d):
        v = data[d].get('PE')
        return f"{_wd(d)}{v if v else '？'}"

    def _fmt_pe_pct(d):
        v = data[d].get('PE分位%')
        return f"{_wd(d)}{v if v else '？'}%"

    def _fmt_erp(d):
        v = data[d].get('ERP%')
        return f"{_wd(d)}{v if v else '？'}%"

    def _fmt_margin(d):
        v = data[d].get('两融(亿)')
        return f"{_wd(d)}{v['value'] if v else '？'}"

    def _fmt_margin_pct(d):
        v = data[d].get('两融占比%')
        return f"{_wd(d)}{v['value'] if v else '？'}%"

    def _fmt_ifbasis(d):
        v = data[d].get('IF基差')
        return f"{_wd(d)}{v['value'] if v else '❌'}"  # P0 fix: None→❌ (与其它字段一致, 跟 v3.3 模板对齐)

    return {
        'sent_line': " → ".join([_fmt_score(d) for d in dates]),
        'pe_line': " → ".join([_fmt_pe(d) for d in dates]),
        'pe_pct_line': " → ".join([_fmt_pe_pct(d) for d in dates]),
        'erp_line': " → ".join([_fmt_erp(d) for d in dates]),
        'rz_line': " → ".join([_fmt_margin(d) for d in dates]),
        'rz_pct_line': " → ".join([_fmt_margin_pct(d) for d in dates]),
        'ifbasis_line': " → ".join([_fmt_ifbasis(d) for d in dates]),
        'dates': dates,
    }


def _extract_main_report(extract_only: bool):
    """extract-only 模式: 仅抽数据到 json 不推送 (v3.4 数据流)"""
    if extract_only:
        data = _load_5d_data()
        lines = _render_lines(data)
        json_path = Path('/tmp/weekend_emotion_data.json')
        json_path.write_text(json.dumps(lines, ensure_ascii=False, indent=2))
        print(f"[{TS}] v3.4 情绪轨迹数据已写入 {json_path}")
        for k, v in lines.items():
            print(f"  {k}: {v}")
        sys.exit(0)

def _build_and_push_report():
    """读取内容文件 → 注入 v3.4 7 字段情绪轨迹 → 保存 → 推送"""
    if not os.path.exists(content_file):
        msg = f"{content_file} 不存在，请先由LLM生成报告内容"
        print(f"[{TS}] ❌ {msg}")
        notify_failure("周末要闻", msg)
        sys.exit(1)

    with open(content_file, encoding='utf-8') as f:
        report = f.read()

    if not report.strip():
        msg = "报告内容为空"
        print(f"[{TS}] ❌ {msg}")
        notify_failure("周末要闻", msg)
        sys.exit(1)

    # ── 修正标题日期（周末区间：上周六 → 本周日）───────────
    sat = (datetime.now(_TZ) - timedelta(days=1)).strftime("%Y年%m月%d日")
    sun = datetime.now(_TZ).strftime("%Y年%m月%d日")
    _correct_title = f"📰 【财经周末要闻】{sat} - {sun}"
    if re.match(r'^📰 【财经周末要闻】', report):
        report = re.sub(r'^📰 【财经周末要闻】.*', _correct_title, report, count=1, flags=re.MULTILINE)

    # 提取 v3.4 5d 数据 + 渲染 7 行
    print(f"[{TS}] 加载 v3.4 5d 7 字段数据...")
    data = _load_5d_data()
    lines = _render_lines(data)

    # ── 注入 7 字段真实数据 (覆盖 LLM 写的占位符) ────────
    # 注: 涨停家数趋势/北向资金 按 v3.4 决策不展示, 故未注入
    _injection_specs = [
        ('量化情绪打分',  'sent_line'),
        ('两融余额（亿元）',  'rz_line'),
        ('两融余额占流通市值比例', 'rz_pct_line'),
        ('沪深300PE',   'pe_line'),
        ('近5年分位点',  'pe_pct_line'),
        ('股市风险溢价（ERP）', 'erp_line'),
        ('IF基差',     'ifbasis_line'),
    ]
    injected = 0
    for label, key in _injection_specs:
        if not lines.get(key):
            continue
        # 匹配: "• 标签：xxxx"  (允许中间有空格/全角)
        pat = re.compile(rf'•\s*{re.escape(label)}[：:].*?(?=[\n•])', re.DOTALL)
        if pat.search(report):
            report = pat.sub(f'• {label}：{lines[key]}', report)
            print(f"[{TS}] ✓ {label} 已注入")
            injected += 1
    print(f"[{TS}] 注入段完成: {injected}/7 字段")

    print(f"[{TS}] 第三步：保存Markdown报告...")
    os.makedirs(REPORTS_DIR, exist_ok=True)
    _date_str = datetime.now(_TZ).strftime("%Y%m%d")
    _path = REPORTS_DIR / f"财经周末要闻_{_date_str}.md"
    with open(_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  已保存: {_path}")

    print("\n" + "="*60)
    print(report)
    print("="*60)

    print(f"\n[{TS}] 第四步：推送...")
    errcode = wx(report)
    if errcode == 0:
        print(f"\n[{TS}] ✅ 已推送")
        sys.exit(0)
    else:
        msg = f"webhook 返回错误: err={errcode}"
        print(f"[{TS}] ❌ {msg}")
        notify_failure("周末要闻", msg)
        sys.exit(1)

if __name__ == "__main__":
    _acquire_lock()
    err = 0
    try:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('--extract-only', action='store_true')
        args = parser.parse_args()

        if args.extract_only:
            _extract_main_report(True)
        else:
            _build_and_push_report()
    except Exception as e:
        print(f"[{TS}] ❌ 执行异常: {e}")
        import traceback; traceback.print_exc()
        notify_failure("周末要闻", f"脚本执行异常: {e}")
        err = 1
    finally:
        _release_lock()
        print(f"\n[{TS}] 完成")
        sys.exit(0 if err == 0 else 1)