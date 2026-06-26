#!/bin/bash

# Blogger Auto-Publish Setup Script
# Version: 1.0.0
# Date: 2026-03-28

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [ "$EUID" -eq 0 ]; then
        log_warning "Running as root. It's recommended to run as a regular user."
        read -p "Continue anyway? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Check Node.js version
check_node() {
    log_info "Checking Node.js version..."
    if ! command -v node &> /dev/null; then
        log_error "Node.js is not installed. Please install Node.js 14.0.0 or higher."
        log_info "Visit: https://nodejs.org/"
        exit 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2)
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)
    
    if [ $NODE_MAJOR -lt 14 ]; then
        log_error "Node.js version $NODE_VERSION is too old. Please upgrade to 14.0.0 or higher."
        exit 1
    fi
    
    log_success "Node.js $NODE_VERSION detected"
}

# Check npm
check_npm() {
    log_info "Checking npm..."
    if ! command -v npm &> /dev/null; then
        log_error "npm is not installed. Please install npm."
        exit 1
    fi
    
    NPM_VERSION=$(npm --version)
    log_success "npm $NPM_VERSION detected"
}

# Install dependencies
install_dependencies() {
    log_info "Installing dependencies..."
    
    if [ -f "package.json" ]; then
        npm install
        if [ $? -eq 0 ]; then
            log_success "Dependencies installed successfully"
        else
            log_error "Failed to install dependencies"
            exit 1
        fi
    else
        log_warning "package.json not found. Installing googleapis directly..."
        npm install googleapis@latest
        if [ $? -eq 0 ]; then
            log_success "Google APIs library installed"
        else
            log_error "Failed to install googleapis"
            exit 1
        fi
    fi
}

# Check for credentials file
check_credentials() {
    log_info "Checking for Google API credentials..."
    
    if [ -f "credentials.json" ]; then
        log_success "Found credentials.json"
        return 0
    fi
    
    log_warning "credentials.json not found"
    echo ""
    echo "To use this skill, you need Google API credentials:"
    echo ""
    echo "1. Go to: https://console.cloud.google.com/"
    echo "2. Create a new project or select existing"
    echo "3. Enable 'Blogger API v3'"
    echo "4. Create OAuth 2.0 credentials (Web application)"
    echo "5. Set redirect URI: http://localhost:3000/oauth2callback"
    echo "6. Download credentials.json"
    echo ""
    echo "Place credentials.json in this directory and run setup again."
    echo ""
    
    return 1
}

# Check for blog ID
check_blog_id() {
    log_info "Checking for blog ID..."
    
    if [ -n "$BLOG_ID" ]; then
        log_success "Blog ID found in environment: $BLOG_ID"
        return 0
    fi
    
    if [ -f "config.js" ] && grep -q "blogId" config.js; then
        log_success "Blog ID found in config.js"
        return 0
    fi
    
    log_warning "Blog ID not configured"
    echo ""
    echo "You need to set your Blogger blog ID:"
    echo ""
    echo "Method 1: Environment variable"
    echo "  export BLOG_ID=\"your-blog-id-here\""
    echo ""
    echo "Method 2: Edit config.js"
    echo "  Set the blogId property"
    echo ""
    echo "Method 3: Use find-blog-id.js script"
    echo "  node find-blog-id.js"
    echo ""
    echo "To find your blog ID:"
    echo "1. Log in to Blogger"
    echo "2. Go to your blog"
    echo "3. Check URL or settings for numeric ID"
    echo ""
    
    return 1
}

# First-time authorization
run_authorization() {
    log_info "Checking authorization status..."
    
    if [ -f "token.json" ]; then
        log_success "Found existing token.json"
        echo ""
        echo "To re-authorize, delete token.json and run:"
        echo "  node auth.js login"
        echo ""
        return 0
    fi
    
    log_warning "No authorization token found"
    echo ""
    echo "You need to authorize this application:"
    echo ""
    echo "1. Make sure credentials.json is in place"
    echo "2. Run: node auth.js login"
    echo "3. Follow the browser prompts"
    echo "4. token.json will be automatically generated"
    echo ""
    echo "For complete authorization flow:"
    echo "  node complete-auth.js"
    echo ""
    
    read -p "Run authorization now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -f "complete-auth.js" ]; then
            node complete-auth.js
        elif [ -f "auth.js" ]; then
            node auth.js login
        else
            log_error "Authorization scripts not found"
        fi
    fi
}

