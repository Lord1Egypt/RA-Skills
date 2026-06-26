#!/usr/bin/env python3
"""
基金实盘交易命令行工具 - OAuth 2.0 版本

Usage:
    fund-trading.py register [--username NAME]
    fund-trading.py account [--list] [--switch MEMBER_ID]
    fund-trading.py list
    fund-trading.py detail --fund-code CODE
    fund-trading.py recommend
    fund-trading.py position
    fund-trading.py orders [--order-type TYPE] [--page NUM] [--size NUM]
    fund-trading.py subscribe --fund-code CODE --amount AMOUNT
    fund-trading.py redeem --fund-code CODE --shares SHARES
    fund-trading.py cancel --trade-id TRADE_ID

Examples:
    fund-trading.py register --username 我的账户
    fund-trading.py account --list
    fund-trading.py list
    fund-trading.py position
    fund-trading.py subscribe --fund-code 000048 --amount 1000
"""

import argparse
import json
import os
import random
import string
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
CONFIG_FILE = DATA_DIR / "config.json"

API_ENDPOINT = "http://127.0.0.1:8080/openApi"
RECOMMEND_API = "https://m2.nicaifu.com/mobileGateway/V1/channel/getPageChannelInfo"


def format_amount(value, unit="元"):
    if value is None or value == "" or value == "-":
        return None
    try:
        num = float(value)
        if num >= 10000:
            return f"{num / 10000:.2f}万{unit}"
        return f"{num:.2f}{unit}"
    except (ValueError, TypeError):
        return None


def format_percent(value):
    if value is None or value == "" or value == "-":
        return None
    try:
        num = float(value)
        sign = "+" if num > 0 else ""
        return f"{sign}{num:.2f}%"
    except (ValueError, TypeError):
        return None


def format_shares(value):
    if value is None or value == "" or value == "-":
        return None
    try:
        num = float(value)
        return f"{num:.2f}份"
    except (ValueError, TypeError):
        return None


def safe_get(data, key, default=""):
    value = data.get(key)
    if value is None or value == "" or value == "-":
        return default if default else None
    return value


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return {"current_member_id": None, "accounts": [], "tokens": {}}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
    if "accounts" not in config:
        config["accounts"] = []
    if "current_member_id" not in config:
        config["current_member_id"] = None
    if "tokens" not in config:
        config["tokens"] = {}
    return config


def save_config(config: dict):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def get_current_account() -> dict:
    config = load_config()
    member_id = config.get("current_member_id")
    if not member_id:
        print("❌ 未找到当前账户，请先注册或切换账户")
        print("   使用: fund-trading.py register --username 我的账户")
        sys.exit(1)

    for acc in config.get("accounts", []):
        if acc.get("member_id") == member_id:
            return acc

    print(f"❌ 未找到账户配置: {member_id}")
    sys.exit(1)


