## Description: <br>
Comprehensive Effect-TS development guide for TypeScript, focused on Effect v4 for new projects while supporting v3 codebases, with guidance for typed errors, concurrency, dependency injection, resources, schemas, observability, HTTP, configuration, SQL, CLI, RPC, STM, and Effect AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when building, debugging, reviewing, migrating, or generating TypeScript code with Effect. It helps agents choose version-appropriate Effect APIs, avoid common hallucinated APIs, and produce guidance, code examples, commands, and configuration patterns for Effect v4 and v3 projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated server, file upload, database, AI, and observability examples may be copied into production without normal engineering review. <br>
Mitigation: Review generated code before use, with particular attention to upload validation and cleanup, database behavior, API-key handling, and observability configuration. <br>
Risk: Effect v4 is beta and API names can change across exact beta versions. <br>
Mitigation: Detect the installed Effect version, pin exact v4 beta versions for new projects, and verify APIs against the referenced Effect documentation before applying generated code. <br>
Risk: The skill includes examples that use optional sensitive credentials for AI providers. <br>
Mitigation: Keep OPENAI_API_KEY and ANTHROPIC_API_KEY out of generated output, logs, and committed files; treat them as runtime secrets only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/effect-ts) <br>
- [Publisher profile](https://clawhub.ai/user/tenequm) <br>
- [Source homepage](https://github.com/tenequm/skills/tree/main/skills/effect-ts) <br>
- [Effect v4 source and migration guides](https://github.com/Effect-TS/effect-smol) <br>
- [Effect v4 LLM guide](https://github.com/Effect-TS/effect-smol/blob/main/LLMS.md) <br>
- [Effect v3 documentation](https://effect.website/docs) <br>
- [Effect LLM topic index](https://effect.website/llms.txt) <br>
- [Effect full LLM documentation](https://effect.website/llms-full.txt) <br>
- [Effect API reference](https://tim-smart.github.io/effect-io-ai/) <br>
- [LLM Corrections](references/llm-corrections.md) <br>
- [Core Patterns](references/core-patterns.md) <br>
- [Concurrency](references/concurrency.md) <br>
- [Dependency Injection](references/dependency-injection.md) <br>
- [Error Modeling](references/error-modeling.md) <br>
- [Resource Management](references/resource-management.md) <br>
- [Retry and Scheduling](references/retry-scheduling.md) <br>
- [Schema](references/schema.md) <br>
- [HTTP Client and Server](references/http.md) <br>
- [Effect AI](references/effect-ai.md) <br>
- [Testing Effect Code](references/testing.md) <br>
- [Migrating from Effect v3 to v4](references/migration-v4.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference optional OPENAI_API_KEY or ANTHROPIC_API_KEY environment variables for Effect AI examples.] <br>

## Skill Version(s): <br>
0.5.0 (source: SKILL.md frontmatter, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
