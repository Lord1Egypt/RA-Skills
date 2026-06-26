# Blogger Auto-Publish Skill Setup Guide

## Prerequisites

1. **Google Account** with access to Blogger
2. **Google Cloud Project** with Blogger API enabled
3. **Node.js** 14.0.0 or higher

## Step 1: Google Cloud Setup

### 1.1 Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project" or select existing
3. Name your project (e.g., "blogger-auto-publish")

### 1.2 Enable Blogger API
1. In the Cloud Console, go to **APIs & Services** > **Library**
2. Search for "Blogger API"
3. Click "Enable"

### 1.3 Create OAuth 2.0 Credentials
1. Go to **APIs & Services** > **Credentials**
2. Click "Create Credentials" > "OAuth 2.0 Client ID"
3. Application type: **Web application**
4. Name: "Blogger Auto-Publish"
5. Authorized redirect URIs: `http://localhost`
6. Click "Create"

### 1.4 Download Credentials
1. Click the download icon next to your new OAuth client
2. Save as `credentials.json`
3. Rename to `credentials-example.json` and replace placeholder values

## Step 2: Get Your Blog ID

### Method 1: From Blogger URL
1. Go to your Blogger dashboard
2. Click on your blog
3. Look at the URL: `https://www.blogger.com/blog/posts/1234567890123456789`
4. The number at the end is your Blog ID

### Method 2: Using the Script
```bash
# After setting up credentials, run:
node find-blog-id.js
```

## Step 3: Install Dependencies

```bash
npm install googleapis@latest
```

## Step 4: Configure the Skill

### 4.1 Update config.js
Edit `config.js` and set:
```javascript
blogId: "YOUR_ACTUAL_BLOG_ID"
```

### 4.2 Update credentials-example.json
Replace all placeholder values with your actual Google API credentials.

### 4.3 Rename the file
```bash
mv credentials-example.json credentials.json
```

## Step 5: First-Time Authorization

```bash
# Run the authorization script
node auth.js login

# Or use the complete auth script
node complete-auth.js
```

This will open a browser window. Log in with your Google account and grant permissions.

## Step 6: Test the Skill

```bash
# Test API connection
node test-publish.js

# Publish a test article
node publish.js --file posts/example-post.md --draft
```

## Step 7: Create Your Own Articles

1. Create Markdown files in the `posts/` directory
2. Add frontmatter metadata:
```markdown
---
title: Your Article Title
labels: tag1, tag2, tag3
draft: false
---

# Your Content Here
```

3. Publish:
```bash
node publish.js --file posts/your-article.md
```

## Troubleshooting

### Common Issues

1. **"Invalid credentials"**
   - Check that `credentials.json` has correct values
   - Ensure Blogger API is enabled in Google Cloud

2. **"Blog not found"**
   - Verify your Blog ID is correct
   - Ensure you have write permissions on the blog

3. **OAuth errors**
   - Delete `token.json` and re-run authorization
   - Check redirect URI matches Google Cloud Console

### Getting Help

- Check the `references/` directory for detailed guides
- Review error messages in console
- Ensure all environment variables are set correctly