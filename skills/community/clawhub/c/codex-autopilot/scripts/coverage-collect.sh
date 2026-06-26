#!/bin/bash
# coverage-collect.sh — 覆盖率收集与归一化输出
# 用法:
#   coverage-collect.sh detect <project_dir>
#   coverage-collect.sh monorepo <project_dir>
#   coverage-collect.sh packages <project_dir>
#   coverage-collect.sh collect <project_dir>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=autopilot-lib.sh
source "${SCRIPT_DIR}/autopilot-lib.sh"
if [ -f "${SCRIPT_DIR}/autopilot-constants.sh" ]; then
    # shellcheck disable=SC1091
    source "${SCRIPT_DIR}/autopilot-constants.sh"
fi

RUN_LOG_BASENAME=".autopilot-test-run.log"

inspect_packages() {
    local project_dir="$1"
    python3 - "$project_dir" <<'PYEOF'
import fnmatch
import glob
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def parse_pnpm_workspace_patterns(path: Path) -> list[str]:
    if not path.exists():
        return []

    patterns: list[str] = []
    in_packages = False
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not in_packages:
            if re.match(r"^\s*packages\s*:\s*$", line):
                in_packages = True
            continue
        if re.match(r"^\S", line):
            break
        match = re.match(r"^\s*-\s*(.+?)\s*$", line)
        if not match:
            continue
        value = match.group(1).strip().strip("'\"")
        if value:
            patterns.append(value)
    return patterns


def get_workspace_patterns(root_dir: Path) -> list[str]:
    package_json = load_json(root_dir / "package.json")
    patterns: list[str] = []
    workspaces = package_json.get("workspaces")
    if isinstance(workspaces, list):
        patterns.extend(str(item) for item in workspaces if isinstance(item, str))
    elif isinstance(workspaces, dict):
        packages = workspaces.get("packages")
        if isinstance(packages, list):
            patterns.extend(str(item) for item in packages if isinstance(item, str))
    patterns.extend(parse_pnpm_workspace_patterns(root_dir / "pnpm-workspace.yaml"))

    deduped: list[str] = []
    seen: set[str] = set()
    for pattern in patterns:
        if pattern not in seen:
            deduped.append(pattern)
            seen.add(pattern)
    return deduped


def detect_package_manager(package_dir: Path) -> str:
    for base in (package_dir, root):
        if (base / "pnpm-lock.yaml").exists():
            return "pnpm"
        if (base / "package-lock.json").exists():
            return "npm"
        if (base / "yarn.lock").exists():
            return "yarn"
        if (base / "bun.lockb").exists() or (base / "bun.lock").exists():
            return "bun"
    return "npm"


def has_bats_tests(package_dir: Path) -> bool:
    test_dir = package_dir / "test"
    return test_dir.is_dir() and any(test_dir.glob("*.bats"))


def normalize_test_script(value: object) -> str:
    if not isinstance(value, str):
        return ""
    script = value.strip()
    if not script:
        return ""
    if "no test specified" in script.lower():
        return ""
    return script


def package_info(package_dir: Path) -> dict:
    package_json = load_json(package_dir / "package.json")
    scripts = package_json.get("scripts") if isinstance(package_json.get("scripts"), dict) else {}
    test_script = normalize_test_script((scripts or {}).get("test"))
    deps: set[str] = set()
    for section in ("devDependencies", "dependencies", "peerDependencies"):
        values = package_json.get(section)
        if isinstance(values, dict):
            deps.update(key.lower() for key in values.keys())

    lower_script = test_script.lower()
    framework = "unknown"
    has_tests = False

    if test_script:
        has_tests = True
        if "node --test" in lower_script:
            framework = "node_test"
        elif "vitest" in deps or "vitest" in lower_script:
            framework = "vitest"
        elif "jest" in deps or "jest" in lower_script:
            framework = "jest"
        else:
            framework = "package_script"
    elif (package_dir / "build.gradle").exists() or (package_dir / "build.gradle.kts").exists():
        has_tests = True
        framework = "junit"
    elif has_bats_tests(package_dir):
        has_tests = True
        framework = "bats"

    relative_dir = "."
    try:
        relative_dir = str(package_dir.relative_to(root)).replace("\\", "/")
    except Exception:
        relative_dir = str(package_dir).replace("\\", "/")

    return {
        "name": package_json.get("name") or package_dir.name,
        "dir": str(package_dir),
        "relative_dir": relative_dir,
        "framework": framework,
        "package_manager": detect_package_manager(package_dir),
        "test_script": test_script,
        "has_tests": has_tests,
    }


def discover_workspace_packages(root_dir: Path, patterns: list[str]) -> list[dict]:
    include_patterns = [pattern for pattern in patterns if not pattern.startswith("!")]
    exclude_patterns = [pattern[1:] for pattern in patterns if pattern.startswith("!")]

    discovered: dict[str, dict] = {}
    for pattern in include_patterns:
        for match in glob.glob(str(root_dir / pattern), recursive=True):
            candidate = Path(match)
            if not candidate.is_dir():
                continue
            if candidate == root_dir:
                continue
            if any(part in {"node_modules", ".git"} for part in candidate.parts):
                continue
            rel = str(candidate.relative_to(root_dir)).replace("\\", "/")
            if any(fnmatch.fnmatch(rel, excluded) for excluded in exclude_patterns):
                continue
            if not (candidate / "package.json").exists():
                continue
            info = package_info(candidate)
            if info["has_tests"]:
                discovered[rel] = info

    return [discovered[key] for key in sorted(discovered)]


workspace_patterns = get_workspace_patterns(root)
monorepo = bool(workspace_patterns)
packages = discover_workspace_packages(root, workspace_patterns) if monorepo else []

if not packages:
    root_info = package_info(root)
    if root_info["has_tests"]:
        packages = [root_info]

print(
    json.dumps(
        {
            "root": str(root),
            "monorepo": monorepo,
            "workspace_patterns": workspace_patterns,
            "packages": packages,
        },
        ensure_ascii=False,
    )
)
PYEOF
}

detect_monorepo() {
    local project_dir="$1"
    inspect_packages "$project_dir" | jq -r '.monorepo'
}

list_test_packages() {
    local project_dir="$1"
    inspect_packages "$project_dir"
}

detect_framework() {
    local project_dir="$1"
    local inspected
    inspected=$(inspect_packages "$project_dir")
    if echo "$inspected" | jq -e '.monorepo == true and (.packages | length) > 0' >/dev/null 2>&1; then
        echo "monorepo"
        return 0
    fi
    echo "$inspected" | jq -r '.packages[0].framework // "unknown"'
}

collect_istanbul_coverage() {
    local project_dir="$1" tool="$2"
    local summary_file="${project_dir}/coverage/coverage-summary.json"
    local lcov_file="${project_dir}/coverage/lcov.info"

    if [ ! -f "$summary_file" ]; then
        jq -n --arg tool "$tool" --arg now "$(now_ts)" '{tool:$tool,line_coverage:0,files:[],generated_at:($now|tonumber),error:"missing_coverage_summary"}'
        return 0
    fi

    python3 - "$project_dir" "$summary_file" "$lcov_file" "$tool" <<'PYEOF'
import json
import sys
from pathlib import Path

project_dir = Path(sys.argv[1]).resolve()
summary_path = Path(sys.argv[2])
lcov_path = Path(sys.argv[3])
tool = sys.argv[4]


def rel_path(path_text: str) -> str:
    p = Path(path_text)
    if p.is_absolute():
        try:
            return str(p.resolve().relative_to(project_dir)).replace("\\", "/")
        except Exception:
            return str(p).replace("\\", "/")
    return str(p).replace("\\", "/").lstrip("./")


summary = json.loads(summary_path.read_text(encoding="utf-8"))
total = summary.get("total", {})
total_lines = total.get("lines", {}) or {}
line_coverage = float(total_lines.get("pct") or 0)
covered = int(total_lines.get("covered") or 0)
total_count = int(total_lines.get("total") or 0)
missed = max(total_count - covered, 0)

uncovered_map = {}
if lcov_path.exists():
    current_file = ""
    with lcov_path.open("r", encoding="utf-8", errors="ignore") as fh:
        for raw in fh:
            line = raw.strip()
            if line.startswith("SF:"):
                current_file = line[3:]
                uncovered_map.setdefault(rel_path(current_file), [])
            elif line.startswith("DA:") and current_file:
                data = line[3:].split(",", 1)
                if len(data) != 2:
                    continue
                try:
                    line_no = int(data[0])
                    hits = int(float(data[1]))
                except ValueError:
                    continue
                if hits == 0:
                    uncovered_map.setdefault(rel_path(current_file), []).append(line_no)

files = []
for path_text, data in summary.items():
    if path_text == "total":
        continue
    pct = float((data.get("lines", {}) or {}).get("pct") or 0)
    file_path = rel_path(path_text)
    files.append(
        {
            "path": file_path,
            "line_pct": pct,
            "uncovered_lines": uncovered_map.get(file_path, [])[:80],
        }
    )

files.sort(key=lambda item: (item.get("line_pct", 0), item.get("path", "")))

print(
    json.dumps(
        {
            "tool": tool,
            "line_coverage": line_coverage,
            "line_covered": covered,
            "line_total": total_count,
            "line_missed": missed,
            "files": files,
            "generated_at": int(__import__("time").time()),
        },
        ensure_ascii=False,
    )
)
PYEOF
}

collect_node_test_coverage() {
    local project_dir="$1"
    local run_log="${project_dir}/${RUN_LOG_BASENAME}"

    if [ ! -f "$run_log" ]; then
        jq -n --arg now "$(now_ts)" '{tool:"node_test",line_coverage:0,files:[],generated_at:($now|tonumber),error:"missing_node_test_run_log"}'
        return 0
    fi

    python3 - "$project_dir" "$run_log" <<'PYEOF'
import json
import re
import sys
from pathlib import Path

project_dir = Path(sys.argv[1]).resolve()
run_log = Path(sys.argv[2])


def rel_path(path_text: str) -> str:
    p = Path(path_text.strip())
    if p.is_absolute():
        try:
            return str(p.resolve().relative_to(project_dir)).replace("\\", "/")
        except Exception:
            return str(p).replace("\\", "/")
    return str(p).replace("\\", "/").lstrip("./")


files = []
line_coverage = 0.0
in_report = False
for raw in run_log.read_text(encoding="utf-8", errors="ignore").splitlines():
    line = raw.strip()
    if "# start of coverage report" in line:
        in_report = True
        continue
    if "# end of coverage report" in line:
        break
    if not in_report or not line.startswith("# "):
        continue

    payload = line[2:].strip()
    if not payload or payload.startswith("file |"):
        continue

    parts = [part.strip() for part in payload.split("|")]
    if len(parts) < 4:
        continue

    name = parts[0]
    try:
        pct = float(parts[1])
    except ValueError:
        continue

    uncovered_field = parts[4] if len(parts) > 4 else ""
    uncovered_lines = []
    for chunk in uncovered_field.split(","):
        value = chunk.strip()
        if not value:
            continue
        range_match = re.match(r"^(\d+)-(\d+)$", value)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2))
            uncovered_lines.extend(list(range(start, end + 1)))
            continue
        if value.isdigit():
            uncovered_lines.append(int(value))

    if name.lower() == "all files":
        line_coverage = pct
        continue

    files.append(
        {
            "path": rel_path(name),
            "line_pct": pct,
            "uncovered_lines": uncovered_lines[:80],
        }
    )

files.sort(key=lambda item: (item.get("line_pct", 0), item.get("path", "")))

print(
    json.dumps(
        {
            "tool": "node_test",
            "line_coverage": line_coverage,
            "files": files,
            "generated_at": int(__import__("time").time()),
        },
        ensure_ascii=False,
    )
)
PYEOF
}

collect_junit_coverage() {
    local project_dir="$1"
    local xml_file="${project_dir}/build/reports/jacoco/test/jacocoTestReport.xml"

    if [ ! -f "$xml_file" ]; then
        jq -n --arg now "$(now_ts)" '{tool:"junit",line_coverage:0,files:[],generated_at:($now|tonumber),error:"missing_jacoco_xml"}'
        return 0
    fi

    local line missed covered pct
    line=$(grep -m1 'counter type="LINE"' "$xml_file" 2>/dev/null || true)
    missed=$(echo "$line" | sed -n 's/.*missed="\([0-9][0-9]*\)".*/\1/p')
    covered=$(echo "$line" | sed -n 's/.*covered="\([0-9][0-9]*\)".*/\1/p')
    missed=$(normalize_int "$missed")
    covered=$(normalize_int "$covered")

    if [ $((missed + covered)) -gt 0 ]; then
        pct=$(awk -v c="$covered" -v m="$missed" 'BEGIN{printf "%.2f", (c*100)/(c+m)}')
    else
        pct="0"
    fi

    jq -n \
        --arg pct "$pct" \
        --arg covered "$covered" \
        --arg missed "$missed" \
        --arg now "$(now_ts)" \
        '{tool:"junit",line_coverage:($pct|tonumber),line_covered:($covered|tonumber),line_missed:($missed|tonumber),line_total:(($covered|tonumber)+($missed|tonumber)),files:[],generated_at:($now|tonumber)}'
}

