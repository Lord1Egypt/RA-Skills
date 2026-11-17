---
name: fec-doc-sync
description: Use when synchronizing frontend project documentation with source-of-truth files such as package.json, lockfiles, config, env examples, routes, API clients or server routes, schemas, components, tests, CI, build/deploy config, ADRs, changelogs, or migration notes. Do not use for general prose polishing only; Chinese triggers include document synchronization, update README, docs sync, environment variable documentation, command list, API Document synchronization.
---

# Document synchronization

## Purpose

Synchronize front-end project documentation from code, configuration, tests, types, scripts and runtime templates to avoid README, docs, environment variable descriptions, API/routing descriptions, architectural decisions and migration notes from drifting from actual project behavior.

## Procedure

1. Identify the project stack, document entry and the scope that needs to be synchronized this time; README synchronization must scan the root directory `README*`, `docs/*/README*`, package, application, deployment or runtime related README, and exclude `node_modules`, build products and third-party dependency directories.
2. Gather sources of truth: `package.json`, lockfile, framework and build configurations, `.env.example`, routes, API clients or server routes, types/schemas, components, tests, CI, build/deploy config.
3. Compare commands, environment variables, routes, API behaviors, deployment steps and support matrix in README, docs, ADR, changelog, example prompts, setup/deploy/env docs.
4. Only update stable public conventions; do not write temporary debugging conclusions, one-time reports or unimplemented designs into long-term documents.
5. If the warehouse already has multilingual documents or internationalized README, after updating the public facts of the main README, you must check whether other language READMEs need to be synchronized; function names, command names, script names, package names, component/API names, report file names, paths, environment variables, routing/API names, version constraints, and support matrices must be consistent across languages.
6. Product copy can maintain localized expression, but must not retain old facts, old default recommendations, or expired examples; when high-quality translation is not possible, at least synchronize key facts, and mark the risks of manual translation in the output.
7. When the project exposes plug-ins, SDKs, CLIs, component libraries, templates or integration capabilities, synchronize the corresponding function list, integration instructions, command/script instructions, public metadata, example prompt words or example usage.
8. Run relevant documentation consistency, legacy searches, report format consistency, type checks, testing, build or packaging checks.

## Constraints

- Do not turn README into complete implementation details; public documentation retains high-signal summaries.
- Do not introduce command, path, environment variable, API behavior, or capability names that are inconsistent with the source of truth.
- Do not write unconfirmed TODOs, drafts, or experimental capabilities as supported behavior.
- Do not modify user project private documents unless explicitly specified by the user.
- If multi-language documents cannot be fully translated, at least keep the command names, environment variables, route/API names, version constraints and report formats consistent.
- Do not reduce internationalized README synchronization to just the main README; public facts, feature lists, report lists, command/script descriptions, and example usage must check all language entries.
- Do not treat ADR as a long review; only record the background, decisions, trade-offs, scope of impact, verification and rollback clues.

## Expected Output

- List synchronized README/docs/ADR/changelog/env/setup/deploy documents.
- List the checked README/docs entries and indicate which language files have been synchronized, which do not need to be synchronized, and which require manual confirmation.
- Summarize the sources of truth used, update scope, verification orders, and non-coverage risks.
- Aggregate legacy caliber searches, report filename/path/command consistency and multilingual key fact consistency verification results.
- Highlight product copy, translations, external service configurations, or release notes that still require manual confirmation.
