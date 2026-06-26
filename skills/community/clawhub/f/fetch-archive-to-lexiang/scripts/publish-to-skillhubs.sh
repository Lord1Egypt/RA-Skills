#!/usr/bin/env bash
# publish-to-skillhubs.sh
# 一键将 fetch-archive-to-lexiang 发布到所有主要 SkillHub 平台
#
# 用法：
#   bash scripts/publish-to-skillhubs.sh           # 发布到所有平台
#   bash scripts/publish-to-skillhubs.sh --dry-run  # 预览模式（不实际发布）
#   bash scripts/publish-to-skillhubs.sh --platform agentskillhub  # 仅发布到特定平台
#
# 支持平台：
#   1. agentskillhub  → agentskillhub.dev（REST API，无需额外登录）
#   2. skillshubai    → skills-hub.ai（需 npx @skills-hub-ai/cli login）
#   3. clawhub        → clawhub.ai（需 clawhub login）
#   4. agentskillshub → agent-skills-hub GitHub repo（需 gh auth login）

set -euo pipefail

# ── 配置 ──────────────────────────────────────────────────────────────────
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GITHUB_REPO="ajaxhe/fetch-archive-to-lexiang"
GITHUB_REPO_URL="https://github.com/${GITHUB_REPO}"
SKILL_NAME="fetch-archive-to-lexiang"
SKILL_VERSION="2.1.0"
DRY_RUN=false
TARGET_PLATFORM="all"

# ── 参数解析 ──────────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --platform) TARGET_PLATFORM="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# ── 工具函数 ──────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'; BOLD='\033[1m'

log_info()    { echo -e "${GREEN}✅${NC} $*"; }
log_warn()    { echo -e "${YELLOW}⚠️ ${NC} $*"; }
log_error()   { echo -e "${RED}❌${NC} $*"; }
log_section() { echo -e "\n${BOLD}── $* ──────────────────────────${NC}"; }

run_or_dry() {
  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}[DRY RUN]${NC} $*"
  else
    eval "$@"
  fi
}

# ── 前置检查 ──────────────────────────────────────────────────────────────
log_section "前置检查"
cd "$SKILL_DIR"
echo "Skill 目录: $SKILL_DIR"
echo "GitHub 仓库: $GITHUB_REPO_URL"
echo "Dry Run: $DRY_RUN"

if [ ! -f "SKILL.md" ]; then
  log_error "SKILL.md 不存在，请在 skill 根目录运行此脚本"
  exit 1
fi

# ── Step 0: 确保最新代码已推送到 GitHub ──────────────────────────────────
log_section "Step 0: 同步到 GitHub"

GIT_STATUS=$(git status --porcelain)
if [ -n "$GIT_STATUS" ]; then
  log_warn "有未提交的变更，先提交："
  git status --short
  run_or_dry 'git add -A && git commit -m "chore: prepare for SkillHub publishing" && git push'
else
  log_info "工作区干净，检查是否需要 push..."
  BEHIND=$(git rev-list HEAD..origin/main --count 2>/dev/null || echo "0")
  AHEAD=$(git rev-list origin/main..HEAD --count 2>/dev/null || echo "0")
  if [ "$AHEAD" -gt 0 ]; then
    run_or_dry 'git push'
    log_info "已推送 ${AHEAD} 个提交到 GitHub"
  else
    log_info "已与 GitHub 同步"
  fi
fi

# ══════════════════════════════════════════════════════════════════════════
# Platform 1: agentskillhub.dev（REST API，无需账号认证）
# ══════════════════════════════════════════════════════════════════════════
publish_agentskillhub() {
  log_section "Platform 1: agentskillhub.dev"

  echo "📡 分析仓库..."
  ANALYZE_RESPONSE=$(curl -s -o /tmp/analyze_body.json -w "%{http_code}" -X POST \
    "https://agentskillhub.dev/api/v1/repos/analyze" \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"${GITHUB_REPO_URL}\"}")

  HTTP_CODE="$ANALYZE_RESPONSE"
  BODY=$(cat /tmp/analyze_body.json 2>/dev/null || echo "{}")

  echo "HTTP $HTTP_CODE: $BODY"

  if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
    if [ "$DRY_RUN" = false ]; then
      echo "📥 触发 import..."
      curl -s -X POST \
        "https://agentskillhub.dev/api/v1/repos/import" \
        -H "Content-Type: application/json" \
        -d "{\"url\": \"${GITHUB_REPO_URL}\", \"skills\": [\"${SKILL_NAME}\"]}"
      log_info "agentskillhub.dev 导入已触发"
    fi
  elif [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "403" ]; then
    log_warn "agentskillhub.dev 需要认证"
    echo "  → 访问 https://agentskillhub.dev 注册账号"
    echo "  → 在 web 界面使用「Add Skills」→ 粘贴仓库 URL: ${GITHUB_REPO_URL}"
  else
    log_warn "agentskillhub.dev 返回 HTTP $HTTP_CODE，可能需要在 web 界面手动导入"
    echo "  → 访问 https://agentskillhub.dev"
    echo "  → 使用「Add Skills」粘贴: ${GITHUB_REPO_URL}"
  fi
}

