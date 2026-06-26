#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_ROOT/../.." && pwd)"
STRICT_DEPS="${STRICT_DEPS:-0}"
CHECK_REMOTE_SKILL="${CHECK_REMOTE_SKILL:-0}"
REMOTE_PROBE_MODE="${REMOTE_PROBE_MODE:-warn}"
SKILLS_HOME="${CODEX_HOME:-$HOME/.codex}/skills"
DEPENDENCY_CATALOG="$SKILL_ROOT/config/dependency-sources.json"

if [[ -f "$REPO_ROOT/scripts/validate_skill_repo.py" && -d "$REPO_ROOT/skills/claws-temple-bounty" ]]; then
  VALIDATOR_PATH="$REPO_ROOT/scripts/validate_skill_repo.py"
  PROBE_SCRIPT="$SKILL_ROOT/scripts/task4-live-skill-probe.sh"
  SELF_HEAL_COMMAND="bash scripts/self-heal-local-dependency.sh"
  VALIDATOR_MODE="repo"
else
  VALIDATOR_PATH="$SKILL_ROOT/scripts/validate_clawhub_bundle.py"
  PROBE_SCRIPT="$SKILL_ROOT/scripts/task4-live-skill-probe.sh"
  SELF_HEAL_COMMAND="bash scripts/self-heal-local-dependency.sh"
  VALIDATOR_MODE="bundle"
fi

get_catalog_field() {
  local dep="$1"
  local field="$2"
  python3 - "$DEPENDENCY_CATALOG" "$dep" "$field" <<'PY'
import json
import sys
from pathlib import Path

catalog = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
entry = catalog["dependencies"].get(sys.argv[2], {})
print(entry.get(sys.argv[3], ""))
PY
}

print_dep_source_hint() {
  local dep="$1"
  local normalized="$dep"
  normalized="${normalized%%:*}"
  local repo_url env_name
  repo_url="$(get_catalog_field "$normalized" default_repo_url)"
  env_name="$(get_catalog_field "$normalized" env_override)"
  if [[ -n "$repo_url" ]]; then
    echo "[smoke-check] suggestion: run $SELF_HEAL_COMMAND $normalized"
    echo "[smoke-check] suggestion: default source repo -> $repo_url"
    echo "[smoke-check] suggestion: optional local override -> export $env_name=/path/to/local/repo-or-skill"
  fi
}

echo "[smoke-check] validating repository structure and visible-layer rules"
if [[ "$VALIDATOR_MODE" == "repo" ]]; then
  python3 "$VALIDATOR_PATH"
else
  python3 "$VALIDATOR_PATH" "$SKILL_ROOT"
fi

echo "[smoke-check] checking Task 3 proposal URLs are present"
python3 - "$SKILL_ROOT" <<'PY'
import json
import sys
from pathlib import Path

skill_root = Path(sys.argv[1])
config_path = skill_root / "config" / "faction-proposals.json"
config = json.loads(config_path.read_text(encoding="utf-8"))
for faction in config["factions"]:
    expected = f"https://tmrwdao.com/dao/{config['dao_alias']}/proposal/{faction['proposal_id']}"
    if faction["proposal_url"] != expected:
        raise SystemExit(
            f"proposal_url mismatch for {faction['brand_key']}: {faction['proposal_url']} != {expected}"
        )
print("proposal_url entries verified")
PY

echo "[smoke-check] checking local dependency skills"
missing_deps=()
for dep in agent-spectrum resonance-contract tomorrowdao-agent-skills portkey-ca-agent-skills; do
  if [[ ! -d "$SKILLS_HOME/$dep" ]]; then
    missing_deps+=("$dep")
    continue
  fi
  if [[ ! -f "$SKILLS_HOME/$dep/SKILL.md" ]]; then
    missing_deps+=("$dep:missing-skill-entry")
  fi
done

