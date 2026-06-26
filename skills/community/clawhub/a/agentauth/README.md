# agentauth (Approval Flow for OpenClaw)

This skill adds **human approval + identity verification** before OpenClaw performs dangerous actions.

OpenClaw will automatically use this when it detects a **high-risk action**, such as:

- Deleting files or data
- Sending emails or external writes
- Database changes
- Deployments or production changes
- Security or permission updates

---

## Installation

You can install this skill into OpenClaw using the provided script or manually.

### Option 1 — Using the install script (recommended)

```bash
npm run deploy:local
```

Optionally, you can pass a custom OpenClaw directory:

```bash
npm run deploy:local -- /path/to/openclaw
```

If no path is provided, the script will use:

```bash
~/.openclaw
```

The script will:

- Build the project
- Package the skill
- Install it into your OpenClaw `skills` directory

### Option 2 — Manual installation

If you prefer to install manually:

```bash
npm install
npm run build
```

If you prefer to install manually:

1. **Build the project**

```bash
npm install
npm run build
```

2. **Package and install the skill**

```bash
mkdir agentauth
cp SKILL.md agentauth
cp -r scripts agentauth
mv agentauth ~/.openclaw/skills
```

If using a custom OpenClaw directory:

```bash
mv agentauth <openclaw-directory>/skills/
```

Restart OpenClaws gateway and it will automatically detect and use the skill when needed.

---

## Initialize the Skill

Once the skill is installed, ask OpenClaw to initialize it by saying something like:

```
Initialize my AgentAuth
```

OpenClaw will send you a secure link where you can:

- Create a passkey
- Automatically configure your credentials

No manual credential setup is required.

---

## Cleanup the Skill

Before uninstalling the skill, ask OpenClaw to clean it up by saying something like:

```
Cleanup my AgentAuth
```

OpenClaw will send you a secure link where you can:

- Approve the cleanup process

This will restore any modified configuration files to their original state and remove integrations.

## Command Used by OpenClaw

```bash
node ./scripts/cli.cjs approval-flow "<toolCall>" "<displayString>" [--notify <channel:target>]
```

---

## What Happens

1. **When OpenClaw detects a dangerous action that it needs to use**

2. It runs:

   ```bash
   node ./scripts/cli.cjs approval-flow ...
   ```

3. The script:

   - Creates an approval session with agentauth
   - Generates an approval URL

4. The user is notified:

   - If `--notify` is set → message is sent (Telegram, Slack, etc.)
   - If notification fails → browser opens automatically

5. The user:

   - Opens the approval link
   - Sees the required action
   - Approves or denies using a **passkey**

6. OpenClaw **waits** until one of these happens:

   - Approved
   - Denied
   - Timeout

7. OpenClaw continues based on the result:

   - **Approved** → action is executed
   - **Denied** → action is ignored 
   - **Timeout** → action is ignored

---

## License

MIT-0 © LoginID Inc.
