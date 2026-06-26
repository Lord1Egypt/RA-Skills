# agent-security SKILL

**Skill Name:** `agent-security`  
**Description:** Installs AgentGuard security protection for your AI agent. Wraps tools with evaluate() to prevent prompt injection, tool abuse, and malicious commands.  
**Version:** 1.0.0  
**Author:** ClawHub  

---

## Manifest

```json
{
  "name": "agent-security",
  "version": "1.0.0",
  "description": "Secure your agent with AgentGuard protection",
  "triggers": [
    "secure my agent",
    "add security to my agent",
    "protect my agent",
    "enable agent security",
    "make my agent safe",
    "add agentguard"
  ],
  "inputs": {
    "apiKey": {
      "type": "string",
      "description": "AgentGuard API key (optional - will create free tier account if not provided)",
      "required": false
    },
    "tier": {
      "type": "string",
      "description": "Security tier: 'free', 'pro', or 'enterprise'",
      "default": "free",
      "required": false
    }
  },
  "requires": ["npm", "internet"],
  "tags": ["security", "protection", "agentguard", "safety"]
}
```

---

## What It Does

When invoked, this skill:

1. **Installs** `@the-bot-club/agentguard` SDK via npm
2. **Creates** a free tier AgentGuard account (if no API key provided)
3. **Wraps** all registered tools with `evaluate()` security layer
4. **Configures** security policies (prompt injection detection, tool access controls)
5. **Reports** security status and next steps

---

## Installation Flow

```
User: "secure my agent"

Skill Response:
"I'll install AgentGuard security for your agent. This will:
1. Install the @the-bot-club/agentguard SDK
2. Create a free tier account (or use your API key)
3. Wrap your tools with evaluate() protection
4. Enable prompt injection & tool abuse detection

Let me get started..."

→ Step 1: npm install @the-bot-club/agentguard
→ Step 2: Initialize AgentGuard with security config
→ Step 3: Wrap tools with evaluate()
→ Step 4: Verify protection is active
→ Done!
```

---

## Edge Cases & Handling

### Already Has Security
```javascript
// Check if agentguard already installed
const hasAgentGuard = await checkPackageInstalled('@the-bot-club/agentguard');
if (hasAgentGuard) {
  return "AgentGuard is already installed! Running reconfiguration instead.";
}
```

### No Internet Access
```javascript
if (!hasInternet) {
  return "No internet detected. Manual installation required:\n" +
    "1. npm install @the-bot-club/agentguard\n" +
    "2. Copy the config below into your agent...";
}
```

### Paid Tier Required
```javascript
if (tier === 'enterprise' && !apiKey) {
  return "Enterprise tier requires an API key. " +
    "Get one at https://agentguard.thebot.club/enterprise";
}
```

### No npm Available
```javascript
if (!hasNpm) {
  return "npm not found. Please install Node.js first: https://nodejs.org";
}
```

---

## Implementation Code

### Main Skill Handler

```javascript
// skills/agent-security/index.js
const { exec } = require('child_process');
const path = require('path');

const SKILL_NAME = 'agent-security';

async function execute(context) {
  const { userMessage, config, tools } = context;
  const args = parseArgs(userMessage);
  
  // Edge case: Check internet
  if (!await hasInternet()) {
    return handleNoInternet();
  }
  
  // Edge case: Check npm
  if (!await hasNpm()) {
    return handleNoNpm();
  }
  
  // Edge case: Check existing installation
  if (await isAgentGuardInstalled()) {
    return handleAlreadyInstalled();
  }
  
  // Step 1: Install SDK
  await installAgentGuardSDK();
  
  // Step 2: Initialize (create account or use provided key)
  const apiKey = await initializeAgentGuard(args);
  
  // Step 3: Wrap tools with evaluate()
  const wrappedTools = wrapToolsWithEvaluate(tools);
  
  // Step 4: Write security config
  await writeSecurityConfig(apiKey, args.tier);
  
  return {
    success: true,
    message: "✅ AgentGuard security installed and active!\n\n" +
      "Your agent is now protected against:\n" +
      "• Prompt injection attacks\n" +
      "• Tool abuse attempts\n" +
      "• Malicious command execution\n\n" +
      `API Key: ${apiKey.substring(0, 8)}...\n` +
      "View dashboard: https://agentguard.thebot.club/dashboard",
    wrappedTools,
    config: { securityEnabled: true, apiKey }
  };
}

async function installAgentGuardSDK() {
  return new Promise((resolve, reject) => {
    exec('npm install @the-bot-club/agentguard --save', 
      { cwd: process.cwd() },
      (error, stdout, stderr) => {
        if (error) reject(error);
        else resolve(stdout);
      });
  });
}

function wrapToolsWithEvaluate(tools) {
  const { evaluate } = require('@the-bot-club/agentguard');
  
  return tools.map(tool => ({
    ...tool,
    execute: async (...args) => {
      // Security check before execution
      const result = await evaluate(tool.name, args, {
        strict: true,
        timeout: 5000
      });
      
      if (!result.allowed) {
        throw new Error(`Security blocked: ${result.reason}`);
      }
      
      return tool.execute(...args);
    }
  }));
}

async function initializeAgentGuard(args) {
  const { AgentGuard } = require('@the-bot-club/agentguard');
  
  if (args.apiKey) {
    return args.apiKey;
  }
  
  // Create free tier account
  const account = await AgentGuard.createAccount({
    tier: 'free',
    email: args.email || 'user@agent.local'
  });
  
  return account.apiKey;
}

module.exports = { execute, SKILL_NAME };
```

