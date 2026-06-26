#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${HOME}/.openclaw/workspace/skills"

mkdir -p "${TARGET_DIR}"

# ── 1. 安装 Agent Reach（网页读取依赖）──────────────────────────
echo "==> Checking Agent Reach ..."
if command -v agent-reach &>/dev/null; then
  echo "    agent-reach already installed, skipping."
else
  echo "    Installing agent-reach via pip ..."
  pip install agent-reach
  echo "    Running agent-reach install ..."
  agent-reach install --env=auto
fi

# ── 2. 安装 Skills ─────────────────────────────────────────────
install_skill() {
  local skill_name="$1"
  local src="${SCRIPT_DIR}/skills/${skill_name}"
  local dst="${TARGET_DIR}/${skill_name}"

  if [[ ! -d "${src}" ]]; then
    echo "Missing skill directory: ${src}" >&2
    exit 1
  fi

  rm -rf "${dst}"
  cp -R "${src}" "${dst}"
  echo "    Installed ${skill_name} -> ${dst}"
}

echo "==> Installing skills ..."
install_skill "ai_news_fetcher"
install_skill "ai_news_reporter"

# ── 3. 验证 ────────────────────────────────────────────────────
echo
echo "==> Verifying agent-reach ..."
if command -v agent-reach &>/dev/null; then
  agent-reach doctor || echo "    ⚠️  agent-reach doctor reported issues, please check manually."
else
  echo "    ⚠️  agent-reach command not found. You may need to restart your shell or check PATH."
fi

echo
echo "Done!"
echo
echo "Next steps:"
echo "1. Copy bitable_target.example.json to bitable_target.json for each skill"
echo "2. Fill in your own Feishu app/table configuration"
echo "3. Test the pipeline:"
echo "   curl -s 'https://r.jina.ai/https://openai.com/zh-Hans-CN/news/' \\"
echo "     | python3 ~/.openclaw/workspace/skills/ai_news_fetcher/normalize_agent_reach.py --source 'OpenAI新闻'"
