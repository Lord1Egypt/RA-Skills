## Description: <br>
Validate, package, and verify ClawHub skills before and after publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daowuu](https://clawhub.ai/user/daowuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to audit ClawHub skill releases before and after publishing, including frontmatter checks, packaging validation, dependency declaration review, version verification, and repeated publish failure diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read the user-selected skill directory and propose or run local Python, OpenClaw, and ClawHub CLI commands. <br>
Mitigation: Install and use it only when comfortable with local directory inspection and command execution; review command targets before proceeding. <br>
Risk: Publishing checks can affect an intended ClawHub release if the active account, skill path, slug, or version is wrong. <br>
Mitigation: Confirm the active ClawHub account, target skill path, slug, and intended version before approving any publish step. <br>
Risk: Post-publish state can be confusing when latest version, scan status, or page visibility lags behind the publish attempt. <br>
Mitigation: Use post-publish verification and distinguish publish failure, latest tag mismatch, pending scan, and metadata or code mismatch before republishing. <br>


## Reference(s): <br>
- [ClawHub Release Auditor skill page](https://clawhub.ai/daowuu/clawhub-release-auditor) <br>
- [daowuu publisher profile](https://clawhub.ai/user/daowuu) <br>
- [ClawHub homepage](https://clawhub.ai) <br>
- [ClawHub Publisher Checklist](references/checklist.md) <br>
- [ClawHub Publishing Research Notes](references/research-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and optional JSON from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local Python, OpenClaw, and ClawHub CLI commands for the user to review and run.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
