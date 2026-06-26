# Cursor Agent CLI Skill

AI-powered coding assistant for the terminal.

## Quick Start

```bash
# Interactive session
agent

# With initial prompt
agent "refactor auth module"

# Non-interactive (scripts)
agent -p "fix bugs" --output-format json
```

## Installation

```bash
# Install Cursor Agent CLI
curl https://cursor.com/install -fsS | bash

# Verify
agent --version
```

## Modes

- **Agent** (default) - Full access, can modify code
- **Plan** (`--plan`) - Read-only planning
- **Ask** (`--mode=ask`) - Q&A only

## Key Features

✅ Interactive AI coding sessions  
✅ Non-interactive mode for CI/CD  
✅ Cloud Agent (background execution)  
✅ Multi-model support (GPT-5, Sonnet-4)  
✅ Session persistence & resume  
✅ Git worktree integration  
✅ Sandbox mode for safety  

## Common Commands

```bash
agent ls                    # List sessions
agent resume                # Resume latest
agent --continue            # Continue previous
agent --list-models         # Available models
agent login                 # Authenticate
agent update                # Update CLI
```

## Use Cases

- 🔄 Code refactoring
- 🐛 Bug fixing
- ✨ Feature development
- 🔍 Code review
- 📝 Documentation
- 🧪 Test generation
- ⚡ Performance optimization
- 🚀 CI/CD integration

## Documentation

📖 Full guide: [SKILL.md](./SKILL.md)  
🌐 Official: https://cursor.com/docs/cli/overview

---

**Version**: 2026.02.27-e7d2ef6  
**License**: Proprietary (Cursor)
