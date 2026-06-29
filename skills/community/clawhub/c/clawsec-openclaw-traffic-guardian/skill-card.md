## Description: <br>
OpenClaw runtime traffic monitoring baseline for opt-in HTTP/HTTPS proxy inspection, egress detection, inbound injection detection, and social-account policy review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw builders and operators use this skill as a baseline for opt-in runtime traffic monitoring. It helps plan process-scoped proxy inspection, exfiltration and injection detection, social-account policy review, and redacted local findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Future proxy inspection could expose sensitive traffic if enabled too broadly. <br>
Mitigation: Keep monitoring opt-in and process-scoped, avoid global proxy or CA changes, and redact snippets before logging or alerting. <br>
Risk: This release does not include active proxy or runtime code. <br>
Mitigation: Treat it as an implementation baseline, verify release artifacts before standalone installs, and review any future runtime implementation before deployment. <br>
Risk: Social-account mutation triggers could activate in workflows that only need observation or research. <br>
Mitigation: Review trigger wording for the target environment and keep POLICY_REVIEW findings operator-reviewed without auto-blocking, auto-approving, or rewriting requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-openclaw-traffic-guardian) <br>
- [Project homepage](https://clawsec.prompt.security/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with command snippets and JSONL schema examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and python3; this release is a specification-only scaffold with no active proxy or runtime code.] <br>

## Skill Version(s): <br>
0.0.1-beta5 (source: evidence.release.version; artifact SKILL.md and CHANGELOG.md agree) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
