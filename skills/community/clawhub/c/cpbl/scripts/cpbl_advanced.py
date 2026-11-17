#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
CPBL 進階數據查詢（stats.cpbl.com.tw 官方進階數據站）

資料來源：https://stats.cpbl.com.tw（中華職棒進階數據 Statcast 級）
- /v1/leaderboards/exit-velocity   擊球初速 × 仰角（Statcast）
- /v1/leaderboards/batted-ball     擊球彈道（滾地/飛球/平飛/內飛/高飛）
- /v1/leaderboards/pitch-tracking  球種球速轉速
- /v1/leaderboards/pr-table        wOBA/AVG/SLG PR 百分位
- /v1/leaderboards/summary         聯盟年度總覽
- /v1/players/logs                 單一球員逐球紀錄（Trackman）
- /v1/players/{acnt}               球員基本資料
- /v1/players/autocomplete         球員搜尋

用法：
  # 打者擊球初速排行
  uv run skills/cpbl/scripts/cpbl_advanced.py leaderboard exit-velocity --type batter --year 2026
  # 投手球種追蹤
  uv run skills/cpbl/scripts/cpbl_advanced.py leaderboard pitch-tracking --type pitcher --year 2026
  # wOBA PR 百分位（打者）
  uv run skills/cpbl/scripts/cpbl_advanced.py leaderboard pr-table --type batter --year 2026
  # 過濾：月份/球隊/守位/球種
  uv run skills/cpbl/scripts/cpbl_advanced.py leaderboard exit-velocity --type batter --year 2026 --month 8 --team 兄弟 --position SS
  # 聯盟年度總覽
  uv run skills/cpbl/scripts/cpbl_advanced.py summary --year 2026
  # 單一球員逐球紀錄
  uv run skills/cpbl/scripts/cpbl_advanced.py logs --player 曾子祐 --year 2026 --limit 10
  # 球員基本資料
  uv run skills/cpbl/scripts/cpbl_advanced.py info --player 曾子祐
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime
from typing import Optional

BASE = "https://stats.cpbl.com.tw/api/proxy/v1"

TEAM_CODES = {
    "中信兄弟": "ACN011", "統一7-ELEVEn獅": "ADD011", "樂天桃猿": "AJL011",
    "富邦悍將": "AEO011", "味全龍": "AAA011", "台鋼雄鷹": "AKP011",
    "中信": "ACN011", "統一": "ADD011", "獅": "ADD011", "桃猿": "AJL011",
    "悍將": "AEO011", "龍": "AAA011", "雄鷹": "AKP011", "兄弟": "ACN011",
    "富邦": "AEO011", "味全": "AAA011", "台鋼": "AKP011",
}

POSITION_CODE_LABEL = {
    "P": "投手", "C": "捕手", "1B": "一壘手", "2B": "二壘手", "3B": "三壘手",
    "SS": "游擊手", "LF": "左外野手", "CF": "中外野手", "RF": "右外野手",
    "DH": "指定打擊", "PH": "代打",
}

FIELD_CODE_LABEL = {
    "F04": "台南", "F07": "嘉義市", "F08": "新莊", "F09": "澄清湖",
    "F10": "天母", "F12": "花蓮", "F13": "斗六", "F17": "台東",
    "F19": "洲際", "F23": "樂天桃園", "F29": "大巨蛋",
}

KIND_NAMES = {
    'A': '一軍例行賽', 'B': '一軍明星賽', 'C': '一軍總冠軍賽',
    'D': '二軍例行賽', 'E': '一軍季後挑戰賽', 'F': '二軍總冠軍賽',
    'G': '一軍熱身賽', 'H': '未來之星邀請賽', 'X': '國際交流賽',
}