# ══════════════════════════════════════════════════════════════════════════
# Platform 2: skills-hub.ai（需要登录）
# ══════════════════════════════════════════════════════════════════════════
publish_skillshubai() {
  log_section "Platform 2: skills-hub.ai"

  if ! command -v npx &>/dev/null; then
    log_warn "npx 未安装，跳过 skills-hub.ai"
    return
  fi

  # 检查是否已登录
  if npx --yes @skills-hub-ai/cli whoami &>/dev/null 2>&1; then
    log_info "已登录 skills-hub.ai"
  else
    log_warn "未登录 skills-hub.ai，正在打开登录流程..."
    echo "  登录后请重新运行此脚本，或手动执行："
    echo "  cd ${SKILL_DIR} && npx @skills-hub-ai/cli publish . --github-repo ${GITHUB_REPO_URL}"
    npx --yes @skills-hub-ai/cli login
    echo ""
    read -r -p "登录完成了吗？(y/N) " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
      log_warn "跳过 skills-hub.ai"
      return
    fi
  fi

  if [ "$DRY_RUN" = false ]; then
    run_or_dry "npx @skills-hub-ai/cli publish . \
      --github-repo '${GITHUB_REPO_URL}' \
      --tags 'fetch,archive,youtube,podcast,pdf,chinese,lexiang,paywall,substack,medium'"
    log_info "skills-hub.ai 发布成功"
  else
    echo "[DRY RUN] npx @skills-hub-ai/cli publish . --github-repo ${GITHUB_REPO_URL}"
  fi
}

# ══════════════════════════════════════════════════════════════════════════
# Platform 3: clawhub.ai（需要登录）
# ══════════════════════════════════════════════════════════════════════════
publish_clawhub() {
  log_section "Platform 3: clawhub.ai"

  if ! command -v clawhub &>/dev/null; then
    echo "安装 clawhub CLI..."
    run_or_dry "npm install -g @clawhub/cli"
  fi

  # 检查是否已登录
  CLAWHUB_USER=$(clawhub whoami 2>/dev/null | grep -v '^-' | tr -d '[:space:]' || echo "")
  if [ -n "$CLAWHUB_USER" ]; then
    log_info "已登录 clawhub.ai（用户：${CLAWHUB_USER}）"
  else
    log_warn "未登录 clawhub.ai，正在打开登录流程..."
    echo "  → 需要 GitHub OAuth 授权（会打开浏览器）"
    run_or_dry "clawhub login"
    echo ""
    read -r -p "登录完成了吗？(y/N) " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
      log_warn "跳过 clawhub.ai"
      return
    fi
  fi

  # 发布：clawhub 需要 --workdir 指向 skills 的父目录
  SKILLS_PARENT="$(dirname "${SKILL_DIR}")"

  if [ "$DRY_RUN" = false ]; then
    run_or_dry "clawhub --workdir '${SKILLS_PARENT}' publish '${SKILL_NAME}' \
      --slug '${SKILL_NAME}' \
      --name 'Fetch & Archive to Lexiang' \
      --version '${SKILL_VERSION}' \
      --changelog 'See README.md for full changelog' \
      --tags 'latest,fetch,archive,youtube,podcast,pdf,chinese,lexiang' \
      --clawscan-note 'Uses Chrome CDP for authenticated scraping, Lexiang MCP APIs, yt-dlp/Whisper for transcription.'"
    log_info "clawhub.ai 发布成功 → https://clawhub.ai/skills/${SKILL_NAME}"
  else
    echo "[DRY RUN] clawhub --workdir ${SKILLS_PARENT} publish ${SKILL_NAME} --version ${SKILL_VERSION}"
  fi
}

