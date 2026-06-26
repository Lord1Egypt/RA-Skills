---
name: claude-delegate
description: Delegate various coding tasks to Claude Code. Use this skill when you need assistance with code generation, bug fixing, feature implementation, code review, refactoring, or file exploration. It streamlines calling Claude Code for non-interactive execution, handling parameters like `--print --permission-mode bypassPermissions`. Triggers on phrases like 'write code for', 'fix this bug in', 'implement feature', 'review this pr', 'refactor', 'explore files for', 'debug', 'code task for claude'.
---

# Claude Delegate

Use this skill to delegate coding tasks to Claude Code. It simplifies the process by providing the correct command structure for non-interactive execution.

## Usage

To delegate a task to Claude Code, use the `exec` tool with the `bash` command, specifying the working directory and the task as a string. Claude Code will run with `--print --permission-mode bypassPermissions` automatically.

```bash
bash workdir:/path/to/project command:"claude --permission-mode bypassPermissions --print 'your coding task here'"
```

### Examples

*   **build a feature:**
    ```bash
    bash workdir:~/projects/my-app command:"claude --permission-mode bypassPermissions --print 'build a user authentication module'"
    ```

*   **refactor a module:**
    ```bash
    bash workdir:~/projects/my-lib command:"claude --permission-mode bypassPermissions --print 'refactor the data processing module for better performance'"
    ```

*   **review a pull request:**
    ```bash
    bash workdir:/tmp/pr-review command:"claude --permission-mode bypassPermissions --print 'review the changes in pull request #123 and provide feedback'"
    ```
