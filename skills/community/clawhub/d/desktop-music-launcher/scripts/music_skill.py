#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
music_skill.py
发现本机音乐软件，启动软件，并基于已安装软件构造搜索/播放入口。
控制版增强：
- macOS 下支持 Spotify / Music.app 的 AppleScript 控制
- 支持 play/pause/next/previous/status
- 支持对查询执行“尽力开始播放”的 UI 自动化模式（需要辅助功能 + 自动化权限）
- 对 Spotify 提供可选的 Web API 精确搜索 + 轨道 URI 播放链路（需要用户自行提供 access token）
默认只做本机安全操作：扫描、启动可执行文件、打开 URI/网页、将本地文件交给播放器、
在 macOS 上调用 osascript 执行可审计的 AppleScript。
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
import urllib.error
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
RESOURCE_DIR = ROOT_DIR / "resources"
APPS_FILE = RESOURCE_DIR / "music_apps.json"
RECOMMEND_FILE = RESOURCE_DIR / "recommendation_profiles.json"


def load_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"资源文件不存在: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"资源文件格式错误: {path} -> {exc}")


def current_os() -> str:
    raw = platform.system().lower()
    if raw.startswith("darwin"):
        return "macos"
    if raw.startswith("windows"):
        return "windows"
    return "linux"


def expand_path(p: str) -> str:
    return os.path.expandvars(os.path.expanduser(p))


def which_all(commands: List[str]) -> List[str]:
    hits = []
    for cmd in commands:
        real = cmd.strip()
        if not real or " " in real:
            continue
        found = shutil.which(real)
        if found:
            hits.append(found)
    return sorted(set(hits))


