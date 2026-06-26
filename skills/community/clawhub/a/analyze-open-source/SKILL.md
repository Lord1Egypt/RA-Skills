---
name: analyze-open-source
description: Analyze and explain open-source project code logic, architecture, data flows, APIs, and algorithms. Use when the user asks to analyze a project, understand codebase structure, explain code logic, or requests a technical walkthrough of an open-source repository.
---

# Analyze Open-Source Project

Systematically analyze an open-source project's codebase to help the user quickly understand its architecture, core logic, data flows, key APIs, and algorithm implementations.

All analysis output MUST be in Chinese (zh-CN).

## Execution Workflow

Follow these steps strictly in order. Use parallel subagents (Task tool with subagent_type="explore") where noted.

### Phase 1: Context Gathering

Read these files first (use parallel reads):

1. `README.md` (or `README.rst`, `README.txt`) — project purpose, features, quick start
2. Primary config/dependency file — detect tech stack:
   - Node.js: `package.json`
   - Python: `pyproject.toml` > `setup.py` > `requirements.txt`
   - Go: `go.mod`
   - Java/Kotlin: `pom.xml` or `build.gradle`
   - Rust: `Cargo.toml`
   - C/C++: `CMakeLists.txt` or `Makefile`
   - .NET: `*.csproj` or `*.sln`
3. CI/Docker files if present (`Dockerfile`, `.github/workflows/`) — reveals build & deploy info

Summarize: project name, purpose, tech stack, major dependencies, and build/run commands.

### Phase 2: Directory Structure Scan

Run a directory listing (depth 2) to map out the project layout.

Classify each top-level directory into one of:
- **core**: main business logic
- **api**: HTTP/gRPC/CLI interface layer
- **model/entity**: data models or domain objects
- **config**: configuration and environment
- **util/common**: shared utilities
- **test**: test suites
- **docs**: documentation
- **scripts/tools**: build or deployment scripts
- **other**: anything else

### Phase 3: Entry Point Identification

Search for program entry points based on the detected tech stack:

| Tech Stack | Typical Entry Points |
|---|---|
| Node.js | `package.json` "main"/"scripts.start", `index.js`, `src/index.ts`, `app.js` |
| Python | `__main__.py`, `main.py`, `app.py`, `manage.py`, `cli.py` |
| Go | `main.go`, `cmd/*/main.go` |
| Java | classes with `public static void main`, `@SpringBootApplication` |
| Rust | `src/main.rs`, `src/lib.rs` |
| C/C++ | `main.c`, `main.cpp` |
| Web Frontend | `src/index.tsx`, `src/main.ts`, `src/App.vue` |

Read the entry point file(s) and trace the initialization/bootstrap sequence.

### Phase 4: Deep Analysis

Perform all four dimensions of analysis. Use parallel explore subagents for independent dimensions.

#### 4a. Architecture & Module Dependencies

- Identify the architectural pattern (MVC, Clean Architecture, Hexagonal, Microservices, Monolith, etc.)
- Map module dependencies — which modules import/call which
- Produce a **Mermaid graph** showing module relationships

#### 4b. Core Business Flow & Data Flow

- Trace the primary user-facing workflow(s) end-to-end
- Identify how data enters, transforms, persists, and exits the system
- Produce a **Mermaid flowchart** or **sequence diagram** for the most important flow

#### 4c. Key API Interfaces & Call Chains

- List public API endpoints or exported interfaces
- For the top 3-5 most important APIs, trace the call chain from handler to data layer
- Note middleware, interceptors, or decorators in the chain

#### 4d. Algorithm & Function Implementation

- Identify non-trivial algorithms or complex business logic
- Extract the key code snippets (keep concise, max ~30 lines each)
- Annotate each snippet explaining the logic step by step

## Output Format

Use the template defined in [template.md](template.md) to structure the final report.

Key formatting rules:
- Use Markdown headings (`##`, `###`) for clear hierarchy
- Include at least **2 Mermaid diagrams** (architecture graph + primary flow)
- Code snippets use CODE REFERENCE format (`startLine:endLine:filepath`) when citing existing code
- Keep the entire report readable in under 15 minutes

## Guidelines

- **Depth over breadth**: It is better to deeply explain 3 critical modules than to shallowly list 20.
- **Follow the data**: When in doubt about what to analyze next, follow the data flow.
- **Cite code**: Always reference specific files and line numbers — never make vague claims.
- **Be opinionated**: State clearly what the architectural strengths and weaknesses are.
- **Progressive disclosure**: Start with executive summary; put detailed analysis in later sections. The user should get 80% of the value from the first 20% of the report.
