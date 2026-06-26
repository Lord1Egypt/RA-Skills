---
name: clawguard-auditor
description: ClawGuard v3 Auditor - 企业级 Skill 安全审计器，支持意图偏离检测、SAST、供应链安全、ML 异常检测。当用户要求审计、检测、安装前检查一个 Skill 的安全性时触发。
metadata:
  category: security
---

# 🛡️ ClawGuard Auditor (CG-A) v3

Enterprise-grade Security Kernel for OpenClaw Skills. ClawGuard Auditor provides comprehensive pre-flight static and semantic analysis, supply chain security verification, and AI-powered anomaly detection.

## When to Use

Activate ClawGuard Auditor when:
- A user asks to install or load a new Skill
- A user asks to audit an existing Skill or repository
- A new external code source is being added to the environment

## How to Execute

Follow these steps when auditing a Skill:

### Step 1: Read the Target Skill
- Find and read the `SKILL.md` file in the target directory
- Read all code files (.js, .py, .sh, etc.)
- **Also scan code blocks inside SKILL.md** (v3 新增)

### Step 2: Check Metadata
- Verify the SKILL.md has valid frontmatter (name, version, description)
- Check if the `metadata.risk` field is "safe"
- Check for suspicious binaries in `metadata.requires`

### Step 3: Scan for Dangerous Patterns

#### Critical Patterns (Immediate Reject)

| Pattern | Description | Example |
|---------|-------------|---------|
| `eval()` | Dynamic code execution | `eval(userInput)` |
| `exec()` | Command execution | `exec(cmd)` |
| `__import__()` | Dynamic imports | `__import__('os')` |
| `compile()` | Dynamic compilation | `compile(src, '', 'exec')` |
| `child_process.execSync` | Sync command execution | `execSync(cmd, {shell: true})` |
| `subprocess.Popen` | Process spawning | `Popen(shell=True)` |
| `os.system()` | Shell execution | `os.system(cmd)` |

#### High Risk Patterns (Block + Review)

| Pattern | Description | Example |
|---------|-------------|---------|
| `fetch()` to dynamic URL | Dynamic network requests | `fetch(url + userInput)` |
| `XMLHttpRequest` | Browser network | `new XMLHttpRequest()` |
| `WebSocket` | Real-time comms | `new WebSocket(url)` |
| `process.env` | Env access | `process.env[KEY]` |
| `os.environ` | Env access | `os.environ.get(KEY)` |

### Step 4: Check Intent Match (v3 核心功能)

**Compare what the Skill claims to do (description) vs what the code actually does**

If a "Weather Tool" reads SSH keys, that's an **INTENT MISMATCH**!

#### Intent Mismatch Detection Process

1. **Extract stated purpose** from SKILL.md description
2. **Analyze actual behavior** from code
3. **Compute intent score** using semantic similarity
4. **Flag mismatches** if score < threshold

#### Example Mismatches

| Skill Description | Actual Behavior | Intent Score | Action |
|------------------|-----------------|--------------|--------|
| "Weather Formatter" | Reads `~/.ssh/id_rsa` | 0.2 | REJECT |
| "File Organizer" | Spawns background process | 0.4 | REJECT |
| "Markdown Helper" | Makes HTTP POST to unknown domain | 0.3 | REJECT |
| "Calculator" | Writes to `/etc/cron` | 0.1 | REJECT |

### Step 5: Check Dependencies
- Look at package.json, requirements.txt, go.mod
- Flag known malicious packages
- Check for typosquatting patterns

### Step 6: Output Result

Based on findings, output one of:
- **APPROVED**: No critical issues found
- **CONDITIONAL**: Some concerns, needs human review
- **REJECTED**: Critical security issues detected

## Purpose

ClawGuard Auditor is the first line of defense for OpenClaw environments. Before any Skill is installed or executed, it performs rigorous security analysis covering:

