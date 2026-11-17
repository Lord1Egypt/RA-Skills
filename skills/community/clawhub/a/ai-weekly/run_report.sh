#!/usr/bin/env bash
# run_report.sh — ai-weekly 统一启动器（框架无关：WorkBuddy / OpenClaw / 任意 Agent 通用）
#
# Python 解析优先级（第一个「已安装 feedparser/requests/beautifulsoup4」的即采用）:
#   1) $AIWEEKLY_PYTHON 环境变量（显式覆盖，跨框架部署首选）
#   2) python3 / python（系统或 OpenClaw venv）
#   3) WorkBuddy 受管 venv（仅作最后兜底，不影响其他框架）
# 找不到可用 Python 时,给出明确的 venv 创建 + 安装命令后退出。
#
# 用法(把原本的 `python scripts/xxx.py ...` 换成):
#   bash run_report.sh scripts/fetch_ai_news.py --output news.json
#   bash run_report.sh scripts/generate_site.py --api-json news.json -o AI_News.html
#   bash run_report.sh scripts/validate_report.py --html AI_News.html
#   AIWEEKLY_PYTHON=/opt/openclaw/venv/bin/python bash run_report.sh scripts/generate_site.py ...
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 候选 Python(按优先级);~ 稍后展开
CANDIDATES=()
# 1) 显式覆盖（跨框架部署首选）
if [ -n "${AIWEEKLY_PYTHON:-}" ]; then
  CANDIDATES+=("$AIWEEKLY_PYTHON")
fi
# 2) 系统 / OpenClaw venv
CANDIDATES+=("python3" "python")
# 3) WorkBuddy 受管 venv（仅最后兜底，其他框架通常命中前两项）
CANDIDATES+=(
  "$HOME/.workbuddy/binaries/python/envs/aiweekly/Scripts/python.exe"
  "$HOME/.workbuddy/binaries/python/envs/aiweekly/bin/python"
  "$HOME/.workbuddy/binaries/python/versions/3.13.12/python.exe"
)

PY=""
for cand in "${CANDIDATES[@]}"; do
  cand="${cand/#\~/$HOME}"
  [ -z "$cand" ] && continue
  if command -v "$cand" >/dev/null 2>&1 || [ -f "$cand" ]; then
    if "$cand" -c "import feedparser, requests, bs4" >/dev/null 2>&1; then
      PY="$cand"
      break
    fi
  fi
done

if [ -z "$PY" ]; then
  echo "❌ 未找到已安装依赖(feedparser/requests/beautifulsoup4)的 Python。"
  echo "请先创建 venv 并安装依赖（任选一种 Python 3.10+）："
  echo "  python3 -m venv .venv && .venv/bin/pip install -r $SCRIPT_DIR/requirements.txt"
  echo "  或显式指定：AIWEEKLY_PYTHON=/path/to/python bash run_report.sh ..."
  exit 1
fi

echo "🐍 使用 Python: $PY"

# deploy 子命令：部署周报到公开托管（P0-1：多后端·去 GitHub 化）
# 用法：bash run_report.sh deploy --html AI_News_xxx.html [--deploy-to tencent-cos|vercel|...]
if [ "${1:-}" = "deploy" ]; then
  shift
  cd "$SCRIPT_DIR" || exit 1
  exec "$PY" scripts/deploy.py "$@"
fi

exec "$PY" "$@"
