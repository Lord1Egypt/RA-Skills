#!/usr/bin/env python3
"""
Brown Dust 2 — 兑换码自动兑换。
从 BD2Pulse 抓取最新兑换码，通过官方 API 一键兑换。
零外部依赖，零浏览器操作。
"""

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import List, Dict, Optional

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

_REDEEM_API = "https://loj2urwaua.execute-api.ap-northeast-1.amazonaws.com/prod/coupon"
_APP_ID = "bd2-live"

_BD2PULSE_URL = "https://thebd2pulse.com/zh-CN/"

_NICKNAME_FILE = Path(__file__).resolve().parent.parent / ".nickname"


def save_nickname(nickname: str):
    with open(_NICKNAME_FILE, "w") as f:
        f.write(nickname.strip())
    print(f"💾 昵称已保存: {nickname}", file=sys.stderr)


def load_nickname() -> Optional[str]:
    if _NICKNAME_FILE.exists():
        return _NICKNAME_FILE.read_text().strip()
    return None


def fetch_codes() -> List[Dict[str, str]]:
    """从 BD2Pulse 抓取最新兑换码列表"""
    req = urllib.request.Request(_BD2PULSE_URL, headers={"User-Agent": _UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8")
    except Exception as e:
        print(f"抓取 BD2Pulse 失败: {e}", file=sys.stderr)
        return []

    codes = []
    pattern = re.compile(
        r'<code[^>]*>\s*([A-Za-z0-9]+)\s*</code>'
        r'|`([A-Za-z0-9]+)`',
        re.IGNORECASE
    )
    for m in pattern.finditer(html):
        code = (m.group(1) or m.group(2) or "").strip().upper()
        if code and len(code) >= 6 and code not in [c["code"] for c in codes]:
            codes.append({"code": code, "description": ""})

    if not codes:
        code_pattern = re.compile(r'\b([A-Z0-9]{8,20})\b')
        seen = set()
        for m in code_pattern.finditer(html):
            c = m.group(1)
            if c.startswith(("BD2", "BURAJ", "THANK", "2026", "2025")) and c not in seen:
                seen.add(c)
                codes.append({"code": c, "description": ""})

    return codes


def redeem_code(nickname: str, code: str) -> Dict:
    """调用官方 API 兑换一个码"""
    payload = json.dumps({
        "appId": _APP_ID,
        "userId": nickname,
        "code": code,
    }).encode("utf-8")

    req = urllib.request.Request(
        _REDEEM_API,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": _UA,
            "Origin": "https://redeem.bd2.pmang.cloud",
            "Referer": "https://redeem.bd2.pmang.cloud/bd2/index.html",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(body)
        except Exception:
            return {"success": False, "error": f"HTTP {e.code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


_ERROR_MESSAGES = {
    "ValidationFailed": "无效的兑换码",
    "InvalidCode": "无效的兑换码",
    "ExpiredCode": "兑换码已过期",
    "AlreadyUsed": "已兑换过",
    "ExceededUses": "使用次数已达上限",
    "UnavailableCode": "兑换码不可用",
    "IncorrectUser": "昵称不正确",
    "ClaimRewardsFailed": "领取奖励失败",
}


def redeem_all(nickname: str, codes: List[Dict[str, str]]) -> List[Dict]:
    """批量兑换所有码"""
    results = []
    for i, item in enumerate(codes):
        code = item["code"]
        resp = redeem_code(nickname, code)

        success = resp.get("success", False)
        error = resp.get("error", "")
        error_msg = _ERROR_MESSAGES.get(error, error)

        result = {
            "code": code,
            "description": item.get("description", ""),
            "success": success,
            "error": error,
            "error_msg": error_msg,
            "already_used": error == "AlreadyUsed",
        }
        results.append(result)

        if i < len(codes) - 1:
            time.sleep(1)

    return results


def format_output(nickname: str, results: List[Dict]) -> str:
    lines = [f"🎮 Brown Dust 2 兑换结果 — {nickname}", ""]

    new_success = 0
    already = 0
    failed = 0

    for r in results:
        code = r["code"]
        if r["success"]:
            lines.append(f"  ✅ {code} — 兑换成功！")
            new_success += 1
        elif r["already_used"]:
            lines.append(f"  ⏭️  {code} — 已兑换过")
            already += 1
        else:
            lines.append(f"  ❌ {code} — {r['error_msg']}")
            failed += 1

    lines.append("")
    lines.append(f"📊 总计 {len(results)} 个码：✅ {new_success} 新兑换，⏭️ {already} 已兑换，❌ {failed} 失败")

    if new_success > 0:
        lines.append("")
        lines.append("📬 奖励已发送到游戏内邮箱，重启游戏后领取！")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Brown Dust 2 兑换码自动兑换",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 保存昵称（只需一次）
  python3 redeem.py --save-nickname "你的游戏昵称"

  # 自动抓取 BD2Pulse 最新码并全部兑换
  python3 redeem.py

  # 指定昵称兑换
  python3 redeem.py --nickname "你的游戏昵称"

  # 手动指定兑换码
  python3 redeem.py --code BD21000BOOST
  python3 redeem.py --code BD21000BOOST,BD2RADIOMAGICAL

  # 只查看当前有哪些码（不兑换）
  python3 redeem.py --list

  # JSON 输出
  python3 redeem.py --json
""",
    )
    parser.add_argument("--nickname", help="游戏内昵称")
    parser.add_argument("--save-nickname", help="保存昵称到本地")
    parser.add_argument("--code", help="手动指定兑换码（逗号分隔）")
    parser.add_argument("--list", action="store_true", help="仅列出当前可用兑换码，不兑换")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    if args.save_nickname:
        save_nickname(args.save_nickname)
        print(f"✅ 昵称已保存: {args.save_nickname}")
        return

    if args.list:
        codes = fetch_codes()
        if not codes:
            print("❌ 没有找到可用的兑换码")
            return
        if args.json:
            print(json.dumps(codes, ensure_ascii=False, indent=2))
        else:
            print(f"🎮 BD2Pulse 当前兑换码 ({len(codes)} 个)：\n")
            for c in codes:
                print(f"  📎 {c['code']}")
        return

    nickname = args.nickname
    if not nickname:
        nickname = load_nickname()
    if not nickname:
        print("❌ 需要游戏内昵称。请运行：")
        print("")
        print('  python3 redeem.py --save-nickname "你的游戏昵称"')
        print("")
        print("或使用 --nickname 参数指定")
        sys.exit(1)

    if args.code:
        codes = [{"code": c.strip().upper(), "description": ""} for c in args.code.split(",") if c.strip()]
    else:
        print("🔍 正在从 BD2Pulse 抓取最新兑换码...", file=sys.stderr)
        codes = fetch_codes()

    if not codes:
        print("❌ 没有找到可用的兑换码")
        return

    print(f"📋 找到 {len(codes)} 个兑换码，开始兑换...\n", file=sys.stderr)
    results = redeem_all(nickname, codes)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_output(nickname, results))


if __name__ == "__main__":
    main()
