#!/usr/bin/env node
/**
 * OpenClaw Command: fb-post-setup-help
 * Display Facebook Page posting setup guide.
 * 
 * Usage:
 *   openclaw fb-post-setup-help
 */

const { Command } = require('commander');

const program = new Command();

program
  .name('fb-post-setup-help')
  .description('Display Facebook Page posting setup guide')
  .action(() => {
    console.log(`
📘 Facebook Page Posting - Complete Setup Guide

This guide will help you set up Facebook Page posting with OpenClaw.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Create a Facebook App (if you don't have one)

  1. Go to: https://developers.facebook.com/
  2. Click "My Apps" → "Create App"
  3. Choose "Other" → "Next"
  4. Give your app a name → "Create App"
  5. Skip the "Add Products to Your App" for now

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 2: Get Your Page Access Token

  1. Go to: https://developers.facebook.com/tools/explorer/
  2. Select your app from the dropdown
  3. Click "Get Token" → "Get Page Access Token"
  4. Select these permissions:
     • pages_manage_posts (create and manage posts)
     • pages_read_engagement (read page content)
     • pages_show_list (list your pages)
  5. Click "Continue"
  6. Select the Page you want to post from
  7. Click "Continue" → "Done"
  8. Copy the generated token (starts with EAAB...)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 3: Find Your Page ID

  Option A - From Facebook:
    1. Go to your Facebook Page
    2. Click "About" → "Page Info"
    3. Find "Page ID"

  Option B - From Graph API:
    1. Go to: https://graph.facebook.com/me/accounts?access_token=YOUR_TOKEN
    2. Find your Page in the list
    3. Copy the "id" field

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 4: Run the Setup Command

  openclaw fb-post-setup <page_id> "<access_token>" "Page Name"

  Example:
    openclaw fb-post-setup "123456789" "EAAB...token..." "My Business Page"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 5: Test Your Connection

  openclaw fb-post-test

  This will verify:
    ✓ Configuration file exists
    ✓ API connectivity
    ✓ Page access
    ✓ Post permissions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 6: Start Posting!

  Post immediately:
    openclaw fb-post "Hello from OpenClaw!"

  Post an image:
    openclaw fb-post-image "Check this out!" "https://example.com/image.jpg"

  Schedule a post:
    openclaw fb-post-schedule "Tomorrow's post!" "tomorrow 9am"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Time Formats for Scheduled Posts

  Natural language:
    "tomorrow 9am"
    "next monday 10am"
    "in 2 hours"
    "in 30 minutes"
    "next week"
    "next month"

  ISO format:
    "2024-12-31T23:59:59Z"
    "2024-12-31 23:59:59"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Available Commands

  Setup & Configuration:
    openclaw fb-post-setup <page_id> <access_token> [page_name]
    openclaw fb-post-setup-help
    openclaw fb-post-test

  Posting:
    openclaw fb-post "<message>"
    openclaw fb-post-image "<caption>" "<url>"

  Scheduling:
    openclaw fb-post-schedule "<message>" "<time>"
    openclaw fb-post-schedule-list
    openclaw fb-post-schedule-delete <post_id>

  Management:
    openclaw fb-post-drafts
    openclaw fb-post-delete <post_id>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Security Notes

  • Never share your access token
  • Store it securely in your workspace
  • Page tokens last 60 days
  • Regenerate if compromised
  • Use Page tokens, not User tokens

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Troubleshooting

  Error 190 (Token Expired):
    • Regenerate token at https://developers.facebook.com/tools/explorer/
    • Page tokens last 60 days

  Error 10 (Missing Permissions):
    • Regenerate token with required permissions
    • Make sure you selected the correct Page

  Invalid Page ID:
    • Verify the Page ID is correct
    • Check that the token has access to that Page

  "User has not authorized the app":
    • You must be an admin of the Page
    • Re-authorize with the correct Page selected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Resources

  • Facebook Graph API: https://developers.facebook.com/docs/pages/
  • Graph API Explorer: https://developers.facebook.com/tools/explorer/
  • OpenClaw Docs: https://docs.openclaw.ai
  • OpenClaw Discord: https://discord.com/invite/clawd

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to get started?

  1. Get your token and page ID
  2. Run: openclaw fb-post-setup <page_id> "<token>" "Page Name"
  3. Test: openclaw fb-post-test
  4. Post: openclaw fb-post "Hello!"

Happy posting! 🚀
    `);
  });

program.parse();
