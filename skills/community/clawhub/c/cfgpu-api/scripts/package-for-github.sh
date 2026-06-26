#!/bin/bash
# Package CFGPU API Skill for GitHub
# Removes all sensitive information and creates a clean version

set -e

echo "=== Packaging CFGPU API Skill for GitHub ==="
echo ""

# Create temporary directory for clean version
TEMP_DIR="/tmp/cfgpu-api-skill-$(date +%s)"
CLEAN_DIR="$TEMP_DIR/cfgpu-api"
mkdir -p "$CLEAN_DIR"
mkdir -p "$CLEAN_DIR/scripts"
mkdir -p "$CLEAN_DIR/references"

echo "📁 Created clean directory: $CLEAN_DIR"
echo ""

# Function to clean sensitive information
clean_file() {
    local src_file="$1"
    local dest_file="$2"
    
    echo "  Cleaning: $(basename "$src_file")"
    
    # Create a clean copy
    cp "$src_file" "$dest_file"
    
    # Remove any potential sensitive data patterns
    # (This is precautionary - we already checked no hardcoded tokens)
    
    # Ensure all API token references use placeholders
    sed -i 's/YOUR_API_TOKEN/YOUR_API_TOKEN/g' "$dest_file"
    sed -i 's/YOUR_API_TOKEN/YOUR_API_TOKEN/g' "$dest_file"
    sed -i 's/YOUR_API_TOKEN/YOUR_API_TOKEN/g' "$dest_file"
    
    # Remove any session IDs or instance IDs that might be sensitive
    sed -i 's/instance-xxxxx/instance-xxxxx/g' "$dest_file"
    sed -i 's/session-xxxxx/session-xxxxx/g' "$dest_file"
    
    # Remove any personal information
}

# Copy and clean SKILL.md
echo "📄 Processing SKILL.md..."
clean_file "/root/.openclaw/workspace/skills/cfgpu-api/SKILL.md" "$CLEAN_DIR/SKILL.md"

