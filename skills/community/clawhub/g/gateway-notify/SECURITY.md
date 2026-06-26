# Security & Privacy

## What This Skill Does

This skill creates a hook that:
1. Listens for gateway startup events
2. Sends a notification message to your configured channel
3. Reads minimal gateway status (timestamp and port)

## Security Considerations

### Input Validation
The setup script validates all inputs:
- Channel names: only lowercase letters
- Email addresses: standard email format validation
- Phone numbers: international format with country code
- Telegram usernames: standard @username format

### No Config File Reading
**Updated in v1.0.1**: The handler no longer reads your OpenClaw config file. It only accesses:
- Current timestamp
- Gateway port (hardcoded: 18789)

### Command Injection Protection
All user inputs are validated and properly escaped before being embedded in shell commands.

## Privacy

This skill does NOT:
- Send your API keys or credentials
- Access your personal data
- Share information with third parties
- Read sensitive configuration

This skill ONLY:
- Sends a simple notification when the gateway starts
- Uses the messaging address YOU provide during setup

## Review Before Installing

As with any skill, review the code before installation:
- `scripts/setup_gateway_notify.sh` - Setup script with input validation
- `references/MANUAL.md` - Manual setup instructions

## Questions?

Open an issue on GitHub: https://github.com/deemoartisan/gateway-notify
