#!/usr/bin/env bash
# wechat-publisher: 使用 curl 直接调用微信 API 发布 Markdown 到草稿箱
# 此脚本不依赖 wenyan-cli，兼容所有 Node.js 版本
# Usage: ./publish-curl.sh <markdown-file>

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 微信 API 端点
TOKEN_URL="https://api.weixin.qq.com/cgi-bin/token"
UPLOAD_URL="https://api.weixin.qq.com/cgi-bin/material/add_material"
DRAFT_URL="https://api.weixin.qq.com/cgi-bin/draft/add"

# 临时目录
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

# 日志函数
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# 显示帮助
show_help() {
    cat << EOF
Usage: $0 <markdown-file>

使用 curl 直接调用微信 API 发布 Markdown 文章到草稿箱。
不依赖 wenyan-cli，兼容所有 Node.js 版本。

Arguments:
  markdown-file    要发布的 Markdown 文件路径

Environment Variables:
  WECHAT_APP_ID     微信公众号 AppID
  WECHAT_APP_SECRET 微信公众号 AppSecret

Example:
  $0 article.md

  WECHAT_APP_ID=wx123 WECHAT_APP_SECRET=secret $0 article.md
EOF
}

# 检查环境变量
check_env() {
    if [ -z "$WECHAT_APP_ID" ] || [ -z "$WECHAT_APP_SECRET" ]; then
        # 尝试从 TOOLS.md 读取
        local tools_md="$HOME/.openclaw/workspace/TOOLS.md"
        if [ -f "$tools_md" ]; then
            log_info "从 TOOLS.md 读取凭证..."
            export WECHAT_APP_ID=$(grep "export WECHAT_APP_ID=" "$tools_md" 2>/dev/null | head -1 | sed 's/.*export WECHAT_APP_ID=//' | tr -d ' "' || echo "")
            export WECHAT_APP_SECRET=$(grep "export WECHAT_APP_SECRET=" "$tools_md" 2>/dev/null | head -1 | sed 's/.*export WECHAT_APP_SECRET=//' | tr -d ' "' || echo "")
        fi
    fi

    if [ -z "$WECHAT_APP_ID" ] || [ -z "$WECHAT_APP_SECRET" ]; then
        log_error "环境变量未设置！"
        echo ""
        echo "请设置以下环境变量："
        echo "  export WECHAT_APP_ID=your_app_id"
        echo "  export WECHAT_APP_SECRET=your_app_secret"
        echo ""
        echo "或在 ~/.zshrc / ~/.bashrc 中添加上述配置"
        exit 1
    fi
}

# 检查文件存在
check_file() {
    local file="$1"
    if [ ! -f "$file" ]; then
        log_error "文件不存在: $file"
        exit 1
    fi
}

# 获取 access_token
get_access_token() {
    log_info "获取 access_token..."
    local response=$(curl -s "${TOKEN_URL}?grant_type=client_credential&appid=${WECHAT_APP_ID}&secret=${WECHAT_APP_SECRET}")
    local access_token=$(echo "$response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    local errcode=$(echo "$response" | grep -o '"errcode":[0-9]*' | cut -d':' -f2)

    if [ -n "$errcode" ] && [ "$errcode" != "0" ]; then
        local errmsg=$(echo "$response" | grep -o '"errmsg":"[^"]*"' | cut -d'"' -f4)
        log_error "获取 access_token 失败: $errmsg (errcode: $errcode)"
        exit 1
    fi

    if [ -z "$access_token" ]; then
        log_error "获取 access_token 失败"
        echo "响应: $response"
        exit 1
    fi

    log_success "access_token 获取成功"
    echo "$access_token"
}

# 上传图片
upload_image() {
    local image_path="$1"
    local access_token="$2"

    log_info "上传图片: $(basename "$image_path")"

    local response=$(curl -s -X POST \
        "${UPLOAD_URL}?access_token=${access_token}&type=image" \
        -F "media=@${image_path}")

    local errcode=$(echo "$response" | grep -o '"errcode":[0-9]*' | cut -d':' -f2)

    if [ -n "$errcode" ] && [ "$errcode" != "0" ]; then
        local errmsg=$(echo "$response" | grep -o '"errmsg":"[^"]*"' | cut -d'"' -f4)
        log_error "上传图片失败: $errmsg"
        return 1
    fi

    local media_id=$(echo "$response" | grep -o '"media_id":"[^"]*"' | cut -d'"' -f4)
    log_success "图片上传成功 (media_id: ${media_id:0:20}...)"
    echo "$media_id"
}

# 解析 Markdown frontmatter
parse_frontmatter() {
    local file="$1"
    local output="$2"

    # 提取 frontmatter 和正文
    awk '
    BEGIN { in_frontmatter=0; frontmatter=""; content="" }
    /^---$/ {
        if (in_frontmatter == 0) {
            in_frontmatter=1
            next
        } else {
            in_frontmatter=2
            next
        }
    }
    {
        if (in_frontmatter == 1) {
            frontmatter = frontmatter $0 "\n"
        } else {
            content = content $0 "\n"
        }
    }
    END {
        print frontmatter > "'"$3"'"
        print content > "'"$4"'"
    }
    ' "$file"
}

# 从 frontmatter 提取字段
extract_field() {
    local frontmatter="$1"
    local field="$2"
    echo "$frontmatter" | grep "^${field}:" | sed "s/^${field}: *//" | tr -d '"'
}

# 检查命令是否存在
check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "缺少命令: $1"
        log_info "请安装: $2"
        exit 1
    fi
}