collect_bats_coverage() {
    local project_dir="$1"
    local pass_rate="0"
    local output rc total failed

    if command -v bats >/dev/null 2>&1; then
        set +e
        output=$(cd "$project_dir" && run_with_timeout 120 bats test/ 2>&1)
        rc=$?
        set -e

        total=$(echo "$output" | sed -n 's/.*\([0-9][0-9]*\) tests, .*/\1/p' | tail -n1)
        failed=$(echo "$output" | sed -n 's/.*tests, \([0-9][0-9]*\) failures.*/\1/p' | tail -n1)
        total=$(normalize_int "$total")
        failed=$(normalize_int "$failed")

        if [ "$total" -gt 0 ]; then
            pass_rate=$(awk -v t="$total" -v f="$failed" 'BEGIN{printf "%.2f", ((t-f)*100)/t}')
        elif [ "$rc" -eq 0 ]; then
            pass_rate="100"
        fi
    fi

    jq -n --arg pct "$pass_rate" --arg now "$(now_ts)" '{tool:"bats",line_coverage:($pct|tonumber),files:[],generated_at:($now|tonumber),note:"pass_rate_fallback"}'
}

collect_package_script_fallback() {
    jq -n --arg now "$(now_ts)" '{tool:"package_script",line_coverage:0,files:[],generated_at:($now|tonumber),error:"coverage_collection_not_supported"}'
}

collect_single_package_coverage() {
    local project_dir="$1" tool="$2"
    case "$tool" in
        jest)
            collect_istanbul_coverage "$project_dir" "jest"
            ;;
        vitest)
            collect_istanbul_coverage "$project_dir" "vitest"
            ;;
        node_test)
            collect_node_test_coverage "$project_dir"
            ;;
        junit)
            collect_junit_coverage "$project_dir"
            ;;
        bats)
            collect_bats_coverage "$project_dir"
            ;;
        package_script)
            collect_package_script_fallback
            ;;
        *)
            jq -n --arg now "$(now_ts)" '{tool:"unknown",line_coverage:0,files:[],generated_at:($now|tonumber),error:"framework_unknown"}'
            ;;
    esac
}

