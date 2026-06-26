# Installation Guide

## Prerequisites

Before installing this skill, ensure you have:

1. **Node.js** (version 14.0.0 or higher)
   ```bash
   node --version
   ```

2. **Google Cloud Account** with Blogger API enabled
3. **Blogger Blog** with write permissions
4. **OpenClaw** (version 2026.3.0 or higher)

## Installation Methods

### Method 1: Using .skill Package (Recommended)

1. Download the `.skill` package
2. Extract to OpenClaw skills directory:
   ```bash
   tar -xzf blogger-auto-publish-1.0.0.skill -C ~/.openclaw/skills/
   ```
3. Verify installation:
   ```bash
   ls -la ~/.openclaw/skills/blogger-auto-publish/
   ```

### Method 2: Using Zip Package

1. Download the `.zip` package
2. Extract to OpenClaw skills directory:
   ```bash
   unzip blogger-auto-publish-1.0.0.zip -d ~/.openclaw/skills/
   ```

### Method 3: Manual Installation

1. Clone or download the skill files
2. Copy to OpenClaw skills directory:
   ```bash
   mkdir -p ~/.openclaw/skills/blogger-auto-publish
   cp -r blogger-auto-publish/* ~/.openclaw/skills/blogger-auto-publish/
   ```

## Configuration Steps

### Step 1: Get Google API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **Blogger API v3**
4. Create **OAuth 2.0 Client ID** (Web application type)
5. Configure authorized redirect URIs:
   - `http://localhost:3000/oauth2callback`
6. Download `credentials.json`

### Step 2: Get Your Blog ID

1. Log in to [Blogger](https://www.blogger.com/)
2. Go to your blog
3. Find the blog ID in the URL or settings
4. Alternatively, use the provided script:
   ```bash
   node find-blog-id.js
   ```

### Step 3: First-Time Authorization

1. Place `credentials.json` in the skill directory
2. Set your blog ID:
   ```bash
   export BLOG_ID="your-blog-id-here"
   ```
3. Run the authorization:
   ```bash
   node auth.js login
   ```
4. Follow the browser prompts to authorize
5. `token.json` will be automatically generated

## Project Setup Script

For quick setup, use the included script:

```bash
# Make script executable
chmod +x scripts/setup-blogger.sh

# Run setup
./scripts/setup-blogger.sh
```

The setup script will:
1. Check Node.js version
2. Install dependencies
3. Guide you through credential setup
4. Help with first-time authorization

## Verification

After installation, verify everything works:

1. **Check skill recognition**:
   ```bash
   openclaw skills list | grep blogger
   ```

2. **Test blog listing**:
   ```bash
   node list_blogs.js
   ```

3. **Test with example post**:
   ```bash
   node publish.js --file posts/example-post.md --title "Test Post"
   ```

## Environment Variables

For persistent configuration, set these environment variables:

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export BLOG_ID="your-blog-id"
export CREDENTIALS_PATH="$HOME/.openclaw/skills/blogger-auto-publish/credentials.json"
export TOKEN_PATH="$HOME/.openclaw/skills/blogger-auto-publish/token.json"
export POSTS_DIR="$HOME/Documents/blog-posts"
```

## Updating

To update the skill:

1. Backup your configuration files:
   ```bash
   cp ~/.openclaw/skills/blogger-auto-publish/credentials.json /tmp/
   cp ~/.openclaw/skills/blogger-auto-publish/token.json /tmp/
   cp ~/.openclaw/skills/blogger-auto-publish/config.js /tmp/
   ```

2. Remove old version:
   ```bash
   rm -rf ~/.openclaw/skills/blogger-auto-publish
   ```

3. Install new version using one of the methods above

4. Restore your configuration:
   ```bash
   cp /tmp/credentials.json ~/.openclaw/skills/blogger-auto-publish/
   cp /tmp/token.json ~/.openclaw/skills/blogger-auto-publish/
   cp /tmp/config.js ~/.openclaw/skills/blogger-auto-publish/
   ```

## Troubleshooting

### Common Issues

1. **"Cannot find module 'googleapis'"**
   ```bash
   npm install googleapis@latest
   ```

2. **Authorization errors**
   - Delete `token.json` and re-run authorization
   - Check `credentials.json` is valid
   - Verify redirect URI configuration

3. **Blog not found**
   - Verify blog ID is correct
   - Check you have write permissions
   - Use `find-blog-id.js` to discover ID

4. **API quota exceeded**
   - Wait before retrying
   - Reduce batch size
   - Check Google Cloud Console for quota usage

### Getting Help

If you encounter issues:

1. Check the `references/` directory for detailed documentation
2. Review error messages in the console
3. Ensure all prerequisites are met
4. Check OpenClaw logs for skill-related errors

## Uninstallation

To remove the skill:

1. Remove the skill directory:
   ```bash
   rm -rf ~/.openclaw/skills/blogger-auto-publish
   ```

2. Remove environment variables from your shell profile

3. Revoke OAuth permissions (optional):
   - Visit [Google Account Permissions](https://myaccount.google.com/permissions)
   - Find "Blogger Auto-Publish" and click "Remove Access"

## Support

For additional support:
- OpenClaw documentation: https://docs.openclaw.ai
- Skill repository: https://github.com/openclaw/skills
- Community Discord: https://discord.com/invite/clawd