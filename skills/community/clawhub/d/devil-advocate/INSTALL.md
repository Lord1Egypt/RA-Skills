
# Devil's Advocate Skill - Installation Guide

## Manual Installation

### 1. Copy the skill to OpenClaw skills directory

```powershell
# Windows
xcopy /E /I devil-advocate %USERPROFILE%\.openclaw\skills\devil-advocate

# Linux/Mac
cp -r devil-advocate ~/.openclaw/skills/devil-advocate
```

### 2. Restart OpenClaw Gateway

```bash
openclaw restart
```

### 3. Verify Installation

Open Dashboard and check if the skill is loaded:
http://127.0.0.1:18789/

---

## Verify Effectiveness

After installation, you can test with the following questions:

1. "What database should I use?"
2. "Does this code need optimization?"
3. "Should we refactor this module?"

Observe if the answer:
- Considers multiple perspectives
- Mentions risks and limitations
- Provides alternative solutions
- Avoids overly absolute statements

---

## Uninstall

```powershell
# Windows
rmdir /S /Q %USERPROFILE%\.openclaw\skills\devil-advocate

# Linux/Mac
rm -rf ~/.openclaw/skills/devil-advocate
```