collect_monorepo_coverage() {
    local project_dir="$1"
    local packages_json tmp_jsonl
    packages_json=$(list_test_packages "$project_dir")
    tmp_jsonl=$(mktemp /tmp/autopilot-coverage-packages.XXXXXX)

    while IFS= read -r package_item; do
        [ -n "$package_item" ] || continue
        local package_dir relative_dir name framework package_json
        package_dir=$(echo "$package_item" | jq -r '.dir')
        relative_dir=$(echo "$package_item" | jq -r '.relative_dir')
        name=$(echo "$package_item" | jq -r '.name')
        framework=$(echo "$package_item" | jq -r '.framework')
        package_json=$(collect_single_package_coverage "$package_dir" "$framework")
        echo "$package_json" | jq -c \
            --arg name "$name" \
            --arg dir "$package_dir" \
            --arg relative_dir "$relative_dir" \
            --arg framework "$framework" \
            '
            .name=$name
            | .dir=$dir
            | .relative_dir=$relative_dir
            | .tool=($framework // .tool)
            | .files |= map(
                if ($relative_dir == "." or $relative_dir == "") then
                    .
                else
                    .path = ($relative_dir + "/" + .path)
                end
            )
        ' >> "$tmp_jsonl"
    done < <(echo "$packages_json" | jq -c '.packages[]?')

    python3 - "$tmp_jsonl" "$(now_ts)" <<'PYEOF'
import json
import sys
from pathlib import Path

jsonl_path = Path(sys.argv[1])
generated_at = int(sys.argv[2])

packages = []
files = []
weighted_covered = 0.0
weighted_total = 0.0
fallback_coverages = []

for raw in jsonl_path.read_text(encoding="utf-8", errors="ignore").splitlines():
    raw = raw.strip()
    if not raw:
        continue
    package = json.loads(raw)
    packages.append(package)
    files.extend(package.get("files", []))

    line_total = package.get("line_total")
    line_covered = package.get("line_covered")
    if isinstance(line_total, (int, float)) and line_total > 0 and isinstance(line_covered, (int, float)):
        weighted_total += float(line_total)
        weighted_covered += float(line_covered)
    else:
        try:
            fallback_coverages.append(float(package.get("line_coverage") or 0))
        except Exception:
            pass

if weighted_total > 0:
    line_coverage = round((weighted_covered * 100.0) / weighted_total, 2)
else:
    line_coverage = round(sum(fallback_coverages) / len(fallback_coverages), 2) if fallback_coverages else 0.0

result = {
    "tool": "monorepo",
    "monorepo": True,
    "package_count": len(packages),
    "packages": packages,
    "line_coverage": line_coverage,
    "files": sorted(files, key=lambda item: (float(item.get("line_pct") or 0), item.get("path") or "")),
    "generated_at": generated_at,
}

if weighted_total > 0:
    result["line_total"] = int(weighted_total)
    result["line_covered"] = int(weighted_covered)
    result["line_missed"] = int(max(weighted_total - weighted_covered, 0))

print(json.dumps(result, ensure_ascii=False))
PYEOF
    rm -f "$tmp_jsonl"
}

collect_single_root_coverage() {
    local project_dir="$1"
    local inspected package_item framework name relative_dir package_json
    inspected=$(list_test_packages "$project_dir")
    package_item=$(echo "$inspected" | jq -c '.packages[0] // empty')
    if [ -z "$package_item" ]; then
        jq -n --arg now "$(now_ts)" '{tool:"unknown",monorepo:false,package_count:0,packages:[],line_coverage:0,files:[],generated_at:($now|tonumber),error:"no_test_packages"}'
        return 0
    fi

    framework=$(echo "$package_item" | jq -r '.framework // "unknown"')
    name=$(echo "$package_item" | jq -r '.name // "project"')
    relative_dir=$(echo "$package_item" | jq -r '.relative_dir // "."')
    package_json=$(collect_single_package_coverage "$project_dir" "$framework")
    echo "$package_json" | jq \
        --arg name "$name" \
        --arg dir "$project_dir" \
        --arg relative_dir "$relative_dir" \
        --arg framework "$framework" \
        --arg now "$(now_ts)" \
        '
        .monorepo=false
        | .package_count=1
        | .packages=[
            {
                name:$name,
                dir:$dir,
                relative_dir:$relative_dir,
                tool:$framework,
                line_coverage:.line_coverage,
                line_covered:(.line_covered // null),
                line_total:(.line_total // null),
                line_missed:(.line_missed // null),
                files:.files,
                generated_at:.generated_at,
                error:(.error // null)
            }
        ]
        | .generated_at=($now|tonumber)
    '
}

collect_coverage() {
    local project_dir="$1"
    if [ "$(detect_monorepo "$project_dir")" = "true" ]; then
        collect_monorepo_coverage "$project_dir"
        return 0
    fi
    collect_single_root_coverage "$project_dir"
}

usage() {
    cat <<'USAGE'
用法:
  coverage-collect.sh detect <project_dir>
  coverage-collect.sh monorepo <project_dir>
  coverage-collect.sh packages <project_dir>
  coverage-collect.sh collect <project_dir>
USAGE
}

main() {
    local cmd="${1:-}"
    case "$cmd" in
        detect)
            local project_dir="${2:-}"
            [ -n "$project_dir" ] || { usage; exit 1; }
            detect_framework "$project_dir"
            ;;
        monorepo)
            local project_dir="${2:-}"
            [ -n "$project_dir" ] || { usage; exit 1; }
            detect_monorepo "$project_dir"
            ;;
        packages)
            local project_dir="${2:-}"
            [ -n "$project_dir" ] || { usage; exit 1; }
            list_test_packages "$project_dir"
            ;;
        collect)
            local project_dir="${2:-}"
            [ -n "$project_dir" ] || { usage; exit 1; }
            collect_coverage "$project_dir"
            ;;
        *)
            usage
            exit 1
            ;;
    esac
}

main "$@"
