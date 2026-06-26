#!/bin/bash
# fly-install.sh - ClawHub 备用安装脚本
# 当 clawhub CLI 速率限制时，通过多种方式安装技能
# 支持：1) GitHub 搜索克隆 2) ClawHub zip 下载 3) 手动指导

set -e

SKILL_NAME="$1"
SKILLS_DIR="${2:-$HOME/.openclaw/workspace/skills}"
CLAWHUB_API="https://wry-manatee-359.convex.site/api/v1/download"
GITHUB_API="https://api.github.com/search/repositories"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
  echo -e "${BLUE}[STEP]${NC} $1"
}

# 显示用法
usage() {
  cat << EOF
Usage: $0 <skill-name> [skills-directory]

Arguments:
  skill-name          要安装的技能名称
  skills-directory    技能安装目录（默认: $HOME/.openclaw/workspace/skills）

Examples:
  $0 nano-pdf
  $0 skill-vetter /custom/skills/path
  $0 --help

Installation methods (tried in order):
  1. GitHub search and clone
  2. ClawHub zip download
  3. Manual instructions

EOF
}

# 检查参数
if [ -z "$SKILL_NAME" ] || [ "$SKILL_NAME" == "--help" ] || [ "$SKILL_NAME" == "-h" ]; then
  usage
  exit 0
fi

# 检查目录是否存在
if [ ! -d "$SKILLS_DIR" ]; then
  log_info "创建技能目录: $SKILLS_DIR"
  mkdir -p "$SKILLS_DIR"
fi

cd "$SKILLS_DIR"

# 检查是否已安装
check_installed() {
  if [ -d "$SKILL_NAME" ] && [ -f "$SKILL_NAME/SKILL.md" ]; then
    return 0
  fi
  return 1
}

if check_installed; then
  log_warn "技能 '$SKILL_NAME' 已安装"
  read -p "是否重新安装? (y/N): " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log_info "取消安装"
    exit 0
  fi
  log_info "备份旧版本..."
  mv "$SKILL_NAME" "${SKILL_NAME}-backup-$(date +%s)"
fi

log_info "开始安装技能: $SKILL_NAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 方法 1: GitHub 搜索克隆
try_github_clone() {
  log_step "方法 1: 尝试从 GitHub 搜索并克隆..."
  
  # 搜索 GitHub
  local search_query="${SKILL_NAME}+openclaw+skill"
  log_info "搜索 GitHub: $search_query"
  
  local repos
  repos=$(curl -s "${GITHUB_API}?q=${search_query}&per_page=3" 2>/dev/null | \
    jq -r '.items[]? | select(.name | ascii_downcase == "'"$(echo "$SKILL_NAME" | tr '[:upper:]' '[:lower:]')"'") | \
    "\(.full_name)|\(.clone_url)"' 2>/dev/null)
  
  if [ -z "$repos" ]; then
    # 尝试更宽泛的搜索
    repos=$(curl -s "${GITHUB_API}?q=${SKILL_NAME}+openclaw" 2>/dev/null | \
      jq -r '.items[0]? | "\(.full_name)|\(.clone_url)"' 2>/dev/null)
  fi
  
  if [ -z "$repos" ] || [ "$repos" == "null|null" ]; then
    log_warn "GitHub 未找到匹配仓库"
    return 1
  fi
  
  # 解析结果
  local repo_full_name=$(echo "$repos" | head -1 | cut -d'|' -f1)
  local clone_url=$(echo "$repos" | head -1 | cut -d'|' -f2)
  
  if [ -z "$clone_url" ] || [ "$clone_url" == "null" ]; then
    log_warn "无法获取克隆地址"
    return 1
  fi
  
  log_info "找到仓库: $repo_full_name"
  log_info "克隆地址: $clone_url"
  
  # 执行克隆
  if git clone --depth 1 "$clone_url" "$SKILL_NAME" 2>&1 | tail -3; then
    if [ -f "$SKILL_NAME/SKILL.md" ]; then
      log_info "✅ GitHub 克隆成功!"
      return 0
    else
      log_warn "克隆成功但缺少 SKILL.md"
      rm -rf "$SKILL_NAME"
      return 1
    fi
  else
    log_error "GitHub 克隆失败"
    return 1
  fi
}

# 方法 2: ClawHub zip 下载
try_clawhub_zip() {
  log_step "方法 2: 尝试从 ClawHub 下载 zip..."
  
  local download_url="${CLAWHUB_API}?slug=${SKILL_NAME}"
  local zip_file="${SKILL_NAME}.zip"
  
  log_info "下载: $download_url"
  
  # 下载
  local download_success=false
  if command -v wget >/dev/null 2>&1; then
    if wget -q -O "$zip_file" "$download_url" 2>/dev/null; then
      download_success=true
    fi
  elif command -v curl >/dev/null 2>&1; then
    if curl -sL -o "$zip_file" "$download_url" 2>/dev/null; then
      download_success=true
    fi
  fi
  
  if [ "$download_success" != "true" ]; then
    log_warn "下载失败"
    return 1
  fi
  
  # 检查文件大小
  local file_size
  file_size=$(stat -f%z "$zip_file" 2>/dev/null || stat -c%s "$zip_file" 2>/dev/null || echo "0")
  
  if [ "$file_size" -lt 100 ]; then
    log_warn "下载文件太小，可能不存在该技能"
    rm -f "$zip_file"
    return 1
  fi
  
  log_info "下载完成: $file_size 字节"
  
  # 解压
  if unzip -q "$zip_file" -d "$SKILL_NAME" 2>/dev/null; then
    rm -f "$zip_file"
    if [ -f "$SKILL_NAME/SKILL.md" ]; then
      log_info "✅ Zip 安装成功!"
      return 0
    else
      log_warn "解压成功但缺少 SKILL.md"
      rm -rf "$SKILL_NAME"
      return 1
    fi
  else
    log_error "解压失败"
    rm -f "$zip_file"
    return 1
  fi
}

# 方法 3: 输出手动指导
show_manual_instructions() {
  log_step "方法 3: 手动安装指导"
  cat << EOF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 手动安装 '$SKILL_NAME' 的方法：

方法 A - GitHub 克隆：
  1. 访问 https://github.com/search?q=${SKILL_NAME}+openclaw
  2. 找到对应的仓库
  3. 执行: git clone --depth 1 <clone_url> ${SKILL_NAME}

方法 B - ClawHub zip：
  1. 访问 https://clawhub.ai/skills
  2. 搜索 '${SKILL_NAME}'
  3. 点击 "Download zip"
  4. 解压到: ${SKILLS_DIR}/${SKILL_NAME}/

方法 C - 官方 CLI（等速率限制解除）：
  npx clawhub install ${SKILL_NAME}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF
}

# 验证安装
verify_installation() {
  if check_installed; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_info "✅ 安装成功!"
    echo "📦 技能名称: $SKILL_NAME"
    echo "📁 安装位置: $SKILLS_DIR/$SKILL_NAME"
    echo ""
    echo "📄 文件列表:"
    ls -la "$SKILL_NAME/"
    echo ""
    echo "📝 技能信息:"
    head -10 "$SKILL_NAME/SKILL.md" 2>/dev/null | grep -E "^name:|^description:" || head -5 "$SKILL_NAME/SKILL.md"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    return 0
  else
    log_error "❌ 安装失败"
    return 1
  fi
}

# 主流程
main() {
  local success=false
  
  # 尝试方法 1: GitHub
  if try_github_clone; then
    success=true
  fi
  
  # 尝试方法 2: ClawHub zip
  if [ "$success" != "true" ] && try_clawhub_zip; then
    success=true
  fi
  
  # 方法 3: 手动指导
  if [ "$success" != "true" ]; then
    show_manual_instructions
    exit 1
  fi
  
  # 验证
  verify_installation
}

main
