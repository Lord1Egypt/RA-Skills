# code-reviewer Examples

## Example 1: Review a Single File

### User Request
> "Review the security of auth.js"

### Agent Action
```javascript
const CodeReviewer = require('./analyzer.js');
const reviewer = new CodeReviewer();
await reviewer.analyzeFile('./src/auth.js');
console.log(reviewer.generateReport('terminal'));
```

### Output
```
🔍 Code Review Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Files analyzed: 1
📝 Lines analyzed: 156
⚠️  Issues found: 3

Severity Breakdown:
  🔴 Critical: 1
  🟠 High:     1
  🟡 Medium:   1
  🟢 Low:      0

Top Issues:
  1. [🔴 CRITICAL] Hardcoded API Key (auth.js:12)
  2. [🟠 HIGH] Dangerous eval() Usage (auth.js:45)
  3. [🟡 MEDIUM] Missing Error Handling (auth.js:1)

💡 Run with --detailed for full report
```

---

## Example 2: Full Project Review

### User Request
> "Generate a complete code review report for my project"

### Agent Action
```javascript
const CodeReviewer = require('./analyzer.js');
const fs = require('fs');
const path = require('path');

const reviewer = new CodeReviewer({
  languages: ['javascript', 'python'],
  severity: 'medium',
  output: 'markdown'
});

// Analyze all files
const analyzeDir = (dir) => {
  const files = fs.readdirSync(dir);
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory() && file !== 'node_modules') {
      analyzeDir(filePath);
    } else if (stat.isFile()) {
      const ext = path.extname(file);
      if (['.js', '.py'].includes(ext)) {
        reviewer.analyzeFile(filePath);
      }
    }
  });
};

analyzeDir('./src');

// Generate detailed report
const report = reviewer.generateReport('markdown');
fs.writeFileSync('code-review-report.md', report);

console.log('✅ Review complete! Report saved to code-review-report.md');
console.log(reviewer.generateReport('terminal'));
```

---

## Example 3: Pre-commit Hook

### User Request
> "Check my staged changes before I commit"

### Agent Action
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 Running code review on staged files..."

# Get staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(js|py)$')

if [ -z "$STAGED_FILES" ]; then
  echo "✅ No code files to review"
  exit 0
fi

# Run code review
node ~/.openclaw/workspace/skills/code-reviewer/analyzer.js $STAGED_FILES

if [ $? -ne 0 ]; then
  echo "❌ Code review found critical issues. Commit aborted."
  echo "💡 Fix the issues or use 'git commit --no-verify' to skip"
  exit 1
fi

echo "✅ Code review passed!"
exit 0
```

---

## Example 4: CI/CD Integration

### GitHub Actions Workflow

```yaml
name: Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install code-reviewer
        run: npx clawhub install code-reviewer
      
      - name: Run code review
        run: |
          node code-reviewer/analyzer.js ./src --detailed
          cat code-review-report.md >> $GITHUB_STEP_SUMMARY
      
      - name: Check for critical issues
        run: |
          CRITICAL=$(grep -c "CRITICAL" code-review-report.md || true)
          if [ $CRITICAL -gt 0 ]; then
            echo "❌ Found $CRITICAL critical issues"
            exit 1
          fi
```

---

## Example 5: Slack Notification

### User Request
> "Review the code and notify the team on Slack"

### Agent Action
```javascript
const CodeReviewer = require('./analyzer.js');
const https = require('https');

const reviewer = new CodeReviewer();
// ... analyze files ...

const report = reviewer.generateReport('terminal');

// Send to Slack
const slackWebhook = process.env.SLACK_WEBHOOK_URL;
const payload = {
  text: '🔍 Code Review Results',
  blocks: [
    {
      type: 'section',
      text: {
        type: 'mrkdwn',
        text: `\`\`\`\n${report}\n\`\`\``
      }
    }
  ]
};

const req = https.request(slackWebhook, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' }
}, (res) => {
  console.log('✅ Sent to Slack');
});

req.write(JSON.stringify(payload));
req.end();
```

---

## Example 6: Custom Rules

### .codereview.json
```json
{
  "severity": {
    "min": "high",
    "failOnCritical": true
  },
  "ignore": {
    "files": [
      "*.test.js",
      "*.spec.js",
      "dist/*",
      "build/*"
    ],
    "rules": [
      "magic-numbers",
      "console-log"
    ]
  },
  "languages": ["javascript", "typescript"],
  "output": {
    "format": "markdown",
    "path": "./reports/code-review.md"
  },
  "checks": {
    "security": true,
    "performance": true,
    "quality": true,
    "bestPractices": true
  }
}
```

---

## Example 7: Interactive Review Session

### User Conversation
```
User: Review my code

Agent: I'll run a code review on your project. Give me a moment...
[Analyzing...]

Agent: ⚠️ Found 5 issues in your code:

1. 🔴 CRITICAL - SQL Injection in query.js:45
   Would you like me to show you how to fix this?

User: Yes, show me the fix

Agent: Here's the vulnerable code:
```js
const query = `SELECT * FROM users WHERE id = ${userId}`;
```

And here's the secure version:
```js
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

I can apply this fix for you. Should I proceed?

User: Yes, please fix it

Agent: ✅ Fixed! The file has been updated.
Would you like me to review the other 4 issues?
```

---

## Example 8: Scheduled Reviews

### Cron Job
```bash
# Run daily code review at 2 AM
0 2 * * * cd /path/to/project && node code-reviewer/analyzer.js ./src --detailed && mail -s "Daily Code Review" team@company.com < code-review-report.md
```

---

## Example 9: IDE Integration (VS Code)

### tasks.json
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Review Current File",
      "type": "shell",
      "command": "node",
      "args": [
        "${workspaceFolder}/code-reviewer/analyzer.js",
        "${file}"
      ],
      "group": "test",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

### Keybinding (keybindings.json)
```json
{
  "key": "ctrl+shift+r",
  "command": "workbench.action.tasks.runTask",
  "args": "Review Current File"
}
```

---

## Example 10: API Server Mode

### server.js
```javascript
const express = require('express');
const CodeReviewer = require('./analyzer.js');
const app = express();

app.use(express.json());

app.post('/review', async (req, res) => {
  const { code, language } = req.body;
  
  const reviewer = new CodeReviewer({ languages: [language] });
  
  // Write code to temp file
  const tempFile = `/tmp/review-${Date.now()}.${language}`;
  fs.writeFileSync(tempFile, code);
  
  // Analyze
  await reviewer.analyzeFile(tempFile);
  
  // Clean up
  fs.unlinkSync(tempFile);
  
  // Return results
  res.json({
    stats: reviewer.stats,
    issues: reviewer.issues
  });
});

app.listen(3000, () => {
  console.log('🔍 Code review API running on port 3000');
});
```

### Usage
```bash
curl -X POST http://localhost:3000/review \
  -H "Content-Type: application/json" \
  -d '{
    "code": "const password = \"admin123\";",
    "language": "javascript"
  }'
```

---

**Made with 🌸 by 翠花**
