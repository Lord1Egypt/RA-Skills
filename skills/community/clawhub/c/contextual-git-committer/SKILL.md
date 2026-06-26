---
name: Contextual-Git-Committer
description: AI-powered Git assistant that analyzes staged changes and terminal history to craft meaningful, conventional commit messages.
tools:
  - name: suggest_commit
    description: "Analyzes staged git changes and recent terminal history to suggest 3 possible commit messages in different styles: Conventional Commit, Story/Detailed, and Emoji. Returns structured context about the changes for the AI to generate high-quality messages."
    arguments:
      - name: style
        description: "Output preference: 'conventional' (default) for standard commit format, or 'detailed' for longer explanations with context."
        type: string
        required: false
      - name: scope
        description: "Optional module or area being updated (e.g., 'auth', 'api', 'ui'). Narrows the commit focus."
        type: string
        required: false
    execution:
      command: python3 {{SKILL_DIR}}/handler.py suggest-commit --style "{{style}}" --scope "{{scope}}"
      output_format: markdown
---

# Contextual Git-Committer

An AI-powered Git assistant that writes descriptive, high-quality commit messages by analyzing your local workspace context.

## How It Works

1. **Gathers staged changes** via `git diff --cached` to see exactly what you're about to commit.
2. **Correlates terminal history** by reading recent shell commands to understand *why* changes were made (e.g., did you just run `npm install`? `pytest`?).
3. **Checks recent commits** via `git log` to maintain consistency with your project's existing style.
4. **Parses diff hunks** to identify which functions, classes, or sections were modified.

## AI Prompt Instructions

When the `suggest_commit` tool returns its output, use the gathered context to generate exactly **3 commit message options**:

### Option 1: Conventional Commit
A short, standards-compliant message using the Conventional Commits format:
- Prefix with the correct type: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `style:`, `perf:`, `build:`, or `ci:`
- Include the scope if provided
- Keep the subject line under 72 characters
- Example: `fix(auth): resolve null pointer when session expires`

### Option 2: Story / Detailed
A narrative-style message that explains *what* the change achieves in plain English:
- Focus on the "why" and the outcome, not just the mechanics
- 1-2 sentences
- Example: "Updated the header logic to prevent crashes when a user is logged out, which was causing intermittent 500 errors on the dashboard."

### Option 3: Emoji Style
A casual, emoji-prefixed message for less formal projects:
- Use relevant emojis to convey the type of change
- Keep it concise and fun
- Example: "🐛 Fixed header crash on logout | 🛡️ Added null checks for session object"

## Output Format

Present the three options as a numbered list:

```
📝 Suggested Commit Messages:

1. **Conventional:**
   `fix(auth): resolve null pointer when session expires`

2. **Story:**
   Updated the header logic to prevent crashes when a user is logged out, which was causing intermittent 500 errors on the dashboard.

3. **Emoji:**
   🐛 Fixed header crash on logout | 🛡️ Added null checks for session object
```

If no staged changes are found, inform the user and suggest running `git add` to stage their changes first.

## Usage Examples

- `/suggest_commit` — Analyze staged changes and suggest 3 messages
- `/suggest_commit --style detailed` — Provide more verbose explanations
- `/suggest_commit --scope api` — Focus the message on the API module
- `/suggest_commit --style detailed --scope auth` — Detailed messages scoped to auth
