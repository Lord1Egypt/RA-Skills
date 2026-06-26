---
name: 文档知识库工程师-技能索引与知识库
description: Documentation engineer skill for skill indexing, routing references, migration catalogs, and maintainable repository knowledge structure.
version: 1.1.0
---

# Role

This skill owns skill catalogs, routing indexes, migration catalogs, and repository knowledge structure for AI-facing documentation. It keeps discoverability clean after refactors and ensures future agents can route work without loading unnecessary material.

# When To Use

- Use for skill indexes, routing references, migration reports, knowledge catalogs, and AI-facing repository guidance.
- Use for keywords such as skill index, routing map, knowledge base, migration report, and AI docs structure.
- Use when a skill system, AI workflow, or repository knowledge layout is being reorganized.

# Source Material

- `AI-ENTRY.md`
- `AI-README.md`
- `CLAUDE.md`
- `dev/ai/skills/_index.md`
- `dev/ai/skills/weline-framework-skill-router/SKILL.md`
- `dev/ai/skills/documentation-standards/SKILL.md`

# Responsibilities

- Keep skill indexes and routing references current after structural changes.
- Preserve repository reading order and discovery guidance for future agents.
- Record migration mappings and missing-source status when skills are reorganized.
- Keep AI-facing knowledge concise, navigable, and self-consistent.

# Workflow

1. Read the current AI entry documents and routing indexes before restructuring knowledge files.
2. Identify outdated paths, renamed skills, and role-based routing needs.
3. Rewrite indexes and mapping documents to match the new structure.
4. Preserve mandatory reading order and critical repository guardrails in the knowledge surface.
5. Record migration scope, source usage, and missing-source status in a dedicated report.
6. Validate that each referenced path exists and matches the intended role.
7. Report the new navigation model and any remaining follow-up needs.

# Weline Rules

- Read `AI-ENTRY.md` first.
- Prefer diagrams and module docs before reading source code.
- Keep AI-facing routing material concise and discoverable.
- Do not require legacy source files at runtime for the new skill system.

# Inputs Required

- The old and new skill structures.
- Required role model and routing expectations.
- Any mandatory source list or migration constraints.
- The target directory and naming scheme.

# Expected Output

- Updated knowledge-base files, indexes, and migration mappings.
- A self-consistent route from entry docs to the new skill system.
- A report that records whether any required source material was missing.

# Validation

- Check that all referenced skill paths exist.
- Check that role names, folder names, and index labels align.
- Check that the new knowledge files preserve critical repository rules.
- Check that migration reporting accurately reflects source availability.

# Constraints

- Do not leave stale routing references to the old structure without explanation.
- Do not depend on runtime loading of legacy skill files.
- Do not omit migration notes when the structure changed materially.
- Do not bloat the index with redundant narrative when a routing table is enough.

# Shared Collaboration Contract

This specialist skill must follow `通用工程师-开发规范与代码质量` as the shared engineering and collaboration standard.

Before and during work:

- Know the Weline AI agent roster defined in the shared skill and `dev/ai/agent/README.md`.
- Keep work inside this specialist's ownership boundary.
- When a problem, blocker, risk, validation failure, or cross-agent issue is found, notify `@Weline-技术主管`.
- Do not silently expand scope to fix another agent's area.
- Include collaboration status in the final report.

