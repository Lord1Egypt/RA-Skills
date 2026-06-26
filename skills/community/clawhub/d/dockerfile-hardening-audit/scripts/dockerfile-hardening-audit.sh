#!/usr/bin/env bash
set -euo pipefail

DOCKERFILE_GLOB="${DOCKERFILE_GLOB:-**/Dockerfile*}"
TOP_N="${TOP_N:-20}"
OUTPUT_FORMAT="${OUTPUT_FORMAT:-text}"
WARN_SCORE="${WARN_SCORE:-3}"
CRITICAL_SCORE="${CRITICAL_SCORE:-6}"
REQUIRE_NON_ROOT_USER="${REQUIRE_NON_ROOT_USER:-1}"
REQUIRE_HEALTHCHECK="${REQUIRE_HEALTHCHECK:-1}"
FLAG_FLOATING_TAGS="${FLAG_FLOATING_TAGS:-1}"
FLAG_UNPINNED_IMAGES="${FLAG_UNPINNED_IMAGES:-1}"
FLAG_ADD_INSTRUCTIONS="${FLAG_ADD_INSTRUCTIONS:-1}"
FLAG_REMOTE_SCRIPT_PIPE="${FLAG_REMOTE_SCRIPT_PIPE:-1}"
FILE_MATCH="${FILE_MATCH:-}"
FILE_EXCLUDE="${FILE_EXCLUDE:-}"
FAIL_ON_CRITICAL="${FAIL_ON_CRITICAL:-0}"

if [[ "$OUTPUT_FORMAT" != "text" && "$OUTPUT_FORMAT" != "json" ]]; then
  echo "ERROR: OUTPUT_FORMAT must be 'text' or 'json' (got: $OUTPUT_FORMAT)" >&2
  exit 1
fi

for value_name in TOP_N WARN_SCORE CRITICAL_SCORE REQUIRE_NON_ROOT_USER REQUIRE_HEALTHCHECK FLAG_FLOATING_TAGS FLAG_UNPINNED_IMAGES FLAG_ADD_INSTRUCTIONS FLAG_REMOTE_SCRIPT_PIPE FAIL_ON_CRITICAL; do
  value="${!value_name}"
  if ! [[ "$value" =~ ^[0-9]+$ ]]; then
    echo "ERROR: $value_name must be a non-negative integer (got: $value)" >&2
    exit 1
  fi
done

if [[ "$TOP_N" -eq 0 ]]; then
  echo "ERROR: TOP_N must be >= 1" >&2
  exit 1
fi

if [[ "$WARN_SCORE" -gt "$CRITICAL_SCORE" ]]; then
  echo "ERROR: WARN_SCORE must be <= CRITICAL_SCORE" >&2
  exit 1
fi

python3 - "$DOCKERFILE_GLOB" "$TOP_N" "$OUTPUT_FORMAT" "$WARN_SCORE" "$CRITICAL_SCORE" "$REQUIRE_NON_ROOT_USER" "$REQUIRE_HEALTHCHECK" "$FLAG_FLOATING_TAGS" "$FLAG_UNPINNED_IMAGES" "$FLAG_ADD_INSTRUCTIONS" "$FLAG_REMOTE_SCRIPT_PIPE" "$FILE_MATCH" "$FILE_EXCLUDE" "$FAIL_ON_CRITICAL" <<'PY'
import glob
import json
import re
import sys
from pathlib import Path

(
    dockerfile_glob,
    top_n_raw,
    output_format,
    warn_score_raw,
    critical_score_raw,
    require_non_root_user_raw,
    require_healthcheck_raw,
    flag_floating_tags_raw,
    flag_unpinned_images_raw,
    flag_add_instructions_raw,
    flag_remote_script_pipe_raw,
    file_match_raw,
    file_exclude_raw,
    fail_on_critical_raw,
) = sys.argv[1:]

