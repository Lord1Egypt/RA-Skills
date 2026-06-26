#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR_RAW="${FOUNDER_SIGNAL_HOME:-$HOME/.founder-signal}"
DATA_DIR="$(python3 - "${DATA_DIR_RAW}" <<'PY'
import sys
from pathlib import Path

print(Path(sys.argv[1]).expanduser().resolve())
PY
)"
LOG_DIR="${DATA_DIR}/logs"
LOG_FILE="${LOG_DIR}/founder-signal-cron.log"
LOCK_DIR="${DATA_DIR}/.founder-signal-run.lock"
LOCK_PID_FILE="${LOCK_DIR}/pid"
LOCK_ACQUIRED=0
PROFILE_ID=""
CONFIG_PATH=""
RUN_ALL=1
RUN_ID=""
RUN_DIR=""
ABS_RUN_DIR=""
REQUIRE_ACTION_CARD=0
REQUIRE_PUBLISH_INTENT=0
REQUIRE_ALL_PROFILES=0

usage() {
  cat <<EOF
Usage:
  bash scripts/run_founder_signal_once.sh
  bash scripts/run_founder_signal_once.sh --all
  bash scripts/run_founder_signal_once.sh --profile <profile_id>
  bash scripts/run_founder_signal_once.sh --config founder-signal.config.json
  bash scripts/run_founder_signal_once.sh --all --require-action-card --require-publish-intent

Options:
  --all                 Run all enabled product profiles. This is the default.
  --profile <profile>   Run only the named product profile.
  --config <path>       Validate/import a canonical config JSON, then run that profile.
  --require-action-card  Exit non-zero unless an Action Card is generated.
  --require-publish-intent
                        Exit non-zero unless a Draft publish intent is generated.
  --require-all-profiles Apply required artifact checks to every requested profile.
  --help                Show this help text.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)
      RUN_ALL=1
      PROFILE_ID=""
      shift
      ;;
    --profile)
      if [[ $# -lt 2 ]]; then
        usage >&2
        exit 1
      fi
      RUN_ALL=0
      PROFILE_ID="$2"
      shift 2
      ;;
    --config)
      if [[ $# -lt 2 ]]; then
        usage >&2
        exit 1
      fi
      CONFIG_PATH="$2"
      RUN_ALL=0
      shift 2
      ;;
    --require-action-card)
      REQUIRE_ACTION_CARD=1
      shift
      ;;
    --require-publish-intent)
      REQUIRE_PUBLISH_INTENT=1
      shift
      ;;
    --require-all-profiles)
      REQUIRE_ALL_PROFILES=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      usage >&2
      exit 1
      ;;
  esac
done

mkdir -p "${DATA_DIR}/runs" "${LOG_DIR}" "${DATA_DIR}/state" "${DATA_DIR}/config-imports" "${DATA_DIR}/profiles"
exec >> "${LOG_FILE}" 2>&1

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*"
}

write_failed_marker() {
  local failure_message="${1:-Founder Signal runner failed.}"
  if [[ -d "${ABS_RUN_DIR:-}" ]] && [[ ! -f "${ABS_RUN_DIR}/FAILED.md" ]]; then
    PYTHONPATH="${SKILL_DIR}/src${PYTHONPATH:+:${PYTHONPATH}}" python3 - "${DATA_DIR}" "${ABS_RUN_DIR}" "${RUN_ID}" "${failure_message}" "${LOG_FILE}" <<'PY' || true
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from founder_signal.report import write_failed_marker, write_report

root_dir = Path(sys.argv[1])
run_dir = Path(sys.argv[2])
run_id = sys.argv[3]
failure_message = sys.argv[4]
log_file = sys.argv[5]
artifact = {
    "run_id": run_id,
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "failed",
    "run_dir": str(run_dir),
    "root_dir": str(root_dir),
    "failure_message": failure_message,
    "error": failure_message,
    "log_file": log_file,
    "failures": [failure_message],
    "safety_decision": "unsafe_to_score_from_this_runtime",
}
(run_dir / "run.json").write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
write_report(run_dir=run_dir, artifact=artifact)
write_failed_marker(run_dir=run_dir, artifact=artifact)
PY
  fi

  if [[ -d "${ABS_RUN_DIR:-}" ]] && [[ ! -f "${ABS_RUN_DIR}/FAILED.md" ]]; then
    cat <<EOF > "${ABS_RUN_DIR}/FAILED.md"
# Founder Signal Run Failed

- Run ID: ${RUN_ID}
- Run directory: ${ABS_RUN_DIR}
- Failure: ${failure_message}
- Logged at: $(timestamp)
- Log file: ${LOG_FILE}
EOF
  fi
}

cleanup() {
  local exit_code=$?
  if [[ ${exit_code} -ne 0 ]]; then
    log "Founder Signal run failed with exit code ${exit_code}."
    write_failed_marker "Shell runner exited with status ${exit_code}."
  fi

  if [[ ${LOCK_ACQUIRED} -eq 1 ]]; then
    rm -f "${LOCK_PID_FILE}"
    rmdir "${LOCK_DIR}" 2>/dev/null || true
  fi
}

trap cleanup EXIT

acquire_lock() {
  if mkdir "${LOCK_DIR}" 2>/dev/null; then
    LOCK_ACQUIRED=1
    printf '%s\n' "$$" > "${LOCK_PID_FILE}"
    return 0
  fi

  local existing_pid=""
  if [[ -f "${LOCK_PID_FILE}" ]]; then
    existing_pid="$(tr -d '[:space:]' < "${LOCK_PID_FILE}" || true)"
  fi

  if [[ -n "${existing_pid}" ]] && kill -0 "${existing_pid}" 2>/dev/null; then
    log "Founder Signal run skipped because PID ${existing_pid} already holds the lock."
    exit 0
  fi

  log "Founder Signal runner found a stale lock; clearing it."
  rm -f "${LOCK_PID_FILE}"
  rmdir "${LOCK_DIR}" 2>/dev/null || true

  if mkdir "${LOCK_DIR}" 2>/dev/null; then
    LOCK_ACQUIRED=1
    printf '%s\n' "$$" > "${LOCK_PID_FILE}"
    return 0
  fi

  log "Founder Signal runner could not acquire the lock after stale-lock cleanup."
  exit 1
}

