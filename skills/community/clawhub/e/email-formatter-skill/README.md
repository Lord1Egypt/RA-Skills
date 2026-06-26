# Email Formatter Skill

Professional email formatting and analysis tool for AI agents.

## Quick Start

### Installation

```bash
chmod +x install.sh
./install.sh
```

The installer will:
- Create `~/.email-formatter-skill/` directory
- Copy helper scripts
- Install optional dependencies (if possible)
- Set up executable permissions

### Basic Usage

**Security Scan (Always run first):**
```bash
python3 ~/.email-formatter-skill/scripts/security_scan.py "Your email text here"
```

**Grammar Check:**
```bash
python3 ~/.email-formatter-skill/scripts/grammar_check.py "Your email text here"
```

**Tone Analysis:**
```bash
python3 ~/.email-formatter-skill/scripts/tone_analyzer.py "Your email text here"
```

**Readability Score:**
```bash
python3 ~/.email-formatter-skill/scripts/readability.py "Your email text here"
```

## What's Included

### Scripts

1. **security_scan.py** - Detects phishing, threats, harassment, and other security issues
2. **grammar_check.py** - Basic grammar and spelling checks
3. **tone_analyzer.py** - Analyzes email tone (formal, casual, aggressive, etc.)
4. **readability.py** - Calculates Flesch Reading Ease and readability metrics

### Features

✅ No external dependencies required (uses Python standard library)
✅ Optional enhanced features with `language-tool-python` and `textstat`
✅ Security-first approach - blocks dangerous content
✅ Comprehensive tone analysis
✅ Professional formatting guidelines
✅ Privacy-focused (no data storage)

## Workflow for AI Agents

```bash
# 1. Security scan first (CRITICAL)
python3 scripts/security_scan.py "$EMAIL_TEXT"
if [ $? -eq 2 ]; then
    echo "BLOCKED: Critical security issue"
    exit 1
fi

# 2. Analyze current state
python3 scripts/tone_analyzer.py "$EMAIL_TEXT"
python3 scripts/grammar_check.py "$EMAIL_TEXT"
python3 scripts/readability.py "$EMAIL_TEXT"

# 3. Format email using guidelines
# (Agent applies formatting rules from SKILL.md)

# 4. Re-scan formatted version
python3 scripts/security_scan.py "$FORMATTED_EMAIL"
```

## Exit Codes

- **0**: Success, no issues
- **1**: Warning, proceed with caution
- **2**: Critical block, do not proceed

## Requirements

- Python 3.7+
- Bash shell

### Optional (Enhanced Features)
- `language-tool-python`: Advanced grammar checking
- `textstat`: Additional readability metrics

## File Structure

```
~/.email-formatter-skill/
├── scripts/
│   ├── security_scan.py
│   ├── grammar_check.py
│   ├── tone_analyzer.py
│   └── readability.py
├── config.txt
└── (SKILL.md - reference documentation)
```

## Security Features

The security scanner detects:
- 🚨 Phishing attempts
- 🚨 Credential requests
- 🚨 Impersonation
- 🚨 Threats and harassment
- 🚨 Sensitive data leaks
- 🚨 Academic dishonesty
- ⚠️ Manipulation tactics
- ⚠️ Discriminatory content

## Examples

### Security Scan
```bash
$ python3 scripts/security_scan.py "Please verify your password immediately"

🛑 SECURITY SCAN RESULTS
🚨 CRITICAL ISSUES (1):
   • [PHISHING] Credential verification request
❌ BLOCKED: Cannot format this email
```

### Tone Analysis
```bash
$ python3 scripts/tone_analyzer.py "Hey! Let me know ASAP!!!"

📊 PRIMARY TONE: CASUAL
🎯 OTHER TONES: ENTHUSIASTIC, URGENT
⚠️ WARNINGS:
   • Too many exclamation marks (unprofessional)
```

### Grammar Check
```bash
$ python3 scripts/grammar_check.py "i recieved your email tommorow"

⚠️ ISSUES FOUND:
  • Grammar: 'i' should be capitalized to 'I'
  • Spelling: 'recieved' → 'received'
  • Spelling: 'tommorow' → 'tomorrow'
```

### Readability
```bash
$ python3 scripts/readability.py "This is a simple, clear email."

📖 Flesch Reading Ease: 82.3/100
📚 Reading Level: Easy (6th grade)
✅ Readability is good!
```

## License

MIT License - Free to use and modify

## Version

1.0.0

## Support

For issues or questions, refer to the main SKILL.md documentation.
