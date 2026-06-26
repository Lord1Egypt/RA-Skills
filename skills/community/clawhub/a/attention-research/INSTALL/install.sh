#!/bin/bash
#
# attention-research: Install Script
# Usage: ./install.sh --fresh | --migrate

set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG_DIR="$SKILL_ROOT/CONFIG"
SCRIPTS_DIR="$SKILL_ROOT/SCRIPTS"
CRON_JOBS_FILE="$HOME/.openclaw/cron/jobs.json"

MODE="fresh"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --fresh) MODE="fresh"; shift ;;
    --migrate) MODE="migrate"; shift ;;
    --help) echo "Usage: $0 [--fresh|--migrate]"; exit 0 ;;
  esac
done

check_prereqs() {
  echo "=== Prerequisites ==="
  python3 --version || exit 1
  python3 -c "import yaml" 2>/dev/null || {
    echo "Installing pyyaml..."
    python3 -m pip install pyyaml --break-system-packages --quiet
  }
  echo "  Python: ok"
  echo "  PyYAML: ok"
}

prompt_config() {
  echo "=== Configuration ==="
  echo "Web search: handled by the invoking agent's own search tool."
  echo "Delivery channel (Telegram chat ID, WhatsApp recipient) is set"
  echo "in CONFIG/default-paths.yaml. The agent reads it at delivery time."
}

ensure_topic_structure() {
  local research_root="$HOME/.openclaw/workspace/docs/research"
  mkdir -p "$research_root"
  python3 -c "
import yaml, os, json, pathlib

research_root = pathlib.Path('$research_root')
cfg = yaml.safe_load(open('$CONFIG_DIR/topics.yaml'))

for topic, topic_cfg in cfg.get('topics', {}).items():
    if not topic_cfg.get('enabled', True):
        continue
    td = research_root / 'topics' / topic
    for sub in ['news', 'threads', 'entities', 'updates']:
        (td / sub).mkdir(parents=True, exist_ok=True)
    mf = td / 'META.json'
    if not mf.exists():
        meta = {'schema': 'attention-research.v1', 'topic': topic,
                'lastHeartbeatUpdate': None, 'lastMorningUpdate': None,
                'lastAfternoonUpdate': None, 'retryCount': 0,
                'retryDate': None, 'lastError': None, 'note': None}
        json.dump(meta, open(mf, 'w'), indent=2)
        print(f'  Created: {topic}/META.json')
print(f'Topic structure ready: {research_root}')
"
}

install_fresh() {
  echo "=== Fresh Install ==="
  ensure_topic_structure
  echo ""
  echo "Running setup-cron.sh..."
  bash "$SCRIPTS_DIR/setup-cron.sh"
  echo ""
  echo "=== Done ==="
  echo "Next: openclaw cron status"
}

install_migrate() {
  echo "=== Migrate ==="
  bash "$SCRIPTS_DIR/setup-cron.sh"
}

main() {
  echo "=== attention-research install ==="
  echo "Mode: $MODE"
  echo ""
  check_prereqs
  prompt_config
  case "$MODE" in
    fresh) install_fresh ;;
    migrate) install_migrate ;;
  esac
}

main