def run_command(command: List[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def has_osascript() -> bool:
    return bool(shutil.which("osascript"))


def open_target(target: str, app_name: Optional[str] = None) -> Dict[str, Any]:
    os_name = current_os()
    try:
        if os_name == "windows":
            os.startfile(target)  # type: ignore[attr-defined]
        elif os_name == "macos":
            cmd = ["open"]
            if app_name:
                cmd.extend(["-a", app_name])
            cmd.append(target)
            run_command(cmd)
        else:
            opener = shutil.which("xdg-open")
            if not opener:
                raise RuntimeError("找不到 xdg-open")
            run_command([opener, target])
        return {"ok": True, "target": target, "app": app_name}
    except Exception as exc:
        return {"ok": False, "target": target, "app": app_name, "error": str(exc)}


def launch_command_string(command: str, extra_args: Optional[List[str]] = None) -> Dict[str, Any]:
    extra_args = extra_args or []
    try:
        if current_os() == "windows":
            parts = command.split()
            if len(parts) == 1 and shutil.which(parts[0]):
                subprocess.Popen([parts[0], *extra_args])
            else:
                subprocess.Popen(command if not extra_args else f'{command} {" ".join(extra_args)}', shell=True)
        else:
            parts = command.split()
            subprocess.Popen(parts + extra_args)
        return {"ok": True, "command": command, "args": extra_args}
    except Exception as exc:
        return {"ok": False, "command": command, "args": extra_args, "error": str(exc)}


def exists_any(paths: List[str]) -> List[str]:
    hits = []
    for path_str in paths:
        real = expand_path(path_str)
        if Path(real).exists():
            hits.append(real)
    return hits


def detect_apps() -> List[Dict[str, Any]]:
    os_name = current_os()
    catalog = load_json(APPS_FILE)["apps"]
    results: List[Dict[str, Any]] = []

    for app in catalog:
        platform_info = app.get("platforms", {}).get(os_name)
        if not platform_info:
            continue

        matched_paths = exists_any(platform_info.get("paths", []) + platform_info.get("app_paths", []))
        matched_bins = which_all(platform_info.get("commands", []))

        installed = bool(matched_paths or matched_bins)
        results.append({
            "id": app["id"],
            "label": app["label"],
            "os": os_name,
            "installed": installed,
            "matched_paths": matched_paths,
            "matched_bins": matched_bins,
            "supports": platform_info.get("supports", []),
            "search_uri_template": platform_info.get("search_uri_template"),
            "search_web_template": platform_info.get("search_web_template"),
        })

    return results


def choose_app(app_id: Optional[str] = None, capability: Optional[str] = None) -> Dict[str, Any]:
    apps = detect_apps()
    installed = [a for a in apps if a["installed"]]
    if app_id:
        for app in installed:
            if app["id"] == app_id:
                if capability and capability not in app.get("supports", []):
                    raise SystemExit(f"已安装 {app_id}，但不支持能力: {capability}")
                return app
        raise SystemExit(f"未找到已安装应用: {app_id}")

    if capability:
        for app in installed:
            if capability in app.get("supports", []):
                return app

    if installed:
        return installed[0]

    raise SystemExit("没有检测到已安装音乐软件。请先安装 Spotify / Apple Music / VLC / mpv 等。")


def open_app(app_id: Optional[str]) -> Dict[str, Any]:
    target = choose_app(app_id=app_id, capability="open")
    if target["matched_paths"]:
        executable = target["matched_paths"][0]
        try:
            subprocess.Popen([executable])
            return {"ok": True, "method": "path", "app": target["id"], "target": executable}
        except Exception as exc:
            return {"ok": False, "method": "path", "app": target["id"], "target": executable, "error": str(exc)}

    if target["matched_bins"]:
        cmd = Path(target["matched_bins"][0]).name
        return launch_command_string(cmd)

    if current_os() == "macos":
        label = target["label"].split(" / ")[0]
        return launch_command_string("open", ["-a", label])

    return {"ok": False, "app": target["id"], "error": "找不到可启动路径或命令"}


def format_template(template: str, query: str) -> str:
    encoded = urllib.parse.quote(query)
    return template.replace("{query}", encoded)


def search_music(query: str, app_id: Optional[str], auto_open: bool) -> Dict[str, Any]:
    try:
        target = choose_app(app_id=app_id, capability=None)
    except SystemExit:
        target = {
            "id": "browser-fallback",
            "search_web_template": "https://open.spotify.com/search/{query}",
            "supports": ["search_web"],
        }

    result: Dict[str, Any] = {"app": target["id"], "query": query, "auto_open": auto_open}

    uri_template = target.get("search_uri_template")
    web_template = target.get("search_web_template")

    if uri_template:
        uri = format_template(uri_template, query)
        result["target"] = uri
        result["method"] = "uri"
        if auto_open:
            result["open_result"] = open_target(uri)
        return result

    if web_template:
        url = format_template(web_template, query)
        result["target"] = url
        result["method"] = "web"
        if auto_open:
            result["open_result"] = open_target(url)
        return result

    result["warning"] = "该应用不支持直接搜索入口，已返回 query，请手动在应用内搜索。"
    return result


def applescript_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def run_osascript(script: str) -> Dict[str, Any]:
    if current_os() != "macos":
        return {"ok": False, "error": "AppleScript 仅支持 macOS"}
    if not has_osascript():
        return {"ok": False, "error": "当前系统缺少 osascript"}

    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            check=True,
        )
        return {
            "ok": True,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except subprocess.CalledProcessError as exc:
        return {
            "ok": False,
            "stdout": (exc.stdout or "").strip(),
            "stderr": (exc.stderr or "").strip(),
            "error": f"AppleScript 执行失败: {exc.returncode}",
        }


def macos_music_app_name() -> str:
    if Path("/System/Applications/Music.app").exists() or Path("/Applications/Music.app").exists():
        return "Music"
    return "iTunes"


def macos_direct_control(app_id: str, action: str) -> Dict[str, Any]:
    if current_os() != "macos":
        return {"ok": False, "app": app_id, "action": action, "error": "控制版仅在 macOS 提供 AppleScript 直控"}

    if app_id == "spotify":
        scripts = {
            "play": 'tell application "Spotify" to play',
            "pause": 'tell application "Spotify" to pause',
            "playpause": 'tell application "Spotify" to playpause',
            "next": 'tell application "Spotify" to next track',
            "previous": 'tell application "Spotify" to previous track',
            "status": textwrap.dedent("""\
                tell application "Spotify"
                  if not running then
                    return "not_running"
                  end if
                  set s to player state as text
                  set trackName to ""
                  set artistName to ""
                  try
                    set trackName to name of current track
                    set artistName to artist of current track
                  end try
                  return s & "|" & artistName & "|" & trackName
                end tell
            """),
        }
    elif app_id == "apple-music":
        app_name = macos_music_app_name()
        scripts = {
            "play": f'tell application "{app_name}" to play',
            "pause": f'tell application "{app_name}" to pause',
            "playpause": textwrap.dedent(f"""\
                tell application "{app_name}"
                  if player state is playing then
                    pause
                  else
                    play
                  end if
                end tell
            """),
            "next": f'tell application "{app_name}" to next track',
            "previous": f'tell application "{app_name}" to previous track',
            "status": textwrap.dedent(f"""\
                tell application "{app_name}"
                  if not running then
                    return "not_running"
                  end if
                  set s to player state as text
                  set trackName to ""
                  set artistName to ""
                  try
                    set trackName to name of current track
                    set artistName to artist of current track
                  end try
                  return s & "|" & artistName & "|" & trackName
                end tell
            """),
        }
    else:
        return {"ok": False, "app": app_id, "action": action, "error": "当前只支持 Spotify 和 Apple Music 的控制直连"}

    script = scripts.get(action)
    if not script:
        return {"ok": False, "app": app_id, "action": action, "error": f"不支持的动作: {action}"}

    result = run_osascript(script)
    payload = {"app": app_id, "action": action, **result}

    if action == "status" and result.get("ok"):
        raw = result.get("stdout", "")
        if raw == "not_running":
            payload["state"] = "not_running"
        else:
            state, artist, track = (raw.split("|", 2) + ["", "", ""])[:3]
            payload["state"] = state
            payload["artist"] = artist
            payload["track"] = track
    return payload


def spotify_access_token(cli_token: Optional[str] = None) -> Optional[str]:
    return cli_token or os.environ.get("SPOTIFY_ACCESS_TOKEN") or None


def spotify_search_top_track(query: str, token: str, market: Optional[str] = None) -> Dict[str, Any]:
    params = {"q": query, "type": "track", "limit": "1"}
    if market:
        params["market"] = market
    url = "https://api.spotify.com/v1/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {
            "ok": False,
            "query": query,
            "error": f"Spotify Search API HTTP {exc.code}",
            "details": body[:500],
        }
    except Exception as exc:
        return {"ok": False, "query": query, "error": f"Spotify Search API 请求失败: {exc}"}

    items = (((payload or {}).get("tracks") or {}).get("items") or [])
    if not items:
        return {"ok": False, "query": query, "error": "Spotify Search API 未返回匹配歌曲"}

    item = items[0]
    artists = ", ".join(a.get("name", "") for a in item.get("artists", []))
    return {
        "ok": True,
        "query": query,
        "track_name": item.get("name", ""),
        "artist_name": artists,
        "album_name": (item.get("album") or {}).get("name", ""),
        "spotify_uri": item.get("uri", ""),
        "external_url": ((item.get("external_urls") or {}).get("spotify", "")),
        "id": item.get("id", ""),
        "source": "spotify-web-api",
    }


def macos_spotify_play_track_uri(track_uri: str) -> Dict[str, Any]:
    script = textwrap.dedent(f"""\
        tell application "Spotify"
          activate
          play track "{applescript_escape(track_uri)}"
          delay 0.4
          return "playing"
        end tell
    """)
    result = run_osascript(script)
    return {"app": "spotify", "method": "spotify_track_uri", "track_uri": track_uri, **result}


def macos_spotify_quick_search_play(query: str, wait_seconds: float = 0.9) -> Dict[str, Any]:
    q = applescript_escape(query)
    script = textwrap.dedent(f"""\
        tell application "Spotify" to activate
        delay 0.5
        tell application "System Events"
          keystroke "k" using command down
          delay 0.25
          keystroke "{q}"
          delay {wait_seconds}
          key code 36
        end tell
        return "submitted_quick_search_play"
    """)
    result = run_osascript(script)
    return {
        "app": "spotify",
        "query": query,
        "method": "spotify_quick_search_enter",
        "requires_permissions": ["Accessibility", "Automation"],
        "best_effort": True,
        "warning": "未提供 Spotify access token，已使用桌面快速搜索回车播放首个候选；结果受当前客户端 UI 与排序影响。",
        **result,
    }


def macos_apple_music_ui_play_query(query: str, wait_seconds: float = 2.2) -> Dict[str, Any]:
    q = applescript_escape(query)
    app_name = macos_music_app_name()
    target = f"musics://music.apple.com/us/search?term={urllib.parse.quote(query)}"
    script = textwrap.dedent(f"""\
        open location "{target}"
        delay {wait_seconds}
        tell application "{app_name}" to activate
        delay 0.6
        tell application "System Events"
          keystroke "f" using command down
          delay 0.3
          keystroke "{q}"
          delay 0.8
          key code 36
          delay 0.6
          key code 36
        end tell
        return "submitted_music_search_play"
    """)
    result = run_osascript(script)
    return {
        "app": "apple-music",
        "query": query,
        "method": "apple_music_search_ui",
        "requires_permissions": ["Accessibility", "Automation"],
        "best_effort": True,
        **result,
    }


def macos_ui_play_query(
    app_id: str,
    query: str,
    spotify_token: Optional[str] = None,
    spotify_market: Optional[str] = None,
) -> Dict[str, Any]:
    if current_os() != "macos":
        return {"ok": False, "app": app_id, "query": query, "error": "UI 自动化仅支持 macOS"}
    if app_id not in {"spotify", "apple-music"}:
        return {"ok": False, "app": app_id, "query": query, "error": "UI 自动化目前仅支持 Spotify 和 Apple Music"}

    if app_id == "spotify":
        token = spotify_access_token(spotify_token)
        if token:
            search_result = spotify_search_top_track(query, token, spotify_market)
            if search_result.get("ok") and search_result.get("spotify_uri"):
                play_result = macos_spotify_play_track_uri(search_result["spotify_uri"])
                merged = {
                    "app": "spotify",
                    "query": query,
                    "lookup": search_result,
                    "lookup_mode": "spotify-web-api",
                    **play_result,
                }
                return merged
            return {
                "app": "spotify",
                "query": query,
                "lookup_mode": "spotify-web-api",
                "lookup": search_result,
                "fallback_attempted": True,
                "fallback": macos_spotify_quick_search_play(query),
                "warning": "Spotify API 精确查找失败，已退化到桌面快速搜索播放。",
            }
        return macos_spotify_quick_search_play(query)

    return macos_apple_music_ui_play_query(query)


def play_music(
    query: Optional[str],
    app_id: Optional[str],
    file_path: Optional[str],
    url: Optional[str],
    auto_open: bool,
    control_mode: str = "auto",
    spotify_token: Optional[str] = None,
    spotify_market: Optional[str] = None,
) -> Dict[str, Any]:
    if file_path and url:
        raise SystemExit("--file 与 --url 不能同时使用")

    if file_path:
        target = choose_app(app_id=app_id, capability="play_file")
        real = expand_path(file_path)
        if not Path(real).exists():
            raise SystemExit(f"本地文件不存在: {real}")
        result = {"app": target["id"], "method": "play_file", "target": real, "auto_open": auto_open}
        if auto_open:
            if target["matched_paths"]:
                executable = target["matched_paths"][0]
                try:
                    subprocess.Popen([executable, real])
                    result["open_result"] = {"ok": True, "method": "path+arg", "app": target["id"], "target": real}
                except Exception as exc:
                    result["open_result"] = {"ok": False, "error": str(exc)}
            elif target["matched_bins"]:
                cmd = Path(target["matched_bins"][0]).name
                result["open_result"] = launch_command_string(cmd, [real])
        return result

    if url:
        target = choose_app(app_id=app_id, capability="play_url")
        result = {"app": target["id"], "method": "play_url", "target": url, "auto_open": auto_open}
        if auto_open:
            if target["matched_paths"]:
                executable = target["matched_paths"][0]
                try:
                    subprocess.Popen([executable, url])
                    result["open_result"] = {"ok": True, "method": "path+arg", "app": target["id"], "target": url}
                except Exception as exc:
                    result["open_result"] = {"ok": False, "error": str(exc)}
            elif target["matched_bins"]:
                cmd = Path(target["matched_bins"][0]).name
                result["open_result"] = launch_command_string(cmd, [url])
        return result

    if not query:
        raise SystemExit("未提供要播放的 query / file / url")

    target = None
    try:
        target = choose_app(app_id=app_id, capability=None)
    except SystemExit:
        pass

    if target and current_os() == "macos" and target["id"] in {"spotify", "apple-music"} and control_mode in {"auto", "macos-ui"}:
        return macos_ui_play_query(target["id"], query, spotify_token=spotify_token, spotify_market=spotify_market)

    return search_music(query=query, app_id=app_id, auto_open=auto_open)


def recommend(query: str, top_k: int = 3) -> Dict[str, Any]:
    rec = load_json(RECOMMEND_FILE)
    profiles = rec.get("profiles", {})
    matches = []

    lowered = query.lower()
    for key, profile in profiles.items():
        score = 0
        for kw in profile.get("keywords", []):
            if kw.lower() in lowered:
                score += 1
        if score > 0:
            matches.append((score, key, profile))

    matches.sort(key=lambda item: (-item[0], item[1]))

    suggestions: List[Dict[str, Any]] = []
    if matches:
        for _, key, profile in matches[:top_k]:
            for item in profile.get("suggestions", [])[:top_k]:
                suggestions.append({
                    "profile": key,
                    "description": profile.get("description", ""),
                    "query": item["query"],
                    "reason": item["reason"],
                })
    else:
        for item in rec.get("fallback", [])[:top_k]:
            suggestions.append({
                "profile": "fallback",
                "description": "未识别明确场景，给出通用候选",
                "query": item["query"],
                "reason": item["reason"],
            })

    seen = set()
    unique = []
    for item in suggestions:
        if item["query"] in seen:
            continue
        seen.add(item["query"])
        unique.append(item)

    return {
        "input": query,
        "top_k": top_k,
        "suggestions": unique[:top_k],
        "hint": "可将 suggestions[0].query 继续用于 search 或 play 命令",
    }


def control_app(app_id: str, action: str) -> Dict[str, Any]:
    return macos_direct_control(app_id, action)


def print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="本机音乐软件技能脚本（控制增强版）")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("scan", help="扫描本机已安装音乐软件")

    p_open = sub.add_parser("open", help="打开音乐软件")
    p_open.add_argument("--app", dest="app_id", help="指定应用 ID，例如 spotify / vlc")

    p_search = sub.add_parser("search", help="在音乐软件中搜索歌曲/歌手/专辑")
    p_search.add_argument("query", help="要搜索的内容")
    p_search.add_argument("--app", dest="app_id", help="指定应用 ID")
    p_search.add_argument("--open", action="store_true", dest="auto_open", help="直接打开 URI/网页")

    p_play = sub.add_parser("play", help="播放歌曲、文件或 URL")
    p_play.add_argument("query", nargs="?", help="歌曲/歌手/关键词")
    p_play.add_argument("--app", dest="app_id", help="指定应用 ID")
    p_play.add_argument("--file", dest="file_path", help="要交给播放器播放的本地文件路径")
    p_play.add_argument("--url", dest="url", help="要交给播放器播放的网络 URL")
    p_play.add_argument("--open", action="store_true", dest="auto_open", help="直接打开结果")
    p_play.add_argument(
        "--control-mode",
        choices=["auto", "basic", "macos-ui"],
        default="auto",
        help="auto: 自动选择；basic: 只走普通打开/搜索；macos-ui: 强制使用 macOS 控制链路",
    )
    p_play.add_argument(
        "--spotify-token",
        dest="spotify_token",
        help="可选：Spotify Web API access token；未提供时，也可从环境变量 SPOTIFY_ACCESS_TOKEN 读取",
    )
    p_play.add_argument(
        "--spotify-market",
        dest="spotify_market",
        help="可选：Spotify 搜索市场，例如 JP / TW / HK / US",
    )

    p_ctrl = sub.add_parser("control", help="控制播放器状态（macOS 下支持 Spotify / Apple Music）")
    p_ctrl.add_argument("--app", required=True, dest="app_id", help="spotify / apple-music")
    p_ctrl.add_argument(
        "--action",
        required=True,
        choices=["play", "pause", "playpause", "next", "previous", "status"],
        help="控制动作",
    )

    p_recommend = sub.add_parser("recommend", help="根据场景或情绪推荐可搜索的歌单/歌曲方向")
    p_recommend.add_argument("query", help="例如：适合写代码的歌 / 跑步音乐 / 失恋听什么")
    p_recommend.add_argument("-k", "--top-k", type=int, default=3, dest="top_k", help="返回候选数量，默认 3")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scan":
        print_json({"os": current_os(), "apps": detect_apps(), "has_osascript": has_osascript()})
        return
    if args.command == "open":
        print_json(open_app(args.app_id))
        return
    if args.command == "search":
        print_json(search_music(args.query, args.app_id, args.auto_open))
        return
    if args.command == "play":
        print_json(play_music(
            args.query,
            args.app_id,
            args.file_path,
            args.url,
            args.auto_open,
            args.control_mode,
            args.spotify_token,
            args.spotify_market,
        ))
        return
    if args.command == "control":
        print_json(control_app(args.app_id, args.action))
        return
    if args.command == "recommend":
        print_json(recommend(args.query, args.top_k))
        return

    parser.print_help()
    raise SystemExit(1)


if __name__ == "__main__":
    main()
