#!/usr/bin/env bash
# game_query.sh - Cross-platform game library query tool (with Chinese names)
# Usage: game_query.sh <command> [options]
# Commands:
#   list          List all games across platforms (with CN names)
#   steam         List Steam games only
#   epic          List Epic games only
#   search <term> Search games by name across platforms
#   stats         Show library statistics
#   unplayed      List unplayed games (Steam only)
#   recommend     Recommend highly-rated unplayed games (Steam only)
#   cn-update     Update Chinese names cache from Steam API
#   help          Show this help

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
STEAM_CLI="steam"
LEGENDARY_CLI="${LEGENDARY_CLI:-legendary}"
CACHE_DIR="/tmp/game-library-cache"
CACHE_TTL=3600  # 1 hour

mkdir -p "$CACHE_DIR"

# --- CN name helper ---
cn_name() {
    # Returns CN name for an English game name from cache
    local en_name="$1"
    local cache_file="$SKILL_DIR/cn_names_cache.json"
    if [[ -f "$cache_file" ]]; then
        python3 -c "
import json, sys
with open('$cache_file', 'r', encoding='utf-8') as f:
    cache = json.load(f)
target = '$en_name'.strip().lower()
for appid, info in cache.items():
    if info['en'].strip().lower() == target:
        cn = info.get('cn', info['en'])
        if cn != info['en']:
            print(f'{cn} ({info[\"en\"]})')
        else:
            print(info['en'])
        sys.exit(0)
print('$en_name')
" 2>/dev/null || echo "$en_name"
    else
        echo "$en_name"
    fi
}

# --- Cache helpers ---
cache_valid() {
    local f="$CACHE_DIR/$1.json"
    if [[ -f "$f" ]]; then
        local now=$(date +%s)
        local mtime=$(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f" 2>/dev/null || echo 0)
        local age=$(( now - mtime ))
        [[ $age -lt $CACHE_TTL ]]
    else
        false
    fi
}

read_cache() { cat "$CACHE_DIR/$1.json"; }
write_cache() { cat > "$CACHE_DIR/$1.json"; }

# --- Data fetching ---
fetch_steam_library() {
    if cache_valid "steam_library"; then
        read_cache "steam_library"
        return
    fi
    $STEAM_CLI library --limit 500 --json 2>/dev/null | write_cache "steam_library"
    read_cache "steam_library"
}

fetch_epic_library() {
    if cache_valid "epic_library"; then
        read_cache "epic_library"
        return
    fi
    $LEGENDARY_CLI list 2>/dev/null | python3 -c "
import sys, json
games = []
for line in sys.stdin:
    line = line.strip()
    if line.startswith('* '):
        name = line[2:].split('(')[0].strip()
        app_name = ''
        version = ''
        if 'App name:' in line:
            parts = line.split('App name:')
            if len(parts) > 1:
                app_name = parts[1].split('|')[0].split(')')[0].strip()
        if 'Version:' in line:
            parts = line.split('Version:')
            if len(parts) > 1:
                version = parts[1].split(')')[0].strip()
        games.append({'name': name, 'app_name': app_name, 'version': version, 'platform': 'epic'})
print(json.dumps(games))
" | write_cache "epic_library"
    read_cache "epic_library"
}

# --- Display with CN names ---
display_with_cn() {
    # Reads JSON from stdin, displays with Chinese names
    local platform="$1"
    python3 -c "
import json, sys, os

cn_cache = {}
cache_file = os.path.expanduser('$SKILL_DIR/cn_names_cache.json')
if os.path.exists(cache_file):
    with open(cache_file, 'r', encoding='utf-8') as f:
        cn_cache = json.load(f)

# Build lookup: en_name.lower() -> cn_name
cn_lookup = {}
for appid, info in cn_cache.items():
    cn_lookup[info['en'].strip().lower()] = info.get('cn', info['en'])

games = json.load(sys.stdin)
for g in games:
    name = g.get('name', '').strip()
    cn = cn_lookup.get(name.lower(), name)
    if cn != name:
        display = f'{cn}（{name}）'
    else:
        display = name
    
    if '$platform' == 'steam':
        hours = round(g.get('playtime', 0) / 60, 1)
        status = f'{hours}h' if hours > 0 else '未玩'
        print(f'  {display} [{status}]')
    else:
        print(f'  {display}')
" 2>/dev/null
}

# --- Commands ---
cmd_stats() {
    echo "=== 📊 游戏库统计 ==="
    echo ""

    local steam_data
    steam_data=$(fetch_steam_library)
    local steam_count=$(echo "$steam_data" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d))" 2>/dev/null || echo "?")
    local steam_played=$(echo "$steam_data" | python3 -c "import sys,json; d=json.load(sys.stdin); print(sum(1 for g in d if g.get('playtime',0)>0))" 2>/dev/null || echo "?")
    local steam_unplayed=$(echo "$steam_data" | python3 -c "import sys,json; d=json.load(sys.stdin); print(sum(1 for g in d if g.get('playtime',0)==0))" 2>/dev/null || echo "?")
    local steam_hours=$(echo "$steam_data" | python3 -c "import sys,json; d=json.load(sys.stdin); print(round(sum(g.get('playtime',0) for g in d)/60,1))" 2>/dev/null || echo "?")

    echo "🎮 Steam"
    echo "   游戏: $steam_count | 已玩: $steam_played | 未玩: $steam_unplayed | 时长: ${steam_hours}h"

    local epic_data
    epic_data=$(fetch_epic_library)
    local epic_count=$(echo "$epic_data" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d))" 2>/dev/null || echo "?")

    echo ""
    echo "🎮 Epic"
    echo "   游戏: $epic_count | (无游玩时长 API)"

    echo ""
    echo "📦 总计: $((steam_count + epic_count)) 款游戏，横跨 2 个平台"
}

