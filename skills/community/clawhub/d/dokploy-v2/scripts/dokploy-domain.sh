#!/bin/bash
# Dokploy Domain Management

# Source helper functions
source "$(dirname "$0")/dokploy.sh"

# Colors (redirect log_info to stderr)
log_info() { echo -e "\033[0;34m[INFO]\033[0m $1" >&2; }
log_success() { echo -e "\033[0;32m[SUCCESS]\033[0m $1"; }
log_error() { echo -e "\033[0;31m[ERROR]\033[0m $1" >&2; }
log_warn() { echo -e "\033[1;33m[WARN]\033[0m $1" >&2; }

main() {
case "$1" in
    list)
        local appId=""

        shift
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --application|--app)
                    appId="$2"
                    shift 2
                    ;;
                *)
                    ;;
            esac
        done

        if [ -z "$appId" ]; then
            log_error "Usage: dokploy domain list --app <app-id>"
            exit 1
        fi

        log_info "Fetching domains for application $appId..."

        # New API uses dedicated endpoints
        local response=$(api_request "GET" "/domain.byApplicationId?applicationId=$appId")

        echo "$response" | jq -r ".[] | \"ID: \(.domainId)\n  Domain: \(.host)\n  App: \(.applicationId)\n  Path: \(.path)\n  Port: \(.port)\n  HTTPS: \(.https)\"" 2>/dev/null || log_error "Failed to fetch domains"
        ;;
    get)
        if [ -z "$2" ]; then
            log_error "Usage: dokploy domain get <domain-id>"
            exit 1
        fi
        log_info "Fetching domain $2..."
        local response=$(api_request "GET" "/domain.one?domainId=$2")
        echo "$response" | jq '.' 2>/dev/null || log_error "Failed to fetch domain"
        ;;
    create)
        local appId=""
        local host=""
        local path="/"
        local port=80
        local https="true"

        shift
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --application|--app)
                    appId="$2"
                    shift 2
                    ;;
                --host|--domain)
                    host="$2"
                    shift 2
                    ;;
                --path)
                    path="$2"
                    shift 2
                    ;;
                --port)
                    port="$2"
                    shift 2
                    ;;
                --no-https)
                    https="false"
                    shift
                    ;;
                *)
                    log_error "Unknown option: $1"
                    exit 1
                    ;;
            esac
        done

        if [ -z "$appId" ] || [ -z "$host" ]; then
            log_error "Usage: dokploy domain create --app <id> --host <name> [--path <path>] [--port <port>] [--no-https]"
            exit 1
        fi

        # New API requires 'host' instead of 'domain'
        local data=$(jq -n \
            --arg applicationId "$appId" \
            --arg host "$host" \
            --arg path "$path" \
            --argjson port "$port" \
            --argjson https "$https" \
            '{
                applicationId: $applicationId,
                host: $host,
                path: $path,
                port: $port,
                https: $https
            }')

        log_info "Creating domain '$host' for application $appId..."
        local response=$(api_request "POST" "/domain.create" "$data")
        local domainId=$(echo "$response" | jq -r '.domainId')

        if [ -n "$domainId" ] && [ "$domainId" != "null" ]; then
            log_success "Domain created with ID: $domainId"
        else
            log_error "Failed to create domain"
            echo "$response" | jq '.' 2>/dev/null || echo "$response"
            exit 1
        fi
        ;;
    update)
        if [ -z "$2" ]; then
            log_error "Usage: dokploy domain update <domain-id> --host <name> [--path <path>] [--port <port>]"
            exit 1
        fi

        local domainId="$2"
        local host=""
        local path=""
        local port=""
        local https=""

        shift 2
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --host|--domain)
                    host="$2"
                    shift 2
                    ;;
                --path)
                    path="$2"
                    shift 2
                    ;;
                --port)
                    port="$2"
                    shift 2
                    ;;
                --https)
                    https="$2"
                    shift 2
                    ;;
                --no-https)
                    https="false"
                    shift
                    ;;
                *)
                    ;;
            esac
        done

        # Build update data, new API uses POST to /domain.update
        local data=$(jq -n --arg domainId "$domainId" '{domainId: $domainId}')

        if [ -n "$host" ]; then
            data=$(echo "$data" | jq --arg host "$host" '. + {host: $host}')
        fi
        if [ -n "$path" ]; then
            data=$(echo "$data" | jq --arg path "$path" '. + {path: $path}')
        fi
        if [ -n "$port" ]; then
            data=$(echo "$data" | jq --argjson port "$port" '. + {port: $port}')
        fi
        if [ -n "$https" ]; then
            data=$(echo "$data" | jq --argjson https "$https" '. + {https: $https}')
        fi

        log_info "Updating domain $domainId..."
        local response=$(api_request "POST" "/domain.update" "$data")

        if echo "$response" | jq -e '.domainId' > /dev/null 2>&1; then
            log_success "Domain updated"
        else
            log_error "Failed to update domain"
            echo "$response"
            exit 1
        fi
        ;;
    delete)
        if [ -z "$2" ]; then
            log_error "Usage: dokploy domain delete <domain-id>"
            exit 1
        fi

        log_warn "Are you sure you want to delete domain $2?"
        read -p "Type 'yes' to confirm: " confirm

        if [ "$confirm" != "yes" ]; then
            log_info "Cancelled"
            exit 0
        fi

        log_info "Deleting domain $2..."
        # New API uses POST to /domain.delete with body
        local data=$(jq -n --arg domainId "$2" '{domainId: $domainId}')
        local response=$(api_request "POST" "/domain.delete" "$data")

        if echo "$response" | jq -e 'true' > /dev/null 2>&1; then
            log_success "Domain deleted"
        else
            if echo "$response" | jq -e '.domainId' > /dev/null 2>&1; then
                 log_success "Domain deleted"
            else
                 log_error "Failed to delete domain"
                 echo "$response"
                 exit 1
            fi
        fi
        ;;
    *)
        echo "Usage: dokploy domain <command>"
        echo ""
        echo "Commands:"
        echo "  list --app <id>            List domains"
        echo "  get <domain-id>             Get domain details"
        echo "  create --app <id> ...       Create domain"
        echo "  update <id> --host <name>   Update domain"
        echo "  delete <domain-id>           Delete domain"
        echo ""
        echo "Create options:"
        echo "  --application <id>   Application ID (required)"
        echo "  --host <name>        Domain name (required)"
        echo "  --path <path>       Path (default: /)"
        echo "  --port <port>       Port (default: 80)"
        echo "  --no-https          Disable HTTPS"
        ;;
esac
}

# Only run main if script is executed directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi