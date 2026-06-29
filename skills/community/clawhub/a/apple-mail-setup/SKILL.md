# Apple Mail Channel Setup & Configuration Skill

## Overview
This skill helps you install, configure, and use the Apple Mail channel plugin for OpenClaw and Hermes on macOS.

## Prerequisites
- macOS system (required for Apple Mail and AppleScript)
- Apple Mail.app configured with at least one email account
- Node.js >= 18.0.0
- OpenClaw >= 2026.1.0 or Hermes

## Installation

### Step 1: Install the Plugin

```bash
# Via ClawHub (Recommended)
openclaw plugins install @jehadurre/openclaw-apple-mail

# Or via npm
npm install @jehadurre/openclaw-apple-mail
```

### Step 2: Verify Installation

```bash
openclaw plugins list
# Should show: @jehadurre/openclaw-apple-mail@1.0.1
```

## Configuration

### Basic Configuration

Add to your `openclaw.json` or Hermes config:

```json
{
  "channels": {
    "apple-mail": {
      "enabled": true,
      "accounts": {
        "personal": {
          "email": "your-email@example.com",
          "mailboxAccount": "iCloud",
          "allowFrom": ["*"],
          "pollIntervalMs": 30000,
          "archiveOnReply": false
        }
      }
    }
  }
}
```

### Configuration Options

#### `enabled` (boolean)
- **Default**: `true`
- **Description**: Enable or disable the Apple Mail channel globally

#### `accounts` (object)
Define one or more email accounts to monitor.

##### Per-Account Settings:

**`email`** (string, required)
- Your email address as configured in Apple Mail

**`mailboxAccount`** (string)
- **Default**: `"iCloud"`
- The account name in Apple Mail (e.g., "iCloud", "Gmail", "Work")

**`allowFrom`** (array of strings)
- **Default**: `[]`
- Sender allowlist for security
- Use `["*"]` to allow all senders
- Use `["boss@company.com", "client@domain.com"]` for specific senders

**`pollIntervalMs`** (number)
- **Default**: `30000` (30 seconds)
- How often to check for new emails (in milliseconds)

**`archiveOnReply`** (boolean)
- **Default**: `false`
- Automatically archive email thread after sending reply

### Multi-Account Configuration Example

```json
{
  "channels": {
    "apple-mail": {
      "enabled": true,
      "accounts": {
        "work": {
          "email": "john@company.com",
          "mailboxAccount": "Exchange",
          "allowFrom": ["*"],
          "pollIntervalMs": 15000,
          "archiveOnReply": true
        },
        "personal": {
          "email": "john@gmail.com",
          "mailboxAccount": "Gmail",
          "allowFrom": ["family@domain.com", "friend@email.com"],
          "pollIntervalMs": 60000,
          "archiveOnReply": false
        }
      }
    }
  }
}
```

## Usage

### Starting the Channel

```bash
# Start OpenClaw/Hermes with Apple Mail channel
openclaw start

# Or for Hermes
hermes start
```

The plugin will:
1. Connect to Apple Mail via AppleScript
2. Monitor configured mailboxes
3. Create isolated sessions per email thread
4. Allow AI agents to read and respond to emails

### Testing the Setup

Send a test email to one of your configured accounts. OpenClaw/Hermes should:
- Detect the new email
- Create a session for the thread
- Process according to your agent configuration

### Monitoring

```bash
# Check OpenClaw logs
openclaw logs

# Check active sessions
openclaw sessions list
```

## Features

### Per-Thread Session Isolation
Each email thread gets its own isolated session, preventing context mixing between conversations.

### HTML Processing
- Automatically extracts and cleans HTML email content
- Converts tables to markdown
- Sanitizes potentially malicious content
- Preserves formatting for AI agents

### Smart Threading
- Maintains conversation context across replies
- Groups related emails together
- Handles Re: and Fwd: prefixes correctly

### Security
- Sender allowlist per account
- HTML sanitization
- AppleScript sandboxing

## Troubleshooting

### Issue: Plugin not found
```bash
# Reinstall
npm install -g @jehadurre/openclaw-apple-mail
openclaw plugins install @jehadurre/openclaw-apple-mail
```

### Issue: AppleScript permissions denied
1. Open **System Preferences → Security & Privacy → Privacy**
2. Select **Automation**
3. Enable access for Terminal/OpenClaw to control Mail.app

### Issue: Emails not detected
- Verify `email` matches exactly as configured in Mail.app
- Check `mailboxAccount` name matches the account in Mail.app
- Ensure Mail.app is running
- Check `allowFrom` settings

### Issue: Cannot send replies
- Verify account has send permissions in Mail.app
- Check Mail.app can send emails manually
- Review OpenClaw logs for errors

## Advanced Configuration

### Custom Polling Intervals per Account

For high-priority work email:
```json
{
  "work": {
    "email": "urgent@company.com",
    "pollIntervalMs": 5000  // Check every 5 seconds
  }
}
```

For low-priority personal email:
```json
{
  "personal": {
    "email": "casual@gmail.com",
    "pollIntervalMs": 300000  // Check every 5 minutes
  }
}
```

### Strict Sender Filtering

Only allow specific clients and your boss:
```json
{
  "work": {
    "email": "sales@company.com",
    "allowFrom": [
      "boss@company.com",
      "client1@bigcorp.com",
      "client2@enterprise.com"
    ]
  }
}
```

### Auto-Archive for Customer Support

Automatically archive threads after replying:
```json
{
  "support": {
    "email": "support@company.com",
    "archiveOnReply": true,
    "pollIntervalMs": 10000
  }
}
```

## API Reference

### Channel ID
`apple-mail`

### Configuration Schema
See `openclaw.plugin.json` for full JSON schema.

### Events
- `email:received` - New email detected
- `email:sent` - Reply sent successfully
- `session:created` - New thread session created
- `session:archived` - Thread archived

## Links

- **npm**: https://www.npmjs.com/package/@jehadurre/openclaw-apple-mail
- **GitHub**: https://github.com/JehadurRE/openclaw-apple-mail
- **Documentation**: https://openclaw-apple-mail.jehadurre.me
- **Issues**: https://github.com/JehadurRE/openclaw-apple-mail/issues
- **Author**: Md. Jehadur Rahman (Emran) - https://jehadurre.me

## Support

For issues, questions, or contributions:
1. Check the [GitHub Issues](https://github.com/JehadurRE/openclaw-apple-mail/issues)
2. Read the [Contributing Guide](https://github.com/JehadurRE/openclaw-apple-mail/blob/master/CONTRIBUTING.md)
3. Contact the author via [Dev.to @jehadurre](https://dev.to/jehadurre)

## License

MIT License - See [LICENSE](https://github.com/JehadurRE/openclaw-apple-mail/blob/master/LICENSE)

---

**Version**: 1.0.1  
**Author**: Md. Jehadur Rahman (Emran)  
**Last Updated**: June 2026
