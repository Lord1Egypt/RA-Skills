#!/bin/bash
# Cyber Growth - 神经成长协议
# 赛博朋克风格的成长追踪系统
# 用法: grow.sh <command> [options]

set -uo pipefail

# ==================== 配置 ====================
DATA_FILE="${CYBER_GROWTH_DATA:-$HOME/.openclaw/memory/cyber-growth.json}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEXICON="$SKILL_DIR/references/cyber-lexicon.md"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# ==================== 初始化数据文件 ====================
init_data() {
    if [ ! -f "$DATA_FILE" ]; then
        mkdir -p "$(dirname "$DATA_FILE")"
        cat > "$DATA_FILE" << 'EOF'
{
  "version": "1.0",
  "profile": {
    "handle": "Runner",
    "title": "新手 Runner",
    "createdAt": ""
  },
  "totalXp": 0,
  "chromeLevel": 1,
  "domains": {},
  "records": [],
  "protocols": {},
  "feishu": {
    "app_token": "",
    "table_id": ""
  }
}
EOF
        # 设置创建时间
        local now
        now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        sed -i '' "s/\"createdAt\": \"\"/\"createdAt\": \"$now\"/" "$DATA_FILE" 2>/dev/null || \
        sed -i "s/\"createdAt\": \"\"/\"createdAt\": \"$now\"/" "$DATA_FILE" 2>/dev/null || true
        echo -e "${GREEN}⚡ NERV NEURAL INTERFACE ONLINE${NC}"
        echo -e "${DIM}Entry plug inserted. Synchronized.${NC}"
        echo -e "${DIM}Data file: $DATA_FILE${NC}"
    fi
}

# ==================== JSON 工具函数 ====================
json_get() {
    local key="$1"
    python3 -c "
import json, sys
with open('$DATA_FILE') as f:
    data = json.load(f)
keys = '$key'.split('.')
val = data
for k in keys:
    if isinstance(val, dict) and k in val:
        val = val[k]
    else:
        print('')
        sys.exit(0)
print(val if not isinstance(val, (dict, list)) else json.dumps(val))
" 2>/dev/null || echo ""
}

json_set() {
    local key="$1"
    local value="$2"
    python3 -c "
import json
with open('$DATA_FILE') as f:
    data = json.load(f)
keys = '$key'.split('.')
d = data
for k in keys[:-1]:
    if k not in d:
        d[k] = {}
    d = d[k]
d[keys[-1]] = $value
with open('$DATA_FILE', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
" 2>/dev/null
}

# ==================== XP & 等级计算 ====================
xp_for_level() {
    local level="$1"
    python3 -c "
import math
total = 0
for l in range(1, $level):
    total += int(50 * l * (1.1 ** (l - 1)))
print(total)
" 2>/dev/null || echo "0"
}

level_for_xp() {
    local xp="$1"
    python3 -c "
import math
xp = $xp
level = 1
total = 0
while True:
    need = int(50 * level * (1.1 ** (level - 1)))
    if total + need > xp:
        break
    total += need
    level += 1
print(level)
" 2>/dev/null || echo "1"
}

get_title() {
    local level="$1"
    case $level in
        1|2) echo "候补驾驶员" ;;
        3|4) echo "D级适格者" ;;
        5|6) echo "初号机驾驶员" ;;
        7|8) echo "同步率突破者" ;;
        9|10) echo "觉醒者" ;;
        11|12) echo "暴走核心" ;;
        13|14) echo "量产机猎手" ;;
        15|16) echo "朗基努斯持有者" ;;
        17|18) echo "人类补完者" ;;
        *) echo "亚当之子" ;;
    esac
}

get_domain_icon() {
    local domain="$1"
    case "$domain" in
        api) echo "🔌" ;;
        security) echo "🛡️" ;;
        automation) echo "⚙️" ;;
        ops) echo "📊" ;;
        frontend) echo "🖥️" ;;
        backend) echo "🔧" ;;
        data) echo "📈" ;;
        ai) echo "🧠" ;;
        cloud) echo "☁️" ;;
        docs) echo "📝" ;;
        social) echo "📡" ;;
        feishu) echo "🔗" ;;
        *) echo "⚡" ;;
    esac
}

get_domain_name() {
    local domain="$1"
    case "$domain" in
        api) echo "API Protocol" ;;
        security) echo "Security Shell" ;;
        automation) echo "Automation Rig" ;;
        ops) echo "Ops Matrix" ;;
        frontend) echo "Frontend Chrome" ;;
        backend) echo "Backend Core" ;;
        data) echo "Data Stream" ;;
        ai) echo "Neural Link" ;;
        cloud) echo "Cloud Grid" ;;
        docs) echo "Doc Codec" ;;
        social) echo "Signal Hub" ;;
        feishu) echo "Feishu Nexus" ;;
        *) echo "General Ops" ;;
    esac
}

get_type_label() {
    local t="$1"
    case "$t" in
        patch) echo "紧急修复" ;;
        exploit) echo "弱点利用" ;;
        new-chrome) echo "新机体装备" ;;
        mission-cleared) echo "使徒击破" ;;
        signal-broadcast) echo "通讯广播" ;;
        memory-overflow) echo "同步失控" ;;
        *) echo "记录" ;;
    esac
}

# 进度条
progress_bar() {
    local pct="$1"
    local width=10
    local filled=$((pct * width / 100))
    local empty=$((width - filled))
    local bar=""
    for ((i=0; i<filled; i++)); do bar="${bar}█"; done
    for ((i=0; i<empty; i++)); do bar="${bar}░"; done
    echo "$bar"
}

