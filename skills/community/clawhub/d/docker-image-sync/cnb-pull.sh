#!/bin/bash
# Docker官网镜像拉取能力
#
# 安全特性：
#   ✅ .env 加载：无 shell source，使用 IFS 逐行解析，避免注入
#   ✅ workflow 内嵌：不在制品内的是用户自建私有仓库
#   ✅ 默认私有仓库：不在制品内的是用户自建私有仓库，镜像名不暴露
#
# 用法:
#   cnb-pull.sh <镜像名>[:标签]       # 普通拉取
#   cnb-pull.sh --check              # 检测安装状态
#   cnb-pull.sh --setup              # 创建私有仓库、设置 Secrets 并测试
set -u   # 未定义变量时报错（安全），去掉 -e（会让 &>/dev/null 的命令静默失败时直接退出）

# ─── 参数解析 ────────────────────────────────────────────
ACTION="pull"
if [[ "${1:-}" == "--check" ]]; then
    ACTION="check"
elif [[ "${1:-}" == "--setup" ]]; then
    ACTION="setup"
elif [[ -z "${1:-}" ]]; then
    echo "用法: cnb-pull.sh <镜像名>[:标签]"
    echo "       cnb-pull.sh --check    # 检测安装状态"
    echo "       cnb-pull.sh --setup   # 创建私有仓库、设置 Secrets 并测试"
    exit 1
fi

