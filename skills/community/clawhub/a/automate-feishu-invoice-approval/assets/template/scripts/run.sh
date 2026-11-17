#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$(cd -- "${script_dir}/.." && pwd)"
export PYTHONPATH="${project_dir}/src"
exec python3 -m invoice_approval_bot.cli run
