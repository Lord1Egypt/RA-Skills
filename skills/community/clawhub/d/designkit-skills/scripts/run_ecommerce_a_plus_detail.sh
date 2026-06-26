#!/usr/bin/env bash
# A+详情页 webapi 执行入口
# 用法:
#   bash run_ecommerce_a_plus_detail.sh detail_plan_submit --input-json '{"images":["..."],"product_info":"..."}'
#   bash run_ecommerce_a_plus_detail.sh detail_plan_poll --input-json '{"task_id":"..."}'
#   bash run_ecommerce_a_plus_detail.sh detail_render_submit --input-json '{"images":["..."],"modules":[...],"product_info":"..."}'
#   bash run_ecommerce_a_plus_detail.sh detail_render_regen --input-json '{"task_id":"..."}'
#   bash run_ecommerce_a_plus_detail.sh detail_render_poll --input-json '{"batch_id":"..."}'
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/ecommerce_a_plus_detail.py" "$@"
