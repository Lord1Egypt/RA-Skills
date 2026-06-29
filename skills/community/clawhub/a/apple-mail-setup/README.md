# Apple Mail Channel Setup Skill

[![npm version](https://badge.fury.io/js/@jehadurre%2Fopenclaw-apple-mail-skill.svg)](https://www.npmjs.com/package/@jehadurre/openclaw-apple-mail-skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: macOS](https://img.shields.io/badge/Platform-macOS-blue.svg)](https://www.apple.com/macos)

OpenClaw skill for installing, configuring, and using the **Apple Mail channel plugin** with comprehensive setup instructions and examples.

## What is this?

This is an **OpenClaw Skill** that provides step-by-step guidance for setting up and using the `@jehadurre/openclaw-apple-mail` channel plugin. Skills help users quickly understand and implement complex features.

## Installation

### Install the Skill

```bash
# Via ClawHub (Recommended)
openclaw skills install @jehadurre/openclaw-apple-mail-skill

# Or via npm
npm install @jehadurre/openclaw-apple-mail-skill
```

### What You Get

- 📖 **Comprehensive documentation** on setup and configuration
- ⚙️ **Configuration examples** for common use cases
- 🛠️ **Troubleshooting guide** for common issues
- 💡 **Best practices** for multi-account setups
- 🚀 **Quick start templates** ready to customize

## Quick Start

After installing the skill, activate it in OpenClaw:

```bash
openclaw skills activate apple-mail-setup
```

Then follow the interactive prompts or read the full documentation:

```bash
openclaw skills docs apple-mail-setup
```

## What the Skill Covers

### 1. Installation
- Installing the Apple Mail plugin via ClawHub or npm
- Verifying successful installation
- System requirements and prerequisites

### 2. Configuration
- Basic single-account setup
- Multi-account configuration
- Advanced options (polling intervals, allowlists, auto-archive)

### 3. Usage
- Starting and monitoring the channel
- Testing email detection
- Viewing active sessions

### 4. Troubleshooting
- AppleScript permission issues
- Email detection problems
- Sending reply failures
- Common configuration errors

### 5. Advanced Topics
- Per-account polling intervals
- Strict sender filtering
- Auto-archiving for customer support
- HTML processing and sanitization

## Configuration Examples

### Basic Setup

```json
{
  "channels": {
    "apple-mail": {
      "enabled": true,
      "accounts": {
        "personal": {
          "email": "your-email@example.com",
          "mailboxAccount": "iCloud",
          "allowFrom": ["*"]
        }
      }
    }
  }
}
```

### Work + Personal Accounts

```json
{
  "channels": {
    "apple-mail": {
      "enabled": true,
      "accounts": {
        "work": {
          "email": "john@company.com",
          "mailboxAccount": "Exchange",
          "pollIntervalMs": 15000,
          "archiveOnReply": true
        },
        "personal": {
          "email": "john@gmail.com",
          "mailboxAccount": "Gmail",
          "allowFrom": ["family@domain.com"],
          "pollIntervalMs": 60000
        }
      }
    }
  }
}
```

## Requirements

- **Platform**: macOS (required for Apple Mail and AppleScript)
- **Mail App**: Apple Mail configured with email accounts
- **Node.js**: >= 18.0.0
- **OpenClaw**: >= 2026.1.0 (or Hermes)
- **Plugin**: `@jehadurre/openclaw-apple-mail` >= 1.0.0

## Features

✅ **Step-by-step installation guide**  
✅ **Multiple configuration templates**  
✅ **Troubleshooting solutions**  
✅ **Best practices and tips**  
✅ **Security and permissions setup**  
✅ **Multi-account management**  
✅ **API reference**

## Related Packages

- **Plugin**: [@jehadurre/openclaw-apple-mail](https://www.npmjs.com/package/@jehadurre/openclaw-apple-mail)
- **GitHub**: [JehadurRE/openclaw-apple-mail](https://github.com/JehadurRE/openclaw-apple-mail)
- **Documentation**: [openclaw-apple-mail.jehadurre.me](https://openclaw-apple-mail.jehadurre.me)

## Author

**Md. Jehadur Rahman (Emran)**
- Website: [jehadurre.me](https://jehadurre.me)
- Dev.to: [@jehadurre](https://dev.to/jehadurre)
- GitHub: [@JehadurRE](https://github.com/JehadurRE)

## License

MIT © Md. Jehadur Rahman (Emran)

## Contributing

Contributions welcome! Please read the [Contributing Guide](https://github.com/JehadurRE/openclaw-apple-mail-skill/blob/master/CONTRIBUTING.md) first.

## Support

- 🐛 [Report Issues](https://github.com/JehadurRE/openclaw-apple-mail-skill/issues)
- 📖 [Read Documentation](https://openclaw-apple-mail.jehadurre.me)
- 💬 [Contact Author](https://jehadurre.me)

---

Made with ❤️ for the OpenClaw community
