#!/bin/bash
#==============================================================================
# A股日报 - 公共函数库
#==============================================================================

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="${SKILL_DIR}/config.json"
LOG_DIR="${SKILL_DIR}/logs"
mkdir -p "${LOG_DIR}"

# 日志函数
alog() {
    local level="$1"; shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" >> "${LOG_DIR}/aastock-$(date '+%Y%m%d').log"
}

#==============================================================================
# 配置文件
#==============================================================================
read_config() {
    local key="$1"
    python3 -c "
import json
with open('${CONFIG_FILE}', 'r') as f:
    config = json.load(f)
    keys = '${key}'.split('.')
    val = config
    for k in keys:
        val = val.get(k, None)
        if val is None:
            print('')
            break
    if val is not None:
        print(json.dumps(val) if isinstance(val, (dict, list)) else val)
" 2>/dev/null
}

get_portfolio() { read_config "portfolio"; }
is_weekend() { [ "$(date '+%u')" = "6" ] || [ "$(date '+%u')" = "7" ]; }
is_trading_day() { [ "$(date '+%u')" -ge 1 ] && [ "$(date '+%u')" -le 5 ]; }

#==============================================================================
# API Key 管理
#==============================================================================
KEY_LIST=""
KEY_INDEX=0
KEY_COUNT=0

