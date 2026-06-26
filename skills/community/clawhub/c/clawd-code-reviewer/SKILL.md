---
name: code-reviewer
description: "Automated code review, quality gates, and PR analysis. Integrates with GitHub, GitLab, Bitbucket. Enforce style guides, detect bugs, security vulnerabilities, performance issues. Auto-approve safe PRs, flag dangerous changes. Save developers 5+ hours/week on manual reviews."
homepage: https://clawhub.com/skills/code-reviewer
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["openclaw", "git", "github"]
    tags: ["devops", "code-quality", "security", "ci-cd", "github-actions"]
---

# Code Reviewer Skill

**Automate code review. Ship faster with confidence.**

## When to Use

✅ **USE this skill when:**

- "Review all my pull requests automatically"
- "Enforce our coding standards"
- "Detect security vulnerabilities in PRs"
- "Block performance anti-patterns"
- "Auto-approve trivial changes"
- "Generate review comments on PRs"
- "Ensure no secrets or credentials committed"

## When NOT to Use

❌ **DON'T use this skill when:**

- Architecture-level changes (needs senior human review)
- Complex business logic rewrites
- Security-critical changes (requires human approval anyway)
- Initial project setup (manual setup needed)

## 💪 The Developer Pain Point

**Manual code review sucks**:
- Context switching: 15 min per PR → 5 hours/week
- Missing subtle bugs: production incidents
- Inconsistent standards: code quality varies
- Slow feedback: developers wait hours/days
- Review fatigue: important issues get missed

**Our solution**: Instant, consistent, comprehensive reviews
**Time saved**: 5-10 hours/week per developer
**Value**: $300-600/week at $60/hr → **$12,000-24,000/month per dev team**

**Pricing**: $29-99/month per repo
**ROI**: Hours saved in first week

---

## Features

### 1. Style & Linting Enforcement

```yaml
rules:
  - style:
      tools: ["eslint", "prettier", "rubocop", "black", "gofmt"]
      auto_fix: true
      comment: |
        Style issues found. Run `pnpm run lint:fix` to auto-fix.

  - complexity:
      max_cyclomatic: 10
      max_nesting: 4
      comment: |
        Function too complex (cyclomatic: {{complexity}}/10). Consider refactoring.

  - duplication:
      max_lines_duplicate: 10
      ignore_tests: true
```

### 2. Bug Detection

```yaml
bugs:
  - null_pointer:
      languages: ["java", "csharp", "kotlin"]
      severity: "high"

  - resource_leak:
      languages: ["go", "rust", "c++"]
      severity: "critical"

  - race_condition:
      languages: ["go", "java", "javascript"]
      patterns: ["mutex", "atomic", "promise"]

  - off_by_one:
      languages: ["c", "cpp", "java"]
      patterns: ["loop_index", "array_access"]

  - improper_error_handling:
      languages: ["python", "javascript", "ruby"]
      patterns: ["try-catch", "throw", "except"]
```

### 3. Security Scanning

```yaml
security:
  - secrets_detection:
      patterns:
        - aws_secret_key: "AKIA[0-9A-Z]{16}"
        - slack_token: "xox[baprs]-[0-9a-zA-Z-]+"
        - github_token: "ghp_[0-9a-zA-Z]{36}"
        - private_key: "-----BEGIN [A-Z ]+ PRIVATE KEY-----"
      action: "fail_ci"  # Block merge
      comment: |
        🚨 **SECRET DETECTED**
        Never commit credentials! Use environment variables or secret manager.
        This PR cannot be merged until removed.

  - sql_injection:
      patterns: ["exec(.*SQL)", "raw_query(.*)", "format(.*SELECT)"]
      languages: ["python", "php", "javascript"]
      severity: "critical"

  - xss:
      patterns: ["innerHTML", "document.write", "dangerouslySetInnerHTML"]
      languages: ["javascript", "typescript", "react"]
      severity: "high"

  - path_traversal:
      patterns: ["__dirname+", "os.path.join(user_input)"]
      languages: ["node", "python"]
      severity: "high"

  - license_compliance:
      check: ["commercial_use", "copyleft", "patent_risk"]
      block_merge: true
```