# ==================== 命令: record ====================
cmd_record() {
    local description="" domain="general" xp=0 type="mission-cleared"

    # 解析参数
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --domain) domain="$2"; shift 2 ;;
            --xp) xp="$2"; shift 2 ;;
            --type) type="$2"; shift 2 ;;
            -*) echo "未知参数: $1"; exit 1 ;;
            *)
                if [ -z "$description" ]; then
                    description="$1"
                fi
                shift
                ;;
        esac
    done

    if [ -z "$description" ]; then
        echo "用法: grow.sh record <描述> [--domain <领域>] [--xp <数值>] [--type <类型>]"
        exit 1
    fi

    init_data

    local now
    now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local date_short
    date_short=$(date +"%Y-%m-%d")

    # 获取当前数据
    local total_xp
    total_xp=$(json_get "totalXp")
    total_xp=${total_xp:-0}

    local old_level
    old_level=$(json_get "chromeLevel")
    old_level=${old_level:-1}

    # 计算新数据
    local new_xp=$((total_xp + xp))
    local new_level
    new_level=$(level_for_xp "$new_xp")

    # 获取领域 XP
    local domain_xp
    domain_xp=$(json_get "domains.$domain.xp")
    domain_xp=${domain_xp:-0}
    local new_domain_xp=$((domain_xp + xp))
    local domain_level
    domain_level=$(level_for_xp "$new_domain_xp")

    # 生成记录 ID
    local record_id="rec_$(date +%s%N | cut -c1-13)"

    # 添加记录
    python3 -c "
import json
with open('$DATA_FILE') as f:
    data = json.load(f)

record = {
    'id': '$record_id',
    'date': '$date_short',
    'timestamp': '$now',
    'description': '$description',
    'domain': '$domain',
    'xp': $xp,
    'type': '$type'
}

data['records'].append(record)
data['totalXp'] = $new_xp
data['chromeLevel'] = $new_level
data['profile']['title'] = '$(get_title "$new_level")'

if '$domain' not in data['domains']:
    data['domains']['$domain'] = {'xp': 0, 'level': 1}
data['domains']['$domain']['xp'] = $new_domain_xp
data['domains']['$domain']['level'] = $domain_level

with open('$DATA_FILE', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
" 2>/dev/null

    # 输出记录确认
    local type_label
    type_label=$(get_type_label "$type")
    local icon
    icon=$(get_domain_icon "$domain")

    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}  📡 ${GREEN}TRANSMISSION LOGGED${NC}              ${CYAN}║${NC}"
    echo -e "${CYAN}╠══════════════════════════════════════╣${NC}"
    echo -e "${CYAN}║${NC}  ${BOLD}$description${NC}"
    echo -e "${CYAN}║${NC}"
    printf "${CYAN}║${NC}  ${GREEN}+${xp} XP${NC}  │  ${icon} $(get_domain_name "$domain")  │  ${YELLOW}${type_label}${NC}\n"
    echo -e "${CYAN}║${NC}"

    # 升级检测
    if [ "$new_level" -gt "$old_level" ]; then
        echo -e "${CYAN}║${NC}  ${MAGENTA}${BOLD}⚡ SYNC RATE BREAKTHROUGH${NC}  ${old_level} → ${new_level}"
        echo -e "${CYAN}║${NC}  ${DIM}New designation: 「$(get_title "$new_level")」${NC}"
    else
        local pct
        local current_floor
        current_floor=$(xp_for_level "$new_level")
        local next_need
        next_need=$(xp_for_level "$((new_level + 1))")
        local in_level=$((new_xp - current_floor))
        local need_level=$((next_need - current_floor))
        if [ "$need_level" -gt 0 ]; then
            pct=$((in_level * 100 / need_level))
        else
            pct=100
        fi
        local bar
        bar=$(progress_bar "$pct")
        echo -e "${CYAN}║${NC}  Sync Rate: ${BOLD}${new_level}${NC}  ${bar}  ${pct}%"
    fi

    echo -e "${CYAN}║${NC}  Neural Load: ${BOLD}${new_xp} XP${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════╝${NC}"
    echo ""

    # 检测里程碑协议
    local unlocked
    unlocked=$(check_protocols "$new_level" "$new_xp")
    if [ -n "$unlocked" ]; then
        echo "$unlocked" | while IFS='|' read -r status pid pname bonus; do
            if [ "$status" = "UNLOCKED" ]; then
                print_ceremony "$pid" "$pname" "$bonus"
                # 给协议解锁的 XP 奖励
                if [ -n "$bonus" ] && [ "$bonus" -gt 0 ]; then
                    python3 -c "
import json
with open('$DATA_FILE') as f:
    data = json.load(f)
data['totalXp'] = data.get('totalXp', 0) + $bonus
# 重新计算等级
xp = data['totalXp']
lv = 1
total = 0
while True:
    need = int(50 * lv * (1.1 ** (lv - 1)))
    if total + need > xp:
        break
    total += need
    lv += 1
data['chromeLevel'] = lv
with open('$DATA_FILE', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
" 2>/dev/null
                fi
            fi
        done
    fi

    # 同步到飞书（可选）
    sync_to_feishu "$record_id" "$date_short" "$description" "$domain" "$xp" "$type" "$new_level"
}

# ==================== 命令: status ====================
cmd_status() {
    init_data

    local total_xp
    total_xp=$(json_get "totalXp")
    total_xp=${total_xp:-0}

    local level
    level=$(json_get "chromeLevel")
    level=${level:-1}

    local title
    title=$(json_get "profile.title")
    title=${title:-"新手 Runner"}

    local handle
    handle=$(json_get "profile.handle")
    handle=${handle:-"Runner"}

    # 计算当前等级进度
    local current_floor
    current_floor=$(xp_for_level "$level")
    local next_need
    next_need=$(xp_for_level "$((level + 1))")
    local in_level=$((total_xp - current_floor))
    local need_level=$((next_need - current_floor))
    local pct=0
    if [ "$need_level" -gt 0 ]; then
        pct=$((in_level * 100 / need_level))
    fi
    local bar
    bar=$(progress_bar "$pct")

    # 连续记录天数
    local streak
    streak=$(calc_streak)

    # 输出状态面板
    echo ""
    echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}${BOLD}║${NC}  🔮 ${BOLD}NERV NEURAL INTERFACE${NC} v1.0          ${CYAN}${BOLD}║${NC}"
    echo -e "${CYAN}${BOLD}╠══════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}${BOLD}║${NC}  Pilot: ${BOLD}${handle}${NC}  ${DIM}「${title}」${NC}"
    echo -e "${CYAN}${BOLD}║${NC}  Sync Rate: ${BOLD}${level}${NC}  ${bar}  ${pct}%"
    echo -e "${CYAN}${BOLD}║${NC}  Neural Load: ${BOLD}${total_xp} XP${NC}  │  S² Engine: ${GREEN}${streak} days${NC}"
    echo -e "${CYAN}${BOLD}╠══════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}${BOLD}║${NC}  🧠 ${BOLD}EVA UNITS${NC}"

    # 显示各领域
    python3 -c "
