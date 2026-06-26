#!/bin/bash
# CFGPU API Helper Script
# Provides convenient functions for CFGPU API operations

set -e

# Configuration
CFGPU_API_BASE="https://api.cfgpu.com"
CFGPU_API_TOKEN="${CFGPU_API_TOKEN:-}"
CFGPU_API_TOKEN_FILE="${CFGPU_API_TOKEN_FILE:-$HOME/.cfgpu/token}"

# Load API token from file if not set
if [ -z "$CFGPU_API_TOKEN" ] && [ -f "$CFGPU_API_TOKEN_FILE" ]; then
    CFGPU_API_TOKEN=$(cat "$CFGPU_API_TOKEN_FILE" | tr -d '\n')
fi

# Check if API token is set
check_token() {
    if [ -z "$CFGPU_API_TOKEN" ]; then
        echo "Error: CFGPU_API_TOKEN is not set"
        echo "Set it as environment variable or in $CFGPU_API_TOKEN_FILE"
        exit 1
    fi
}

# Make API request
api_request() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    
    check_token
    
    local curl_cmd="curl -s -H 'Authorization: $CFGPU_API_TOKEN'"
    
    if [ "$method" = "POST" ] && [ -n "$data" ]; then
        curl_cmd="$curl_cmd -H 'Content-Type: application/json' -d '$data'"
    fi
    
    if [ "$method" = "POST" ]; then
        curl_cmd="$curl_cmd -X POST"
    fi
    
    eval "$curl_cmd '$CFGPU_API_BASE$endpoint'"
}

# List available regions
list_regions() {
    echo "Available regions:"
    api_request "GET" "/userapi/v1/region/list" | jq -r '.[] | "  \(.code): \(.name)"'
}

# List available GPU types
list_gpu_types() {
    echo "Available GPU types:"
    api_request "GET" "/userapi/v1/gpu/list" | jq -r '.[] | "  \(.code): \(.name)"'
}

# List system images
list_system_images() {
    local adapt_type="${1:-VM}"
    echo "System images (adaptType: $adapt_type):"
    api_request "GET" "/userapi/v1/image/systemList?adaptType=$adapt_type" | jq -r '.[] | "  \(.name): \(.children[].children[].children[].code)"' 2>/dev/null || \
    echo "  (Complex structure, use raw API for detailed view)"
}

# List user images
list_user_images() {
    local adapt_type="${1:-VM}"
    echo "User images (adaptType: $adapt_type):"
    api_request "GET" "/userapi/v1/image/privateList?adaptType=$adapt_type" | jq -r '.[] | "  \(.code): \(.name)"'
}

# Create instance
create_instance() {
    local region="$1"
    local gpu_type="$2"
    local gpu_num="${3:-1}"
    local image_id="$4"
    local duration="${5:-1}"
    local price_type="${6:-Day}"
    local instance_name="${7:-CFGPU-Instance}"
    local expand_size="${8:-0}"
    
    local data=$(cat <<EOF
{
    "priceType": "$price_type",
    "regionCode": "$region",
    "gpuType": "$gpu_type",
    "gpuNum": $gpu_num,
    "expandSize": $expand_size,
    "imageId": "$image_id",
    "serviceTime": $duration,
    "instanceName": "$instance_name"
}
EOF
    )
    
    echo "Creating instance..."
    api_request "POST" "/userapi/v1/instance/create" "$data" | jq '.'
}

# Get instance status
get_instance_status() {
    local instance_id="$1"
    api_request "GET" "/userapi/v1/instance/$instance_id/status" | jq '.'
}

# Get all instances status
get_all_instances_status() {
    api_request "GET" "/userapi/v1/instance/status" | jq '.'
}

# Start instance
start_instance() {
    local instance_id="$1"
    echo "Starting instance $instance_id..."
    api_request "POST" "/userapi/v1/instance/$instance_id/start" | jq '.'
}

# Stop instance
stop_instance() {
    local instance_id="$1"
    echo "Stopping instance $instance_id..."
    api_request "POST" "/userapi/v1/instance/$instance_id/stop" | jq '.'
}

# Release instance
release_instance() {
    local instance_id="$1"
    echo "Releasing instance $instance_id..."
    api_request "POST" "/userapi/v1/instance/$instance_id/release" | jq '.'
}

# Change instance image
change_instance_image() {
    local instance_id="$1"
    local image_id="$2"
    
    local data=$(cat <<EOF
{
    "imageId": "$image_id"
}
EOF
    )
    
    echo "Changing image for instance $instance_id..."
    api_request "POST" "/userapi/v1/instance/$instance_id/changeImage" "$data" | jq '.'
}

