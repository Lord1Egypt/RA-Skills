#!/usr/bin/env bash
# pages-deploy: One-click static site deployment to BytePlus Edge Pages
# Smart routing: creates project if not exists, updates deployment if exists

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEST=""

# ========== Parameter Parsing ==========
NAME=""
DIR=""
DESC=""
REGION=""
DOMAIN=""
BUILD_CMD=""
SECRETS_FILE=""

usage() {
    cat <<EOF
Usage: bash deploy.sh --name <project-name> --dir <site-directory> [options]

Required:
  --name        Pages project name
  --dir         Static site resource directory (must contain index.html)

Options:
  --desc        Project description
  --region      Acceleration region: global / chinese_mainland / outside_chinese_mainland
  --domain      Custom domain
  --build-cmd   Build command to run before deployment (e.g. "npm run build")
  --secrets-file  AK/SK config file path
  -h, --help    Show help
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --name)     NAME="$2"; shift 2;;
        --dir)      DIR="$2"; shift 2;;
        --desc)     DESC="$2"; shift 2;;
        --region)   REGION="$2"; shift 2;;
        --domain)   DOMAIN="$2"; shift 2;;
        --build-cmd) BUILD_CMD="$2"; shift 2;;
        --secrets-file) SECRETS_FILE="$2"; shift 2;;
        -h|--help)  usage;;
        *)          echo "Unknown option: $1"; usage;;
    esac
done

if [[ -z "$NAME" || -z "$DIR" ]]; then
    echo "Error: --name and --dir are required"
    usage
fi

# ========== Utility Functions ==========
log_info()  { echo "[INFO]  $*"; }
log_warn()  { echo "[WARN]  $*"; }
log_error() { echo "[ERROR] $*" >&2; }
log_ok()    { echo "[OK]    $*"; }

# ========== Step 1: Install nest CLI ==========
install_nest() {
    log_info "Checking nest CLI..."

    # Check global installation first
    if command -v nest &>/dev/null; then
        NEST="nest"
        log_ok "Found global nest: $(nest --version 2>&1 | grep 'Version:' || echo 'installed')"
        return
    fi

    # Check local installation
    local local_nest="$HOME/.nest-cli/node_modules/.bin/nest"
    if [[ -x "$local_nest" ]]; then
        NEST="$local_nest"
        log_ok "Found local nest: $($NEST --version 2>&1 | grep 'Version:' || echo 'installed')"
        return
    fi

    # Check current directory installation (Cowork environment)
    local cowork_nest="/home/gem/tmp/nest-cli/node_modules/.bin/nest"
    if [[ -x "$cowork_nest" ]]; then
        NEST="$cowork_nest"
        log_ok "Found cowork nest: $($NEST --version 2>&1 | grep 'Version:' || echo 'installed')"
        return
    fi

    # Auto install
    log_info "Installing @byteplus/nest CLI..."
    local install_dir="$HOME/.nest-cli"
    if npm install @byteplus/nest --prefix "$install_dir" 2>/dev/null; then
        NEST="$install_dir/node_modules/.bin/nest"
        log_ok "Installed nest CLI to $install_dir"
    else
        # Fallback to /tmp
        install_dir="/tmp/nest-cli-$$"
        npm install @byteplus/nest --prefix "$install_dir" 2>/dev/null
        NEST="$install_dir/node_modules/.bin/nest"
        log_ok "Installed nest CLI to $install_dir (fallback)"
    fi
}

# ========== Step 2: Configure Authentication ==========
setup_auth() {
    log_info "Checking authentication..."

    # Check if already configured
    if $NEST pages list &>/dev/null; then
        log_ok "Authentication is configured"
        return
    fi

    # Read from secrets file
    local secrets="${SECRETS_FILE:-}"
    if [[ -z "$secrets" ]]; then
        # Try default path
        local userdata="/opt/tiger/mira_nas/userdata/${MY_EMPLOY_NO:-unknown}/secrets/byteplus.json"
        if [[ -f "$userdata" ]]; then
            secrets="$userdata"
        fi
    fi

    if [[ -n "$secrets" && -f "$secrets" ]]; then
        local ak sk
        ak=$(python3 -c "import json; print(json.load(open('$secrets'))['access_key'])" 2>/dev/null || true)
        sk=$(python3 -c "import json; print(json.load(open('$secrets'))['secret_key'])" 2>/dev/null || true)
        if [[ -n "$ak" && -n "$sk" ]]; then
            $NEST config set -g cloud.access_key "$ak"
            $NEST config set -g cloud.secret_key "$sk"
            log_ok "Authentication configured from secrets file"
            return
        fi
    fi

    # Read from environment variables
    if [[ -n "${BYTEPLUS_ACCESS_KEY:-}" && -n "${BYTEPLUS_SECRET_KEY:-}" ]]; then
        $NEST config set -g cloud.access_key "$BYTEPLUS_ACCESS_KEY"
        $NEST config set -g cloud.secret_key "$BYTEPLUS_SECRET_KEY"
        log_ok "Authentication configured from environment variables"
        return
    fi

    log_error "Authentication not configured. Please set up AK/SK:"
    echo "  Option 1: Create secrets/byteplus.json with {\"access_key\": \"xxx\", \"secret_key\": \"xxx\"}"
    echo "  Option 2: Set BYTEPLUS_ACCESS_KEY and BYTEPLUS_SECRET_KEY environment variables"
    echo "  Option 3: Run: nest config set -g cloud.access_key YOUR_AK && nest config set -g cloud.secret_key YOUR_SK"
    exit 1
}

