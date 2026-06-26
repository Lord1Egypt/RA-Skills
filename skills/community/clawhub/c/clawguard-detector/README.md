# 🛡️ ClawGuard Detect (CG-TD)

**ClawGuard Detect** is a real-time behavioral monitoring and threat detection system for OpenClaw environments. It provides continuous runtime protection by detecting attacks as they happen, including data exfiltration, reverse shells, privilege escalation, and prompt injection.

## 🌟 Why ClawGuard Detect?

Static analysis and configuration checks happen before execution, but threats can also occur during runtime. ClawGuard Detect:

- **Real-time Monitoring**: Watches commands, file access, and network traffic
- **Attack Chain Detection**: Correlates multi-stage attacks
- **Prompt Injection**: Detects malicious user inputs
- **MITRE ATT&CK Coverage**: Maps detections to industry standards
- **ML Anomaly Detection**: Uses machine learning for novel threats

## 🚀 How to Install & Load ClawGuard Detect

Place the `detect-skill` folder in your OpenClaw skills directory:

```
/workspace/skills/clawguard-detect/
```

Then load it:

> *"Please load and activate the threat detector at `path/to/ClawGuard/detect-skill`"*

## 🛡️ How to Use ClawGuard Detect

### Automatic Protection

Once loaded, ClawGuard Detect runs continuously:

- **Command Monitoring**: Every executed command is analyzed
- **File Access**: Sensitive file access triggers alerts
- **Network Traffic**: Outbound connections are checked
- **Prompt Analysis**: User inputs are scanned for injection

### Manual Threat Check

Check for specific threats:

> *"Check if there are any active threats in this session"*

## 🔍 What Does ClawGuard Detect Monitor?

### 1. Command Monitoring

Detects malicious commands:
- Data exfiltration (`curl` with credentials)
- Reverse shells (bash, nc, python, etc.)
- Privilege escalation (sudo, chmod 777)
- Persistence mechanisms (cron, SSH keys)

### 2. File Access Monitoring

Watches for unauthorized access to:
- Credential files (.ssh, .aws, .env)
- System files (/etc/passwd, /etc/shadow)
- History files (.bash_history)
- OpenClaw memory files

### 3. Network Traffic Analysis

Monitors outbound connections:
- Suspicious domains
- Hardcoded IP addresses
- DNS tunneling
- Data exfiltration

### 4. Prompt Injection Detection

Analyzes user inputs for:
- Role hijacking ("you are now...")
- Instruction override ("ignore previous...")
- Jailbreak attempts (DAN, developer mode)
- Hidden commands (HTML/CSS/Unicode)

### 5. Attack Chain Detection

Correlates events across time:
- Reconnaissance → Access → Exfiltration
- Privilege escalation → Persistence
- Any multi-stage attack pattern

## 🎯 MITRE ATT&CK Coverage

ClawGuard Detect maps detections to MITRE ATT&CK:

| Tactic | Techniques | Coverage |
|--------|-----------|----------|
| Execution | T1059 (Command/Script) | ✅ |
| Persistence | T1053, T1098, T1543 | ✅ |
| Privilege Escalation | T1068, T1548 | ✅ |
| Credential Access | T1003, T1056, T1552 | ✅ |
| Discovery | T1082, T1083 | ✅ |
| Exfiltration | T1041, T1048, T1567 | ✅ |
| Command & Control | T1071, T1132 | ✅ |

## 🚨 Alert Severity Levels

| Level | Threshold | Response |
|-------|-----------|----------|
| CRITICAL | 1 match | Block + Alert + Log |
| HIGH | 1 match | Block + Alert |
| MEDIUM | 3+ matches/min | Alert + Log |
| LOW | 5+ matches/min | Log only |

## 📁 Project Structure

```
detect-skill/
├── SKILL.md              # Skill definition and documentation
├── README.md             # This file
├── cli.js                # Command-line interface
└── src/
    └── detector.js       # Real-time threat detection engine
```

## 🔧 Configuration

Customize detection sensitivity:

```javascript
const detector = new ThreatDetector({
  blockConfidence: 0.9,    // Block threshold
  alertConfidence: 0.7,    // Alert threshold
  autoBlock: true,         // Auto-block threats
  notifyUser: true         // Notify on threats
});
```

## ⚠️ Disclaimer

ClawGuard Detect is a security tool designed to reduce risk, but cannot guarantee 100% protection. Always follow the principle of least privilege when deploying autonomous agents.

---

**ClawGuard Detect: Your vigilant guardian against runtime threats.** 🦅
