#!/usr/bin/env bash
# setup-tokens.sh
# 一次性：登录各 SkillHub 平台，提取 token，写入 GitHub Secrets
#
# 用法：
#   bash scripts/setup-tokens.sh
#
# 完成后，GitHub Actions 会在每次推送 SKILL.md 时自动更新所有平台。
#
# 需要提前安装：
#   brew install gh          # GitHub CLI
#   npm install -g @clawhub/cli skhub  # 平台 CLI 工具

set -euo pipefail

REPO="ajaxhe/fetch-archive-to-lexiang"
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BOLD='\033[1m'; NC='\033[0m'
log_info()    { echo -e "${GREEN}✅${NC} $*"; }
log_warn()    { echo -e "${YELLOW}⚠️ ${NC} $*"; }
log_section() { echo -e "\n${BOLD}── $* ──────────────────────────────${NC}"; }

# ──────────────────────────────────────────────
# 前置检查
# ──────────────────────────────────────────────
log_section "前置检查"

if ! command -v gh &>/dev/null; then
  log_warn "GitHub CLI 未安装：brew install gh && gh auth login"
  exit 1
fi

if ! gh auth status &>/dev/null 2>&1; then
  echo "请先登录 GitHub CLI："
  gh auth login
fi

log_info "GitHub CLI 已登录（$(gh api user --jq .login)）"

# ──────────────────────────────────────────────
# Token 1: clawhub.ai
# ──────────────────────────────────────────────
log_section "Token 1: clawhub.ai"

CLAWHUB_CONFIG="$HOME/Library/Application Support/clawhub/config.json"
if [ ! -f "$CLAWHUB_CONFIG" ]; then
  CLAWHUB_CONFIG="$HOME/.config/clawhub/config.json"
fi

if [ -f "$CLAWHUB_CONFIG" ]; then
  CLAWHUB_TOKEN=$(python3 -c "import json; d=json.load(open('$CLAWHUB_CONFIG')); print(d.get('token',''))" 2>/dev/null)
  if [ -n "$CLAWHUB_TOKEN" ]; then
    echo "$CLAWHUB_TOKEN" | gh secret set CLAWHUB_TOKEN --repo "$REPO"
    log_info "CLAWHUB_TOKEN 已写入 GitHub Secrets（${CLAWHUB_TOKEN:0:12}...）"
  else
    log_warn "clawhub token 为空，请先运行：clawhub login"
  fi
else
  log_warn "未找到 clawhub 配置文件，请运行：npm install -g @clawhub/cli && clawhub login"
fi

# ──────────────────────────────────────────────
# Token 2: agentskillhub.dev
# ──────────────────────────────────────────────
log_section "Token 2: agentskillhub.dev (skhub)"

SKHUB_AUTH="$HOME/.skhub/auth.json"

if [ ! -f "$SKHUB_AUTH" ]; then
  echo "需要登录 agentskillhub.dev（会打开浏览器）..."
  skhub login
  sleep 2
fi

if [ -f "$SKHUB_AUTH" ]; then
  AGENTSKILLHUB_TOKEN=$(python3 -c "
import json
data=json.load(open('$SKHUB_AUTH'))
# auth.json 结构: {version, credentials: {url: {token, tokenId, ...}}}
creds=data.get('credentials',{})
for url,cred in creds.items():
    if 'agentskillhub' in url:
        print(cred.get('token',''))
        break
else:
    # 取第一个
    for cred in creds.values():
        if cred.get('token'):
            print(cred['token'])
            break
" 2>/dev/null)

  if [ -n "$AGENTSKILLHUB_TOKEN" ]; then
    echo "$AGENTSKILLHUB_TOKEN" | gh secret set AGENTSKILLHUB_TOKEN --repo "$REPO"
    log_info "AGENTSKILLHUB_TOKEN 已写入 GitHub Secrets（${AGENTSKILLHUB_TOKEN:0:12}...）"
  else
    log_warn "从 auth.json 提取 token 失败，请手动登录：skhub login"
  fi
else
  log_warn "skhub 登录后仍未找到 auth.json"
fi

# ──────────────────────────────────────────────
# Token 3: skills-hub.ai
# ──────────────────────────────────────────────
log_section "Token 3: skills-hub.ai"

SKILLSHUB_CONFIG="$HOME/.skills-hub/config.json"

if [ ! -f "$SKILLSHUB_CONFIG" ]; then
  echo ""
  echo "skills-hub.ai 的 CLI 登录依赖有问题，请用以下方式获取 API Key："
  echo ""
  echo "  方式 A（推荐）："
  echo "    1. 访问 https://skills-hub.ai/settings/api-keys"
  echo "    2. 创建一个 API Key"
  echo "    3. 粘贴到下方："
  echo ""
  read -r -p "请粘贴 skills-hub.ai API Key（留空跳过）: " SKILLSHUBAI_INPUT
  if [ -n "$SKILLSHUBAI_INPUT" ]; then
    # 写入 config
    mkdir -p "$HOME/.skills-hub"
    echo "{\"apiUrl\": \"https://api.skills-hub.ai\", \"apiKey\": \"$SKILLSHUBAI_INPUT\"}" > "$SKILLSHUB_CONFIG"
    echo "$SKILLSHUBAI_INPUT" | gh secret set SKILLSHUBAI_TOKEN --repo "$REPO"
    log_info "SKILLSHUBAI_TOKEN 已写入 GitHub Secrets"
  else
    log_warn "已跳过 skills-hub.ai（可后续手动添加 SKILLSHUBAI_TOKEN secret）"
  fi
else
  SKILLSHUBAI_TOKEN=$(python3 -c "
import json
d=json.load(open('$SKILLSHUB_CONFIG'))
print(d.get('apiKey') or d.get('accessToken',''))
" 2>/dev/null)
  if [ -n "$SKILLSHUBAI_TOKEN" ]; then
    echo "$SKILLSHUBAI_TOKEN" | gh secret set SKILLSHUBAI_TOKEN --repo "$REPO"
    log_info "SKILLSHUBAI_TOKEN 已写入 GitHub Secrets（${SKILLSHUBAI_TOKEN:0:12}...）"
  else
    log_warn "~/.skills-hub/config.json 存在但 token 为空"
  fi
fi

# ──────────────────────────────────────────────
# 验证
# ──────────────────────────────────────────────
log_section "已配置的 GitHub Secrets"
gh secret list --repo "$REPO" 2>/dev/null | grep -E "CLAWHUB|AGENTSKILLHUB|SKILLSHUBAI" || echo "（无法列出 secrets）"

echo ""
log_info "Setup 完成！"
echo ""
echo "现在每次推送到 main，GitHub Actions 会自动更新所有平台。"
echo "可手动触发：gh workflow run 'Publish to SkillHub Platforms' --repo $REPO"
