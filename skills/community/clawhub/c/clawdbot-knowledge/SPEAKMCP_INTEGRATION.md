# Ockham Agent - SpeakMCP Integration Guide

Complete guide for integrating the Ockham Agent with your SpeakMCP installation.

---

## 📋 Prerequisites

- ✅ SpeakMCP installed and running
- ✅ Python 3.10+ installed
- ✅ Anthropic or OpenAI API key

---

## 🚀 Quick Setup (5 minutes)

### 1. Install Dependencies

```powershell
cd "C:\Download\speakmcp projekt\SpeakMCP\mcp-servers\ockham-agent"
pip install -r requirements.txt
```

### 2. Set API Key

**Option A: Environment Variable (Recommended)**
```powershell
# PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Or add to your PowerShell profile (~\Documents\PowerShell\Profile.ps1)
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'sk-ant-your-key', 'User')
```

**Option B: .env File**
```powershell
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" > .env
```

### 3. Test the Server

```powershell
python server.py
```

You should see:
```
Starting Ockham Agent MCP Server...
Supported languages: Python, TypeScript, Java
```

Press `Ctrl+C` to stop.

### 4. Add to SpeakMCP

**In SpeakMCP UI:**

1. Press `Ctrl+Shift+S` (open Settings)
2. Go to **MCP Servers** tab
3. Add the following configuration:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Download\\speakmcp projekt"]
    },
    "ockham-agent": {
      "command": "python",
      "args": ["mcp-servers/ockham-agent/server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

4. Click **Save**
5. Restart SpeakMCP

---

## 🎯 Usage Examples

### Example 1: Fix a Bug via Voice

**Say (hold Ctrl+Alt):**
```
"Use Ockham Agent to fix the NullPointerException in UserService.java line 42"
```

**What happens:**
1. SpeakMCP transcribes your voice
2. LLM calls `ockham_fix_bug` tool
3. Ockham Agent:
   - Analyzes the stacktrace
   - Finds relevant code
   - Generates 3 patch variants (tiny, small, fallback)
   - Tests each patch
   - Selects the simplest one that works
4. Results returned to you

### Example 2: Add a Feature

**Type (Ctrl+T):**
```
Use Ockham Agent to add email validation to the user registration form in src/components/RegisterForm.tsx
```

**Result:**
- Minimal TypeScript patch
- Tests pass
- ESLint clean
- TypeScript types correct

### Example 3: Evaluate a Patch

**Type:**
```
Evaluate this patch with Ockham Agent:
[paste your diff here]
```

**Result:**
- Complexity score
- Test results
- Lint results
- Security scan results
- Recommendation (accept/modify/reject)

---

## 🛠️ Integration Patterns

### Pattern 1: Automated Bug Triage

**Workflow:**
```
1. CI/CD detects test failure
2. Copy stacktrace
3. Speak: "Ockham, fix this: [paste stacktrace]"
4. Review proposed patch
5. Apply if acceptable
```

### Pattern 2: Code Review Assistant

**Workflow:**
```
1. Create feature branch with changes
2. Generate diff: git diff main...feature
3. Speak: "Ockham, evaluate my changes"
4. Review complexity report
5. Refactor if needed
```

### Pattern 3: Technical Debt Reduction

**Workflow:**
```
1. Identify duplicate code
2. Speak: "Ockham, refactor this duplicate logic in UserService"
3. Review minimal refactoring
4. Apply incrementally
```

---

## 📝 Voice Commands

Here are effective voice commands for Ockham Agent:

### Bug Fixing
```
"Ockham, fix the bug in file.py line 42"
"Use Ockham to fix the NullPointerException"
"Ockham Agent, solve this error: [describe error]"
```

### Feature Addition
```
"Ockham, add validation to the login form"
"Use Ockham Agent to implement rate limiting"
"Add feature with Ockham: [describe feature]"
```

### Refactoring
```
"Ockham, refactor this duplicate code"
"Use Ockham to simplify this function"
"Ockham Agent, clean up UserService"
```

### Evaluation
```
"Ockham, evaluate this patch"
"Use Ockham to check my changes"
"Ockham Agent, analyze this diff"
```

---

## ⚙️ Configuration Options

### Adjust Complexity Strictness

**Lenient (allows more complex solutions):**
```json
{
  "lambda_": 0.5
}
```

**Balanced (default):**
```json
{
  "lambda_": 1.0
}
```

**Strict (heavily favors minimal patches):**
```json
{
  "lambda_": 1.5
}
```

### Language-Specific Settings

**Python projects:**
```json
{
  "language": "python",
  "weights": {
    "loc": 1.0,
    "deps": 5.0
  }
}
```

**TypeScript projects:**
```json
{
  "language": "typescript",
  "weights": {
    "loc": 1.0,
    "api": 3.0
  }
}
```

---

## 🔧 Advanced Integration

### Custom Workflow Script

Create `fix_with_ockham.ps1`:

```powershell
param(
    [string]$IssueText,
    [string]$RepoPath = ".",
    [string]$Language = "python"
)

# Call Ockham Agent via SpeakMCP
$prompt = @"
Use Ockham Agent to fix this issue:
Issue: $IssueText
Repo: $RepoPath
Language: $Language
"@

# Use SpeakMCP CLI or voice
Write-Host $prompt
Write-Host "`nSpeak this into SpeakMCP (Ctrl+Alt)"
```

Usage:
```powershell
.\fix_with_ockham.ps1 -IssueText "NullPointerException in getUserData" -Language "java"
```

### Git Hook Integration

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Evaluate commits with Ockham before pushing

DIFF=$(git diff --cached)

if [ ! -z "$DIFF" ]; then
    echo "Evaluating changes with Ockham Agent..."

    # Call Ockham (requires SpeakMCP running)
    # Manual: paste diff into SpeakMCP and say "Ockham evaluate"

    echo "Review Ockham's analysis before pushing"
fi
```

---

## 📊 Monitoring & Feedback

### View Agent Logs

```powershell
# Ockham Agent logs
cat ockham-agent.log

# SpeakMCP logs
cat "$env:APPDATA\SpeakMCP\logs\main.log"
```

### Track Metrics

After using Ockham Agent, check:
- **Success rate**: How many patches passed all checks
- **Complexity scores**: Average complexity of accepted patches
- **Time saved**: Compared to manual fixes

---

## 🐛 Troubleshooting

### Ockham Agent Not Showing Up

**Check:**
1. MCP configuration is correct (see step 4 above)
2. Python dependencies installed
3. API key is set
4. SpeakMCP restarted after adding config

**Test manually:**
```powershell
cd mcp-servers\ockham-agent
python server.py
```

### "Module not found" Error

```powershell
# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
python --version  # Should be 3.10+
where python
```

### API Key Not Working

```powershell
# Verify API key
$env:ANTHROPIC_API_KEY

# Test API key
curl https://api.anthropic.com/v1/messages `
  -H "x-api-key: $env:ANTHROPIC_API_KEY" `
  -H "anthropic-version: 2023-06-01" `
  -H "content-type: application/json" `
  -d '{"model":"claude-3-sonnet-20240229","messages":[{"role":"user","content":"test"}],"max_tokens":10}'
```

### Tools Not Executing

**Check SpeakMCP logs:**
```powershell
cat "$env:APPDATA\SpeakMCP\logs\main.log" | Select-String "ockham"
```

**Common issues:**
- Agent mode not activated (use Ctrl+Alt, not just Ctrl)
- Wrong repo path in command
- Language not supported (only Python, TypeScript, Java)

---

## 💡 Tips & Best Practices

### 1. Start with Simple Cases

Begin with:
- ✅ Null pointer fixes
- ✅ Off-by-one errors
- ✅ Simple validation

Avoid initially:
- ❌ Large architectural changes
- ❌ Multi-module refactors
- ❌ New framework integrations

### 2. Review Before Applying

**Always:**
1. Read the generated patch
2. Check the complexity score
3. Verify tests passed
4. Review security scan
5. Apply incrementally

### 3. Tune for Your Project

After 5-10 uses, adjust:
- `lambda_` based on patch sizes
- Weights based on project priorities
- Language adapter commands

### 4. Use with Git Branches

```powershell
# Create feature branch
git checkout -b fix/ockham-$(Get-Date -Format "yyyyMMdd-HHmm")

# Let Ockham generate patch
# Review in branch
# Merge if good
```

---

## 📚 Learning Resources

### Documentation
- [Ockham Agent README](README.md)
- [SpeakMCP Documentation](../../README.md)
- [MCP Protocol](https://modelcontextprotocol.io/)

### Examples
- See `examples/` directory for sample workflows
- Check `tests/` for usage patterns

---

## 🎯 Success Checklist

- [ ] Dependencies installed
- [ ] API key configured
- [ ] Server runs manually
- [ ] MCP config added to SpeakMCP
- [ ] SpeakMCP restarted
- [ ] Voice command works
- [ ] First bug fixed successfully
- [ ] Patch evaluated and applied
- [ ] Complexity tuned for project

---

## 🆘 Getting Help

**Issues?**
1. Check this guide first
2. Review logs (Ockham + SpeakMCP)
3. Test components individually
4. Open issue on GitHub

**Community:**
- [SpeakMCP Discord](https://discord.gg/cK9WeQ7jPq)
- [GitHub Issues](https://github.com/aj47/SpeakMCP/issues)

---

**Ready to code with Ockham's Razor! ✂️🤖**
