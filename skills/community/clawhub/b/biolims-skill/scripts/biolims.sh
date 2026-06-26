#!/bin/bash
# biolims.sh - Bio-LIMS API Script (v2.0)
#
# Usage:
#   biolims.sh order <order_id>                    # Query order details
#   biolims.sh order-list [page] [rows]           # Paginated order list query
#   biolims.sh create-order '<json>'               # Create a new order
#   biolims.sh update-order '<json>'               # Update an order
#   biolims.sh order-samples <order_id>            # Query order sample list
#   biolims.sh order-fees <order_id>               # Query order fee information
#   biolims.sh complete-order <order_id>           # Complete an order
#   biolims.sh cancel-order <order_id>             # Cancel an order
#
# Token auto-management: logs in to obtain token on first call, auto-refreshes on expiry.
# Token cached at: /tmp/biolims_token_cache.json

set -e

BASE_URL="${BIOLIMS_URL:-http://example.com/biolims}"
TOKEN_CACHE="/tmp/biolims_token_cache.json"
COOKIE_JAR="/tmp/biolims_cookies.txt"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect and select Python (Windows Python via .exe if WSL)
if command -v python3.exe &>/dev/null; then
    PYTHON="python3.exe"
elif command -v python.exe &>/dev/null; then
    PYTHON="python.exe"
elif command -v python3 &>/dev/null; then
    PYTHON="python3"
else
    PYTHON="python"
fi

USERNAME="${BIOLIMS_USER:-demo}"
PASSWORD="${BIOLIMS_PASSWORD:-demo}"
DATA_SOURCE="${BIOLIMS_DS:-demo}"
SOLE_ID=$(cat /proc/sys/kernel/random/uuid 2>/dev/null || uuidgen 2>/dev/null || echo "$(date +%s)-$$-biolims")

# ---------------------------------------------------------------------------
# Token Management
# ---------------------------------------------------------------------------
get_cached_token() {
    if [[ ! -f "$TOKEN_CACHE" ]]; then
        return 1
    fi
    local now
    now=$(date +%s)
    local expires_at
    expires_at=$($PYTHON -c "import json; print(json.load(open('$TOKEN_CACHE'))['expires_at'])" 2>/dev/null || echo "0")
    if [[ "$now" -ge "$expires_at" ]]; then
        return 1  # expired
    fi
    $PYTHON -c "import json; print(json.load(open('$TOKEN_CACHE'))['token'])"
}

login() {
    # Use Python script to encrypt password
    local encrypted_password
    # Convert WSL path to Windows path for python.exe
    local win_script_dir
    if [[ "$PYTHON" == *".exe" ]]; then
        win_script_dir=$(wslpath -w "$SCRIPT_DIR" 2>/dev/null || echo "$SCRIPT_DIR")
        encrypted_password=$($PYTHON "$win_script_dir\\encrypt_password.py" "$PASSWORD")
    else
        encrypted_password=$($PYTHON "$SCRIPT_DIR/encrypt_password.py" "$PASSWORD")
    fi

    if [[ -z "$encrypted_password" ]]; then
        echo '{"error":"Password encryption failed"}' >&2
        exit 1
    fi

    # URL-encode password (Base64 characters +, /, = need encoding)
    local url_encoded_password
    url_encoded_password=$(echo -n "$encrypted_password" | $PYTHON -c "import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read()))")

    # Call login API (note: parameters passed via URL, cookies saved)
    local resp_headers_file resp_body_file
    resp_headers_file=$(mktemp)
    resp_body_file=$(mktemp)

    # Use -c option to save cookies
    curl -s -c "$COOKIE_JAR" -D "$resp_headers_file" -X POST "$BASE_URL/user/Login?username=$USERNAME&password=$url_encoded_password" \
        -H "Content-Type: application/json" \
        -H "code: $DATA_SOURCE" \
        -H "X-DS: $DATA_SOURCE" \
        -H "accept-language: zh_CN" \
        -H "X-Sole-ID: $SOLE_ID" \
        -o "$resp_body_file"

    # Extract Token from response headers
    local token
    token=$(grep -i "^token:" "$resp_headers_file" | sed 's/^token: *//I' | tr -d '\r\n' || echo "")

    if [[ -z "$token" ]]; then
        echo '{"error":"Login failed, no token received"}' >&2
        cat "$resp_body_file" >&2
        rm -f "$resp_headers_file" "$resp_body_file"
        exit 1
    fi

    rm -f "$resp_headers_file" "$resp_body_file"

    # Cache token (set 25-minute expiry to avoid using an expired token)
    local now expires_at
    now=$(date +%s)
    expires_at=$((now + 25 * 60))  # Expires in 25 minutes

    # Use heredoc to save JSON, avoiding quote issues
    cat > "$TOKEN_CACHE" <<EOF
{"token": "$token", "expires_at": $expires_at}
EOF

    echo "$token"
}

get_token() {
    local token
    token=$(get_cached_token 2>/dev/null) || token=$(login)
    echo "$token"
}

