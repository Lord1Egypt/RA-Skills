# Blogger Auto-Publish Skill

Automatically publish Markdown articles to Google Blogger.

## Quick Start

### 1. Install Dependencies
```bash
cd ~/.openclaw/skills/blogger-auto-publish
npm install
```

### 2. Configure Credentials
Place your `credentials.json` file in the skill directory.

### 3. Set Blog ID
```bash
export BLOG_ID="your-blog-id-here"
# Or edit config.js
```

### 4. Authorize
```bash
node auth.js
# Follow the instructions to authorize
```

### 5. Publish a Post
```bash
node publish.js --file example.md --title "My First Post"
```

## Usage

### Authorization
```bash
# Start authorization
node auth.js

# Complete authorization with code
node auth.js --code YOUR_CODE

# Check authorization status
node auth.js --check

# Remove token
node auth.js --logout
```

### Publishing
```bash
# Publish a Markdown file
node publish.js --file post.md

# Publish with custom title
node publish.js --file post.md --title "Custom Title"

# Publish as draft
node publish.js --file post.md --draft true

# Add labels
node publish.js --file post.md --labels "tech,tutorial,blog"

# List all posts
node publish.js --list
```

## Markdown Format

### Basic Example
```markdown
# My Article Title

This is the first paragraph.

## Section 1

More content here...

- List item 1
- List item 2
- List item 3
```

### With Frontmatter
```markdown
---
title: My Custom Title
labels: technology, tutorial, programming
draft: true
---

# Article Content

Your content here...
```

## Configuration

Edit `config.js` or set environment variables:
- `BLOG_ID`: Your Blogger blog ID
- `CREDENTIALS_PATH`: Path to credentials.json
- `TOKEN_PATH`: Path to token.json
- `POSTS_DIR`: Directory for Markdown posts

## Troubleshooting

### Common Issues

1. **"Cannot find module 'googleapis'"**
   ```bash
   npm install googleapis@latest
   ```

2. **Authorization errors**
   - Delete `token.json` and re-run `node auth.js`
   - Check `credentials.json` is valid
   - Ensure redirect URI is `http://localhost:3000/oauth2callback`

3. **Blog not found**
   - Verify blog ID is correct
   - Check you have write permissions

## License

MIT