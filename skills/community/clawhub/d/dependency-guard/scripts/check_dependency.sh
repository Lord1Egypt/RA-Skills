#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  check_dependency.sh <ecosystem> <package> [version] [--mode deep|shallow] [--output <path>]

Examples:
  check_dependency.sh npm zod
  check_dependency.sh npm react 19.1.0 --mode deep
  check_dependency.sh pypi requests 2.32.3 --output tmp/socket-report.md

This helper produces a Socket CLI markdown report artifact for agent review.
Interpret the result with references/decision-matrix.md.

Authentication:
  - Preferred: Socket MCP `depscore`
  - CLI fallback: `socket login`
  - If your installed CLI supports it, submitting a blank token may enable limited public access
  - Users with a private Socket token can also set SOCKET_SECURITY_API_TOKEN
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -lt 2 ]]; then
  usage >&2
  exit 64
fi

ecosystem="$1"
package="$2"
version=""
mode="deep"
output=""

shift 2

if [[ $# -gt 0 && "${1:-}" != --* ]]; then
  version="$1"
  shift
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      mode="${2:-}"
      shift 2
      ;;
    --output)
      output="${2:-}"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 64
      ;;
  esac
done

if [[ "$mode" != "deep" && "$mode" != "shallow" ]]; then
  echo "Invalid mode: $mode" >&2
  exit 64
fi

if ! command -v socket >/dev/null 2>&1; then
  echo "Socket CLI not found. Install it first: npm install -g socket" >&2
  exit 69
fi

target="$package"
purl="pkg:${ecosystem}/${package}"
if [[ -n "$version" ]]; then
  target="${package}@${version}"
  purl="${purl}@${version}"
fi

if [[ -z "$output" ]]; then
  mkdir -p tmp/socket-reports
  safe_name="${package//\//_}"
  output="tmp/socket-reports/${safe_name}-${mode}.md"
fi

mkdir -p "$(dirname "$output")"

if ! socket package "$mode" "$ecosystem" "$target" --markdown >"$output"; then
  rm -f "$output"
  echo "Socket package lookup failed. Authenticate with \`socket login\` or set SOCKET_SECURITY_API_TOKEN. If your Socket CLI supports blank-submit login, that may enable limited public access." >&2
  exit 70
fi

cat <<EOF
status=report_generated
tool=socket-cli
mode=$mode
purl=$purl
report=$output
next_step=apply references/decision-matrix.md to the generated report before changing manifests or lockfiles
EOF
