## Description: <br>
Skill Sandbox helps developers test untrusted Python skills before installing by running them in a monitored environment and reporting filesystem, environment, network, and subprocess behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Trypto1019](https://clawhub.ai/user/Trypto1019) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and ClawHub users use this skill to run untrusted Python skill scripts with monitoring before deciding whether to install them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat a SAFE report as proof that an unknown skill had no filesystem, network, subprocess, or credential behavior. <br>
Mitigation: Treat Skill Sandbox as a lightweight inspection helper and run unknown skills inside Docker, a VM, or another disposable environment. <br>
Risk: The skill's sandbox claims are stronger than what the implementation enforces. <br>
Mitigation: Do not rely on this skill as a real sandbox or as the only control before installing or executing untrusted skills. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Trypto1019/arc-skill-sandbox) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Trypto1019) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON report descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 on macOS or Linux; sandbox reports may include SAFE, SUSPICIOUS, or DANGEROUS verdicts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
