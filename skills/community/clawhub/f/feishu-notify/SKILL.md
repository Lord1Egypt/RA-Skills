---
name: feishu-notify
description: This skill should be used when users need to send notifications to Feishu (Lark) via webhook. It supports multiple message types including text, rich text, interactive cards, and images. Users must configure webhook URLs in ~/.openclaw/skills/feishu-notify/config.json before using this skill.
---

# Feishu Notify Skill

This skill enables sending notifications to Feishu (Lark) using webhook URLs. It supports various message types including text messages, rich text posts, interactive cards, and images.

## Configuration Requirements

**IMPORTANT**: Before using this skill, you must configure your Feishu webhook URLs:

Create the configuration file at `~/.openclaw/skills/feishu-notify/config.json` with the following content:

```json
{
  "webhooks": {
    "default": "https://open.feishu.cn/open-apis/bot/v2/hook/your-webhook-url",
    "alerts": "https://open.feishu.cn/open-apis/bot/v2/hook/your-alerts-webhook-url",
    "notifications": "https://open.feishu.cn/open-apis/bot/v2/hook/your-notifications-webhook-url"
  }
}
```

### Configuration Structure

- **default**: Default webhook URL used when no specific webhook is specified
- **alerts**: Webhook URL for alert messages
- **notifications**: Webhook URL for general notifications
- **custom**: You can add as many custom webhooks as needed (e.g., "devops", "finance", "marketing")

### Configuration Priority

The skill loads configuration from:
- User's config.json at `~/.openclaw/skills/feishu-notify/config.json` (only source)

## When to Use This Skill

Activate this skill when:
- Users want to send notifications to Feishu groups
- Users need to send alerts or notifications to Feishu
- Users mention "send to Feishu", "notify Feishu", or "message Feishu"
- Users want to send different types of messages (text, card, image) to Feishu

## Skill Components

### Scripts

The `scripts/send_message.py` script provides a reliable way to send messages to Feishu via webhook. This script:
- Loads webhook URLs from user's config.json file
- Supports multiple message types (text, post, interactive, image)
- Handles message templates from templates directory (with security restrictions)
- Provides error handling and response validation

### Templates

The `templates/` directory contains message templates for different scenarios:
- **text_simple.json**: Simple text message template
- **post_rich.json**: Rich text (post) message template
- **card_alert.json**: Interactive card for alerts
- **card_notification.json**: Interactive card for notifications
- **card_task.json**: Interactive card for task updates

### References

The `references/api_documentation.md` contains documentation about Feishu webhook API, including:
- Webhook authentication and format
- Supported message types and structures
- Message template specifications
- Error handling and response codes

## Workflow

When this skill is activated:

1. **Check configuration** - Verify that `~/.openclaw/skills/feishu-notify/config.json` exists and contains valid webhook URLs. If not, prompt user to configure it.

2. **Determine message type** based on user's request:
   - **Text message**: For simple text notifications
   - **Post (Rich text)**: For formatted messages with elements
   - **Interactive card**: For rich cards with buttons, images, and structured content
   - **Image message**: For sending image URLs

3. **Select webhook** based on context:
   - Use "default" if no specific webhook is mentioned
   - Use named webhooks (e.g., "alerts", "notifications") if specified
   - Use custom webhooks if provided by name

4. **Build or load message**:
   - Use a predefined template from templates directory
   - Or build a custom message based on user's content
   - Fill in template variables with user-provided data

5. **Send message** using webhook URL:
   - Run `scripts/send_message.py` with webhook name and message type
   - The script loads appropriate webhook URL from config.json
   - Returns delivery status and response

6. **Present results** to user:
   - Confirm message delivery status
   - Display any errors if delivery failed
   - Provide feedback on what was sent

## Important Notes

- Feishu webhooks use POST method with JSON body
- Each webhook URL is specific to a Feishu group/chat
- Message types include: "text", "post", "interactive", "image"
- Webhook URLs are **secrets** and should be kept secure
  - Never commit `config.json` to version control
  - Set file permissions to restrict access (chmod 600 on Unix/Linux)
  - Treat webhook URLs like API keys
- Message size limit: 200KB for most message types
- Interactive cards support buttons, images, markdown, and more
- The script validates the response from Feishu API
- Template loading is restricted to the `templates/` directory for security
- The agent can call this skill autonomously (messages may be sent without explicit confirmation)

## Message Types

### 1. Text Message
Simple text-only messages.
```json
{
  "msg_type": "text",
  "content": {
    "text": "Your message here"
  }
}
```

### 2. Post (Rich Text) Message
Messages with rich formatting including text, links, @mentions, images, and more.

### 3. Interactive Card Message
Rich cards with structured content, buttons, images, and interactive elements.

### 4. Image Message
Messages with image URLs (image_key or image_url).

## Example Interactions

User: "Send a notification to Feishu: 'Deployment completed successfully'"
Action: Use "default" webhook, send text message with provided text

User: "Send an alert to Feishu about server error: 'Connection timeout'"
Action: Use "alerts" webhook, use card_alert template with error details

User: "Send a task update to Feishu: Task #123 completed by John"
Action: Use "notifications" webhook, use card_task template with task information

User: "Send a rich message to devops webhook about deployment status"
Action: Use "devops" webhook, use post_rich template with deployment details

User: "Notify the team about the meeting at 3 PM"
Action: Use "default" webhook, send text message with meeting details

## Error Handling

If configuration is missing:
- Inform user that webhook URLs need to be configured
- Provide instructions on creating `~/.openclaw/skills/feishu-notify/config.json`
- Show required JSON format
- Remind user to keep webhook URLs secret

If webhook is not found:
- Check if the specified webhook name exists in config
- Suggest using "default" webhook or adding the named webhook

If message sending fails:
- Check if the webhook URL is valid
- Verify network connectivity
- Display error message from Feishu API
- Suggest checking the webhook configuration

If template loading fails:
- Ensure the template file is within the `templates/` directory
- For security reasons, arbitrary JSON files cannot be used as templates
- Use predefined templates or add new ones to the `templates/` directory

## Template Usage

Templates are stored in the `templates/` directory with JSON format. Each template includes:
- Message type definition
- Content structure with placeholders
- Variable replacement support

**Security**: For security reasons, template loading is restricted to the `templates/` directory only. Arbitrary JSON files cannot be used as templates.

To use a template:
1. Select the appropriate template based on the message type
2. Replace placeholder variables with actual content
3. Send using the `send_message.py` script with the template path

**Note**: When adding custom templates, place them in the `templates/` directory to ensure they can be loaded by the script.
