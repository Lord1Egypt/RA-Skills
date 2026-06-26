#!/usr/bin/env bash
# Must be executed with bash, not sh/dash.
if [ -z "${BASH_VERSION:-}" ]; then
  echo "Please run with bash, for example:" >&2
  echo "  bash /root/.openclaw/workspace/skills/eda-spec2gds/scripts/bootstrap_eda_demo.sh" >&2
  exit 1
fi
set -euo pipefail

# Bootstrap MVP open-source EDA environment and run a smoke test demo.
# Target: Ubuntu 24.04+
# Usage:
#   bash /root/.openclaw/workspace/skills/eda-spec2gds/scripts/bootstrap_eda_demo.sh
# Optional env:
#   OPENLANE_VERSION=2.3.10
#   OPENLANE_IMAGE=efabless/openlane:latest
#   SKIP_OPENLANE_PULL=1

OPENLANE_VERSION="${OPENLANE_VERSION:-2.3.10}"
OPENLANE_IMAGE="${OPENLANE_IMAGE:-efabless/openlane:latest}"
SKIP_OPENLANE_PULL="${SKIP_OPENLANE_PULL:-0}"

SKILL_DIR="/root/.openclaw/workspace/skills/eda-spec2gds"
RUN_ROOT="$SKILL_DIR/eda-runs"
RUN_NAME="simple_fifo_demo"
RUN_DIR="$RUN_ROOT/$RUN_NAME"

log() {
  printf '\n[%s] %s\n' "$(date '+%F %T')" "$*"
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }
}

if [[ ! -d "$SKILL_DIR" ]]; then
  echo "Skill directory not found: $SKILL_DIR" >&2
  exit 1
fi

require_cmd python3
require_cmd bash

if [[ "${EUID}" -eq 0 ]]; then
  AS_ROOT=1
else
  AS_ROOT=0
  require_cmd sudo
fi

run_privileged() {
  if [[ "$AS_ROOT" -eq 1 ]]; then
    "$@"
  else
    sudo "$@"
  fi
}

log "Installing apt packages"
run_privileged apt-get update
run_privileged apt-get install -y \
  yosys \
  iverilog \
  verilator \
  gtkwave \
  klayout \
  docker.io \
  python3-pip \
  python3-venv

log "Enabling Docker service"
run_privileged systemctl enable --now docker
if [[ "$AS_ROOT" -eq 1 ]]; then
  NEED_NEWGRP=0
else
  if ! id -nG "$USER" | grep -qw docker; then
    log "Adding $USER to docker group"
    run_privileged usermod -aG docker "$USER"
    NEED_NEWGRP=1
  else
    NEED_NEWGRP=0
  fi
fi

log "Preparing OpenLane virtualenv"
python3 -m venv "$HOME/.venvs/openlane"
# shellcheck disable=SC1091
source "$HOME/.venvs/openlane/bin/activate"
pip install --upgrade pip
pip install "openlane==${OPENLANE_VERSION}"

if [[ "$SKIP_OPENLANE_PULL" != "1" ]]; then
  log "Pulling OpenLane image: $OPENLANE_IMAGE"
  if [[ "$NEED_NEWGRP" == "1" ]]; then
    sg docker -c "docker pull $OPENLANE_IMAGE"
  else
    docker pull "$OPENLANE_IMAGE"
  fi
fi

log "Running environment check"
chmod +x "$SKILL_DIR"/scripts/*.sh "$SKILL_DIR"/scripts/*.py
"$SKILL_DIR/scripts/check_env.sh" || true

log "Preparing smoke test project"
mkdir -p "$RUN_ROOT"
python3 "$SKILL_DIR/scripts/init_project.py" "$RUN_NAME" "$RUN_ROOT" >/dev/null
cp "$SKILL_DIR/assets/examples/simple-fifo/input/raw-spec.md" "$RUN_DIR/input/raw-spec.md"
python3 "$SKILL_DIR/scripts/normalize_spec.py" \
  "$RUN_DIR/input/raw-spec.md" \
  "$RUN_DIR/input/normalized-spec.yaml" >/dev/null
cp "$SKILL_DIR/assets/examples/simple-fifo/rtl/design.v" "$RUN_DIR/rtl/design.v"
cp "$SKILL_DIR/assets/examples/simple-fifo/tb/testbench.v" "$RUN_DIR/tb/testbench.v"
cp "$SKILL_DIR/assets/examples/simple-fifo/constraints/config.json" "$RUN_DIR/constraints/config.json"

log "Running lint"
"$SKILL_DIR/scripts/run_lint.sh" "$RUN_DIR/rtl/design.v" "$RUN_DIR/lint/lint.log" || true

log "Running simulation"
"$SKILL_DIR/scripts/run_sim.sh" "$RUN_DIR/rtl/design.v" "$RUN_DIR/tb/testbench.v" "$RUN_DIR/sim" || true
if [[ -f "$RUN_DIR/sim/output.vcd" ]]; then
  log "Waveform generated: $RUN_DIR/sim/output.vcd"
fi

log "Running synthesis"
"$SKILL_DIR/scripts/run_synth.sh" "$RUN_DIR/rtl/design.v" simple_fifo "$RUN_DIR/synth" || true

log "Collecting reports"
python3 "$SKILL_DIR/scripts/collect_reports.py" "$RUN_DIR" > "$RUN_DIR/reports/artifacts.json"
python3 "$SKILL_DIR/scripts/summarize_run.py" "$RUN_DIR" > "$RUN_DIR/reports/run-summary.json"

log "Smoke test summary"
cat "$RUN_DIR/reports/run-summary.json"

log "Key output paths"
echo "Run dir: $RUN_DIR"
echo "Artifacts: $RUN_DIR/reports/artifacts.json"
echo "Summary:   $RUN_DIR/reports/run-summary.json"

if [[ "$NEED_NEWGRP" == "1" ]]; then
  cat <<'EOF'

NOTE:
- Docker group was updated for your user.
- In this shell, Docker was invoked via `sg docker -c ...` where needed.
- For future normal docker usage, re-login or run: newgrp docker
EOF
fi

cat <<'EOF'

Next optional step:
- After confirming docker works in your shell, you can try backend manually:
  source ~/.venvs/openlane/bin/activate
  cd /root/.openclaw/workspace/skills/eda-spec2gds
  ./scripts/run_openlane.sh eda-runs/simple_fifo_demo constraints/config.json
EOF