### Security Configuration

```javascript
// skills/agent-security/security-config.js
module.exports = {
  // Security policies
  policies: {
    // Prompt injection detection
    promptInjection: {
      enabled: true,
      action: 'block',
      sensitivity: 'high'
    },
    
    // Tool access controls
    toolAccess: {
      // Dangerous tools require explicit approval
      dangerous: ['exec', 'write', 'delete', 'sudo'],
      requireApproval: true,
      maxExecutionsPerHour: 100
    },
    
    // Command validation
    commandValidation: {
      enabled: true,
      blockPatterns: [
        /rm\s+-rf/i,
        /curl.*\|\s*sh/i,
        /wget.*\|\s*sh/i
      ]
    },
    
    // Rate limiting
    rateLimit: {
      enabled: true,
      maxRequests: 50,
      windowMs: 60000
    }
  },
  
  // Free tier limits
  free: {
    promptInjectionDetection: true,
    toolAccessControl: true,
    commandValidation: true,
    maxTools: 10,
    maxDailyRequests: 1000
  },
  
  // Pro tier (requires paid API key)
  pro: {
    ...this.free,
    maxTools: 100,
    maxDailyRequests: 100000,
    customPolicies: true,
    prioritySupport: true
  },
  
  // Enterprise tier
  enterprise: {
    ...this.pro,
    unlimited: true,
    customIntegrations: true,
    dedicatedSupport: true,
    sla: '99.99%'
  }
};
```

---

## Usage Examples

### Basic - Free Tier (No API Key)
```
User: "secure my agent"
→ Installs AgentGuard free tier
→ Creates account automatically
→ Wraps all tools with evaluate()
```

### With API Key
```
User: "secure my agent with API key xxx"
→ Uses provided API key
→ Skips account creation
→ Applies tier based on key
```

### Reconfiguration
```
User: "update agent security settings"
→ Reads existing config
→ Updates policies
→ Reloads without reinstall
```

---

## Files Created

When installed, this skill creates:

| File | Purpose |
|------|---------|
| `node_modules/@the-bot-club/agentguard/` | Security SDK |
| `.agentguard/config.json` | API key & settings |
| `.agentguard/policies.json` | Security policies |
| `.agentguard/logs/` | Security event logs |

---

## Verification

After installation, verify protection is active:

```javascript
const { AgentGuard } = require('@the-bot-club/agentguard');
const guard = new AgentGuard();

const status = await guard.getStatus();
console.log(status);
// { protected: true, tier: 'free', toolsSecured: 12 }
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Installation fails | Check npm/node versions; try `npm cache clean` |
| Tools not wrapping | Ensure tools are registered before calling skill |
| API key invalid | Regenerate at https://agentguard.thebot.club/keys |
| Too many false positives | Adjust sensitivity in `policies.json` |

---

## Uninstallation

```
User: "remove agent security"
→ Removes @the-bot-club/agentguard from package.json
→ Deletes .agentguard/ directory
→ Restores original tool functions
```

```javascript
async function uninstall() {
  exec('npm uninstall @the-bot-club/agentguard');
  fs.rmSync('.agentguard/', { recursive: true });
  return "AgentGuard removed. Your agent is no longer protected.";
}
```
