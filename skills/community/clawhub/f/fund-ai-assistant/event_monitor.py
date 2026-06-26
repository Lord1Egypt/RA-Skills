#!/usr/bin/env python3
"""
宏观事件监控系统 v1.0
监控4类触发条件，生成推送报告

触发条件：
  1. 沪深300单日涨跌幅 > 2%
  2. 人民币汇率破7.15 / 7.25 / 7.3（三级预警）
  3. 美联储FOMC会议（会前一天提醒 + 会后当天分析）
  4. LPR利率调整（辅助验证，与FOMC信号联动）

推送渠道（通过环境变量配置，详见 push() 函数）：
  PUSH_WEBHOOK_URL  企业微信/飞书/Slack等通用Webhook
  BARK_PUSH_URL     Bark iOS通知
  PUSH_EMAIL         SMTP邮件（需配 SMTP_USER/PASS）
  QQ_WEBHOOK_URL    QQ机器人（go-cqhttp / Lagrange等）
  （均未配置时由 OpenClaw cron agent 读取 stdout 推送）

使用方式:
  python3 event_monitor.py                  # 全量检查
  python3 event_monitor.py --fomc           # 仅FOMC检查
  python3 event_monitor.py --沪深300         # 仅A股预警
  python3 event_monitor.py --汇率           # 仅汇率预警
  python3 event_monitor.py --lpr            # 仅LPR检查
  python3 event_monitor.py --dry-run         # 模拟触发，不推送
"""

import json
import sys
import os
import re
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple

# ============ 通用推送函数（方案A）============
# 优先级：WEBHOOK > BARK > EMAIL > QQ_WEBHOOK > STDOUT
# 环境变量配置，无需修改代码

def _push_webhook(url: str, message: str) -> bool:
    """POST到任意webhook URL（支持企业微信/飞书/Slack/自定义等）"""
    try:
        data = json.dumps({"content": message}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"[WARN] Webhook推送失败: {e}")
        return False


def _push_bark(url: str, message: str) -> bool:
    """推送到 Bark（iOS 通知）"""
    try:
        import urllib.parse
        encoded = urllib.parse.quote(message)
        bark_url = f"{url}/{encoded}"
        req = urllib.request.Request(bark_url, method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"[WARN] Bark推送失败: {e}")
        return False


