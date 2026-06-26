# Class Seven - Tool Integration Guide

## Native Tools (sessions_spawn)

### When to Use Native
- Deterministic tasks with clear success criteria
- File operations, shell commands
- Tasks not requiring deep reasoning
- Quick, low-cost operations

### Spawning Agents
```python
# Basic spawn
result = sessions_spawn(
    task="Implement user authentication",
    label="developer-auth"
)

# With specific model
result = sessions_spawn(
    task="Design database schema",
    model="anthropic/claude-sonnet-4-5",
    label="architect-db"
)

# With timeout
result = sessions_spawn(
    task="Debug memory leak",
    runTimeoutSeconds=600,
    label="debugger-memory"
)
```

## Claude Code Integration

### When to Use Claude Code
- Complex architecture decisions
- Multi-file refactoring
- Deep debugging requiring context analysis
- Tasks requiring high reasoning depth

### Calling Claude Code
```powershell
# Analysis mode
claude -p "Analyze this codebase for security vulnerabilities"

# Interactive mode (for complex tasks)
claude
# Then use natural language within Claude Code
```

### Claude Code Agent Role
```
Role: Senior Engineer / Architect
Strengths: Context management, complex reasoning, large codebases
Use for: Architecture, complex debugging, refactoring
Cost: Higher (but worth it for complex tasks)
```

## Kimi Integration

### When to Use Kimi
- Rapid prototyping
- Chinese language context
- Pattern matching tasks
- Code review and best practices
- Lower latency requirements

### Calling Kimi
```powershell
# Direct CLI
kimi "Generate a Python FastAPI CRUD scaffold"

# With file context
kimi "Review this code" --file ./src/main.py

# Interactive
kimi
```

### Kimi Agent Role
```
Role: Full-stack Developer
Strengths: Fast iteration, bilingual, good for MVPs
Use for: Quick implementation, prototyping, documentation
Cost: Efficient for most tasks
```

## Tool Selection Decision Tree

```
Is task well-defined and deterministic?
├── YES → Use Native
└── NO → Requires reasoning
    ├── Complex architecture/design?
    │   ├── YES → Use Claude Code
    │   └── NO → Continue
    ├── Multi-file analysis needed?
    │   ├── YES → Use Claude Code
    │   └── NO → Continue
    ├── Chinese context preferred?
    │   ├── YES → Use Kimi
    │   └── NO → Continue
    ├── Quick prototype/MVP?
    │   ├── YES → Use Kimi
    │   └── NO → Continue
    └── Default → Use Kimi (cost-effective)
```

## Cost-Effectiveness Matrix

| Task Complexity | Recommended Tool | Est. Token Cost | Time |
|-----------------|------------------|-----------------|------|
| Simple script | Native | Low | Fast |
| CRUD API | Kimi | Medium | Fast |
| Microservice | Kimi/Claude | Medium-High | Medium |
| System design | Claude Code | High | Medium |
| Complex debugging | Claude Code | High | Slow |
| Refactoring | Claude Code | High | Medium |
| Documentation | Kimi | Low-Medium | Fast |
| Test generation | Native/Kimi | Low-Medium | Fast |

## Hybrid Workflows

### Example: Full Feature Development

```
Phase 1: Requirements (Kimi - fast, bilingual)
  ↓
Phase 2: Architecture (Claude Code - deep reasoning)
  ↓
Phase 3: Implementation (Kimi - fast iteration)
  ↓
Phase 4: Testing (Native - deterministic)
  ↓
Phase 5: Debugging (Claude Code if complex, else Kimi)
```

### Example: Bug Fix

```
Phase 1: Triage (Kimi - quick assessment)
  ↓
  ├── Simple bug → Kimi fixes directly
  └── Complex bug → Claude Code deep analysis
                        ↓
                   Kimi implements fix
                        ↓
                   Native runs tests
```

## Environment Setup

### Required Tools
```powershell
# Claude Code
irm https://claude.ai/install.ps1 | iex

# Kimi CLI
irm https://code.kimi.com/install.ps1 | iex
```

### Configuration
Both tools should be configured for Windows/PowerShell:

```json
// ~/.claude/settings.json
{
  "systemPrompt": "Use Windows PowerShell commands. Never use: &&, grep, curl, cat, rm -rf, mkdir -p"
}

// ~/.kimi/config.toml
system_prompt = "Use Windows PowerShell commands. Avoid: &&, grep, curl, cat, rm -rf, mkdir -p"
```

## Monitoring & Logging

Track tool usage for optimization:
```json
{
  "session_id": "<id>",
  "agents": [
    {"role": "PM", "tool": "Kimi", "tokens": 1500, "duration": 30},
    {"role": "Developer", "tool": "Claude", "tokens": 8000, "duration": 120}
  ],
  "total_cost": "$0.45",
  "success": true
}
```