# ---------------------------------------------------------------------------
# API Calls
# ---------------------------------------------------------------------------
call_api() {
    local method="$1"
    local path="$2"
    local body="$3"
    local retry_count=0
    local max_retries=1

    while [[ $retry_count -le $max_retries ]]; do
        local token
        token=$(get_token)

        # Extract XSRF-TOKEN from cookie file
        local xsrf_token=""
        if [[ -f "$COOKIE_JAR" ]]; then
            xsrf_token=$(grep "XSRF-TOKEN" "$COOKIE_JAR" | awk '{print $NF}' || echo "")
        fi

        # Send request, use -b to load cookies, add XSRF-TOKEN header
        local response
        response=$(curl -s -b "$COOKIE_JAR" -X "$method" "$BASE_URL$path" \
            -H "Content-Type: application/json" \
            -H "Token: $token" \
            -H "X-DS: $DATA_SOURCE" \
            -H "accept-language: zh_CN" \
            -H "X-Sole-ID: $SOLE_ID" \
            ${xsrf_token:+-H "X-XSRF-TOKEN: $xsrf_token"} \
            ${body:+-d "$body"})

        # Check if response is 401 (Token expired)
        local status
        status=$(echo "$response" | $PYTHON -c "import sys, json; d=json.load(sys.stdin); print(d.get('status', 200))" 2>/dev/null || echo "200")

        if [[ "$status" == "401" && $retry_count -lt $max_retries ]]; then
            # Token expired, clear cache and retry
            echo '{"info":"Token expired, re-logging in..."}' >&2
            rm -f "$TOKEN_CACHE" "$COOKIE_JAR"
            retry_count=$((retry_count + 1))
            sleep 1
            continue
        fi

        # Return response
        echo "$response"
        return 0
    done
}

# ---------------------------------------------------------------------------
# Command Dispatch
# ---------------------------------------------------------------------------
CMD="${1:-}"