if (( ${#missing_deps[@]} > 0 )); then
  for dep in "${missing_deps[@]}"; do
    print_dep_source_hint "$dep"
  done
  if [[ "$STRICT_DEPS" == "1" ]]; then
    echo "[smoke-check] missing dependency skills in $SKILLS_HOME: ${missing_deps[*]}" >&2
    exit 1
  fi
  echo "[smoke-check] warning: missing dependency skills in $SKILLS_HOME: ${missing_deps[*]}"
  echo "[smoke-check] warning: this is a repo self-check only; use release-gate.sh for a hard release gate"
else
  echo "[smoke-check] dependency skills verified"
fi

echo "[smoke-check] checking resonance-contract dependency version"
python3 - "$SKILLS_HOME" "$STRICT_DEPS" "$DEPENDENCY_CATALOG" <<'PY'
import re
import sys
import json
from pathlib import Path

skills_home = Path(sys.argv[1])
strict = sys.argv[2] == "1"
catalog = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
issues: list[str] = []

dep_dir = skills_home / "resonance-contract"
skill_path = dep_dir / "SKILL.md"
dep_cfg = catalog["dependencies"]["resonance-contract"]
min_version_raw = dep_cfg["min_version"]
min_version = tuple(int(part) for part in min_version_raw.split("."))
repo_url = dep_cfg["default_repo_url"]

if not skill_path.exists():
    issues.append(f"missing SKILL.md in {dep_dir}")
else:
    text = skill_path.read_text(encoding="utf-8")
    match = re.search(r"^version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", text, re.MULTILINE)
    if not match:
        issues.append(f"could not resolve resonance-contract version from {skill_path}")
    else:
        raw = match.group(1)
        actual = tuple(int(part) for part in raw.split("."))
        if actual < min_version:
            issues.append(
                f"resonance-contract version {raw} is below required {min_version_raw}; "
                f"upgrade from {repo_url}"
            )

if issues:
    joined = "; ".join(issues)
    if strict:
        raise SystemExit(joined)
    print(f"[smoke-check] warning: {joined}")
else:
    print("[smoke-check] resonance-contract dependency version verified")
PY

echo "[smoke-check] checking TomorrowDAO dependency version and Task 3 preflight tools"
python3 - "$SKILL_ROOT" "$SKILLS_HOME" "$STRICT_DEPS" "$DEPENDENCY_CATALOG" <<'PY'
import json
import sys
from pathlib import Path

skill_root = Path(sys.argv[1])
skills_home = Path(sys.argv[2])
strict = sys.argv[3] == "1"
catalog = json.loads(Path(sys.argv[4]).read_text(encoding="utf-8"))
config = json.loads((skill_root / "config" / "faction-proposals.json").read_text(encoding="utf-8"))
dep_dir = skills_home / "tomorrowdao-agent-skills"
issues: list[str] = []

def parse_version(raw: str) -> tuple[int, ...]:
    return tuple(int(part) for part in raw.split(".") if part.isdigit())

pkg_path = dep_dir / "package.json"
dep_cfg = catalog["dependencies"]["tomorrowdao-agent-skills"]
catalog_min_version = dep_cfg["min_version"]
repo_url = dep_cfg["default_repo_url"]
if not pkg_path.exists():
    issues.append(f"missing package.json in {dep_dir}")
else:
    pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
    actual_version = str(pkg.get("version") or "")
    min_version = config["dependency_min_version"]
    if min_version != catalog_min_version:
        issues.append(
            f"dependency catalog min version {catalog_min_version} does not match Task 3 config {min_version}"
        )
    if parse_version(actual_version) < parse_version(min_version):
        issues.append(
            f"tomorrowdao-agent-skills version {actual_version} is below required {min_version}; "
            f"upgrade from {repo_url}"
        )

tool_markers = [
    config["token_balance_tool_name"],
    config["token_allowance_tool_name"],
    config["dependency_invocation"]["approve_tool_name"],
    config["dependency_invocation"]["tool_name"],
]
server_path = dep_dir / "src" / "mcp" / "server.ts"
openclaw_path = dep_dir / "openclaw.json"
cli_path = dep_dir / "tomorrowdao_skill.ts"
for path in (server_path, openclaw_path):
    if not path.exists():
        issues.append(f"missing expected dependency file: {path}")
        continue
    text = path.read_text(encoding="utf-8")
    for tool_marker in tool_markers:
        if tool_marker not in text:
            issues.append(f"{tool_marker} not found in {path}")
cli_markers = (
    "token-balance-view",
    "token-allowance-view",
    "tokenApprove",
    "daoVote",
)
if not cli_path.exists():
    issues.append(f"missing expected dependency file: {cli_path}")
else:
    cli_text = cli_path.read_text(encoding="utf-8")
    for cli_marker in cli_markers:
        if cli_marker not in cli_text:
            issues.append(f"{cli_marker} not found in {cli_path}")

if issues:
    joined = "; ".join(issues)
    if strict:
        raise SystemExit(joined)
    print(f"[smoke-check] warning: {joined}")
else:
    print("[smoke-check] tomorrowdao dependency version and Task 3 preflight tools verified")
PY

echo "[smoke-check] checking Portkey CA dependency version and forward-call tool"
python3 - "$SKILLS_HOME" "$STRICT_DEPS" "$DEPENDENCY_CATALOG" <<'PY'
import json
import re
import sys
from pathlib import Path

skills_home = Path(sys.argv[1])
strict = sys.argv[2] == "1"
catalog = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
issues: list[str] = []

dep_dir = skills_home / "portkey-ca-agent-skills"
skill_path = dep_dir / "SKILL.md"
pkg_path = dep_dir / "package.json"
server_path = dep_dir / "src" / "mcp" / "server.ts"
catalog_min = catalog["dependencies"]["portkey-ca-agent-skills"]["min_version"]
repo_url = catalog["dependencies"]["portkey-ca-agent-skills"]["default_repo_url"]

def parse_version(raw: str) -> tuple[int, ...]:
    return tuple(int(part) for part in raw.split(".") if part.isdigit())

if not skill_path.exists():
    issues.append(f"missing SKILL.md in {dep_dir}")
else:
    text = skill_path.read_text(encoding="utf-8")
    match = re.search(r'^version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?\s*$', text, re.MULTILINE)
    if not match:
      issues.append(f"could not resolve portkey-ca-agent-skills version from {skill_path}")
    elif parse_version(match.group(1)) < parse_version(catalog_min):
      issues.append(
          f"portkey-ca-agent-skills version {match.group(1)} is below required {catalog_min}; upgrade from {repo_url}"
      )

if not pkg_path.exists():
    issues.append(f"missing package.json in {dep_dir}")
else:
    pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
    actual_version = str(pkg.get("version") or "")
    if parse_version(actual_version) < parse_version(catalog_min):
        issues.append(
            f"portkey-ca-agent-skills package version {actual_version} is below required {catalog_min}; "
            f"upgrade from {repo_url}"
        )

if not server_path.exists():
    issues.append(f"missing expected dependency file: {server_path}")
else:
    text = server_path.read_text(encoding="utf-8")
    if "portkey_forward_call" not in text:
        issues.append("portkey_forward_call not found in portkey-ca-agent-skills MCP server")

if issues:
    joined = "; ".join(issues)
    if strict:
        raise SystemExit(joined)
    print(f"[smoke-check] warning: {joined}")
else:
    print("[smoke-check] portkey-ca-agent-skills dependency version and CA write tool verified")
PY

if [[ "$CHECK_REMOTE_SKILL" == "1" ]]; then
  echo "[smoke-check] checking remote Task 4 live skill"
  PROBE_MODE="$REMOTE_PROBE_MODE" \
    bash "$PROBE_SCRIPT"
  echo "[smoke-check] remote live skill reachable"
fi

echo "[smoke-check] OK"
