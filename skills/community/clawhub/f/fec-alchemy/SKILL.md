---
name: fec-alchemy
description: Use when absorbing ideas, capabilities, workflows, architecture, quality systems, ecosystem extensions, or engineering practices from any reference system into the current project through original, project-native redesign rather than copying.
---

# Integration of project absorption and originality

## Purpose

Convert excellent ideas, capabilities, and engineering practices from one or more reference systems into improvements in the current project that are original, maintainable, and consistent with the target project style.

Suitable for absorbing, borrowing, benchmarking, migrating or integrating another code base, product, framework, library, service, CLI, plug-in, documentation system, AI/Agent tool chain, architecture or engineering workflow. This Skill should not be used for general bug fixes, individual API usage issues, or direct file format conversions, unless the user explicitly requests project-level ingestion or adaptation.

## Procedure

1. Clarify goals and reference systems:
- Treat the current repository as the target system and its architecture, naming, testing, release model and maintenance boundaries as the source of truth.
- Treat external repositories, uploaded packages, documentation, examples, product descriptions or running experiences as reference systems that only provide evidence and inspiration.
- Identify the scope of absorption: product capabilities, architectural patterns, domain models, interface protocols, data flow, runtime behavior, development experience, quality system, delivery process, documentation knowledge or ecological expansion.
- When there is a lot of information, you can use [assets/intake-template.md](assets/intake-template.md) to create a brief list.
2. Establish a target project baseline:
- First read the target project README, package metadata, directory structure, configuration, existing entries, extension points, test commands and release notes.
- Find out that the target project already has similar capabilities and determine whether they should be enhanced, merged, replaced, split, documented or added.
3. Scan reference items:
- Prioritize reading README, package metadata, source code layout, project form related directories, key modules, tests, examples and release notes.
- Record observations as capabilities, intentions, patterns, and trade-offs, not as a checklist of documents to copy.
4. Refining candidate capabilities:
- For each candidate, describe the problem it solves, user value, suitability, dependencies, risks, verifiability and relationship to the current status of the target project.
- For candidates whose licenses and sources are unclear or whose implementation is highly bound to reference projects, only refine ideas and do not reuse expressions.
5. Map to target architecture:
- Redesign using native naming, module boundaries, dependency strategies, coding conventions and testing methods of the target project.
- Avoid creating parallel systems that compete with existing modules; avoid blindly introducing dependencies just because the reference project uses them.
- Non-trivial changes can use [assets/absorption-plan-template.md](assets/absorption-plan-template.md).
6. Original realization or plan:
- Write new code or new documentation without copying non-trivial code, prompt words, configurations or documentation expressions from the reference project.
- Unify the boundaries of responsibilities and remove duplicate instructions when absorbing ecological extensions, prompt words, commands, plug-ins, automations, agents or rules.
- Large tasks are delivered in vertical thin slices first, and rejected or delayed candidates are recorded.
7. Verification and reporting:
- Run the most relevant type checks, lints, tests, builds, documentation checks or skill checks.
- If it cannot be verified, clearly state the cause of the blockage, the scope of the risk and the information that requires user confirmation.
- Use [assets/review-checklist.md](assets/review-checklist.md) for manual review when necessary.

## Constraints

- Don't turn absorb tasks into mechanized diff merging.
- Does not copy the naming scheme, file structure, or implementation details of the reference project in its entirety.
- Do not reuse verbatim non-trivial code, documentation, hints, or configurations from reference projects when the license or user intent is unclear.
- Do not compromise security, privacy, permission boundaries, testing, maintainability, or target project product direction to match the reference project.
- Do not claim originality unless the output can explain why the target design is different, why it is suitable for the target project, and how to verify it.
- Don't cram long reference material into the main description; large assignments read [references/methodology.md](references/methodology.md), licenses and original risks read [references/originality-and-licensing.md](references/originality-and-licensing.md).

## Expected Output

Analysis task output:

- Absorption candidates
- Recommended target design
- Realize the plan
- Description of risks and licenses
- Verification Checklist

Implementation class task output:

- Changes completed
- Instructions for originalization
- Verification results
- Remaining work

In warehouse-level tasks, if the host tool supports file editing, the project's local plan document should be created or updated.

## Detailed reference

- [references/methodology.md](references/methodology.md) - Absorb methodology in detail.
- [references/originality-and-licensing.md](references/originality-and-licensing.md) - Originality, license and provenance risk constraints.
