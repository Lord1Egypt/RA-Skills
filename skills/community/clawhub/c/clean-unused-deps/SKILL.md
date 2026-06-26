---
name: clean-unused-deps
description: Clean up unused npm dependencies in a project. Use when you want to remove packages that are installed but not used in the codebase.
---

# Clean Unused Dependencies

This skill helps identify and remove unused npm dependencies from a project.

## Workflow

1. Identify unused dependencies using `depcheck`
2. Remove the unused dependencies with `npm uninstall`

## Prerequisites

- Node.js and npm installed
- `depcheck` installed globally (`npm install -g depcheck`)

## Instructions

1. Run `depcheck` in the project root to identify unused dependencies
2. Review the output and identify packages to remove
3. Run `npm uninstall <package-name>` for each unused package

## Example

```bash
# Check for unused dependencies
depcheck

# Remove unused package
npm uninstall unused-package-name
```

For multiple packages:
```bash
npm uninstall package1 package2 package3
```