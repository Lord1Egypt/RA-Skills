#!/usr/bin/env python3
"""A股数据API - OpenClaw Skill 调用脚本"""
import json
import sys
import urllib.request
import urllib.error

API_HOST = "https://api.jyfg.de5.net:2096"
DEFAULT_TOKEN = "admin_mllx_2026"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def call_api(endpoint, code, token=DEFAULT_TOKEN):
    """调用API接口"""
    url = f"{API_HOST}/v1/{endpoint}?code={code}&token={token}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}", "detail": body}
    except Exception as e:
        return {"error": str(e)}


def format_quote(data):
    """格式化行情输出"""
    name = data.get("name", "")
    price = data.get("最新价", "")
    change = data.get("涨跌幅", "")
    vol = data.get("成交量", "")
    amt = data.get("成交额", "")
    turn = data.get("换手率", "")
    pe = data.get("市盈率", "")
    pb = data.get("市净率", "")
    mcap = data.get("总市值", "")

    lines = [
        f"📊 {name} 实时行情",
        f"价格: {price}  涨跌: {change}%",
        f"成交: {_fmt_num(vol)}股  金额: {_fmt_num(amt)}",
        f"换手: {turn}%  PE: {pe}  PB: {pb}",
    ]
    if mcap:
        lines.append(f"总市值: {_fmt_num(mcap)}")
    return "\n".join(lines)


def format_flow(data):
    """格式化资金流向输出"""
    lines = ["💰 资金流向"]
    for k, v in data.items():
        if k in ("code", "name", "source", "cost_s"):
            continue
        clean = k.replace("(区间)", "").strip()
        if clean:
            lines.append(f"  {clean}: {v}")
    return "\n".join(lines)


def format_finance(data):
    """格式化财务数据输出"""
    lines = ["📋 财务数据"]
    for k, v in data.items():
        if k in ("code", "name", "source", "cost_s", "date"):
            continue
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)


def format_kline(data):
    """格式化K线数据"""
    lines = ["📈 K线技术指标"]
    for k, v in data.items():
        if k in ("code", "name", "source", "cost_s"):
            continue
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)


def _fmt_num(n):
    """格式化大数字"""
    try:
        n = float(n)
        if n >= 1e12:
            return f"{n/1e12:.2f}万亿"
        elif n >= 1e8:
            return f"{n/1e8:.2f}亿"
        elif n >= 1e4:
            return f"{n/1e4:.2f}万"
        return f"{n:.2f}"
    except (ValueError, TypeError):
        return str(n)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 astock_api.py <端点> <股票代码> [token]")
        print("端点: quote, kline, flow, finance, valuation, concept")
        print("示例: python3 astock_api.py quote 600519")
        sys.exit(1)

    endpoint = sys.argv[1]
    code = sys.argv[2]
    token = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_TOKEN

    result = call_api(endpoint, code, token)

    if "error" in result:
        print(f"❌ 错误: {result['error']}")
        sys.exit(1)

    formatters = {
        "quote": format_quote,
        "kline": format_kline,
        "flow": format_flow,
        "finance": format_finance,
        "valuation": format_finance,
        "concept": lambda d: f"📌 所属概念: {json.dumps(d.get('所属概念', d), ensure_ascii=False, indent=2)}",
    }

    fmt = formatters.get(endpoint, lambda d: json.dumps(d, ensure_ascii=False, indent=2))
    print(fmt(result))
    print(f"\n⏱ 耗时: {result.get('cost_s', '?')}s  来源: {result.get('source', '?')}")