# ══════════════════════════════════════════════════════════════════════════
# Platform 4: agent-skills-hub GitHub（PR 贡献）
# ══════════════════════════════════════════════════════════════════════════
publish_agentskillshub_pr() {
  log_section "Platform 4: agent-skills-hub (GitHub PR)"

  if ! command -v gh &>/dev/null; then
    log_warn "GitHub CLI (gh) 未安装"
    echo "  → brew install gh && gh auth login"
    echo "  → 然后重新运行：bash scripts/publish-to-skillhubs.sh --platform agentskillshub"
    return
  fi

  if ! gh auth status &>/dev/null 2>&1; then
    log_warn "gh 未登录，运行：gh auth login"
    return
  fi

  FORK_DIR="/tmp/agent-skills-hub-fork-$$"
  TARGET_SKILL_DIR="${FORK_DIR}/skills/${SKILL_NAME}"

  echo "📋 Fork & 克隆 agent-skills-hub..."
  run_or_dry "gh repo fork agent-skills-hub/agent-skills-hub --clone --fork-name agent-skills-hub-fork --remote=true || true"
  run_or_dry "git clone https://github.com/\$(gh api user --jq .login)/agent-skills-hub ${FORK_DIR} 2>/dev/null || git clone https://github.com/agent-skills-hub/agent-skills-hub ${FORK_DIR}"

  if [ "$DRY_RUN" = false ]; then
    mkdir -p "$TARGET_SKILL_DIR"
    cp -r "${SKILL_DIR}/SKILL.md" "$TARGET_SKILL_DIR/"
    cp -r "${SKILL_DIR}/README.md" "$TARGET_SKILL_DIR/"
    cp -r "${SKILL_DIR}/config.json.example" "$TARGET_SKILL_DIR/"
    cp -r "${SKILL_DIR}/scripts" "$TARGET_SKILL_DIR/"
    cp -r "${SKILL_DIR}/references" "$TARGET_SKILL_DIR/"
    [ -f "${SKILL_DIR}/.gitignore" ] && cp "${SKILL_DIR}/.gitignore" "$TARGET_SKILL_DIR/"

    cd "$FORK_DIR"
    git config user.email "$(git config --global user.email || echo 'agent@github.com')"
    git config user.name "$(git config --global user.name || echo 'GitHub Actions')"
    git checkout -b "add-${SKILL_NAME}"
    git add "skills/${SKILL_NAME}/"
    git commit -m "feat: add ${SKILL_NAME} skill

    Universal web article fetcher and archiver for AI agents.

    Features:
    - Bypass paywalls (Substack, Medium, 知识星球)
    - YouTube video download + Whisper transcription
    - Podcast audio download + transcription
    - PDF extraction with bilingual translation
    - Archive to Lexiang knowledge base

    Source: ${GITHUB_REPO_URL}"

    git push origin "add-${SKILL_NAME}"

    gh pr create \
      --repo "agent-skills-hub/agent-skills-hub" \
      --title "feat: add ${SKILL_NAME}" \
      --body "## ${SKILL_NAME}

    Universal web article fetcher and archiver.

    **Features:**
    - Bypass paywalls (Substack, Medium, 知识星球)
    - YouTube video download + Whisper transcription  
    - Podcast audio + transcription (小宇宙FM etc.)
    - PDF extraction + bilingual translation
    - Archive to [Lexiang](https://lexiangla.com) knowledge base

    **Source:** ${GITHUB_REPO_URL}

    ---
    *Automated PR via publish-to-skillhubs.sh*"

    log_info "PR 已创建 → https://github.com/agent-skills-hub/agent-skills-hub/pulls"
    cd "$SKILL_DIR"
    rm -rf "$FORK_DIR"
  fi
}

# ══════════════════════════════════════════════════════════════════════════
# 主流程：执行
# ══════════════════════════════════════════════════════════════════════════
log_section "开始发布 → ${TARGET_PLATFORM}"
[ "$DRY_RUN" = true ] && echo -e "${YELLOW}🔍 DRY RUN 模式：不会实际发布${NC}\n"

case "$TARGET_PLATFORM" in
  all)
    publish_agentskillhub
    publish_skillshubai
    publish_clawhub
    publish_agentskillshub_pr
    ;;
  agentskillhub)   publish_agentskillhub ;;
  skillshubai)     publish_skillshubai ;;
  clawhub)         publish_clawhub ;;
  agentskillshub)  publish_agentskillshub_pr ;;
  *)
    log_error "未知平台: $TARGET_PLATFORM"
    echo "支持: all | agentskillhub | skillshubai | clawhub | agentskillshub"
    exit 1
    ;;
esac

# ── 总结 ──────────────────────────────────────────────────────────────────
log_section "发布完成 🎉"
echo ""
echo "📍 平台链接（发布后生效）："
echo "  agentskillhub.dev → https://agentskillhub.dev/skills/${GITHUB_REPO}"
echo "  skills-hub.ai     → https://skills-hub.ai/browse?q=fetch-archive-to-lexiang"
echo "  clawhub.ai        → https://clawhub.ai/skills/${SKILL_NAME}"
echo "  agent-skills-hub  → https://github.com/agent-skills-hub/agent-skills-hub/pulls"
echo ""
echo "💡 后续 CI 自动发布："
echo "  - 已配置 GitHub Actions（.github/workflows/publish-to-skillhubs.yml）"
echo "  - 每次推送 SKILL.md 或脚本更新，自动触发所有平台更新"
echo "  - 需要在 GitHub 仓库 Settings → Secrets 中添加："
echo "      SKILLSHUBAI_TOKEN  → npx @skills-hub-ai/cli login 后获取"
echo "      CLAWHUB_TOKEN      → clawhub login 后获取"
