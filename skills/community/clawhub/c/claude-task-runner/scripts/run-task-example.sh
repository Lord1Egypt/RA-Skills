#!/usr/bin/env bash
set -euo pipefail

RUNNER="/Users/zhengweidong/.openclaw/workspace/scripts/cc-task-runner.sh"
SCHEMA="$(cd "$(dirname "$0")/.." && pwd)/references/task-schema-example.json"

bash "$RUNNER" run \
  "example-task" \
  "GLM-5.1" \
  "/tmp" \
  --json-schema-file "$SCHEMA" \
  --expect-file "/tmp/example-task.txt" \
  --expect-contains "runner ok" \
  -- "Use Bash to create /tmp/example-task.txt with content: runner ok. Then return structured success output."
