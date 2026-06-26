## Description: <br>
Fact Check guides an agent to identify and verify factual, technical, date, URL, API, and version claims before presenting them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futurizerush](https://clawhub.ai/user/futurizerush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent operators use this skill to verify technical claims, current versions, API fields, CLI flags, file paths, URLs, and dates before shipping work or answering users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification commands or limited network/API checks could expose private repository paths, confidential URLs, or authenticated session context. <br>
Mitigation: Use the skill in environments where private data handling is understood, avoid fetching untrusted user-provided content beyond status checks, and review commands before execution when sensitive resources are involved. <br>
Risk: Unverified or stale claims can still remain when required tools, network access, or credentials are unavailable. <br>
Mitigation: Label unavailable checks as unverified or unverifiable and avoid presenting them as confirmed facts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/futurizerush/fact-check-verify) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown report with evidence tables and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include verified, corrected, unverified, or unverifiable claim labels with cited evidence sources.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