def get_token(
    client_id: str, client_secret: str, force_refresh: bool = False
) -> Optional[str]:
    """获取 OAuth 2.0 Access Token"""
    config = load_config()
    token_key = f"{client_id}"

    if not force_refresh:
        cached = config.get("tokens", {}).get(token_key)
        if cached:
            expires_at = cached.get("expires_at", 0)
            if time.time() < expires_at - 300:
                return cached.get("access_token")

    url = f"{API_ENDPOINT}/openapi/v1/oauth/token"
    body = json.dumps(
        {
            "grantType": "client_credentials",
            "clientId": client_id,
            "clientSecret": client_secret,
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"❌ 获取Token失败: HTTP {e.code}")
        print(f"   响应: {error_body}")
        return None
    except Exception as e:
        print(f"❌ 获取Token失败: {e}")
        return None

    access_token = result.get("accessToken")
    expires_in = result.get("expiresIn", 2592000)

    if access_token:
        if "tokens" not in config:
            config["tokens"] = {}
        config["tokens"][token_key] = {
            "access_token": access_token,
            "expires_at": time.time() + expires_in,
        }
        save_config(config)
        return access_token

    return None


def make_request(path: str, body: Optional[dict] = None, method: str = "POST") -> dict:
    """使用 Bearer Token 调用 API"""
    account = get_current_account()
    client_id = account.get("app_key") or account.get("client_id")
    client_secret = account.get("app_secret") or account.get("client_secret")

    if not client_id or not client_secret:
        print("❌ 当前账户缺少 client_id 或 client_secret")
        return {"error": "缺少认证信息"}

    token = get_token(client_id, client_secret)
    if not token:
        return {"error": "获取Token失败"}

    url = f"{API_ENDPOINT}{path}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    data = json.dumps(body or {}).encode("utf-8") if method == "POST" else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        if e.code == 401:
            new_token = get_token(client_id, client_secret, force_refresh=True)
            if new_token:
                headers["Authorization"] = f"Bearer {new_token}"
                req = urllib.request.Request(
                    url, data=data, headers=headers, method=method
                )
                try:
                    with urllib.request.urlopen(req, timeout=30) as response:
                        return json.loads(response.read().decode("utf-8"))
                except Exception:
                    pass
        return {"error": f"HTTP {e.code}: {error_body}"}
    except urllib.error.URLError as e:
        return {"error": f"Connection error: {e.reason}"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse error: {e}"}


def make_get_request(path: str) -> dict:
    """GET 请求"""
    return make_request(path, method="GET")


def cmd_register(args):
    username = args.username or f"user_{int(time.time())}"

    url = f"{API_ENDPOINT}/openapi/v1/channel/register"
    body = json.dumps({"username": username}).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )

    try:
        print(f"🔄 正在注册账户: {username}...")
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"❌ 注册失败: HTTP {e.code}")
        print(f"   响应: {error_body}")
        return
    except urllib.error.URLError as e:
        print(f"❌ 连接失败: {e.reason}")
        return

    if (
        result.get("retCode") not in ["S", "000000", "000000"]
        and result.get("retState") != "SUCCESS"
    ):
        print(f"❌ 注册失败: {result.get('retMsg', '未知错误')}")
        return

    api_result = result.get("apiResult", {})
    member_id = api_result.get("memberId") or username
    client_id = api_result.get("appKey") or api_result.get("clientId")
    client_secret = api_result.get("appSecret") or api_result.get("clientSecret")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    account = {
        "member_id": member_id,
        "username": username,
        "client_id": client_id,
        "client_secret": client_secret,
        "created_at": created_at,
    }

    config = load_config()
    config["accounts"].append(account)
    config["current_member_id"] = member_id
    save_config(config)

    print(f"✅ 注册成功!")
    print(f"   账户名: {username}")
    print(f"   MEMBER_ID: {member_id}")
    print(f"   CLIENT_ID: {client_id}")
    print(f"   CLIENT_SECRET: {client_secret}")
    print(f"   创建时间: {created_at}")
    print(f"\n📌 已自动切换到新账户")


def cmd_account(args):
    config = load_config()

    if args.switch:
        for acc in config.get("accounts", []):
            if acc.get("member_id") == args.switch:
                config["current_member_id"] = args.switch
                save_config(config)
                print(f"✅ 已切换到账户: {args.switch}")
                return
        print(f"❌ 未找到账户: {args.switch}")
        return

    if args.list:
        accounts = config.get("accounts", [])
        if not accounts:
            print("📭 暂无账户，请先注册")
            print("   使用: fund-trading.py register --username 账户名")
            return

        current = config.get("current_member_id")
        print("┌" + "─" * 50 + "┐")
        print("│" + " 账户列表".center(46) + "│")
        print("├" + "─" * 50 + "┤")

        for i, acc in enumerate(accounts, 1):
            is_current = "👉 " if acc.get("member_id") == current else "   "
            username = safe_get(acc, "username") or "未命名"
            member_id = safe_get(acc, "member_id") or "-"
            client_id = safe_get(acc, "client_id") or safe_get(acc, "app_key") or "-"
            created = safe_get(acc, "created_at") or "-"

            print(f"│ {is_current}{i}. {username}")
            print(f"│    MEMBER_ID: {member_id}")
            print(f"│    CLIENT_ID: {client_id}")
            print(f"│    创建时间: {created}")
            if i < len(accounts):
                print("├" + "─" * 50 + "┤")

        print("└" + "─" * 50 + "┘")
        return

    current = config.get("current_member_id")
    if current:
        print(f"📌 当前账户: {current}")
    else:
        print("📭 未设置当前账户")


def cmd_list(args):
    result = make_get_request("/openapi/v1/shipan/fund/list")

    if result.get("retState") != "SUCCESS" and result.get("retCode") not in [
        "S",
        "000000",
    ]:
        print(f"❌ 查询失败: {result.get('retMsg', result.get('error', '未知错误'))}")
        return

    data = result.get("apiResult", [])
    if not data:
        print("📭 暂无可申购基金")
        return

    total = len(data)
    display_data = data[:20]

    print("┌" + "─" * 70 + "┐")
    print(
        "│" + f" 基金列表 (共{total}只，显示前{len(display_data)}只) ".center(66) + "│"
    )
    print("├" + "─" * 70 + "┤")
    print("│ 代码     名称                         净值     状态   │")
    print("├" + "─" * 70 + "┤")

    for fund in display_data:
        code = safe_get(fund, "productCode") or "-"
        name = safe_get(fund, "productName") or safe_get(fund, "productSName") or "-"
        if len(name) > 18:
            name = name[:16] + ".."

        net = format_amount(fund.get("dailyNet"), "")
        net_str = f"{net:>8}" if net else "    -   "

        status = "可申购" if fund.get("buyStatus") == 1 else "暂停"

        print(f"│ {code:<8} {name:<22} {net_str}  {status}  │")

    print("└" + "─" * 70 + "┘")


def cmd_detail(args):
    result = make_get_request(
        f"/openapi/v1/shipan/fund/detail?productCode={args.fund_code}"
    )

    if result.get("retState") != "SUCCESS" and result.get("retCode") not in [
        "S",
        "000000",
    ]:
        print(f"❌ 查询失败: {result.get('retMsg', result.get('error', '未知错误'))}")
        return

    data = result.get("apiResult")
    if not data:
        print("📭 未找到该基金")
        return

    code = safe_get(data, "productCode") or "-"
    name = safe_get(data, "productName") or "-"
    sname = safe_get(data, "productSName")
    risk = safe_get(data, "risk")
    daily_net = format_amount(data.get("dailyNet"), "")
    day_rate = format_percent(data.get("dayRate"))
    week_rate = format_percent(data.get("weekRate"))
    month_rate = format_percent(data.get("monthRate"))
    year_rate = format_percent(data.get("yearRate"))
    this_year_rate = format_percent(data.get("thisyearrate"))
    min_buy = safe_get(data, "minBuyAmt")
    buy_status = "可申购" if data.get("buyStatus") == 1 else "暂停"
    sale_status = "可赎回" if data.get("saleStatus") == 1 else "暂停"

    print("┌" + "─" * 50 + "┐")
    print("│" + " 基金详情 ".center(46) + "│")
    print("├" + "─" * 50 + "┤")

    print(f"│  基金代码: {code:<33}│")
    print(f"│  基金名称: {name[:28]:<33}│")
    if sname:
        print(f"│  基金简称: {sname[:28]:<33}│")
    if risk:
        print(f"│  风险等级: {risk:<33}│")
    if daily_net:
        print(f"│  单位净值: {daily_net:<33}│")

    print("├" + "─" * 50 + "┤")
    print("│" + " 📈 收益表现 ".center(46) + "│")
    print("├" + "─" * 50 + "┤")

    if day_rate:
        day_icon = (
            "🔴" if data.get("dayRate") and float(data.get("dayRate", 0)) < 0 else "🟢"
        )
        print(f"│  日涨跌:   {day_icon} {day_rate:<29}│")
    if week_rate:
        print(f"│  近一周:   {week_rate:<32}│")
    if month_rate:
        print(f"│  近一月:   {month_rate:<32}│")
    if year_rate:
        print(f"│  近一年:   {year_rate:<32}│")
    if this_year_rate:
        print(f"│  今年以来: {this_year_rate:<30}│")

    print("├" + "─" * 50 + "┤")
    print("│" + " 💰 交易信息 ".center(46) + "│")
    print("├" + "─" * 50 + "┤")

    if min_buy:
        print(f"│  最小申购: {min_buy}元{' ' * 28}│")
    print(f"│  申购状态: {buy_status:<33}│")
    print(f"│  赎回状态: {sale_status:<33}│")

    print("└" + "─" * 50 + "┘")


def cmd_recommend(args):
    url = f"{RECOMMEND_API}?channelCode=ACT_FUND_GSBJJ20230523"

    print("🔄 正在获取推荐基金...")

    req = urllib.request.Request(url, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"❌ 获取推荐基金失败: {e}")
        return

    if result.get("retState") != "SUCCESS":
        print(f"❌ 获取推荐基金失败: {result.get('retMsg', '未知错误')}")
        return

    api_result = result.get("apiResult", {})
    group_list = api_result.get("groupVoList", [])

    if not group_list:
        print("📭 暂无推荐基金")
        return

    print("📋 固收宝 - 推荐基金列表\n")

    for group in group_list:
        items = group.get("items", [])
        if not items:
            continue

        desc_json = group.get("descJson", "")
        if desc_json:
            try:
                desc = json.loads(desc_json)
                title = desc.get("title", "")
                subtitle = desc.get("subtitle", "")
                if title:
                    print(f"### {title}")
                if subtitle:
                    print(f"{subtitle}\n")
            except:
                pass

        count = 0
        for item in items:
            if item.get("bizType") != "fund":
                continue
            if not item.get("canDisplay", True):
                continue
            if count >= 5:
                break

            code = item.get("bizCode", "-")
            name = item.get("name", "-")
            profit_rate = item.get("profitRate", "-")
            rate_tip = item.get("rateTip", "近一年涨幅")
            brand_ad = item.get("brandAd", [])

            tags = []
            for ad in brand_ad:
                if ad.get("show") and ad.get("part1st"):
                    tags.append(ad["part1st"])

            tag_str = " | ".join(tags[:2]) if tags else ""

            print(f"  • {code} {name}")
            print(f"    {rate_tip}: {profit_rate}%")
            if tag_str:
                print(f"    {tag_str}")
            print()
            count += 1

        print()


def cmd_position(args):
    result = make_request("/openapi/v1/shipan/asset/query")

    if result.get("retState") not in ["SUCCESS"] and result.get("retCode") not in [
        "S",
        "000000",
    ]:
        print(f"❌ 查询失败: {result.get('retMsg', result.get('error', '未知错误'))}")
        return

    data = result.get("apiResult")
    if not data:
        print("📭 您暂无基金持仓")
        return

    total_asset = safe_get(data, "totalAsset")
    total_profit = safe_get(data, "totalProfit")
    profit_rate = safe_get(data, "totalProfitRate")
    holdings = data.get("holdings", [])

    if not total_asset and not holdings:
        print("📭 您暂无基金持仓")
        return

    print("┌" + "─" * 50 + "┐")
    print("│" + " 💰 资产概览 ".center(46) + "│")
    print("├" + "─" * 50 + "┤")

    if total_asset:
        asset_str = format_amount(total_asset)
        print(f"│  总资产: {asset_str:<39}│")

    if total_profit is not None and profit_rate is not None:
        try:
            profit_num = float(total_profit)
            rate_num = float(profit_rate)
            icon = "📈" if profit_num >= 0 else "📉"
            print(f"│  总收益: {icon} {profit_num:.2f}元 ({rate_num:.2f}%){' ' * 14}│")
        except (ValueError, TypeError):
            pass

    print("└" + "─" * 50 + "┘")

    if holdings:
        print("\n┌" + "─" * 70 + "┐")
        print("│" + " 📊 持仓明细 ".center(66) + "│")
        print("├" + "─" * 70 + "┤")
        print("│ 基金代码  名称                    份额        市值        │")
        print("├" + "─" * 70 + "┤")

        for pos in holdings:
            code = safe_get(pos, "fundCode") or "-"
            name = safe_get(pos, "fundName") or "-"
            if len(name) > 16:
                name = name[:14] + ".."

            shares = format_shares(pos.get("share"))
            value = format_amount(pos.get("marketValue"))
            profit = safe_get(pos, "profit")

            shares_str = f"{shares:>10}" if shares else "         -"
            value_str = f"{value:>10}" if value else "         -"

            print(f"│ {code:<8} {name:<18} {shares_str} {value_str}  │")

        print("└" + "─" * 70 + "┘")


