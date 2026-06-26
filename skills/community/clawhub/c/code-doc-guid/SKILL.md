---
name: code-doc-guid
description: "Codebase navigation and documentation assistant. Helps AI locate code definitions, understand dependencies, and maintain documentation consistency. BLOCKING REQUIREMENT: Use this skill BEFORE any file modification/move/delete operation to check dependencies, and AFTER modifications to update the index."
---

# Code Documentation & Navigation Guide

This skill provides a **Codebase Knowledge Graph** to help you navigate complex projects without reading thousands of files. It uses a local SQLite database to store file relationships, dependency layers, and symbol definitions.

## ⚠️ CRITICAL: BLOCKING REQUIREMENTS (触发条件)

**STOP! READ THIS BEFORE PROCEEDING.**

You **MUST** invoke this skill (`code-doc-guid`) as a **BLOCKING STEP** before performing any of the following actions. Failure to do so is a violation of protocol.

### 🔴 Mandatory Pre-Action Check (Recon Phase)
**Trigger**: You are about to:
*   Modify any code file (`Write`, `SearchReplace`).
*   Rename or move files (`RunCommand: mv/ren`).
*   Delete files (`DeleteFile`).
*   Refactor a class, function, or variable.

**Action**: You MUST run `python ... codebase_manager.py inspect/search` FIRST.
**Reason**: You cannot safely modify code without knowing who depends on it. "Guessing" is strictly prohibited.

### 🟢 Mandatory Post-Action Sync (Archive Phase)
**Trigger**: You have just finished a set of file modifications.
**Action**: You MUST run `python ... codebase_manager.py update`.
**Reason**: The knowledge graph must remain consistent with the disk state for the next turn.

---

## Workflow & Commands

All commands are run via `python scripts/codebase_manager.py <command> [args]`.
*(Note: If running manually, adjust the path to where you saved the script)*

### 1. `search` - Find Symbols & Concepts
Use this to locate code by name or intent (docstring).

*   **Command**: `search <query>`
*   **Example**: `search "UserAuth"`
*   **Output**: JSONL format containing file paths, symbol names, and docstrings.
*   **Action**: Use this to find the *exact file path* before reading it.

### 2. `inspect` - Analyze Dependencies & Risk
Use this to understand the impact of a change.

*   **Command**: `inspect <filename_fragment>`
*   **Example**: `inspect "auth_service"`
*   **Output (JSON)**:
    *   `risk_score`: **HIGH** / **MEDIUM** / **LOW**.
    *   `doc_file`: Path to the detailed report (e.g., `.trae/codeguiddoc.md`).
*   **Action Guidelines**:
    1.  **Read the JSON summary** first.
    2.  **IF RISK IS HIGH**:
        *   **STOP**. Do not modify code yet.
        *   **READ** the generated markdown file (`doc_file`). It contains a **Mermaid Graph** and full dependency list.
        *   **SHOW** the Mermaid graph to the user (if possible) or summarize the impact: "This change affects 25 files, including core modules A and B."
        *   **ASK** for confirmation.

### 3. `update` - Refresh Index
Use this after **ANY** file modification.

*   **Command**: `update`
*   **Output**: "Processing X changed files..."
*   **Note**: It is incremental and very fast (<1s usually). Always run this before finishing your turn.

### 4. `graph` - Export Visuals (Optional)
Use this only when the user explicitly asks for an architecture overview.

*   **Command**: `graph`
*   **Output**: Generates `.trae/architecture_layers.md` (Human readable) and `.trae/dependency_graph.json` (Machine readable).

## Token Economy Strategy

To save tokens and time:
1.  **Don't read whole files** to find one function. Use `search` -> `Read(limit=20, offset=N)`.
2.  **Don't guess dependencies**. Use `inspect` to see the exact relationship graph.
3.  **Trust the Layering**. If you are modifying a **Layer 0** file, be extremely careful—it breaks everything. If modifying **Layer 5**, it's likely safe.