# Create example files
create_examples() {
    log_info "Creating example files..."
    
    # Create posts directory if it doesn't exist
    mkdir -p posts
    
    # Create example post if none exists
    if [ ! -f "posts/example-post.md" ]; then
        cat > posts/example-post.md << 'EOF'
---
title: Example Blog Post
labels: example, test, tutorial
draft: true
---

# Example Blog Post

This is an example Markdown post for testing the Blogger Auto-Publish skill.

## Features Demonstrated

1. **Markdown formatting** - Headers, lists, and more
2. **Code blocks** - With syntax highlighting
3. **Links** - [OpenClaw Documentation](https://docs.openclaw.ai)
4. **Images** - ![](https://via.placeholder.com/400x200)

## Code Example

```javascript
// Example JavaScript code
function greet(name) {
    console.log(`Hello, ${name}!`);
    return `Welcome to Blogger Auto-Publish`;
}

// Call the function
const message = greet('Reader');
console.log(message);
```

## Next Steps

1. Test publishing this as a draft
2. Review the published post
3. Modify and publish your own content
4. Set up automated publishing

---

*This post was automatically generated by the setup script.*
EOF
        log_success "Created example post: posts/example-post.md"
    fi
    
    # Create config example if no config exists
    if [ ! -f "config.js" ]; then
        cat > config.js << 'EOF'
// Blogger Auto-Publish Configuration
// Copy this file to config.js and update values

module.exports = {
  // Required: Your Blogger blog ID
  // Get this from Blogger URL or use find-blog-id.js
  blogId: process.env.BLOG_ID || "YOUR_BLOG_ID_HERE",
  
  // File paths
  credentialsPath: process.env.CREDENTIALS_PATH || "./credentials.json",
  tokenPath: process.env.TOKEN_PATH || "./token.json",
  postsDir: process.env.POSTS_DIR || "./posts",
  
  // API settings
  maxRetries: parseInt(process.env.MAX_RETRIES) || 3,
  retryDelay: parseInt(process.env.RETRY_DELAY) || 1000,
  
  // Content settings
  defaultLabels: ['auto-published'],
  convertMarkdown: true,
  validateEnglish: true,
  
  // Logging
  logLevel: process.env.LOG_LEVEL || 'info'
};
EOF
        log_success "Created config template: config.js"
        log_warning "Please edit config.js and set your blog ID"
    fi
}

# Show usage instructions
show_usage() {
    echo ""
    echo "========================================="
    echo "BLOGGER AUTO-PUBLISH SETUP COMPLETE"
    echo "========================================="
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Edit config.js and set your blog ID"
    echo "2. Place credentials.json in this directory"
    echo "3. Run authorization: node auth.js login"
    echo "4. Test with example: node publish.js --file posts/example-post.md"
    echo ""
    echo "Available commands:"
    echo "  node list_blogs.js                 - List your blogs"
    echo "  node publish.js --file <path>      - Publish an article"
    echo "  node delete-all-drafts.js          - Delete draft posts"
    echo "  node find-blog-id.js               - Find your blog ID"
    echo ""
    echo "For more examples, see references/EXAMPLES.md"
    echo ""
}

# Main setup function
main() {
    echo ""
    echo "========================================="
    echo "Blogger Auto-Publish Setup"
    echo "Version 1.0.0"
    echo "========================================="
    echo ""
    
    # Run checks and setup steps
    check_root
    check_node
    check_npm
    install_dependencies
    check_credentials
    check_blog_id
    create_examples
    run_authorization
    
    show_usage
}

# Run main function
main "$@"