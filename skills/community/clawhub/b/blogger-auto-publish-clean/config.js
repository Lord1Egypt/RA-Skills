// Blogger Auto-Publish Configuration
// IMPORTANT: Replace with your own credentials before use!

module.exports = {
  // Blog ID (required) - get from your Blogger URL
  // Example: https://www.blogger.com/blog/posts/1234567890123456789
  blogId: process.env.BLOG_ID || "YOUR_BLOG_ID_HERE",
  
  // Path to Google API credentials
  credentialsPath: process.env.CREDENTIALS_PATH || "./credentials-example.json",
  
  // Path to store OAuth token
  tokenPath: process.env.TOKEN_PATH || "./token.json",
  
  // Directory containing Markdown posts
  postsDir: process.env.POSTS_DIR || "./posts",
  
  // API settings
  maxRetries: 3,
  retryDelay: 1000,
  
  // Blogger API scopes
  scopes: [
    'https://www.googleapis.com/auth/blogger'
  ],
  
  // Redirect URI for OAuth
  redirectUri: process.env.REDIRECT_URI || "http://localhost"
};