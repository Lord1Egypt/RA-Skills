#!/usr/bin/env python3
"""
赛前预览分析脚本 - 生成 H2H + 近期状态综合分析报告

用法:
  python match_preview.py --team1 33 --team2 40 --league "Premier League"
  python match_preview.py --team1 "Manchester United" --team2 "Liverpool"
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# 添加脚本目录到 sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from fetch_football_data import (
    load_config, get_api_client, resolve_league,
    LEAGUE_NAME_MAP, ApiError, QuotaExceededError,
)


def get_team_id_by_name(client, name: str, league_name: str = None) -> int:
    """通过名称搜索球队 ID"""
    data = client.get_teams(search=name)
    teams = data.get("response", [])
    if not teams:
        raise ApiError(f"未找到球队: {name}")

    if league_name:
        # 如果有联赛上下文，优先匹配该联赛的球队
        for t in teams:
            if t.get("team", {}).get("name", "").lower() == name.lower():
                return t["team"]["id"]

    # 返回第一个匹配
    return teams[0]["team"]["id"]


def get_recent_form(client, team_id: int, last: int = 6) -> list:
    """获取球队最近 N 场比赛结果"""
    data = client.get_fixtures(team=team_id, last=last)
    return data.get("response", [])


def format_form_string(matches: list, team_id: int) -> str:
    """将最近比赛转化为 W/D/L 形态字符串"""
    form = []
    for m in matches:
        goals = m["goals"]
        home_goal = goals.get("home") or 0
        away_goal = goals.get("away") or 0
        is_home = m["teams"]["home"]["id"] == team_id

        if is_home:
            if home_goal > away_goal:
                form.append("W")
            elif home_goal < away_goal:
                form.append("L")
            else:
                form.append("D")
        else:
            if away_goal > home_goal:
                form.append("W")
            elif away_goal < home_goal:
                form.append("L")
            else:
                form.append("D")

    return " → ".join(form)


def generate_preview(team1_name: str, team2_name: str,
                     team1_id: int, team2_id: int,
                     client, league_name: str = None) -> str:
    """生成完整赛前预览报告"""
    lines = [
        f"# ⚽ 赛前预览: {team1_name} vs {team2_name}",
        "",
        f"> 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]

    # 1. H2H 数据
    try:
        h2h_data = client.get_h2h(team1_id, team2_id)
        matches = h2h_data.get("response", [])

        home_wins = sum(1 for m in matches if m["teams"]["home"]["winner"])
        away_wins = sum(1 for m in matches if m["teams"]["away"]["winner"])
        draws = len(matches) - home_wins - away_wins

        lines.extend([
            "---",
            "",
            "## 📊 历史交锋 (H2H)",
            "",
            f"| {team1_name} 胜 | 平局 | {team2_name} 胜 | 总场次 |",
            "|---|---|---|---|",
            f"| {home_wins} | {draws} | {away_wins} | {len(matches)} |",
            "",
        ])

        # 最近5场H2H
        lines.extend([
            "### 最近交锋",
            "| 日期 | 赛事 | 主队 | 比分 | 客队 |",
            "|------|------|------|------|------|",
        ])
        for m in matches[:5]:
            date = m["fixture"]["date"][:10]
            league = m["league"]["name"]
            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]
            hg = m["goals"]["home"] or 0
            ag = m["goals"]["away"] or 0
            lines.append(f"| {date} | {league} | {home} | {hg} - {ag} | {away} |")
        lines.append("")

    except Exception as e:
        lines.append(f"⚠️ H2H 数据获取失败: {e}")
        lines.append("")

    # 2. 近期状态
    try:
        t1_form = get_recent_form(client, team1_id)
        t2_form = get_recent_form(client, team2_id)

        lines.extend([
            "---",
            "",
            "## 📈 近期状态",
            "",
        ])

        # 球队1
        form1_str = format_form_string(t1_form, team1_id)
        t1_recent = t1_form[:6]
        t1_wins = sum(1 for m in t1_recent
                      if (m["teams"]["home"]["id"] == team1_id and m["teams"]["home"]["winner"])
                      or (m["teams"]["away"]["id"] == team1_id and m["teams"]["away"]["winner"]))
        t1_losses = sum(1 for m in t1_recent
                        if (m["teams"]["home"]["id"] == team1_id and m["teams"]["away"]["winner"])
                        or (m["teams"]["away"]["id"] == team1_id and m["teams"]["home"]["winner"]))
        t1_draws = len(t1_recent) - t1_wins - t1_losses

        lines.extend([
            f"### {team1_name}",
            f"- 近 {len(t1_recent)} 场: **{t1_wins}胜 {t1_draws}平 {t1_losses}负**",
            f"- 形态: {form1_str}",
            "",
        ])

        # 球队2
        form2_str = format_form_string(t2_form, team2_id)
        t2_recent = t2_form[:6]
        t2_wins = sum(1 for m in t2_recent
                      if (m["teams"]["home"]["id"] == team2_id and m["teams"]["home"]["winner"])
                      or (m["teams"]["away"]["id"] == team2_id and m["teams"]["away"]["winner"]))
        t2_losses = sum(1 for m in t2_recent
                        if (m["teams"]["home"]["id"] == team2_id and m["teams"]["away"]["winner"])
                        or (m["teams"]["away"]["id"] == team2_id and m["teams"]["home"]["winner"]))
        t2_draws = len(t2_recent) - t2_wins - t2_losses

        lines.extend([
            f"### {team2_name}",
            f"- 近 {len(t2_recent)} 场: **{t2_wins}胜 {t2_draws}平 {t2_losses}负**",
            f"- 形态: {form2_str}",
            "",
        ])

        # 近期比赛详情
        lines.extend([
            f"### {team1_name} 近期比赛",
            "| 日期 | 对阵 | 比分 | 结果 |",
            "|------|------|------|------|",
        ])
        for m in t1_recent:
            date = m["fixture"]["date"][:10]
            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]
            hg = m["goals"]["home"] or 0
            ag = m["goals"]["away"] or 0
            is_home = m["teams"]["home"]["id"] == team1_id
            if is_home:
                result = "胜" if hg > ag else ("负" if hg < ag else "平")
            else:
                result = "胜" if ag > hg else ("负" if ag < hg else "平")
            lines.append(f"| {date} | {home} vs {away} | {hg} - {ag} | **{result}** |")
        lines.append("")

        lines.extend([
            f"### {team2_name} 近期比赛",
            "| 日期 | 对阵 | 比分 | 结果 |",
            "|------|------|------|------|",
        ])
        for m in t2_recent:
            date = m["fixture"]["date"][:10]
            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]
            hg = m["goals"]["home"] or 0
            ag = m["goals"]["away"] or 0
            is_home = m["teams"]["home"]["id"] == team2_id
            if is_home:
                result = "胜" if hg > ag else ("负" if hg < ag else "平")
            else:
                result = "胜" if ag > hg else ("负" if ag < hg else "平")
            lines.append(f"| {date} | {home} vs {away} | {hg} - {ag} | **{result}** |")
        lines.append("")

    except Exception as e:
        lines.append(f"⚠️ 近期状态数据获取失败: {e}")
        lines.append("")

    # 3. 总结
    lines.extend([
        "---",
        "",
        "## 📋 总结",
        "",
        f"- **{team1_name}** 在 H2H 中 "
        f"{'占优' if home_wins > away_wins else ('劣势' if home_wins < away_wins else '与对手势均力敌')}"
        f" ({home_wins}胜 {draws}平 {away_wins}负)",
        f"- **{team1_name}** 近期状态: {t1_wins}胜{t1_losses}负",
        f"- **{team2_name}** 近期状态: {t2_wins}胜{t2_losses}负",
        "",
        "> ⚠️ 本报告仅提供客观数据参考，不构成任何预测或博彩建议。",
        "",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="足球赛前预览分析")
    parser.add_argument("--team1", required=True, help="主队名称或 ID")
    parser.add_argument("--team2", required=True, help="客队名称或 ID")
    parser.add_argument("--league", help="联赛名称（辅助搜索球队）")

    args = parser.parse_args()

    config = load_config()
    client = get_api_client(config)

    if not client:
        print("❌ 未配置 API Key！")
        sys.exit(1)

    try:
        # 解析球队 ID
        t1_id = int(args.team1) if args.team1.isdigit() else get_team_id_by_name(
            client, args.team1, args.league)
        t2_id = int(args.team2) if args.team2.isdigit() else get_team_id_by_name(
            client, args.team2, args.league)

        # 获取名称
        t1_data = client.get_teams(team_id=t1_id)
        t2_data = client.get_teams(team_id=t2_id)
        t1_name = t1_data["response"][0]["team"]["name"]
        t2_name = t2_data["response"][0]["team"]["name"]

        # 生成报告
        report = generate_preview(t1_name, t2_name, t1_id, t2_id, client, args.league)
        print(report)

    except QuotaExceededError as e:
        print(f"❌ {e}")
        sys.exit(2)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(3)


if __name__ == "__main__":
    main()
