---
name: ai-dev-runtime
description: AI Dev Runtime tools - read_file, search, edit, run_terminal, run_tests (hybrid semantic+keyword search, learning memory)
command-tool: ai_dev_runtime_command
command-dispatch: tool
metadata:
  {
    "openclaw": {
      "emoji": "🛠️",
      "homepage": "https://github.com/your-org/AiDevRuntime"
    }
  }
---

Use these tools to interact with AI Dev Runtime:

- **ai_dev_runtime_command**: Slash command — `/ai-dev-runtime <task>` runs full dev task (plan → edit → test → fix)
- **ai_dev_runtime_invoke**: Low-level tool calls — read_file, search, edit, edit_multi, apply_patch, find_references, call_hierarchy, run_terminal, run_tests
- **ai_dev_runtime_run_task**: Batch task execution (multi-step coding)
- **ai_dev_runtime_fix_bug**: Bug-fix workflow (analyze → patch → verify)
- **ai_dev_runtime_analyze**: Codebase analysis (semantic + keyword search, learning memory)

**For higher accuracy**: Before calling ai_dev_runtime_fix_bug or ai_dev_runtime_run_task, use memory_search to find similar past fixes (e.g. "login bug", "500 error", "pytest"). Pass the snippets as prior_memory so Runtime can use them.

Set AI_DEV_RUNTIME_URL (default http://localhost:8000) and optionally AI_DEV_RUNTIME_API_KEY. Ensure AiDevRuntime HTTP server is running.
