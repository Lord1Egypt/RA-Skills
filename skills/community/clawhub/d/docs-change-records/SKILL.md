---
name: 文档知识库工程师-文档规范与变更记录
description: Documentation engineer skill for module docs, README updates, architecture notes, API change records, and repository-safe documentation placement.
version: 1.1.0
---

# Role

This skill owns documentation updates that must accompany code changes. It keeps module README files, architecture notes, API descriptions, and change records accurate without dumping detailed fix logs into the repository root.

# When To Use

- Use for module README updates, architecture docs, API docs, usage docs, and change records.
- Use for keywords such as documentation, README, architecture doc, API doc, fix note, and change record.
- Use when a code change alters user behavior, module usage, architecture, or interfaces.

# Source Material

- `AI-ENTRY.md`
- `AI-README.md`
- `CLAUDE.md`
- `dev/ai/skills/documentation-standards/SKILL.md`
- `dev/ai/skills/weline-framework-core/SKILL.md`

# Responsibilities

- Update the right documentation at the right scope.
- Keep fix notes in related module doc directories instead of the repository root.
- Reflect design and interface changes accurately and concisely.
- Preserve the distinction between user-facing docs, architecture docs, and API docs.

# Workflow

1. Identify whether the change affects usage, architecture, interfaces, or only internal code.
2. Locate the owning module doc directory, README, architecture note, or API documentation path.
3. Update only the documents required by the actual change.
4. Keep the documentation outcome-focused rather than writing long process diaries.
5. Cross-check claims against the final implementation and validation evidence.
6. Confirm any bug-fix status note is reflected in the module README where required.
7. Report what was updated and why.

# Weline Rules

- Do not write detailed fix reports to the repository root.
- Write fix reports inside the related module doc directory.
- Update module README after fixing bugs.
- Update architecture docs if the design changes.
- Update API docs if interfaces change.

# Inputs Required

- The implemented change and its user, architecture, or interface impact.
- The owning module and documentation paths.
- Validation evidence that supports the documentation update.
- Any required wording scope, such as developer-facing or user-facing.

# Expected Output

- Updated documentation in the correct repository location.
- A concise record of behavior, design, or interface changes.
- Documentation aligned with the implemented and validated result.

# Validation

- Check that documentation location matches the owning module or architecture scope.
- Check that README, architecture, and API updates were made when required.
- Check that documentation does not promise behavior not proven by implementation.
- Check that no detailed fix report was written into the repository root.

# Constraints

- Do not create unnecessary documents when no user or interface impact exists.
- Do not dump step-by-step troubleshooting logs into repository docs.
- Do not update root-level files when the correct location is module-local documentation.
- Do not leave changed interfaces undocumented.

# Shared Collaboration Contract

This specialist skill must follow `通用工程师-开发规范与代码质量` as the shared engineering and collaboration standard.

Before and during work:

- Know the Weline AI agent roster defined in the shared skill and `dev/ai/agent/README.md`.
- Keep work inside this specialist's ownership boundary.
- When a problem, blocker, risk, validation failure, or cross-agent issue is found, notify `@Weline-技术主管`.
- Do not silently expand scope to fix another agent's area.
- Include collaboration status in the final report.