init_api_keys() {
    if [ -n "$KEY_LIST" ]; then return; fi
    
    if [ -n "$EASTMONEY_APIKEY" ]; then
        KEY_LIST="$EASTMONEY_APIKEY"
        KEY_COUNT=1
    else
        local vault_file="${HOME}/.openclaw/workspace/vault/credentials/eastmoney.json"
        if [ -f "$vault_file" ]; then
            KEY_LIST=$(python3 -c "
import json
with open('${vault_file}') as f:
    data = json.load(f)
    keys = data.get('keys', [])
    print('|||'.join(keys))
" 2>/dev/null)
            KEY_COUNT=$(echo "$KEY_LIST" | python3 -c "import sys; print(len(sys.stdin.read().split('|||')))" 2>/dev/null)
        fi
    fi
    
    [ -z "$KEY_LIST" ] && KEY_LIST="mkt_qUycJtiyNGUu0z7CtEX5RrAZZuCYVAr1hhx3bsk_HZ4" && KEY_COUNT=1
}

get_current_api_key() {
    init_api_keys
    echo "$KEY_LIST" | python3 -c "import sys; print(sys.stdin.read().split('|||')[$KEY_INDEX])" KEY_INDEX=$KEY_INDEX
}

rotate_api_key() {
    init_api_keys
    KEY_INDEX=$(( (KEY_INDEX + 1) % KEY_COUNT ))
}

#==============================================================================
# API 调用
#==============================================================================
API_BASE="https://mkapi2.dfcfs.com"

api_post() {
    local endpoint="$1"
    local data="$2"
    local retry_count=0
    
    init_api_keys
    
    while [ $retry_count -lt $KEY_COUNT ]; do
        local api_key=$(get_current_api_key)
        [ -z "$api_key" ] && break
        
        local response=$(curl -s -X POST "${API_BASE}${endpoint}" \
            -H "Content-Type: application/json" \
            -H "apikey: ${api_key}" \
            -d "${data}" 2>&1)
        
        if echo "$response" | grep -qE '"status":113|"status":-1|"code":113|"code":-1|"limit"|限流'; then
            rotate_api_key
            retry_count=$((retry_count + 1))
            sleep 1
            continue
        fi
        
        echo "$response"
        return 0
    done
    
    return 1
}

news_search() {
    api_post "/finskillshub/api/claw/news-search" \
        "{\"query\": \"${1}\", \"size\": ${2:-10}}"
}

data_query() {
    api_post "/finskillshub/api/claw/query" \
        "{\"toolQuery\": \"${1}\"}"
}

#==============================================================================
# 行情 API
#==============================================================================
#==============================================================================
# 行情 API - 使用 eastmoney-tools (mkapi2.dfcfs.com)
#==============================================================================
get_stock_quote() {
    local secid="$1"
    # secid 格式: 1.601668 (上海) 或 0.003816 (深圳)
    local prefix="${secid%%.*}"
    local code="${secid#*.}"
    local query_code
    if [ "$prefix" = "1" ]; then
        query_code="${code}.SH"
    else
        query_code="${code}.SZ"
    fi
    
    local result
    result=$(curl -s --connect-timeout 10 \
        -X POST "https://mkapi2.dfcfs.com/finskillshub/api/claw/query" \
        -H "Content-Type: application/json" \
        -H "apikey: $(get_current_api_key)" \
        -d "{\"toolQuery\":\"${query_code} 行情数据 资金流向\"}" 2>/dev/null)
    
    echo "$result" | python3 -c "
import json,sys
try:
    d = json.loads(sys.stdin.read())
    if not d.get('success'):
        print('N/A|N/A|N/A|N/A|N/A')
        sys.exit(0)
    tables = d.get('data',{}).get('data',{}).get('searchDataResultDTO',{}).get('dataTableDTOList',[])
    for t in tables:
        table = t.get('table',{})
        if 'f2' not in table:
            continue
        name = t.get('entityTagDTO',{}).get('securityName','') or t.get('entityName','')
        # 清理名称中的股票代码
        import re
        name = re.sub(r'\([0-9]+\.SH\)|\([0-9]+\.SZ\)','',name).strip()
        
        price = table['f2'][0] if isinstance(table['f2'],list) else table['f2']
        pct_raw = table.get('f3',['-'])[0] if isinstance(table.get('f3',['-']),list) else table.get('f3','-')
        pct = str(pct_raw).replace('%','')
        change = table.get('f4',['-'])[0] if isinstance(table.get('f4',['-']),list) else table.get('f4','-')
        flow = table.get('f62',['0'])[0] if isinstance(table.get('f62',['0']),list) else table.get('f62','0')
        
        # 如果 f62 没有数据，尝试从其他表找主力净额
        if str(flow) in ['0','-','None','']:
            for t2 in tables:
                t2_table = t2.get('table',{})
                for k,v in t2_table.items():
                    if isinstance(v,list) and v and ('主力净额' in str(k) or 'f62' in str(k)):
                        flow = str(v[0])
                        break
        
        print(f'{name}|{price}|{change}|{pct}|{flow}')
        break
    else:
        print('N/A|N/A|N/A|N/A|N/A')
except:
    print('N/A|N/A|N/A|N/A|N/A')
"
}


get_sector_flow() {
    local limit="${1:-10}"
    curl -s "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=${limit}&po=1&np=1&ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2&fid=f62&fs=m:0+t:2,m:0+t:23,m:1+t:2,m:1+t:10&fields=f12,f14,f3,f62,f6" 2>/dev/null | \
    python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    items = data.get('data', {}).get('diff', [])
    for item in items:
        name = item.get('f14', '')
        flow = item.get('f62', 0) or 0
        flow_str = f'{flow/100000000:.2f}亿' if abs(flow) >= 100000000 else f'{flow/10000:.2f}万'
        print(f'{name}|{flow_str}')
except:
    pass
"
}

get_limit_up() {
    local limit="${1:-10}"
    curl -s "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=${limit}&po=1&np=1&ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&fields=f12,f14,f2,f3" 2>/dev/null | \
    python3 -c "
import json,sys
try:
    data = json.load(sys.stdin)
    items = data.get('data', {}).get('diff', [])
    for item in items:
        print(f\"{item.get('f14','')}|{item.get('f12','')}|{item.get('f2','')}|{item.get('f3',0)}\")
except:
    pass
"
}

get_limit_stats() {
    local up=$(curl -s "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=1&po=1&np=1&ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&fields=f12&cb=jQuery" 2>/dev/null | grep -o '"total":[0-9]*' | head -1 | cut -d: -f2)
    local down=$(curl -s "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=1&po=0&np=1&ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&fields=f12&cb=jQuery" 2>/dev/null | grep -o '"total":[0-9]*' | head -1 | cut -d: -f2)
    echo "${up:-0}|${down:-0}"
}

divider() { echo "━━━━━━━━━━━━━━━━"; }

build_header() {
    local type="$1"
    local time="$2"
    echo "📊 ${type} | $(date '+%Y-%m-%d') ${time}"
    divider
}