# ─── 加载环境变量（安全解析，无 shell source）────────────
# 解析 .env 文件，仅提取技能需要的变量，避免注入风险
load_env() {
    local env_file="$HOME/.openclaw/.env"
    if [[ ! -f "$env_file" ]]; then
        return 0  # 文件不存在，继续用默认值
    fi

    # 读取文件内容，防止 shell 注入
    while IFS= read -r line || [[ -n "$line" ]]; do
        # 跳过注释行和空行
        [[ "$line" =~ ^# ]] && continue
        [[ -z "${line// }" ]] && continue

        # 仅匹配我们需要的变量前缀（防止注入）
        if [[ "$line" =~ ^[A-Za-z_][A-Za-z0-9_]*= ]]; then
            local key="${line%%=*}"
            case "$key" in
                CNB_TOKEN|CNB_REGISTRY|CNB_REPO_SLUG|CNB_GITHUB_REPO|GITHUB_TOKEN)
                    # 去除首尾引号和多余空白（安全的赋值方式）
                    local val="${line#*=}"
                    val="${val//\"/}"
                    val="${val//\'/}"
                    val="${val#"${val%%[![:space:]]*}"}"
                    val="${val%"${val##*[![:space:]]}"}"
                    export "$key"="$val"
                    ;;
            esac
        fi
    done < "$env_file"
}
load_env

CNB_TOKEN="${CNB_TOKEN:-}"
CNB_REGISTRY="${CNB_REGISTRY:-docker.cnb.cool}"
CNB_REPO_SLUG="${CNB_REPO_SLUG:-}"
CNB_GITHUB_REPO="${CNB_GITHUB_REPO:-}"
GIT_REPO="${CNB_GITHUB_REPO}"
IMAGES_FILE="images.txt"
CNB_IMAGE_NAME=""

# 工作目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ─── 彩色输出 ────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()    { echo -e "${GREEN}ℹ️  $1${NC}"; }
warn()    { echo -e "${YELLOW}⚠️  $1${NC}"; }
error()   { echo -e "${RED}❌ $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }

# ─── 检查必要参数 ────────────────────────────────────────
check_params() {
    local missing=0
    [[ -z "$CNB_TOKEN" ]]          && { error "CNB_TOKEN 未设置"; missing=$((missing+1)); }
    [[ -z "$CNB_REPO_SLUG" ]]       && { error "CNB_REPO_SLUG 未设置"; missing=$((missing+1)); }
    [[ -z "$CNB_GITHUB_REPO" ]]     && { error "CNB_GITHUB_REPO 未设置"; missing=$((missing+1)); }
    [[ -z "$GITHUB_TOKEN" ]]        && { error "GITHUB_TOKEN 未设置"; missing=$((missing+1)); }
    [[ $missing -gt 0 ]] && exit 1
}

# ─── GitHub 登录检测 + 创建私有仓库 ──────────────────────
do_check() {
    info "检测 GitHub 登录状态..."
    if ! command -v gh &>/dev/null; then
        error "gh CLI 未安装，请先安装：brew install gh"
        exit 1
    fi

    if ! gh auth status 2>&1 | grep -q "Logged in to github.com"; then
        error "未检测到 GitHub 登录"
        echo ""
        echo "请选择以下方式之一解决："
        echo "  1. 运行 'gh auth login' 在终端登录（推荐）"
        echo "  2. 提供 GitHub Personal Access Token 给 openclaw，我会帮你配置 GITHUB_TOKEN"
        echo ""
        echo "获取 Token 路径：GitHub → Settings → Developer settings → Personal access tokens → Generate new token"
        echo "所需权限：repo (全部) + workflow"
        exit 1
    fi

    info "GitHub 已登录 ✓"

    local GH_USER=$(gh api user --jq '.login')
    local REPO_NAME="cnb-docker-sync"
    local REPO_FULL="${GH_USER}/${REPO_NAME}"

    if gh repo view "${REPO_FULL}" &>/dev/null; then
        info "私有仓库已存在：${REPO_FULL}"
        echo "   仓库可见性：$(gh repo view "${REPO_FULL}" --json visibility --jq '.visibility')"
    else
        info "将创建私有仓库：${REPO_FULL}"
        gh repo create "${REPO_NAME}" --private --clone=false 2>&1 | grep -v "^$"
        info "私有仓库创建完成"
    fi

    echo ""
    echo "✅ GitHub 检测完成"
    echo "   你的同步仓库：${REPO_FULL}（私有，不会暴露镜像名）"
    echo ""
    echo "下一步：请提供 CNB 参数（CNB_TOKEN、CNB_REGISTRY、CNB_REPO_SLUG）给 openclaw"
}

# ─── 创建私有仓库 + 设置 Secrets + 嵌入 workflow ────────
do_setup() {
    check_params

    local GH_USER REPO_NAME REPO_FULL REPO_SLUG_LOWER TEMP_DIR

    GH_USER=$(gh api user --jq '.login' 2>&1)
    if [[ -z "$GH_USER" ]]; then
        error "无法获取 GitHub 用户名，请检查 GITHUB_TOKEN 权限"
        exit 1
    fi

    REPO_NAME="cnb-docker-sync"
    REPO_FULL="${GH_USER}/${REPO_NAME}"
    REPO_SLUG_LOWER=$(echo "$CNB_REPO_SLUG" | tr '[:upper:]' '[:lower:]')

    # 创建私有仓库（如不存在）
    if ! gh repo view "${REPO_FULL}" &>/dev/null; then
        info "创建私有仓库 ${REPO_FULL}..."
        gh repo create "${REPO_NAME}" --private --clone=false 2>&1 | grep -v "^$"
    fi

    info "设置 GitHub Repository Secrets..."

    # 设置 CNB 相关 secrets
    gh secret set CNB_REGISTRY --repo "${REPO_FULL}" --body "${CNB_REGISTRY}" \
        || { error "设置 CNB_REGISTRY 失败"; exit 1; }
    gh secret set CNB_REPO_SLUG_LOWERCASE --repo "${REPO_FULL}" --body "${REPO_SLUG_LOWER}" \
        || { error "设置 CNB_REPO_SLUG_LOWERCASE 失败"; exit 1; }
    gh secret set CNB_TOKEN --repo "${REPO_FULL}" --body "${CNB_TOKEN}" \
        || { error "设置 CNB_TOKEN 失败"; exit 1; }

    success "所有 Secrets 设置完成！"
    echo ""

    # 将内嵌 workflow 推送至用户私有仓库
    local WORKFLOW_DIR="${SCRIPT_DIR}/workflow"
    if [[ -d "$WORKFLOW_DIR" ]]; then
        info "推送内嵌 workflow 到 ${REPO_FULL}..."
        TEMP_DIR=$(mktemp -d)
        git clone --depth 1 "https://x-access-token:${GITHUB_TOKEN}@github.com/${REPO_FULL}.git" "$TEMP_DIR" 2>/dev/null

        mkdir -p "$TEMP_DIR/.github/workflows"
        cp "$WORKFLOW_DIR"/docker-image-sync.yml "$TEMP_DIR/.github/workflows/docker-image-sync.yml"

        cd "$TEMP_DIR"
        git config user.email "automation@openclaw"
        git config user.name "OpenClaw CNB Sync"
        git add .
        git commit -m "feat: add CNB Docker sync workflow"
        git push origin main 2>/dev/null

        rm -rf "$TEMP_DIR"
        success "内嵌 workflow 已推送至私有仓库"
    fi

    info "测试拉取镜像：postgres:latest"
    echo ""

    local IMAGE_REF="postgres:latest"
    parse_image "$IMAGE_REF"

    info "尝试直接从 CNB 拉取..."
    local CNB_IMAGE="${CNB_REGISTRY}/${CNB_REPO_SLUG}/${CNB_IMAGE_NAME}:${REMOTE_TAG}"

    echo "$CNB_TOKEN" | docker login "$CNB_REGISTRY" -u cnb --password-stdin &>/dev/null

    if docker pull "$CNB_IMAGE" 2>/dev/null; then
        echo ""
        success "🎉 技能测试通过！镜像 postgres:latest 已拉取到本地"
        echo "   本地镜像: $CNB_IMAGE"
        echo ""
        echo "✅ CNB 镜像同步技能已准备完毕，可以正常使用！"
    else
        echo ""
        warn "CNB 上未找到镜像，尝试代理中转模式（需要 1-3 分钟）..."
        echo ""
        proxy_sync_and_pull
    fi
}

# ─── 解析镜像参数 ────────────────────────────────────────
parse_image() {
    local IMAGE_REF="${1:-}"
    IFS=':' read -r REMOTE_IMAGE REMOTE_TAG <<< "$IMAGE_REF"
    REMOTE_TAG="${REMOTE_TAG:-latest}"
    CNB_IMAGE_NAME="${REMOTE_IMAGE//\//-}"
}

# ─── 直接从 CNB 拉取 ─────────────────────────────────────
pull_direct() {
    info "直接从 CNB 拉取..."
    local CNB_IMAGE="${CNB_REGISTRY}/${CNB_REPO_SLUG}/${CNB_IMAGE_NAME}:${REMOTE_TAG}"
    echo "$CNB_TOKEN" | docker login "$CNB_REGISTRY" -u cnb --password-stdin 2>/dev/null
    if docker pull "$CNB_IMAGE" 2>/dev/null; then
        success "镜像 $IMAGE_REF 已从 CNB 拉取到本地"
        echo "   本地镜像: $CNB_IMAGE"
        return 0
    fi
    return 1
}

try_direct_pull() {
    info "尝试直接从 CNB 拉取..."
    if pull_direct; then
        return 0
    fi
    warn "CNB 上未找到该镜像，尝试代理中转模式..."
    return 1
}

# ─── 代理中转模式 ────────────────────────────────────────
proxy_sync_and_pull() {
    info "代理中转模式"
    info "目标镜像: $REMOTE_IMAGE:$REMOTE_TAG"

    if ! command -v gh &>/dev/null; then
        error "gh CLI 未安装"
        exit 1
    fi

    local GH_USER REPO_NAME REPO_FULL TEMP_DIR

    GH_USER=$(gh api user --jq '.login' 2>&1)
    REPO_NAME="cnb-docker-sync"
    REPO_FULL="${GH_USER}/${REPO_NAME}"
    local GIT_TOKEN="${GITHUB_TOKEN}"

    TEMP_DIR=$(mktemp -d)

    info "克隆仓库（私有仓库）..."
    git clone --depth 1 --branch main "https://x-access-token:${GIT_TOKEN}@github.com/${REPO_FULL}.git" "$TEMP_DIR" 2>/dev/null

    echo "${REMOTE_IMAGE}:${REMOTE_TAG}" > "$TEMP_DIR/$IMAGES_FILE"
    info "更新 images.txt: ${REMOTE_IMAGE}:${REMOTE_TAG}"

    cd "$TEMP_DIR"
    git config user.email "automation@openclaw"
    git config user.name "OpenClaw CNB Sync"
    git add "$IMAGES_FILE"
    git commit -m "代理同步: ${REMOTE_IMAGE}:${REMOTE_TAG}"
    git push origin main 2>/dev/null

    info "已推送 images.txt，触发 GitHub Actions 同步到 CNB"
    info "等待 Actions 完成（约 1-3 分钟）..."

    local WAIT_COUNT=0
    local MAX_WAIT=180
    while [[ $WAIT_COUNT -lt $MAX_WAIT ]]; do
        sleep 10
        WAIT_COUNT=$((WAIT_COUNT + 10))

        local RUN_STATUS=$(gh run list --repo "$REPO_FULL" --limit 1 --json status,conclusion --jq '.[0] | "\(.status) \(.conclusion)"' 2>/dev/null)

        if echo "$RUN_STATUS" | grep -q "completed success"; then
            info "Actions 执行成功！"
            break
        elif echo "$RUN_STATUS" | grep -q "completed failure"; then
            error "Actions 执行失败，请检查 GitHub Actions 日志"
            rm -rf "$TEMP_DIR"
            exit 1
        fi

        info "Actions 还在运行... (已等待 ${WAIT_COUNT}s)"
    done

    if [[ $WAIT_COUNT -ge $MAX_WAIT ]]; then
        error "等待超时（${MAX_WAIT}s），请手动检查 Actions 状态"
        rm -rf "$TEMP_DIR"
        exit 1
    fi

    rm -rf "$TEMP_DIR"

    sleep 5
    info "从 CNB 拉取镜像..."
    local CNB_IMAGE="${CNB_REGISTRY}/${CNB_REPO_SLUG}/${CNB_IMAGE_NAME}:${REMOTE_TAG}"

    echo "$CNB_TOKEN" | docker login "$CNB_REGISTRY" -u cnb --password-stdin 2>/dev/null

    if docker pull "$CNB_IMAGE"; then
        success "镜像 $IMAGE_REF 已从 CNB 拉取到本地"
        echo "   本地镜像: $CNB_IMAGE"
    else
        error "拉取失败，镜像可能需要更多时间同步到 CNB"
        error "请稍后手动执行: docker pull $CNB_IMAGE"
        exit 1
    fi
}

# ─── 普通拉取 ────────────────────────────────────────────
do_pull() {
    check_params
    parse_image "$1"

    if try_direct_pull; then
        exit 0
    fi

    proxy_sync_and_pull
}

# ─── 入口 ────────────────────────────────────────────────
case "$ACTION" in
    check)  do_check ;;
    setup)  do_setup ;;
    pull)   do_pull "$1" ;;
esac