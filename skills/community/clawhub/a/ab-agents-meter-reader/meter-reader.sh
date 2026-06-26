#!/bin/bash
# AB Agents Meter Reader
# Reads meter readings from photos

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${HOME}/.meter-readings"
CONFIG_FILE="${CONFIG_DIR}/config.json"
HISTORY_FILE="${CONFIG_DIR}/history.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Load config
load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        TENANT_NAME=$(cat "$CONFIG_FILE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tenant_name',''))" 2>/dev/null || echo "")
        APARTMENT_ADDR=$(cat "$CONFIG_FILE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('apartment_address',''))" 2>/dev/null || echo "")
        METER_LAYOUT=$(cat "$CONFIG_FILE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('meter_layout','left=hot,right=cold'))" 2>/dev/null || echo "left=hot,right=cold")
    else
        TENANT_NAME=""
        APARTMENT_ADDR=""
        METER_LAYOUT="left=hot,right=cold"
    fi
}

# Save config
save_config() {
    mkdir -p "$CONFIG_DIR"
    cat > "$CONFIG_FILE" << EOF
{
    "tenant_name": "$TENANT_NAME",
    "apartment_address": "$APARTMENT_ADDR",
    "meter_layout": "$METER_LAYOUT"
}
EOF
}

# Setup (first run)
setup() {
    echo -e "${YELLOW}=== First Run Setup ===${NC}"
    echo ""
    
    read -p "Your name (tenant): " TENANT_NAME
    read -p "Apartment address: " APARTMENT_ADDR
    echo ""
    echo "Meter layout - how to tell hot/cold water apart?"
    echo "  1) left=hot,right=cold (default)"
    echo "  2) left=cold,right=hot"
    echo "  3) Custom description"
    read -p "Choice [1]: " LAYOUT_CHOICE
    
    case "$LAYOUT_CHOICE" in
        2) METER_LAYOUT="left=cold,right=hot" ;;
        3) read -p "Custom layout: " METER_LAYOUT ;;
        *) METER_LAYOUT="left=hot,right=cold" ;;
    esac
    
    save_config
    echo -e "${GREEN}✓ Setup complete!${NC}"
    echo ""
}

# Analyze meter photo
analyze_meter() {
    local IMAGE_PATH="$1"
    local PROMPT="$2"
    
    source /root/.openclaw/.minimax-env 2>/dev/null || true
    
    if [[ -z "${MINIMAX_API_KEY:-}" ]]; then
        echo -e "${RED}Error: MINIMAX_API_KEY not set${NC}"
        exit 1
    fi
    
    # MCP call
    {
        echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"meter-reader","version":"1.0"}}}'
        sleep 1
        echo "{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/call\",\"params\":{\"name\":\"understand_image\",\"arguments\":{\"prompt\":\"$PROMPT\",\"image_source\":\"$IMAGE_PATH\"}}}"
    } | uvx minimax-coding-plan-mcp 2>/dev/null | python3 -c "
import json, sys
for line in sys.stdin:
    try:
        resp = json.loads(line)
        if resp.get('id') == 2 and 'result' in resp:
            for item in resp['result'].get('content', []):
                if item.get('type') == 'text' and not item.get('isError'):
                    print(item['text'])
                    exit(0)
    except: continue
"
}

# Parse reading from vision output
parse_reading() {
    local text="$1"
    local pattern="$2"
    
    # Try to extract number
    echo "$text" | grep -oE "[0-9]{4,}" | head -1 || echo ""
}

# Read electricity meter
read_electricity() {
    local IMAGE_PATH="$1"
    local TYPE="$2"  # single, dual
    
    echo -e "${YELLOW}Analyzing electricity meter...${NC}"
    
    if [[ "$TYPE" == "dual" ]]; then
        # Day (T1)
        echo -n "Day (T1): "
        RESULT=$(analyze_meter "$IMAGE_PATH" "Это электрический счётчик. Какая цифра слева - 1 или 2? Какое число на экране в кВтч? Ответ: T1=число")
        echo "$RESULT"
        
        # Night (T2) - ask for second reading
        echo "If meter shows T2, what's the number?"
        echo "(If same photo shows both, tell me both T1 and T2 readings)"
    else
        echo -n "Reading: "
        RESULT=$(analyze_meter "$IMAGE_PATH" "Это электрический счётчик. Какое число на экране в кВтч?")
        echo "$RESULT"
    fi
}