def _push_email(to_addr: str, subject: str, message: str) -> bool:
    """通过 SMTP 发送邮件"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header

        smtp_host = os.environ.get("SMTP_HOST", "smtp.qq.com")
        smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        smtp_user = os.environ.get("SMTP_USER", "")
        smtp_pass = os.environ.get("SMTP_PASS", "")

        if not smtp_user or not smtp_pass:
            print("[WARN] SMTP_USER/SMTP_PASS 未配置，邮件推送跳过")
            return False

        msg = MIMEText(message, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = smtp_user
        msg["To"] = to_addr

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [to_addr], msg.as_string())
        return True
    except Exception as e:
        print(f"[WARN] 邮件推送失败: {e}")
        return False


def _push_qq_webhook(url: str, message: str) -> bool:
    """通过 HTTP POST 推送到 QQ（兼容 go-cqhttp / Lagrange 等）"""
    try:
        data = json.dumps({
            "group_id": None,
            "message": message,
        }).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"[WARN] QQ推送失败: {e}")
        return False


def push(message: str, subject: str = "宏观事件监控"):
    """
    通用推送入口（方案A）
    按以下环境变量优先级执行：
      1. PUSH_WEBHOOK_URL    → HTTP POST 到指定URL（最通用）
      2. BARK_PUSH_URL       → Bark iOS通知
      3. PUSH_EMAIL          → SMTP邮件
      4. QQ_WEBHOOK_URL      → QQ机器人（go-cqhttp / Lagrange等）
      5. （未配置任何渠道）   → 静默（不报错）
    """
    # 1. Webhook（最通用，企业微信/飞书/Slack/自定义都支持）
    webhook = os.environ.get("PUSH_WEBHOOK_URL", "").strip()
    if webhook:
        ok = _push_webhook(webhook, message)
        print(f"[INFO] Webhook推送 {'成功' if ok else '失败'}")
        return

    # 2. Bark
    bark = os.environ.get("BARK_PUSH_URL", "").strip()
    if bark:
        ok = _push_bark(bark, message)
        print(f"[INFO] Bark推送 {'成功' if ok else '失败'}")
        return

    # 3. Email
    email_to = os.environ.get("PUSH_EMAIL", "").strip()
    if email_to:
        ok = _push_email(email_to, subject, message)
        print(f"[INFO] 邮件推送 {'成功' if ok else '失败'}")
        return

    # 4. QQ（通过QQ机器人HTTP接口）
    qq_webhook = os.environ.get("QQ_WEBHOOK_URL", "").strip()
    if qq_webhook:
        ok = _push_qq_webhook(qq_webhook, message)
        print(f"[INFO] QQ推送 {'成功' if ok else '失败'}")
        return

    # 5. 无渠道配置：静默跳过（不打印，避免cron输出干扰）
    # 推送内容仍会通过 stdout→OpenClaw agent→消息通道传达
    pass

# 汇率预警阈值（简化版）
# 原理：免费API数据为央行官方价估算，可靠触发范围有限
# 设定估算价 >= 7.25 才触发危险级预警
# 估算价在 7.10-7.25 之间仅显示观察状态，不发推送
FOREX_ALERT_THRESHOLD = 7.25   # 危险级触发阈值（估算市场价）
FOREX_OBSERVE_LEVEL  = 7.10   # 观察级阈值（仅显示，不推送）

# 沪深300预警阈值
CSI300_THRESHOLD = 2.0  # 百分比

# FOMC 2026年会议日期（来源：美联储官方日历）
FOMC_2026_DATES = [
    "2026-01-28",  # (已过)
    "2026-03-17",  # (已过)
    "2026-05-05",  # 
    "2026-06-16",
    "2026-07-28",
    "2026-09-15",
    "2026-11-03",
    "2026-12-15",
]

# ============ 数据获取 ============

def fetch_usd_cny() -> Tuple[Optional[float], str]:
    """
    获取美元兑人民币市场汇率（USDCNY）
    返回: (汇率值, 数据质量标签)
    质量标签: "market"=市场实时价 / "official"=央行官方价(仅供参考) / "unknown"=无法判断
    使用标准库 urllib，无第三方依赖
    """
    # ===== 策略1: 通过 Tavily 实时搜索获取市场汇率 =====
    tavily_key = os.environ.get("TAVILY_API_KEY", "").strip()
    if not tavily_key:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        try:
            with open(config_path) as f:
                cfg = json.load(f)
                tavily_key = cfg.get("tavily_api_key", "") or ""
        except Exception:
            pass

    if tavily_key:
        try:
            tv_data_raw = json.dumps({
                "api_key": tavily_key,
                "query": "USD CNY exchange rate today latest",
                "max_results": 3,
                "include_answer": True,
            }).encode("utf-8")
            tv_req = urllib.request.Request(
                "https://api.tavily.com/search",
                data=tv_data_raw,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(tv_req, timeout=10) as tv_response:
                tv_data = json.loads(tv_response.read().decode("utf-8"))
            answer = tv_data.get("answer", "")
            m = re.search(r'7\.\d{3,4}', answer)
            if m:
                market_rate = float(m.group(0))
                if 7.0 <= market_rate <= 7.6:
                    print(f"[INFO] Tavily 市场汇率: {market_rate}")
                    return market_rate, "market"
        except Exception as e:
            print(f"[WARN] Tavily 汇率获取失败: {e}")

    # ===== 策略2: 免费 API（返回央行官方中间价，需标注） =====
    rates = []
    try:
        r1 = urllib.request.urlopen(
            urllib.request.Request(
                "https://api.frankfurter.app/latest?from=USD&to=CNY",
                headers={"User-Agent": "Mozilla/5.0"},
            ),
            timeout=8,
        )
        d = json.loads(r1.read().decode("utf-8"))
        if "rates" in d and "CNY" in d["rates"]:
            rates.append(("frankfurter", d["rates"]["CNY"]))
    except Exception as e:
        print(f"[WARN] frankfurter失败: {e}")

    try:
        r2 = urllib.request.urlopen(
            urllib.request.Request(
                "https://open.er-api.com/v6/latest/USD",
                headers={"User-Agent": "Mozilla/5.0"},
            ),
            timeout=8,
        )
        d = json.loads(r2.read().decode("utf-8"))
        if d.get("result") == "success" and "rates" in d:
            rates.append(("er-api", d["rates"].get("CNY", 0)))
    except Exception as e:
        print(f"[WARN] exchangerate-api失败: {e}")

    if not rates:
        return None, "unknown"

    avg_rate = sum(r for _, r in rates) / len(rates)

    # ===== 数据质量判断 =====
    # PBOC 官方中间价区间大致在 6.80-7.00
    # 市场汇率（USDCNY离岸）区间大致在 7.00-7.40
    # 如果免费API返回 < 7.05，很可能是央行官方价，不是市场实时价
    if avg_rate < 7.05:
        # 官方价，需要加上市场与官方的正常溢价来估算市场价
        # 近年来官方与市场价差通常在 0-5%，取中间值估算
        estimated_market = avg_rate * 1.035  # 估算市场汇率
        print(f"[WARN] 数据为央行官方价({avg_rate:.4f})，估算市场汇率≈{estimated_market:.4f}")
        return estimated_market, "official"
    else:
        return avg_rate, "market"


def fetch_csi300_change() -> Optional[float]:
    """获取沪深300当日涨跌幅（%）"""
    try:
        # 腾讯财经 沪深300 实时行情
        url = "https://qt.gtimg.cn/q=sh000300"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://gu.qq.com"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            text = resp.read().decode("gbk", errors="replace")
        # 格式: v_sh000300="1~沪深300~000300~4440.79~4478.91~4492.85~168321705~..."
        # 位置: 1=名称, 2=代码, 3=当前, 4=昨收, 5=今开, 6=成交量...
        m = re.search(r'v_sh000300="([^"]+)"', text)
        if m:
            parts = m.group(1).split("~")
            if len(parts) >= 4:
                current = float(parts[3])
                prev_close = float(parts[4])
                if prev_close > 0:
                    change_pct = (current - prev_close) / prev_close * 100
                    return change_pct
    except Exception as e:
        print(f"[ERROR] 获取沪深300失败: {e}")
    return None


def fetch_lpr() -> Optional[dict]:
    """获取最新LPR利率（含历史对比）"""
    # LPR具体数值（每月20日公布）从央行公告获取
    # 此处通过监控USDCNY市场汇率间接反映LPR传导效果
    # LPR降息→人民币贬值压力↑ → USDCNY↑
    # 该函数保留用于未来接入LPR官方API
    return None


# ============ 条件判断 ============

def check_forex() -> Tuple[bool, str]:
    """
    检查人民币汇率（简化版：单一阈值触发）
    策略：估算市场价 >= 7.25 才触发危险级预警
          估算市场价 >= 7.10 显示观察状态，不发推送
    """
    rate, quality = fetch_usd_cny()
    if rate is None or quality == "unknown":
        return False, ""

    # 数据质量标注
    quality_label = "✅市场实时" if quality == "market" else "⚠️官方价估算"

    if rate >= FOREX_ALERT_THRESHOLD:
        # ===== 触发危险级预警 =====
        msg = (
            f"🔴 【汇率危险级预警】USD/CNY≈{rate:.4f}（{quality_label}）\n"
            f"   跟你有没有关系：直接影响债券基金和黄金ETF的估值！\n"
            f"   人民币贬值→外资流出→债券承压；黄金以USD计价→相对变贵\n"
            f"   我的判断：已达危险区间，建议等待2-3天确认趋势后再决策\n"
            f"   不确定的地方：估算值与真实市场价可能有0.1元误差\n"
            f"   ⚠️ 不要在恐慌时赎回债券！"
        )
        return True, msg
    elif rate >= FOREX_OBSERVE_LEVEL:
        # ===== 观察状态（不发推送，只在报告中显示）=====
        msg = (
            f"🟡 【汇率观察中】USD/CNY≈{rate:.4f}（{quality_label}）\n"
            f"   跟你有没有关系：暂时影响有限，但开始留意\n"
            f"   提示：当前为估算值，真实市场价可能有偏差，仅供参考"
        )
        return False, msg  # 不触发推送，但返回内容供报告使用
    else:
        # ===== 正常 =====
        return False, f"✅ 人民币汇率正常：USD/CNY≈{rate:.4f}（{quality_label}）"


def check_csi300() -> Tuple[bool, str]:
    """检查沪深300单日涨跌幅"""
    change = fetch_csi300_change()
    if change is None:
        return False, ""

    abs_change = abs(change)
    direction = "暴涨" if change > 0 else "暴跌"
    emoji = "📈" if change > 0 else "📉"

    if abs_change > CSI300_THRESHOLD:
        if change > 0:
            msg = (
                f"{emoji}【警报·沪深300{direction} {change:+.2f}%】\n"
                f"   跟你有没有关系：直接影响混合型基金的涨跌！\n"
                f"   做什么：不要在上涨时追入！大涨后往往有回调\n"
                f"   建议：持有不动，等情绪稳定"
            )
        else:
            msg = (
                f"{emoji}【警报·沪深300{direction} {change:+.2f}%】\n"
                f"   跟你有没有关系：直接影响混合型基金的涨跌！\n"
                f"   做什么：不要在恐慌时赎回！不要动，等反弹\n"
                f"   ⚠️ 损失厌恶是人类本能，但逆向操作才能赚钱"
            )
        return True, msg
    else:
        return False, f"✅ 沪深300今日{change:+.2f}%（未触发±2%预警线）"


def check_fomc() -> Tuple[bool, str, List[str]]:
    """
    检查FOMC状态
    返回: (是否有FOMC相关, 报告, 待执行操作列表)
    """
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")

    events = []
    actions = []

    for fomc_date in FOMC_2026_DATES:
        if fomc_date == today:
            events.append(("today", f"🎯 今天美联储FOMC公布利率决议"))
            actions.append("run_analysis")
        elif fomc_date == tomorrow:
            events.append(("tomorrow", f"📋 明天美联储FOMC会议（关注利率决议）"))
            actions.append("pre_warning")
        elif fomc_date == yesterday:
            events.append(("yesterday", f"📊 昨日美联储FOMC会议结果请关注"))

    if not events:
        # 找最近的会议
        past = [d for d in FOMC_2026_DATES if d < today]
        future = [d for d in FOMC_2026_DATES if d > today]
        nearest = future[0] if future else (past[-1] if past else None)
        if nearest:
            nd = datetime.strptime(nearest, "%Y-%m-%d")
            days_diff = (nd - now).days
            if days_diff <= 14:
                events.append(("upcoming", f"📅 {days_diff}天后美联储FOMC会议（{nearest}）"))

    if not events:
        return False, f"✅ 近期无FOMC会议", []

    lines = ["【美联储FOMC动态】"]
    lines.extend([e[1] for e in events])

    if any(e[0] in ("today", "tomorrow") for e in events):
        lines.append("跟你有没有关系：直接影响黄金ETF、债券基金和QDII基金")
        if any(e[0] == "today" for e in events):
            lines.append("建议：今晚不要操作，等明日消化后再判断")
        else:
            lines.append("建议：可提前关注，但不要因为预期提前操作")

    return True, "\n".join(lines), actions


def check_lpr(lpr_data: Optional[dict]) -> Tuple[bool, str]:
    """检查LPR是否有调整"""
    if not lpr_data:
        return False, ""

    changed = []
    if lpr_data.get("1y_prev") and lpr_data["1y"] != lpr_data["1y_prev"]:
        diff = lpr_data["1y"] - lpr_data["1y_prev"]
        direction = "下调" if diff < 0 else "上调"
        changed.append(f"1年期LPR{direction}{abs(diff):.2f}%（{lpr_data['1y_prev']}%→{lpr_data['1y']}%）")

    if lpr_data.get("5y_prev") and lpr_data["5y"] != lpr_data["5y_prev"]:
        diff = lpr_data["5y"] - lpr_data["5y_prev"]
        direction = "下调" if diff < 0 else "上调"
        changed.append(f"5年期LPR{direction}{abs(diff):.2f}%（{lpr_data['5y_prev']}%→{lpr_data['5y']}%）")

    if changed:
        msg = (
            f"🏦 【LPR利率调整】{' '.join(changed)}\n"
            f"   跟你有没有关系：LPR下调→债券利好；LPR上调→债券承压\n"
            f"   建议：结合当前FOMC周期判断，孤立一次LPR调整影响有限"
        )
        return True, msg

    return False, ""


# ============ 主流程 ============

def main():
    args = sys.argv[1:]
    is_dry_run = "--dry-run" in args
    specific_check = None
    for flag in ["--fomc", "--沪深300", "--汇率", "--lpr"]:
        if flag in args:
            specific_check = flag.replace("--", "")
            break

    reports = []
    triggered_count = 0

    # 1. 沪深300检查
    if specific_check in [None, "沪深300"]:
        triggered, report = check_csi300()
        if report:
            reports.append(report)
            if triggered:
                triggered_count += 1
        elif specific_check == "沪深300":
            reports.append("⚠️ 暂无法获取沪深300数据")

    # 2. 汇率检查
    if specific_check in [None, "汇率"]:
        triggered, report = check_forex()
        if report:
            reports.append(report)
            if triggered:
                triggered_count += 1
        elif specific_check == "汇率":
            reports.append("⚠️ 暂无法获取汇率数据")

    # 3. FOMC检查
    if specific_check in [None, "fomc"]:
        triggered, report, actions = check_fomc()
        if report:
            reports.append(report)
            if triggered:
                triggered_count += 1
        elif specific_check == "fomc":
            reports.append("✅ 近期无FOMC相关事件")

    # 4. LPR检查
    if specific_check in [None, "lpr"]:
        lpr_data = fetch_lpr()
        triggered, report = check_lpr(lpr_data)
        if report:
            reports.append(report)
            if triggered:
                triggered_count += 1
        elif specific_check == "lpr":
            reports.append("⚠️ 暂无法获取LPR数据")

    # 组装输出
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    output = [f"📊 宏观事件监控报告 | {now_str}", ""]
    output.extend(reports)
    output.append("")
    output.append(f"[{triggered_count}项触发 | dry-run模式]" if is_dry_run else f"[{triggered_count}项触发]")

    full_report = "\n".join(output)
    print(full_report)

    # 推送：有危险级触发时执行通用推送（方案A）
    # dry-run 模式跳过推送
    if is_dry_run:
        print("\n[dry-run] 未执行推送")
        return

    if triggered_count > 0:
        print(f"\n[{triggered_count}项触发，执行推送...]")
        push(full_report, subject=f"宏观预警 {triggered_count}项触发")
    else:
        # 无触发时也打印（OpenClaw cron agent 读取 stdout）
        pass


if __name__ == "__main__":
    main()
