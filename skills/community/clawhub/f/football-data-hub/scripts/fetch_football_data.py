#!/usr/bin/env python3
"""
Football Data Hub - 足球数据获取脚本
三级数据源：openligadb (零配置) → API-Football (RapidAPI) → football-data.org

用法:
  python fetch_football_data.py --endpoint standings --league "德甲"
  python fetch_football_data.py --endpoint standings --league "Premier League" --season 2025
  python fetch_football_data.py --endpoint fixtures --league "bl1" --season 2025
  python fetch_football_data.py --endpoint teams --search "Bayern"
  python fetch_football_data.py --endpoint fixtures --league "bl1" --matchday 1
  python fetch_football_data.py --endpoint leagues
"""

import argparse
import json
import os
import sys
import time

# Windows 编码兼容：仅在非交互式管道输出时强制 UTF-8
if sys.platform == "win32" and not sys.stdout.isatty():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import yaml

try:
    import requests
except ImportError:
    print("请安装 requests: pip install requests pyyaml")
    sys.exit(1)

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = SKILL_DIR / "config.yaml"
CONFIG_EXAMPLE = SKILL_DIR / "config.example.yaml"

# 中文名 → openligadb shortcut 映射（覆盖主要联赛）
OL_SHORTCUT_MAP = {
    "德甲": "bl1", "bundesliga": "bl1",
    "德乙": "bl2", "2. bundesliga": "bl2",
    "德丙": "bl3", "3. liga": "bl3",
    "德国杯": "dfb", "dfb-pokal": "dfb",
    "英超": "eng_prem", "premier league": "eng_prem", "pl": "eng_prem",
    "西甲": "spa_laliga", "la liga": "spa_laliga",
    "意甲": "ita_seriea", "serie a": "ita_seriea",
    "法甲": "fra_ligue1", "ligue 1": "fra_ligue1",
    "欧冠": "ucl", "champions league": "ucl",
    "欧联": "el", "europa league": "el",
}

# ──────────────────────────────────────────────────────────────────────────
# OpenLigaDB 客户端 (零配置，无需 API Key)
# ──────────────────────────────────────────────────────────────────────────