# Read water meter
read_water() {
    local IMAGE_PATH="$1"
    
    echo -e "${YELLOW}Analyzing water meters...${NC}"
    RESULT=$(analyze_meter "$IMAGE_PATH" "Это счётчики воды. Слева обычно холодная, справа горячая. Какие числа показаны в кубометрах? Ответ формат: холодная=число, горячая=число")
    echo "$RESULT"
}

# Save reading
save_reading() {
    local DATE=$(date +%Y-%m-%d)
    local ELEC_DAY="$1"
    local ELEC_NIGHT="$2"
    local WATER_COLD="$3"
    local WATER_HOT="$4"
    
    mkdir -p "$CONFIG_DIR"
    
    # Create or update history
    if [[ -f "$HISTORY_FILE" ]]; then
        # Add new reading
        python3 << PY
import json

with open("$HISTORY_FILE", 'r') as f:
    data = json.load(f)

if "readings" not in data:
    data["readings"] = []

data["readings"].append({
    "date": "$DATE",
    "electricity_day": $ELEC_DAY,
    "electricity_night": $ELEC_NIGHT,
    "water_cold": $WATER_COLD,
    "water_hot": $WATER_HOT
})

with open("$HISTORY_FILE", 'w') as f:
    json.dump(data, f, indent=2)
PY
    else
        cat > "$HISTORY_FILE" << EOF
{
    "config": {
        "tenant": "$TENANT_NAME",
        "address": "$APARTMENT_ADDR",
        "layout": "$METER_LAYOUT"
    },
    "readings": [
        {
            "date": "$DATE",
            "electricity_day": $ELEC_DAY,
            "electricity_night": $ELEC_NIGHT,
            "water_cold": $WATER_COLD,
            "water_hot": $WATER_HOT
        }
    ]
}
EOF
    fi
    
    echo -e "${GREEN}✓ Reading saved!${NC}"
}

# Generate message for landlord
generate_message() {
    local DATE=$(date +%Y-%m-%d)
    
    # Get latest reading
    if [[ -f "$HISTORY_FILE" ]]; then
        LAST=$(python3 -c "
import json
with open('$HISTORY_FILE', 'r') as f:
    data = json.load(f)
readings = data.get('readings', [])
if readings:
    r = readings[-1]
    print(f\"{r['electricity_day']}|{r['electricity_night']}|{r['water_cold']}|{r['water_hot']}\")
" 2>/dev/null)
        
        if [[ -n "$LAST" ]]; then
            IFS='|' read -r ELEC_DAY ELEC_NIGHT WATER_COLD WATER_HOT <<< "$LAST"
            
            cat << EOF
Добрый вечер!

Показания счётчиков на $DATE:

⚡ Электричество:
- День (Т1): $ELEC_DAY кВтч
- Ночь (Т2): $ELEC_NIGHT кВтч

💧 Вода:
- Холодная: $WATER_COLD м³
- Горячая: $WATER_HOT м³

---
Квартира: $APARTMENT_ADDR
Арендатор: $TENANT_NAME
EOF
            return
        fi
    fi
    
    echo "No readings found. Run meter-reader.sh first."
}

# Main
load_config

# Check if first run
if [[ -z "$TENANT_NAME" ]] || [[ "$1" == "--setup" ]]; then
    setup
fi

case "${1:-}" in
    --message|-m)
        generate_message
        ;;
    --setup)
        setup
        ;;
    --history)
        cat "$HISTORY_FILE" 2>/dev/null || echo "No history yet"
        ;;
    *)
        if [[ $# -eq 0 ]]; then
            echo "Usage: meter-reader.sh <photo.jpg> [type]"
            echo "  type: electricity, water, auto (default)"
            exit 1
        fi
        
        IMAGE_PATH="$1"
        TYPE="${2:-auto}"
        
        if [[ ! -f "$IMAGE_PATH" ]]; then
            echo -e "${RED}File not found: $IMAGE_PATH${NC}"
            exit 1
        fi
        
        if [[ "$TYPE" == "auto" ]]; then
            # Try to detect type from image
            RESULT=$(analyze_meter "$IMAGE_PATH" "Это счётчик электричества или воды? Ответь одним словом: электричество или вода")
            
            if echo "$RESULT" | grep -qi "электричество\|electricity\|счётчик"; then
                TYPE="electricity"
            else
                TYPE="water"
            fi
        fi
        
        case "$TYPE" in
            electricity|elec)
                read_electricity "$IMAGE_PATH" dual
                ;;
            water)
                read_water "$IMAGE_PATH"
                ;;
            *)
                echo -e "${RED}Unknown type: $TYPE${NC}"
                exit 1
                ;;
        esac
        ;;
esac
