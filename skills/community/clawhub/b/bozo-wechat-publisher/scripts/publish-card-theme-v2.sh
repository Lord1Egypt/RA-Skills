#!/usr/bin/env bash
# bozo-wechat-publisher: 使用自定义卡片主题发布到微信公众号 v2
# 将主题 CSS 内联到 body 中，只发送 body 内容到微信 API
# Usage: ./publish-card-theme-v2.sh <markdown-file> <theme-id>

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# 技能目录
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
THEMES_DIR="$SKILL_DIR/themes"

# 默认配置
DEFAULT_THEME="card-tech-dark"
DEFAULT_HIGHLIGHT="dracula"
TOOLS_MD="$HOME/.openclaw/workspace/TOOLS.md"

# 微信 API 端点
TOKEN_URL="https://api.weixin.qq.com/cgi-bin/token"
STABLE_TOKEN_URL="https://api.weixin.qq.com/cgi-bin/stable_token"
UPLOAD_URL="https://api.weixin.qq.com/cgi-bin/material/add_material"
DRAFT_URL="https://api.weixin.qq.com/cgi-bin/draft/add"

# 打印函数
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_header() {
    echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# 检查 wenyan-cli
check_wenyan() {
    if ! command -v wenyan &> /dev/null; then
        print_error "wenyan-cli 未安装！"
        npm install -g @wenyan-md/cli
    fi
}

# 从 TOOLS.md 读取环境变量
load_credentials() {
    if [ -z "$WECHAT_APP_ID" ] || [ -z "$WECHAT_APP_SECRET" ]; then
        if [ -f "$TOOLS_MD" ]; then
            print_info "从 TOOLS.md 读取凭证..."
            export WECHAT_APP_ID=$(grep "export WECHAT_APP_ID=" "$TOOLS_MD" 2>/dev/null | head -1 | sed 's/.*export WECHAT_APP_ID=//' | tr -d ' "' || echo "")
            export WECHAT_APP_SECRET=$(grep "export WECHAT_APP_SECRET=" "$TOOLS_MD" 2>/dev/null | head -1 | sed 's/.*export WECHAT_APP_SECRET=//' | tr -d ' "' || echo "")
        fi
    fi
}

# 检查环境变量
check_env() {
    load_credentials
    if [ -z "$WECHAT_APP_ID" ] || [ -z "$WECHAT_APP_SECRET" ]; then
        print_error "环境变量未设置！"
        exit 1
    fi
}

# 检查文件
check_file() {
    local file="$1"
    if [ ! -f "$file" ]; then
        print_error "文件不存在: $file"
        exit 1
    fi
}

# 检查主题
check_theme() {
    local theme_id="$1"
    local theme_file="$THEMES_DIR/${theme_id}.html"
    if [ ! -f "$theme_file" ]; then
        print_error "主题文件不存在: $theme_file"
        exit 1
    fi
    echo "$theme_file"
}

# 提取 frontmatter 字段
extract_field() {
    local file="$1"
    local field="$2"
    grep "^${field}:" "$file" | head -1 | sed "s/^${field}: *//" | tr -d '"'
}

# 从主题文件中提取 CSS 样式（去掉 head 标签）
extract_theme_css() {
    local theme_file="$1"
    # 提取 <style> 标签内的内容
    sed -n '/<style>/,/<\/style>/p' "$theme_file" | sed '1d;$d'
}

# 发布文章
publish_article() {
    local markdown_file="$1"
    local theme_id="$2"
    local theme_file="$3"

    print_header "准备发布"

    # 提取元数据
    local title=$(extract_field "$markdown_file" "title")
    local cover=$(extract_field "$markdown_file" "cover")
    local author=$(extract_field "$markdown_file" "author")
    local source_url=$(extract_field "$markdown_file" "source_url")

    # 验证必填字段
    if [ -z "$title" ]; then
        print_error "frontmatter 缺少 title 字段"
        exit 1
    fi

    print_info "文章信息:"
    echo "  标题: $title"
    echo "  作者: ${author:-未设置}"
    echo "  主题: $theme_id"
    echo ""

    # 使用 wenyan-cli 渲染 HTML
    print_info "使用 wenyan-cli 渲染文章..."

    local tmp_html=$(mktemp)
    wenyan render -f "$markdown_file" -t default -h "$DEFAULT_HIGHLIGHT" --no-mac-style > "$tmp_html"

    if [ $? -ne 0 ]; then
        print_error "wenyan 渲染失败"
        rm -f "$tmp_html"
        exit 1
    fi

    print_success "HTML 渲染完成"

    # wenyan render 输出不是完整的 HTML，直接使用整个输出
    # 输出以 <section id="wenyan"> 开头，没有 <html>/<body> 标签
    local body_content=$(cat "$tmp_html")
    rm -f "$tmp_html"

    # 提取主题 CSS 样式
    print_info "应用主题样式..."
    local theme_css=$(extract_theme_css "$theme_file")

    # 创建最终 HTML：style 标签 + body 内容
    local final_content="<style>${theme_css}</style>${body_content}"

    print_success "主题应用完成"
    echo ""

    # 获取稳定版 access_token
    print_info "获取 access_token..."
    local response=$(curl -s -X POST "${STABLE_TOKEN_URL}" \
        -H "Content-Type: application/json" \
        -d "{\"grant_type\":\"client_credential\",\"appid\":\"${WECHAT_APP_ID}\",\"secret\":\"${WECHAT_APP_SECRET}\"}")
    local access_token=$(echo "$response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    local errcode=$(echo "$response" | grep -o '"errcode":[0-9]*' | cut -d':' -f2)

    if [ -n "$errcode" ] && [ "$errcode" != "0" ]; then
        local errmsg=$(echo "$response" | grep -o '"errmsg":"[^"]*"' | cut -d'"' -f4)
        print_error "获取 access_token 失败: $errmsg"
        exit 1
    fi

    print_success "access_token 获取成功"

    # 上传封面图（必须）
    local thumb_media_id=""
    if [ -n "$cover" ]; then
        print_info "上传封面图..."
        local cover_path=""
        if [[ "$cover" == /* ]]; then
            cover_path="$cover"
        else
            local md_dir=$(dirname "$markdown_file")
            cover_path="$md_dir/$cover"
        fi

        if [ -f "$cover_path" ]; then
            local upload_response=$(curl -s -X POST \
                "${UPLOAD_URL}?access_token=${access_token}&type=image" \
                -F "media=@${cover_path}")
            thumb_media_id=$(echo "$upload_response" | grep -o '"media_id":"[^"]*"' | cut -d'"' -f4)
            if [ -n "$thumb_media_id" ]; then
                print_success "封面图上传成功"
            else
                print_warn "封面图上传失败，将使用默认封面"
            fi
        else
            print_warn "封面图不存在: $cover_path"
        fi
    fi

    # 如果没有封面图，使用默认图片
    if [ -z "$thumb_media_id" ]; then
        print_warn "使用默认封面图"
        # 使用主题中的 logo.png 作为默认封面
        local default_cover="$SKILL_DIR/assets/logo.png"
        if [ -f "$default_cover" ]; then
            local upload_response=$(curl -s -X POST \
                "${UPLOAD_URL}?access_token=${access_token}&type=image" \
                -F "media=@${default_cover}")
            thumb_media_id=$(echo "$upload_response" | grep -o '"media_id":"[^"]*"' | cut -d'"' -f4)
        fi
    fi
    echo ""

    # 转义 HTML 内容为 JSON 字符串
    local escaped_content=$(echo "$final_content" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | tr -d '\n' | tr -d '\r')

    # 构建 JSON payload（必须包含 thumb_media_id）
    local json_payload=$(mktemp)
    cat > "$json_payload" << EOF
{
  "articles": [
    {
      "title": "$title",
      "author": "${author:-}",
      "content": "$escaped_content",
      "digest": "",
      "content_source_url": "${source_url:-}",
      "thumb_media_id": "$thumb_media_id",
      "show_cover_pic": 1
    }
  ]
}
EOF

    # 发布草稿
    print_info "发布到草稿箱..."
    response=$(curl -s -X POST \
        "${DRAFT_URL}?access_token=${access_token}" \
        -H "Content-Type: application/json" \
        -d @"$json_payload")

    rm -f "$json_payload"

    # 打印 API 响应（调试）
    print_info "API 响应: $response"
    echo ""

    # 检查结果
    errcode=$(echo "$response" | grep -o '"errcode":[0-9]*' | cut -d':' -f2)

    if [ -z "$errcode" ] || [ "$errcode" == "0" ]; then
        local media_id=$(echo "$response" | grep -o '"media_id":"[^"]*"' | cut -d'"' -f4)
        print_success "发布成功！"
        echo ""
        echo -e "${GREEN}═══════════════════════════════════════${NC}"
        echo -e "${GREEN}  📱 文章已发布到草稿箱${NC}"
        echo -e "${GREEN}═══════════════════════════════════════${NC}"
        echo ""
        echo "  media_id: $media_id"
        echo ""
        echo "  请前往微信公众号后台查看:"
        echo "  https://mp.weixin.qq.com/"
        echo ""
        echo -e "${PURPLE}主题: $theme_id${NC}"
    else
        local errmsg=$(echo "$response" | grep -o '"errmsg":"[^"]*"' | cut -d'"' -f4)
        print_error "发布失败: $errmsg (errcode: $errcode)"
        exit 1
    fi
}

# 显示帮助
show_help() {
    cat << EOF
Usage: $0 <markdown-file> [theme-id]

使用自定义卡片主题发布 Markdown 文章到微信公众号草稿箱。
主题 CSS 样式会被内联到 body 中。

Arguments:
  markdown-file    要发布的 Markdown 文件路径
  theme-id         主题 ID (默认: card-tech-dark)

可用主题:
  card-tech-dark   卡片科技暗色 (默认)
  card-neon-light  卡片霓虹浅色

Examples:
  $0 article.md
  $0 article.md card-tech-dark
  $0 article.md card-neon-light
EOF
}

# 主函数
main() {
    if [ $# -eq 0 ] || [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
        show_help
        exit 0
    fi

    local markdown_file="$1"
    local theme_id="${2:-$DEFAULT_THEME}"

    check_wenyan
    check_env
    check_file "$markdown_file"

    local theme_file=$(check_theme "$theme_id")
    publish_article "$markdown_file" "$theme_id" "$theme_file"
}

# 运行
main "$@"
