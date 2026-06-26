---
name: cxm-neural-memory
description: Use this skill when you need to understand the architecture of a codebase, perform semantic searches across files, map dependencies before refactoring, or ingest non-code documentation into your context memory. It leverages the CXM (ContextMachine) tool to prevent context collapse.
---

# CXM Neural Memory Skill

This skill provides you with a localized "Neural Memory" and architectural mapping tool. It allows you to find code semantically and map dependencies using bundled AST-parsing tools.

## 🔒 Security & Transparency (Disclosure)

To ensure safe and transparent operation, be aware of the following behaviors:
- **Local Indexing:** This skill performs recursive file reads within the project to build a local vector index (FAISS) stored in `~/.cxm`.
- **Resource Footprint:** Initial indexing is CPU-intensive. Runtime RAM usage ranges from ~300MB (Mini-BERT) to ~1GB (MPNet).
- **Network Access:** On the very first execution, this skill will download a pre-trained model (~80MB to ~400MB) from the HuggingFace Hub. No project data is ever uploaded.
- **File Modification:** The tool can patch files. It strictly respects the `allowed_write_paths` and `mode` (e.g., `ask_first`) defined in the project's `.cxm.yaml`.

## 🛠️ Local Engine Usage

You are already bundled with the CXM source code. All commands must be executed via the local `src/cli.py` script.

**Crucial Instruction:** Always use the `--agent-mode` flag to receive strict, parseable JSON.

## Core Capabilities & Usage

### 1. Semantic Search (Vibe Searching)

Use this when you need to find logic by its purpose, even if you don't know the exact file name or variable names.

**Command:**
```bash
python src/cli.py --agent-mode harvest --semantic "your natural language query"
```

**Interpretation:** 
The JSON output contains a `results` array with `path`, `content`, and `start_line`/`end_line` for precise targeting.

### 2. Dependency Graphing (Architectural Mapping)

Use this before refactoring to see which files or modules depend on your target file.

**Command:**
```bash
python src/cli.py --agent-mode map path/to/file.py
```

**Interpretation:**
The JSON output includes an `edges` list and a `hotspots` array showing the most heavily used modules in the project.

### 3. Architecture Ingestion

Force CXM to index non-code files like `README.md`, `docker-compose.yml`, or `package.json` to understand the system's infrastructure.

**Command:**
```bash
python src/cli.py --agent-mode ingest .
```

## Workflow for Complex Refactoring

1. **Locate:** Use `semantic search` to find the relevant code sections.
2. **Map:** Run `map` on the identified files to see the blast radius.
3. **Execute:** Apply your changes knowing the full architectural context.