PITCH_TYPE_NAMES = {
    "fastball": "快速球", "breakingball": "變化球",
    "fourseam": "四縫線", "fourseamfastball": "四縫線", "twoseam": "二縫線",
    "twoseamfastball": "二縫線", "sinker": "伸卡球", "cutter": "卡特球",
    "slider": "滑球", "sweeper": "橫掃滑球", "curveball": "曲球",
    "surve": "滑曲球", "changeup": "變速球", "splitter": "指叉球",
    "forkball": "叉指球", "knuckleball": "蝴蝶球", "screwball": "螺旋球",
}


def api_get(path: str, params: dict) -> dict:
    """呼叫 stats.cpbl.com.tw API（經 /api/proxy）"""
    filtered = {k: v for k, v in params.items() if v not in ("", None, 0, "0")}
    url = f"{BASE}{path}"
    if filtered:
        url += "?" + urllib.parse.urlencode(filtered)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CPBL-Stats-Script",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def find_player_acnt(name: str) -> Optional[str]:
    """用 autocomplete 找球員 acnt"""
    data = api_get("/players/autocomplete", {})
    for p in data.get("Data", {}).get("Players", []):
        if name in p.get("CHName", "") or name in (p.get("AboriginalName") or ""):
            return p["Acnt"], p["CHName"], p.get("Team", {}).get("Name", "")
    return None


# ─── 輸出呈現 ───

def fmt_leaderboard_exit_velocity(rows, limit):
    print(f"🔥 擊球初速排行（{len(rows)} 人）")
    print(f"{'排名':<4}{'球員':<12}{'球隊':<10}{'BBE':<6}{'平均初速':<10}{'最大初速':<10}{'平均仰角':<9}{'HardHit%':<10}{'Barrels':<8}")
    for i, r in enumerate(rows[:limit], 1):
        p = r["Player"]; t = r["Team"]
        hardhit = f"{r.get('HardHitp', 0)*100:.1f}%"
        print(f"{i:<4}{p['Name']:<12}{t['Name']:<10}{r.get('Bbe', 0):<6}"
              f"{r.get('EvAvg', 0):.1f} km/h{'':<3}{r.get('EvMax', 0):.1f} km/h{'':<3}"
              f"{r.get('LaAvg', 0):.1f}°{'':<5}{hardhit:<10}{r.get('Barrels', 0):<8}")


def fmt_leaderboard_batted_ball(rows, limit):
    print(f"🪐 擊球彈道排行（{len(rows)} 人）")
    print(f"{'排名':<4}{'球員':<12}{'球隊':<10}{'BBE':<6}{'滾地%':<8}{'飛球%':<8}{'平飛%':<8}{'內飛%':<8}{'高飛%':<8}")
    for i, r in enumerate(rows[:limit], 1):
        p = r["Player"]; t = r["Team"]
        print(f"{i:<4}{p['Name']:<12}{t['Name']:<10}{r.get('Bbe', 0):<6}"
              f"{r.get('Gbp', 0)*100:.1f}%{'':<2}{r.get('Airp', 0)*100:.1f}%{'':<2}"
              f"{r.get('Fbp', 0)*100:.1f}%{'':<2}{r.get('Ldp', 0)*100:.1f}%{'':<2}"
              f"{r.get('Pup', 0)*100:.1f}%")


def fmt_leaderboard_pitch_tracking(rows, limit):
    print(f"⚡ 球種球速轉速排行（{len(rows)} 筆）")
    print(f"{'排名':<4}{'球員':<12}{'球隊':<10}{'球種':<10}{'球數':<7}{'均速':<12}{'極速':<12}{'轉速':<12}{'轉速峰值':<10}")
    for i, r in enumerate(rows[:limit], 1):
        p = r["Player"]; t = r["Team"]
        pt = PITCH_TYPE_NAMES.get(r.get("PitchType", ""), r.get("PitchType", ""))
        print(f"{i:<4}{p['Name']:<12}{t['Name']:<10}{pt:<10}{r.get('Pitches', 0):<7}"
              f"{r.get('Kph', 0):.1f} km/h{'':<3}{r.get('KphMax', 0):.1f} km/h{'':<3}"
              f"{r.get('SpinRate', 0):.0f} rpm{'':<4}{r.get('SpinRateMax', 0):.0f} rpm")


