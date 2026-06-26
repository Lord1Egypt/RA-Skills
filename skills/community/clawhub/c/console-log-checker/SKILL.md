# console-log-checker

## Description
检查项目中是否存在 console.log 语句，帮助开发者清理调试代码。

## When to Use
Use this skill when a user wants to:
- Check for forgotten console.log statements before commit/deploy
- Audit codebase for debugging statements
- Clean up leftover console.log calls

## Inputs

- path (string, optional)
  The directory path to check. Defaults to current working directory.

- exclude (string, optional)
  Comma-separated glob patterns to exclude (e.g., "node_modules,dist,build").

## Behavior

You are a code quality assistant.

When invoked:

1. Use Grep tool to search for `console\.log` patterns in the codebase.
2. Exclude common directories like node_modules, dist, build by default.
3. Report findings in a structured format.

## Output Format

Return a summary with:

### Console.log Check Results

| File | Line | Content Preview |
|------|------|-----------------|
| path/to/file.js | 42 | console.log("debug...") |

**Total found:** X occurrences

## Recommendations
- Suggest removing or replacing with proper logging
- Flag any in production-critical files