acquire_lock
while true; do
  RUN_ID="$(date '+%Y-%m-%d-%H%M%S')"
  RUN_DIR="runs/$RUN_ID"
  ABS_RUN_DIR="${DATA_DIR}/${RUN_DIR}"
  if [[ ! -e "${ABS_RUN_DIR}" ]]; then
    break
  fi
  sleep 1
done

mkdir -p "${ABS_RUN_DIR}"
log "Founder Signal run started: ${RUN_ID}"
log "Run directory: ${ABS_RUN_DIR}"
if [[ -n "${CONFIG_PATH}" ]]; then
  log "Config path: ${CONFIG_PATH}"
elif [[ -n "${PROFILE_ID}" ]]; then
  log "Profile mode: ${PROFILE_ID}"
else
  log "Profile mode: all enabled profiles"
fi

if [[ "${FOUNDER_SIGNAL_HOLD_SECONDS:-0}" != "0" ]]; then
  sleep "${FOUNDER_SIGNAL_HOLD_SECONDS}"
fi

export PYTHONPATH="${SKILL_DIR}/src${PYTHONPATH:+:${PYTHONPATH}}"
export FOUNDER_SIGNAL_PROFILE_ID="${PROFILE_ID}"
export FOUNDER_SIGNAL_REQUIRE_ACTION_CARD="${REQUIRE_ACTION_CARD}"
export FOUNDER_SIGNAL_REQUIRE_PUBLISH_INTENT="${REQUIRE_PUBLISH_INTENT}"
export FOUNDER_SIGNAL_REQUIRE_ALL_PROFILES="${REQUIRE_ALL_PROFILES}"
export FOUNDER_SIGNAL_HOME="${DATA_DIR}"

if [[ -n "${CONFIG_PATH}" ]]; then
  PREPARED_PROFILE_ID="$(
    python3 - "${DATA_DIR}" "${CONFIG_PATH}" <<'PY'
import sys
from pathlib import Path

from founder_signal.setup import import_user_config

root_dir = Path(sys.argv[1])
config_path = Path(sys.argv[2])
result = import_user_config(root_dir=root_dir, config_path=config_path)
print(result.profile_id)
PY
  )"
  PREPARED_PROFILE_ID="${PREPARED_PROFILE_ID//$'\n'/}"
  if [[ -n "${PROFILE_ID}" ]] && [[ "${PROFILE_ID}" != "${PREPARED_PROFILE_ID}" ]]; then
    log "Founder Signal config profile mismatch: requested ${PROFILE_ID}, imported ${PREPARED_PROFILE_ID}."
    exit 1
  fi
  PROFILE_ID="${PREPARED_PROFILE_ID}"
  export FOUNDER_SIGNAL_PROFILE_ID="${PROFILE_ID}"
  log "Config import ready for profile: ${PROFILE_ID}"
fi

python3 - "${DATA_DIR}" "${ABS_RUN_DIR}" <<'PY'
import json
import os
import sys
from pathlib import Path

from founder_signal import run_once

root_dir = Path(sys.argv[1])
run_dir = Path(sys.argv[2])
selected_profile_id = os.environ.get("FOUNDER_SIGNAL_PROFILE_ID") or None
require_action_card = os.environ.get("FOUNDER_SIGNAL_REQUIRE_ACTION_CARD") == "1"
require_publish_intent = os.environ.get("FOUNDER_SIGNAL_REQUIRE_PUBLISH_INTENT") == "1"
require_all_profiles = os.environ.get("FOUNDER_SIGNAL_REQUIRE_ALL_PROFILES") == "1"
result = run_once(
    root_dir=root_dir,
    run_dir=run_dir,
    selected_profile_id=selected_profile_id,
)
print(json.dumps(result, indent=2))
if result.get("status") == "failed":
    sys.exit(1)

failures = []
profile_results = result.get("profile_results") or []
if require_action_card and not result.get("action_card_generated"):
    failures.append("required Action Card was not generated")
def has_draft_url(item):
    return bool(item.get("draft_public_publish_succeeded")) and bool(str(item.get("draft_public_url") or item.get("draft_url") or "").strip())

if require_publish_intent and not has_draft_url(result):
    failures.append("required Draft public page URL was not generated")
if require_all_profiles:
    if not profile_results:
        failures.append("required profile checks found no profile results")
    for item in profile_results:
        profile_id = item.get("profile_id") or "unknown"
        if require_action_card and not item.get("action_card_generated"):
            failures.append(f"{profile_id}: required Action Card was not generated")
        if require_publish_intent and not has_draft_url(item):
            failures.append(f"{profile_id}: required Draft public page URL was not generated")
if failures:
    result["status"] = "failed"
    result["next_step"] = "provide_verified_evidence_and_retry_e2e"
    result["failures"] = list(dict.fromkeys([str(item) for item in result.get("failures", [])] + failures))
    result["error"] = "; ".join(failures)
    (run_dir / "run.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    from founder_signal.report import write_failed_marker, write_report

    write_report(run_dir=run_dir, artifact=result)
    write_failed_marker(run_dir=run_dir, artifact=result)
    print(json.dumps(result, indent=2))
    sys.exit(1)
PY

log "Founder Signal run completed: ${RUN_ID}"
