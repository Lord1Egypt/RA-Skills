#!/usr/bin/env bash
# bozo-wechat-publisher: 使用自定义卡片主题发布到微信公众号
# Usage: ./publish-card-theme.sh <markdown-file> <theme-id>

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
        print_info "正在安装 wenyan-cli..."
        npm install -g @wenyan-md/cli
        if [ $? -eq 0 ]; then
            print_success "wenyan-cli 安装成功！"
        else
            print_error "安装失败！请手动运行: npm install -g @wenyan-md/cli"
            exit 1
        fi
    fi
}

# 从 TOOLS.md 读取环境变量
load_credentials() {
    if [ -z "$WECHAT_APP_ID" ] || [ -z "$WECHAT_APP_SECRET" ]; then
        if [ -f "$TOOLS_MD" ]; then
            print_info "从 TOOLS.md 读取凭证..."
            export WECHAT_APP_ID=$(grep "export WECHAT_APP_ID=" "$TOOLS_MD" | head -1 | sed 's/.*export WECHAT_APP_ID=//' | tr -d ' "' || echo "")
            export WECHAT_APP_SECRET=$(grep "export WECHAT_APP_SECRET=" "$TOOLS_MD" | head -1 | sed 's/.*export WECHAT_APP_SECRET=//' | tr -d ' "' || echo "")
        fi
    fi
}

# 检查环境变量
check_env() {
    load_credentials

    if [ -z "$WECHAT_APP_ID" ] || [ -z "$WECHAT_APP_SECRET" ]; then
        print_error "环境变量未设置！"
        echo ""
        echo "请设置以下环境变量："
        echo "  export WECHAT_APP_ID=your_app_id"
        echo "  export WECHAT_APP_SECRET=your_app_secret"
        echo ""
        echo "或在 ~/.zshrc / ~/.bashrc 中添加上述配置"
        echo ""
        echo "或在 $TOOLS_MD 中添加："
        echo "  ## 🔐 WeChat Official Account"
        echo "  export WECHAT_APP_ID=your_app_id"
        echo "  export WECHAT_APP_SECRET=your_app_secret"
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
        print_info "可用主题: card-tech-dark, card-neon-light"
        exit 1
    fi

    echo "$theme_file"
}

