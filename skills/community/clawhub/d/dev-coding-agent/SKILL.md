---
name: dev-coding-agent
description: 'Enhanced coding agent for development workflows. Optimized for building features, fixing bugs, and code refactoring with OpenCode integration.'
metadata:
  {
    "openclaw": { "emoji": "👨‍💻", "requires": { "anyBins": ["opencode"] } },
    "author": "Roger",
    "version": "1.0.0"
  }
---

# Development Coding Agent

Specialized coding agent skill optimized for software development tasks using OpenCode.

## Quick Start

### Basic Usage
```bash
# Simple task in your project
bash pty:true workdir:~/your-project command:"opencode run 'Add feature or fix bug'"

# Background task for complex work
bash pty:true workdir:~/your-project background:true command:"opencode run 'Build complete feature'"
```

### Common Development Patterns

#### Bug Fixing
```bash
bash pty:true workdir:~/project command:"opencode run 'Fix the [specific issue] in [file/component]'"
```

#### Feature Development  
```bash
bash pty:true workdir:~/project command:"opencode run 'Implement [feature name] with [requirements]'"
```

#### Code Refactoring
```bash
bash pty:true workdir:~/project background:true command:"opencode run 'Refactor [module] to improve [performance/readability/maintainability]'"
```

#### Testing
```bash
bash pty:true workdir:~/project command:"opencode run 'Add unit tests for [function/module] using [testing framework]'"
```

## Best Practices

1. **Always specify the work directory** - keeps context focused
2. **Use descriptive prompts** - include file names, expected behavior, and constraints
3. **Monitor background tasks** - use `process action:log` to track progress
4. **Git required** - ensure your project is a git repository (OpenCode requirement)

## Examples

### Create React Component
```bash
bash pty:true workdir:~/my-app command:"opencode run 'Create a reusable Button component with variants (primary, secondary, danger), loading state, and TypeScript interface'"
```

### API Development
```bash
bash pty:true workdir:~/backend command:"opencode run 'Add user registration endpoint with email validation, password hashing, and JWT token generation'"
```

### Database Migration
```bash
bash pty:true workdir:~/project command:"opencode run 'Create database migration to add created_at and updated_at timestamps to all existing tables'"
```

## Requirements

- OpenCode CLI installed (`npm install -g opencode`)
- Git repository for target project
- PTY support enabled (automatic with `pty:true`)