class OpenLigaDBClient:
    """OpenLigaDB — 完全免费、无需认证的足球数据 API"""

    BASE_URL = "https://api.openligadb.de"
    _league_cache = None  # 联赛列表缓存

    @classmethod
    def _get(cls, endpoint: str) -> dict:
        url = f"{cls.BASE_URL}/{endpoint}"
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()

    @classmethod
    def get_leagues(cls) -> list:
        """获取所有可用联赛"""
        if cls._league_cache is None:
            cls._league_cache = cls._get("getavailableleagues")
        return cls._league_cache

    @classmethod
    def find_league(cls, query: str, season: int = None) -> Optional[dict]:
        """按名称/快捷名搜索联赛，返回最佳匹配"""
        q = query.lower().strip()

        # 1. 先查 shortcut 映射
        shortcut = OL_SHORTCUT_MAP.get(q)
        if shortcut:
            for lg in cls.get_leagues():
                if lg["leagueShortcut"].lower() == shortcut.lower():
                    # leagueSeason 是字符串，比较时统一转 int
                    s = int(lg.get("leagueSeason", 0))
                    if season and s != season:
                        continue
                    return lg
            # shortcut 映射的没找到当前赛季，找最新
            best = None
            best_year = 0
            tgt = season or datetime.now().year
            for lg in cls.get_leagues():
                if lg["leagueShortcut"].lower() == shortcut.lower():
                    sy = int(lg.get("leagueSeason", 0))
                    # 优先匹配目标赛季，其次选最近的
                    if sy == tgt:
                        return lg
                    if season:
                        if 0 < abs(sy - tgt) < abs(best_year - tgt) or best is None:
                            best = lg
                            best_year = sy
                    else:
                        if sy > best_year:
                            best = lg
                            best_year = sy
            return best

        # 2. 模糊搜索
        matches = []
        for lg in cls.get_leagues():
            name = lg["leagueName"].lower()
            if q in name:
                matches.append(lg)

        if not matches:
            return None

        # 有 season 时精确匹配
        if season:
            exact = [m for m in matches if int(m.get("leagueSeason", 0)) == season]
            if exact:
                return exact[0]

        # 返回最新赛季
        return max(matches, key=lambda m: int(m.get("leagueSeason", 0)))

    @classmethod
    def get_standings(cls, league_shortcut: str, season: int) -> list:
        """获取积分榜 (返回 list of team dicts)"""
        data = cls._get(f"getbltable/{league_shortcut}/{season}")
        # openligadb 不返回排名，按积分排序
        data.sort(key=lambda t: (-t["points"], -t["goalDiff"], -t["goals"]))
        for i, t in enumerate(data):
            t["rank"] = i + 1
        return data

    @classmethod
    def get_fixtures(cls, league_shortcut: str, season: int) -> list:
        """获取该赛季所有比赛"""
        return cls._get(f"getmatchdata/{league_shortcut}/{season}")

    @classmethod
    def get_matchday_fixtures(cls, league_shortcut: str, season: int,
                               matchday: int) -> list:
        """获取指定轮次比赛"""
        return cls._get(f"getmatchdata/{league_shortcut}/{season}/{matchday}")

    @classmethod
    def get_current_matchday(cls, league_shortcut: str, season: int = None) -> int:
        """获取当前轮次"""
        if season is None:
            season = datetime.now().year
        return cls._get(f"getcurrentgroup/{league_shortcut}/{season}")

    @classmethod
    def get_team_info(cls, team_name: str) -> Optional[dict]:
        """按名称搜索球队 (仅覆盖 openligadb 内数据)"""
        current_year = datetime.now().year
        for shortcut in ["bl1", "bl2", "bl3"]:
            for yr in (current_year, current_year - 1):
                try:
                    standings = cls.get_standings(shortcut, yr)
                    for t in standings:
                        if team_name.lower() in t["teamName"].lower():
                            return {
                                "name": t["teamName"],
                                "shortName": t.get("shortName", ""),
                                "iconUrl": t.get("teamIconUrl", ""),
                                "league": shortcut.upper(),
                                "season": yr,
                            }
                except Exception:
                    continue
        return None

    @classmethod
    def search_all_leagues(cls, keyword: str) -> list:
        """搜索所有联赛中包含关键词的"""
        results = []
        k = keyword.lower()
        for lg in cls.get_leagues():
            if k in lg["leagueName"].lower() or k in lg["leagueShortcut"].lower():
                results.append(lg)
        # 按赛季降序
        results.sort(key=lambda r: r.get("leagueSeason", 0), reverse=True)
        return results[:30]


# ──────────────────────────────────────────────────────────────────────────
# API-Football 客户端 (需要 RapidAPI Key)
# ──────────────────────────────────────────────────────────────────────────

class ApiFootballClient:
    BASE_URL = "https://v3.football.api-sports.io"
    RATE_LIMIT_INTERVAL = 1.2

    def __init__(self, rapidapi_key: str):
        self.session = requests.Session()
        self.session.headers.update({
            "X-RapidAPI-Key": rapidapi_key,
            "X-RapidAPI-Host": "v3.football.api-sports.io",
        })
        self.last_request = 0

    def _rate_limit(self):
        elapsed = time.time() - self.last_request
        if elapsed < self.RATE_LIMIT_INTERVAL:
            time.sleep(self.RATE_LIMIT_INTERVAL - elapsed)
        self.last_request = time.time()

    def _get(self, endpoint: str, params: dict = None) -> dict:
        self._rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/{endpoint}", params=params or {}, timeout=15)
        if resp.status_code == 429:
            raise QuotaExceededError("API-Football 配额耗尽")
        resp.raise_for_status()
        data = resp.json()
        if data.get("errors"):
            raise ApiError(str(data["errors"]))
        return data

    def get_leagues(self, search: str = None) -> dict:
        return self._get("leagues", {"search": search} if search else {})

    def get_standings(self, league_id: int, season: int = None) -> dict:
        return self._get("standings", {"league": league_id, "season": season or datetime.now().year})

    def get_fixtures(self, **kwargs) -> dict:
        params = {k: v for k, v in kwargs.items() if v is not None
                  and k in ("league", "season", "team", "date", "from", "to",
                            "live", "status", "next", "last")}
        return self._get("fixtures", params)

    def get_teams(self, **kwargs) -> dict:
        params = {}
        if kwargs.get("team_id"):
            return self._get("teams", {"id": kwargs["team_id"]})
        if kwargs.get("search"):
            params["search"] = kwargs["search"]
        if kwargs.get("league_id"):
            params["league"] = kwargs["league_id"]
        if kwargs.get("season"):
            params["season"] = kwargs["season"]
        return self._get("teams", params)

    def get_players(self, team_id: int = None, season: int = None,
                     search: str = None, player_id: int = None) -> dict:
        params = {}
        if player_id:
            return self._get("players", {"id": player_id, "season": season or datetime.now().year})
        if search:
            params["search"] = search
        if team_id:
            params["team"] = team_id
        if season:
            params["season"] = season
        return self._get("players", params)

    def get_h2h(self, team1_id: int, team2_id: int, last: int = 10) -> dict:
        return self._get("fixtures/headtohead", {"h2h": f"{team1_id}-{team2_id}", "last": last})


