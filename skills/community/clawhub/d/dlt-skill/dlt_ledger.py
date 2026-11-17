# -*- coding: utf-8 -*-
"""
大乐透「诚实账本 + 预算守护」模块（本地 · 私密 · 非预测）

目标（基于 NCPG 伤害减损实证）：
- 诚实账本：持续记录每期花费/中奖/累计净亏与 ROI，让玩家看见真实亏损，
  在想加注时拉他一把。这是研究证明对玩家最有保护价值的功能之一。
- 预算守护：设定月度上限；超支时醒目告警，把"只花闲钱"变成硬约束。

本次升级（客户提的需求）：
1. 客户自填：--entry 交互式记账（期号/花费/中奖/备注），也有 --record-spend/--record-win 快捷命令。
2. 私密性：可选口令加密（--lock/--unlock）。锁定后账本文件仅持口令者可读，
   自动记账在锁定时优雅跳过；文件默认仅存本地、不联网、不上传（客户自己唯一可见）。
3. 逐期分析：period_analysis() 给出每期 投入/产出/净亏/ROI 与累计曲线。
4. 合理化建议：generate_advice() 基于真实数据给出分级建议（超预算/追号/负期望等）。

设计要点：
- 纯标准库（json/os/datetime/base64/hashlib/getpass/argparse），无外部依赖。
- 按 period 幂等 upsert，重复跑同期限不会重复计入花费。
- 所有"中奖/净亏"均为已发生交易的真实统计，不预测、不承诺。
- 不改 generate_predictions 任何输出，守住一致性红线。
- 加密说明：采用 PBKDF2-HMAC-SHA256 派生密钥 + SHA-256 流密码（CTR 式）。
  这是"本地防窥"级保护（防他人随手打开文件读取），非对抗专业攻击者的军工级加密；
  口令遗忘无法找回，请牢记。
"""
import json
import os
import base64
import hashlib
import getpass
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER_PATH = os.path.join(HERE, 'dlt_ledger.json')
BUDGET_PATH = os.path.join(HERE, 'dlt_budget.json')

# 大乐透返奖率≈51%：长期每花100元平均拿回约51元（理论参考线）
THEORETICAL_RETURN_RATE = 0.51
DEFAULT_MONTHLY_LIMIT = 200.0  # 默认月度预算上限(元)：约月收入0.5%的保守档


class LedgerLocked(Exception):
    """账本已加密锁定，需解锁后才能读写。"""


# ---------------- 加密（本地防窥，可选） ----------------
def _keystream(key: bytes, length: int, nonce: bytes) -> bytes:
    out = b''
    counter = 0
    while len(out) < length:
        h = hashlib.sha256(key + nonce + counter.to_bytes(8, 'big')).digest()
        out += h
        counter += 1
    return out[:length]


def _encrypt_text(plaintext: str, passphrase: str) -> dict:
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', passphrase.encode('utf-8'), salt, 200_000)
    nonce = os.urandom(8)
    pt = plaintext.encode('utf-8')
    ks = _keystream(key, len(pt), nonce)
    ct = bytes(a ^ b for a, b in zip(pt, ks))
    return {
        "v": 1,
        "algo": "pbkdf2-sha256+sha256-stream",
        "salt": base64.b64encode(salt).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "ct": base64.b64encode(ct).decode(),
    }


def _decrypt_text(blob: dict, passphrase: str) -> str:
    salt = base64.b64decode(blob["salt"])
    nonce = base64.b64decode(blob["nonce"])
    ct = base64.b64decode(blob["ct"])
    key = hashlib.pbkdf2_hmac('sha256', passphrase.encode('utf-8'), salt, 200_000)
    ks = _keystream(key, len(ct), nonce)
    pt = bytes(a ^ b for a, b in zip(ct, ks))
    return pt.decode('utf-8')


def is_ledger_locked() -> bool:
    if not os.path.exists(LEDGER_PATH):
        return False
    try:
        with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
            d = json.load(f)
        return isinstance(d, dict) and d.get("algo") == "pbkdf2-sha256+sha256-stream" and "ct" in d
    except Exception:
        return False


def lock_ledger(passphrase: str) -> int:
    """用口令加密账本（加密后明文被覆盖，仅持口令可读）。返回原记录条数。"""
    data = load_ledger()  # 若已锁定会抛 LedgerLocked，由调用方处理
    blob = _encrypt_text(json.dumps(data, ensure_ascii=False), passphrase)
    with open(LEDGER_PATH, 'w', encoding='utf-8') as f:
        json.dump(blob, f, ensure_ascii=False)
    return len(data)


def unlock_ledger(passphrase: str) -> list:
    """用口令解密账本（解密后恢复为明文本地文件）。返回记录列表。"""
    with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
        blob = json.load(f)
    pt = _decrypt_text(blob, passphrase)
    data = json.loads(pt)
    save_ledger(data)
    return data