import json
with open('$DATA_FILE') as f:
    data = json.load(f)

domains = data.get('domains', {})
if not domains:
    print('NO_DOMAINS')
else:
    sorted_domains = sorted(domains.items(), key=lambda x: x[1].get('xp', 0), reverse=True)
    for name, info in sorted_domains[:8]:
        xp = info.get('xp', 0)
        lv = info.get('level', 1)
        floor = 0
        for l in range(1, lv):
            floor += int(50 * l * (1.1 ** (l - 1)))
        next_floor = floor
        for l in range(1, lv + 1):
            next_floor += int(50 * l * (1.1 ** (l - 1)))
        in_lv = xp - floor
        need = next_floor - floor
        pct = min(int(in_lv * 100 / need), 100) if need > 0 else 100
        filled = pct * 10 // 100
        bar = '█' * filled + '░' * (10 - filled)
        icons = {'api': '🔌', 'security': '🛡️', 'automation': '⚙️', 'ops': '📊', 'frontend': '🖥️', 'backend': '🔧', 'data': '📈', 'ai': '🧠', 'cloud': '☁️', 'docs': '📝', 'social': '📡', 'feishu': '🔗'}
        icon = icons.get(name, '⚡')
        print(f'{icon}|{name}|{lv}|{bar}|{pct}|{xp}')
" 2>/dev/null | while IFS='|' read -r icon name lv bar pct xp; do
    if [ "$icon" = "NO_DOMAINS" ]; then
        echo -e "${CYAN}${BOLD}║${NC}  ${DIM}No augments yet. Start recording!${NC}"
    else
        printf "${CYAN}${BOLD}║${NC}  %s %-16s  Lv.%-2d  %s  %3d%%  (%sXP)\n" "$icon" "$name" "$lv" "$bar" "$pct" "$xp"
    fi
done

    echo -e "${CYAN}${BOLD}╠══════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}${BOLD}║${NC}  📡 ${BOLD}RECENT SORTIES${NC}"

    # 显示最近 5 条记录
    python3 -c "
import json
with open('$DATA_FILE') as f:
    data = json.load(f)
records = data.get('records', [])
for r in records[-5:]:
    xp = r.get('xp', 0)
    desc = r.get('description', '')[:30]
    t = r.get('type', '').upper()
    sign = '+' if xp >= 0 else ''
    print(f'  {sign}{xp}XP | {desc} | [{t}]')
" 2>/dev/null | while IFS= read -r line; do
    echo -e "${CYAN}${BOLD}║${NC}  ${GREEN}${line}${NC}"
done

    echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════╝${NC}"
    echo ""
}

# ==================== 命令: log ====================
cmd_log() {
    init_data
    local limit=10

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --limit) limit="$2"; shift 2 ;;
            *) shift ;;
        esac
    done

    echo ""
    echo -e "${CYAN}${BOLD}━━━ ENTRY PLUG LOG (last ${limit}) ━━━${NC}"
    echo ""

    python3 -c "
import json
with open('$DATA_FILE') as f:
    data = json.load(f)
records = data.get('records', [])[-${limit}:]
for r in reversed(records):
    date = r.get('date', '')
    desc = r.get('description', '')
    xp = r.get('xp', 0)
    domain = r.get('domain', '')
    t = r.get('type', '')
    sign = '+' if xp >= 0 else ''
    print(f'  {date}  {sign}{xp:>4d}XP  [{domain:12s}]  {desc}')
" 2>/dev/null
    echo ""
}

# ==================== 命令: tree ====================
cmd_tree() {
    init_data

    echo ""
    echo -e "${CYAN}${BOLD}━━━ EVA HANGAR ━━━${NC}"
    echo ""

    python3 -c "
import json
with open('$DATA_FILE') as f:
    data = json.load(f)

domains = data.get('domains', {})
total = data.get('totalXp', 0)

# 计算各领域进度
all_domains = ['api', 'security', 'automation', 'ops', 'frontend', 'backend', 'data', 'ai', 'cloud', 'docs', 'social', 'feishu']
icons = {'api': '🔌', 'security': '🛡️', 'automation': '⚙️', 'ops': '📊', 'frontend': '🖥️', 'backend': '🔧', 'data': '📈', 'ai': '🧠', 'cloud': '☁️', 'docs': '📝', 'social': '📡', 'feishu': '🔗'}
names = {'api': 'API Protocol', 'security': 'Security Shell', 'automation': 'Automation Rig', 'ops': 'Ops Matrix', 'frontend': 'Frontend Chrome', 'backend': 'Backend Core', 'data': 'Data Stream', 'ai': 'Neural Link', 'cloud': 'Cloud Grid', 'docs': 'Doc Codec', 'social': 'Signal Hub', 'feishu': 'Feishu Nexus'}

for d in all_domains:
    icon = icons.get(d, '⚡')
    name = names.get(d, d)
    info = domains.get(d, {'xp': 0, 'level': 1})
    xp = info.get('xp', 0)
    lv = info.get('level', 1)
    
    if xp == 0:
        status = 'LOCKED'
        print(f'  {icon} {name:18s}  {status}')
    else:
        floor = 0
        for l in range(1, lv):
            floor += int(50 * l * (1.1 ** (l - 1)))
        next_floor = floor
        for l in range(1, lv + 1):
            next_floor += int(50 * l * (1.1 ** (l - 1)))
        in_lv = xp - floor
        need = next_floor - floor
        pct = min(int(in_lv * 100 / need), 100) if need > 0 else 100
        filled = pct * 10 // 100
        bar = '█' * filled + '░' * (10 - filled)
        print(f'  {icon} {name:18s}  Lv.{lv:<3d} {bar} {pct:>3d}%  ({xp}XP)')

print(f'\\n  Total Neural Load: {total} XP')
" 2>/dev/null
    echo ""
}

