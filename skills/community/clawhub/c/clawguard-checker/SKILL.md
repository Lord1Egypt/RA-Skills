---
name: clawguard-security-checker
description: ClawGuard Security Checker v3 - Advanced configuration analysis, runtime integrity verification, permission modeling, and one-click hardening recommendations
metadata:
  category: security
---

# 🔧 ClawGuard Security Checker (CG-SC) v3

Enterprise-grade security configuration analyzer and runtime integrity verifier for OpenClaw environments. Provides comprehensive security posture assessment with advanced configuration analysis, permission modeling, and one-click hardening recommendations.

## When to Use

Activate ClawGuard Checker when:
- A user asks to check the security status of the OpenClaw instance
- Periodic security review is needed
- After configuration changes
- User asks for "security check", "hardening", or "how to secure"

## How to Execute

Follow these steps when performing a security check:

### Step 1: Check Configuration File
- Find and read `~/.openclaw/openclaw.json`
- Verify these security settings:
  - `gateway.bind` should be "localhost" (not "0.0.0.0" or "lan")
  - `gateway.tls.enabled` should be true
  - `gateway.auth.deviceAuth` should be true
  - `tools.profile` should be "restricted" (not "full")
  - `tools.fs.workspaceOnly` should be true

### Step 2: Check for Exposed Credentials
Search for exposed secrets in:
- Config files (API keys, tokens, passwords)
- Environment files (.env)
- Log files

### Step 3: Check File Permissions
Verify these permissions:
- `~/.openclaw/openclaw.json` should be 600 (owner read/write only)
- `~/.openclaw/` directory should be 700
- SSH keys should be 600
- Not running as root user

### Step 4: Check Network Settings
- Gateway port should not be exposed to 0.0.0.0
- Trusted proxies should be limited
- Rate limiting should be enabled

### Step 5: Generate Hardening Recommendations (v3)

Based on findings, generate specific recommendations:
- **CRITICAL issues**: Generate immediate fix
- **HIGH issues**: Generate configuration changes
- **MEDIUM issues**: Suggest improvements

### Step 6: Output Result
Calculate security score and output:
- Score: 0-100
- Grade: A+ to F
- List of issues found
- **Hardening recommendations (v3)**

## Purpose

ClawGuard Security Checker is the second line of defense, providing continuous security posture monitoring for OpenClaw instances. It verifies:

- **Configuration Security**: Comprehensive analysis of OpenClaw configuration files
- **Runtime Integrity**: Cryptographic verification of system files and runtime components
- **Permission Modeling**: Advanced permission analysis and least-privilege enforcement
- **Network Security**: Multi-layered network policy validation
- **Log Forensics**: AI-powered anomaly detection in audit logs
- **Compliance**: Security benchmark compliance checking
- **Hardening (v3)**: One-click security configuration generation

## Core Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│               CLAWGUARD SECURITY CHECKER WORKFLOW               │
└─────────────────────────────────────────────────────────────────┘

    [Scheduled/Manual Check Trigger]
                │
                ▼
    ┌───────────────────────┐
    │  1. CONFIGURATION     │ ← Parse and validate openclaw.json
    │     ANALYSIS           │
    └───────────┬───────────┘
                │ PASS
                ▼
    ┌───────────────────────┐
    │  2. CREDENTIAL SCAN   │ ← Detect exposed secrets
    └───────────┬───────────┘
                │ PASS
                ▼
    ┌───────────────────────┐
    │  3. PERMISSION        │ ← File/directory permission analysis
    │     MODELING           │
    └───────────┬───────────┘
                │ PASS
                ▼
    ┌───────────────────────┐
    │  4. RUNTIME INTEGRITY │ ← SHA-256 + quantum-resistant hashes
    └───────────┬───────────┘
                │ PASS
                ▼
    ┌───────────────────────┐
    │  5. NETWORK SECURITY  │ ← Port, firewall, proxy analysis
    └───────────┬───────────┘
                │ PASS
                ▼
    ┌───────────────────────┐
    │  6. HARDENING (v3)   │ ← Generate security recommendations
    └───────────┬───────────┘
                │ PASS
                ▼
         [SECURITY REPORT]
