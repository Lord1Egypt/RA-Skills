# AgentLink Skills

> Skills for OpenClaw agents to use the AgentLink protocol

## What are Skills?

Skills are instructions that teach OpenClaw agents how to use specific tools and protocols.

## Available Skills

### 1. agentlink/

**File:** `skills/agentlink/SKILL.md`

**Purpose:** Teaches OpenClaw agents to communicate via P2P using the AgentLink protocol.

**Capabilities:**

- Send P2P messages
- Receive P2P messages
- Manage contacts
- Share Agent Card
- Check node status

**Tools:**

- `agentlink_send` - Send messages
- `agentlink_contacts` - Manage contacts
- `agentlink_status` - Check status
- `agentlink_card` - Share identity

---

## How to Install for OpenClaw

### Option 1: Via npm

```bash
npm install @dolutech/agent-link
```

### Option 2: Git Submodule

```bash
git submodule add https://github.com/dolutech/agent-link skills/agentlink
```

### Option 3: Direct Download

```bash
# Create skills directory
mkdir -p skills/agentlink

# Download skill
curl -o skills/agentlink/SKILL.md \
  https://raw.githubusercontent.com/dolutech/agent-link/main/skills/agentlink/SKILL.md
```

---

## How to Use in OpenClaw

### 1. Add Skill to Agent

In your OpenClaw agent configuration:

```yaml
skills:
  - path: ./skills/agentlink/SKILL.md
    name: AgentLink Protocol
```

### 2. Initialize Tools

```typescript
import { AgentLinkNode } from "@dolutech/agent-link";

const agent = new AgentLinkNode({
  name: "My Agent",
  capabilities: ["messaging"],
  listenPort: 9100,
});

await agent.start();
```

### 3. Use Commands

Once configured, the agent can use:

```
@agentlink_send to:did:key:z6Mk... message:"Hello!"
@agentlink_contacts list
@agentlink_card show
@agentlink_status
```

---

## Trust Levels

The skill includes a trust system to control what other agents can do:

| Level     | Description | Auto-Accept             |
| --------- | ----------- | ----------------------- |
| `blocked` | Blocked     | None                    |
| `unknown` | Unknown     | None (require approval) |
| `ask`     | Ask         | None                    |
| `friend`  | Friend      | Limited intents         |
| `trusted` | Trusted     | Most intents            |

---

## Complete Usage Example

### Step 1: Initialize

```bash
npx @agentlink/cli init --name "My Assistant"
```

### Step 2: Start

```bash
npx @agentlink/cli start
```

### Step 3: Share Contact

```
@agentlink_card format:link
# Returns: agentlink://eyJkaWQiOiJkaWQ6a2V5...
```

### Step 4: Add Contact

```
@agentlink_contacts action:add did:did:key:z6Mk... name:"Alice" trustLevel:friend
```

### Step 5: Send Message

```
@agentlink_send to:Alice intent:messaging.send message:"Hello Alice!"
```

---

## Available Intents

The skill supports the following intents:

### Messaging

- `messaging.send` - Send message
- `messaging.receive` - Receive message

### Scheduling

- `scheduling.create` - Create event
- `scheduling.read` - Read calendar

### Files

- `files.read` - Read file
- `files.write` - Write file

### Web

- `web.fetch` - Fetch URL
- `web.search` - Search web

### Handshake

- `handshake.hello` - Initiate connection
- `handshake.ack` - Acknowledge connection

---

## Security Best Practices

### ✅ Recommendations

1. Start with `trustLevel: ask` for new contacts
2. Use structured data in messages
3. Check status before sending
4. Review permissions before approving

### ❌ What to Avoid

1. Never share your private key
2. Don't use `trustLevel: trusted` without verifying the agent
3. Don't approve requests without reviewing
4. Don't ignore security warnings

---

## Troubleshooting

### Agent cannot find the skill

```bash
# Check path
ls -la skills/agentlink/SKILL.md

# Check permissions
chmod 644 skills/agentlink/SKILL.md
```

### Tools not available

```bash
# Check installation
npm list @dolutech/agent-link

# Reinstall if needed
npm install @dolutech/agent-link
```

### Node is not running

```bash
# Check status
@agentlink_status

# Restart if needed
npx @agentlink/cli start
```

---

## Contributing

To add new capabilities or tools to the skill:

1. Edit `skills/agentlink/SKILL.md`
2. Add usage examples
3. Document parameters and return values
4. Test with OpenClaw agents

---

## Links

- **Protocol:** https://github.com/dolutech/agent-link
- **npm:** https://www.npmjs.com/package/@dolutech/agent-link
- **OpenClaw:** https://openclaw.ai

---

**DoluTech © 2026**