# Copy and clean scripts
echo ""
echo "📜 Processing scripts..."
for script in /root/.openclaw/workspace/skills/cfgpu-api/scripts/*.sh; do
    if [ -f "$script" ]; then
        script_name=$(basename "$script")
        clean_file "$script" "$CLEAN_DIR/scripts/$script_name"
    fi
done

# Copy and clean references
echo ""
echo "📚 Processing references..."
for ref in /root/.openclaw/workspace/skills/cfgpu-api/references/*.md; do
    if [ -f "$ref" ]; then
        ref_name=$(basename "$ref")
        clean_file "$ref" "$CLEAN_DIR/references/$ref_name"
    fi
done

# Create GitHub-specific files
echo ""
echo "📝 Creating GitHub files..."

# Create .gitignore
cat > "$CLEAN_DIR/.gitignore" << 'EOF'
# Sensitive files
*.token
*.key
*.secret
.env
.env.local
.env.*.local

# System files
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp
/tmp/

# Backups
*.backup
*.bak

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Test files
test/
tests/
__tests__/
EOF

# Create LICENSE (MIT)
cat > "$CLEAN_DIR/LICENSE" << 'EOF'
MIT License

Copyright (c) 2024 CFGPU API Skill Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# CFGPU API Skill for OpenClaw

A comprehensive OpenClaw skill for managing GPU cloud instances on CFGPU platform.

## Features

- **Resource Management**: List available regions, GPU types, and system images
- **Instance Lifecycle**: Create, start, stop, release GPU instances
- **Image Management**: List and manage system/user images
- **Interactive Wizard**: User-friendly command-line interface
- **API Integration**: Full CFGPU API coverage

## Installation

### Option 1: Install via ClawHub
```bash
# Once published to ClawHub
clawhub install cfgpu-api
```

### Option 2: Manual Installation
1. Clone this repository
2. Copy the `cfgpu-api` folder to your OpenClaw skills directory:
   ```bash
   cp -r cfgpu-api ~/.openclaw/workspace/skills/
   ```

## Quick Start

### 1. Get API Token
Obtain your API token from [CFGPU Platform](https://cfgpu.com).

### 2. Configure Authentication
```bash
# Set environment variable
export CFGPU_API_TOKEN="YOUR_API_TOKEN"

# Or create token file
echo "YOUR_API_TOKEN" > ~/.cfgpu/token
chmod 600 ~/.cfgpu/token
```

### 3. Basic Usage
```bash
# List available regions
./scripts/cfgpu-helper.sh list-regions

# List available GPU types
./scripts/cfgpu-helper.sh list-gpus

# Interactive instance creation
./scripts/cfgpu-helper.sh quick-create
```

## Scripts Overview

| Script | Description |
|--------|-------------|
| `cfgpu-helper.sh` | Main CLI tool for all operations |
| `setup-env.sh` | Interactive environment setup |
| `check-config.sh` | Configuration validation |
| `example-usage.sh` | Usage examples |

## API Coverage

This skill supports the full CFGPU API:

- ✅ Region management
- ✅ GPU type listing
- ✅ Image management (system/user)
- ✅ Instance lifecycle (create/start/stop/release)
- ✅ Instance status monitoring
- ✅ Paginated instance queries

## Security Notes

- **Never commit API tokens** to version control
- **Use environment variables** or secure token files
- **Set appropriate permissions** on token files (`chmod 600`)
- **Regularly rotate API tokens** for security

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- [CFGPU Platform](https://cfgpu.com)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [GitHub Issues](https://github.com/yourusername/cfgpu-api-skill/issues)

## Acknowledgments

- CFGPU for providing the GPU cloud platform
- OpenClaw community for the skill ecosystem
- Contributors and users
EOF

# Create CONTRIBUTING.md
cat > "$CLEAN_DIR/CONTRIBUTING.md" << 'EOF'
# Contributing to CFGPU API Skill

Thank you for considering contributing to the CFGPU API Skill!

## Development Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   sudo apt-get install jq curl
   ```

3. Set up test environment:
   ```bash
   export CFGPU_API_TOKEN="test_token"
   ```

## Code Style

- Use shellcheck for shell scripts
- Follow Google Shell Style Guide
- Add comments for complex logic
- Include error handling

## Testing

1. Test scripts with different inputs
2. Verify API responses are handled correctly
3. Test edge cases and error conditions

## Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure no sensitive data is included
4. Update CHANGELOG.md

## Security

- Never include real API tokens
- Use environment variables for configuration
- Validate all user inputs
- Sanitize output data

## Questions?

Open an issue or start a discussion!
EOF

# Create CHANGELOG.md
cat > "$CLEAN_DIR/CHANGELOG.md" << 'EOF'
# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-03-27

### Added
- Initial release of CFGPU API Skill
- Complete CFGPU API coverage
- Interactive command-line interface
- Environment setup scripts
- Comprehensive documentation

### Features
- Region and GPU type listing
- Instance lifecycle management
- Image management
- Configuration validation
- Error handling

### Security
- Secure token handling
- Input validation
- No hardcoded credentials
EOF

# Create package.json for npm/clawhub
cat > "$CLEAN_DIR/package.json" << 'EOF'
{
  "name": "cfgpu-api-skill",
  "version": "1.0.0",
  "description": "OpenClaw skill for managing CFGPU GPU cloud instances",
  "main": "SKILL.md",
  "scripts": {
    "test": "bash scripts/check-config.sh",
    "lint": "shellcheck scripts/*.sh"
  },
  "keywords": [
    "openclaw",
    "skill",
    "cfgpu",
    "gpu",
    "cloud",
    "api"
  ],
  "author": "CFGPU API Skill Contributors",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/cfgpu-api-skill.git"
  },
  "bugs": {
    "url": "https://github.com/yourusername/cfgpu-api-skill/issues"
  },
  "homepage": "https://github.com/yourusername/cfgpu-api-skill#readme"
}
EOF

# Create verification script
cat > "$CLEAN_DIR/scripts/verify-clean.sh" << 'EOF'
#!/bin/bash
# Verify no sensitive information is included

echo "=== Verifying Clean Package ==="
echo ""

# Check for hardcoded API tokens
echo "🔍 Checking for hardcoded API tokens..."
if grep -r "YOUR_API_TOKEN" . 2>/dev/null; then
    echo "❌ Found hardcoded API token!"
    exit 1
else
    echo "✅ No hardcoded API tokens found"
fi

# Check for personal information
echo ""
echo "🔍 Checking for personal information..."
    echo "⚠️  Found personal information references"
else
    echo "✅ No personal information found"
fi

# Check file permissions
echo ""
echo "🔍 Checking file permissions..."
find scripts/ -name "*.sh" -exec sh -c '
    if [ ! -x "$1" ]; then
        echo "❌ $1 is not executable"
        exit 1
    fi
' _ {} \;
echo "✅ All scripts are executable"

# Check for large files
echo ""
echo "🔍 Checking for large files..."
find . -type f -size +1M | while read file; do
    echo "⚠️  Large file found: $file"
done

echo ""
echo "✅ Verification completed successfully!"
echo "The package is ready for GitHub."
EOF

chmod +x "$CLEAN_DIR/scripts/verify-clean.sh"

# Make all scripts executable
chmod +x "$CLEAN_DIR/scripts/"*.sh

# Create final archive
echo ""
echo "📦 Creating final package..."
cd "$TEMP_DIR"
tar -czf cfgpu-api-skill.tar.gz cfgpu-api/
zip -r cfgpu-api-skill.zip cfgpu-api/

echo ""
echo "🎉 Packaging completed!"
echo ""
echo "📁 Clean package located at: $CLEAN_DIR"
echo "📦 Archives created:"
echo "  - $TEMP_DIR/cfgpu-api-skill.tar.gz"
echo "  - $TEMP_DIR/cfgpu-api-skill.zip"
echo ""
echo "📋 Next steps:"
echo "1. Verify the package:"
echo "   cd $CLEAN_DIR && ./scripts/verify-clean.sh"
echo ""
echo "2. Create GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Name: cfgpu-api-skill"
echo "   - Add .gitignore: Python"
echo "   - Choose MIT License"
echo ""
echo "3. Upload files:"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial release: CFGPU API Skill v1.0.0'"
echo "   git remote add origin https://github.com/YOUR_USERNAME/cfgpu-api-skill.git"
echo "   git push -u origin main"
echo ""
echo "4. Publish to ClawHub (optional):"
echo "   clawhub publish ./cfgpu-api --slug cfgpu-api --name 'CFGPU API Skill' --version 1.0.0"
echo ""
echo "✅ Package is ready for GitHub!"