top_n = int(top_n_raw)
warn_score = int(warn_score_raw)
critical_score = int(critical_score_raw)
require_non_root_user = require_non_root_user_raw == '1'
require_healthcheck = require_healthcheck_raw == '1'
flag_floating_tags = flag_floating_tags_raw == '1'
flag_unpinned_images = flag_unpinned_images_raw == '1'
flag_add_instructions = flag_add_instructions_raw == '1'
flag_remote_script_pipe = flag_remote_script_pipe_raw == '1'
fail_on_critical = fail_on_critical_raw == '1'

file_match = None
if file_match_raw:
    try:
        file_match = re.compile(file_match_raw)
    except re.error as exc:
        print(f"ERROR: invalid FILE_MATCH {file_match_raw!r}: {exc}", file=sys.stderr)
        sys.exit(1)

file_exclude = None
if file_exclude_raw:
    try:
        file_exclude = re.compile(file_exclude_raw)
    except re.error as exc:
        print(f"ERROR: invalid FILE_EXCLUDE {file_exclude_raw!r}: {exc}", file=sys.stderr)
        sys.exit(1)

files = sorted(glob.glob(dockerfile_glob, recursive=True))
if not files:
    print(f"ERROR: no files matched DOCKERFILE_GLOB={dockerfile_glob}", file=sys.stderr)
    sys.exit(1)

if file_match:
    files = [path for path in files if file_match.search(path)]

if file_exclude:
    files = [path for path in files if not file_exclude.search(path)]

if not files:
    print(
        "ERROR: no files left after FILE_MATCH/FILE_EXCLUDE filtering "
        f"(match={file_match_raw or '<none>'}, exclude={file_exclude_raw or '<none>'})",
        file=sys.stderr,
    )
    sys.exit(1)

from_re = re.compile(r"^\s*FROM\s+([^\s]+)", re.IGNORECASE)
user_re = re.compile(r"^\s*USER\s+([^#\s]+)", re.IGNORECASE)
healthcheck_re = re.compile(r"^\s*HEALTHCHECK\b", re.IGNORECASE)
add_re = re.compile(r"^\s*ADD\s+", re.IGNORECASE)
remote_pipe_re = re.compile(r"\b(?:curl|wget)\b[^\n|]*\|\s*(?:bash|sh)\b", re.IGNORECASE)

def classify_image_ref(image_ref: str):
    if image_ref.lower() == 'scratch':
        return {'floating': False, 'unpinned': False, 'tag': None}

    if '@sha256:' in image_ref.lower():
        return {'floating': False, 'unpinned': False, 'tag': None}

    leaf = image_ref.split('/')[-1]
    tag = None
    if ':' in leaf:
        tag = leaf.rsplit(':', 1)[1].strip().lower()

    unpinned = tag is None
    floating = tag in {'latest', 'main', 'master', 'edge'} if tag else False
    return {'floating': floating, 'unpinned': unpinned, 'tag': tag}

rows = []
parse_errors = []

