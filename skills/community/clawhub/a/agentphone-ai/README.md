# AgentPhone for Claude Code

Give your AI agents phone numbers, SMS, and voice calls — right from Claude Code.

## Setup

1. Install the skill:
   ```bash
   npx skills.sh install agentphone
   ```

2. Set your API key:
   ```bash
   export AGENTPHONE_API_KEY=your_key_here
   ```
   Get your API key at [agentphone.to](https://agentphone.to).

3. Start using it:
   ```
   /agentphone create an agent called My Assistant and buy it a phone number
   ```

## What it can do

- Create and manage AI voice agents
- Buy and manage phone numbers
- Make AI-powered outbound calls
- Read SMS conversations and messages
- Set up webhooks for inbound events
- Check account usage and limits
- List available voices for agents

## How it works

This skill connects Claude Code to the [AgentPhone API](https://agentphone.to) via MCP. Your agents can make and receive phone calls, send and read SMS messages, and handle inbound communication through webhooks.

## Structure

```
SKILL.md              # Main skill definition
references/
  api-reference.md    # Complete MCP tool reference (26 tools)
```

## License

MIT