def cmd_orders(args):
    body = {
        "pageNo": args.page,
        "pageSize": args.size,
    }
    if args.order_type and args.order_type != "all":
        body["tradeType"] = args.order_type

    result = make_request("/openapi/v1/shipan/trade/query", body)

    data = result.get("apiResult")
    if not data:
        print("📭 暂无交易记录")
        return

    records = data.get("result", []) if isinstance(data, dict) else data
    if not records:
        print("📭 暂无交易记录")
        return

    total = (
        data.get("totalCount", len(records)) if isinstance(data, dict) else len(records)
    )

    print("┌" + "─" * 80 + "┐")
    print("│" + f" 📋 交易记录 (共{total}条) ".center(76) + "│")
    print("├" + "─" * 80 + "┤")
    print("│ 订单号                    类型    基金           金额        状态     │")
    print("├" + "─" * 80 + "┤")

    for order in records:
        order_id = safe_get(order, "tradeId") or "-"
        if len(order_id) > 24:
            order_id = order_id[:22] + ".."

        code = safe_get(order, "fundCode") or "-"
        name = safe_get(order, "fundName") or "-"
        if len(name) > 8:
            name = name[:6] + ".."

        trade_type = safe_get(order, "tradeTypeDesc") or "-"
        if len(trade_type) > 4:
            trade_type = trade_type[:4]

        amount = format_amount(order.get("tradeAmount"))
        amount_str = f"{amount:>10}" if amount else "         -"

        status = safe_get(order, "tradeStatusDesc") or "-"

        type_icon = (
            "💰" if "建仓" in str(trade_type) or "申购" in str(trade_type) else "📤"
        )
        status_icon = (
            "✅" if "确认" in str(status) and "待" not in str(status) else "⏳"
        )

        fund_display = f"{code} {name}"
        if len(fund_display) > 12:
            fund_display = fund_display[:12]

        print(
            f"│ {order_id:<24} {type_icon}{trade_type:<4} {fund_display:<12} {amount_str}  {status_icon}{status:<6}│"
        )

    print("└" + "─" * 80 + "┘")


def cmd_subscribe(args):
    body = {
        "fundCode": args.fund_code,
        "amount": args.amount,
    }

    print(f"💰 申购基金: {args.fund_code}, 金额: {args.amount}元")

    result = make_request("/openapi/v1/shipan/trade/subscribe", body)

    if result.get("retState") == "SUCCESS" or result.get("retCode") == "000000":
        api_result = result.get("apiResult") or {}
        order_id = api_result.get("tradeId", "-")
        print(f"✅ 申购成功! 订单号: {order_id}")
    else:
        print(f"❌ 申购失败: {result.get('retMsg', result.get('error', '未知错误'))}")