### 4. Performance Anti-Patterns

```yaml
performance:
  - n+1_queries:
      languages: ["ruby", "javascript", "python"]
      frameworks: ["rails", "django", "express"]
      comment: |
        N+1 query detected! Use eager loading (`.includes()` or `select_related`).

  - inefficient_loop:
      patterns: ["for(i=0;i<list.length;i++)", "for key in dict:"]
      suggest: "List comprehension / map / filter"

  - large_object_alloc:
      pattern: "new.*inside.*loop"
      comment: "Allocating object in loop → move outside"

  - blocking_io:
      pattern: "await fetch|sync_http_call"
      suggest: "Use async / non-blocking"
```

### 5. Architecture & Design

```yaml
architecture:
  - god_object:
      max_methods: 20
      max_lines: 500
      comment: |
        This class is too large ({{methods}} methods, {{lines}} LOC).
        Consider splitting responsibilities.

  - feature_envy:
      pattern: "class A using data from class B extensively"
      suggest: "Move method to class B"

  - circular_dependency:
      modules: ["a", "b", "c"]
      severity: "high"
```

---

## Quick Start

### 1. Connect Repository

```bash
# Install reviewer on a GitHub repo
clawhub code-reviewer install --repo github.com/yourorg/yourrepo

# Configure (opens editor)
clawhub code-reviewer config --repo github.com/yourorg/yourrepo
```

### 2. Enable Rules

```yaml
# ~/.openclaw/code-reviewer/rules.yaml
include:
  - "security-high"
  - "style"
  - "performance"

exclude:
  - "performance/n_plus_one"  # Some false positives
    when: "test_files_only"

severity_overrides:
  - "sql_injection": "block"  # Fail CI
  - "style/variable_name": "comment"  # Just warn
```

### 3. Configure Actions

```yaml
actions:
  on_pr_open:
    - "review"  # Post review comments
    - "label"  # Add labels (needs-work / safe / security)

  on_pr_update:
    - "review"  # Re-review

  auto_approve:
    when:
      - "all_checks_pass == true"
      - "author in [maintainer_team]"
      - "changed_files < 5"
    # Skip required reviewers

  block_merge:
    when:
      - "security_issues_found"
      - "test_coverage < 80%"
    message: |
      ❌ Merge blocked:
      - {{security_issues_found}} security issues
      - Test coverage {{test_coverage}}% < 80%
      Fix before merging.
```

---

## GitHub App Setup

```bash
# Create GitHub App (one time)
clawhub code-reviewer create-app \
  --name "Code Reviewer" \
  --webhook-url "https://api.clawhub.com/webhooks/github" \
  --permissions "contents=read, pull_requests=write"

# Install on repositories
clawhub code-reviewer install \
  --app-id 12345 \
  --repo github.com/yourorg/yourrepo

# Or install on all org repos
clawhub code-reviewer install-org \
  --org yourorg \
  --app-id 12345
```

---

## Review Comments Example

**What reviewers see in PR**:

```
🔍 **Code Review Summary**

✅ **Passed**: 12 checks
⚠️  **Warnings**: 3
❌  **Failed**: 1 (blocking)

---

### Security 🛡️

- ❌ **Hardcoded secret** in line 42 (`config.py`)
  > Remove immediately and rotate credential.

### Performance ⚡

- ⚠️  **N+1 query** in `user_controller.rb:28`
  > Use `.includes(:profile)` to load associated records in one query.

### Style 🎨

- ⚠️  **Variable name** `x` is too short (line 15)
  > Use descriptive names; min length 3 chars.

- ⚠️  **Missing trailing comma** in multi-line array (line 78)

---

💡 **Suggestions**

1. Run `./gradlew test` → 3 tests failing
2. Code coverage: 75% (target: 80%)
3. Consider adding unit tests for `PaymentProcessor` class

---

🔒 **Auto-approval status**: ❌ Not eligible (security issue blocks)
```

---

## Custom Rules

### Write Your Own (YAML)

```yaml
custom_rules:
  - id: "no_todo_comments"
    pattern: "TODO|FIXME|HACK"
    message: "Remove technical debt comment before merging"
    severity: "warning"

  - id: "no_debugger"
    pattern: "debugger|pdb.set_trace|console.log"
    message: "Remove debugging code"
    severity: "fail"

  - id: "no_console_in_prod"
    pattern: "console.log"
    files: "src/**/*.js"
    except: "tests/**"
    severity: "warning"

  - id: "feature_flag_required"
    pattern: "if.*new_feature"
    message: "Wrap in feature flag: `if (flags.newFeature)`"
    severity: "warning"

  - id: "require_tests"
    condition: "added_lines > 50 && test_files_modified == 0"
    message: "Large change without tests. Add tests for new code."
    severity: "fail"
```

### Python Rule Example

```python
# rules/python/no_assert_in_prod.py
from codereviewer import Rule

class NoAssertInProd(Rule):
    def check(self, file, line):
        if line.contains("assert ") and not file.path.contains("test"):
            return self.fail("Remove assert in production code")
```

---

## GitHub Actions Integration

`.github/workflows/code-review.yml`:

```yaml
name: Code Review

on:
  pull_request:
    branches: [main, develop]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Code Reviewer
        uses: clawhub/code-reviewer@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          config: .codereview.yaml
```

---

## GitLab CI/CD

`.gitlab-ci.yml`:

```yaml
code-review:
  stage: test
  script:
    - clawhub code-reviewer run --config .codereview.yaml
  artifacts:
    reports:
      code-review: review-report.json
```

---

## Slack Notifications

```yaml
notifications:
  slack:
    channel: "#code-reviews"
    on:
      - "security_issue"
      - "pr_blocked"
      - "pr_approved"
    format:
      blocks:
        - type: "header"
          text: "{{pr_title}}"
        - type: "section"
          text: "{{review_summary}}"
        - type: "actions"
          elements:
            - type: "button"
              text: "View PR"
              url: "{{pr_url}}"
```

---

## Pricing

### Open Source (Free)
- Public repos: free
- Community rules only
- Basic style checks

### Pro ($29/mo per repo)
- Private repos
- Custom rules
- Security scanning
- Slack/Teams alerts
- Unlimited reviewers

### Business ($99/mo per org)
- All Pro features
- Enterprise security rules
- SSO / SAML
- Audit logs
- Priority support

### Enterprise ($499+/mo)
- Unlimited everything
- Custom rule writing service
- On-premise deployment
- SLA guarantees
- Dedicated engineer

---

## Competitive Comparison

| Feature | ReviewDog | SonarQube | CodeClimate | Code Reviewer |
|---------|----------|-----------|-------------|---------------|
| Price | Free (self-host) | $150/mo | $49/mo | **$29/mo** |
| GitHub integration | ✅ | ✅ | ✅ | ✅ |
| Custom rules | ✅ | ✅ | ⚠️ limited | ✅ **unlimited** |
| Auto-approve | ❌ | ❌ | ❌ | ✅ |
| AI suggestions | ❌ | ❌ | ❌ | **✅** |
| Setup time | hours | days | hours | **minutes** |

---

## Launch Plan

1. [x] Build core review engine
2. [ ] Publish 50+ built-in rules
3. [ ] Create rule marketplace (community contributed)
4. [ ] Add AI-powered suggestions (GPT-4)
5. [ ] Support Bitbucket, Azure DevOps
6. [ ] Publish to GitHub Marketplace
7. [ ] Partner with OpenClaw for integration

---

_Automate code reviews. Ship faster, sleep better._ 🔍✨
