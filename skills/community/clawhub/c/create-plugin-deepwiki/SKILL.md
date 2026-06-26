---
name: create-plugin
description: Create minimal, convention-matching plugins or extensions for an existing codebase. Use when the user asks for a plugin, extension, custom module, integration, or add-on for an open-source/project repository and wants the work to stay simple, readable, and aligned with the host project's structure and style.
---

# Create Plugin

Build the smallest plugin that solves the requested problem while fitting the host codebase.

## Workflow

1. Learn the codebase before designing anything.
	- Read the GitHub repository first.
	- Read official docs linked from the repository, especially installation, API, examples, and contribution/style guidance.
	- If the `deepwiki` skill is installed, use DeepWiki MCP for public-repo source-code queries before guessing.
	- Use DeepWiki MCP for three things in particular:
		- `structure` to map the documentation/wiki layout,
		- `contents` to read relevant topic pages,
		- `ask` to query extension points, module organization, APIs, naming patterns, and built-in examples to copy.
	- Ask questions that are concrete and code-oriented, for example:
		- "What are the main extension points for adding a new plugin/module?"
		- "Which built-in modules are the smallest and best examples to study first?"
		- "How is the package organized, and where should a minimal extension live?"

2. Learn the modular structure.
	- Identify the extension points, package layout, naming conventions, imports, base classes, and how existing modules are organized.
	- Use DeepWiki MCP source-code queries to accelerate this discovery when the repo is public.
	- Inspect one or two similar built-in modules or extensions and mirror their shape.

3. Make a short plan before coding.
	- State the minimal implementation approach.
	- Prefer the smallest API and fewest files that still feel native to the project.
	- Call out any deliberate simplifications.

4. Implement the plugin.
	- Match the host project's conventions first: formatting, file layout, typing style, docstrings, imports, naming, and dependency choices.
	- Prefer readability over novelty.
	- Avoid adding dependencies unless clearly justified.
	- Do not modify upstream/vendor code unless the user explicitly asks for an in-tree patch.

5. Check convention fit.
	- Verify that names, module boundaries, and public API feel consistent with the host codebase.
	- If the environment is difficult, it is acceptable to skip full runtime testing, but still do lightweight checks that are feasible, such as syntax checks, lint-style review, or import-path review.
	- Be explicit about what was and was not verified.

6. Document the plugin.
	- Add minimal usage documentation.
	- Explain the core API, state/inputs/outputs if relevant, and the main simplifying assumptions.
	- Keep documentation proportionate to the plugin size.

## Design Rules

- Start from existing examples in the host repo before inventing structure.
- Keep the extension minimal and easy to read.
- Prefer a narrow, obvious API.
- Follow the host project's patterns more than generic best practices when the two differ.
- When uncertain, choose the simpler design and note the limitation.
- Do not promise physical/functional fidelity beyond what the implementation actually does.

## Output Checklist

Before finishing, confirm all of the following:
- the repository and docs were reviewed first
- the modular structure was inspected
- a plan was made before implementation
- the plugin is minimal and readable
- the code follows host-project conventions as closely as practical
- documentation was added
- verification scope is stated honestly

## References

- For a worked example based on CAX, read `references/cax-recrystallization-example.md`.
- Only read the reference when the current task is similar or when you want an example of how to apply this workflow to a scientific/plugin-style extension.
- If the `deepwiki` skill is available, read its SKILL and use its `ask`, `structure`, and `contents` commands for public GitHub repositories during the repo-learning phase.
