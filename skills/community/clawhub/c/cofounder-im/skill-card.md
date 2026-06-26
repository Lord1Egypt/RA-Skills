## Description: <br>
Pulls startup project data and AI-generated build specifications from CoFounder.im, then helps an agent review, plan, and orchestrate the build. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexfilatov](https://clawhub.ai/user/alexfilatov) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to fetch completed CoFounder.im startup plans, review the generated build specification, and coordinate approved implementation phases in OpenClaw or compatible coding agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a CoFounder.im API token to fetch user project plans. <br>
Mitigation: Install only when comfortable granting that token, keep the token scoped to CoFounder.im, and avoid exposing it in generated files or command output. <br>
Risk: Fetched build plans can propose extra credentials, cloud access, destructive commands, package installs, or other network activity. <br>
Mitigation: Review each phase and command before approval, run builds in a clean workspace, and reject requests for unnecessary credentials or broad access. <br>
Risk: Generated implementation plans may be incomplete, incorrect, or unsuitable for an existing repository. <br>
Mitigation: Require user confirmation before spawning sub-agents or running verification commands, and verify the resulting project against the intended build plan. <br>


## Reference(s): <br>
- [CoFounder.im OpenClaw homepage](https://cofounder.im/openclaw) <br>
- [CoFounder.im](https://cofounder.im) <br>
- [ClawHub skill page](https://clawhub.ai/alexfilatov/cofounder-im) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires COFOUNDER_API_TOKEN plus curl and jq; fetched build plans may identify additional project-specific tools.] <br>

## Skill Version(s): <br>
1.2.1 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
