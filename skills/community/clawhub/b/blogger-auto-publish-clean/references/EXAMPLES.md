# Examples

This document provides practical examples of using the Blogger Auto-Publish skill.

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [Article Publishing](#article-publishing)
3. [Batch Processing](#batch-processing)
4. [Management Tasks](#management-tasks)
5. [Advanced Scenarios](#advanced-scenarios)
6. [Integration Examples](#integration-examples)

## Basic Examples

### Example 1: List All Blogs
```bash
# List all blogs accessible with current credentials
node list_blogs.js

# Output example:
# Found 2 blogs:
# 1. My Tech Blog (ID: 1234567890123456789)
# 2. Personal Journal (ID: 9876543210987654321)
```

### Example 2: Find Blog ID
```bash
# If you don't know your blog ID
node find-blog-id.js

# Or search by blog name
node find-blog-id.js --name "Tech Blog"
```

### Example 3: First-Time Authorization
```bash
# Complete authorization flow
node complete-auth.js

# Or step by step
node auth.js login
# Follow browser prompts...
```

## Article Publishing

### Example 4: Publish a Single Article
```bash
# Publish an article from Markdown file
node publish.js --file posts/my-article.md

# With custom title
node publish.js --file posts/my-article.md --title "My Custom Title"

# As a draft
node publish.js --file posts/my-article.md --draft

# With specific labels
node publish.js --file posts/my-article.md --labels "technology,programming,tutorial"
```

### Example 5: Article with Front Matter
Create `posts/example-with-frontmatter.md`:
```markdown
---
title: Getting Started with Node.js
labels: nodejs, javascript, backend, tutorial
draft: false
published: 2026-03-28
author: John Doe
---

# Getting Started with Node.js

Node.js is a powerful JavaScript runtime...

## Installation

```bash
npm install
```

## Key Features

- Event-driven architecture
- Non-blocking I/O
- Large ecosystem
```

Publish it:
```bash
node publish.js --file posts/example-with-frontmatter.md
```

### Example 6: Publish with Custom Configuration
```bash
# Use environment variables
export BLOG_ID="YOUR_BLOG_ID_HERE"
export MAX_RETRIES=5
node publish.js --file posts/article.md

# Or command line arguments
node publish.js --file posts/article.md --blog-id "YOUR_BLOG_ID_HERE" --max-retries 5
```

## Batch Processing

### Example 7: Publish All Articles in Directory
```bash
# Publish all .md files in posts directory
for file in posts/*.md; do
  echo "Publishing $file..."
  node publish.js --file "$file"
  sleep 2 # Add delay to avoid rate limits
done
```

### Example 8: Publish Only Drafts
```bash
# Find and publish only draft articles
for file in posts/*.md; do
  if grep -q "draft: true" "$file"; then
    echo "Publishing draft: $file"
    node publish.js --file "$file"
    sleep 1
  fi
done
```

### Example 9: Scheduled Publishing with Cron
Create a script `schedule-publish.sh`:
```bash
#!/bin/bash
# Schedule this to run daily at 9 AM

# Set environment
export BLOG_ID="YOUR_BLOG_ID_HERE"
export CREDENTIALS_PATH="/path/to/credentials.json"
export TOKEN_PATH="/path/to/token.json"

# Publish today's articles
TODAY=$(date +%Y-%m-%d)
for file in posts/${TODAY}-*.md; do
  if [ -f "$file" ]; then
    echo "Publishing scheduled article: $file"
    node /path/to/blogger-auto-publish/publish.js --file "$file"
  fi
done
```

Make it executable and schedule:
```bash
chmod +x schedule-publish.sh
# Add to crontab: 0 9 * * * /path/to/schedule-publish.sh
```

## Management Tasks

### Example 10: List All Posts
```bash
# List all posts in blog
node list_posts.js

# List with details
node list_posts.js --verbose

# List only drafts
node list_posts.js --status draft

# List by label
node list_posts.js --label "tutorial"
```

### Example 11: Delete Test Posts
```bash
# Delete posts with "test" in title
node delete-test-posts.js

# Delete posts from specific date
node delete-test-posts.js --date 2026-03-27

# Dry run (show what would be deleted)
node delete-test-posts.js --dry-run
```

### Example 12: Delete All Drafts
```bash
# Delete all draft posts
node delete-all-drafts.js

# Confirm before deleting each
node delete-all-drafts.js --confirm

# Delete drafts older than 30 days
node delete-all-drafts.js --older-than 30
```

### Example 13: Direct Draft Deletion
```bash
# More direct method (bypasses some checks)
node direct-delete-drafts.js

# Delete specific draft by ID
node direct-delete-drafts.js --post-id "1234567890123456789_123456789"
```

## Advanced Scenarios

### Example 14: Content Validation Pipeline
Create `validate-and-publish.sh`:
```bash
#!/bin/bash
# Validate content before publishing

ARTICLE=$1

# Check if file exists
if [ ! -f "$ARTICLE" ]; then
  echo "Error: File not found: $ARTICLE"
  exit 1
fi

# Validate English content (simple check)
if ! grep -q "[a-zA-Z]" "$ARTICLE"; then
  echo "Warning: Article may not contain English text"
  read -p "Continue anyway? (y/n): " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
  fi
fi

# Check minimum length
WORD_COUNT=$(wc -w < "$ARTICLE")
if [ $WORD_COUNT -lt 100 ]; then
  echo "Warning: Article is short ($WORD_COUNT words)"
fi

# Publish
node publish.js --file "$ARTICLE" --title "$(basename "$ARTICLE" .md)"
```

Usage:
```bash
chmod +x validate-and-publish.sh
./validate-and-publish.sh posts/my-article.md
```

### Example 15: Markdown to HTML Preview
Create `preview-html.js`:
```javascript
const fs = require('fs');
const { convertMarkdownToHtml } = require('./utils/markdown_to_html');

async function preview(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const html = await convertMarkdownToHtml(content);
  
  // Save preview
  const previewFile = filePath.replace('.md', '.preview.html');
  fs.writeFileSync(previewFile, html);
  console.log(`Preview saved to: ${previewFile}`);
  
  // Also show in console
  console.log('\n=== HTML Preview (first 500 chars) ===');
  console.log(html.substring(0, 500) + '...');
}

// Run if called directly
if (require.main === module) {
  const file = process.argv[2];
  if (!file) {
    console.error('Usage: node preview-html.js <markdown-file>');
    process.exit(1);
  }
  preview(file).catch(console.error);
}

module.exports = { preview };
```

Usage:
```bash
node preview-html.js posts/my-article.md
```

### Example 16: Blog Migration Script
Create `migrate-blog.js`:
```javascript
const fs = require('fs');
const path = require('path');
const { publishArticle } = require('./blogger');

async function migrateFromWordpress(exportFile) {
  const data = JSON.parse(fs.readFileSync(exportFile, 'utf8'));
  
  for (const post of data.posts) {
    // Convert to Markdown
    const markdown = `---
title: "${post.title}"
labels: ${post.categories.join(', ')}
draft: ${post.status === 'draft'}
published: ${post.date}
---

${post.content}`;
    
    // Save as Markdown
    const filename = `posts/${post.slug}.md`;
    fs.writeFileSync(filename, markdown);
    
    // Publish
    console.log(`Migrating: ${post.title}`);
    await publishArticle(filename);
    
    // Delay to avoid rate limits
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

// Run migration
if (require.main === module) {
  const exportFile = process.argv[2];
  migrateFromWordpress(exportFile).catch(console.error);
}
```

## Integration Examples

### Example 17: Integration with Static Site Generator
Create `hugo-to-blogger.js`:
```javascript
const fs = require('fs');
const path = require('path');
const { publishArticle } = require('./blogger');

async function publishFromHugo(contentDir) {
  const files = fs.readdirSync(contentDir);
  
  for (const file of files) {
    if (file.endsWith('.md')) {
      const filePath = path.join(contentDir, file);
      const content = fs.readFileSync(filePath, 'utf8');
      
      // Extract Hugo front matter
      const lines = content.split('\n');
      if (lines[0] === '---') {
        const endIndex = lines.indexOf('---', 1);
        const frontMatter = lines.slice(1, endIndex).join('\n');
        
        // Convert to Blogger format
        const bloggerContent = content.substring(lines.slice(0, endIndex + 1).join('\n').length);
        
        // Create temporary file
        const tempFile = `/tmp/${file}`;
        fs.writeFileSync(tempFile, bloggerContent);
        
        // Publish
        console.log(`Publishing: ${file}`);
        await publishArticle(tempFile);
        
        // Cleanup
        fs.unlinkSync(tempFile);
      }
    }
  }
}
```

### Example 18: Webhook Integration
Create `webhook-server.js`:
```javascript
const express = require('express');
const { publishArticle } = require('./blogger');

const app = express();
app.use(express.json());

app.post('/webhook/blogger/publish', async (req, res) => {
  try {
    const { article, title, labels, draft } = req.body;
    
    // Create temporary Markdown file
    const tempFile = `/tmp/article-${Date.now()}.md`;
    const content = `---
title: "${title}"
labels: "${labels || ''}"
draft: ${draft || false}
---

${article}`;
    
    fs.writeFileSync(tempFile, content);
    
    // Publish
    const result = await publishArticle(tempFile);
    
    // Cleanup
    fs.unlinkSync(tempFile);
    
    res.json({
      success: true,
      postId: result.id,
      url: result.url
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

app.listen(3000, () => {
  console.log('Webhook server listening on port 3000');
});
```

### Example 19: CLI Wrapper Script
Create `blogger-cli`:
```bash
#!/bin/bash
# Blogger CLI wrapper

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "$1" in
  publish)
    node "$SCRIPT_DIR/publish.js" "${@:2}"
    ;;
  list)
    node "$SCRIPT_DIR/list_blogs.js" "${@:2}"
    ;;
  drafts)
    node "$SCRIPT_DIR/delete-all-drafts.js" "${@:2}"
    ;;
  auth)
    node "$SCRIPT_DIR/auth.js" "${@:2}"
    ;;
  *)
    echo "Usage: blogger-cli {publish|list|drafts|auth} [options]"
    echo ""
    echo "Commands:"
    echo "  publish    Publish an article"
    echo "  list       List blogs or posts"
    echo "  drafts     Manage draft posts"
    echo "  auth       Authentication management"
    exit 1
    ;;
esac
```

Make it available system-wide:
```bash
chmod +x blogger-cli
sudo ln -s "$(pwd)/blogger-cli" /usr/local/bin/blogger
```

Usage:
```bash
# Now you can use it from anywhere
blogger publish --file article.md
blogger list
blogger drafts --confirm
```

### Example 20: Docker Container
Create `Dockerfile`:
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Set permissions
RUN chown -R nodejs:nodejs /app
USER nodejs

# Default command
CMD ["node", "index.js"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  blogger-auto-publish:
    build: .
    environment:
      - BLOG_ID=${BLOG_ID}
      - CREDENTIALS_PATH=/app/credentials.json
      - TOKEN_PATH=/app/token.json
    volumes:
      - ./credentials.json:/app/credentials.json:ro
      - ./token.json:/app/token.json
      - ./posts:/app/posts:ro
      - ./logs:/app/logs
    command: node publish.js --file /app/posts/scheduled.md
```

## Troubleshooting Examples

### Example 21: Debug Script
Create `debug-auth.js`:
```javascript
const fs = require('fs');
const { google } = require('googleapis');

async function debugAuth() {
  console.log('=== Debug Authentication ===\n');
  
  // Check credentials file
  try {
    const creds = JSON.parse(fs.readFileSync('./credentials.json', 'utf8'));
    console.log('✓ credentials.json is valid JSON');
    console.log(`  Client ID: ${creds.web.client_id.substring(0, 20)}...`);
  } catch (error) {
    console.log('✗ credentials.json error:', error.message);
  }
  
  // Check token file
  try {
    const token = JSON.parse(fs.readFileSync('./token.json', 'utf8'));
    console.log('✓ token.json is valid JSON');
    
    // Check token expiry
    if (token.expiry_date && token.expiry_date < Date.now()) {
      console.log('⚠ Token expired:', new Date(token.expiry_date).toISOString());
    } else {
      console.log('✓ Token is valid');
    }
  } catch (error) {
    console.log('✗ token.json error:', error.message);
  }
  
  // Test API connection
  try {
    const auth = new google.auth.OAuth2(
      creds.web.client_id,
      creds.web.client_secret,
      creds.web.redirect_uris[0]
    );
    auth.setCredentials(token);
    
    const blogger = google.blogger({ version: 'v3', auth });
    const response = await blogger.blogs.get({ blogId: 'self' });
    console.log('✓ API connection successful');
    console.log(`  Blog: ${response.data.name}`);
  } catch (error) {
    console.log('✗ API connection failed:', error.message);
  }
}

debugAuth().catch(console.error);
```

## Best Practices Summary

1. **Always test with drafts first** before publishing live
2. **Use environment variables** for sensitive data
3. **Implement error handling** and retry logic
4. **Monitor API usage** to avoid rate limits
5. **Keep backups** of your Markdown files
6. **Validate content** before publishing
7. **Use version control** for your articles
8. **Schedule publishing** during low-traffic periods
9. **Regularly clean up** test and draft posts
10. **Review published posts** for formatting issues