# ========== Step 3: Validate Site Directory ==========
validate_site() {
    log_info "Validating site directory: $DIR"

    if [[ ! -d "$DIR" ]]; then
        log_error "Directory not found: $DIR"
        exit 1
    fi

    if [[ ! -f "$DIR/index.html" ]]; then
        log_error "index.html not found in $DIR"
        log_warn "The site directory must contain an index.html file"
        exit 1
    fi

    local file_count
    file_count=$(find "$DIR" -type f | wc -l)
    local dir_size
    dir_size=$(du -sh "$DIR" 2>/dev/null | cut -f1)
    log_ok "Site valid: $file_count files, $dir_size total"
}

# ========== Step 4: Build (optional) ==========
run_build() {
    if [[ -n "$BUILD_CMD" ]]; then
        log_info "Running build command: $BUILD_CMD"
        eval "$BUILD_CMD"
        log_ok "Build completed"
    elif [[ -f "$DIR/../package.json" || -f "package.json" ]]; then
        # Detect if build script exists
        local pkg="${DIR}/../package.json"
        [[ -f "package.json" ]] && pkg="package.json"
        if python3 -c "import json; scripts=json.load(open('$pkg')).get('scripts',{}); exit(0 if 'build' in scripts else 1)" 2>/dev/null; then
            log_info "Detected package.json with build script"
            log_warn "Skipping auto-build. Use --build-cmd 'npm run build' to enable"
        fi
    fi
}

# ========== Step 5: Smart Deploy (create or update) ==========
deploy() {
    log_info "Checking if project '$NAME' exists..."

    # Try to find project in list
    local pages_id=""
    local list_output
    list_output=$($NEST pages list 2>&1) || true

    # Parse output to find project ID by name
    pages_id=$(echo "$list_output" | grep -i "$NAME" | head -1 | awk '{print $1}' || true)

    if [[ -n "$pages_id" && "$pages_id" == p-* ]]; then
        # Project exists → incremental deploy
        log_info "Project found (ID: $pages_id), deploying update..."
        $NEST pages deploy --pages "$pages_id" --upload "$DIR"
        log_ok "Update deployed to project: $pages_id"

        # Update description and region (if specified)
        local update_args=""
        [[ -n "$DESC" ]] && update_args="$update_args --description '$DESC'"
        [[ -n "$REGION" ]] && update_args="$update_args --region $REGION"
        if [[ -n "$update_args" ]]; then
            eval "$NEST pages update -p $pages_id $update_args" || true
        fi
    else
        # Project not found → create
        log_info "Project not found, creating new project '$NAME'..."
        local create_args="--name $NAME --upload $DIR"
        [[ -n "$DESC" ]] && create_args="$create_args --description '$DESC'"

        $NEST pages create $create_args
        log_ok "New project '$NAME' created and deployed"

        # Re-fetch project ID
        sleep 2
        list_output=$($NEST pages list 2>&1) || true
        pages_id=$(echo "$list_output" | grep -i "$NAME" | head -1 | awk '{print $1}' || true)

        # Set acceleration region
        if [[ -n "$REGION" && -n "$pages_id" && "$pages_id" == p-* ]]; then
            $NEST pages update -p "$pages_id" --region "$REGION" || true
        fi
    fi

    # Bind custom domain
    if [[ -n "$DOMAIN" && -n "$pages_id" && "$pages_id" == p-* ]]; then
        log_info "Binding custom domain: $DOMAIN"
        $NEST pages domain add --pages "$pages_id" --domain "$DOMAIN" 2>/dev/null || true
        log_warn "Please add CNAME record at your DNS provider:"
        echo "  $DOMAIN → <pages-cname-target>"
        echo "  Then verify: nest pages domain verify --pages $pages_id --domain $DOMAIN"
    fi

    # Show project details
    if [[ -n "$pages_id" && "$pages_id" == p-* ]]; then
        echo ""
        log_info "Project details:"
        $NEST pages get -p "$pages_id" 2>&1 || true
    fi

    echo ""
    log_ok "Deployment complete!"
    log_warn "Note: CDN propagation takes 1-5 minutes"

    # China mainland reminder
    if [[ -z "$DOMAIN" ]]; then
        log_warn "China mainland production does not provide a default domain; a custom domain must be bound for access"
        echo "  Use: bash deploy.sh --name $NAME --dir $DIR --domain your-domain.com"
    fi
}

# ========== Main ==========
main() {
    echo "========================================"
    echo "  Pages Deploy - Static Site Deployer"
    echo "========================================"
    echo ""

    install_nest
    setup_auth
    validate_site
    run_build
    deploy

    echo ""
    echo "========================================"
    echo "  Done!"
    echo "========================================"
}

main