for file_path in files:
    try:
        text = Path(file_path).read_text(encoding='utf-8')
    except Exception as exc:
        parse_errors.append(f"{file_path}: {exc}")
        continue

    lines = text.splitlines()
    from_images = []
    floating_from = []
    unpinned_from = []
    add_lines = []
    remote_pipe_lines = []
    user_declared = None
    user_line = None
    has_healthcheck = False

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        from_match = from_re.match(line)
        if from_match:
            image_ref = from_match.group(1)
            from_images.append({'line': idx, 'image': image_ref})
            classification = classify_image_ref(image_ref)
            if flag_floating_tags and classification['floating']:
                floating_from.append({'line': idx, 'image': image_ref, 'tag': classification['tag']})
            if flag_unpinned_images and classification['unpinned']:
                unpinned_from.append({'line': idx, 'image': image_ref})

        user_match = user_re.match(line)
        if user_match:
            user_declared = user_match.group(1).strip()
            user_line = idx

        if healthcheck_re.match(line):
            has_healthcheck = True

        if flag_add_instructions and add_re.match(line):
            add_lines.append({'line': idx, 'instruction': stripped})

        if flag_remote_script_pipe and remote_pipe_re.search(line):
            remote_pipe_lines.append({'line': idx, 'instruction': stripped})

    user_is_root = False
    missing_non_root_user = False
    if require_non_root_user:
        if user_declared is None:
            missing_non_root_user = True
        else:
            normalized = user_declared.strip().lower()
            user_is_root = normalized in {'root', '0', '0:0', 'root:root'}

    missing_healthcheck = require_healthcheck and not has_healthcheck

    score = 0
    score += 3 if (missing_non_root_user or user_is_root) else 0
    score += 2 if missing_healthcheck else 0
    score += len(floating_from) * 2
    score += len(unpinned_from) * 1
    score += len(add_lines) * 1
    score += len(remote_pipe_lines) * 2

    severity = 'ok'
    if score >= critical_score:
        severity = 'critical'
    elif score >= warn_score:
        severity = 'warn'

    rows.append(
        {
            'dockerfile': file_path,
            'severity': severity,
            'score': score,
            'from_images': from_images,
            'floating_from_images': floating_from,
            'unpinned_from_images': unpinned_from,
            'missing_non_root_user': missing_non_root_user,
            'user_is_root': user_is_root,
            'user_declared': user_declared,
            'user_line': user_line,
            'missing_healthcheck': missing_healthcheck,
            'add_instructions': add_lines,
            'remote_script_pipe': remote_pipe_lines,
        }
    )

rows.sort(key=lambda row: (-row['score'], row['dockerfile']))
critical_rows = [row for row in rows if row['severity'] == 'critical']

summary = {
    'files_scanned': len(files),
    'files_evaluated': len(rows),
    'parse_errors': parse_errors,
    'critical_dockerfiles': len(critical_rows),
    'warn_dockerfiles': len([row for row in rows if row['severity'] == 'warn']),
    'ok_dockerfiles': len([row for row in rows if row['severity'] == 'ok']),
    'warn_score': warn_score,
    'critical_score': critical_score,
    'checks': {
        'require_non_root_user': require_non_root_user,
        'require_healthcheck': require_healthcheck,
        'flag_floating_tags': flag_floating_tags,
        'flag_unpinned_images': flag_unpinned_images,
        'flag_add_instructions': flag_add_instructions,
        'flag_remote_script_pipe': flag_remote_script_pipe,
        'file_match': file_match_raw or None,
        'file_exclude': file_exclude_raw or None,
    },
}

if output_format == 'json':
    print(json.dumps({'summary': summary, 'dockerfiles': rows[:top_n], 'all_dockerfiles': rows, 'critical_dockerfiles': critical_rows}, indent=2, sort_keys=True))
else:
    print('DOCKERFILE HARDENING AUDIT')
    print('---')
    print(
        'SUMMARY: '
        f"files={summary['files_scanned']} evaluated={summary['files_evaluated']} "
        f"critical={summary['critical_dockerfiles']} warn={summary['warn_dockerfiles']} ok={summary['ok_dockerfiles']}"
    )
    if parse_errors:
        print('PARSE_ERRORS:')
        for err in parse_errors:
            print(f'- {err}')
    print('---')
    print(f"TOP DOCKERFILES ({min(top_n, len(rows))})")
    if not rows:
        print('none')
    else:
        for row in rows[:top_n]:
            user_display = row['user_declared'] if row['user_declared'] is not None else '<missing>'
            print(
                f"- [{row['severity']}] file={row['dockerfile']} score={row['score']} "
                f"from={len(row['from_images'])} floating={len(row['floating_from_images'])} "
                f"unpinned={len(row['unpinned_from_images'])} user={user_display} "
                f"healthcheck_missing={int(row['missing_healthcheck'])} add={len(row['add_instructions'])} "
                f"remote_pipe={len(row['remote_script_pipe'])}"
            )

sys.exit(1 if (fail_on_critical and critical_rows) else 0)
PY
