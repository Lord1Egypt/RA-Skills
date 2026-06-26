## Description: <br>
Trusted publish assistant for bot and agent teams that publishes and syncs local skills to ClawHub with non-browser token login, preflight safety checks, and a repeatable release flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, bot builders, and OpenClaw operators use this skill to publish a single local skill folder or sync a local skills directory to ClawHub through repeatable CLI-based release steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a ClawHub token with publishing authority. <br>
Mitigation: Use the least-privileged token available, keep it in the runtime environment or trusted env file, and rotate or confirm the token if authentication fails. <br>
Risk: Publishing the wrong skill path, sync root, or registry could release unintended content. <br>
Mitigation: Review the target path or sync root before running, use dry-run where possible, and avoid untrusted registry overrides. <br>
Risk: The default single-skill preflight blocks CJK text unless explicitly allowed. <br>
Mitigation: Use --allow-cjk only when the target registry policy and release content permit it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wanng-ide/clawhub-skill-publisher) <br>
- [ClawHub Registry](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for local publishing or sync workflows; execution depends on the ClawHub CLI and an authorized CLAWHUB_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
