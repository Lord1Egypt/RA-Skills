#!/usr/bin/env bash
# run_command.sh - Run a shell command inside the E2B Desktop sandbox
# Usage: run_command.sh "command"

set -e

CMD="${1:?Usage: run_command.sh \"command\"}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python3 - <<PYEOF
import os, sys
exec(open("$SCRIPT_DIR/_connect.py").read())

result = desktop.commands.run("""$CMD""")
if hasattr(result, 'stdout') and result.stdout:
    print(result.stdout, end="")
if hasattr(result, 'stderr') and result.stderr:
    print(result.stderr, end="", file=sys.stderr)
if hasattr(result, 'exit_code'):
    sys.exit(result.exit_code)
PYEOF