# ==================== 命令: report ====================
cmd_report() {
    init_data
    local days=7

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --days) days="$2"; shift 2 ;;
            *) shift ;;
        esac
    done

    local cutoff
    cutoff=$(date -v-${days}d +"%Y-%m-%d" 2>/dev/null || date -d "-${days} days" +"%Y-%m-%d")

    echo ""
    echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}${BOLD}║${NC}  📊 ${BOLD}MAGI REPORT${NC} — Last ${days} Days            ${CYAN}${BOLD}║${NC}"
    echo -e "${CYAN}${BOLD}║${NC}  ${DIM}MELCHIOR+BALTHASAR+CASPAR consensus${NC}      ${CYAN}${BOLD}║${NC}"
    echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════╝${NC}"
    echo ""

    python3 -c "
import json
from datetime import datetime, timedelta
with open('$DATA_FILE') as f:
    data = json.load(f)

cutoff = '$cutoff'
records = [r for r in data.get('records', []) if r.get('date', '') >= cutoff]

if not records:
    print('  ${DIM}No transmissions in this period.${NC}')
else:
    total_xp = sum(r.get('xp', 0) for r in records)
    count = len(records)
    
    # 按领域统计
    by_domain = {}
    for r in records:
        d = r.get('domain', 'general')
        by_domain[d] = by_domain.get(d, 0) + r.get('xp', 0)
    
    # 按类型统计
    by_type = {}
    for r in records:
        t = r.get('type', 'other')
        by_type[t] = by_type.get(t, 0) + 1
    
    print(f'  📡 Total Transmissions: {count}')
    print(f'  ⚡ XP Gained: +{total_xp}')
    print(f'  📈 Avg XP/Day: {round(total_xp / $days, 1)}')
    print()
    print('  By Domain:')
    for d, xp in sorted(by_domain.items(), key=lambda x: x[1], reverse=True):
        print(f'    {d:16s} +{xp}XP')
    print()
    print('  By Type:')
    for t, c in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        print(f'    {t:20s} {c}')
    
    print()
    print('  Recent Highlights:')
    for r in records[-5:]:
        desc = r.get('description', '')[:40]
        xp = r.get('xp', 0)
        print(f'    +{xp}XP  {desc}')
" 2>/dev/null
    echo ""
}

# ==================== 计算连续天数 ====================
calc_streak() {
    python3 -c "
import json
from datetime import datetime, timedelta
with open('$DATA_FILE') as f:
    data = json.load(f)

records = data.get('records', [])
if not records:
    print(0)
    exit()

dates = sorted(set(r.get('date', '') for r in records if r.get('date')))
if not dates:
    print(0)
    exit()

today = datetime.now().strftime('%Y-%m-%d')
streak = 0
check = datetime.now()

while True:
    d = check.strftime('%Y-%m-%d')
    if d in dates:
        streak += 1
        check = check - timedelta(days=1)
    elif d == today:
        # today might not have a record yet
        check = check - timedelta(days=1)
    else:
        break

print(streak)
" 2>/dev/null || echo "0"
}

# ==================== 里程碑协议检测 ====================
# 预定义协议列表
PROTOCOLS_FIRST_BLOOD="first-blood"
PROTOCOLS_WEEK_STREAK="week-streak"
PROTOCOLS_FIVE_RECORDS="five-records"

check_protocols() {
    local new_level="$1" new_xp="$2"

    python3 -c "
import json
from datetime import datetime, timedelta

with open('$DATA_FILE') as f:
    data = json.load(f)

protocols = data.get('protocols', {})
records = data.get('records', [])
new_level = $new_level
total_xp = $new_xp
unlocked = []

# First Blood: 第一次记录
if 'first-blood' not in protocols and len(records) >= 1:
    protocols['first-blood'] = {'unlocked': True, 'unlockedAt': datetime.utcnow().isoformat() + 'Z'}
    unlocked.append(('FIRST BLOOD', '首次出击完成', 10))

# Five Records: 5 条记录
if 'five-records' not in protocols and len(records) >= 5:
    protocols['five-records'] = {'unlocked': True, 'unlockedAt': datetime.utcnow().isoformat() + 'Z'}
    unlocked.append(('FIVE SORTIES', '五次出击达成', 25))

# Week Streak: 连续 7 天
dates = sorted(set(r.get('date', '') for r in records if r.get('date')))
if dates and 'week-streak' not in protocols:
    streak = 0
    check = datetime.now()
    while True:
        d = check.strftime('%Y-%m-%d')
        if d in dates:
            streak += 1
            check = check - timedelta(days=1)
        else:
            break
    if streak >= 7:
        protocols['week-streak'] = {'unlocked': True, 'unlockedAt': datetime.utcnow().isoformat() + 'Z'}
        unlocked.append(('DATASTREAM STABLE', '数据流稳定 (7天)', 50))

# Level Milestones
level_protocols = {3: ('CLASS-D QUALIFIED', 'D级适格者认证', 30), 5: ('UNIT-01 ACTIVATED', '初号机启动', 50), 7: ('SYNC RATE 70%', '同步率突破70%', 80), 10: ('AWAKENED', '觉醒者认证', 100)}
for lv, (pid, pname, bonus) in level_protocols.items():
    key = f'level-{lv}'
    if key not in protocols and new_level >= lv:
        protocols[key] = {'unlocked': True, 'unlockedAt': datetime.utcnow().isoformat() + 'Z'}
        unlocked.append((pid, pname, bonus))

data['protocols'] = protocols
with open('$DATA_FILE', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# 输出解锁的协议
for pid, pname, bonus in unlocked:
    print(f'UNLOCKED|{pid}|{pname}|{bonus}')
" 2>/dev/null
}

print_ceremony() {
    local pid="$1" pname="$2" bonus="$3"

    echo ""
    echo -e "${MAGENTA}${BOLD}  🔓🔓🔓 PROTOCOL UNLOCKED 🔓🔓🔓${NC}"
    echo -e "${CYAN}  ╔═══════════════════════════════════════╗${NC}"
    echo -e "${CYAN}  ║${NC}  ${BOLD}「${pid}」${NC}"
    echo -e "${CYAN}  ║${NC}  ${DIM}${pname}${NC}"
    echo -e "${CYAN}  ║${NC}"
    echo -e "${CYAN}  ║${NC}  ${GREEN}${BOLD}+${bonus} XP BONUS${NC}"
    echo -e "${CYAN}  ╚═══════════════════════════════════════╝${NC}"
    echo ""

    # EVA 风格台词
    case "$pid" in
        "FIRST BLOOD") echo -e "  ${DIM}「真嗣，你做得很好」${NC}" ;;
        "DATASTREAM STABLE") echo -e "  ${DIM}「连续作战能力确认，优秀的驾驶员」${NC}" ;;
        "UNIT-01 ACTIVATED") echo -e "  ${DIM}「初号机，启动！」${NC}" ;;
        "AWAKENED") echo -e "  ${DIM}「这...这就是觉醒的力量吗」${NC}" ;;
        *) echo -e "  ${DIM}「协议确认，继续前进」${NC}" ;;
    esac
    echo ""
}