def cmd_redeem(args):
    body = {
        "fundCode": args.fund_code,
        "share": args.shares,
    }

    print(f"📤 赎回基金: {args.fund_code}, 份额: {args.shares}份")

    result = make_request("/openapi/v1/shipan/trade/redeem", body)

    if result.get("retState") == "SUCCESS" or result.get("retCode") == "000000":
        api_result = result.get("apiResult") or {}
        order_id = api_result.get("tradeId", "-")
        print(f"✅ 赎回成功! 订单号: {order_id}")
    else:
        print(f"❌ 赎回失败: {result.get('retMsg', result.get('error', '未知错误'))}")


def cmd_cancel(args):
    body = {"tradeId": args.trade_id}

    print(f"📤 撤销订单: {args.trade_id}")

    result = make_request("/openapi/v1/shipan/trade/cancel", body)

    if result.get("retState") == "SUCCESS" or result.get("retCode") == "000000":
        api_result = result.get("apiResult") or {}
        print(f"✅ 撤单成功: {api_result.get('message', '操作完成')}")
    else:
        print(f"❌ 撤单失败: {result.get('retMsg', result.get('error', '未知错误'))}")


def main():
    parser = argparse.ArgumentParser(
        description="基金实盘交易工具 (OAuth 2.0)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  fund-trading.py register --username 我的账户
  fund-trading.py account --list
  fund-trading.py list
  fund-trading.py recommend
  fund-trading.py position
  fund-trading.py subscribe --fund-code 000048 --amount 1000
  fund-trading.py redeem --fund-code 000048 --shares 100
""",
    )
    subparsers = parser.add_subparsers(dest="command", help="命令")

    p_register = subparsers.add_parser("register", help="注册新账户")
    p_register.add_argument("--username", "-u", help="账户名称")
    p_register.set_defaults(func=cmd_register)

    p_account = subparsers.add_parser("account", help="账户管理")
    p_account.add_argument("--list", "-l", action="store_true", help="列出所有账户")
    p_account.add_argument("--switch", "-s", help="切换账户 (member_id)")
    p_account.set_defaults(func=cmd_account)

    p_list = subparsers.add_parser("list", help="查询基金列表")
    p_list.set_defaults(func=cmd_list)

    p_detail = subparsers.add_parser("detail", help="查询基金详情")
    p_detail.add_argument("--fund-code", "-c", required=True, help="基金代码")
    p_detail.set_defaults(func=cmd_detail)

    p_recommend = subparsers.add_parser("recommend", help="获取推荐基金")
    p_recommend.set_defaults(func=cmd_recommend)

    p_position = subparsers.add_parser("position", help="查询持仓")
    p_position.set_defaults(func=cmd_position)

    p_orders = subparsers.add_parser("orders", help="查询交易记录")
    p_orders.add_argument("--order-type", "-t", help="订单类型: subscribe/redeem/all")
    p_orders.add_argument("--page", "-p", type=int, default=1, help="页码")
    p_orders.add_argument("--size", "-s", type=int, default=20, help="每页数量")
    p_orders.set_defaults(func=cmd_orders)

    p_subscribe = subparsers.add_parser("subscribe", help="申购基金")
    p_subscribe.add_argument("--fund-code", "-c", required=True, help="基金代码")
    p_subscribe.add_argument(
        "--amount", "-a", required=True, type=float, help="申购金额"
    )
    p_subscribe.set_defaults(func=cmd_subscribe)

    p_redeem = subparsers.add_parser("redeem", help="赎回基金")
    p_redeem.add_argument("--fund-code", "-c", required=True, help="基金代码")
    p_redeem.add_argument("--shares", "-s", required=True, type=float, help="赎回份额")
    p_redeem.set_defaults(func=cmd_redeem)

    p_cancel = subparsers.add_parser("cancel", help="撤销订单")
    p_cancel.add_argument("--trade-id", "-t", required=True, help="订单号")
    p_cancel.set_defaults(func=cmd_cancel)

    args = parser.parse_args()

    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
