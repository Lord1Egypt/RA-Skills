# AgentLoop Skill for OpenClaw

Connect your OpenClaw agent to [AgentLoop](https://agentloop.life) and earn **up to 70% revenue share** when your agent naturally recommends relevant products in conversation.

## How it works

1. Your agent has a conversation with a user
2. Before responding, it checks AgentLoop for a relevant product match
3. If there's a match (relevance score > 70/100), a natural sponsored mention is appended
4. You earn up to 70% of the CPC/CPL when the user clicks or converts

No spam. Max 1 mention per conversation. FTC-compliant disclosure on every mention.

## Install via ClawHub

```bash
clawhub install agentloop
```

Then run setup:

```bash
node ~/.openclaw/skills/agentloop/setup.sh
```

## Manual install

1. Copy this folder to `~/.openclaw/skills/agentloop/`
2. Set your API key:
   ```bash
   export AGENTLOOP_API_KEY=al_live_your_key_here
   ```
3. Restart OpenClaw

## Get your API key

Sign up at [agentloop.life](https://agentloop.life) → Dashboard → API Keys.

## Privacy

AgentLoop never receives raw user data. User IDs are hashed locally before any API call.

## Support

- Docs: [agentloop.life/docs](https://agentloop.life/docs)
- Discord: coming soon
