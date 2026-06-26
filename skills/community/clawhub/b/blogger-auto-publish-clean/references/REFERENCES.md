# API Reference

## Google Blogger API v3

This skill uses the official Google Blogger API v3. Below are the key endpoints and methods used.

### Authentication

The skill uses OAuth 2.0 for authentication. The flow is:

1. User authorizes the application via browser
2. Google returns an authorization code
3. Code is exchanged for access and refresh tokens
4. Tokens are stored in `token.json` for future use

### Key API Endpoints

#### 1. Blogs Resource
- `GET /blogs/{blogId}` - Get blog information
- `GET /blogs/{blogId}/posts` - List blog posts
- `POST /blogs/{blogId}/posts` - Create new post
- `GET /blogs/{blogId}/posts/{postId}` - Get specific post
- `PUT /blogs/{blogId}/posts/{postId}` - Update post
- `DELETE /blogs/{blogId}/posts/{postId}` - Delete post

#### 2. Posts Resource
- `GET /posts` - List posts across all blogs (requires `blogger` scope)
- `GET /posts/bypath` - Get post by path

### Request/Response Examples

#### Create Post Request
```json
{
  "kind": "blogger#post",
  "blog": {
    "id": "8070105920543249955"
  },
  "title": "My New Post",
  "content": "<p>This is the HTML content of my post.</p>",
  "labels": ["technology", "tutorial"],
  "status": "draft"
}
```

#### Create Post Response
```json
{
  "kind": "blogger#post",
  "id": "8070105920543249955_123456789",
  "blog": {
    "id": "8070105920543249955"
  },
  "published": "2026-03-28T06:47:00-07:00",
  "updated": "2026-03-28T06:47:00-07:00",
  "url": "https://www.blogger.com/feeds/8070105920543249955/posts/default/123456789",
  "selfLink": "https://www.googleapis.com/blogger/v3/blogs/8070105920543249955/posts/123456789",
  "title": "My New Post",
  "content": "<p>This is the HTML content of my post.</p>",
  "labels": ["technology", "tutorial"],
  "status": "draft"
}
```

### Rate Limits

Google Blogger API has the following limits:

- **Queries per day**: 50,000 (default, can be increased)
- **Queries per 100 seconds per user**: 1,000
- **Queries per 100 seconds**: 10,000

### Error Codes

| Code | Meaning | Suggested Action |
|------|---------|------------------|
| 400 | Bad Request | Check request parameters |
| 401 | Unauthorized | Re-authenticate |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Verify resource exists |
| 429 | Too Many Requests | Wait and retry |
| 500 | Internal Server Error | Retry later |

## Node.js Google APIs Library

### Installation
```bash
npm install googleapis@latest
```

### Initialization
```javascript
const { google } = require('googleapis');
const blogger = google.blogger('v3');
```

### Authentication Methods

#### 1. OAuth2 Client
```javascript
const { OAuth2Client } = require('google-auth-library');
const oauth2Client = new OAuth2Client(
  clientId,
  clientSecret,
  redirectUri
);
```

#### 2. Service Account (Not used in this skill)
```javascript
const auth = new google.auth.GoogleAuth({
  keyFile: 'path/to/service-account-key.json',
  scopes: ['https://www.googleapis.com/auth/blogger']
});
```

### Key Methods

#### List Blogs
```javascript
async function listBlogs(auth) {
  const res = await blogger.blogs.list({
    auth: auth,
    userId: 'self'
  });
  return res.data.items;
}
```

#### Create Post
```javascript
async function createPost(auth, blogId, postData) {
  const res = await blogger.posts.insert({
    auth: auth,
    blogId: blogId,
    requestBody: postData
  });
  return res.data;
}
```

#### List Posts
```javascript
async function listPosts(auth, blogId) {
  const res = await blogger.posts.list({
    auth: auth,
    blogId: blogId,
    maxResults: 50
  });
  return res.data.items;
}
```

## Environment Variables

### Required Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `BLOG_ID` | Your Blogger blog ID | `YOUR_BLOG_ID_HERE` |
| `CREDENTIALS_PATH` | Path to credentials.json | `./credentials.json` |
| `TOKEN_PATH` | Path to token.json | `./token.json` |