def fmt_pr_table(rows, limit):
    print(f"📊 wOBA/AVG/SLG PR 百分位（{len(rows)} 人）")
    print(f"{'排名':<4}{'球員':<12}{'球隊':<10}{'打席':<6}{'wOBA':<8}{'PR':<6}{'AVG':<8}{'PR':<6}{'SLG':<8}{'PR':<6}")
    for i, r in enumerate(rows[:limit], 1):
        p = r["Player"]; t = r["Team"]
        print(f"{i:<4}{p['Name']:<12}{t['Name']:<10}{r.get('Pa', 0):<6}"
              f"{r.get('Woba', 0):.3f}{'':<3}{r.get('WobaPR', 0):<6}"
              f"{r.get('Ba', 0):.3f}{'':<3}{r.get('BaPR', 0):<6}"
              f"{r.get('Slg', 0):.3f}{'':<3}{r.get('SlgPR', 0):<6}")


def fmt_summary(summary):
    print("📈 聯盟進階數據總覽")
    for section, title in [("ExitVelocity", "擊球初速"), ("BattedBall", "彈道分布"), ("PitchTracking", "球種追蹤")]:
        rows = summary.get(section) or summary.get("Leaderboard", {}).get(section)
        if not rows:
            continue
        r = rows[0]
        print(f"\n── {title} ──")
        for k, v in r.items():
            if k in ("Player", "Team") or v is None:
                continue
            if isinstance(v, float):
                print(f"  {k}: {v:.3f}")
            else:
                print(f"  {k}: {v}")


def fmt_logs(logs, limit):
    print(f"📋 逐球紀錄（{len(logs)} 筆，顯示前 {min(limit, len(logs))}）")
    for log in logs[:limit]:
        tm = log.get("Trackman", {})
        pitch = tm.get("Pitch", {})
        release = pitch.get("Release", {})
        speed = f"{release.get('RelSpeed', 0):.0f} km/h" if release.get("RelSpeed") else "-"
        spin = f"{release.get('SpinRate', 0):.0f} rpm" if release.get("SpinRate") else "-"
        tag = tm.get("Play", {}).get("PitchTag", {})
        ptype = PITCH_TYPE_NAMES.get(tag.get("AutoPitchType", ""), tag.get("AutoPitchType", ""))
        print(f"[{log.get('InningSeq', '?')}局] {log.get('HitterName', '')} vs {log.get('PitcherName', '')} "
              f"| {log.get('Content', '')} | {ptype} {speed} {spin}")


def fmt_player_info(info):
    b = info.get("Player", {}).get("Basic", {})
    team = info.get("Player", {}).get("AcntImgPath", "")
    print(f"👤 {b.get('CHName', '')}（{b.get('Engname', '')}）")
    print(f"  背號: {b.get('UniformNo', '-')} | 守位: {POSITION_CODE_LABEL.get(b.get('Sex', ''), '-')}")
    print(f"  身高: {b.get('Height', '-')} cm | 體重: {b.get('Weight', '-')} kg | 生日: {b.get('BirthDate', '-')}")
    print(f"  國籍: {b.get('Nation', '-')} | 學校: {b.get('SchoolName', '-')}")
    if b.get("Rmk"):
        print(f"  經歷: {b.get('Rmk', '').strip()}")


# ─── CLI ───