# ──────────────────────────────────────────────────────────────────────────
# football-data.org 客户端 (需要 API Key)
# ──────────────────────────────────────────────────────────────────────────

class FootballDataClient:
    BASE_URL = "https://api.football-data.org/v4"

    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.session.headers.update({"X-Auth-Token": api_key})
        self.last_request = 0

    def _rate_limit(self):
        elapsed = time.time() - self.last_request
        if elapsed < 6.0:
            time.sleep(6.0 - elapsed)
        self.last_request = time.time()

    def _get(self, endpoint: str, params: dict = None) -> dict:
        self._rate_limit()
        resp = self.session.get(f"{self.BASE_URL}/{endpoint}", params=params, timeout=15)
        if resp.status_code == 429:
            raise QuotaExceededError("football-data.org 请求过于频繁")
        resp.raise_for_status()
        return resp.json()

    def get_standings(self, competition_code: str) -> dict:
        return self._get(f"competitions/{competition_code}/standings")

    def get_matches(self, competition_code: str = None, **kwargs) -> dict:
        params = {}
        for k in ("dateFrom", "dateTo", "status", "matchday"):
            if k in kwargs and kwargs[k] is not None:
                params[k] = kwargs[k]
        if competition_code:
            return self._get(f"competitions/{competition_code}/matches", params)
        return self._get("matches", params)


# ──────────────────────────────────────────────────────────────────────────
# 异常 & 客户端工厂
# ──────────────────────────────────────────────────────────────────────────

class ApiError(Exception):
    pass


class QuotaExceededError(ApiError):
    pass