### Optional Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `POSTS_DIR` | Directory for Markdown posts | `./posts` |
| `MAX_RETRIES` | Maximum retry attempts | `3` |
| `RETRY_DELAY` | Delay between retries (ms) | `1000` |
| `LOG_LEVEL` | Logging level | `info` |

## Configuration File (config.js)

### Default Configuration
```javascript
module.exports = {
  // Required
  blogId: process.env.BLOG_ID || null,
  
  // File paths
  credentialsPath: process.env.CREDENTIALS_PATH || './credentials.json',
  tokenPath: process.env.TOKEN_PATH || './token.json',
  postsDir: process.env.POSTS_DIR || './posts',
  
  // API settings
  maxRetries: parseInt(process.env.MAX_RETRIES) || 3,
  retryDelay: parseInt(process.env.RETRY_DELAY) || 1000,
  
  // Content settings
  defaultLabels: ['auto-published'],
  convertMarkdown: true,
  validateEnglish: true,
  
  // Logging
  logLevel: process.env.LOG_LEVEL || 'info',
  logFile: process.env.LOG_FILE || './logs/blogger.log'
};
```

## Markdown Processing

### Supported Markdown Features
- Headers (#, ##, ###)
- Lists (ordered and unordered)
- Links and images
- Code blocks (with syntax highlighting)
- Blockquotes
- Tables
- Horizontal rules

### Front Matter Support
Articles can include YAML front matter:

```yaml
---
title: My Article Title
labels: technology, programming, tutorial
draft: true
custom_field: value
---
```

### HTML Conversion
The skill uses a Markdown-to-HTML converter that:
1. Parses Markdown with front matter
2. Converts to clean HTML
3. Preserves code formatting
4. Handles special characters

## Error Handling

### Retry Logic
The skill includes automatic retry for:
- Network timeouts
- Rate limit errors (429)
- Temporary server errors (5xx)

### Logging
Four log levels are supported:
1. **error** - Critical failures
2. **warn** - Warnings and issues
3. **info** - General information
4. **debug** - Detailed debugging

### Error Recovery
- Failed posts are logged for manual review
- Partial failures don't stop batch processing
- Configuration errors are caught early

## Security Considerations

### Token Storage
- `token.json` contains sensitive OAuth tokens
- File should have restricted permissions (600)
- Refresh tokens are automatically used
- Tokens expire and require re-authorization

### Credential Management
- `credentials.json` should never be committed to git
- Use environment variables for production
- Rotate credentials periodically
- Monitor API usage in Google Cloud Console

### Best Practices
1. Use separate Google Cloud projects for development/production
2. Restrict API keys to specific IP ranges if possible
3. Monitor usage and set up alerts for unusual activity
4. Regularly review authorized applications in Google Account

## Performance Tips

### Batch Processing
- Process 5-10 articles at a time
- Add delays between API calls
- Use async/await for better flow control

### Caching
- Cache blog information to reduce API calls
- Store post IDs for future updates
- Keep local copy of published articles

### Monitoring
- Track API quota usage
- Monitor error rates
- Log processing times for optimization

## Migration and Backup

### Exporting Data
```bash
# Export all posts as JSON
node export-posts.js --format json --output posts-backup.json

# Export as Markdown
node export-posts.js --format markdown --output posts-backup/
```

### Importing Data
```bash
# Import from JSON backup
node import-posts.js --file posts-backup.json

# Import from Markdown directory
node import-posts.js --dir posts-backup/
```

## Related Resources

### Official Documentation
- [Google Blogger API v3 Reference](https://developers.google.com/blogger/docs/3.0/reference)
- [Google APIs Node.js Client](https://github.com/googleapis/google-api-nodejs-client)
- [OAuth 2.0 for Web Applications](https://developers.google.com/identity/protocols/oauth2/web-server)

### Community Resources
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills)
- [Blogger Developer Forum](https://support.google.com/blogger/community)
- [Stack Overflow - Blogger API](https://stackoverflow.com/questions/tagged/blogger-api)

### Tools and Libraries
- [Markdown-it](https://github.com/markdown-it/markdown-it) - Markdown parser
- [YAML](https://github.com/nodeca/js-yaml) - YAML parser for front matter
- [Winston](https://github.com/winstonjs/winston) - Logging library