## Description: <br>
Consults official documentation before answering questions about specific third-party software, APIs, SDKs, CLIs, packages, frameworks, or tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itoldis](https://clawhub.ai/user/itoldis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to verify software-specific answers against official documentation before responding, especially for API signatures, CLI flags, installation steps, configuration, compatibility, and tool errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Official documentation lookups can add latency or fail when authoritative documentation is unavailable. <br>
Mitigation: State when official documentation cannot be found and clearly mark any fallback answer as unverified against current docs. <br>
Risk: Using a mismatched documentation page or version can still lead to stale or incorrect software guidance. <br>
Mitigation: Prefer official docs or repositories that match the user's version and include the specific page used as a compact footer link. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown response with a compact documentation-link footer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers should be grounded in official documentation and include a direct source link.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