def load_config() -> dict:
    for cfg in [CONFIG_FILE, CONFIG_EXAMPLE]:
        if cfg.exists():
            with open(cfg, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
    return {}


def get_client(config: dict):
    """按优先级返回客户端: API-Football → football-data.org → None (降级到 openligadb)"""
    af_key = config.get("api_football", {}).get("rapidapi_key", "")
    if af_key and af_key not in ("YOUR_RAPIDAPI_KEY_HERE", ""):
        return ApiFootballClient(af_key), "api-football"
    fd_key = config.get("football_data", {}).get("api_key", "")
    if fd_key and fd_key not in ("YOUR_API_KEY_HERE", ""):
        return FootballDataClient(fd_key), "football-data"
    return None, "openligadb"


# ──────────────────────────────────────────────────────────────────────────
# 格式化输出
# ──────────────────────────────────────────────────────────────────────────

def format_ol_standings(data: list, league_name: str, season: int) -> str:
    """格式化 openligadb 积分榜"""
    lines = [f"## 📊 {league_name} 积分榜 ({season})", ""]
    lines.append("| # | 球队 | 场次 | 胜 | 平 | 负 | 进球 | 失球 | 净胜 | 积分 |")
    lines.append("|---|------|------|----|----|----|------|------|------|------|")

    for t in data:
        rank = t.get("rank", "?")
        name = t["teamName"]
        pld = t["matches"]
        w, d, l = t["won"], t["draw"], t["lost"]
        gf, ga = t["goals"], t["opponentGoals"]
        gd = t["goalDiff"]
        pts = t["points"]
        indicator = " 🏆" if rank == 1 else (" 🔵" if isinstance(rank, int) and rank <= 4 else "")
        lines.append(f"| {rank}{indicator} | {name} | {pld} | {w} | {d} | {l} | {gf} | {ga} | {gd} | **{pts}** |")

    lines.append("")
    lines.append(f"> 数据来源: OpenLigaDB (免费公开数据)")
    return "\n".join(lines)


def format_ol_fixtures(matches: list, league_name: str, matchday: int = None) -> str:
    """格式化 openligadb 比赛数据"""
    title = f"📅 {league_name}"
    if matchday:
        title += f" 第{matchday}轮"
    lines = [f"## {title} ({len(matches)} 场)", ""]
    lines.append("| 日期 | 主队 | 比分 | 客队 |")
    lines.append("|------|------|------|------|")

    for m in matches:
        dt = m.get("matchDateTime", "?")[:16].replace("T", " ")
        t1 = m["team1"]["teamName"]
        t2 = m["team2"]["teamName"]

        results = m.get("matchResults", [])
        if results and len(results) >= 2:
            # 最终结果
            r = results[-1]
            s1, s2 = r.get("pointsTeam1", "?"), r.get("pointsTeam2", "?")
            score = f"{s1} - {s2}"
        elif results:
            r = results[-1]
            s1, s2 = r.get("pointsTeam1", "?"), r.get("pointsTeam2", "?")
            score = f"{s1} - {s2} (HT)"
        else:
            score = "vs"

        lines.append(f"| {dt} | {t1} | {score} | {t2} |")

    lines.append("")
    lines.append(f"> 数据来源: OpenLigaDB (免费公开数据)")
    return "\n".join(lines)


def format_ol_leagues(leagues: list) -> str:
    """格式化联赛列表"""
    lines = ["## 🏆 可用联赛 (OpenLigaDB)", ""]
    lines.append("| ID | 联赛名 | 简称 | 赛季 |")
    lines.append("|-----|--------|------|------|")

    shortcuts = set()
    for lg in leagues:
        sc = lg.get("leagueShortcut", "?")
        if sc not in shortcuts:
            shortcuts.add(sc)
            lines.append(f"| {lg['leagueId']} | {lg['leagueName'][:40]} | {sc} | {lg.get('leagueSeason', '?')} |")

    lines.append("")
    lines.append(f"> 共 {len(leagues)} 个联赛，{len(shortcuts)} 个独立赛事")
    lines.append("> 常用: `bl1`(德甲) `bl2`(德乙) `bl3`(德丙) `dfb`(德国杯) `cl`(欧冠) `el`(欧联)")
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────────
# 主入口
# ──────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Football Data Hub - 足球数据查询")
    parser.add_argument("--endpoint", required=True,
                        choices=["standings", "fixtures", "teams", "players",
                                 "h2h", "leagues"],
                        help="查询端点")
    parser.add_argument("--league", help="联赛名称或 ID/快捷名 (如 bl1, eng_prem)")
    parser.add_argument("--team", help="球队名称")
    parser.add_argument("--team1", type=int, help="H2H 主队 ID")
    parser.add_argument("--team2", type=int, help="H2H 客队 ID")
    parser.add_argument("--search", help="搜索关键词")
    parser.add_argument("--id", type=int, help="球队/球员 ID")
    parser.add_argument("--season", type=int, help="赛季年份")
    parser.add_argument("--matchday", type=int, help="指定轮次")
    parser.add_argument("--next", type=int, help="未来 N 场比赛")
    parser.add_argument("--last", type=int, help="最近 N 场比赛")
    parser.add_argument("--status", help="比赛状态")
    parser.add_argument("--format", default="markdown",
                        choices=["json", "markdown"], help="输出格式")
    parser.add_argument("--raw", action="store_true", help="输出原始 JSON")

    args = parser.parse_args()
    season = args.season or datetime.now().year
    config = load_config()
    client, source = get_client(config)

    # ── 使用 OpenLigaDB (零配置模式) ──
    if source == "openligadb":
        ol = OpenLigaDBClient

        if args.endpoint == "leagues":
            leagues = ol.search_all_leagues(args.search or "")
            print(format_ol_leagues(leagues))
            return

        # teams+search 不需要 league
        if args.endpoint == "teams" and args.search:
            info = ol.get_team_info(args.search)
            if info:
                print(f"## ⚽ {info['name']}")
                print(f"- **联赛**: {info['league']}")
                print(f"- **赛季**: {info['season']}")
                if info.get("iconUrl"):
                    print(f"- **队徽**: {info['iconUrl']}")
            else:
                print(f"⚠️ 未找到球队: {args.search}")
                print("💡 OpenLigaDB 主要覆盖德国联赛球队")
            return

        if not args.league:
            print("❌ 请指定 --league (如: 德甲, Premier League, bl1)")
            print("💡 用 --endpoint leagues 查看所有可用联赛")
            sys.exit(1)

        lg = ol.find_league(args.league, season)
        if not lg:
            print(f"❌ 未找到联赛: {args.league}")
            print(f"💡 试试 --endpoint leagues 查看可用列表")
            sys.exit(1)

        lg_name = lg["leagueName"]
        lg_shortcut = lg["leagueShortcut"]
        lg_season = lg.get("leagueSeason", season)

        try:
            if args.endpoint == "standings":
                data = ol.get_standings(lg_shortcut, lg_season)
                print(format_ol_standings(data, lg_name, lg_season))

            elif args.endpoint == "fixtures":
                if args.matchday:
                    matches = ol.get_matchday_fixtures(lg_shortcut, lg_season, args.matchday)
                else:
                    matches = ol.get_fixtures(lg_shortcut, lg_season)
                    # 按 matchday 分组
                    if args.matchday is None and not args.raw:
                        mds = {}
                        for m in matches:
                            md = m.get("group", {}).get("groupOrderID", 0)
                            mds.setdefault(md, []).append(m)
                        # 显示最新完成的轮次
                        completed = [md for md in sorted(mds.keys())
                                     if any(r.get("matchResults") for r in mds[md])]
                        if completed:
                            latest = completed[-1]
                            matches = mds[latest]
                            print(format_ol_fixtures(matches, lg_name, latest))
                            print(f"💡 查看其他轮次: --matchday N (1-{max(mds.keys())})")
                            return
                        else:
                            # 显示第一轮
                            first = sorted(mds.keys())[0]
                            matches = mds[first]
                            print(format_ol_fixtures(matches, lg_name, first))
                            return
                print(format_ol_fixtures(matches, lg_name, args.matchday))

            elif args.endpoint == "teams":
                data = ol.get_standings(lg_shortcut, lg_season)
                lines = [f"## ⚽ {lg_name} 球队列表 ({lg_season})", ""]
                for t in data:
                    lines.append(f"- **{t['teamName']}** ({t.get('shortName', '')})")
                print("\n".join(lines))

            elif args.endpoint == "players":
                print("⚠️ OpenLigaDB 不支持球员数据查询")
                print("💡 配置 API-Football Key 即可查询球员数据")

            elif args.endpoint == "h2h":
                print("⚠️ OpenLigaDB 不支持 H2H 查询")
                print("💡 配置 API-Football Key 即可查询 H2H 数据")

        except Exception as e:
            print(f"❌ OpenLigaDB 错误: {e}")
            print("💡 提示: 尝试其他联赛或配置 API Key 获取更全面的数据")
            sys.exit(1)

    # ── 使用 API-Football ──
    elif source == "api-football":
        print("⚠️ API-Football 模式待实现 (需要配置 RapidAPI Key)")
        print("💡 当前默认使用 OpenLigaDB 零配置模式")

    # ── 使用 football-data.org ──
    elif source == "football-data":
        print("⚠️ football-data.org 模式待实现 (需要配置 API Key)")
        print("💡 当前默认使用 OpenLigaDB 零配置模式")


if __name__ == "__main__":
    main()