- **Advanced SAST**: Static Application Security Testing with comprehensive rule coverage
- **Semantic Intent Analysis (v3)**: AI-powered behavioral profiling to detect intent mismatches
- **Supply Chain Security**: Dependency verification, typo-squatting detection, CVE scanning
- **ML-based Anomaly Detection**: Machine learning models to identify novel attack patterns
- **Obfuscation Detection**: Multi-layer obfuscation and encoding attack detection
- **SKILL.md Code Scanning (v3)**: Scan code blocks inside documentation files

## Core Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLAWGUARD AUDITOR WORKFLOW                   │
└─────────────────────────────────────────────────────────────────┘

    [Skill Installation Request]
                │
                ▼
    ┌───────────────────────┐
    │  1. METADATA VALIDATION  │ ← Frontmatter parsing & validation
    └───────────┬───────────┘
                │ PASS
                ▼
    ┌───────────────────────┐
    │  2. PROVENANCE ANALYSIS │ ← Source trust scoring
    └───────────┬───────────┘
                │ PASS
                ▼
    ┌───────────────────────┐
    │  3. SAST ANALYSIS       │ ← Advanced static analysis
    │  ├─ Execution Risks     │
    │  ├─ Network Anomalies   │
    │  ├─ File System Threats │
    │  └─ Obfuscation Detection │
    └───────────┬───────────┘
                │ PASS
                ▼
    ┌───────────────────────┐
    │  4. SEMANTIC INTENT     │ ← v3 AI-powered behavior analysis
    │     ANALYSIS (v3)        │
    └───────────┬───────────┘
                │ PASS
                ▼
    ┌───────────────────────┐
    │  5. SUPPLY CHAIN       │ ← Dependency & CVE analysis
    │     SECURITY            │
    └───────────┬───────────┘
                │ PASS
                ▼
    ┌───────────────────────┐
    │  6. ML ANOMALY         │ ← Novel pattern detection
    │     DETECTION           │
    └───────────┬───────────┘
                │ PASS
                ▼
         [AUDIT COMPLETE]
```

## Phase 1: Metadata Validation

### Frontmatter Schema

| Field | Required | Validation Rules |
|-------|----------|------------------|
| name | YES | Must match directory name, lowercase with hyphens |
| version | YES | Must be valid semver (e.g., 1.0.0) |
| description | YES | Min 10 chars, max 500 chars |
| author | NO | If present, validate format |
| homepage | NO | If present, must be valid HTTPS URL |
| metadata.category | YES | Must be one of: security, utility, data, integration |
| metadata.risk | YES | Must be "safe" for new Skills |
| metadata.requires | NO | If present, validate each binary exists |

### Validation Rules

| Check | Severity | Action |
|-------|----------|--------|
| Missing YAML frontmatter | CRITICAL | REJECT |
| Invalid name format | HIGH | REJECT |
| Version not semver | MEDIUM | WARN |
| Missing description | MEDIUM | REJECT |
| risk != "safe" | HIGH | WARN |
| Suspicious binary in requires | CRITICAL | REJECT |

### Enhanced Binary Detection

Reject Skills requiring:
- Network tools: `nc`, `ncat`, `socat`, `netcat`, `socat`
- Remote access: `ssh`, `scp`, `rsync` (unless explicitly justified)
- Package managers: `pip install`, `npm install -g` (unless in sandbox)
- System modification: `chmod`, `chown`, `sudo` (unless documented)

## Phase 2: Provenance Analysis

### Trust Scoring Algorithm

```
TRUST_SCORE = BASE_SCORE + SOURCE_BONUS + HISTORY_BONUS - RISK_FACTORS

BASE_SCORE: 50
SOURCE_BONUS:
  - Official OpenClaw repo: +30
  - GitHub >1000 stars: +20
  - GitHub >500 stars: +15
  - Verified author: +10
  - Personal/Gist: -20

HISTORY_BONUS:
  - First seen >1 year ago: +10
  - Active maintenance (commit in last 6mo): +5

RISK_FACTORS:
  - No git history: -15
  - Single commit: -10
  - Many contributors but no reviews: -5