```

## Phase 1: Configuration Analysis

### Configuration File Schema

The analyzer examines `openclaw.json` for security-relevant settings:

```json
{
  "gateway": {
    "bind": "localhost",
    "port": 8080,
    "tls": {
      "enabled": true,
      "certPath": "/path/to/cert.pem",
      "keyPath": "/path/to/key.pem"
    },
    "auth": {
      "deviceAuth": true,
      "tokenExpiry": 3600
    },
    "cors": {
      "allowedOrigins": ["https://example.com"]
    }
  },
  "tools": {
    "profile": "restricted",
    "fs": {
      "workspaceOnly": true,
      "allowedPaths": ["/workspace/*"]
    },
    "network": {
      "egressRestrictions": true,
      "allowedDomains": ["api.github.com", "api.openai.com"]
    },
    "exec": {
      "allowedCommands": ["git", "npm", "node"]
    }
  },
  "security": {
    "update": {
      "checkOnStart": true,
      "autoUpdate": false
    },
    "audit": {
      "enabled": true,
      "retentionDays": 30
    }
  }
}
```

### Configuration Security Checks

| Check | Severity | Points | Detection Rule |
|-------|----------|--------|----------------|
| Gateway bind 0.0.0.0 | CRITICAL | -20 | `gateway.bind === "0.0.0.0"` |
| Gateway bind lan | HIGH | -15 | `gateway.bind === "lan"` |
| CORS * allowed | HIGH | -15 | `allowedOrigins.includes("*")` |
| tools.exec.security = "full" | CRITICAL | -20 | `tools.exec.security === "full"` |
| Device auth disabled | HIGH | -15 | `deviceAuth === false` |
| Token expiry > 24h | MEDIUM | -5 | `tokenExpiry > 86400` |
| TLS not enabled | HIGH | -15 | `tls.enabled === false` |
| fs.workspaceOnly false | HIGH | -15 | `fs.workspaceOnly === false` |
| Sandbox disabled | HIGH | -15 | `sandbox.enabled === false` |
| No egress restrictions | HIGH | -10 | `network.egressRestrictions === false` |

### Hardening Recommendations (v3)

| Issue | Current | Recommended |
|-------|---------|-------------|
| Gateway bind | `"0.0.0.0"` | `"127.0.0.1"` |
| Auth mode | `null` or `"none"` | `"token"` |
| Exec security | `"full"` | `"allowlist"` |
| Sandbox | `enabled: false` | `enabled: true` |
| TLS | `enabled: false` | `enabled: true` |
| CORS | `origin: "*"` | `origin: ["your-domain.com"]` |

## Phase 2: Credential Exposure Detection

### Multi-Layer Credential Scanning

| Layer | Target | Method |
|-------|--------|--------|
| Layer 1 | Configuration files | Pattern matching |
| Layer 2 | Environment files (.env) | Direct file scan |
| Layer 3 | Log files | Historical credential check |
| Layer 4 | Memory dumps | Process memory (optional) |

### Enhanced Credential Detection (v3)

```javascript
const CREDENTIAL_PATTERNS = [
  // API Keys
  { pattern: /sk-[a-zA-Z0-9]{20,}/g, type: 'openai_key', severity: 'CRITICAL' },
  { pattern: /sk-ant-[a-zA-Z0-9_-]{20,}/g, type: 'anthropic_key', severity: 'CRITICAL' },
  { pattern: /AKIA[0-9A-Z]{16}/g, type: 'aws_access_key', severity: 'CRITICAL' },
  { pattern: /ghp_[a-zA-Z0-9]{36}/g, type: 'github_token', severity: 'CRITICAL' },
  { pattern: /gho_[a-zA-Z0-9]{36}/g, type: 'github_oauth', severity: 'CRITICAL' },
  { pattern: /glpat-[a-zA-Z0-9_-]{20}/g, type: 'gitlab_token', severity: 'CRITICAL' },

  // Private Keys
  { pattern: /-----BEGIN (RSA |DSA |EC |OPENSSH) PRIVATE KEY-----/g, type: 'private_key', severity: 'CRITICAL' },

  // Generic Secrets
  { pattern: /api[_-]?key["\s:=]+[a-zA-Z0-9]{16,}/gi, type: 'api_key', severity: 'HIGH' },
  { pattern: /password["\s:=]+["'][^"']{8,}["']/gi, type: 'password', severity: 'HIGH' },
];
```

### Detection Rules

| Credential Type | Pattern | Severity | Action |
|---------------|---------|----------|--------|
| AWS Access Key | `AKIA...` | CRITICAL | Alert + Rotate |
| GitHub Token | `ghp_...` | CRITICAL | Alert + Revoke |
| OpenAI Key | `sk-...` | CRITICAL | Alert + Revoke |
| Private Key | `-----BEGIN...` | CRITICAL | Alert + Alert SOC |
| Weak Password | < 12 chars | HIGH | Alert + Change |

## Phase 3: Permission Modeling

### File System Permission Analysis

```javascript
const CRITICAL_PATHS = [
  { path: '~/.openclaw/openclaw.json', expectedMode: '600', severity: 'HIGH' },
  { path: '~/.openclaw/', expectedMode: '700', severity: 'HIGH' },
  { path: '~/.ssh/', expectedMode: '700', severity: 'CRITICAL' },
  { path: '~/.aws/', expectedMode: '700', severity: 'CRITICAL' },
];
```

### Permission Check Matrix

| Check | Severity | Points | Rule |
|-------|----------|--------|------|
| Config file world-readable | CRITICAL | -20 | Mode & 007 !== 0 |
| Config file group-readable | HIGH | -10 | Mode & 070 !== 0 |
| SSH keys world-readable | CRITICAL | -20 | Mode & 004 !== 0 |
| Running as root | CRITICAL | -25 | UID === 0 |
| Workspace world-writable | HIGH | -15 | Mode & 002 !== 0 |

## Phase 4: Network Security Analysis

### Port and Binding Analysis

| Check | Severity | Points | Detection |
|-------|----------|--------|-----------|
| Gateway on 0.0.0.0 | CRITICAL | -20 | Exposed to all interfaces |
| Gateway on lan | HIGH | -15 | Exposed to local network |
| Gateway on localhost | LOW | 0 | Only local access |
| TLS disabled | HIGH | -15 | Unencrypted communication |

### Network Security Checks

```javascript
const NETWORK_SECURITY_CHECKS = [
  {
    check: 'rate_limiting',
    rule: (config) => config.rateLimit?.enabled === true,
    severity: 'HIGH',
    points: -10,
    message: 'Rate limiting not enabled',
    fix: { rateLimit: { enabled: true, max: 100, windowMs: 60000 } }
  },
  {
    check: 'egress_whitelist',
    rule: (config) => config.network?.allowedDomains?.length > 0,
    severity: 'HIGH',
    points: -10,
    message: 'No egress domain whitelist configured',
    fix: { network: { allowedDomains: ['api.github.com', 'api.openai.com'] } }
  },
  {
    check: 'trusted_proxies',
    rule: (config) => config.trustedProxies?.length <= 2,
    severity: 'MEDIUM',
    points: -5,
    message: 'Limited proxy trust configured'
  }
];
```

## Phase 5: Hardening Recommendations (v3 核心功能)

### One-Click Hardening

Based on detected issues, generate hardened configuration:

```javascript
const HARDEENING_RULES = {
  // Gateway Hardening
  gateway: {
    bind: { value: '127.0.0.1', reason: 'Only local access' },
    tls: { value: { enabled: true }, reason: 'Encrypted communication' },
    auth: { value: { mode: 'token', token: '<GENERATE>' }, reason: 'Authentication required' },
    rateLimit: { value: { enabled: true, max: 100, windowMs: 60000 }, reason: 'DDoS protection' },
    cors: { value: { enabled: true, origin: [], credentials: true }, reason: 'Controlled access' }
  },

  // Tools Hardening
  tools: {
    exec: {
      security: { value: 'allowlist', reason: 'Controlled execution' },
      allowlist: { value: ['ls', 'cat', 'grep', 'find', 'echo', 'pwd'], reason: 'Minimal command set' }
    },
    fs: {
      workspaceOnly: { value: true, reason: 'File system isolation' }
    }
  },

  // Sandbox Hardening
  sandbox: {
    enabled: { value: true, reason: 'Runtime isolation' },
    allowedPaths: { value: ['/tmp', '~/workspace'], reason: 'Controlled file access' },
    deniedPaths: { value: ['/home', '/root', '/etc', '/var'], reason: 'Protect system files' },
    maxMemory: { value: 512, reason: 'Resource limit' },
    timeout: { value: 60000, reason: 'Execution timeout' }
  }
};
```

### Hardened Config Example

```json
{
  "gateway": {
    "bind": "127.0.0.1",
    "auth": {
      "mode": "token",
      "token": "<GENERATE: crypto.randomBytes(32).toString('hex')>"
    },
    "tls": {
      "enabled": true
    },
    "rateLimit": {
      "enabled": true,
      "max": 100,
      "windowMs": 60000
    }
  },
  "tools": {
    "exec": {
      "security": "allowlist",
      "allowlist": ["ls", "cat", "grep", "find", "echo", "pwd"]
    },
    "fs": {
      "workspaceOnly": true
    }
  },
  "sandbox": {
    "enabled": true,
    "allowedPaths": ["/tmp", "~/workspace"],
    "deniedPaths": ["/home", "/root", "/etc", "/var"],
    "maxMemory": 512,
    "timeout": 60000
  },
  "logging": {
    "enabled": true,
    "level": "info",
    "auditLog": true
  }
}
```

## Security Scoring

### Scoring Formula

```
SECURITY_SCORE = 100 - CONFIG_PENALTY - CREDENTIAL_PENALTY - PERMISSION_PENALTY - NETWORK_PENALTY

Where:
- CONFIG_PENALTY = CRITICAL*20 + HIGH*15 + MEDIUM*5
- CREDENTIAL_PENALTY = CRITICAL*25 + HIGH*15 + MEDIUM*5
- PERMISSION_PENALTY = CRITICAL*25 + HIGH*15 + MEDIUM*5
- NETWORK_PENALTY = CRITICAL*20 + HIGH*15 + MEDIUM*5
```

### Score Classification

| Grade | Score | Color | Action |
|-------|-------|-------|--------|
| **A+** | 95-100 | 🟢 | Excellent - Continue monitoring |
| **A** | 90-94 | 🟢 | Good - Minor improvements possible |
| **B** | 80-89 | 🟢 | Satisfactory - Address warnings |
| **C** | 70-79 | 🟡 | Fair - Fix within 1 week |
| **D** | 60-69 | 🟠 | Poor - Fix within 24 hours |
| **F** | 0-59 | 🔴 | Critical - Fix immediately |

## Output Formats

### Terminal Output (v3)

```
╔══════════════════════════════════════════════════════════════╗
║        🔧 CLAWGUARD SECURITY CHECK REPORT v3.0.0   ║
╠══════════════════════════════════════════════════════════════╣
║ Instance: openclaw-abc123                              ║
║ Time: YYYY-MM-DD HH:MM:SS                             ║
╚══════════════════════════════════════════════════════════════╝

▶ GATEWAY SECURITY [-35]
  🔴 [CRITICAL] Gateway bind: 0.0.0.0 (exposed)
     Fix: Set gateway.bind = "127.0.0.1"
  🔴 [CRITICAL] Auth disabled
     Fix: Set gateway.auth.mode = "token"
  🟡 [HIGH] TLS not enabled
     Fix: Set gateway.tls.enabled = true

▶ TOOLS SECURITY [-20]
  🔴 [CRITICAL] Exec security: full
     Fix: Set tools.exec.security = "allowlist"
     and add: tools.exec.allowlist = ["ls", "cat", "grep", ...]

▶ SANDBOX [-15]
  🟠 [HIGH] Sandbox disabled
     Fix: Set sandbox.enabled = true

▶ CREDENTIALS [0]
  ✓ No exposed credentials

▶ PERMISSIONS [0]
  ✓ Config file mode 600
  ✓ Directory mode 700

╔══════════════════════════════════════════════════════════════╗
║ SECURITY GRADE: F (30/100)                              ║
╠══════════════════════════════════════════════════════════════╣
║ CRITICAL: 3 | HIGH: 2 | MEDIUM: 0                     ║
╠══════════════════════════════════════════════════════════════╣
║ 🛡️ HARDENING RECOMMENDATION (v3)                      ║
║                                                        ║
║ Run with --fix to generate hardened configuration:     ║
║   node cli.js --fix                                   ║
╚══════════════════════════════════════════════════════════════╝
```

## v3 vs v2 Features

| Feature | v2 | v3 |
|---------|----|----|
| Configuration Analysis | ✅ | ✅ |
| Credential Detection | ✅ | ✅ |
| Permission Modeling | ✅ | ✅ |
| Network Security | ✅ | ✅ |
| Log Forensics | ✅ | ✅ |
| **Hardening Recommendations** | ❌ | **✅ (v3)** |
| **One-Click Fix Generation** | ❌ | **✅ (v3)** |
| **Automated Config Generation** | ❌ | **✅ (v3)** |
| **Security Grade A-F** | Basic | **Enhanced (v3)** |

---

*ClawGuard Security Checker: Vigilant protection for your AI agents.* 🔧