# Query instances (paginated)
query_instances() {
    local keyword="${1:-}"
    local status="${2:-}"
    local current_page="${3:-1}"
    local page_size="${4:-10}"
    
    local data=$(cat <<EOF
{
    "keyWord": "$keyword",
    "status": "$status",
    "currentPage": $current_page,
    "pageSize": $page_size
}
EOF
    )
    
    api_request "POST" "/userapi/v1/instance/page" "$data" | jq '.'
}

# Quick instance creation wizard
quick_create() {
    echo "=== CFGPU Instance Creation Wizard ==="
    
    # List regions
    echo "Available regions:"
    list_regions
    read -p "Enter region code: " region
    
    # List GPU types
    echo ""
    echo "Available GPU types:"
    list_gpu_types
    read -p "Enter GPU type code: " gpu_type
    
    # GPU count
    read -p "Enter GPU count [1]: " gpu_num
    gpu_num=${gpu_num:-1}
    
    # Image selection
    echo ""
    echo "Image selection:"
    echo "1. List system images"
    echo "2. List user images"
    echo "3. Enter image ID directly"
    read -p "Choose option [1]: " image_option
    image_option=${image_option:-1}
    
    case $image_option in
        1)
            list_system_images
            ;;
        2)
            list_user_images
            ;;
    esac
    
    read -p "Enter image ID: " image_id
    
    # Duration
    read -p "Enter service time [1]: " service_time
    service_time=${service_time:-1}
    
    # Price type
    echo ""
    echo "Price types: Day, Week, Month, Usage"
    read -p "Enter price type [Day]: " price_type
    price_type=${price_type:-Day}
    
    # Instance name
    read -p "Enter instance name [CFGPU-Instance]: " instance_name
    instance_name=${instance_name:-CFGPU-Instance}
    
    # Create instance
    echo ""
    echo "Creating instance with parameters:"
    echo "  Region: $region"
    echo "  GPU Type: $gpu_type"
    echo "  GPU Count: $gpu_num"
    echo "  Image: $image_id"
    echo "  Service Time: $service_time $price_type"
    echo "  Instance Name: $instance_name"
    
    read -p "Proceed? [y/N]: " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        create_instance "$region" "$gpu_type" "$gpu_num" "$image_id" "$service_time" "$price_type" "$instance_name"
    else
        echo "Creation cancelled."
    fi
}

# Show usage
usage() {
    cat <<EOF
CFGPU API Helper Script

Usage: $0 <command> [arguments]

Commands:
  list-regions                    List available regions
  list-gpus                       List available GPU types
  list-system-images [adaptType]  List system images (default: VM)
  list-user-images [adaptType]    List user images (default: VM)
  
  create <region> <gpu_type> <gpu_num> <image_id> [duration] [price_type] [name] [expand_size]
                                  Create a new instance
  quick-create                    Interactive instance creation wizard
  
  status <instance_id>            Get instance status
  all-status                      Get all instances status
  start <instance_id>             Start instance
  stop <instance_id>              Stop instance
  release <instance_id>           Release instance
  change-image <instance_id> <image_id>
                                  Change instance image
  
  query [keyword] [status] [page] [page_size]
                                  Query instances (paginated)

Environment:
  CFGPU_API_TOKEN                 API token for authentication
  CFGPU_API_TOKEN_FILE            File containing API token (default: ~/.cfgpu/token)

Examples:
  $0 list-regions
  $0 list-gpus
  $0 quick-create
  $0 create hz qnid2x6c 1 image_exc6f72b 1 Day "My-GPU-Instance"
  $0 status instance-xxxxx
  $0 start instance-xxxxx
  $0 query "test" "RUNNING"
EOF
}

# Main execution
main() {
    if [ $# -eq 0 ]; then
        usage
        exit 1
    fi
    
    command="$1"
    shift
    
    case "$command" in
        list-regions)
            list_regions
            ;;
        list-gpus)
            list_gpu_types
            ;;
        list-system-images)
            list_system_images "$@"
            ;;
        list-user-images)
            list_user_images "$@"
            ;;
        create)
            create_instance "$@"
            ;;
        quick-create)
            quick_create
            ;;
        status)
            get_instance_status "$1"
            ;;
        all-status)
            get_all_instances_status
            ;;
        start)
            start_instance "$1"
            ;;
        stop)
            stop_instance "$1"
            ;;
        release)
            release_instance "$1"
            ;;
        change-image)
            change_instance_image "$1" "$2"
            ;;
        query)
            query_instances "$@"
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            echo "Unknown command: $command"
            usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"