# ==================== 命令: eta（使徒倒计时） ====================
cmd_eta() {
    init_data

    local total_xp
    total_xp=$(json_get "totalXp")
    total_xp=${total_xp:-0}

    local level
    level=$(json_get "chromeLevel")
    level=${level:-1}

    local next_level=$((level + 1))
    local next_title
    next_title=$(get_title "$next_level")

    local current_floor
    current_floor=$(xp_for_level "$level")
    local next_need
    next_need=$(xp_for_level "$next_level")
    local in_level=$((total_xp - current_floor))
    local need_level=$((next_need - current_floor))
    local remaining=$((need_level - in_level))

    local pct=0
    if [ "$need_level" -gt 0 ]; then
        pct=$((in_level * 100 / need_level))
    fi
    local bar
    bar=$(progress_bar "$pct")

    # 计算预计天数（基于最近 7 天平均）
    local cutoff
    cutoff=$(date -v-7d +"%Y-%m-%d" 2>/dev/null || date -d "-7 days" +"%Y-%m-%d")
    local avg_xp
    avg_xp=$(python3 -c "
import json
with open('$DATA_FILE') as f:
    data = json.load(f)
records = [r for r in data.get('records', []) if r.get('date', '') >= '$cutoff']
total = sum(r.get('xp', 0) for r in records)
print(max(1, round(total / 7)))
" 2>/dev/null || echo "30")

    local eta_days=99
    if [ "$avg_xp" -gt 0 ]; then
        eta_days=$((remaining / avg_xp))
        if [ $((remaining % avg_xp)) -gt 0 ]; then
            eta_days=$((eta_days + 1))
        fi
    fi

    echo ""
    echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}${BOLD}║${NC}  🎯 ${BOLD}NEXT ANGEL${NC} — Lv.${next_level} 「${next_title}」  ${CYAN}${BOLD}║${NC}"
    echo -e "${CYAN}${BOLD}╠══════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}${BOLD}║${NC}  Progress: ${bar}  ${pct}%"
    echo -e "${CYAN}${BOLD}║${NC}  Remaining: ${BOLD}${remaining} XP${NC}  │  Avg: ${avg_xp} XP/day"
    if [ "$eta_days" -lt 99 ]; then
        echo -e "${CYAN}${BOLD}║${NC}  ETA: ${GREEN}${BOLD}${eta_days} days${NC}  │  ${DIM}$(date -v+${eta_days}d +"%m/%d" 2>/dev/null || date -d "+${eta_days} days" +"%m/%d")${NC}"
    else
        echo -e "${CYAN}${BOLD}║${NC}  ETA: ${DIM}Calculating... start recording!${NC}"
    fi
    echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════╝${NC}"
    echo ""
}

# ==================== 命令: chart（同步率波动图） ====================
cmd_chart() {
    init_data
    local days="${1:-7}"

    echo ""
    echo -e "${CYAN}${BOLD}━━━ SYNC RATE — Last ${days} Days ━━━${NC}"
    echo ""

    python3 -c "
import json
from datetime import datetime, timedelta

with open('$DATA_FILE') as f:
    data = json.load(f)

records = data.get('records', [])
days = $days

# 按天汇总 XP
daily = {}
for i in range(days):
    d = (datetime.now() - timedelta(days=days-1-i)).strftime('%Y-%m-%d')
    daily[d] = 0

for r in records:
    d = r.get('date', '')
    if d in daily:
        daily[d] += r.get('xp', 0)

# 计算累计 XP 转换为等级
xp_values = list(daily.values())
dates = list(daily.keys())

# 计算每天的同步率（等级）
cumulative = 0
levels = []
base_xp = data.get('totalXp', 0) - sum(xp_values)  # 起始 XP
for xp in xp_values:
    cumulative += xp
    total = base_xp + cumulative
    lv = 1
    lv_total = 0
    while True:
        need = int(50 * lv * (1.1 ** (lv - 1)))
        if lv_total + need > total:
            break
        lv_total += need
        lv += 1
    levels.append(lv)

max_lv = max(levels) if levels else 1
min_lv = min(levels) if levels else 1
chart_height = max(max_lv - min_lv + 1, 3)

# 绘制图表
for row in range(chart_height, 0, -1):
    lv = min_lv + row - 1
    label = f'{lv:>2d} |'
    line = ''
    for i, l in enumerate(levels):
        if l == lv:
            line += '  ●'
        elif l > lv:
            line += '  │'
        else:
            line += '   '
    print(f'  {label}{line}')

# X 轴
x_axis = '    +' + '───' * days
print(f'  {x_axis}')

# 日期标签
date_line = '     '
for d in dates:
    dt = datetime.strptime(d, '%Y-%m-%d')
    date_line += dt.strftime('%a')[:2] + '  '
print(f'  {date_line}')

# XP 标注
xp_line = '     '
for xp in xp_values:
    if xp > 0:
        xp_line += f'+{xp:<2d}'
    else:
        xp_line += ' · '
print(f'  {xp_line}')
" 2>/dev/null
    echo ""
}

# ==================== 增强版 report ====================
cmd_report() {
    init_data
    local days=7

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --days) days="$2"; shift 2 ;;
            *) shift ;;
        esac
    done

    local cutoff
    cutoff=$(date -v-${days}d +"%Y-%m-%d" 2>/dev/null || date -d "-${days} days" +"%Y-%m-%d")

    echo ""
    echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}${BOLD}║${NC}  📊 ${BOLD}MAGI WEEKLY REPORT${NC}                         ${CYAN}${BOLD}║${NC}"
    echo -e "${CYAN}${BOLD}║${NC}  ${DIM}MELCHIOR + BALTHASAR + CASPAR consensus${NC}       ${CYAN}${BOLD}║${NC}"
    echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════╝${NC}"
    echo ""

    python3 -c "
import json
from datetime import datetime, timedelta

with open('$DATA_FILE') as f:
    data = json.load(f)

cutoff = '$cutoff'
records = [r for r in data.get('records', []) if r.get('date', '') >= cutoff]
total_xp = data.get('totalXp', 0)
level = data.get('chromeLevel', 1)

if not records:
    print('  ${DIM}No sorties this period. Pilot on standby.${NC}')
else:
    xp_gained = sum(r.get('xp', 0) for r in records)
    count = len(records)
    
    # 按领域统计
    by_domain = {}
    for r in records:
        d = r.get('domain', 'general')
        by_domain[d] = by_domain.get(d, 0) + r.get('xp', 0)
    
    # 按类型统计
    by_type = {}
    for r in records:
        t = r.get('type', 'other')
        by_type[t] = by_type.get(t, 0) + 1
    
    # MVP（最高 XP 记录）
    mvp = max(records, key=lambda r: r.get('xp', 0))
    
    # Top 3 领域
    top_domains = sorted(by_domain.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # 下一目标
    next_lv = level + 1
    floor = 0
    for l in range(1, next_lv):
        floor += int(50 * l * (1.1 ** (l - 1)))
    remaining = floor - total_xp
    
    # 标题映射
    titles = {1: '候补驾驶员', 2: '候补驾驶员', 3: 'D级适格者', 4: 'D级适格者', 5: '初号机驾驶员', 6: '初号机驾驶员', 7: '同步率突破者', 8: '同步率突破者', 9: '觉醒者', 10: '觉醒者'}
    title = titles.get(next_lv, '未知')
    
    print('  ┌─────────────────────────────────────┐')
    print(f'  │  📡 总出击: {count:>3d} 次    ⚡ 总XP: +{xp_gained:<5d}  │')
    print(f'  │  📈 日均: {round(xp_gained / $days, 1):>5.1f} XP    🎯 当前: Lv.{level:<2d}     │')
    print('  └─────────────────────────────────────┘')
    print()
    print('  🏆 本周 MVP')
    print(f'     +{mvp[\"xp\"]}XP | {mvp[\"description\"][:35]}')
    print()
    print('  🧠 领域 TOP 3')
    icons = {'api': '🔌', 'security': '🛡️', 'automation': '⚙️', 'ops': '📊', 'frontend': '🖥️', 'backend': '🔧', 'data': '📈', 'ai': '🧠', 'cloud': '☁️', 'docs': '📝', 'social': '📡', 'feishu': '🔗'}
    for i, (d, xp) in enumerate(top_domains, 1):
        icon = icons.get(d, '⚡')
        bar_len = min(int(xp / max(xp_gained, 1) * 20), 20)
        bar = '█' * bar_len + '░' * (20 - bar_len)
        print(f'     {i}. {icon} {d:12s} {bar} +{xp}XP')
    print()
    print('  ⚔️ 作战类型')
    type_icons = {'patch': '🔧', 'exploit': '⚡', 'new-chrome': '🆕', 'mission-cleared': '🎯', 'signal-broadcast': '📡', 'memory-overflow': '⚠️'}
    type_names = {'patch': '紧急修复', 'exploit': '弱点利用', 'new-chrome': '新机体装备', 'mission-cleared': '使徒击破', 'signal-broadcast': '通讯广播', 'memory-overflow': '同步失控'}
    for t, c in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        icon = type_icons.get(t, '📌')
        name = type_names.get(t, t)
        print(f'     {icon} {name:12s} × {c}')
    print()
    print(f'  🎯 下周目标: Lv.{next_lv} 「{title}」')
    print(f'     距离: {max(0, remaining)} XP')
    if remaining > 0:
        avg = round(xp_gained / max($days, 1), 1)
        if avg > 0:
            eta = int(remaining / avg) + 1
            print(f'     预计: {eta} 天（按当前速度）')
    print()
    
    # 近期记录
    print('  📡 本周战报')
    for r in records[-10:]:
        desc = r.get('description', '')[:30]
        xp = r.get('xp', 0)
        d = r.get('date', '')[5:]  # MM-DD
        t = r.get('type', '')
        t_icon = type_icons.get(t, '📌')
        print(f'     {d}  +{xp:>3d}XP  {t_icon} {desc}')
" 2>/dev/null
    echo ""
}

# ==================== 命令: monthly（月度人类补完报告） ====================
cmd_monthly() {
    init_data
    local month="${1:-}"

    # 默认上个月，如果今天 <= 5 则取上上个月
    if [ -z "$month" ]; then
        local day
        day=$(date +%d)
        day=$((10#$day))  # 去掉前导零
        if [ "$day" -le 5 ]; then
            month=$(date -v-1m +"%Y-%m" 2>/dev/null || date -d "last month" +"%Y-%m")
        else
            month=$(date +"%Y-%m")
        fi
    fi

    local month_start="${month}-01"
    local month_end
    month_end=$(python3 -c "from datetime import datetime; import calendar; y,m=map(int,'$month'.split('-')); print(f'{y}-{m:02d}-{calendar.monthrange(y,m)[1]}')" 2>/dev/null)
    local month_name
    month_name=$(python3 -c "y,m=map(int,'$month'.split('-')); print(f'{y}年{m:02d}月')" 2>/dev/null)

    echo ""
    echo -e "${MAGENTA}${BOLD}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}${BOLD}║${NC}  ✨ ${BOLD}人类补完报告${NC} — ${month_name}                          ${MAGENTA}${BOLD}║${NC}"
    echo -e "${MAGENTA}${BOLD}║${NC}  ${DIM}HUMAN INSTRUMENTALITY MONTHLY REPORT${NC}                   ${MAGENTA}${BOLD}║${NC}"
    echo -e "${MAGENTA}${BOLD}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""

    python3 -c "
import json
from datetime import datetime, timedelta
from collections import defaultdict

with open('$DATA_FILE') as f:
    data = json.load(f)

records = data.get('records', [])
total_xp = data.get('totalXp', 0)
level = data.get('chromeLevel', 1)

# 筛选本月记录
month_records = [r for r in records if '$month_start' <= r.get('date', '') <= '$month_end']

if not month_records:
    print('  ${DIM}本月无出击记录。Pilot 持续待命中。${NC}')
    print()
    print('  建议：')
    print('  • 每天至少完成一项小任务（10-30 XP）')
    print('  • 尝试新领域，解锁新 EVA Unit')
    print('  • 保持 DataStream 不中断')
else:
    xp_month = sum(r.get('xp', 0) for r in month_records)
    count = len(month_records)
    
    # 计算本月天数
    start = datetime.strptime('$month_start', '%Y-%m-%d')
    end = datetime.strptime('$month_end', '%Y-%m-%d')
    days_in_month = (end - start).days + 1
    
    # 实际活跃天数
    active_days = len(set(r.get('date', '') for r in month_records))
    avg_xp_day = round(xp_month / max(active_days, 1), 1)
    avg_xp_calendar = round(xp_month / days_in_month, 1)
    
    # 按领域统计
    by_domain = defaultdict(int)
    for r in month_records:
        by_domain[r.get('domain', 'general')] += r.get('xp', 0)
    
    # 按类型统计
    by_type = defaultdict(int)
    for r in month_records:
        by_type[r.get('type', 'other')] += 1
    
    # Top 3 高光时刻
    top_moments = sorted(month_records, key=lambda r: r.get('xp', 0), reverse=True)[:3]
    
    # 领域 TOP 3
    top_domains = sorted(by_domain.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # 本月新增领域
    all_domains_before = set()
    for r in records:
        if r.get('date', '') < '$month_start':
            all_domains_before.add(r.get('domain', ''))
    new_domains = set(by_domain.keys()) - all_domains_before
    
    # 本月等级变化
    # 找到月初的等级
    xp_before_month = total_xp - xp_month
    def calc_level(xp):
        lv = 1
        total = 0
        while True:
            need = int(50 * lv * (1.1 ** (lv - 1)))
            if total + need > xp:
                break
            total += need
            lv += 1
        return lv
    
    level_start = calc_level(xp_before_month)
    level_now = level
    level_gained = level_now - level_start
    
    # 等级称号映射
    titles = {1: '候补驾驶员', 2: '候补驾驶员', 3: 'D级适格者', 4: 'D级适格者', 5: '初号机驾驶员', 6: '初号机驾驶员', 7: '同步率突破者', 8: '同步率突破者', 9: '觉醒者', 10: '觉醒者'}
    current_title = titles.get(level_now, '超频核心')
    
    # ━━━━━━━━━━ 输出报告 ━━━━━━━━━━
    
    # 本月总览
    print('  ┌──────────────────────────────────────────────────┐')
    print(f'  │  📊 本月总览                                      │')
    print(f'  │     总出击: {count:>3d} 次      活跃天数: {active_days:>2d}/{days_in_month} 天    │')
    print(f'  │     总 XP: +{xp_month:<6d}     日均XP: {avg_xp_day:>6.1f}       │')
    print(f'  │     等级: Lv.{level_start} → Lv.{level_now} ({\"+\" if level_gained >= 0 else \"\"}{level_gained})                 │')
    print(f'  │     称号: 「{current_title}」                        │')
    print('  └──────────────────────────────────────────────────┘')
    print()
    
    # 领域分布（ASCII 饼图风格）
    print('  🧠 领域分布')
    icons = {'api': '🔌', 'security': '🛡️', 'automation': '⚙️', 'ops': '📊', 'frontend': '🖥️', 'backend': '🔧', 'data': '📈', 'ai': '🧠', 'cloud': '☁️', 'docs': '📝', 'social': '📡', 'feishu': '🔗', 'general': '⚡'}
    domain_names = {'api': 'API Protocol', 'security': 'Security Shell', 'automation': 'Automation Rig', 'ops': 'Ops Matrix', 'frontend': 'Frontend Chrome', 'backend': 'Backend Core', 'data': 'Data Stream', 'ai': 'Neural Link', 'cloud': 'Cloud Grid', 'docs': 'Doc Codec', 'social': 'Signal Hub', 'feishu': 'Feishu Nexus', 'general': 'General Ops'}
    
    sorted_domains = sorted(by_domain.items(), key=lambda x: x[1], reverse=True)
    bar_max = 20
    for d, xp in sorted_domains:
        icon = icons.get(d, '⚡')
        name = domain_names.get(d, d)
        pct = round(xp / xp_month * 100, 1) if xp_month > 0 else 0
        bar_len = int(pct / 100 * bar_max)
        bar = '█' * bar_len + '░' * (bar_max - bar_len)
        pie = '●' if sorted_domains[0][0] == d else '○'
        print(f'     {pie} {icon} {name:18s} {bar} {pct:>5.1f}%  (+{xp}XP)')
    print()
    
    # 作战类型分布
    print('  ⚔️ 作战类型')
    type_icons = {'patch': '🔧', 'exploit': '⚡', 'new-chrome': '🆕', 'mission-cleared': '🎯', 'signal-broadcast': '📡', 'memory-overflow': '⚠️'}
    type_names = {'patch': '紧急修复', 'exploit': '弱点利用', 'new-chrome': '新机体装备', 'mission-cleared': '使徒击破', 'signal-broadcast': '通讯广播', 'memory-overflow': '同步失控'}
    for t, c in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
        icon = type_icons.get(t, '📌')
        name = type_names.get(t, t)
        pct = round(c / count * 100, 1)
        print(f'     {icon} {name:12s} × {c:<3d} ({pct}%)')
    print()
    
    # 最高光时刻 TOP 3
    print('  🏆 最高光时刻 TOP 3')
    for i, r in enumerate(top_moments, 1):
        desc = r.get('description', '')[:35]
        xp = r.get('xp', 0)
        d = r.get('date', '')[5:]
        t = r.get('type', '')
        t_icon = type_icons.get(t, '📌')
        medal = ['🥇', '🥈', '🥉'][i-1]
        print(f'     {medal} {d}  +{xp:>3d}XP  {t_icon} {desc}')
    print()
    
    # 新领域
    if new_domains:
        print('  🆕 新解锁 EVA Unit')
        for d in new_domains:
            icon = icons.get(d, '⚡')
            name = domain_names.get(d, d)
            xp = by_domain[d]
            print(f'     {icon} {name} — 首月 {xp} XP')
        print()
    
    # 下月进化方向建议
    print('  🎯 下月进化方向建议')
    
    # 分析薄弱领域
    all_expected = ['api', 'security', 'automation', 'ops', 'feishu', 'social', 'ai', 'cloud', 'docs']
    weak_domains = []
    for d in all_expected:
        if d not in by_domain or by_domain[d] < 50:
            weak_domains.append(d)
    
    # 分析最强领域
    strongest = top_domains[0][0] if top_domains else None
    
    suggestions = []
    
    # 建议1：均衡发展
    if len(by_domain) < 4:
        suggestions.append(f'     • 尝试新领域，目前只活跃在 {len(by_domain)} 个领域，目标 4+')
    
    # 建议2：补弱
    if weak_domains:
        weak_names = [domain_names.get(d, d) for d in weak_domains[:2]]
        suggestions.append(f'     • 补强薄弱领域: {\" / \".join(weak_names)}')
    
    # 建议3：持续稳定
    if active_days < days_in_month * 0.5:
        suggestions.append(f'     • 提升活跃度，本月仅活跃 {active_days} 天，目标 {int(days_in_month * 0.7)}+ 天')
    
    # 建议4：突破瓶颈
    if level_gained == 0:
        suggestions.append(f'     • 本月等级未提升，加大出击频率冲 Lv.{level_now + 1}')
    
    # 建议5：深挖最强领域
    if strongest:
        s_name = domain_names.get(strongest, strongest)
        suggestions.append(f'     • 深挖 {s_name}，争取冲击 Lv.{data[\"domains\"].get(strongest, {}).get(\"level\", 1) + 1}')
    
    # 默认建议
    if not suggestions:
        suggestions.append('     • 保持当前节奏，均衡发展各领域')
        suggestions.append(f'     • 目标下月 Lv.{level_now + 2}')
    
    for s in suggestions:
        print(s)
    
    # 下月目标 XP
    next_month_days = 30
    target_xp = int(avg_xp_day * next_month_days * 1.2) if avg_xp_day > 0 else 500
    print()
    print(f'  📈 下月目标: +{target_xp} XP (较本月提升 20%)')
    
    # 预计等级
    future_xp = total_xp + target_xp
    future_level = calc_level(future_xp)
    future_title = titles.get(future_level, '超频核心')
    if future_level > level_now:
        print(f'     预计可达: Lv.{future_level} 「{future_title}」')
    
    print()
    print('  ─────────────────────────────────────────────')
    print('  ✨ 人类补完计划，持续推进中...')
    print('  ─────────────────────────────────────────────')

" 2>/dev/null
    echo ""
}

# ==================== 飞书同步 ====================
sync_to_feishu() {
    local record_id="$1" date="$2" description="$3" domain="$4" xp="$5" type="$6" level="$7"

    local app_token table_id
    app_token=$(json_get "feishu.app_token")
    table_id=$(json_get "feishu.table_id")

    if [ -z "$app_token" ] || [ -z "$table_id" ]; then
        return 0
    fi

    # 使用 openclaw 的 feishu 工具同步
    # 这里只做占位，实际需要 openclaw 环境
    echo -e "${DIM}  📡 Syncing to Feishu Bitable...${NC}" >&2
}

# ==================== 主函数 ====================
main() {
    local cmd="${1:-help}"
    shift || true

    case "$cmd" in
        record|r)
            cmd_record "$@"
            ;;
        status|s)
            cmd_status "$@"
            ;;
        log|l)
            cmd_log "$@"
            ;;
        tree|t)
            cmd_tree "$@"
            ;;
        report)
            cmd_report "$@"
            ;;
        eta|e)
            cmd_eta "$@"
            ;;
        chart|c)
            cmd_chart "$@"
            ;;
        monthly|m)
            cmd_monthly "$@"
            ;;
        help|--help|-h)
            echo "Cyber Growth - 神经成长协议"
            echo ""
            echo "用法: grow.sh <command> [options]"
            echo ""
            echo "命令:"
            echo "  record <描述>  记录成长"
            echo "    --domain <领域>   领域 (api/security/automation/...)"
            echo "    --xp <数值>       XP 值"
            echo "    --type <类型>     类型 (patch/exploit/new-chrome/...)"
            echo "  status         查看状态面板"
            echo "  eta            使徒倒计时（距离下一等级）"
            echo "  chart [天数]   同步率波动图"
            echo "  report [--days N]  结构化周报"
            echo "  monthly [YYYY-MM]  月度人类补完报告"
            echo "  log            查看最近记录"
            echo "    --limit <n>       显示条数"
            echo "  tree           查看技能树"
            echo "  help           显示帮助"
            ;;
        *)
            echo "未知命令: $cmd"
            echo "运行 'grow.sh help' 查看用法"
            exit 1
            ;;
    esac
}

main "$@"
