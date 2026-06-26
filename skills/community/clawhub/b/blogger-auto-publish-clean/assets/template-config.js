// Blogger Auto-Publish Configuration Template
// Copy this file to config.js and update with your values

module.exports = {
  // ============================================
  // REQUIRED SETTINGS
  // ============================================
  
  // Your Blogger blog ID
  // Find this in Blogger URL or use find-blog-id.js script
  blogId: process.env.BLOG_ID || "YOUR_BLOG_ID_HERE",
  
  // ============================================
  // FILE PATHS
  // ============================================
  
  // Path to Google API credentials file
  // Download from Google Cloud Console
  credentialsPath: process.env.CREDENTIALS_PATH || "./credentials.json",
  
  // Path to OAuth token file
  // Generated automatically after first authorization
  tokenPath: process.env.TOKEN_PATH || "./token.json",
  
  // Directory containing Markdown articles to publish
  postsDir: process.env.POSTS_DIR || "./posts",
  
  // Log file path (optional)
  logFile: process.env.LOG_FILE || "./logs/blogger.log",
  
  // ============================================
  // API SETTINGS
  // ============================================
  
  // Maximum number of retry attempts for API calls
  maxRetries: parseInt(process.env.MAX_RETRIES) || 3,
  
  // Delay between retries in milliseconds
  retryDelay: parseInt(process.env.RETRY_DELAY) || 1000,
  
  // Timeout for API requests in milliseconds
  timeout: parseInt(process.env.TIMEOUT) || 30000,
  
  // ============================================
  // CONTENT SETTINGS
  // ============================================
  
  // Default labels/tags for all posts
  // Can be overridden in article front matter
  defaultLabels: process.env.DEFAULT_LABELS 
    ? process.env.DEFAULT_LABELS.split(',') 
    : ['auto-published'],
  
  // Automatically convert Markdown to HTML
  convertMarkdown: process.env.CONVERT_MARKDOWN !== 'false',
  
  // Validate that content contains English text
  // Set to false for non-English blogs
  validateEnglish: process.env.VALIDATE_ENGLISH !== 'false',
  
  // Default post status
  // 'draft' or 'live' (published)
  defaultStatus: process.env.DEFAULT_STATUS || 'draft',
  
  // Automatically generate slugs from titles
  generateSlugs: process.env.GENERATE_SLUGS !== 'false',
  
  // ============================================
  // PUBLISHING SETTINGS
  // ============================================
  
  // Publish date handling
  // 'now' - Use current date/time
  // 'file' - Use date from file front matter
  // 'scheduled' - Schedule for future
  publishDate: process.env.PUBLISH_DATE || 'now',
  
  // Timezone for publishing dates
  timezone: process.env.TIMEZONE || 'UTC',
  
  // Delay between publishing multiple articles (ms)
  // Helps avoid rate limiting
  publishDelay: parseInt(process.env.PUBLISH_DELAY) || 2000,
  
  // Maximum articles to publish in one batch
  maxBatchSize: parseInt(process.env.MAX_BATCH_SIZE) || 10,
  
  // ============================================
  // LOGGING SETTINGS
  // ============================================
  
  // Log level: error, warn, info, debug
  logLevel: process.env.LOG_LEVEL || 'info',
  
  // Log to console
  logToConsole: process.env.LOG_TO_CONSOLE !== 'false',
  
  // Log to file
  logToFile: process.env.LOG_TO_FILE !== 'false',
  
  // Log format: 'simple', 'json', 'detailed'
  logFormat: process.env.LOG_FORMAT || 'simple',
  
  // ============================================
  // ADVANCED SETTINGS
  // ============================================
  
  // Custom HTML template for posts
  // Set to null to use default Blogger formatting
  htmlTemplate: process.env.HTML_TEMPLATE || null,
  
  // Custom CSS to inject into posts
  customCss: process.env.CUSTOM_CSS || '',
  
  // Enable/disable features
  features: {
    // Enable image upload to Blogger
    uploadImages: process.env.UPLOAD_IMAGES !== 'false',
    
    // Enable link validation
    validateLinks: process.env.VALIDATE_LINKS !== 'false',
    
    // Enable content length validation
    validateLength: process.env.VALIDATE_LENGTH !== 'false',
    
    // Enable duplicate detection
    detectDuplicates: process.env.DETECT_DUPLICATES !== 'false',
    
    // Enable automatic tagging based on content
    autoTagging: process.env.AUTO_TAGGING !== 'false',
  },
  
  // ============================================
  // SECURITY SETTINGS
  // ============================================
  
  // Require confirmation before publishing
  requireConfirmation: process.env.REQUIRE_CONFIRMATION === 'true',
  
  // Dry run mode (test without actually publishing)
  dryRun: process.env.DRY_RUN === 'true',
  
  // Backup published articles locally
  backupPublished: process.env.BACKUP_PUBLISHED !== 'false',
  
  // Backup directory
  backupDir: process.env.BACKUP_DIR || './backups',
  
  // ============================================
  // INTEGRATION SETTINGS
  // ============================================
  
  // Webhook URL for notifications
  webhookUrl: process.env.WEBHOOK_URL || null,
  
  // Email notifications
  emailNotifications: {
    enabled: process.env.EMAIL_NOTIFICATIONS === 'true',
    to: process.env.EMAIL_TO || '',
    from: process.env.EMAIL_FROM || 'blogger-auto-publish@example.com',
  },
  
  // Slack/Discord notifications
  chatNotifications: {
    enabled: process.env.CHAT_NOTIFICATIONS === 'true',
    webhook: process.env.CHAT_WEBHOOK || '',
  },
  
  // ============================================
  // DEBUG SETTINGS
  // ============================================
  
  // Enable debug mode for troubleshooting
  debug: process.env.DEBUG === 'true',
  
  // Save API responses for debugging
  saveApiResponses: process.env.SAVE_API_RESPONSES === 'true',
  
  // API response directory
  apiResponsesDir: process.env.API_RESPONSES_DIR || './debug/api-responses',
  
  // ============================================
  // DEPRECATED SETTINGS (for backward compatibility)
  // ============================================
  
  // Old setting names mapped to new ones
  _compat: {
    // blog_id -> blogId
    blog_id: function() { return this.blogId; },
    
    // credentials_file -> credentialsPath
    credentials_file: function() { return this.credentialsPath; },
    
    // token_file -> tokenPath
    token_file: function() { return this.tokenPath; },
  }
};

// Helper function to get configuration with environment overrides
function getConfig() {
  const config = module.exports;
  
  // Apply environment variable overrides
  for (const key in config) {
    if (typeof config[key] === 'string' && config[key].startsWith('process.env.')) {
      const envVar = config[key].replace('process.env.', '');
      if (process.env[envVar]) {
        config[key] = process.env[envVar];
      }
    }
  }
  
  return config;
}

// Export helper function
module.exports.getConfig = getConfig;

// Export default configuration
module.exports.default = module.exports;