# ---------------- 读写 ----------------
def load_ledger():
    if not os.path.exists(LEDGER_PATH):
        return []
    if is_ledger_locked():
        raise LedgerLocked("账本已加密锁定，请先用 --unlock 口令解锁。")
    try:
        with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_ledger(data):
    with open(LEDGER_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_budget():
    if not os.path.exists(BUDGET_PATH):
        return {"monthly_limit": DEFAULT_MONTHLY_LIMIT, "block_if_over": False}
    try:
        with open(BUDGET_PATH, 'r', encoding='utf-8') as f:
            b = json.load(f)
        b.setdefault("monthly_limit", DEFAULT_MONTHLY_LIMIT)
        b.setdefault("block_if_over", False)
        return b
    except Exception:
        return {"monthly_limit": DEFAULT_MONTHLY_LIMIT, "block_if_over": False}


def save_budget(b):
    with open(BUDGET_PATH, 'w', encoding='utf-8') as f:
        json.dump(b, f, ensure_ascii=False, indent=2)


# ---------------- 记录 ----------------
def record_spend(period, amount, note="auto: 预测生成(基本投注)"):
    """按 period 幂等 upsert 花费（重复跑同期限不会重复计）。"""
    if is_ledger_locked():
        raise LedgerLocked("账本已锁定，无法自动记账；请先 --unlock。")
    period = int(period)
    data = load_ledger()
    today = datetime.date.today().isoformat()
    for e in data:
        if int(e['period']) == period:
            e['spend'] = float(amount)
            e['date'] = today
            e['note'] = note
            save_ledger(data)
            return e
    data.append({
        "period": period, "date": today,
        "spend": float(amount), "wins": 0.0, "note": note,
    })
    save_ledger(data)
    return data[-1]


def record_win(period, amount):
    """记录某期中奖金额（覆盖式，便于多次修正）。"""
    if is_ledger_locked():
        raise LedgerLocked("账本已锁定，无法回填；请先 --unlock。")
    period = int(period)
    amount = float(amount)
    data = load_ledger()
    for e in data:
        if int(e['period']) == period:
            e['wins'] = amount
            save_ledger(data)
            return e
    # 若该期尚无花费记录, 也允许独立记录中奖
    data.append({
        "period": period, "date": datetime.date.today().isoformat(),
        "spend": 0.0, "wins": amount, "note": "manual: 中奖回填",
    })
    save_ledger(data)
    return data[-1]


# ---------------- 统计 ----------------
def summary():
    data = load_ledger()
    total_spend = sum(float(e.get('spend', 0)) for e in data)
    total_wins = sum(float(e.get('wins', 0)) for e in data)
    net = total_wins - total_spend
    periods = len(data)
    roi = (net / total_spend * 100) if total_spend > 0 else 0.0
    theoretical_wins = total_spend * THEORETICAL_RETURN_RATE
    theoretical_net = theoretical_wins - total_spend
    return {
        "periods": periods,
        "total_spend": round(total_spend, 2),
        "total_wins": round(total_wins, 2),
        "net": round(net, 2),
        "roi": round(roi, 2),
        "theoretical_net": round(theoretical_net, 2),
        "theoretical_return_rate": THEORETICAL_RETURN_RATE,
    }


def period_analysis(limit=None):
    """逐期 投入/产出/净亏/ROI 与累计。返回按 period 升序的列表。"""
    data = load_ledger()
    data = sorted(data, key=lambda e: int(e.get('period', 0)))
    rows = []
    cum_spend = cum_wins = 0.0
    for e in data:
        sp = float(e.get('spend', 0))
        wn = float(e.get('wins', 0))
        cum_spend += sp
        cum_wins += wn
        cum_net = cum_wins - cum_spend
        roi = (wn - sp) / sp * 100 if sp > 0 else (0.0 if wn == 0 else 100.0)
        rows.append({
            "period": int(e.get('period', 0)),
            "spend": round(sp, 2),
            "wins": round(wn, 2),
            "net": round(wn - sp, 2),
            "roi": round(roi, 1),
            "cum_spend": round(cum_spend, 2),
            "cum_wins": round(cum_wins, 2),
            "cum_net": round(cum_net, 2),
        })
    if limit:
        rows = rows[-limit:]
    return rows


def generate_advice():
    """基于真实账本数据，给出分级合理化建议。

    返回 list[(level, text)]，level ∈ lock/info/tip/warn/danger。
    """
    if is_ledger_locked():
        return [("lock", "账本已加密锁定，解锁后才能生成建议。用 --unlock 输入口令。")]
    try:
        data = load_ledger()
    except LedgerLocked:
        return [("lock", "账本已加密锁定，解锁后才能生成建议。")]
    if not data:
        return [("info", "还没有任何记录。从本期开始，把每期花的和中的如实记下来；"
                        "记录 3~5 期后，我就能给你针对性的理性建议。")]
    s = summary()
    b = budget_status()
    rows = period_analysis()
    out = []

    # 1) 负期望本质
    if s['total_spend'] > 0:
        out.append(("warn",
            f"累计净亏 ¥{s['net']:.2f}，实际 ROI {s['roi']:.1f}%，远低于官方返奖率 "
            f"{s['theoretical_return_rate']*100:.0f}%（销售额口径，非单注期望）。这不是运气问题，而是彩票期望为负的数学必然——长期必亏，"
            "任何'下一期能回本'的念头都是赌徒谬误。"))

    # 2) 预算超支 / 临界
    if b['over']:
        out.append(("danger",
            f"本月已花 ¥{b['month_spend']:.2f}，超出上限 ¥{b['monthly_limit']:.2f}。"
            f"建议本月立刻停止购彩，下月重新设定预算后再参与。"))
    elif b['used_pct'] >= 80:
        out.append(("warn",
            f"本月预算已用 {b['used_pct']:.0f}%，仅剩 ¥{b['remaining']:.2f}。"
            f"控制住，别在月末几天超支。"))

    # 3) 追号/加码（后期花费上升但中奖没跟上）
    if len(rows) >= 4:
        half = len(rows) // 2
        early = sum(r['spend'] for r in rows[:half])
        late = sum(r['spend'] for r in rows[half:])
        if early > 0 and late > early * 1.3:
            out.append(("danger",
                "你的投入在近期明显加码（可能在追号、想回本）。这是'沉没成本陷阱'——已经花掉的钱拿不回来，"
                "加码不会提高中奖率，只会让总亏损更大。建议回到固定小额，甚至暂停几期。"))
        # 中奖 stagnation
        late_wins = sum(r['wins'] for r in rows[half:])
        if late > early and late_wins <= early * 0.5:
            out.append(("warn",
                "近期花得更多、中得更少。请停下来：加码不会改变 1/2142万 的头奖概率。"))

    # 4) 期数足够却零像样奖金
    big_win = any(r['wins'] >= 200 for r in rows)
    if s['periods'] >= 5 and not big_win:
        out.append(("warn",
            f"已记录 {s['periods']} 期，未出现像样奖金。一等奖概率约 1/2142万，"
            "绝大多数人长期只中末等奖或不中。把购彩当固定小额娱乐，而非回本手段。"))

    # 5) 正向收尾建议（始终给）
    out.append(("tip",
        f"设定并守住月度预算（当前上限 ¥{b['monthly_limit']:.0f}），只花闲钱；"
        "同等花费下可用合买/覆盖工具覆盖更多不重复组合，但绝不因此加码。"))
    out.append(("tip",
        "把本账本当'消费凭证'而不是'投资账'。若某月净亏让你心里不适，那正是该收手的信号——"
        "需要时可用 --lock 给账本上口令，让它只对你自己可见。"))
    return out


def budget_status(monthly_limit=None):
    if monthly_limit is None:
        monthly_limit = load_budget()["monthly_limit"]
    monthly_limit = float(monthly_limit)
    now = datetime.datetime.now()
    ym = (now.year, now.month)
    try:
        data = load_ledger()
    except LedgerLocked:
        data = []
    month_spend = sum(
        float(e.get('spend', 0)) for e in data
        if _in_month(e.get('date', ''), ym)
    )
    remaining = monthly_limit - month_spend
    over = month_spend > monthly_limit
    return {
        "month": f"{now.year}-{now.month:02d}",
        "monthly_limit": round(monthly_limit, 2),
        "month_spend": round(month_spend, 2),
        "remaining": round(remaining, 2),
        "over": over,
        "used_pct": round(month_spend / monthly_limit * 100, 1) if monthly_limit > 0 else 0.0,
    }


def _in_month(date_str, ym):
    try:
        d = datetime.date.fromisoformat(date_str)
        return (d.year, d.month) == ym
    except Exception:
        return False


def monthly_bill():
    """按自然月聚合的账单汇总。返回按月份升序的列表。

    注: 预算上限仅存一份"当前值"，历史月份的超支判断是用当前上限近似评估的，
    已在导出文本中标注，避免误导。
    """
    data = load_ledger()  # 锁定态会抛 LedgerLocked
    months = {}
    for e in data:
        date_str = e.get('date', '')
        try:
            d = datetime.date.fromisoformat(date_str)
            key = f"{d.year}-{d.month:02d}"
        except Exception:
            key = "未知月份"
        m = months.setdefault(key, {"spend": 0.0, "wins": 0.0, "periods": 0})
        m["spend"] += float(e.get('spend', 0))
        m["wins"] += float(e.get('wins', 0))
        m["periods"] += 1
    limit = load_budget()["monthly_limit"]
    out = []
    for k in sorted(months.keys()):
        sp = months[k]["spend"]
        wn = months[k]["wins"]
        out.append({
            "month": k,
            "periods": months[k]["periods"],
            "spend": round(sp, 2),
            "wins": round(wn, 2),
            "net": round(wn - sp, 2),
            "budget_limit": round(limit, 2),
            "over": sp > limit,
        })
    return out


# ---------------- 报告渲染 ----------------
_LEVEL_BADGE = {
    "lock": ("🔒", "#ffd9a0"), "info": ("ℹ️", "#9fb4ff"),
    "tip": ("💡", "#7ee0a0"), "warn": ("⚠️", "#ffd9a0"), "danger": ("🛑", "#ff8a8a"),
}


def render_ledger_html():
    # 锁定态：不暴露任何数据，仅提示解锁
    if is_ledger_locked():
        return """
<div class="section">
<div class="section-title">📒 诚实账本 & 预算守护（已加密锁定）</div>
<div class="warning"><h3>🔒 账本已用口令加密</h3>
<p>你的账本文件已加密，仅持口令者可见。本报告中不显示任何账目明细。
运行 <code>python3 dlt_ledger.py --unlock</code> 输入口令后，账本分析与建议会重新出现。
数据始终只存本地、不联网、不上传。</p></div>
</div>
"""
    s = summary()
    b = budget_status()
    budget_color = "#ff6b6b" if b["over"] else ("#ffd9a0" if b["used_pct"] >= 80 else "#7ee0a0")
    budget_state = "⚠️ 已超预算，建议本月停止购彩！" if b["over"] else (
        "🟡 接近预算上限，注意控制" if b["used_pct"] >= 80 else "🟢 预算内，保持")
    net_color = "#ff8a8a" if s["net"] < 0 else "#7ee0a0"

    # 逐期表（最近 12 期）
    rows = period_analysis(limit=12)
    period_rows_html = ""
    if rows:
        period_rows_html = (
            '<div style="font-size:12px; color:#9fb4ff; margin:6px 0 2px;">'
            '📊 逐期投入/产出（最近 %d 期）</div>' % len(rows))
        period_rows_html += (
            '<table style="width:100%; border-collapse:collapse; margin:4px 0 8px; font-size:12px;">'
            '<tr style="color:#7e8bbf;">'
            '<td style="padding:4px 6px; border:1px solid #2a3358;">期号</td>'
            '<td style="padding:4px 6px; border:1px solid #2a3358;">花费</td>'
            '<td style="padding:4px 6px; border:1px solid #2a3358;">中奖</td>'
            '<td style="padding:4px 6px; border:1px solid #2a3358;">净亏</td>'
            '<td style="padding:4px 6px; border:1px solid #2a3358;">累计净亏</td></tr>')
        for r in rows:
            nc = "#ff8a8a" if r["net"] < 0 else "#7ee0a0"
            cnc = "#ff8a8a" if r["cum_net"] < 0 else "#7ee0a0"
            period_rows_html += (
                f'<tr><td style="padding:4px 6px; border:1px solid #2a3358; color:#cdd6f4;">{r["period"]}</td>'
                f'<td style="padding:4px 6px; border:1px solid #2a3358; color:#cdd6f4;">¥{r["spend"]:.2f}</td>'
                f'<td style="padding:4px 6px; border:1px solid #2a3358; color:#cdd6f4;">¥{r["wins"]:.2f}</td>'
                f'<td style="padding:4px 6px; border:1px solid #2a3358; color:{nc};">¥{r["net"]:.2f}</td>'
                f'<td style="padding:4px 6px; border:1px solid #2a3358; color:{cnc};">¥{r["cum_net"]:.2f}</td></tr>')
        period_rows_html += '</table>'

    # 月度账单（按自然月聚合）
    mb = monthly_bill()
    monthly_html = ""
    if mb:
        monthly_html = ('<div style="font-size:12px; color:#9fb4ff; margin:8px 0 2px;">'
                        '🗓️ 月度账单汇总（按自然月聚合）</div>')
        monthly_html += (
            '<table style="width:100%; border-collapse:collapse; margin:4px 0 8px; font-size:12px;">'
            '<tr style="color:#7e8bbf;">'
            '<td style="padding:4px 6px; border:1px solid #2a3358;">月份</td>'
            '<td style="padding:4px 6px; border:1px solid #2a3358;">期数</td>'
            '<td style="padding:4px 6px; border:1px solid #2a3358;">花费</td>'
            '<td style="padding:4px 6px; border:1px solid #2a3358;">中奖</td>'
            '<td style="padding:4px 6px; border:1px solid #2a3358;">净亏</td>'
            '<td style="padding:4px 6px; border:1px solid #2a3358;">超预算</td></tr>')
        for m in mb:
            nc = "#ff8a8a" if m["net"] < 0 else "#7ee0a0"
            over_c = "#ff8a8a" if m["over"] else "#7ee0a0"
            over_t = "⚠️ 超" if m["over"] else "—"
            monthly_html += (
                f'<tr><td style="padding:4px 6px; border:1px solid #2a3358; color:#cdd6f4;">{m["month"]}</td>'
                f'<td style="padding:4px 6px; border:1px solid #2a3358; color:#cdd6f4;">{m["periods"]}</td>'
                f'<td style="padding:4px 6px; border:1px solid #2a3358; color:#cdd6f4;">¥{m["spend"]:.2f}</td>'
                f'<td style="padding:4px 6px; border:1px solid #2a3358; color:#cdd6f4;">¥{m["wins"]:.2f}</td>'
                f'<td style="padding:4px 6px; border:1px solid #2a3358; color:{nc};">¥{m["net"]:.2f}</td>'
                f'<td style="padding:4px 6px; border:1px solid #2a3358; color:{over_c};">{over_t}</td></tr>')
        monthly_html += '</table>'

    # 建议
    advices = generate_advice()
    advice_html = '<div style="margin:6px 0 2px; font-size:12px; color:#9fb4ff;">💡 给你的合理化建议</div>'
    advice_html += '<div style="font-size:12.5px; line-height:1.75;">'
    for level, text in advices:
        icon, color = _LEVEL_BADGE.get(level, ("•", "#cdd6f4"))
        advice_html += f'<div style="margin:5px 0; color:{color};"><b>{icon}</b> {text}</div>'
    advice_html += '</div>'

    # 一键导出按钮（纯客户端：无需服务器，点一下即可下载/打印；中文无乱码）
    _txt = build_export_text()
    _html = build_export_html()
    _txt_b64 = base64.b64encode(_txt.encode('utf-8')).decode()
    _html_b64 = base64.b64encode(_html.encode('utf-8')).decode()
    _btn_style = ("display:inline-block; padding:7px 12px; margin:4px 6px 4px 0; border-radius:7px; "
                  "font-size:12.5px; cursor:pointer; text-decoration:none; color:#fff; "
                  "background:linear-gradient(135deg,#5577ff,#7a5cff); border:none;")
    export_btns = (
        '<div style="margin:10px 0 4px;">'
        '<a href="data:text/plain;base64,' + _txt_b64 + '" download="大乐透账本_客户.txt" '
        'style="' + _btn_style + '">⬇ 下载纯文本账单</a>'
        '<a href="data:text/html;base64,' + _html_b64 + '" download="大乐透账本_客户.html" '
        'style="' + _btn_style + '">⬇ 下载 HTML（可打印为 PDF）</a>'
        '<button onclick="dltPrintLedger()" style="' + _btn_style + '">🖨 直接打印为 PDF</button>'
        '</div>'
        '<script>function dltPrintLedger(){'
        'var b64="' + _html_b64 + '";'
        'var h=atob(b64);'
        'var w=window.open("","_blank");'
        'if(!w){alert("请允许浏览器弹出窗口以打印账单");return;}'
        'w.document.open();w.document.write(h);w.document.close();'
        'w.focus();setTimeout(function(){w.print();},350);}'
        '</script>'
    )

    html = f"""
<div class="section">
<div class="section-title">📒 诚实账本 &amp; 预算守护（你的真实盈亏 · 仅你可见）</div>
<div class="info" style="border-color:#5577ff; background:#10122a;">
<p style="color:#aab4ff; font-size:12.5px; line-height:1.8; margin:6px 0;">
这是系统替你记的<b style="color:#ffd9a0;">真实购彩账</b>：花了多少、中了多少、累计净亏，并附逐期分析与建议。
它不预测、不承诺，只把事实摆出来——研究证明，看清真实亏损最能帮人及时收手。
数据仅存你本地、不联网、不上传；可用 <code>--lock</code> 加口令，让它只对你自己可见。
</p>
</div>

<table style="width:100%; border-collapse:collapse; margin:8px 0; font-size:13px;">
  <tr>
    <td style="padding:6px 8px; border:1px solid #2a3358; color:#9fb4ff;">累计期数</td>
    <td style="padding:6px 8px; border:1px solid #2a3358; color:#e6ebff;"><b>{s['periods']}</b> 期</td>
    <td style="padding:6px 8px; border:1px solid #2a3358; color:#9fb4ff;">累计花费</td>
    <td style="padding:6px 8px; border:1px solid #2a3358; color:#e6ebff;"><b>¥{s['total_spend']:.2f}</b></td>
  </tr>
  <tr>
    <td style="padding:6px 8px; border:1px solid #2a3358; color:#9fb4ff;">累计中奖</td>
    <td style="padding:6px 8px; border:1px solid #2a3358; color:#e6ebff;"><b>¥{s['total_wins']:.2f}</b></td>
    <td style="padding:6px 8px; border:1px solid #2a3358; color:#9fb4ff;">累计净亏</td>
    <td style="padding:6px 8px; border:1px solid #2a3358; color:{net_color};"><b>¥{s['net']:.2f}</b></td>
  </tr>
  <tr>
    <td style="padding:6px 8px; border:1px solid #2a3358; color:#9fb4ff;">实际 ROI</td>
    <td style="padding:6px 8px; border:1px solid #2a3358; color:{net_color};"><b>{s['roi']:.1f}%</b></td>
        <td style="padding:6px 8px; border:1px solid #2a3358; color:#9fb4ff;">官方返奖率</td>
        <td style="padding:6px 8px; border:1px solid #2a3358; color:#9fb4ff;"><b>{s['theoretical_return_rate']*100:.0f}%</b>（销售额口径·非单注期望）</td>
  </tr>
</table>
{period_rows_html}
{monthly_html}

<div style="border:1px solid {budget_color}; border-radius:8px; padding:10px 12px; margin:8px 0; background:#10122a;">
  <div style="font-size:13px; font-weight:700; color:{budget_color};">💰 本月预算（{b['month']}）：{budget_state}</div>
  <div style="font-size:12px; color:#c7ccea; line-height:1.8; margin-top:4px;">
    上限 <b>¥{b['monthly_limit']:.0f}</b> ｜ 已花 <b>¥{b['month_spend']:.2f}</b>（{b['used_pct']:.0f}%）
    ｜ 剩余 <b style="color:{budget_color};">¥{b['remaining']:.2f}</b>
  </div>
  <div style="background:#1a2030; border-radius:6px; height:10px; margin-top:6px; overflow:hidden;">
    <div style="width:{min(100, b['used_pct']):.0f}%; height:100%; background:{budget_color};"></div>
  </div>
</div>
{advice_html}

<p style="font-size:11.5px; color:#8fa0c8; line-height:1.7; margin:6px 0 0;">
📌 账本默认在生成预测时按"基本投注"自动记账；开奖后请用
<code>--record-win 期号 金额</code> 回填中奖，用 <code>--entry</code> 手动补记，用 <code>--set-budget 200</code> 调上限，
用 <code>--lock</code> 加口令保护隐私。数据仅存本地，不联网、不上传。
</p>
{export_btns}
</div>
"""
    return html


# ---------------- 导出（纯文本 / HTML 打印版） ----------------
def build_export_text():
    """生成可发给客户的纯文本账单（含总览/预算/月度/逐期/建议）。"""
    s = summary()
    b = budget_status()
    rows = period_analysis()
    mb = monthly_bill()
    advices = generate_advice()
    L = []
    L.append("大乐透 · 诚实账本导出报告")
    L.append("生成时间: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    L.append("=" * 46)
    L.append("【总览】")
    L.append(f"  累计期数 : {s['periods']}")
    L.append(f"  累计花费 : ¥{s['total_spend']:.2f}")
    L.append(f"  累计中奖 : ¥{s['total_wins']:.2f}")
    L.append(f"  累计净亏 : ¥{s['net']:.2f}")
    L.append(f"  实际ROI  : {s['roi']:.1f}%  (官方返奖率 {s['theoretical_return_rate']*100:.0f}%·销售额口径)")
    L.append("")
    L.append(f"【本月预算】 {b['month']}")
    L.append(f"  上限 ¥{b['monthly_limit']:.0f} ｜ 已花 ¥{b['month_spend']:.2f}（{b['used_pct']:.0f}%）｜ 剩余 ¥{b['remaining']:.2f}")
    L.append("  " + ("⚠️ 已超预算，建议本月停止购彩！" if b['over']
                    else ("🟡 接近上限，注意控制" if b['used_pct'] >= 80 else "🟢 预算内，保持")))
    L.append("")
    L.append("【月度账单】")
    L.append(f"  {'月份':<11}{'期数':>5}{'花费':>13}{'中奖':>13}{'净亏':>13}{'超预算':>8}")
    for m in mb:
        L.append(f"  {m['month']:<11}{m['periods']:>5}"
                 f"{'¥'+format(m['spend'], '.2f'):>13}"
                 f"{'¥'+format(m['wins'], '.2f'):>13}"
                 f"{'¥'+format(m['net'], '.2f'):>13}"
                 f"{('⚠超' if m['over'] else '—'):>8}")
    L.append("  （注：历史月份超支按当前预算上限 ¥%.0f 近似评估）" % b['monthly_limit'])
    L.append("")
    L.append("【逐期投入/产出】")
    L.append(f"  {'期号':<9}{'花费':>11}{'中奖':>11}{'净亏':>11}{'累计净亏':>13}")
    for r in rows:
        L.append(f"  {r['period']:<9}{'¥'+format(r['spend'], '.2f'):>11}"
                 f"{'¥'+format(r['wins'], '.2f'):>11}"
                 f"{'¥'+format(r['net'], '.2f'):>11}"
                 f"{'¥'+format(r['cum_net'], '.2f'):>13}")
    L.append("")
    L.append("【给你的合理化建议】")
    for level, text in advices:
        icon, _ = _LEVEL_BADGE.get(level, ("•", ""))
        L.append(f"  {icon} {text}")
    L.append("")
    L.append("=" * 46)
    L.append("数据仅存本地、不联网、不上传。本账本与建议不预测、不承诺中奖；")
    L.append("彩票期望为负，请把购彩当小额娱乐，量力而行。")
    return "\n".join(L)


def build_export_html():
    """生成自包含 HTML（浏览器打开后 Ctrl/Cmd+P → 另存为 PDF，中文无乱码）。"""
    s = summary()
    b = budget_status()
    rows = period_analysis()
    mb = monthly_bill()
    advices = generate_advice()
    net_c = "#b00020" if s["net"] < 0 else "#1b7f3b"
    budget_c = "#b00020" if b["over"] else ("#b8860b" if b["used_pct"] >= 80 else "#1b7f3b")

    def adv_block():
        out = []
        for level, text in advices:
            icon, color = _LEVEL_BADGE.get(level, ("•", "#333"))
            out.append(f'<div style="margin:6px 0; color:{color};"><b>{icon}</b> {text}</div>')
        return "\n".join(out)

    def period_table():
        out = ['<table class="t"><tr><th>期号</th><th>花费</th><th>中奖</th><th>净亏</th><th>累计净亏</th></tr>']
        for r in rows:
            nc = "#b00020" if r["net"] < 0 else "#1b7f3b"
            cnc = "#b00020" if r["cum_net"] < 0 else "#1b7f3b"
            out.append(f'<tr><td>{r["period"]}</td><td>¥{r["spend"]:.2f}</td><td>¥{r["wins"]:.2f}</td>'
                       f'<td style="color:{nc}">¥{r["net"]:.2f}</td><td style="color:{cnc}">¥{r["cum_net"]:.2f}</td></tr>')
        out.append('</table>')
        return "\n".join(out)

    def monthly_table():
        if not mb:
            return '<p style="color:#666">暂无月度数据。</p>'
        out = ['<table class="t"><tr><th>月份</th><th>期数</th><th>花费</th><th>中奖</th><th>净亏</th><th>超预算</th></tr>']
        for m in mb:
            nc = "#b00020" if m["net"] < 0 else "#1b7f3b"
            oc = "#b00020" if m["over"] else "#1b7f3b"
            out.append(f'<tr><td>{m["month"]}</td><td>{m["periods"]}</td><td>¥{m["spend"]:.2f}</td>'
                       f'<td>¥{m["wins"]:.2f}</td><td style="color:{nc}">¥{m["net"]:.2f}</td>'
                       f'<td style="color:{oc}">{"⚠ 超" if m["over"] else "—"}</td></tr>')
        out.append('</table>')
        return "\n".join(out)

    _budget_state = ("⚠️ 已超预算，建议本月停止购彩！" if b["over"]
                     else ("🟡 接近上限，注意控制" if b["used_pct"] >= 80 else "🟢 预算内，保持"))
    html = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>大乐透诚实账本 · 客户账单</title>
<style>
  body {{ font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", sans-serif; color:#222; margin:32px; }}
  h1 {{ font-size:22px; border-bottom:3px solid #5577ff; padding-bottom:8px; }}
  h2 {{ font-size:16px; margin-top:24px; color:#334; border-left:5px solid #5577ff; padding-left:8px; }}
  .t {{ width:100%; border-collapse:collapse; margin:8px 0; font-size:13px; }}
  .t th, .t td {{ border:1px solid #cdd; padding:5px 8px; text-align:left; }}
  .t th {{ background:#eef1ff; }}
  .card {{ border:1px solid #ccd; border-radius:8px; padding:10px 14px; margin:8px 0; background:#fafbff; }}
  .grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:6px 24px; font-size:14px; }}
  .note {{ color:#778; font-size:12px; }}
  @media print {{ body {{ margin:12mm; }} h2 {{ page-break-after:avoid; }} }}
</style></head>
<body>
<h1>📒 大乐透诚实账本 · 客户账单</h1>
<p class="note">生成时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ｜ 数据仅存本地、不联网、不上传</p>

<h2>一、总览</h2>
<div class="card grid">
  <div>累计期数：<b>{s['periods']}</b></div>
  <div>累计花费：<b>¥{s['total_spend']:.2f}</b></div>
  <div>累计中奖：<b>¥{s['total_wins']:.2f}</b></div>
  <div>累计净亏：<b style="color:{net_c}">¥{s['net']:.2f}</b></div>
  <div>实际 ROI：<b style="color:{net_c}">{s['roi']:.1f}%</b></div>
  <div>官方返奖率：<b>{s['theoretical_return_rate']*100:.0f}%</b>（销售额口径·非单注期望）</div>
</div>

<h2>二、本月预算（{b['month']}）</h2>
<div class="card">
  <div style="color:{budget_c}; font-weight:700;">💰 {_budget_state}</div>
  <div class="note" style="margin-top:4px;">上限 ¥{b['monthly_limit']:.0f} ｜ 已花 ¥{b['month_spend']:.2f}（{b['used_pct']:.0f}%）｜ 剩余 ¥{b['remaining']:.2f}</div>
  <div style="background:#eee; border-radius:6px; height:10px; margin-top:6px; overflow:hidden;">
    <div style="width:{min(100, b['used_pct']):.0f}%; height:100%; background:{budget_c};"></div>
  </div>
</div>

<h2>三、月度账单汇总</h2>
{monthly_table()}
<p class="note">注：历史月份超支按当前预算上限 ¥{b['monthly_limit']:.0f} 近似评估。</p>

<h2>四、逐期投入 / 产出</h2>
{period_table()}

<h2>五、给你的合理化建议</h2>
<div class="card">
{adv_block()}
</div>

<p class="note" style="margin-top:24px; border-top:1px solid #ddd; padding-top:8px;">
本账本与建议不预测、不承诺中奖。彩票期望为负，请把购彩当小额娱乐，量力而行。
如需 PDF：浏览器打开本页 → 打印（Ctrl/Cmd+P）→ 另存为 PDF。
</p>
</body></html>"""
    return html


def export_report(path_prefix="dlt_ledger_export"):
    """导出为 .txt（纯文本）与 .html（可打印为PDF）。返回 (txt_path, html_path)。

    锁定态抛 LedgerLocked，由调用方提示先解锁。
    """
    if is_ledger_locked():
        raise LedgerLocked("账本已加密锁定，请先用 --unlock 解锁后再导出。")
    txt = build_export_text()
    html = build_export_html()
    txt_path = path_prefix + ".txt"
    html_path = path_prefix + ".html"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(txt)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return txt_path, html_path


# ---------------- 交互式记账 ----------------
def _suggest_period():
    """尽力推断当前/下一期号（无依赖时回退到空串由用户手填）。"""
    try:
        from dlt_period import next_period
        return str(next_period())
    except Exception:
        return ""


def interactive_entry():
    print("=" * 40)
    print("  大乐透诚实账本 · 手动记账")
    print("  信息仅存你本地，可随时 --lock 加口令")
    print("=" * 40)
    sug = _suggest_period()
    period = input(f"期号（如 {sug or '26092'}，回车用 {sug or '空'}）: ").strip() or sug
    if not period:
        print("✗ 未期间号，已取消。")
        return
    spend_s = input("本期花费（元，如 10）：").strip()
    try:
        spend = float(spend_s) if spend_s else 0.0
    except ValueError:
        print("✗ 花费格式错误，已取消。")
        return
    wins_s = input("本期中奖（元，无则直接回车）：").strip()
    try:
        wins = float(wins_s) if wins_s else 0.0
    except ValueError:
        print("✗ 中奖格式错误，已取消。")
        return
    note = input("备注（可选，如 机选/自填）：").strip()
    if is_ledger_locked():
        print("✗ 账本已锁定，请先 --unlock 再记账。")
        return
    e = record_spend(period, spend, note or "manual: 客户自填")
    if wins > 0:
        record_win(period, wins)
        print(f"✓ 已记录 期{period}：花费 ¥{spend:.2f}，中奖 ¥{wins:.2f}")
    else:
        print(f"✓ 已记录 期{period}：花费 ¥{spend:.2f}")


# ---------------- CLI ----------------
def main():
    import argparse
    ap = argparse.ArgumentParser(description="大乐透诚实账本/预算守护（私密·非预测）")
    ap.add_argument("--record-spend", nargs=2, metavar=("PERIOD", "AMOUNT"), help="记录某期花费")
    ap.add_argument("--record-win", nargs=2, metavar=("PERIOD", "AMOUNT"), help="回填某期中奖")
    ap.add_argument("--entry", action="store_true", help="交互式手动记账（客户自填）")
    ap.add_argument("--set-budget", type=float, metavar="MONTHLY_LIMIT", help="设置月度预算上限(元)")
    ap.add_argument("--summary", action="store_true", help="打印账本汇总")
    ap.add_argument("--analysis", action="store_true", help="打印逐期投入/产出分析")
    ap.add_argument("--advice", action="store_true", help="打印合理化建议")
    ap.add_argument("--budget", action="store_true", help="打印预算状态")
    ap.add_argument("--monthly", action="store_true", help="打印月度账单汇总（按自然月聚合）")
    ap.add_argument("--export", nargs="?", const="dlt_ledger_export", metavar="PATH",
                    help="一键导出：生成 PATH.txt(纯文本) 与 PATH.html(可打印为PDF)，默认 dlt_ledger_export")
    ap.add_argument("--lock", nargs="?", const="__ASK__", metavar="PASSPHRASE",
                    help="用口令加密账本（仅持口令可见；留空则交互输入）")
    ap.add_argument("--unlock", nargs="?", const="__ASK__", metavar="PASSPHRASE",
                    help="用口令解密账本（留空则交互输入）")
    args = ap.parse_args()

    # 锁定/解锁优先
    if args.lock is not None:
        if is_ledger_locked():
            print("✗ 账本已处于锁定状态，无需重复锁定。如需更换口令，先 --unlock 再 --lock。")
        else:
            pw = args.lock if args.lock != "__ASK__" else getpass.getpass("设置账本口令: ")
            if not pw:
                print("✗ 口令为空，已取消。")
            else:
                n = lock_ledger(pw)
                print(f"🔒 已用口令加密账本（{n} 条记录）。口令遗忘无法找回，请牢记。")
        return
    if args.unlock is not None:
        if not is_ledger_locked():
            print("ℹ️ 账本未锁定，无需解锁。")
        else:
            pw = args.unlock if args.unlock != "__ASK__" else getpass.getpass("输入账本口令: ")
            try:
                data = unlock_ledger(pw)
                print(f"🔓 已解锁，恢复 {len(data)} 条记录为本地明文。")
            except Exception:
                print("✗ 口令错误，解锁失败。")
        return

    if args.entry:
        interactive_entry()
        return

    if args.record_spend:
        p, a = args.record_spend
        try:
            e = record_spend(p, float(a))
            print(f"✓ 已记录花费: 期{p} = ¥{float(a):.2f} (note={e['note']})")
        except LedgerLocked as e:
            print(f"✗ {e}")
    if args.record_win:
        p, a = args.record_win
        try:
            e = record_win(p, float(a))
            print(f"✓ 已回填中奖: 期{p} = ¥{float(a):.2f}")
        except LedgerLocked as e:
            print(f"✗ {e}")
    if args.set_budget is not None:
        b = load_budget()
        b["monthly_limit"] = float(args.set_budget)
        save_budget(b)
        print(f"✓ 月度预算上限已设为 ¥{b['monthly_limit']:.2f}")
    if args.summary:
        try:
            print(json.dumps(summary(), ensure_ascii=False, indent=2))
        except LedgerLocked as e:
            print(f"✗ {e}")
    if args.analysis:
        try:
            print(json.dumps(period_analysis(), ensure_ascii=False, indent=2))
        except LedgerLocked as e:
            print(f"✗ {e}")
    if args.advice:
        for level, text in generate_advice():
            icon, _ = _LEVEL_BADGE.get(level, ("•", ""))
            print(f"{icon} [{level}] {text}")
    if args.budget:
        print(json.dumps(budget_status(), ensure_ascii=False, indent=2))
    if args.monthly:
        try:
            mb = monthly_bill()
            print(f"{'月份':<11}{'期数':>5}{'花费':>13}{'中奖':>13}{'净亏':>13}{'超预算':>8}")
            for m in mb:
                print(f"{m['month']:<11}{m['periods']:>5}"
                      f"{'¥'+format(m['spend'], '.2f'):>13}"
                      f"{'¥'+format(m['wins'], '.2f'):>13}"
                      f"{'¥'+format(m['net'], '.2f'):>13}"
                      f"{('⚠超' if m['over'] else '—'):>8}")
        except LedgerLocked as e:
            print(f"✗ {e}")
    if args.export:
        try:
            txt_path, html_path = export_report(args.export)
            print(f"✓ 已导出纯文本: {txt_path}")
            print(f"✓ 已导出 HTML(可打印为PDF): {html_path}")
            print("  → 双击 .html 用浏览器打开，Ctrl/Cmd+P → 另存为 PDF 即可得到中文无乱码的客户账单。")
        except LedgerLocked as e:
            print(f"✗ {e}")
    if not (args.record_spend or args.record_win or args.set_budget or args.summary
            or args.analysis or args.advice or args.budget or args.monthly
            or args.export or args.entry):
        print(render_ledger_html())


if __name__ == '__main__':
    main()
