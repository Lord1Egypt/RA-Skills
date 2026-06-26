#!/bin/bash

# Insights Generator Module for Review Analyzer
# Generates deep insights report from tagged reviews

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPTS_DIR="$(dirname "$SCRIPT_DIR")/prompts"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to print progress
progress() {
    echo -e "${BLUE}[PROGRESS]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to calculate statistics from tagged reviews
calculate_statistics() {
    local tagged_json="$1"

    if ! command -v python3 &> /dev/null; then
        error "Python3 required for statistics calculation"
        return 1
    fi

    python3 << 'PYTHON_SCRIPT'
import json
import sys
from collections import Counter
from datetime import datetime

def main():
    # Load tagged data
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        print(json.dumps({"error": "Failed to load tagged data"}))
        sys.exit(1)

    if not isinstance(data, list):
        data = [data]

    total = len(data)
    tagged = sum(1 for item in data if item.get('tags'))

    # Sentiment distribution
    sentiment_dist = Counter()
    for item in data:
        s = item.get('sentiment', 'unknown')
        sentiment_dist[s] += 1

    # Top tags extraction
    all_tags = Counter()
    for item in data:
        tags = item.get('tags', {})
        for key, value in tags.items():
            if value and value not in ['未提及', '不明', 'unknown']:
                tag_name = f"{key}:{value}"
                all_tags[tag_name] += 1

    top_tags = dict(all_tags.most_common(15))

    # User personas clustering (simplified)
    personas = []

    # Group by unique combinations of gender + age + occupation
    persona_groups = {}
    for item in data:
        tags = item.get('tags', {})
        gender = tags.get('人群_性别', '不明')
        age = tags.get('人群_年龄段', '不明')
        occupation = tags.get('人群_职业', '不明')

        key = f"{gender}_{age}_{occupation}"
        if key not in persona_groups:
            persona_groups[key] = {
                'name': f"{occupation} ({age}, {gender})",
                'count': 0,
                'tags': {}
            }
        persona_groups[key]['count'] += 1
        persona_groups[key]['tags'] = tags

    # Convert to list and sort by count
    for p in persona_groups.values():
        personas.append(p)

    personas.sort(key=lambda x: x['count'], reverse=True)

    # Output statistics
    stats = {
        'total': total,
        'tagged': tagged,
        'sentiment': dict(sentiment_dist),
        'top_tags': top_tags,
        'personas': personas[:4]  # Top 4 personas
    }

    print(json.dumps(stats, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
PYTHON_SCRIPT
}

# Function to select golden samples
select_golden_samples() {
    local tagged_json="$1"
    local count="${2:-12}"

    if ! command -v python3 &> /dev/null; then
        error "Python3 required for sample selection"
        return 1
    fi

    python3 << 'PYTHON_SCRIPT'
import json
import sys

def main():
    # Load tagged data
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        print(json.dumps([]))
        sys.exit(1)

    if not isinstance(data, list):
        data = [data]

    # Sort by info_score
    scored = [(item, item.get('info_score', 0)) for item in data]
    scored.sort(key=lambda x: x[1], reverse=True)

    # Select top samples
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    samples = [item for item, score in scored[:count]]

    print(json.dumps(samples, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
PYTHON_SCRIPT
}

# Function to format personas details
format_personas() {
    local personas_json="$1"

    if ! command -v python3 &> /dev/null; then
        echo "$personas_json"
        return
    fi

    python3 << 'PYTHON_SCRIPT'
import json
import sys

def main():
    try:
        personas = json.load(sys.stdin)
    except:
        return

    for i, p in enumerate(personas):
        print(f"### 画像 {i+1}: {p['name']} ({p['count']} 条)")

        tags = p.get('tags', {})
        valid_tags = [f"{k}:{v}" for k, v in tags.items()
                     if v and v not in ['未提及', '不明', 'unknown']]

        if valid_tags:
            print(f"标签特征: {', '.join(valid_tags[:8])}")
        print()

if __name__ == '__main__':
    main()
PYTHON_SCRIPT
}

# Function to format sentiment distribution
format_sentiment() {
    local stats_json="$1"
    local total="$2"

    if ! command -v python3 &> /dev/null; then
        return
    fi

    python3 << 'PYTHON_SCRIPT'
import json
import sys

def main():
    try:
        stats = json.load(sys.stdin)
        sentiment = stats.get('sentiment', {})
        total = stats.get('total', 1)

        for s, c in sentiment.items():
            pct = (c / total * 100) if total > 0 else 0
            print(f"- **{s}**: {c} 条 ({pct:.1f}%)")
    except:
        pass

if __name__ == '__main__':
    main()
PYTHON_SCRIPT
}

# Function to format top tags
format_top_tags() {
    local stats_json="$1"

    if ! command -v python3 &> /dev/null; then
        return
    fi

    python3 << 'PYTHON_SCRIPT'
import json
import sys

def main():
    try:
        stats = json.load(sys.stdin)
        top_tags = stats.get('top_tags', {})

        for i, (tag, count) in enumerate(list(top_tags.items())[:15]):
            print(f"{i+1}. **{tag}**: {count} 次")
    except:
        pass

if __name__ == '__main__':
    main()
PYTHON_SCRIPT
}

# Function to format golden samples
format_samples() {
    local samples_json="$1"

    if ! command -v python3 &> /dev/null; then
        return
    fi

    python3 << 'PYTHON_SCRIPT'
import json
import sys

def main():
    try:
        samples = json.load(sys.stdin)
    except:
        return

    for i, s in enumerate(samples):
        print(f"### 样本 {i+1}")
        print(f"**情感**: {s.get('sentiment', '不明')}")
        print(f"**内容**: {s.get('body', '')[:200]}...")

        tags = s.get('tags', {})
        valid_tags = [f"{k}:{v}" for k, v in tags.items()
                     if v and v not in ['未提及', '不明', 'unknown']]

        if valid_tags:
            print(f"**标签**: {', '.join(valid_tags[:6])}")
        print()

if __name__ == '__main__':
    main()
PYTHON_SCRIPT
}

# Function to create insights prompt
create_insights_prompt() {
    local stats_json="$1"
    local personas_json="$2"
    local samples_json="$3"
    local asin="${4:-unknown}"
    local product_name="${5:-}"

    local prompt_template="$PROMPTS_DIR/insights.txt"

    if [[ ! -f "$prompt_template" ]]; then
        error "Prompt template not found: $prompt_template"
        return 1
    fi

    # Extract statistics
    local total=$(echo "$stats_json" | jq -r '.total // 0')
    local tagged=$(echo "$stats_json" | jq -r '.tagged // 0')

    # Format sections
    local personas_details=$(echo "$personas_json" | format_personas)
    local sentiment_distribution=$(echo "$stats_json" | format_sentiment "$total")
    local top_tags=$(echo "$stats_json" | format_top_tags)
    local golden_samples=$(echo "$samples_json" | format_samples)

    # Get current date
    local date=$(date +"%Y-%m-%d")

    # Read and format prompt
    local prompt=$(cat "$prompt_template")
    prompt="${prompt//{total}/$total}"
    prompt="${prompt//{tagged}/$tagged}"
    prompt="${prompt//{asin}/$asin}"
    prompt="${prompt//{product_name}/$product_name}"
    prompt="${prompt//{date}/$date}"
    prompt="${prompt//{personas_count}/$(echo "$personas_json" | jq '. | length')}"
    prompt="${prompt//{personas_details}/$personas_details}"
    prompt="${prompt//{sentiment_distribution}/$sentiment_distribution}"
    prompt="${prompt//{top_tags}/$top_tags}"
    prompt="${prompt//{samples_count}/$(echo "$samples_json" | jq '. | length')}"
    prompt="${prompt//{golden_samples}/$golden_samples}"

    echo "$prompt"
}

# Function to extract strategic JSON from report
extract_strategic_json() {
    local report_file="$1"

    # Extract JSON block between <strategic_json> tags
    sed -n '/<strategic_json>/,/<\/strategic_json>/p' "$report_file" | \
        sed '1d;$d' | \
        jq '.' 2>/dev/null || echo '{}'
}

# Function to validate insights report
validate_insights_report() {
    local report_file="$1"

    # Check required sections
    local required_sections=(
        "洞察总览"
        "数据统计"
        "核心用户画像"
        "核心卖点"
        "痛点"
        "改进建议"
        "潜在机会"
        "典型用户"
        "洞察总结"
        "strategic_json"
    )

    local missing=()
    for section in "${required_sections[@]}"; do
        if ! grep -q "$section" "$report_file"; then
            missing+=("$section")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        error "Missing sections in report: ${missing[*]}"
        return 1
    fi

    # Validate strategic JSON
    local strategic_json=$(extract_strategic_json "$report_file")
    if ! echo "$strategic_json" | jq '.moat and .vulnerability and .execution_matrix' > /dev/null 2>&1; then
        error "Invalid strategic JSON structure"
        return 1
    fi

    return 0
}

# Main function
main() {
    local action="$1"
    shift

    case "$action" in
        "stats")
            calculate_statistics "$@"
            ;;
        "samples")
            select_golden_samples "$@"
            ;;
        "prompt")
            create_insights_prompt "$@"
            ;;
        "validate")
            validate_insights_report "$@"
            ;;
        "extract-json")
            extract_strategic_json "$@"
            ;;
        *)
            echo "Usage: $0 {stats|samples|prompt|validate|extract-json} ..."
            exit 1
            ;;
    esac
}

main "$@"
