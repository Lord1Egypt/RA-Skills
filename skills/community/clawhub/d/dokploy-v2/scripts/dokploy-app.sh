#!/bin/bash
# Dokploy Application Management

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
        local projectId=""
        shift
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --project)
                    projectId="$2"
                    shift 2
                    ;;
                *)
                    ;;
            esac
        done

        if [ -z "$projectId" ]; then
            log_error "Usage: dokploy app list --project <project-id>"
            exit 1
        fi

        log_info "Fetching applications for project $projectId..."
        # New API uses application.search
        local response=$(api_request "GET" "/application.search?projectId=$projectId")

        echo "$response" | jq -r '
            (if type == "array" then . else .items // .data // [] end) |
            .[] |
            "ID: \(.applicationId)\n  Name: \(.name)\n  Type: \(.buildType // "N/A")\n  Project: \(.projectId)\n  Status: \(.applicationStatus // "N/A")\n  Environment: \(.environmentId)"
        ' 2>/dev/null || log_error "Failed to fetch applications"
        ;;
    get)
        if [ -z "$2" ]; then
            log_error "Usage: dokploy app get <application-id>"
            exit 1
        fi
        log_info "Fetching application $2..."
        local response=$(api_request "GET" "/application.one?applicationId=$2")
        echo "$response" | jq '.' 2>/dev/null || log_error "Failed to fetch application"
        ;;
    create)
        local environmentId=""
        local name=""
        local type="docker"
        local image=""
        local env=""

        shift
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --environment-id)
                    environmentId="$2"
                    shift 2
                    ;;
                --project)
                    log_warn "--project is deprecated for create, use --environment-id"
                    ;;
                --name)
                    name="$2"
                    shift 2
                    ;;
                --type)
                    type="$2"
                    shift 2
                    ;;
                --image)
                    image="$2"
                    shift 2
                    ;;
                --env)
                    env="$2"
                    shift 2
                    ;;
                *)
                    log_error "Unknown option: $1"
                    exit 1
                    ;;
            esac
        done

        if [ -z "$environmentId" ] || [ -z "$name" ]; then
            log_error "Usage: dokploy app create --environment-id <id> --name <name> [--type <type>] [--image <image>] [--env \"KEY=VALUE\"]"
            exit 1
        fi

        # 1. Create Application
        local createData=$(jq -n \
            --arg environmentId "$environmentId" \
            --arg name "$name" \
            '{
                environmentId: $environmentId,
                name: $name
            }')

        log_info "Creating application '$name'..."
        local response=$(api_request "POST" "/application.create" "$createData")
        local appId=$(echo "$response" | jq -r '.applicationId')

        if [ -z "$appId" ] || [ "$appId" == "null" ]; then
            log_error "Failed to create application"
            echo "$response" | jq '.' 2>/dev/null || echo "$response"
            exit 1
        fi

        log_success "Application created with ID: $appId"

        # 2. Update Application with details (image, type, env)
        local updateData=$(jq -n \
            --arg applicationId "$appId" \
            --arg buildType "$type" \
            --arg dockerImage "$image" \
            --arg env "$env" \
            '{
                applicationId: $applicationId,
                buildType: $buildType,
                dockerImage: (if $dockerImage != "" then $dockerImage else null end),
                env: (if $env != "" then $env else null end)
            }')

        if [ -n "$env" ]; then
            local formattedEnv=$(echo "$env" | tr ';' '\n')
            updateData=$(echo "$updateData" | jq --arg env "$formattedEnv" '.env = $env')
        fi

        log_info "Configuring application..."
        local updateResp=$(api_request "POST" "/application.update" "$updateData")

        if echo "$updateResp" | jq -e '.applicationId' > /dev/null 2>&1; then
             log_success "Application configured"
        else
             log_warn "Application created but configuration failed"
             echo "$updateResp"
        fi
        ;;
    deploy)
        if [ -z "$2" ]; then
            log_error "Usage: dokploy app deploy <application-id>"
            exit 1
        fi
        log_info "Triggering deployment for application $2..."
        # New API uses POST body
        local data=$(jq -n --arg applicationId "$2" '{applicationId: $applicationId}')
        local response=$(api_request "POST" "/application.deploy" "$data")

        if echo "$response" | jq -e '.deploymentId' > /dev/null 2>&1; then
            local deploymentId=$(echo "$response" | jq -r '.deploymentId')
            log_success "Deployment started with ID: $deploymentId"
            log_info "Check status with: dokploy app deployments $2"
        else
             echo "$response"
        fi
        ;;
    deployments)
        if [ -z "$2" ]; then
            log_error "Usage: dokploy app deployments <application-id>"
            exit 1
        fi
        log_info "Fetching deployments for application $2..."
        local response=$(api_request "GET" "/deployment.all?applicationId=$2")
        echo "$response" | jq -r '.[] | "ID: \(.deploymentId)\n  Status: \(.status)\n  Created: \(.createdAt)\n  Description: \(.description // "N/A")\n"' 2>/dev/null || log_error "Failed to fetch deployments"
        ;;
    logs)
        local appId=""
        local deploymentId=""

        shift
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --deployment)
                    deploymentId="$2"
                    shift 2
                    ;;
                *)
                    appId="$1"
                    shift
                    ;;
            esac
        done

        if [ -z "$deploymentId" ]; then
            log_error "Usage: dokploy app logs <app-id> --deployment <deployment-id>"
            exit 1
        fi

        log_info "Fetching logs for deployment $deploymentId..."
        local response=$(api_request "GET" "/deployment.logs?deploymentId=$deploymentId")
        echo "$response" | jq '.' 2>/dev/null || log_error "Failed to fetch logs"
        ;;
    update)
        if [ -z "$2" ]; then
            log_error "Usage: dokploy app update <application-id> [--name <name>] [--env \"KEY=VALUE\"]"
            exit 1
        fi

        local appId="$2"
        local name=""
        local env=""

        shift 2
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --name)
                    name="$2"
                    shift 2
                    ;;
                --env)
                    env="$2"
                    shift 2
                    ;;
                *)
                    ;;
            esac
        done

        local data=$(jq -n --arg applicationId "$appId" '{applicationId: $applicationId}')

        if [ -n "$name" ]; then
            data=$(echo "$data" | jq --arg name "$name" '. + {name: $name}')
        fi

        if [ -n "$env" ]; then
             local formattedEnv=$(echo "$env" | tr ';' '\n')
             data=$(echo "$data" | jq --arg env "$formattedEnv" '. + {env: $env}')
        fi

        log_info "Updating application $appId..."
        local response=$(api_request "POST" "/application.update" "$data")

        if echo "$response" | jq -e '.applicationId' > /dev/null 2>&1; then
            log_success "Application updated"
        else
            log_error "Failed to update application"
            echo "$response"
            exit 1
        fi
        ;;
    delete)
        if [ -z "$2" ]; then
            log_error "Usage: dokploy app delete <application-id>"
            exit 1
        fi

        log_warn "Are you sure you want to delete application $2?"
        read -p "Type 'yes' to confirm: " confirm

        if [ "$confirm" != "yes" ]; then
            log_info "Cancelled"
            exit 0
        fi

        log_info "Deleting application $2..."
        local data=$(jq -n --arg applicationId "$2" '{applicationId: $applicationId}')
        local response=$(api_request "POST" "/application.delete" "$data")

        if echo "$response" | jq -e 'true' > /dev/null 2>&1; then
            log_success "Application deleted"
        else
            if echo "$response" | jq -e '.applicationId' > /dev/null 2>&1; then
                 log_success "Application deleted"
            else
                 log_error "Failed to delete application"
                 echo "$response"
                 exit 1
            fi
        fi
        ;;
    env)
        shift
        case "$1" in
            list)
                if [ -z "$2" ]; then
                    log_error "Usage: dokploy app env list <application-id>"
                    exit 1
                fi
                log_info "Fetching environment variables for $2..."
                local response=$(api_request "GET" "/application.one?applicationId=$2")
                echo "$response" | jq -r '.env // ""'
                ;;
            set)
                shift
                local appId="$1"
                local key=""
                local value=""

                shift
                while [[ $# -gt 0 ]]; do
                    case "$1" in
                        --key)
                            key="$2"
                            shift 2
                            ;;
                        --value)
                            value="$2"
                            shift 2
                            ;;
                        *)
                            ;;
                    esac
                done

                if [ -z "$appId" ] || [ -z "$key" ]; then
                    log_error "Usage: dokploy app env set <app-id> --key <key> --value <value>"
                    exit 1
                fi

                local response=$(api_request "GET" "/application.one?applicationId=$appId")
                local currentEnv=$(echo "$response" | jq -r '.env // ""')

                local newEnv=$(echo "$currentEnv" | jq -R -s -r --arg key "$key" --arg value "$value" '
                    split("\n") |
                    map(select(length > 0)) |
                    map(split("=") | {(.[0]): (.[1:] | join("="))}) |
                    add |
                    if . == null then {} else . end |
                    . + {($key): $value} |
                    to_entries |
                    map("\(.key)=\(.value)") |
                    join("\n")
                ')

                local data=$(jq -n --arg applicationId "$appId" --arg env "$newEnv" '{applicationId: $applicationId, env: $env}')

                log_info "Setting environment variable $key for $appId..."
                local updateResp=$(api_request "POST" "/application.saveEnvironment" "$data")

                if echo "$updateResp" | jq -e '.applicationId' > /dev/null 2>&1; then
                    log_success "Environment variable set"
                else
                    log_error "Failed to set environment variable"
                    echo "$updateResp"
                    exit 1
                fi
                ;;
            delete)
                shift
                local appId="$1"
                local key=""

                shift
                while [[ $# -gt 0 ]]; do
                    case "$1" in
                        --key)
                            key="$2"
                            shift 2
                            ;;
                        *)
                            ;;
                    esac
                done

                if [ -z "$appId" ] || [ -z "$key" ]; then
                    log_error "Usage: dokploy app env delete <app-id> --key <key>"
                    exit 1
                fi

                local response=$(api_request "GET" "/application.one?applicationId=$appId")
                local currentEnv=$(echo "$response" | jq -r '.env // ""')

                local newEnv=$(echo "$currentEnv" | jq -R -s -r --arg key "$key" '
                    split("\n") |
                    map(select(length > 0)) |
                    map(split("=") | {(.[0]): (.[1:] | join("="))}) |
                    add |
                    if . == null then {} else . end |
                    del(.[$key]) |
                    to_entries |
                    map("\(.key)=\(.value)") |
                    join("\n")
                ')

                local data=$(jq -n --arg applicationId "$appId" --arg env "$newEnv" '{applicationId: $applicationId, env: $env}')

                log_info "Deleting environment variable $key from $appId..."
                local updateResp=$(api_request "POST" "/application.saveEnvironment" "$data")

                if echo "$updateResp" | jq -e '.applicationId' > /dev/null 2>&1; then
                    log_success "Environment variable deleted"
                else
                    log_error "Failed to delete environment variable"
                    echo "$updateResp"
                    exit 1
                fi
                ;;
            *)
                echo "Usage: dokploy app env <command>"
                echo ""
                echo "Commands:"
                echo "  list <app-id>              List environment variables"
                echo "  set <app-id> --key <k> --value <v>  Set environment variable"
                echo "  delete <app-id> --key <k>   Delete environment variable"
                ;;
        esac
        ;;
    *)
        echo "Usage: dokploy app <command>"
        echo ""
        echo "Commands:"
        echo "  list [--project <id>]      List applications"
        echo "  get <app-id>              Get application details"
        echo "  create --environment-id <id> ...   Create application"
        echo "  deploy <app-id>            Trigger deployment"
        echo "  deployments <app-id>       List deployments"
        echo "  logs <app-id> --deployment <id>  Get deployment logs"
        echo "  update <app-id> ...         Update application"
        echo "  delete <app-id>            Delete application"
        echo "  env                        Environment variable commands"
        ;;
esac
}

# Only run main if script is executed directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi