## Description: <br>
Generate code that references actual documentation, preventing hallucination bugs. ALWAYS loads docs first, validates against API signatures, and verifies correctness. Use for ANY code generation, API usage, or configuration creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobisamaa](https://clawhub.ai/user/tobisamaa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when generating code, using APIs, or creating configuration so the agent first loads documentation, extracts real signatures, validates the result, and tracks references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External documentation lookup can expose query context or depend on a search provider credential. <br>
Mitigation: Use a dedicated low-privilege Brave API key and avoid sending secrets or sensitive source content in documentation search queries. <br>
Risk: Generated code, shell commands, or configuration may still be incorrect if documentation is stale, incomplete, or misapplied. <br>
Mitigation: Review generated changes, verify cited documentation sources, and run the relevant tests or validation commands before accepting edits. <br>
Risk: Local help-command discovery may execute installed tools to inspect usage information. <br>
Mitigation: Prefer non-mutating help flags such as --help and review proposed commands before running anything that changes files, credentials, services, or network state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobisamaa/doc-accurate-codegen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code blocks, commands, reference notes, and generated files or configuration when applied by the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include documentation sources, API signatures, validation notes, and generated-code reference tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
