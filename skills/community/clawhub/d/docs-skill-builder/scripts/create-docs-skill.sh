#!/bin/bash
set -e

# Create a Hindsight-docs-style documentation skill source folder.
# The generated source folder contains:
#   scripts/generate-docs-skill.sh
#   skills/<skill-name>/SKILL.md
#   skills/<skill-name>/references/
#
# The agent must map the target repo docs layout first and pass explicit
# --doc-path values. This script does not guess the documentation scope.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
TEMPLATE="$SKILL_ROOT/templates/generate-docs-skill.sh.tmpl"

NAME=""
TOOL_NAME=""
SOURCE_URL=""
OUTPUT=""
DOC_PATHS=()

usage() {
    cat >&2 <<'EOF'
Usage:
  create-docs-skill.sh \
    --name <skill-name> \
    --tool-name <tool-name> \
    --source-url <git-repo-url> \
    --output <source-folder> \
    --doc-path <repo-path> [--doc-path <repo-path> ...]
EOF
    exit 2
}

slug() {
    printf '%s' "$1" \
        | tr '[:upper:]' '[:lower:]' \
        | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//'
}

write_file() {
    local path="$1"
    local content="$2"
    mkdir -p "$(dirname "$path")"
    printf '%s' "$content" > "$path"
}

while [ $# -gt 0 ]; do
    case "$1" in
        --name)
            [ -z "${2:-}" ] && usage
            NAME="$2"
            shift 2
            ;;
        --tool-name)
            [ -z "${2:-}" ] && usage
            TOOL_NAME="$2"
            shift 2
            ;;
        --source-url)
            [ -z "${2:-}" ] && usage
            SOURCE_URL="$2"
            shift 2
            ;;
        --output)
            [ -z "${2:-}" ] && usage
            OUTPUT="$2"
            shift 2
            ;;
        --doc-path)
            [ -z "${2:-}" ] && usage
            DOC_PATHS+=("$2")
            shift 2
            ;;
        *)
            usage
            ;;
    esac
done

[ -z "$NAME" ] && usage
[ -z "$TOOL_NAME" ] && usage
[ -z "$SOURCE_URL" ] && usage
[ -z "$OUTPUT" ] && usage
[ "${#DOC_PATHS[@]}" -eq 0 ] && usage
[ -f "$TEMPLATE" ] || { echo "missing template: $TEMPLATE" >&2; exit 1; }

SKILL_NAME="$(slug "$NAME")"
[ -z "$SKILL_NAME" ] && { echo "invalid --name" >&2; exit 1; }

case "$SOURCE_URL" in
    web+https://*|web+http://*|*.git|*github.com/*|git@*) ;;
    *) echo "source_url_must_be_git_repo_or_web_source" >&2; exit 1 ;;
esac

OUTPUT_DIR="$(cd "$(dirname "$OUTPUT")" && pwd)/$(basename "$OUTPUT")"
if [ -e "$OUTPUT_DIR" ] && [ "$(find "$OUTPUT_DIR" -mindepth 1 -maxdepth 1 2>/dev/null | wc -l | tr -d ' ')" != "0" ]; then
    echo "refusing to overwrite non-empty directory: $OUTPUT_DIR" >&2
    exit 1
fi

GENERATOR="$(python3 - "$TEMPLATE" "$SKILL_NAME" "$TOOL_NAME" "$SOURCE_URL" "${DOC_PATHS[@]}" <<'PY'
import re
import shlex
import sys
from pathlib import Path

template, skill, tool, source, *paths = sys.argv[1:]
values = {
    '__SKILL_NAME_SHELL__': shlex.quote(skill),
    '__TOOL_NAME_SHELL__': shlex.quote(tool),
    '__SOURCE_URL_SHELL__': shlex.quote(source),
    '__DOC_PATHS_SHELL__': ' '.join(shlex.quote(path) for path in paths),
}
pattern = '|'.join(re.escape(token) for token in values)
rendered = re.sub(pattern, lambda match: values[match.group()], Path(template).read_text(encoding='utf-8'))
sys.stdout.buffer.write(rendered.encode('utf-8'))
PY
)"

README="# $TOOL_NAME Docs Skill Source

Hindsight-docs-style source folder for generating \`$SKILL_NAME\` from:

\`\`\`text
$SOURCE_URL
\`\`\`

## Generate / Update

\`\`\`bash
./scripts/generate-docs-skill.sh
\`\`\`

## Install in Codex

After generation, install the generated skill directory with the Codex native
skill installer or copy \`skills/$SKILL_NAME\` into:

\`\`\`text
\$HOME/.codex/skills/$SKILL_NAME
\`\`\`
"

PLACEHOLDER="# $TOOL_NAME Documentation Skill

Run \`./scripts/generate-docs-skill.sh\`.
"

write_file "$OUTPUT_DIR/README.md" "$README"
write_file "$OUTPUT_DIR/scripts/generate-docs-skill.sh" "$GENERATOR"
chmod +x "$OUTPUT_DIR/scripts/generate-docs-skill.sh"
write_file "$OUTPUT_DIR/skills/$SKILL_NAME/SKILL.md" "$PLACEHOLDER"

echo "$OUTPUT_DIR"
