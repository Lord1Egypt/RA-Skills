## Description: <br>
Lighthouse-style efficiency audit for OpenClaw that scores an instance from A+ to F across six categories and identifies wasted tokens, bloated sessions, misconfigured crons, and model right-sizing opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anna-claudette](https://clawhub.ai/user/anna-claudette) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to audit local or authorized remote OpenClaw instances for efficiency issues, then review scored findings and optional remediation suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports may reveal operational details from OpenClaw configuration, cron names, session metadata, and transcript file sizes. <br>
Mitigation: Review reports before sharing them and run the audit only against OpenClaw directories you are authorized to inspect. <br>
Risk: Remote audits execute the audit over SSH against the supplied host. <br>
Mitigation: Verify the --remote host before running and use an authorized low-privilege account. <br>
Risk: Fix mode provides remediation commands or configuration edits that may be inappropriate for some deployments. <br>
Mitigation: Review suggested fixes before applying changes to sessions, cron jobs, skill directories, or OpenClaw configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anna-claudette/clawzembic) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/anna-claudette) <br>
- [ClawHub listing](https://clawhub.io/skills/clawzempic) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Terminal text report by default, JSON when requested, and Markdown-friendly remediation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores six audit categories from A+ to F and can include optional fix suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
