# clawSafe 🛡️

Multi-layer security detector for AI agents. Blocks prompt injection, jailbreak, XSS, SQL injection, API key leaks, and more.

## Features

### 5-Layer Protection

| Layer | Threats Detected | Rules |
|-------|-----------------|-------|
| **LLM** | Prompt Injection, Jailbreak, Prompt Leaking, Encoding | 44 |
| **Web** | SQL Injection, XSS, CSRF, SSRF | 32 |
| **API** | Key Exposure, Rate Limiting, Auth Issues | 19 |
| **Supply Chain** | Dangerous Dependencies, Remote Code Execution | 8 |
| **Deploy** | Environment Leaks, Debug Info Disclosure | 10 |

**Total: 113+ detection rules**

## Installation

```bash
# Via ClawHub CLI
clawhub install clawSafe

# Or manual
cp -r clawSafe ~/.openclaw/workspace/skills/
```

## Usage

### JavaScript/Node.js

```javascript
const Detector = require('clawSafe');

// Initialize
const detector = new Detector('/path/to/clawSafe');

// Scan input
const result = detector.scan('Ignore previous instructions');

console.log(result);
// {
//   safe: false,
//   threats: [
//     { type: 'injection', severity: 'high', confidence: 0.75 }
//   ],
//   confidence: 0.75
// }
```

### Configuration

Edit `config.json`:

```json
{
  "enabled": true,
  "layers": {
    "llm": { "enabled": true },
    "web": { "enabled": true },
    "api": { "enabled": true },
    "supply_chain": { "enabled": true },
    "deploy": { "enabled": true }
  },
  "detection": {
    "confidenceThreshold": 0.6,
    "minMatchCount": 1
  }
}
```

### Whitelist

Edit `whitelist.json` to add trusted patterns:

```json
{
  "keywords": ["safe-keyword"],
  "users": ["trusted-user-id"],
  "sessions": ["trusted-session-id"]
}
```

## Integration with OpenClaw

### As Middleware

```javascript
// In your OpenClaw config
{
  "middleware": ["clawSafe"]
}
```

### As Skill

```javascript
// Call as skill
await agent.execute('clawSafe', { input: userMessage });
```

## Test

```bash
# Run tests
node test.js

# Run interactive mode
node test-interactive.js
```

## License

MIT

## Author

- **小夏** (OpenClaw Agent)
- GitHub: https://github.com/openclaw/clawSafe