cmd_list() {
    echo "=== 🎮 全部游戏库 ==="
    echo ""
    echo "--- Steam ---"
    fetch_steam_library | display_with_cn steam
    echo ""
    echo "--- Epic ---"
    fetch_epic_library | display_with_cn epic
}

cmd_steam() {
    local args=("$@")
    $STEAM_CLI library "${args[@]}" 2>/dev/null
}

cmd_epic() {
    fetch_epic_library | python3 -c "
import json, sys, os
cn_cache = {}
cache_file = os.path.expanduser('$SKILL_DIR/cn_names_cache.json')
if os.path.exists(cache_file):
    with open(cache_file, 'r', encoding='utf-8') as f:
        cn_cache = json.load(f)
cn_lookup = {}
for appid, info in cn_cache.items():
    cn_lookup[info['en'].strip().lower()] = info.get('cn', info['en'])
games = json.load(sys.stdin)
for g in sorted(games, key=lambda x: x['name'].lower()):
    name = g['name'].strip()
    cn = cn_lookup.get(name.lower(), name)
    display = f'{cn}（{name}）' if cn != name else name
    print(f'  {display}')
" 2>/dev/null
}

cmd_search() {
    local term="${1:-}"
    if [[ -z "$term" ]]; then
        echo "用法: game_query.sh search <关键词>"
        exit 1
    fi

    echo "=== 🔍 搜索: '$term' ==="
    echo ""

    echo "--- Steam ---"
    fetch_steam_library | python3 -c "
import json, sys, os
cn_cache = {}
cache_file = os.path.expanduser('$SKILL_DIR/cn_names_cache.json')
if os.path.exists(cache_file):
    with open(cache_file, 'r', encoding='utf-8') as f:
        cn_cache = json.load(f)
cn_lookup = {}
for appid, info in cn_cache.items():
    cn_lookup[info['en'].strip().lower()] = info.get('cn', info['en'])

term = '$term'.lower()
games = json.load(sys.stdin)
found = [g for g in games if term in g.get('name','').lower() or term in cn_lookup.get(g.get('name','').lower(), '').lower()]
if found:
    for g in found:
        name = g.get('name','').strip()
        cn = cn_lookup.get(name.lower(), name)
        display = f'{cn}（{name}）' if cn != name else name
        hours = round(g.get('playtime',0)/60, 1)
        status = f'{hours}h' if hours > 0 else '未玩'
        print(f'  ✅ {display} [{status}]')
else:
    print('  (未找到)')
"

    echo ""
    echo "--- Epic ---"
    fetch_epic_library | python3 -c "
import json, sys, os
cn_cache = {}
cache_file = os.path.expanduser('$SKILL_DIR/cn_names_cache.json')
if os.path.exists(cache_file):
    with open(cache_file, 'r', encoding='utf-8') as f:
        cn_cache = json.load(f)
cn_lookup = {}
for appid, info in cn_cache.items():
    cn_lookup[info['en'].strip().lower()] = info.get('cn', info['en'])

term = '$term'.lower()
games = json.load(sys.stdin)
found = [g for g in games if term in g.get('name','').lower() or term in cn_lookup.get(g.get('name','').lower(), '').lower()]
if found:
    for g in found:
        name = g['name'].strip()
        cn = cn_lookup.get(name.lower(), name)
        display = f'{cn}（{name}）' if cn != name else name
        print(f'  ✅ {display}')
else:
    print('  (未找到)')
"
}

