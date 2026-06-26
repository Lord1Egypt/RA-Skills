#!/bin/bash

# Article Bookmarker Management Script
# Usage: ./bookmark.sh [init|save] [commit_message]

set -e

# Global variables (set by parse_github_path)
GITHUB_REPO_PATH=""
GITHUB_GIT_URL=""

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

function log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

function log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

function log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check required environment variables
function check_env() {
    if [[ -z "$ARTICLE_BOOKMARK_DIR" ]]; then
        log_error "ARTICLE_BOOKMARK_DIR environment variable is not set"
        exit 1
    fi
}

# Check if gh CLI is available
function check_gh() {
    if ! command -v gh &>/dev/null; then
        log_warn "GitHub CLI (gh) is not installed. Cannot create repository automatically."
        return 1
    fi

    # Check if gh is authenticated
    if ! gh auth status &>/dev/null; then
        log_warn "GitHub CLI is not authenticated. Run 'gh auth login' first."
        return 1
    fi

    return 0
}

# Parse ARTICLE_BOOKMARK_GITHUB to extract repo path and git URL
# Supports formats:
#   - username/repo
#   - git@github.com:username/repo.git
#   - https://github.com/username/repo
#   - https://github.com/username/repo.git
# Sets global variables: GITHUB_REPO_PATH, GITHUB_GIT_URL
function parse_github_path() {
    local input="$1"

    if [[ -z "$input" ]]; then
        GITHUB_REPO_PATH=""
        GITHUB_GIT_URL=""
        return 1
    fi

    # Format: git@github.com:username/repo.git
    if [[ "$input" =~ ^git@github\.com:(.+)\.git$ ]]; then
        GITHUB_REPO_PATH="${BASH_REMATCH[1]}"
        GITHUB_GIT_URL="$input"
    # Format: https://github.com/username/repo.git
    elif [[ "$input" =~ ^https?://github\.com/(.+)\.git$ ]]; then
        GITHUB_REPO_PATH="${BASH_REMATCH[1]}"
        GITHUB_GIT_URL="git@github.com:${GITHUB_REPO_PATH}.git"
    # Format: https://github.com/username/repo (without .git)
    elif [[ "$input" =~ ^https?://github\.com/([a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+)/?$ ]]; then
        GITHUB_REPO_PATH="${BASH_REMATCH[1]}"
        GITHUB_GIT_URL="git@github.com:${GITHUB_REPO_PATH}.git"
    # Format: username/repo
    elif [[ "$input" =~ ^[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+$ ]]; then
        GITHUB_REPO_PATH="$input"
        GITHUB_GIT_URL="git@github.com:${input}.git"
    else
        log_error "Invalid ARTICLE_BOOKMARK_GITHUB format: $input"
        log_info "Supported formats:"
        log_info "  - username/repo"
        log_info "  - git@github.com:username/repo.git"
        log_info "  - https://github.com/username/repo"
        log_info "  - https://github.com/username/repo.git"
        GITHUB_REPO_PATH=""
        GITHUB_GIT_URL=""
        return 1
    fi

    return 0
}

# Check if remote repository exists on GitHub
function check_remote_exists() {
    local repo_path="$1"

    if ! check_gh; then
        return 2 # Cannot check
    fi

    if gh repo view "$repo_path" >/dev/null 2>&1; then
        return 0 # Exists
    else
        return 1 # Does not exist
    fi
}

# Create GitHub repository using gh
function create_github_repo() {
    local repo_path="$1"

    if ! check_gh; then
        log_error "Cannot create repository: gh CLI not available or not authenticated"
        return 1
    fi

    log_info "Creating GitHub repository: $repo_path"

    # Extract owner and repo name
    local owner="${repo_path%%/*}"
    local repo="${repo_path#*/}"

    # Create the repository
    if gh repo create "$repo_path" --private --description "Article bookmarks collection" 2>&1; then
        log_info "Repository created successfully: $repo_path"
        return 0
    else
        log_error "Failed to create repository: $repo_path"
        return 1
    fi
}

# Initialize bookmark directory
function cmd_init() {
    check_env

    log_info "Initializing article bookmark directory..."

    # Create directory if not exists
    if [[ ! -d "$ARTICLE_BOOKMARK_DIR" ]]; then
        log_info "Creating directory: $ARTICLE_BOOKMARK_DIR"
        mkdir -p "$ARTICLE_BOOKMARK_DIR"
    else
        log_info "Directory already exists: $ARTICLE_BOOKMARK_DIR"
    fi

    cd "$ARTICLE_BOOKMARK_DIR"

    # Initialize git if not exists
    if [[ ! -d ".git" ]]; then
        log_info "Initializing git repository..."
        git init

        # Create .gitignore if not exists
        if [[ ! -f ".gitignore" ]]; then
            echo "*.bak" >.gitignore
            echo ".DS_Store" >>.gitignore
            log_info "Created .gitignore"
        fi

        # Create README.md if not exists
        if [[ ! -f "README.md" ]]; then
            echo "# Article Bookmarks" >README.md
            echo "" >>README.md
            echo "Collection of bookmarked articles with AI-generated summaries and tags." >>README.md
            log_info "Created README.md"
        fi
    else
        log_info "Git repository already initialized"
    fi

    # Handle ARTICLE_BOOKMARK_GITHUB
    if [[ -n "$ARTICLE_BOOKMARK_GITHUB" ]]; then
        log_info "ARTICLE_BOOKMARK_GITHUB is set: $ARTICLE_BOOKMARK_GITHUB"
        
        # Parse ARTICLE_BOOKMARK_GITHUB to extract repo path and git URL
        if ! parse_github_path "$ARTICLE_BOOKMARK_GITHUB"; then
            exit 1
        fi

        log_info "Parsed repo: $GITHUB_REPO_PATH"

        # Check if remote already configured
        local current_remote=$(git remote get-url origin 2>/dev/null || echo "")

        if [[ -z "$current_remote" ]]; then
            # Add remote
            git remote add origin "$GITHUB_GIT_URL"
            log_info "Added remote origin: $GITHUB_GIT_URL"
        elif [[ "$current_remote" != *"$GITHUB_REPO_PATH"* ]]; then
            # Update remote
            git remote set-url origin "$GITHUB_GIT_URL"
            log_info "Updated remote origin: $GITHUB_GIT_URL"
        fi

        # Check if remote repo exists
        # Note: use "|| remote_exists=$?" to prevent set -e from exiting on non-zero return
        local remote_exists=0
        check_remote_exists "$GITHUB_REPO_PATH" || remote_exists=$?

        if [[ $remote_exists -eq 0 ]]; then
            log_info "Remote repository exists, pulling latest changes..."

            # Fetch and try to pull
            git fetch origin 2>/dev/null || true

            # Check if main/master branch exists remotely
            local branch="main"
            if git show-ref --verify --quiet refs/remotes/origin/main; then
                branch="main"
            elif git show-ref --verify --quiet refs/remotes/origin/master; then
                branch="master"
            fi

            # Set local branch to track remote
            local local_branch
            local_branch=$(git symbolic-ref --short HEAD 2>/dev/null || echo "main")

            if git show-ref --verify --quiet "refs/remotes/origin/${branch}"; then
                git branch --set-upstream-to="origin/${branch}" "$local_branch" 2>/dev/null || true
                git pull --rebase origin "$branch" 2>/dev/null || git pull origin "$branch" 2>/dev/null || log_warn "Pull failed, continuing with local state"
            fi
        elif [[ $remote_exists -eq 1 ]]; then
            log_warn "Remote repository does not exist: $GITHUB_REPO_PATH"
            log_info "Will create on first 'save' command"
        fi
    fi

    log_info "Initialization complete!"
}

# Save and commit bookmarks
function cmd_save() {
    local commit_msg="${1:-"Update bookmarks $(date '+%Y-%m-%d %H:%M')"}"

    check_env

    if [[ ! -d "$ARTICLE_BOOKMARK_DIR" ]]; then
        log_error "Bookmark directory does not exist: $ARTICLE_BOOKMARK_DIR"
        log_info "Run 'init' command first"
        exit 1
    fi

    cd "$ARTICLE_BOOKMARK_DIR"

    # Check if git initialized
    if [[ ! -d ".git" ]]; then
        log_error "Not a git repository. Run 'init' command first"
        exit 1
    fi

    # Check if there are changes
    if [[ -z $(git status --porcelain *.md 2>/dev/null || true) ]]; then
        log_info "No changes to commit"
        return 0
    fi

    log_info "Staging markdown files..."
    git add *.md

    # Also add .gitignore if exist
    if [[ -f ".gitignore" ]]; then
        git add .gitignore
    fi

    log_info "Committing changes..."
    git commit -m "$commit_msg"

    # Handle ARTICLE_BOOKMARK_GITHUB
    if [[ -n "$ARTICLE_BOOKMARK_GITHUB" ]]; then
        # Parse ARTICLE_BOOKMARK_GITHUB to extract repo path and git URL
        if ! parse_github_path "$ARTICLE_BOOKMARK_GITHUB"; then
            exit 1
        fi

        # Check if remote exists
        # Note: use "|| remote_exists=$?" to prevent set -e from exiting on non-zero return
        local remote_exists=0
        check_remote_exists "$GITHUB_REPO_PATH" || remote_exists=$?

        if [[ $remote_exists -eq 1 ]]; then
            # Remote doesn't exist, try to create
            log_warn "Remote repository does not exist: $GITHUB_REPO_PATH"

            if create_github_repo "$GITHUB_REPO_PATH"; then
                log_info "Repository created, pushing..."
                # Wait a moment for GitHub to process
                sleep 2
            else
                log_error "Failed to create repository. Push skipped."
                return 1
            fi
        fi

        # Determine branch name
        local branch
        branch=$(git symbolic-ref --short HEAD 2>/dev/null || echo "main")

        # Push to remote
        log_info "Pushing to remote: $GITHUB_REPO_PATH"

        # Set upstream on first push
        if ! git rev-parse --abbrev-ref --symbolic-full-name @{u} &>/dev/null; then
            git push -u origin "$branch"
        else
            git push origin "$branch"
        fi

        log_info "Push complete!"
    else
        log_info "ARTICLE_BOOKMARK_GITHUB not set, skipping remote push"
    fi
}

# Usage help
function show_help() {
    cat <<EOF
Article Bookmarker Management Script

Usage:
    $0 <command> [options]

Commands:
    init            Initialize bookmark directory
                    - Create ARTICLE_BOOKMARK_DIR if not exists
                    - Initialize git repository if not exists
                    - Pull from ARTICLE_BOOKMARK_GITHUB remote if configured

    save [message]  Save and commit bookmarks
                    - Stage and commit all *.md files
                    - Push to ARTICLE_BOOKMARK_GITHUB if configured
                    - Create GitHub repo if ARTICLE_BOOKMARK_GITHUB doesn't exist

Environment Variables:
    ARTICLE_BOOKMARK_DIR      Required. Path to bookmark storage directory
    ARTICLE_BOOKMARK_GITHUB   Optional. GitHub repository path, supports formats:
                              - username/repo
                              - git@github.com:username/repo.git
                              - https://github.com/username/repo
                              - https://github.com/username/repo.git

Examples:
    export ARTICLE_BOOKMARK_DIR=~/.bookmarks
    export ARTICLE_BOOKMARK_GITHUB=myuser/article-bookmarks
    # or: export ARTICLE_BOOKMARK_GITHUB=git@github.com:myuser/article-bookmarks.git
    # or: export ARTICLE_BOOKMARK_GITHUB=https://github.com/myuser/article-bookmarks
    
    $0 init
    $0 save "Added new article about AI"
    $0 save  # Uses default commit message with timestamp
EOF
}

# Main entry point
function main() {
    local command="${1:-help}"

    case "$command" in
    init)
        cmd_init
        ;;
    save)
        cmd_save "${2:-}"
        ;;
    help | --help | -h)
        show_help
        ;;
    *)
        log_error "Unknown command: $command"
        show_help
        exit 1
        ;;
    esac
}

main "$@"