# 获取 access_token
get_access_token() {
    print_info "获取 access_token..."
    local response=$(curl -s "${TOKEN_URL}?grant_type=client_credential&appid=${WECHAT_APP_ID}&secret=${WECHAT_APP_SECRET}")
    local access_token=$(echo "$response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    local errcode=$(echo "$response" | grep -o '"errcode":[0-9]*' | cut -d':' -f2)

    if [ -n "$errcode" ] && [ "$errcode" != "0" ]; then
        local errmsg=$(echo "$response" | grep -o '"errmsg":"[^"]*"' | cut -d'"' -f4)
        print_error "获取 access_token 失败: $errmsg (errcode: $errcode)"
        exit 1
    fi

    if [ -z "$access_token" ]; then
        print_error "获取 access_token 失败"
        echo "响应: $response"
        exit 1
    fi

    print_success "access_token 获取成功"
    echo "$access_token"
}

# 上传图片
upload_image() {
    local image_path="$1"
    local access_token="$2"

    print_info "上传图片: $(basename "$image_path")"

    local response=$(curl -s -X POST \
        "${UPLOAD_URL}?access_token=${access_token}&type=image" \
        -F "media=@${image_path}")

    local errcode=$(echo "$response" | grep -o '"errcode":[0-9]*' | cut -d':' -f2)

    if [ -n "$errcode" ] && [ "$errcode" != "0" ]; then
        local errmsg=$(echo "$response" | grep -o '"errmsg":"[^"]*"' | cut -d'"' -f4)
        print_error "上传图片失败: $errmsg"
        return 1
    fi

    local media_id=$(echo "$response" | grep -o '"media_id":"[^"]*"' | cut -d'"' -f4)
    local url=$(echo "$response" | grep -o '"url":"[^"]*"' | cut -d'"' -f4)

    print_success "图片上传成功"
    echo "$url|$media_id"
}

# 提取 frontmatter 字段
extract_field() {
    local file="$1"
    local field="$2"
    grep "^${field}:" "$file" | head -1 | sed "s/^${field}: *//" | tr -d '"'
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
        echo "请在文件顶部添加:"
        echo "---"
        echo "title: 文章标题"
        echo "cover: 封面图片路径或 URL"
        echo "---"
        exit 1
    fi

    if [ -z "$cover" ]; then
        print_warn "未指定封面图，将使用第一张图片作为封面"
    fi

    print_info "文章信息:"
    echo "  标题: $title"
    echo "  作者: ${author:-未设置}"
    echo "  主题: $theme_id"
    echo "  封面: ${cover:-未设置}"
    echo ""

    # 获取 access_token
    local access_token=$(get_access_token)
    echo ""

    # 处理封面图
    local thumb_media_id=""
    local cover_url=""

    if [ -n "$cover" ]; then
        if [[ "$cover" == http* ]]; then
            print_warn "网络封面图，直接使用 URL"
            cover_url="$cover"
        elif [ -f "$cover" ]; then
            local result=$(upload_image "$cover" "$access_token")
            cover_url=$(echo "$result" | cut -d'|' -f1)
            thumb_media_id=$(echo "$result" | cut -d'|' -f2)
        else
            # 尝试相对于 markdown 文件的路径
            local md_dir=$(dirname "$markdown_file")
            local cover_path="$md_dir/$cover"
            if [ -f "$cover_path" ]; then
                local result=$(upload_image "$cover_path" "$access_token")
                cover_url=$(echo "$result" | cut -d'|' -f1)
                thumb_media_id=$(echo "$result" | cut -d'|' -f2)
            else
                print_warn "封面图不存在: $cover"
            fi
        fi
    fi

    echo ""

    # 使用 wenyan-cli 渲染 HTML
    print_info "使用 wenyan-cli 渲染文章..."

    # 创建临时 HTML 文件
    local tmp_html=$(mktemp)

    # 先用 wenyan 渲染基础 HTML（使用默认主题）
    wenyan render -f "$markdown_file" -t default -h "$DEFAULT_HIGHLIGHT" --no-mac-style > "$tmp_html"

    if [ $? -ne 0 ]; then
        print_error "wenyan 渲染失败"
        rm -f "$tmp_html"
        exit 1
    fi

    print_success "HTML 渲染完成"

    # 提取 wenyan 生成的 body 内容
    local body_content=$(sed -n '/<body>/,/<\/body>/p' "$tmp_html" | sed '1d;$d')

    # 读取主题模板
    local theme_html=$(cat "$theme_file")

    # 创建最终 HTML（将 body_content 注入到主题模板中）
    local final_html=$(mktemp)

    # 提取主题的样式和结构
    echo "$theme_html" | sed "s|<!-- 内容将被 wenyan-cli 动态注入 -->|$body_content|" > "$final_html"

    # 清理临时文件
    rm -f "$tmp_html"

    print_success "主题应用完成"
    echo ""

    # 提取 body 内部的 HTML 内容（微信只需要 body 部分）
    local html_content=$(sed -n '/<body>/,/<\/body>/p' "$final_html" | sed '1d;$d')

    # 转义 HTML 内容为 JSON 字符串
    local escaped_content=$(echo "$html_content" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | tr -d '\n' | tr -d '\r')

    # 清理临时文件
    rm -f "$final_html"

    # 构建 JSON payload
    local json_payload=$(mktemp)

    # 如果没有封面图，设置 show_cover_pic 为 0
    local show_cover_pic=1
    if [ -z "$thumb_media_id" ]; then
        show_cover_pic=0
        print_warn "未上传封面图，将不显示封面"
    fi

    cat > "$json_payload" << EOF
{
  "articles": [
    {
      "title": "$title",
      "author": "${author:-}",
      "content": "$escaped_content",
      "digest": "",
      "content_source_url": "${source_url:-}",
      "show_cover_pic": $show_cover_pic
    }
  ]
}
EOF

    # 发布草稿
    print_info "发布到草稿箱..."
    local response=$(curl -s -X POST \
        "${DRAFT_URL}?access_token=${access_token}" \
        -H "Content-Type: application/json" \
        -d @"$json_payload")

    # 清理临时文件
    rm -f "$json_payload"

    # 检查结果
    print_info "API 响应: $response"

    local errcode=$(echo "$response" | grep -o '"errcode":[0-9]*' | cut -d':' -f2)

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
        echo ""
        echo "常见错误码:"
        echo "  40001  - AppID 或 AppSecret 错误"
        echo "  40002  - 请求格式错误"
        echo "  40004  - 封面图片无效"
        echo "  40005  - media_id 无效"
        echo "  40007  - media_id 不存在"
        echo "  61007  - content 包含违规内容"
        echo "  85006  - 群发文章数量超过限制"
        exit 1
    fi
}

# 显示帮助
show_help() {
    cat << EOF
Usage: $0 <markdown-file> [theme-id]

使用自定义卡片主题发布 Markdown 文章到微信公众号草稿箱。

Arguments:
  markdown-file    要发布的 Markdown 文件路径
  theme-id         主题 ID (默认: card-tech-dark)

可用主题:
  card-tech-dark   卡片科技暗色 (默认) - 适合技术文章、AI 内容
  card-neon-light  卡片霓虹浅色 - 适合教程、指南

Environment Variables:
  WECHAT_APP_ID     微信公众号 AppID
  WECHAT_APP_SECRET 微信公众号 AppSecret

Examples:
  $0 article.md
  $0 article.md card-tech-dark
  $0 article.md card-neon-light

  # 或指定环境变量
  WECHAT_APP_ID=wx123 WECHAT_APP_SECRET=secret $0 article.md
EOF
}

# 主函数
main() {
    # 检查参数
    if [ $# -eq 0 ] || [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
        show_help
        exit 0
    fi

    local markdown_file="$1"
    local theme_id="${2:-$DEFAULT_THEME}"

    # 执行检查
    check_wenyan
    check_env
    check_file "$markdown_file"

    local theme_file=$(check_theme "$theme_id")

    # 发布文章
    publish_article "$markdown_file" "$theme_id" "$theme_file"
}

# 运行
main "$@"