# 主函数
main() {
    # 检查参数
    if [ $# -eq 0 ] || [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
        show_help
        exit 0
    fi

    local markdown_file="$1"

    # 检查依赖
    check_command "curl" "请安装 curl"
    check_command "jq" "brew install jq (JSON 处理，可选)"

    # 检查环境
    check_env
    check_file "$markdown_file"

    # 解析 frontmatter
    local fm_file="$TMP_DIR/frontmatter.txt"
    local content_file="$TMP_DIR/content.txt"

    parse_frontmatter "$markdown_file" "$fm_file" "$content_file"

    local frontmatter=$(cat "$fm_file")

    # 提取元数据
    local title=$(extract_field "$frontmatter" "title")
    local cover=$(extract_field "$frontmatter" "cover")
    local author=$(extract_field "$frontmatter" "author")
    local source_url=$(extract_field "$frontmatter" "source_url")

    # 验证必填字段
    if [ -z "$title" ]; then
        log_error "frontmatter 缺少 title 字段"
        echo "请在文件顶部添加:"
        echo "---"
        echo "title: 文章标题"
        echo "cover: 封面图片路径或 URL"
        echo "---"
        exit 1
    fi

    if [ -z "$cover" ]; then
        log_warn "未指定封面图，将使用第一张图片作为封面"
    fi

    log_info "文章信息:"
    echo "  标题: $title"
    echo "  作者: ${author:-未设置}"
    echo "  封面: ${cover:-未设置}"

    # 获取 access_token
    local access_token=$(get_access_token)

    # 上传封面图
    local thumb_media_id=""
    if [ -n "$cover" ]; then
        if [[ "$cover" == http* ]]; then
            log_warn "网络封面图暂时不支持，请使用本地图片"
            log_info "建议: 下载图片到本地或使用文章中的第一张图片"
        elif [ -f "$cover" ]; then
            thumb_media_id=$(upload_image "$cover" "$access_token")
        else
            # 尝试相对于 markdown 文件的路径
            local md_dir=$(dirname "$markdown_file")
            local cover_path="$md_dir/$cover"
            if [ -f "$cover_path" ]; then
                thumb_media_id=$(upload_image "$cover_path" "$access_token")
            else
                log_warn "封面图不存在: $cover"
            fi
        fi
    fi

    # 简单处理内容（实际项目中应使用 wenyan-cli 渲染）
    log_info "准备发布内容..."
    local content=$(cat "$content_file")

    # 构建 JSON payload
    local json_payload="$TMP_DIR/payload.json"
    cat > "$json_payload" << EOF
{
  "articles": [
    {
      "title": "$title",
      "author": "${author:-}",
      "content": "$(echo "$content" | sed 's/"/\\"/g' | tr -d '\n')",
      "thumb_media_id": "$thumb_media_id",
      "content_source_url": "${source_url:-}"
    }
  ]
}
EOF

    # 发布草稿
    log_info "发布到草稿箱..."
    local response=$(curl -s -X POST \
        "${DRAFT_URL}?access_token=${access_token}" \
        -H "Content-Type: application/json" \
        -d @"$json_payload")

    # 检查结果
    local errcode=$(echo "$response" | grep -o '"errcode":[0-9]*' | cut -d':' -f2)

    if [ -z "$errcode" ] || [ "$errcode" == "0" ]; then
        local media_id=$(echo "$response" | grep -o '"media_id":"[^"]*"' | cut -d'"' -f4)
        log_success "发布成功！"
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
        echo -e "${YELLOW}提示: 此脚本只做简单格式转换${NC}"
        echo -e "${YELLOW}如需完整排版支持，请使用 wenyan-cli${NC}"
    else
        local errmsg=$(echo "$response" | grep -o '"errmsg":"[^"]*"' | cut -d'"' -f4)
        log_error "发布失败: $errmsg (errcode: $errcode)"
        echo ""
        echo "常见错误码:"
        echo "  40001  - AppID 或 AppSecret 错误"
        echo "  40002  - 请求格式错误"
        echo "  40004  - 封面图片无效"
        echo "  40005  - media_id 无效"
        echo "  40006  - 文章数量超过限制"
        echo "  40007  - media_id 不存在"
        echo "  61007  - content 包含违规内容"
        echo "  85006  - 群发文章数量超过限制"
        exit 1
    fi
}

# 运行
main "$@"
