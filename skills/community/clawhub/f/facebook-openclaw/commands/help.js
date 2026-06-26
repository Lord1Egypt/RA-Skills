#!/usr/bin/env node
/**
 * Display help information
 * Usage: openclaw-facebook-posting --help
 */

module.exports = async () => {
  console.log(`
📘 Facebook Page Posting CLI
=============================

A command-line tool for posting to Facebook Pages via the Graph API.

📋 Commands:
------------
  fb-post-setup <page_id> <access_token> [page_name]
      Configure Facebook Page credentials

  fb-post "<message>"
      Post a text message to your Page

  fb-post-image "<caption>" "<image_url>"
      Post an image with caption to your Page

  fb-post-schedule "<message>" "<scheduled_time>"
      Schedule a post for later (ISO 8601 format)
      Example: "2024-04-20T10:00:00Z"

  fb-post-schedule-list
      List all scheduled posts

  fb-post-schedule-delete <post_id>
      Delete a scheduled post

  fb-post-delete <post_id>
      Delete a post from your Page (may fail due to API deprecation)

  fb-post-hide <post_id>
      Hide (unpublish) a post from your Page
      Recommended alternative to deletion since Facebook deprecated direct deletion (v2.4+)

  fb-post-test
      Test connection and verify credentials

  fb-config-show
      Show current configuration

  --help, -h
      Show this help message

🔑 Getting Started:
-------------------
1. Get a Page Access Token from Facebook Developer Console
   - Required permissions: pages_manage_posts, pages_read_engagement

2. Setup the configuration:
   openclaw-facebook-posting fb-post-setup <page_id> <access_token>

3. Start posting:
   openclaw-facebook-posting fb-post "Hello, Facebook!"

📚 Documentation:
-----------------
Facebook Graph API: https://developers.facebook.com/docs/graph-api/
Page Posts: https://developers.facebook.com/docs/graph-api/reference/page/posts/

💡 Tips:
--------
- Access tokens may expire. Re-run setup if you get authentication errors.
- Use fb-post-test to verify your credentials before posting.
- Scheduled posts use server time (UTC).

`);
};

// CLI entry point
if (require.main === module) {
  module.exports();
}
