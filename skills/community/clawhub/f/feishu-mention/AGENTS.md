# Developer Guide & Agent Rules

This document outlines the development standards, commands, and conventions for the `feishu-mention` repository. All AI agents and developers must adhere to these guidelines to maintain code quality and consistency.

## 1. Project Overview

- **Type**: Node.js package (ES Modules)
- **Purpose**: Parse and resolve Feishu/Lark @mentions in text messages.
- **Key Files**:
    - `index.js`: Main library logic and exports.
    - `test.js`: Simple test script.
    - `package.json`: Dependency and script definitions.

## 2. Build & Test Commands

Since this is a pure JavaScript project, there is no compilation step.

- **Run Tests**:
  ```bash
  npm test
  # OR
  node test.js
  ```
  *Note: The test script verifies basic functionality and API contracts.*

- **Run Examples**:
  ```bash
  npm run example
  ```

- **Linting**:
  - Currently, there is no strict linter configured.
  - Follow the existing code style (see below) rigorously.

## 3. Code Style & Conventions

### General
- **Module System**: Use ES Modules (`import`/`export`). Do NOT use CommonJS (`require`/`module.exports`).
- **Indentation**: 2 spaces.
- **Quotes**: Single quotes (`'`) preferred over double quotes.
- **Semicolons**: Always use semicolons.

### Naming
- **Variables & Functions**: `camelCase` (e.g., `resolveMention`, `cacheDir`).
- **Classes**: `PascalCase` (e.g., `FeishuMentionResolver`).
- **Constants**: `SCREAMING_SNAKE_CASE` for global configuration (e.g., `DEBUG_LOG`).
- **Private Methods**: Prefix with underscore `_` (e.g., `_getCacheFile`).

### Documentation
- Use **JSDoc** for all classes and public methods.
- Include `@param` and `@returns` descriptions.
- Comments should explain *why* complex logic exists, not just *what* it does.

```javascript
/**
 * Resolves a single mention tag.
 * @param {string} mention - The raw mention text (e.g., "@User")
 * @returns {Promise<string>} - The formatted <at> tag
 */
```

### Error Handling & Logging
- Use the internal `log` function instead of `console.log` for library output.
- Use `try...catch` blocks for all file system operations and external API calls.
- Fail gracefully: if a mention cannot be resolved, return the original text rather than throwing an error.

### File System & Paths
- Use `path.join` for all path manipulations to ensure cross-platform compatibility.
- Use `process.env.HOME` or `process.env.USERPROFILE` for resolving user directories.

## 4. Dependencies
- **Runtime**: Node.js (Standard built-in modules: `fs`, `path`, `crypto`).
- **External**: Keep external dependencies to a minimum. Currently, the project relies on standard Node.js APIs.

## 5. Development Workflow
1.  **Analyze**: Understand the requirement and existing code patterns.
2.  **Implement**: Write code in `index.js` or new modules as needed.
3.  **Verify**:
    - Run `node test.js` to ensure no regressions.
    - Create a small reproduction script if fixing a specific bug.
