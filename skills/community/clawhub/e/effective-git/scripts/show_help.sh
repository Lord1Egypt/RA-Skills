#!/bin/bash
# Show help and usage guide for effective-git skill

cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║              Effective Git - Usage Guide                     ║
╚══════════════════════════════════════════════════════════════╝

🚀 Quick Commands (use 'gq' prefix)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  gq b:l              List all branches
  gq b-> <name>       Switch to branch
  gq b:n <name>       Create new branch from current
  gq s                Quick status
  gq l                Recent commits
  gq d                Show changes

  Run 'gq help' for full quick commands list

📝 Full Workflow (use natural language)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  "帮我提交代码"           → Analyze changes, suggest commit strategy
  "推送到远程"             → Safe push with confirmation
  "解决冲突"               → Guided conflict resolution
  "rebase 到 main"         → Safe rebase with backup
  "查看最近的改动"         → Detailed change analysis

🛡️ Safety Features
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✓ Automatic backups before merge/rebase
  ✓ Confirmation required for dangerous operations
  ✓ Never auto-merge conflicts
  ✓ Code loss prevention checks
  ✓ Only push to current branch

🔧 Conflict Resolution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  When conflicts occur:
  1. Automatic backup created
  2. Conflicts analyzed (only conflict sections shown)
  3. Both versions presented with analysis
  4. Recommendation provided
  5. User decides final resolution

  First principle: Never lose code

📚 Documentation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  references/best-practices.md      Git best practices
  references/conflict-resolution.md Detailed conflict guide
  references/quick-commands.md      All quick commands

💡 Examples
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Quick check:
    gq s                    # What's changed?
    gq l                    # Recent commits
    gq b:l                  # List branches

  Branch workflow:
    gq b:n feature-x        # Create new branch
    [make changes]
    "帮我提交代码"           # Commit with analysis
    "推送代码"               # Safe push

  Conflict resolution:
    "rebase 到 main"        # Start rebase
    [if conflicts]
    "解决冲突"               # Get guided resolution

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For more help: Ask "show me git best practices" or "how to resolve conflicts"
EOF
