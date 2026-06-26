## Description: <br>
Monitors configured competitor web pages for text changes and records snapshots, change history, and competitive intelligence reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and business teams use this skill to monitor public competitor web pages for pricing, blog, changelog, and site-content changes and to produce change history or periodic intelligence reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-configured competitor URLs and can make broad outbound web requests. <br>
Mitigation: Use only public competitor URLs that you are authorized to monitor, and review configured domains before scheduled checks. <br>
Risk: The skill stores competitor configuration, page snapshots, and history under the user's home directory. <br>
Mitigation: Avoid monitoring sensitive or private pages and periodically review or remove stored data under ~/.openclaw. <br>
Risk: The advertised social monitoring and external alert channels are not fully supported by the bundled implementation. <br>
Mitigation: Treat the skill as a website diff, history, and report generator unless those features are implemented and reviewed in a future release. <br>
Risk: Path-like competitor names could lead to confusing or unintended local storage paths. <br>
Mitigation: Use simple competitor names made from letters, numbers, spaces, or hyphens. <br>


## Reference(s): <br>
- [Competitive Intelligence Report Templates](references/ci-templates.md) <br>
- [ClawHub Release Page](https://clawhub.ai/Johnnywang2001/competitor-intel-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples; the monitor writes JSON configuration, text snapshots, JSON history, and markdown-style reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists competitor configuration and page snapshots under ~/.openclaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
