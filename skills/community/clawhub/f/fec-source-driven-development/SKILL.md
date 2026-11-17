---
name: fec-source-driven-development
description: Use when frontend decisions depend on framework, library, browser, runtime, package, API, or platform behavior that may have changed, including official documentation checks, version-sensitive patterns, migration choices, or public interface assumptions; Chinese triggers include Check official documentation, source code shall prevail, source-driven, version differences.
---

# Source driven development

## Purpose

Prioritize the use of in-project facts, official documentation, and current version behavior in front-end implementation, review, and architecture decisions, and avoid relying on outdated experience or unverified assumptions.

## Procedure

1. Determine whether it is necessary to check the source
   - Source checking is required when new versions of frameworks, routing, rendering modes, caches, build tools, browser APIs, package publishing formats, authentication protocols, or public interfaces are involved.
   - When it comes to project commitments, read the README, configuration, templates, existing implementations, testing and migration records of this warehouse first.
   - Use the project's existing schema as a source of truth when simply stabilizing the language syntax or significantly partial refactoring.

2. Collect authoritative materials
   - Preferred official documentation, specifications, source code, release notes, migration guide, type definitions and in-project testing.
   - Third-party articles can only be used as clues and cannot be used as the final basis.
   - Record package name, version, document date or page title for rapidly changing libraries.
   - When a user asks to answer a question from a local knowledge base, project repository or `knowledge/` directory, perform local knowledge retrieval first and do not use network search to fill in the facts.

3. Refine decisions
   - Write down recommended practices, deprecated practices, limitations and migration considerations for the current version.
   - Explain the reasons for selection, compatibility, maintenance costs and fallback methods for multiple feasible options.
   - If there is a conflict between the document and the current status of the project, priority will be given to explaining the conflict and making incremental adjustments instead of directly overturning the running system.
   - Record release notes, migration guide, version scope, breaking changes and rollback plans for dependency upgrades, framework migrations and public API changes.

4. Fall to implementation
- Isolate external behavior in the adaptation layer, configuration layer or small utility functions to avoid spreading version assumptions throughout the component.
   - Public interface changes should keep naming, error shapes, default values, and compatibility policies clear.
   - Code comments only record non-obvious source constraints and do not paste large sections of documentation.

5. Test your hypothesis
   - Prove key assumptions with type checking, minimal reproduction, unit testing, component testing, E2E, build or browser validation.
   - If verification is not possible, report uncertainty, risk range, and information that requires confirmation by the user or team.
6. Leave a lightweight record of decisions
   - Supplement ADR/change records or hand off to the document sync process when conclusions impact public interfaces, dependency versions, catalog specifications or team workflows.

## Local Knowledge Retrieval

When the user specifies the local knowledge base path, or the default `knowledge/` directory exists, this process can be used to answer database questions, extract evidence, or assist decision-making.

1. Locate the root directory
   - Use this path when the user explicitly specifies the path.
   - Otherwise, check whether `knowledge/` under the current project exists; if it does not exist, it means that the default knowledge base is not found and the path is requested.
   - No need to use file glob to determine whether the directory exists.

2. Hierarchical navigation
   - Read `data_structure.md` in the root directory and subdirectories first.
   - Select the most relevant few branches according to the directory description, without traversing the entire knowledge base at once.
   - Document candidate files, topics, time/version range and why they are relevant.

3. Progressive search
   - Markdown, text, log: first search with keywords, and then partially read the hit context.
   - PDF: Confirm the available tools and extraction routes before processing, and prioritize extraction of temporary text before retrieval to avoid putting the entire PDF into context.
   - Excel: Confirm the read/analysis route before processing, first look at the worksheet, column names and a few samples, and then filter or aggregate by field.
   - Default to up to 5 rounds of keyword iteration; each round adjusts synonyms, abbreviations, and scope based on found evidence.

4. Answer and traceability
   - Give the conclusion first, and then list the file path, chapter, page number, worksheet or line number as a basis.
   - If there is insufficient evidence, explain which paths have been checked, what information is missing, and how the user can narrow down the scope.
   - Do not mix online information from outside the knowledge base into answers unless the user requests otherwise to check external sources.

## Source Priority

| Priority | Source | Use |
| -------- | ------ | --- |
| 1 | Configuration, testing, and implementation within the project | Determine the true agreement of this warehouse |
| 2 | Official documents, source code, type definitions | Determine current recommended behavior |
| 3 | Standard specifications, browser compatibility data | Determine platform capabilities and compatibility boundaries |
| 4 | Issues, discussions, third-party articles | Auxiliary investigation, cannot be finalized alone |

## Constraints

- Don't give version-sensitive conclusions from memory.
- Do not treat outdated tutorials as current best practices.
- Do not cite sources that cannot be reviewed as critical evidence.
- Do not change the stable project agreement to pursue new developments; the benefits and migration costs must be explained.
- Do not copy long external documents in the delivery; keep only necessary conclusions and links or file paths.
- Don't just say "checked the documentation"; version-sensitive decisions need to be traceable to a specific version, path or official page.

## Expected Output

Output source lists, version or project facts, decision conclusions, implementation impacts, validation orders, and open risks. If code is modified, key behaviors should be supported by tests or build verification.