```

### Source Classification

| Classification | Score Range | Action |
|---------------|-------------|--------|
| **Trusted** | 80-100 | Auto-approve with standard logging |
| **Verified** | 60-79 | Approve with enhanced logging |
| **Unknown** | 40-59 | Manual review required |
| **Suspicious** | 20-39 | Deep audit required |
| **Untrusted** | 0-19 | Auto-reject |

## Phase 3: Advanced SAST Analysis (v3 Enhanced)

### Execution Risk Detection

#### Critical Patterns (Immediate Reject)

| Pattern | Description | Example |
|---------|-------------|---------|
| `exec()` | Dynamic code execution | `exec(user_input)` |
| `eval()` | String evaluation | `eval(code)` |
| `__import__()` | Dynamic imports | `__import__('os')` |
| `compile()` | Dynamic compilation | `compile(src, '', 'exec')` |
| `child_process.execSync` | Sync command execution | `execSync(cmd, {shell: true})` |
| `subprocess.Popen` | Process spawning | `Popen(shell=True)` |
| `os.system()` | Shell execution | `os.system(cmd)` |

### Network Anomaly Detection

#### Critical Patterns

| Pattern | Severity | MITRE ATT&CK |
|---------|----------|--------------|
| `curl` with credentials | CRITICAL | T1041 |
| `wget` with credentials | CRITICAL | T1041 |
| Base64 encoded data to network | CRITICAL | T1132 |
| DNS exfiltration patterns | CRITICAL | T1048.003 |
| Hardcoded IP addresses | HIGH | T1059 |
| Reverse shell signatures | CRITICAL | T1059.004 |
| IPtables modification | HIGH | T1562 |

#### Reverse Shell Signatures (Enhanced Detection)

```javascript
// Comprehensive reverse shell patterns
const REVERSE_SHELL_PATTERNS = [
  // Bash
  /bash\s+-i\s+.*\/?dev\/tcp\//,
  /bash\s+-i\s+.*\/?dev\/udp\//,
  /\/bin\/sh\s+-i\s+.*\/?dev\/tcp\//,

  // Netcat
  /nc\s+.*-e\s+/,
  /ncat\s+.*-e\s+/,
  /nc\s+.*exec:/,
  /ncat\s+.*exec:/,

  // Python
  /python.*socket.*connect.*exec/i,
  /python.*subprocess.*call/i,
  /python.*pty\.spawn/i,

  // Perl
  /perl.*socket.*connect/i,
  /perl.*-e\s+.*socket/i,

  // Ruby
  /ruby.*socket.*connect/i,
  /ruby.*-e\s+.*spawn/i,

  // PHP
  /php.*fsockopen/i,
  /php.*socket_create.*connect/i,

  // Node.js
  /node.*child_process.*spawn.*\/bin\/sh/i,
  /node.*net\.connect.*exec/i,

  // Socat
  /socat\s+.*TCP:.*EXEC:/i,
  /socat\s+.*EXEC:/i,

  // PowerShell
  /powershell.*-NoP.*-NonI.*-W/i,
  /powershell.*IEX.*New-Object/i,
  /powershell.*tcp/i,

  // Tmux/Screen
  /tmux.*new-session.*-d.*-s/i,
  /screen.*-dmS/i,
];
```

### File System Threat Detection (v3 Enhanced)

#### Critical Paths (Read/Write Attempt = High Risk)

**Also scan these paths inside SKILL.md code blocks!**

```javascript
const CRITICAL_PATHS = [
  // Credentials
  '/.ssh/',
  '/.aws/',
  '/.kube/',
  '/.gcp/',
  '/.docker/',
  '/.npm/',
  '/.pypirc/',

  // Environment & Config
  '/.env',
  '/.bashrc',
  '/.bash_profile',
  '/.zshrc',
  '/.profile',

  // System
  '/etc/passwd',
  '/etc/shadow',
  '/etc/sudoers',
  '/etc/cron',

  // Application
  '/home/',
  '/root/',
  '/var/',

  // OpenClaw specific
  '/.openclaw/',
  '/.claude/',
  '/workspace/MEMORY',
  '/workspace/IDENTITY',
  '/workspace/SOUL',
];
```

#### Detection Rules

| Pattern | Severity | Example |
|---------|----------|---------|
| Read critical path | HIGH | `readFile('/etc/passwd')` |
| Write to critical path | CRITICAL | `writeFile('/.ssh/authorized_keys')` |
| Modify cron | CRITICAL | `echo '* * * * *' >> /etc/crontab` |
| SSH key access | CRITICAL | `readFile('~/.ssh/id_rsa')` |

### Obfuscation Detection (v3 Enhanced)

#### Layer 1: Common Encodings

| Encoding | Detection Pattern | Risk |
|----------|------------------|------|
| Base64 | `/^[A-Za-z0-9+/]+={0,2}$/` with len > 20 | MEDIUM |
| Hex | `/^[0-9a-fA-F]+$/` with len > 16 | MEDIUM |
| URL Encoding | `%[0-9A-F]{2}` repeated | LOW |
| Unicode Escape | `\u[0-9A-F]{4}` | MEDIUM |

#### Layer 2: Advanced Obfuscation

| Technique | Detection | Risk |
|-----------|-----------|------|
| String concatenation to hide keywords | `'co'+'ncat'` | HIGH |
| Array join | `['co','ncat'].join('')` | HIGH |
| Character codes | `String.fromCharCode(99, 111, 110, 99, 97, 116)` | HIGH |
| Dynamic code evaluation | `new Function('code')()` | CRITICAL |
| JSFuck | `/\[!\+\[\]/.test(code)` | CRITICAL |
| Zero-width characters | `\u200B\u200C\u200D` | CRITICAL |
| Right-to-Left Override | `\u202E` | CRITICAL |

#### Layer 3: Multi-stage Obfuscation

Detect chains of encoding:
- Base64 → URL → Hex
- Character codes → eval
- Compression → Base64 → eval

## Phase 4: Semantic Intent Analysis (v3 核心功能)

### Intent Mismatch Detection

Unlike basic vetters, ClawGuard analyzes if the Skill's **actual behavior** matches its **stated purpose**.

### Capability-Behavior Mapping

Map required capabilities to actual usage:

```javascript
const CAPABILITY_MATRIX = {
  'CAP_FS_READ': {
    allowed: ['workspace/*', '*.txt', '*.md', '*.json'],
    denied: ['~/.ssh/*', '~/.aws/*', '/etc/*'],
  },
  'CAP_FS_WRITE': {
    allowed: ['workspace/*', 'tmp/*'],
    denied: ['~/.ssh/*', '/etc/*', '~/.bashrc'],
  },
  'CAP_NET_EGRESS': {
    allowed: ['api.github.com', 'api.openai.com', '*.vercel.app'],
    denied: ['*'],
    requires_justification: true,
  },
  'CAP_SYS_EXEC': {
    allowed: ['git', 'npm', 'node', 'python'],
    denied: ['nc', 'ncat', 'socat', 'ssh', 'sudo'],
    requires_justification: true,
  },
};
```

## Phase 5: Supply Chain Security

### Dependency Analysis

#### Package.json Analysis

```javascript
const SUSPICIOUS_NPM_PATTERNS = [
  // Typosquatting targets
  /^react-/,
  /^vue-/,
  /^express-/,
  /^lodash-/,
  /^axios-/,
  /^moment-/,

  // Pseudo packages
  /^npm-/,
  /^node-/,

  // Hidden execution
  'preinstall',
  'postinstall',
  'prepublish',
  'prepare',
];
```

#### Requirements.txt Analysis

```python
SUSPICIOUS_PIP_PATTERNS = [
    # Typosquatting
    r'^requests-',
    r'^urllib3-',
    r'^numpy-',
    r'^pandas-',

    # Code execution
    r'--index-url.*http:',  # HTTP instead of HTTPS
    r'--extra-index-url.*http:',
]
```

### CVE Scanning (Enhanced)

| Source | Coverage | Update Frequency |
|--------|----------|-----------------|
| NVD API | CVEs 2002-2024 | Daily |
| GitHub Advisory | npm packages | Hourly |
| OSV | All ecosystems | Hourly |

#### Vulnerability Severity Mapping

| Severity | CVSS Score | Action |
|----------|------------|--------|
| CRITICAL | 9.0-10.0 | Auto-reject |
| HIGH | 7.0-8.9 | Block + Warn |
| MEDIUM | 4.0-6.9 | Log + Warn |
| LOW | 0.1-3.9 | Log only |

### Registry Reputation Scoring

| Registry | Score | Trust Level |
|----------|-------|-------------|
| npm (official) | 80 | High |
| PyPI (official) | 80 | High |
| GitHub Packages | 70 | Medium-High |
| Unverified mirrors | 10 | Low |

## Phase 6: ML-based Anomaly Detection

### Feature Extraction

Extract features from code for ML model:

```javascript
const FEATURES = {
  // Structural features
  'ast_depth': 0,           // AST tree depth
  'function_count': 0,      // Number of functions
  'loop_nesting': 0,        // Maximum loop nesting
  'dynamic_code_ratio': 0,   // Ratio of dynamic code

  // Behavioral features
  'network_calls': 0,       // Count of network operations
  'file_operations': 0,     // Count of file operations
  'process_spawns': 0,      // Count of process spawns

  // Obfuscation features
  'encoded_strings': 0,     // Count of encoded strings
  'obfuscation_score': 0,   // Obfuscation intensity
  'entropy': 0,             // String entropy

  // Anomaly indicators
  'suspicious_patterns': [], // Matched suspicious patterns
  'risk_signals': [],       // Risk factor signals
};
```

### Novel Attack Detection

ClawGuard uses ensemble detection to identify novel attacks:

```
FINAL_SCORE = 0.3 * RULE_BASED + 0.3 * ISOLATION_FOREST + 0.4 * NEURAL_NET

If FINAL_SCORE > 0.75: Flag as novel threat
```

## Output Format

### Terminal Output (v3 Enhanced)

```
╔══════════════════════════════════════════════════════════════╗
║           🛡️ CLAWGUARD AUDIT REPORT v3.0.0            ║
╠══════════════════════════════════════════════════════════════╣
║ Target: example-skill v1.0.0                               ║
║ Path:   /workspace/skills/example-skill                     ║
║ Time:   YYYY-MM-DD HH:MM:SS                               ║
╚══════════════════════════════════════════════════════════════╝

📋 METADATA ✓
   ✓ Valid frontmatter
   ✓ Category: utility
   ✓ Risk: safe

🔍 SAST ANALYSIS 🔍
   [CRITICAL: 0] [HIGH: 2] [MEDIUM: 3] [LOW: 1]

   ⚠️ HIGH: Dynamic code execution (src/index.js:42)
      Evidence: eval(userInput)

   ⚠️ HIGH: Sensitive file access (SKILL.md code block)
      Evidence: readFile('~/.ssh/id_rsa')

🧠 SEMANTIC INTENT ANALYSIS (v3)
   Match Score: 25%
   Stated: "Weather formatting tool"
   Actual: "Reads SSH keys and exfiltrates data"
   Status: ❌ SEVERE MISMATCH

📦 SUPPLY CHAIN SECURITY
   Dependencies: 15
   Vulnerabilities: 0
   Typosquatting: 0

🤖 ML ANOMALY DETECTION
   Score: 85/100 [MALICIOUS]
   - Isolation Forest: 80%
   - Neural Network: 90%

╔══════════════════════════════════════════════════════════════╗
║ VERDICT: REJECTED                                         ║
║ RISK TIER: 🔴 TIER_4 (Critical Risk)                     ║
║ RISK SCORE: 95/100                                        ║
╠══════════════════════════════════════════════════════════════╣
║ RECOMMENDATION: REJECTED - Critical security issues found  ║
║                                                                ║
║ Issues:                                                    ║
║ 1. SSH key access detected                                 ║
║ 2. Severe intent mismatch (25% match)                       ║
║ 3. Data exfiltration pattern detected                       ║
╚══════════════════════════════════════════════════════════════╝
```

## Risk Scoring Formula (v3)

```
FINAL_SCORE = BASE_PENALTY + SAST_PENALTY + INTENT_PENALTY + SUPPLY_CHAIN_PENALTY + ML_PENALTY

BASE_PENALTY = Provenance score < 50 ? 20 : 0

SAST_PENALTY = CRITICAL*25 + HIGH*15 + MEDIUM*5 + LOW*1

INTENT_PENALTY (v3) = Intent match < 0.3 ? 35 : (Intent match < 0.5 ? 25 : (Intent match < 0.8 ? 10 : 0))

SUPPLY_CHAIN_PENALTY = CVEs.critical*20 + CVEs.high*10 + CVEs.medium*5 + typosquatting*15

ML_PENALTY = ML score > 0.75 ? 25 : (ML score > 0.5 ? 10 : 0)
```

### Risk Tier Classification

| Tier | Score Range | Color | Action |
|------|-------------|-------|--------|
| **TIER_0** | 0-10 | 🟢 GREEN | Auto-approve |
| **TIER_1** | 11-30 | 🟢 GREEN | Approve with logging |
| **TIER_2** | 31-50 | 🟡 YELLOW | Manual review |
| **TIER_3** | 51-70 | 🟠 ORANGE | Deep audit required |
| **TIER_4** | 71-100 | 🔴 RED | Auto-reject |

## Integration with OpenClaw

### Installation Flow

```
User: /install-skill <repo-url>
    │
    ▼
┌─────────────────────────────┐
│ OpenClaw Core               │
│ - Download skill to temp    │
│ - Call ClawGuard Auditor   │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ ClawGuard Auditor          │
│ - Run full audit pipeline  │
│ - Return verdict + report  │
└─────────────┬───────────────┘
              │
       ┌──────┴──────┐
       │ VERDICT     │
       ├─────────────┤
       │ APPROVED    │ → Install to /workspace/skills/
       │ CONDITIONAL │ → Prompt user for confirmation
       │ REJECTED   │ → Quarantine + Alert
       └─────────────┘
```

## Quick Detection Commands

```bash
# Check sensitive file access
grep -r "\.ssh\|\.aws\|\.kube\|/etc/passwd" <skill-dir>

# Check network requests
grep -r "http\.\|fetch\|axios\|request" <skill-dir>

# Check command execution
grep -r "exec\|spawn\|child_process\|subprocess" <skill-dir>

# Check for obfuscation
grep -r "atob\|btoa\|base64\|Buffer\.from" <skill-dir>

# Check SKILL.md code blocks
grep -A50 '```javascript' <skill-dir>/SKILL.md | grep -E "exec|eval|readFile|http\."

# Check for malicious domains
grep -r "evil\|attacker\|malicious\|hacker" <skill-dir>
```

## v3 vs v2 Features

| Feature | v2 | v3 |
|---------|----|----|
| SAST Analysis | ✅ | ✅ |
| Intent Analysis | Basic | **Advanced (v3)** |
| **SKILL.md Code Scanning** | ❌ | **✅ (v3)** |
| Supply Chain Security | ✅ | ✅ |
| ML Anomaly Detection | ✅ | ✅ |
| Obfuscation Detection | ✅ | **Enhanced (v3)** |
| **Intent Mismatch Scoring** | ❌ | **✅ (v3)** |
| **Five-Tier Risk System** | 3 tiers | **5 tiers (v3)** |

---

*ClawGuard Auditor: Security takes precedence over execution.* 🦅
