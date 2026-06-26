# 🛠️ CXM (ContextMachine) - CLI Reference

This document provides a comprehensive overview of all available commands and parameters for the CXM CLI.

## 🌍 Global Parameters
These parameters can be used with any command and must be placed **before** the subcommand.

| Parameter | Alias | Description |
|:---|:---|:---|
| `--project` | `-p` | Use a specific project workspace (stored in `~/.cxm/[name]`). |
| `--github` | `-g` | Use a GitHub repository URL as the workspace. Automatically clones/updates and indexes. |

---

## 💬 Commands

### 1. `cxm ask`
The primary command to generate an AI-optimized RAG prompt.

**Syntax:**
```bash
cxm ask "Your request here" [--no-index]
```

**What it does:**
1. **Auto-Indexing:** Unless `--no-index` is used, it performs a quick incremental scan of your current directory to ensure the "Repo Intelligence" is up-to-date.
2. **Context Gathering:** Automatically pulls Git status, recent file edits, and session history from **Gemini CLI** and **Claude Code CLI**.
3. **Intent Analysis:** Detects if you are fixing a bug, optimizing code, or generating features.
4. **Interactive Refinement:** Asks clarifying questions if the prompt is too vague.
5. **RAG Injection:** Finds and injects the most relevant code snippets from your local index.
6. **Clipboard:** Automatically copies the final enhanced prompt to your clipboard.

**Parameters:**
*   `--no-index`: Skips the automatic incremental indexing (useful for very large repositories where you know no code has changed).

---

### 2. `cxm index`
Manually index a directory to build or update the knowledge base.

**Syntax:**
```bash
cxm index [directory] [--recursive]
```

**Parameters:**
*   `directory`: The folder to index (defaults to `.`).
*   `--recursive`: Recursively scan subdirectories (enabled by default).

---

### 3. `cxm search`
Perform a semantic search against your indexed code without creating a prompt.

**Syntax:**
```bash
cxm search "Search query" [--limit N]
```

**Parameters:**
*   `--limit`: Number of results to show (defaults to 5).

---

### 4. `cxm harvest`
Non-interactive, highly optimized context extraction designed for autonomous AI agents and "Agentic Workflows".

**Syntax:**
```bash
cxm harvest "Search keywords" [--intent "specific intent"] [--limit N]
```

**What it does:**
1. **Silent Retrieval:** Performs RAG search without any interactive prompts or gap checks.
2. **Token Efficiency:** Uses a strict "Token Diet" by prioritizing specific code chunks over full files, compressing whitespace, and enforcing a hard global character limit (12,000 chars) to prevent context window overflow.
3. **Agent-Ready Output:** Prints results directly to `stdout` wrapped in clean XML tags (`<file_context path="...">`) for immediate ingestion by downstream agents.

**Parameters:**
*   `--intent`: Manually override the ML-based intent analysis (e.g., `add_feature`, `fix_bug`).
*   `--limit`: Maximum number of RAG chunks to process (defaults to 5).
*   `--no-index`: Skip incremental indexing before harvesting.

---

### 5. `cxm ctx`
Debug tool to see exactly what "Partner" knows about your current environment.

**Syntax:**
```bash
cxm ctx
```
**Output includes:**
*   Current Git Branch & Status.
*   Active Gemini/Claude CLI session snippets.
*   Recently edited files and system load.

---

## 📂 Data Locations
*   **Global Config:** `~/.cxm/config.yaml`
*   **Workspaces (Index):** `~/.cxm/[project_name]/knowledge-base/`
*   **GitHub Cache:** `~/.cxm/cache/`
*   **Last Generated Prompt:** `~/.cxm/sessions/ask/latest_prompt.txt`

---

## 🤖 Integrated AI CLIs
CXM automatically detects and integrates context from:
*   **Gemini CLI:** Reads from `~/.gemini/tmp/partner/chats/`
*   **Claude Code CLI:** Reads from `~/.claude/projects/` (Session history from `.jsonl` files)
