---
name: cuihua-dependency-updater
description: |
  📦 AI-powered dependency update assistant. Intelligently update npm/yarn packages with safety checks,
  breaking change detection, and automated testing. Keep dependencies fresh without breaking your app.

metadata:
  openclaw:
    requires:
      bins: [node, npm]
      env: []
    primaryEnv: null
  
  version: "1.0.0"
  author: "翠花 (Cuihua) - ClawHub Pioneer"
  license: "MIT"
  tags:
    - dependencies
    - npm
    - yarn
    - updates
    - security
    - package-management
    - automation

capabilities:
  - Intelligent update prioritization
  - Breaking change detection
  - Security vulnerability scanning
  - Automated changelog generation
  - Safe rollback mechanism
  - Batch update strategies
---

# cuihua-dependency-updater 📦

> **Keep dependencies fresh, keep your app safe**

AI-powered dependency management that updates packages intelligently:
- 🔒 **Security-first** - Prioritize security patches
- 🛡️ **Safe updates** - Detect breaking changes before updating
- 🤖 **Smart batching** - Group compatible updates
- 📝 **Auto changelog** - Generate update summaries
- ⏮️ **Easy rollback** - Undo problematic updates

## 🎯 Why cuihua-dependency-updater?

**The problem**:
- ❌ `npm outdated` shows 50+ packages to update
- ❌ No idea which ones are safe to update
- ❌ Breaking changes break your app
- ❌ Security patches mixed with feature updates
- ❌ Manual updates take hours

**cuihua-dependency-updater solves this.**

---

## 🚀 Quick Start

### Check for updates

> "Check outdated dependencies"

**Output**:
```
📦 Dependency Update Report
━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Security updates (3):
  - lodash: 4.17.19 → 4.17.21 (CVE-2020-8203)
  - minimist: 1.2.5 → 1.2.6 (CVE-2021-44906)
  - axios: 0.21.1 → 1.6.0 (CVE-2023-45857)

🟡 Breaking changes (2):
  - webpack: 4.46.0 → 5.89.0 (Major version)
  - react: 17.0.2 → 18.2.0 (Major version)

🟢 Safe updates (12):
  - typescript: 4.9.5 → 5.3.3 (Minor)
  - eslint: 8.50.0 → 8.56.0 (Patch)
  ...

💡 Recommendation: Update security first
```

### Update by priority

> "Update security vulnerabilities"

**Generated**:
```bash
npm update lodash minimist axios
npm audit fix
```

### Smart batch update

> "Update all safe dependencies"

Automatically:
1. Groups compatible updates
2. Tests each batch
3. Rolls back if tests fail
4. Generates changelog

---

## 🎨 Features

### 1. Intelligent Prioritization 🎯

Updates are categorized by risk and impact:

```javascript
{
  "security": [
    { package: "lodash", severity: "high", cve: "CVE-2020-8203" }
  ],
  "breaking": [
    { package: "webpack", from: "4.x", to: "5.x", impact: "high" }
  ],
  "safe": [
    { package: "typescript", from: "4.9", to: "5.3", impact: "low" }
  ]
}
```

### 2. Breaking Change Detection 🔍

AI analyzes changelogs and API changes:

```
⚠️  Breaking changes detected in react@18:

1. ReactDOM.render → createRoot
   Impact: ALL entry points need updates
   
2. Automatic batching
   Impact: State updates may batch differently
   
3. Stricter hydration
   Impact: SSR apps may break

Recommendation: Schedule major update separately
Estimated effort: 2-4 hours
```

### 3. Security Scanning 🔒

Integrates with npm audit and vulnerability databases:

```
🔴 HIGH severity vulnerability
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Package: lodash@4.17.19
CVE: CVE-2020-8203
Severity: HIGH
Impact: Prototype pollution

Affected paths:
  - app → lodash (direct)
  - webpack → lodash (indirect)

Fix available: lodash@4.17.21
Risk: LOW (patch version)

🚀 Safe to update immediately
```

### 4. Automated Testing 🧪

Run tests after each update batch:

```javascript
async function safeUpdate(packages) {
  // Backup current state
  const backup = await saveState();
  
  try {
    // Update packages
    await npm.update(packages);
    
    // Run tests
    const testsPassed = await runTests();
    
    if (!testsPassed) {
      throw new Error('Tests failed');
    }
    
    console.log('✅ Update successful');
    
  } catch (error) {
    // Rollback on failure
    await restore(backup);
    console.log('⏮️  Rolled back due to:', error.message);
  }
}
```

### 5. Changelog Generation 📝

Auto-generate human-readable update summaries:

```markdown
# Dependency Updates - 2026-03-24

## Security Fixes (3)
- lodash: 4.17.19 → 4.17.21
  - Fixed: Prototype pollution vulnerability
  - CVE: CVE-2020-8203
  
- axios: 0.21.1 → 1.6.0
  - Fixed: SSRF vulnerability
  - CVE: CVE-2023-45857

## Feature Updates (5)
- typescript: 4.9.5 → 5.3.3
  - Added: Better type inference
  - Added: Decorators support
  
- eslint: 8.50.0 → 8.56.0
  - Fixed: Several bugs
  - Added: New rules

## Breaking Changes (Postponed)
- webpack: 4.46.0 → 5.89.0
  - Reason: Requires configuration migration
  - Estimated effort: 4 hours
  - Scheduled: Next sprint
```

---

## 📋 Usage Examples

### Example 1: Security Audit

**User**: "Audit dependencies for security issues"

**Agent**:
```
🔍 Security Audit Report
━━━━━━━━━━━━━━━━━━━━━━

Total packages: 1,234
Vulnerabilities: 8

🔴 CRITICAL (1)
  - express-fileupload@1.1.7
    CVE-2020-7699 (RCE)
    Fix: Update to 1.4.0

🟠 HIGH (3)
  - lodash@4.17.19 → 4.17.21
  - minimist@1.2.5 → 1.2.6
  - axios@0.21.1 → 1.6.0

🟡 MEDIUM (4)
  - qs@6.5.2 → 6.11.0
  - ...

💡 Action: npm audit fix --force
Risk: All fixes are patch/minor versions
```

### Example 2: Major Version Update

**User**: "Can I safely update React to v18?"

**Agent**:
```
🔍 Analyzing React 17 → 18 migration...

✅ Compatibility Check:
  - react-dom: Compatible
  - react-router: Needs update to v6
  - redux: Compatible
  - typescript: Compatible

⚠️  Breaking Changes:
  1. ReactDOM.render API removed
     Files affected: 2 (src/index.js, src/test-utils.js)
     
  2. Automatic batching changes
     Potential impact: State update timing
     
  3. Stricter TypeScript types
     Files affected: 15

📊 Migration complexity: MEDIUM
Estimated time: 2-3 hours
Recommendation: Update in separate PR

🔧 Migration steps:
  1. Update packages
  2. Replace ReactDOM.render
  3. Fix TypeScript errors
  4. Test thoroughly
  
Want me to generate a migration guide?
```

### Example 3: Batch Update

**User**: "Update all safe dependencies"

**Agent**:
```
📦 Preparing batch update...

Grouped into 3 batches:

Batch 1 (Testing tools - 5 packages):
  - jest: 29.5.0 → 29.7.0
  - @testing-library/react: 14.0.0 → 14.1.2
  - ...

Batch 2 (Build tools - 4 packages):
  - vite: 5.0.0 → 5.0.10
  - esbuild: 0.19.0 → 0.19.11
  - ...

Batch 3 (Utils - 8 packages):
  - date-fns: 2.30.0 → 3.0.6
  - lodash: 4.17.19 → 4.17.21
  - ...

Process:
1. Update Batch 1 → Run tests → ✅
2. Update Batch 2 → Run tests → ✅
3. Update Batch 3 → Run tests → ✅

✅ All updates successful!
📝 Changelog: UPDATES.md
```

---

## ⚙️ Configuration

Create `.dependencyrc.json`:

```json
{
  "updateStrategy": "conservative",
  "priorities": [
    "security",
    "patch",
    "minor",
    "major"
  ],
  "autoUpdate": {
    "security": true,
    "patch": true,
    "minor": false,
    "major": false
  },
  "testing": {
    "runTests": true,
    "testCommand": "npm test",
    "rollbackOnFail": true
  },
  "exclude": [
    "react",
    "webpack"
  ],
  "changelog": {
    "generate": true,
    "path": "./UPDATES.md"
  }
}
```

---

## 🔧 Update Strategies

### Conservative (Default)
- Security: Auto-update
- Patch: Auto-update
- Minor: Manual review
- Major: Manual review

### Aggressive
- Security: Auto-update
- Patch: Auto-update
- Minor: Auto-update
- Major: Manual review

### Custom
Define your own rules per package:

```json
{
  "packages": {
    "lodash": "aggressive",
    "react": "manual",
    "typescript": "conservative"
  }
}
```

---

## 💰 Pricing

### Free
- ✅ Dependency analysis
- ✅ Security scanning
- ✅ Up to 100 packages

### Pro ($10/month)
- ✅ Unlimited packages
- ✅ Automated updates
- ✅ CI/CD integration
- ✅ Custom strategies

### Enterprise ($79/month)
- ✅ Team policies
- ✅ Monorepo support
- ✅ Advanced rollback
- ✅ Compliance reports

---

## 📚 Resources

- 📖 [Full Documentation](./docs/README.md)
- 🎓 [Migration Guides](./docs/migrations.md)
- 💬 [Discord Community](https://discord.gg/clawd)

---

## 📜 License

MIT

---

## 🙏 Acknowledgments

Built with 🌸 by 翠花 (Cuihua)

---

**Made with 🌸 | Cuihua Series | ClawHub Pioneer**

_Keep dependencies fresh, keep your app safe._