case "$CMD" in
    order)
        # Query order details
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh order <order_id>"}' && exit 1
        call_api POST "/order/selectOrder" "{\"orderId\":\"$2\"}"
        ;;

    order-list)
        # Paginated order list query
        page="${2:-1}"
        rows="${3:-10}"
        call_api POST "/order/selectAllOrderList" "{\"bioTechLeaguePagingQuery\":{\"page\":$page,\"rows\":$rows,\"sort\":{},\"query\":[]}}"
        ;;

    create-order)
        # Create a new order
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh create-order '"'"'<json>'"'"'"}' && exit 1
        call_api POST "/order/saveOrUpdateOrderAllData" "$2"
        ;;

    update-order)
        # Update an order
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh update-order '"'"'<json>'"'"'"}' && exit 1
        call_api POST "/order/saveOrUpdateOrderAllData" "$2"
        ;;

    order-samples)
        # Query order sample list
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh order-samples <order_id>"}' && exit 1
        call_api POST "/order/selectSampleOrderItem" "{\"orderId\":\"$2\",\"bioTechLeaguePagingQuery\":{\"page\":1,\"rows\":100,\"sort\":{},\"query\":[]}}"
        ;;

    order-fees)
        # Query order fee information
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh order-fees <order_id>"}' && exit 1
        call_api POST "/order/selectFee" "{\"orderId\":\"$2\"}"
        ;;

    complete-order)
        # Complete an order
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh complete-order <order_id>"}' && exit 1
        call_api POST "/order/completeTask?id=$2" ""
        ;;

    cancel-order)
        # Cancel an order
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh cancel-order <order_id>"}' && exit 1
        call_api POST "/order/cancelTask?id=$2" ""
        ;;

    sample-types)
        # Query sample type list
        page="${2:-1}"
        rows="${3:-100}"
        call_api POST "/order/selectPopupsSampleType" "{\"page\":$page,\"rows\":$rows,\"sort\":{},\"query\":[]}"
        ;;

    search-sample-type)
        # Search sample type by name
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh search-sample-type <sample_type_name>"}' && exit 1
        # Use pagingSearchOne for fuzzy search
        call_api POST "/order/selectPopupsSampleType" "{\"page\":1,\"rows\":100,\"sort\":{},\"pagingSearchOne\":{\"matchMode\":[\"name\"],\"value\":\"$2\"},\"query\":[]}"
        ;;

    # ==================== Sample Receive Commands (Sample Receive) ====================

    receive-list)
        # Paginated receive order list query
        page="${2:-1}"
        rows="${3:-10}"
        # Per documentation: requires full bioTechLeaguePagingQuery (including pagingSearchOne and fuzzySearch)
        call_api POST "/samplecenter/clinicalSampleReceive/getSampleReceiveList" "{\"bioTechLeaguePagingQuery\":{\"page\":$page,\"rows\":$rows,\"sort\":{},\"query\":[],\"pagingSearchOne\":{},\"fuzzySearch\":{}}}"
        ;;

    receive)
        # Query single receive order details
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh receive <receive_id>"}' && exit 1
        receive_id="$2"
        # Per documentation: full format required
        call_api POST "/samplecenter/clinicalSampleReceive/getSampleReceive" "{\"id\":\"$receive_id\",\"type\":\"edit\",\"bioTechLeaguePagingQuery\":{\"page\":1,\"rows\":10},\"sampleReceive\":{\"id\":\"$receive_id\"},\"sampleReceiveId\":\"$receive_id\"}"
        ;;

    receive-samples)
        # Query sample receive detail list for a receive order
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh receive-samples <receive_id> [page] [rows]"}' && exit 1
        receive_id="$2"
        page="${3:-1}"
        rows="${4:-50}"
        # Per documentation: requires sampleReceiveId, sampleReceive object, bioTechLeaguePagingQuery
        call_api POST "/samplecenter/clinicalSampleReceive/getSampleReceiveItemList" "{\"sampleReceiveId\":\"$receive_id\",\"sampleReceive\":{\"id\":\"$receive_id\"},\"bioTechLeaguePagingQuery\":{\"page\":$page,\"rows\":$rows,\"sort\":{},\"query\":[],\"pagingSearchOne\":{},\"fuzzySearch\":{}}}"
        ;;

    create-receive | update-receive)
        # Create or update a receive order
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh create-receive '\"'\"'<json>'\"'\"'"}' && exit 1
        call_api POST "/samplecenter/clinicalSampleReceive/saveOrUpdateAllData" "$2"
        ;;

    complete-receive)
        # Complete a receive order
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh complete-receive <receive_id>"}' && exit 1
        call_api POST "/samplecenter/clinicalSampleReceive/completeTask?id=$2" ""
        ;;

    scan-barcode)
        # Scan barcode to get sample information
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh scan-barcode <barcode> <receive_id> [acceptDate] [isBoard]"}' && exit 1
        [[ -z "${3:-}" ]] && echo '{"error":"Usage: biolims.sh scan-barcode <barcode> <receive_id> [acceptDate] [isBoard]\n\nIf acceptDate and isBoard are not provided, the receive order will be queried to obtain them"}' && exit 1

        barcode="$2"
        receive_id="$3"
        accept_date="${4:-}"
        is_board="${5:-}"

        # If acceptDate and isBoard are not provided, query the receive order first
        if [[ -z "$accept_date" ]] || [[ -z "$is_board" ]]; then
            # Query receive order
            receive_data=$(call_api POST "/samplecenter/clinicalSampleReceive/getSampleReceive" "{\"id\":\"$receive_id\"}")

            # Use Python to parse JSON and extract acceptDate and isBoard
            accept_date=$($PYTHON -c "import sys, json; d=json.loads('$receive_data'); print(d.get('data', {}).get('sampleReceive', {}).get('acceptDate', ''))" 2>/dev/null)
            is_board=$($PYTHON -c "import sys, json; d=json.loads('$receive_data'); print(d.get('data', {}).get('sampleReceive', {}).get('isBoard', '0'))" 2>/dev/null)

            # If query failed or field is empty, show error
            if [[ -z "$accept_date" ]]; then
                echo '{"error":"Unable to get receive order info. Please verify the receive order ID, or manually provide acceptDate and isBoard parameters"}' && exit 1
            fi
        fi

        # Build the correct request body (must include sampleReceive object)
        call_api POST "/samplecenter/clinicalSampleReceive/scanBarcode" "{\"sampleReceive\":{\"id\":\"$receive_id\",\"acceptDate\":\"$accept_date\",\"isBoard\":\"$is_board\"},\"barCode\":\"$barcode\"}"
        ;;

    scan-order)
        # Scan order code to get unreceived samples
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh scan-order <order_code> [receive_id] [acceptDate] [isBoard]\n\nIf receive_id is NEW, a new receive order will be created; if it is an existing ID, samples will be added to that receive order"}' && exit 1

        order_code="$2"
        receive_id="${3:-NEW}"
        accept_date="${4:-}"
        is_board="${5:-0}"

        # If receive_id is not NEW and acceptDate/isBoard not provided, query the receive order first
        if [[ "$receive_id" != "NEW" ]] && [[ -z "$accept_date" || -z "$is_board" ]]; then
            # Query receive order
            receive_data=$(call_api POST "/samplecenter/clinicalSampleReceive/getSampleReceive" "{\"id\":\"$receive_id\"}")

            # Use Python to parse JSON and extract acceptDate and isBoard
            accept_date=$($PYTHON -c "import sys, json; d=json.loads('$receive_data'); print(d.get('data', {}).get('sampleReceive', {}).get('acceptDate', ''))" 2>/dev/null)
            is_board=$($PYTHON -c "import sys, json; d=json.loads('$receive_data'); print(d.get('data', {}).get('sampleReceive', {}).get('isBoard', '0'))" 2>/dev/null)

            # If query failed or field is empty, show error
            if [[ -z "$accept_date" ]]; then
                echo '{"error":"Unable to get receive order info. Please verify the receive order ID, or manually provide acceptDate and isBoard parameters"}' && exit 1
            fi
        fi

        # If receive_id is NEW and acceptDate not provided, use current time
        if [[ "$receive_id" == "NEW" ]] && [[ -z "$accept_date" ]]; then
            # Generate current time as acceptDate (format: YYYY-MM-DD HH:mm)
            accept_date=$(date "+%Y-%m-%d %H:%M")
        fi

        # Build the correct request body (must include sampleReceive object, ids must be an array)
        call_api POST "/samplecenter/clinicalSampleReceive/scanOrderCode" "{\"sampleReceive\":{\"id\":\"$receive_id\",\"acceptDate\":\"$accept_date\",\"isBoard\":\"$is_board\"},\"ids\":[\"$order_code\"]}"
        ;;

    delete-receive-item)
        # Delete sample receive detail items
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh delete-receive-item <receive_id> <item_id1,item_id2,...> [isBoard]"}' && exit 1
        [[ -z "${3:-}" ]] && echo '{"error":"Usage: biolims.sh delete-receive-item <receive_id> <item_id1,item_id2,...> [isBoard]"}' && exit 1

        receive_id="$2"
        item_ids_raw="$3"
        is_board="${4:-0}"  # Default 0 (no plate), use provided value if 4th argument given

        # Convert comma-separated IDs to JSON array
        item_ids=$(echo "$item_ids_raw" | sed 's/,/","/g')

        # Build the correct request body (field name must be ids, not sampleReceiveItemsId)
        call_api POST "/samplecenter/clinicalSampleReceive/deleteSampleReceiveItem" "{\"ids\":[\"$item_ids\"],\"sampleReceiveId\":\"$receive_id\",\"sampleReceive\":{\"id\":\"$receive_id\",\"isBoard\":\"$is_board\"}}"
        ;;

    get-orders-for-receive)
        # Get available order list (for order code mode selection)
        page="${2:-1}"
        rows="${3:-10}"
        # Per documentation: requires full bioTechLeaguePagingQuery (including pagingSearchOne and fuzzySearch)
        call_api POST "/samplecenter/clinicalSampleReceive/getOrderInfo" "{\"bioTechLeaguePagingQuery\":{\"page\":$page,\"rows\":$rows,\"sort\":{},\"query\":[],\"pagingSearchOne\":{},\"fuzzySearch\":{}}}"
        ;;

    # ==================== Dropdown & Query APIs (Dropdown & Query APIs) ====================

    get-express-companies)
        # Get express company list
        page="${2:-1}"
        rows="${3:-100}"
        # Per documentation: requires full bioTechLeaguePagingQuery (including pagingSearchOne and fuzzySearch)
        call_api POST "/samplecenter/clinicalSampleReceive/getExpressCompanyList" "{\"bioTechLeaguePagingQuery\":{\"page\":$page,\"rows\":$rows,\"sort\":{},\"query\":[],\"pagingSearchOne\":{},\"fuzzySearch\":{}}}"
        ;;

    get-dictionary)
        # Get dictionary data (e.g., transport methods)
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh get-dictionary <type_id>"}' && exit 1
        type_id="$2"
        page="${3:-1}"
        rows="${4:-100}"
        # Per documentation: requires full bioTechLeaguePagingQuery (including pagingSearchOne and fuzzySearch)
        call_api POST "/samplecenter/clinicalSampleReceive/getDicListByTypeId" "{\"typeId\":\"$type_id\",\"bioTechLeaguePagingQuery\":{\"page\":$page,\"rows\":$rows,\"sort\":{},\"query\":[],\"pagingSearchOne\":{},\"fuzzySearch\":{}}}"
        ;;

    get-sample-types-for-receive)
        # Get sample type list (for sample receive)
        page="${2:-1}"
        rows="${3:-9999}"
        # Per documentation: requires both nested and root-level paging fields
        call_api POST "/samplecenter/clinicalSampleReceive/getSampleTypeList" "{\"bioTechLeaguePagingQuery\":{\"page\":$page,\"rows\":$rows,\"sort\":{},\"pagingSearchOne\":{},\"query\":[]},\"page\":$page,\"rows\":$rows,\"sort\":{},\"pagingSearchOne\":{},\"query\":[]}"
        ;;

    get-next-flows)
        # Get next flow list (intersection based on test items)
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh get-next-flows <item_id1,item_id2,...> [page] [rows]\n\nNote: provide sample detail IDs (not product IDs)"}' && exit 1
        # Convert comma-separated sample detail IDs to JSON array
        item_ids=$(echo "$2" | sed 's/,/","/g')
        page="${3:-1}"
        rows="${4:-100}"
        # Per documentation: requires ids (sample detail ID array), modelId, bioTechLeaguePagingQuery
        # Note: productId is automatically extracted from ids by the backend
        call_api POST "/samplecenter/clinicalSampleReceive/getNextFlowListNew" "{\"ids\":[\"$item_ids\"],\"modelId\":\"ClinicalSampleReceive\",\"bioTechLeaguePagingQuery\":{\"page\":$page,\"rows\":$rows,\"sort\":{},\"pagingSearchOne\":{},\"query\":[]},\"page\":$page,\"rows\":$rows,\"sort\":{},\"pagingSearchOne\":{},\"query\":[]}"
        ;;

    get-units)
        # Get unit list
        page="${2:-1}"
        rows="${3:-9999}"
        # Per documentation: requires both nested and root-level paging fields
        call_api POST "/samplecenter/clinicalSampleReceive/getUnitList" "{\"bioTechLeaguePagingQuery\":{\"page\":$page,\"rows\":$rows,\"sort\":{},\"pagingSearchOne\":{},\"query\":[]},\"page\":$page,\"rows\":$rows,\"sort\":{},\"pagingSearchOne\":{},\"query\":[]}"
        ;;

    get-approvers)
        # Get approver list
        page="${2:-1}"
        rows="${3:-10}"
        # Per documentation: entity must be "ClinicalSampleReceive"
        call_api POST "/samplecenter/clinicalSampleReceive/getApproverList" "{\"entity\":\"ClinicalSampleReceive\",\"bioTechLeaguePagingQuery\":{\"page\":$page,\"rows\":$rows}}"
        ;;

    get-products)
        # Get test item (product) list
        page="${2:-1}"
        rows="${3:-100}"
        # Per documentation: requires full bioTechLeaguePagingQuery (including pagingSearchOne and fuzzySearch)
        call_api POST "/samplecenter/clinicalSampleReceive/getProductList" "{\"bioTechLeaguePagingQuery\":{\"page\":$page,\"rows\":$rows,\"sort\":{},\"query\":[],\"pagingSearchOne\":{},\"fuzzySearch\":{}}}"
        ;;

    # ==================== Hole Plate Management (Hole Plate Management) ====================

    auto-add-board)
        # Auto-add hole plate (full format requires JSON parameter, simplified version provided here)
        # Full usage: biolims.sh auto-add-board '<json>'
        # Simplified usage: biolims.sh auto-add-board <receive_id> <row_num> <col_num> <plate_number>

        if [[ "$2" =~ ^\{ ]]; then
            # JSON format - pass directly
            call_api POST "/samplecenter/clinicalSampleReceive/autoAddBoard" "$2"
        else
            # Simplified format - build basic JSON (note: full format requires type, sampleReceiveItems, x, y)
            [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh auto-add-board <receive_id> <row_num> <col_num> <plate_number>"}' && exit 1
            [[ -z "${3:-}" ]] && echo '{"error":"Usage: biolims.sh auto-add-board <receive_id> <row_num> <col_num> <plate_number>"}' && exit 1
            [[ -z "${4:-}" ]] && echo '{"error":"Usage: biolims.sh auto-add-board <receive_id> <row_num> <col_num> <plate_number>"}' && exit 1
            [[ -z "${5:-}" ]] && echo '{"error":"Usage: biolims.sh auto-add-board <receive_id> <row_num> <col_num> <plate_number>"}' && exit 1
            # Per documentation, full format requires: id, type, sampleReceiveItems, rowNum, colNum, banHao, x, y
            # Using defaults here: type="vertical", x=1, y=0, sampleReceiveItems=[] (auto-fetched by backend)
            call_api POST "/samplecenter/clinicalSampleReceive/autoAddBoard" "{\"id\":\"$2\",\"type\":\"vertical\",\"rowNum\":$3,\"colNum\":$4,\"banHao\":\"$5\",\"x\":1,\"y\":0,\"sampleReceiveItems\":[]}"
        fi
        ;;

    clear-hole-plate)
        # Clear hole plate
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh clear-hole-plate <receive_id> <plate_number>"}' && exit 1
        [[ -z "${3:-}" ]] && echo '{"error":"Usage: biolims.sh clear-hole-plate <receive_id> <plate_number>"}' && exit 1
        call_api POST "/samplecenter/clinicalSampleReceive/clearHolePlate" "{\"id\":\"$2\",\"counts\":\"$3\"}"
        ;;

    delete-hole-plate)
        # Delete hole plate
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh delete-hole-plate <receive_id> <plate_number>"}' && exit 1
        [[ -z "${3:-}" ]] && echo '{"error":"Usage: biolims.sh delete-hole-plate <receive_id> <plate_number>"}' && exit 1
        call_api POST "/samplecenter/clinicalSampleReceive/deleteHolePlate" "{\"id\":\"$2\",\"counts\":\"$3\"}"
        ;;

    change-sample-location)
        # Change sample location in hole plate
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh change-sample-location <sample_item_id> <pos_id> <plate_number>"}' && exit 1
        [[ -z "${3:-}" ]] && echo '{"error":"Usage: biolims.sh change-sample-location <sample_item_id> <pos_id> <plate_number>"}' && exit 1
        [[ -z "${4:-}" ]] && echo '{"error":"Usage: biolims.sh change-sample-location <sample_item_id> <pos_id> <plate_number>"}' && exit 1
        # Per documentation: requires sampleReceiveItems array, each element contains id, posId (well position e.g. A1), counts (plate number)
        call_api POST "/samplecenter/clinicalSampleReceive/changeSampleLocation" "{\"sampleReceiveItems\":[{\"id\":\"$2\",\"posId\":\"$3\",\"counts\":\"$4\"}]}"
        ;;

    # ==================== Import & Export APIs (Import & Export) ====================

    parse-receive-file)
        # Parse uploaded Excel file
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh parse-receive-file <file_id> [receive_id]"}' && exit 1
        receive_id="${3:-}"
        if [[ -n "$receive_id" ]]; then
            call_api POST "/samplecenter/clinicalSampleReceive/parseReceiveSheetFile" "{\"fileId\":\"$2\",\"id\":\"$receive_id\"}"
        else
            call_api POST "/samplecenter/clinicalSampleReceive/parseReceiveSheetFile" "{\"fileId\":\"$2\"}"
        fi
        ;;

    batch-export-receive)
        # Batch export sample details
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh batch-export-receive <receive_id>"}' && exit 1
        call_api POST "/samplecenter/clinicalSampleReceive/batchExport" "{\"id\":\"$2\"}"
        ;;

    get-print-templates)
        # Query valid print template information
        page="${2:-1}"
        rows="${3:-100}"
        # Per documentation: requires full bioTechLeaguePagingQuery (including pagingSearchOne and fuzzySearch)
        call_api POST "/samplecenter/clinicalSampleReceive/validTemplateInformation" "{\"bioTechLeaguePagingQuery\":{\"page\":$page,\"rows\":$rows,\"sort\":{},\"query\":[],\"pagingSearchOne\":{},\"fuzzySearch\":{}}}"
        ;;

    print-receive)
        # Print receive order (requires template ID and other parameters, exact input format TBD)
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh print-receive '\"'\"'<json>'\"'\"'"}' && exit 1
        call_api POST "/samplecenter/clinicalSampleReceive/println" "$2"
        ;;

    batch-import)
        # Batch import samples
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh batch-import '\"'\"'<json>'\"'\"'"}' && exit 1
        call_api POST "/samplecenter/clinicalSampleReceive/batchImport" "$2"
        ;;

    # ==================== Custom Fields (Custom Fields) ====================

    get-custom-fields)
        # Get custom field mappings
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh get-custom-fields <flag>\n\nflag options:\n  121-mainTable   - Receive order main table custom fields\n  121-receiveTable - Sample detail sub-table custom fields"}' && exit 1
        call_api GET "/system/custom/selAllFields?flag=$2" ""
        ;;

    # ==================== Experiment Template (Experiment Template) ====================
    # Base path: /masterdata/experimentTemplate
    # System: BioTechLeague LIMS | Version: v10.1.30

    et-list)
        # Paginated template list query (excludes state=30 voided records)
        # Usage: et-list [page] [rows] [templateName fuzzy search]
        page="${2:-1}"
        rows="${3:-10}"
        filter="${4:-}"
        if [[ -n "$filter" ]]; then
            call_api POST "/masterdata/experimentTemplate/ExperimentTemplateList" \
                "{\"page\":$page,\"rows\":$rows,\"query\":[[{\"fieldName\":\"templateName\",\"operator\":\"and\",\"matchMode\":\"contains\",\"value\":\"$filter\"}]]}"
        else
            call_api POST "/masterdata/experimentTemplate/ExperimentTemplateList" \
                "{\"page\":$page,\"rows\":$rows,\"query\":[]}"
        fi
        ;;

    et-detail)
        # Query template details (3-level nesting: main table -> steps ETemplateStepConfigLatest -> components ETemplateItemConfigLatest)
        # Usage: et-detail <template_id> [view|edit]
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-detail <template_id> [view|edit]"}' && exit 1
        mode="${3:-view}"
        call_api POST "/masterdata/experimentTemplate/selectTemplateItemUpgrade" \
            "{\"id\":\"$2\",\"type\":\"$mode\"}"
        ;;

    et-create)
        # Create or update template (@TcLock + @Transactional)
        # Create: no id, system generates ET{yyyy}{6-digit sequence}, state=3 (new)
        # Update: with id, DELETEs old steps/components then INSERTs new data, validates no duplicate labels for same component type within a step
        # Usage: et-create '<json>' or et-create @/path/to/file.json
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-create <json|@file>"}' && exit 1
        json_input="$2"
        [[ "$json_input" == @* ]] && json_input=$(cat "${json_input#@}")
        call_api POST "/masterdata/experimentTemplate/AddExperimentTemplate" "$json_input"
        ;;

    et-copy)
        # Deep copy template (@Transactional, includes steps, components, FastDFS attachment file copy, generates new ET code)
        # Usage: et-copy <template_id>
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-copy <template_id>"}' && exit 1
        call_api POST "/masterdata/experimentTemplate/copySop" "{\"id\":\"$2\"}"
        ;;

    et-cancel)
        # Void template (@Transactional, state->30, only creator can operate, auto-excluded from queries)
        # Usage: et-cancel <id1> [id2 ...]
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-cancel <id1> [id2 ...]"}' && exit 1
        shift
        ids_json=$(printf '"%s",' "$@" | sed 's/,$//')
        call_api POST "/masterdata/experimentTemplate/cancelTemplate" "{\"ids\":[$ids_json]}"
        ;;

    et-complete)
        # Complete template (workflow callback, state->1, auto-registers resultTable custom fields to business_data_table_metadata)
        # Registered table name format: t_experiment_{databaseTableSuffix}, excludes fixed columns nextFlow/result/sampleCode/testProjectName
        # Usage: et-complete <template_id>
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-complete <template_id>"}' && exit 1
        call_api POST "/masterdata/experimentTemplate/updateExperimentTemplate?id=$2" "{}"
        ;;

    et-step-add)
        # Add step (legacy editor, index=1 inserts below, index=0 inserts above)
        # Usage: et-step-add <template_id> <current_step_id> <1|0>
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-step-add <template_id> <step_id> <1|0>"}' && exit 1
        call_api POST "/masterdata/experimentTemplate/updateExperimentTemplateSteps" \
            "{\"templateId\":\"$2\",\"stepId\":\"$3\",\"index\":${4:-1}}"
        ;;

    et-step-delete)
        # Delete step (new editor, @Transactional, cascades deletion of all component entries under this step)
        # Usage: et-step-delete <step_uuid>
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-step-delete <step_uuid>"}' && exit 1
        call_api POST "/masterdata/experimentTemplate/deleteExperimentTemplate" \
            "{\"templateId\":\"$2\"}"
        ;;

    et-reagent-delete)
        # Delete reagent association (from sys_reagent_item_upgrade table)
        # Usage: et-reagent-delete <id1> [id2 ...]
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-reagent-delete <id1> [id2 ...]"}' && exit 1
        shift
        ids_json=$(printf '"%s",' "$@" | sed 's/,$//')
        call_api POST "/masterdata/experimentTemplate/deleteReagentItemUpgradeOne" \
            "{\"reagentItemUpgradeId\":[$ids_json]}"
        ;;

    et-instrument-delete)
        # Delete instrument association (from sys_cos_item_upgrade table)
        # Usage: et-instrument-delete <id1> [id2 ...]
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-instrument-delete <id1> [id2 ...]"}' && exit 1
        shift
        ids_json=$(printf '"%s",' "$@" | sed 's/,$//')
        call_api POST "/masterdata/experimentTemplate/deleteCosItemUpgradeOne" \
            "{\"cosItemUpgradeId\":[$ids_json]}"
        ;;

    et-formula-list)
        # Query formula information (paginated) -- sys_template_upgrade_formula table
        # Usage: et-formula-list <template_id> <item_id> [page] [rows]
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-formula-list <template_id> <item_id> [page] [rows]"}' && exit 1
        [[ -z "${3:-}" ]] && echo '{"error":"Usage: biolims.sh et-formula-list <template_id> <item_id> [page] [rows]"}' && exit 1
        page="${4:-1}"
        rows="${5:-10}"
        call_api POST "/masterdata/experimentTemplate/selectTemplateUpgradeFormula" \
            "{\"templateId\":\"$2\",\"templateItemUpgradeId\":\"$3\",\"bioTechLeaguePagingQuery\":{\"page\":$page,\"rows\":$rows,\"query\":[]}}"
        ;;

    et-formula-update)
        # Update formulas (batch, includes formX inline formulas and formY statistical formulas)
        # Usage: et-formula-update '<json_array>' or et-formula-update @/path/file.json
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-formula-update <json_array|@file>"}' && exit 1
        json_input="$2"
        [[ "$json_input" == @* ]] && json_input=$(cat "${json_input#@}")
        call_api POST "/masterdata/experimentTemplate/updateTemplateUpgradeFormula" "$json_input"
        ;;

    et-formula-delete)
        # Delete formulas (batch)
        # Usage: et-formula-delete <id1> [id2 ...]
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-formula-delete <id1> [id2 ...]"}' && exit 1
        shift
        ids_json=$(printf '"%s",' "$@" | sed 's/,$//')
        call_api POST "/masterdata/experimentTemplate/deleteTemplateUpgradeFormula" "[$ids_json]"
        ;;

    et-threshold-list)
        # Query threshold information -- sys_template_reference_upgrade table
        # Usage: et-threshold-list <template_id> <item_id>
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-threshold-list <template_id> <item_id>"}' && exit 1
        [[ -z "${3:-}" ]] && echo '{"error":"Usage: biolims.sh et-threshold-list <template_id> <item_id>"}' && exit 1
        call_api POST "/masterdata/experimentTemplate/selectTemplateReferenceUpgrade" \
            "{\"templateId\":\"$2\",\"templateItemUpgradeId\":\"$3\"}"
        ;;

    et-threshold-update)
        # Update thresholds (batch)
        # judge options: > < >= <= ==
        # result: 0=unqualified, 1=qualified, 2=needs attention
        # Usage: et-threshold-update '<json_array>' or et-threshold-update @/path/file.json
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-threshold-update <json_array|@file>"}' && exit 1
        json_input="$2"
        [[ "$json_input" == @* ]] && json_input=$(cat "${json_input#@}")
        call_api POST "/masterdata/experimentTemplate/updateTemplateReferenceUpgrade" "$json_input"
        ;;

    et-threshold-delete)
        # Delete thresholds (batch)
        # Usage: et-threshold-delete <id1> [id2 ...]
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-threshold-delete <id1> [id2 ...]"}' && exit 1
        shift
        ids_json=$(printf '"%s",' "$@" | sed 's/,$//')
        call_api POST "/masterdata/experimentTemplate/deleteTemplateReferenceUpgrade" "[$ids_json]"
        ;;

    et-threshold-add)
        # Add threshold via popup
        # Usage: et-threshold-add <template_id> <table_code> <table_code_id>
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-threshold-add <template_id> <table_code> <table_code_id>"}' && exit 1
        call_api POST "/masterdata/experimentTemplate/addPopupsReferenceUpgrade" \
            "{\"templateId\":\"$2\",\"tableCode\":\"$3\",\"tableCodeId\":\"$4\"}"
        ;;

    et-reagents)
        # Popup to select reagents (remote call to RemoteStorageService)
        # Usage: et-reagents [page] [rows]
        page="${2:-1}"
        rows="${3:-10}"
        call_api POST "/masterdata/experimentTemplate/ReagentsList" \
            "{\"page\":$page,\"rows\":$rows,\"query\":[]}"
        ;;

    et-instruments)
        # Popup to select instruments (remote call to RemoteSystemService)
        # Usage: et-instruments [type]
        call_api POST "/masterdata/experimentTemplate/InstrumentList?type=${2:-}" "{}"
        ;;

    et-exp-types)
        # Popup to select experiment types (remote call to RemoteActivitService)
        # Usage: et-exp-types [keyword]
        call_api POST "/masterdata/experimentTemplate/selectPopupsExperimentType?note=${2:-}" "{}"
        ;;

    et-exp-types-search)
        # Fuzzy search experiment types (remote call to RemoteActivitService)
        # Usage: et-exp-types-search <keyword> [note]
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-exp-types-search <keyword>"}' && exit 1
        call_api POST "/masterdata/experimentTemplate/selectFuzzyQueries?FuzzyQueries=$2&note=${3:-}" "{}"
        ;;

    et-sample-types)
        # Query sample types (local DicSampleType table)
        # Usage: et-sample-types
        call_api POST "/masterdata/experimentTemplate/SampleTypeAll" "{}"
        ;;

    et-approvers)
        # Popup to query approvers (remote call to RemoteSystemService)
        # Usage: et-approvers <group_id>
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-approvers <group_id>"}' && exit 1
        call_api POST "/masterdata/experimentTemplate/selectApprover?id=$2" "{}"
        ;;

    et-groups)
        # Popup to query experiment groups (remote call to RemoteSystemService)
        # Usage: et-groups
        call_api POST "/masterdata/experimentTemplate/selectPopupsPersonnelGroup" "{}"
        ;;

    et-custom-fields)
        # Query custom fields (for calculated column configuration, queries business_data_table_metadata table)
        # Usage: et-custom-fields <template_id> [item_id]
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-custom-fields <template_id> [item_id]"}' && exit 1
        call_api POST "/masterdata/experimentTemplate/selectCustomFieldByParam" \
            "{\"templateId\":\"$2\",\"templateItemUpgradeId\":\"${3:-}\"}"
        ;;

    et-check-sql)
        # Validate SQL statement legality (for formula configuration)
        # Usage: et-check-sql '<sql_statement>'
        [[ -z "${2:-}" ]] && echo '{"error":"Usage: biolims.sh et-check-sql \"<sql_statement>\""}' && exit 1
        call_api POST "/masterdata/experimentTemplate/checkSql" "{\"checkSql\":\"$2\"}"
        ;;

    et-all-completed)
        # Query all completed templates (state=1, for use by other modules)
        # Usage: et-all-completed [page] [rows]
        page="${2:-1}"
        rows="${3:-10}"
        call_api POST "/masterdata/experimentTemplate/selectExperimentTemplateAll" \
            "{\"page\":$page,\"rows\":$rows,\"query\":[]}"
        ;;

    # Keep legacy commands for compatibility (marked as deprecated)
    experiments)
        echo '{"error":"This command is deprecated, please use the new order API"}' && exit 1
        ;;
    experiment-result)
        echo '{"error":"This command is deprecated, please use the new order API"}' && exit 1
        ;;
    update-qc)
        echo '{"error":"This command is deprecated, please use the new order API"}' && exit 1
        ;;

    *)
        cat <<EOF
{"error":"Unknown command. Available commands:

Order Management:
  order | order-list | create-order | update-order | order-samples | order-fees | complete-order | cancel-order | sample-types | search-sample-type

Sample Receive:
  receive-list | receive | receive-samples | create-receive | update-receive | complete-receive | scan-barcode | scan-order | delete-receive-item | get-orders-for-receive

Dropdown Queries:
  get-express-companies | get-dictionary | get-sample-types-for-receive | get-next-flows | get-units | get-approvers | get-products

Hole Plate Management:
  auto-add-board | clear-hole-plate | delete-hole-plate | change-sample-location

Import & Export:
  parse-receive-file | batch-import | batch-export-receive | get-print-templates | print-receive

Custom Fields:
  get-custom-fields

Experiment Template (Core):
  et-list | et-detail | et-create | et-copy | et-cancel | et-complete | et-all-completed

Experiment Template (Step Management):
  et-step-add | et-step-delete

Experiment Template (Formula/Threshold):
  et-formula-list | et-formula-update | et-formula-delete
  et-threshold-list | et-threshold-update | et-threshold-delete | et-threshold-add

Experiment Template (Association Deletion):
  et-reagent-delete | et-instrument-delete

Experiment Template (Popup Selection):
  et-reagents | et-instruments | et-exp-types | et-exp-types-search
  et-sample-types | et-approvers | et-groups

Experiment Template (Tools):
  et-custom-fields | et-check-sql
"}
EOF
        exit 1
        ;;
esac
