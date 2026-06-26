# Browser Snapshot System

## Overview

OpenClaw's browser snapshot system provides two main approaches for capturing and interacting with web page content:

1. **AI Snapshots** (default) - Uses Playwright's aria-ref system with numeric references
2. **Role Snapshots** - Uses semantic role-based references with interactive elements

## AI Snapshots (Numeric References)

### Usage
```bash
openclaw browser --browser-profile openclaw snapshot
# or
openclaw browser --browser-profile openclaw snapshot --format ai
```

### Output Format
- Returns text representation of the page with numeric references like `[1]`, `[2]`, etc.
- Each reference corresponds to a specific element on the page
- References are resolved internally using Playwright's aria-ref system

### Actions with AI Snapshots
```bash
# Click element with reference 12
openclaw browser --browser-profile openclaw click 12

# Type into element with reference 23
openclaw browser --browser-profile openclaw type 23 "search query" --submit
```

## Role Snapshots (Semantic References)

### Usage
```bash
# Interactive mode (recommended for automation)
openclaw browser --browser-profile openclaw snapshot --interactive

# Compact mode
openclaw browser --browser-profile openclaw snapshot --compact

# With depth limit
openclaw browser --browser-profile openclaw snapshot --interactive --depth 6

# Scoped to specific selector
openclaw browser --browser-profile openclaw snapshot --selector "#main" --interactive

# Scoped to iframe
openclaw browser --browser-profile openclaw snapshot --frame "iframe#main" --interactive
```

### Output Format
- Returns structured list/tree with semantic references like `[ref=e12]`, `[ref=b5]`, etc.
- References follow role-based naming:
  - `e` = button
  - `b` = link  
  - `i` = input
  - `s` = select
  - `t` = text
  - And more based on ARIA roles

### Actions with Role Snapshots
```bash
# Click semantic reference
openclaw browser --browser-profile openclaw click e12

# Type into input field
openclaw browser --browser-profile openclaw type i23 "search query" --submit

# Highlight element for debugging
openclaw browser --browser-profile openclaw highlight e12
```

## Reference Stability

### Important Notes
- **References are NOT stable across navigation** - Always take a new snapshot after page changes
- **Role snapshots with --frame are scoped to that iframe** until next role snapshot
- **Numeric references may change** between different page loads or dynamic content updates

### Best Practices
1. Always snapshot before performing actions
2. Use role snapshots (`--interactive`) for more reliable automation
3. When actions fail, use `highlight` to verify element location
4. For complex workflows, combine snapshots with wait conditions

## Advanced Snapshot Options

### Efficient Mode
```bash
# Compact preset for automation
openclaw browser --browser-profile openclaw snapshot --efficient
# Equivalent to: --interactive --compact --depth 6 --max-chars lower
```

### Labeled Screenshots
```bash
# Get screenshot with overlay labels
openclaw browser --browser-profile openclaw snapshot --labels
# Returns both text snapshot and MEDIA: path to labeled screenshot
```

### JSON Output
```bash
# Machine-readable output
openclaw browser --browser-profile openclaw snapshot --interactive --json
```

## Troubleshooting

### Common Issues
- **"Element not found"**: Take a new snapshot - references may have changed
- **"Not visible"**: Element might be in iframe - use `--frame` option
- **"Strict mode violation"**: Multiple elements match - use more specific selector or nth option

### Debugging Workflow
1. `snapshot --interactive` to get current state
2. `highlight <ref>` to verify target element
3. Check `errors --clear` for JavaScript errors
4. Use `requests --filter api --clear` to monitor network activity
5. For complex issues, use `trace start` → reproduce → `trace stop`

## Integration with Smart Agents

When using browser tools in agent workflows:

- **Profile selection**: Use `profile="openclaw"` for isolated browser, `profile="chrome"` for extension relay
- **Target specification**: Use `target="host"` for local, `target="node"` for remote nodes
- **Error handling**: Always validate snapshot success before proceeding with actions
- **Context awareness**: Consider using wait conditions before snapshotting dynamic content

The snapshot system is designed to provide deterministic, reliable UI automation while avoiding fragile CSS selectors that break easily with page changes.