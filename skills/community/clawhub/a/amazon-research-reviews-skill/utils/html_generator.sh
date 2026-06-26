#!/bin/bash

# HTML Generator Module for Review Analyzer
# Generates interactive HTML visualization dashboard

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$(dirname "$SCRIPT_DIR")/templates"

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

# Function to escape HTML special characters
escape_html() {
    local text="$1"
    text="${text//&/&amp;}"
    text="${text//</&lt;}"
    text="${text//>/&gt;}"
    text="${text//\"/&quot;}"
    text="${text//\'/&#39;}"
    echo "$text"
}

# Function to convert markdown to HTML (basic)
markdown_to_html() {
    local md="$1"

    # Headers
    md=$(echo "$md" | sed 's/^# \(.*\)/<h1>\1<\/h1>/')
    md=$(echo "$md" | sed 's/^## \(.*\)/<h2>\1<\/h2>/')
    md=$(echo "$md" | sed 's/^### \(.*\)/<h3>\1<\/h3>/')

    # Bold
    md=$(echo "$md" | sed 's/\*\*\([^*]*\)\*\*/<strong>\1<\/strong>/g')

    # Italic
    md=$(echo "$md" | sed 's/\*\([^*]*\)\*/<em>\1<\/em>/g')

    # Links
    md=$(echo "$md" | sed 's/\[\([^]]*\)\](\([^)]*\))/<a href="\2">\1<\/a>/g')

    # Code blocks (basic)
    md=$(echo "$md" | sed 's/`\([^`]*\)`/<code>\1<\/code>/g')

    # Blockquotes
    md=$(echo "$md" | sed 's/^> \(.*\)/<blockquote>\1<\/blockquote>/')

    # Unordered lists (basic - single line)
    md=$(echo "$md" | sed 's/^- \(.*\)/<li>\1<\/li>/g')

    # Paragraphs (wrap text lines)
    # This is simplified; real markdown parsing is more complex

    echo "$md"
}

# Function to generate sentiment bar HTML
generate_sentiment_bar() {
    local label="$1"
    local count="$2"
    local total="$3"
    local color="$4"

    local percent=0
    if [[ "$total" -gt 0 ]]; then
        percent=$(awk "BEGIN {printf \"%.1f\", ($count / $total) * 100}")
    fi

    cat << EOF
                    <div class="sentiment-bar">
                        <div class="sentiment-label">$label</div>
                        <div class="sentiment-track">
                            <div class="sentiment-fill" style="width: $percent%; --sentiment-color: $color;"></div>
                        </div>
                        <div class="sentiment-value">$count ($percent%)</div>
                    </div>
EOF
}

# Function to generate persona card HTML
generate_persona_card() {
    local name="$1"
    local count="$2"
    local color="$3"
    local tags_json="$4"

    # Extract first few tags
    local tags_html=""
    if command -v jq &> /dev/null; then
        local tag_count=$(echo "$tags_json" | jq '. | length' 2>/dev/null || echo "0")
        local i=0
        while [[ $i -lt $tag_count && $i -lt 6 ]]; do
            local key=$(echo "$tags_json" | jq -r ".keys()[$i]" 2>/dev/null)
            local value=$(echo "$tags_json" | jq -r ".\"$key\"" 2>/dev/null)

            if [[ "$value" && "$value" != "未提及" && "$value" != "不明" && "$value" != "无" ]]; then
                tags_html="$tags_html                        <div class=\"persona-tag\">
                            ${key}: <span class=\"persona-tag-value\">${value}</span>
                        </div>
"
            fi
            ((i++))
        done
    fi

    cat << EOF
                <div class="persona-card" style="--persona-color: $color;">
                    <div class="persona-header">
                        <div class="persona-name">$name</div>
                        <div class="persona-count">$count 条</div>
                    </div>
                    <div class="persona-tags">
$tags_html                    </div>
                </div>
EOF
}

# Function to generate tag item HTML
generate_tag_item() {
    local tag_name="$1"
    local count="$2"

    cat << EOF
                <div class="tag-item">
                    <span class="tag-name">$tag_name</span>
                    <span class="tag-count">$count</span>
                </div>
EOF
}

# Function to generate sample card HTML
generate_sample_card() {
    local sentiment="$1"
    local rating="$2"
    local body="$3"
    local info_score="$4"

    # Determine sentiment class
    local sentiment_class="neutral"
    case "$sentiment" in
        "强烈推荐") sentiment_class="strong-positive" ;;
        "推荐") sentiment_class="positive" ;;
        "中立") sentiment_class="neutral" ;;
        "不推荐") sentiment_class="negative" ;;
        "强烈不推荐") sentiment_class="strong-negative" ;;
    esac

    # Generate stars
    local stars=""
    local rating_int=${rating%.*}
    for ((i=0; i<rating_int && i<5; i++)); do
        stars="$stars                            <svg width=\"14\" height=\"14\" viewBox=\"0 0 24 24\" fill=\"currentColor\">
                                <path d=\"M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z\"/>
                            </svg>
