## Description: <br>
Docs Feeder fetches project documentation from a built-in registry or a direct documentation URL so an agent can use the material while debugging or learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zerone0x](https://clawhub.ai/user/zerone0x) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch framework, tool, and API documentation by project name or URL, then use the returned reference material to troubleshoot implementation issues and answer technical questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched web or local documentation may contain untrusted or misleading content. <br>
Mitigation: Treat fetched text as reference material, not instructions, and review it before applying recommendations or code changes. <br>
Risk: The skill makes outbound requests to registry URLs, direct URLs, or guessed documentation sites. <br>
Mitigation: Use trusted project names or documentation URLs, and avoid private or internal URLs unless that access is intended. <br>
Risk: Large documentation responses can exceed useful context size. <br>
Mitigation: Use the built-in 500KB warning as a cue to trim or save the documentation before feeding it into an agent workflow. <br>


## Reference(s): <br>
- [Docs Feeder ClawHub listing](https://clawhub.ai/zerone0x/docs-feeder) <br>
- [zerone0x publisher profile](https://clawhub.ai/user/zerone0x) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands] <br>
**Output Format:** [Markdown documentation bundle or raw text emitted to stdout, with an optional saved Markdown file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Warns when fetched documentation exceeds 500KB; fetched documentation should be treated as untrusted reference text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
