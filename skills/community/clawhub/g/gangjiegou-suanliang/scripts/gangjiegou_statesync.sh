#!/usr/bin/env bash
# 钢结构算量 -> lis-skill-bus 强制契约接线（薄壳，逻辑在 gangjiegou_statesync.py）。
# 正式识图链路缺 bus 时退出码 2，不降级为本地识图。
# 用法：`bash gangjiegou_statesync.sh push|pull --project 项目 ...`，见对应 .py --help。
# 运行时解析（Python / 底座 / vendor）见 scripts/runtime_env.sh
set -uo pipefail
_HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "$_HERE/runtime_env.sh"
exec "${PYTHON_BIN}" "$_HERE/gangjiegou_statesync.py" "$@"