"
    done

    # Escape body
    local body_escaped=$(escape_html "$body")

    cat << EOF
                <div class="sample-card" onclick="this.classList.toggle('expanded')">
                    <div class="sample-header">
                        <span class="sample-sentiment $sentiment_class">$sentiment</span>
                        <div class="sample-rating">
$stars                        </div>
                    </div>
                    <div class="sample-body">
                        <p class="sample-text">$body_escaped</p>
EOF

    if [[ -n "$info_score" ]]; then
        cat << EOF
                        <div class="sample-tags">
                            <span class="sample-tag" style="border-color: var(--accent-gold); color: var(--accent-gold);">信息密度: $info_score/20</span>
                        </div>
EOF
    fi

    cat << EOF
                    </div>
                </div>
EOF
}

# Function to generate HTML report
generate_html_report() {
    local stats_json="$1"
    local tagged_data="$2"
    local insights_md="$3"
    local output_file="$4"

    progress "Generating HTML visualization dashboard..."

    # Extract statistics
    local total=$(echo "$stats_json" | jq -r '.total // 0')
    local tagged=$(echo "$stats_json" | jq -r '.tagged // 0')
    local avg_rating=$(echo "$stats_json" | jq -r '.avg_rating // 0')

    # Get current date
    local analysis_date=$(date +"%Y年%m月%d日")

    # Determine ASIN/product name
    local asin="UNKNOWN"
    local product_name="产品评论分析"

    # Read template
    local template="$TEMPLATES_DIR/report.html"
    if [[ ! -f "$template" ]]; then
        # Use fallback minimal template
        template=""
    fi

    # Build HTML content
    local html_content=""

    if [[ -n "$template" ]]; then
        # Read and process template
        html_content=$(cat "$template")

        # Replace placeholders (using sed for simple replacements)
        html_content="${html_content//\{\{ asin \}\}/$asin}"
        html_content="${html_content//\{\{ analysis_date \}\}/$analysis_date}"
        html_content="${html_content//\{\{ product_name \}\}/$product_name}"
        html_content="${html_content//\{\{ summary.total_reviews \}\}/$total}"
        html_content="${html_content//\{\{ summary.tagged_reviews \}\}/$tagged}"
        html_content="${html_content//\{\{ summary.avg_rating \}\}/$avg_rating}"

        # Note: Complex Jinja2 template processing would require Python/jinja2
        # For bash-only solution, we need a simpler template or pre-processing
    else
        # Generate minimal HTML
        html_content=$(generate_minimal_html "$stats_json" "$tagged_data" "$insights_md")
    fi

    # Write output
    echo "$html_content" > "$output_file"

    success "HTML report generated: $output_file"
}

# Function to generate minimal HTML (fallback)
generate_minimal_html() {
    local stats_json="$1"
    local tagged_data="$2"
    local insights_md="$3"

    local total=$(echo "$stats_json" | jq -r '.total // 0')
    local tagged=$(echo "$stats_json" | jq -r '.tagged // 0')
    local date=$(date +"%Y年%m月%d日")

    # Convert insights markdown to HTML
    local insights_html=$(markdown_to_html "$insights_md")

    cat << EOF
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>评论分析报告</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #0d1117; color: #f0f6fc; line-height: 1.6; padding: 2rem; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #d29922; border-bottom: 1px solid rgba(210, 153, 34, 0.2); padding-bottom: 1rem; }
        h2 { color: #f0f6fc; margin-top: 2rem; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 2rem 0; }
        .stat-card { background: #161b22; padding: 1.5rem; border-left: 3px solid #d29922; }
        .stat-value { font-size: 2rem; font-weight: bold; color: #f0f6fc; }
        .stat-label { color: #8b949e; font-size: 0.875rem; text-transform: uppercase; }
        .insights { background: #161b22; padding: 2rem; border-radius: 8px; }
        .footer { text-align: center; margin-top: 3rem; color: #6e7681; font-size: 0.875rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>评论深度洞察报告</h1>
        <p style="color: #8b949e;">分析时间: $date · 样本量: $total 条</p>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">$total<span style="font-size: 1rem; color: #8b949e;"> 条</span></div>
                <div class="stat-label">Total Reviews</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">$tagged<span style="font-size: 1rem; color: #8b949e;"> 条</span></div>
                <div class="stat-label">Tagged</div>
            </div>
        </div>

        <h2>深度洞察分析</h2>
        <div class="insights">
$insights_html
        </div>

        <div class="footer">
            <p>Generated by AI · $date</p>
            <p>Powered by Claude AI · 22-Dimension Tag System</p>
        </div>
    </div>
</body>
</html>
EOF
}

# Main function
main() {
    local action="$1"
    shift

    case "$action" in
        "generate")
            generate_html_report "$@"
            ;;
        "markdown")
            markdown_to_html "$@"
            ;;
        *)
            echo "Usage: $0 {generate|markdown} ..."
            exit 1
            ;;
    esac
}

main "$@"