def main():
    parser = argparse.ArgumentParser(description="CPBL 進階數據查詢（stats.cpbl.com.tw）")
    sub = parser.add_subparsers(dest="command", required=True)

    # leaderboard
    p_lb = sub.add_parser("leaderboard", help="進階數據排行")
    p_lb.add_argument("category", choices=["exit-velocity", "batted-ball", "pitch-tracking", "pr-table"],
                      help="數據類別")
    p_lb.add_argument("--type", choices=["batter", "pitcher"], default="batter", help="打者/投手（預設 batter）")
    p_lb.add_argument("--year", type=int, default=datetime.now().year)
    p_lb.add_argument("--month", type=int, help="月份 1-12（可省略 = 全年）")
    p_lb.add_argument("--team", help="球隊（模糊，如 兄弟/統一/樂天）")
    p_lb.add_argument("--position", help="守位代碼 P/C/1B/2B/3B/SS/LF/CF/RF/DH/PH")
    p_lb.add_argument("--pitch-type", help="球種（fastball/breakingball/fourseam/slider...）")
    p_lb.add_argument("--limit", type=int, default=10, help="顯示筆數（預設 10）")

    # summary
    p_sm = sub.add_parser("summary", help="聯盟年度進階總覽")
    p_sm.add_argument("--year", type=int, default=datetime.now().year)

    # logs
    p_lg = sub.add_parser("logs", help="單一球員逐球紀錄")
    p_lg.add_argument("--player", required=True, help="球員姓名")
    p_lg.add_argument("--year", type=int, default=datetime.now().year)
    p_lg.add_argument("--type", choices=["batter", "pitcher"], default="batter")
    p_lg.add_argument("--kind", default="A", help="賽事代碼（預設 A 一軍例行賽）")
    p_lg.add_argument("--limit", type=int, default=10)

    # info
    p_in = sub.add_parser("info", help="球員基本資料")
    p_in.add_argument("--player", required=True, help="球員姓名")

    args = parser.parse_args()

    if args.command == "leaderboard":
        params = {
            "searchType": args.type, "year": args.year, "gameKind": "A",
            "month": args.month,
            "teamCode": TEAM_CODES.get(args.team, "") if args.team else "",
            "defendStationCode": args.position or "",
            "pitchType": args.pitch_type or "",
        }
        if args.category == "pitch-tracking":
            params = {
                "gameKind": "A", "year": args.year, "month": args.month,
                "teamCode": TEAM_CODES.get(args.team, "") if args.team else "",
                "pitchType": args.pitch_type or "",
            }
        data = api_get(f"/leaderboards/{args.category}", params)
        rows = data.get("Data", {}).get("Leaderboard", [])
        if args.category == "exit-velocity":
            fmt_leaderboard_exit_velocity(rows, args.limit)
        elif args.category == "batted-ball":
            fmt_leaderboard_batted_ball(rows, args.limit)
        elif args.category == "pitch-tracking":
            fmt_leaderboard_pitch_tracking(rows, args.limit)
        else:
            fmt_pr_table(rows, args.limit)

    elif args.command == "summary":
        data = api_get("/leaderboards/summary", {"gameKind": "A", "year": args.year})
        fmt_summary(data.get("Data", {}))

    elif args.command == "logs":
        found = find_player_acnt(args.player)
        if not found:
            print(f"❌ 找不到球員「{args.player}」", file=sys.stderr)
            sys.exit(1)
        acnt, name, team = found
        print(f"✅ {name}（{team}） acnt={acnt}", file=sys.stderr)
        data = api_get("/players/logs", {
            "playerType": args.type, "acnt": acnt, "year": args.year, "kindCode": args.kind,
        })
        logs = data.get("Data", {}).get("Logs", [])
        if not logs:
            print("（沒有逐球資料）")
        fmt_logs(logs, args.limit)

    elif args.command == "info":
        found = find_player_acnt(args.player)
        if not found:
            print(f"❌ 找不到球員「{args.player}」", file=sys.stderr)
            sys.exit(1)
        acnt, name, team = found
        print(f"✅ {name}（{team}）", file=sys.stderr)
        data = api_get(f"/players/{acnt}", {})
        fmt_player_info(data.get("Data", {}))


if __name__ == "__main__":
    main()