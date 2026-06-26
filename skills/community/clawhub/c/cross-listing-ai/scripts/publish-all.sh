#!/usr/bin/env bash
set -euo pipefail

main() {
  local script_dir

  script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

  "$script_dir/publish-clawhub.sh" "$@"
  "$script_dir/publish-skills.sh"
}

main "$@"