cmd_unplayed() {
    echo "=== 🕹 未玩游戏 ==="
    echo ""
    echo "--- Steam ---"
    $STEAM_CLI library --unplayed --sort reviews --limit 30 --show-reviews --plain 2>/dev/null
    echo ""
    echo "--- Epic ---"
    echo "(Epic 无游玩时长 API，无法判断)"
}

cmd_recommend() {
    echo "=== ⭐ 高分未玩推荐 (Steam) ==="
    $STEAM_CLI library --unplayed --min-reviews 7 --sort reviews --limit 20 --show-reviews --plain 2>/dev/null
}

cmd_cn_update() {
    echo "更新中文名缓存（从 Steam API 获取）..."
    python3 "$SKILL_DIR/scripts/cn_names.py" update
}

cmd_cn_update_xhh() {
    echo "从小黑盒补充中文名..."
    python3 "$SKILL_DIR/scripts/xhh_cn_names.py"
}

cmd_duplicates() {
    echo "=== 🔄 跨平台重复游戏 ==="
    echo ""
    python3 -c "
import json, sys, os

# Load CN cache
cn_cache = {}
cache_file = os.path.expanduser('$SKILL_DIR/cn_names_cache.json')
if os.path.exists(cache_file):
    with open(cache_file, 'r', encoding='utf-8') as f:
        cn_cache = json.load(f)
cn_lookup = {}
for appid, info in cn_cache.items():
    cn_lookup[info['en'].strip().lower()] = info.get('cn', info['en'])

# Load Steam library
with open('$CACHE_DIR/steam_library.json', 'r') as f:
    steam_games = json.load(f)
steam_names = set()
for g in steam_games:
    name = g.get('name', '').strip()
    steam_names.add(name.lower())

# Load Epic library
with open('$CACHE_DIR/epic_library.json', 'r') as f:
    epic_games = json.load(f)
epic_names = set()
for g in epic_games:
    name = g.get('name', '').strip()
    epic_names.add(name.lower())

# Find duplicates
dupes = steam_names & epic_names
if dupes:
    for name in sorted(dupes):
        cn = cn_lookup.get(name, name)
        # Find original casing from steam
        orig = next((g['name'] for g in steam_games if g['name'].strip().lower() == name), name)
        if cn != name:
            display = f'{cn}（{orig}）'
        else:
            display = orig
        print(f'  🎮 {display}')
    print(f'\n总计: {len(dupes)} 款重复')
else:
    print('  (无重复)')
" 2>/dev/null || echo '  请先运行 list 命令以生成缓存'
}

cmd_help() {
    echo "game_query.sh - 跨平台游戏库查询工具（含中文名）"
    echo ""
    echo "命令:"
    echo "  list              列出所有平台游戏（含中文名）"
    echo "  steam [opts]      直接调用 Steam CLI"
    echo "  epic              列出 Epic 游戏（含中文名）"
    echo "  search <关键词>   跨平台搜索（支持中文名搜索）"
    echo "  stats             游戏库统计"
    echo "  unplayed          列出未玩游戏"
    echo "  recommend         高分未玩推荐"
    echo "  cn-update         更新中文名缓存（Steam API）"
    echo "  cn-update-xhh     从小黑盒补充中文名"
    echo "  duplicates        查找跨平台重复游戏"
    echo "  help              显示帮助"
    echo ""
    echo "缓存: $CACHE_DIR (TTL: ${CACHE_TTL}s)"
    echo "中文名缓存: $SKILL_DIR/cn_names_cache.json"
    echo ""
    echo "环境变量:"
    echo "  STEAM_API_KEY     Steam API 密钥（必需）"
    echo "  LEGENDARY_CLI     legendary CLI 路径（默认: legendary）"
}

# --- Main ---
case "${1:-help}" in
    list)      cmd_list ;;
    steam)     shift; cmd_steam "$@" ;;
    epic)      cmd_epic ;;
    search)    shift; cmd_search "$@" ;;
    stats)     cmd_stats ;;
    unplayed)  cmd_unplayed ;;
    recommend) cmd_recommend ;;
    cn-update)    cmd_cn_update ;;
    cn-update-xhh) cmd_cn_update_xhh ;;
    duplicates)   cmd_duplicates ;;
    help|*)       cmd_help ;;
esac
