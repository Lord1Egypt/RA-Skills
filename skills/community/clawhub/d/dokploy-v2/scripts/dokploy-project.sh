#!/bin/bash
# Dokploy Project Management

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
        log_info "Fetching projects..."
        local response=$(api_request "GET" "/project.all")
        echo "$response" | jq -r '.[] | "ID: \(.projectId)\n  Name: \(.name)\n  Description: \(.description // "N/A")\n  Apps: \(.applications | length)\n"' 2>/dev/null || log_error "Failed to fetch projects"
        ;;
    get)
        if [ -z "$2" ]; then
            log_error "Usage: dokploy project get <project-id>"
            exit 1
        fi
        log_info "Fetching project $2..."
        # Updated: /project.byId -> /project.one
        local response=$(api_request "GET" "/project.one?projectId=$2")
        echo "$response" | jq '.' 2>/dev/null || log_error "Failed to fetch project"
        ;;
    create)
        local name=""
        local description=""

        shift
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --name)
                    name="$2"
                    shift 2
                    ;;
                --description)
                    description="$2"
                    shift 2
                    ;;
                *)
                    log_error "Unknown option: $1"
                    exit 1
                    ;;
            esac
        done

        if [ -z "$name" ]; then
            log_error "Usage: dokploy project create --name <name> [--description <desc>]"
            exit 1
        fi

        local data=$(jq -n \
            --arg name "$name" \
            --arg description "$description" \
            '{name: $name, description: $description}')

        log_info "Creating project '$name'..."
        local response=$(api_request "POST" "/project.create" "$data")
        local projectId=$(echo "$response" | jq -r '.projectId')

        if [ -n "$projectId" ] && [ "$projectId" != "null" ]; then
            log_success "Project created with ID: $projectId"
        else
            log_error "Failed to create project"
            echo "$response" | jq '.'
            exit 1
        fi
        ;;
    update)
        if [ -z "$2" ]; then
            log_error "Usage: dokploy project update <project-id> --name <name> [--description <desc>]"
            exit 1
        fi

        local projectId="$2"
        local name=""
        local description=""

        shift 2
        while [[ $# -gt 0 ]]; do
            case "$1" in
                --name)
                    name="$2"
                    shift 2
                    ;;
                --description)
                    description="$2"
                    shift 2
                    ;;
                *)
                    log_error "Unknown option: $1"
                    exit 1
                    ;;
            esac
        done

        local data=$(jq -n \
            --arg projectId "$projectId" \
            --arg name "$name" \
            --arg description "$description" \
            '{projectId: $projectId}')

        if [ -n "$name" ]; then
            data=$(echo "$data" | jq --arg name "$name" '. + {name: $name}')
        fi

        if [ -n "$description" ]; then
            data=$(echo "$data" | jq --arg description "$description" '. + {description: $description}')
        fi

        log_info "Updating project $projectId..."
        # Updated: PATCH /project.update -> POST /project.update
        local response=$(api_request "POST" "/project.update" "$data")

        if echo "$response" | jq -e '.projectId' > /dev/null 2>&1; then
            log_success "Project updated"
        else
            log_error "Failed to update project"
            echo "$response"
            exit 1
        fi
        ;;
    delete)
        if [ -z "$2" ]; then
            log_error "Usage: dokploy project delete <project-id>"
            exit 1
        fi

        log_warn "Are you sure you want to delete project $2?"
        read -p "Type 'yes' to confirm: " confirm

        if [ "$confirm" != "yes" ]; then
            log_info "Cancelled"
            exit 0
        fi

        log_info "Deleting project $2..."
        # Updated: DELETE /project.delete -> POST /project.remove
        local data=$(jq -n --arg projectId "$2" '{projectId: $projectId}')
        local response=$(api_request "POST" "/project.remove" "$data")

        if echo "$response" | jq -e 'true' > /dev/null 2>&1; then
            log_success "Project deleted"
        else
            if echo "$response" | jq -e '.projectId' > /dev/null 2>&1; then
                 log_success "Project deleted"
            else
                 log_error "Failed to delete project"
                 echo "$response"
                 exit 1
            fi
        fi
        ;;
    envs)
        if [ -z "$2" ]; then
            log_error "Usage: dokploy project envs <project-id>"
            exit 1
        fi
        log_info "Fetching environments for project $2..."
        # Updated: /project.byId -> /project.one
        local response=$(api_request "GET" "/project.one?projectId=$2")
        echo "$response" | jq -r '.environments[] | "ID: \(.environmentId)\n  Name: \(.name)\n  Description: \(.description // "N/A")\n"' 2>/dev/null || log_error "Failed to fetch environments"
        ;;
    *)
        echo "Usage: dokploy project <command>"
        echo ""
        echo "Commands:"
        echo "  list                       List all projects"
        echo "  get <project-id>           Get project details"
        echo "  create --name <name>        Create a new project"
        echo "  update <id> --name <name>   Update project"
        echo "  delete <project-id>          Delete a project"
        echo "  envs <project-id>            List environments in a project"
        ;;
esac
}

# Only run main if script is executed directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi