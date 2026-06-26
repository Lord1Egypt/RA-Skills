#!/usr/bin/env bash
# pages-deploy: Manage Pages projects (view, preview, domains, offline, etc.)

set -euo pipefail

# Auto-find nest CLI
find_nest() {
    if command -v nest &>/dev/null; then echo "nest"; return; fi
    local paths=(
        "$HOME/.nest-cli/node_modules/.bin/nest"
        "/home/gem/tmp/nest-cli/node_modules/.bin/nest"
    )
    for p in "${paths[@]}"; do
        [[ -x "$p" ]] && echo "$p" && return
    done
    echo "Error: nest CLI not found. Run deploy.sh first to install." >&2
    exit 1
}

NEST=$(find_nest)

usage() {
    cat <<EOF
Usage: bash manage.sh <command> [options]

Commands:
  list                      List all Pages projects
  get       --pages p-xxx   Show project details
  deployments --pages p-xxx Show deployment history
  serve     --dir ./dist    Start local preview server
  domain-list   --pages p-xxx   List domains
  domain-add    --pages p-xxx --domain xxx   Bind domain
  domain-verify --pages p-xxx --domain xxx   Verify domain
  domain-del    --pages p-xxx --domain xxx   Unbind domain
  offline   --pages p-xxx   Offline project
  delete    --pages p-xxx   Delete project
EOF
    exit 0
}

[[ $# -eq 0 ]] && usage

CMD="$1"; shift
PAGES=""
DIR=""
DOMAIN=""
PORT="8080"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --pages|-p)  PAGES="$2"; shift 2;;
        --dir)       DIR="$2"; shift 2;;
        --domain)    DOMAIN="$2"; shift 2;;
        --port)      PORT="$2"; shift 2;;
        -h|--help)   usage;;
        *)           echo "Unknown: $1"; shift;;
    esac
done

case "$CMD" in
    list)
        $NEST pages list
        ;;
    get)
        [[ -z "$PAGES" ]] && { echo "Error: --pages required"; exit 1; }
        $NEST pages get -p "$PAGES"
        ;;
    deployments)
        [[ -z "$PAGES" ]] && { echo "Error: --pages required"; exit 1; }
        $NEST pages list deployment --pages "$PAGES"
        ;;
    serve)
        [[ -z "$DIR" ]] && { echo "Error: --dir required"; exit 1; }
        echo "Starting local server at http://localhost:$PORT"
        $NEST pages serve "$DIR" --addr ":$PORT"
        ;;
    domain-list)
        [[ -z "$PAGES" ]] && { echo "Error: --pages required"; exit 1; }
        $NEST pages domain list --pages "$PAGES"
        ;;
    domain-add)
        [[ -z "$PAGES" || -z "$DOMAIN" ]] && { echo "Error: --pages and --domain required"; exit 1; }
        $NEST pages domain add --pages "$PAGES" --domain "$DOMAIN"
        echo "Domain added. Please configure CNAME at your DNS provider, then run:"
        echo "  bash manage.sh domain-verify --pages $PAGES --domain $DOMAIN"
        ;;
    domain-verify)
        [[ -z "$PAGES" || -z "$DOMAIN" ]] && { echo "Error: --pages and --domain required"; exit 1; }
        $NEST pages domain verify --pages "$PAGES" --domain "$DOMAIN"
        ;;
    domain-del)
        [[ -z "$PAGES" || -z "$DOMAIN" ]] && { echo "Error: --pages and --domain required"; exit 1; }
        $NEST pages domain delete --pages "$PAGES" --domain "$DOMAIN"
        ;;
    offline)
        [[ -z "$PAGES" ]] && { echo "Error: --pages required"; exit 1; }
        $NEST pages offline --pages "$PAGES"
        ;;
    delete)
        [[ -z "$PAGES" ]] && { echo "Error: --pages required"; exit 1; }
        read -p "Are you sure you want to delete $PAGES? [y/N] " confirm
        [[ "$confirm" =~ ^[yY] ]] && $NEST pages delete --pages "$PAGES" || echo "Cancelled"
        ;;
    *)
        echo "Unknown command: $CMD"
        usage
        ;;
esac
