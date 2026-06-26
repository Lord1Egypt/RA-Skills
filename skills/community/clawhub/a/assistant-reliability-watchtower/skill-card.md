## Description: <br>
Assistant Reliability Watchtower provides deterministic reliability monitoring for OpenClaw assistant workflows, including smoke probes, daily digests, scorecard evidence validation, delivery preambles, and probe/reporting coverage inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wit-oc](https://clawhub.ai/user/wit-oc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run ARW smoke probes, generate reliability digests, validate scorecard reporting evidence, and render operator preambles for OpenClaw assistant workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python helper that can read workspace or environment-derived paths. <br>
Mitigation: Run it in a limited project directory, pass the intended repo root explicitly, and review wrapper commands before using it with sensitive files or secrets. <br>
Risk: The release evidence identifies a least-privilege documentation gap. <br>
Mitigation: Confirm the intended workspace access and artifact paths before installation or operational use. <br>


## Reference(s): <br>
- [ARW RC1 release contract](references/release-contract.md) <br>
- [ARW probe and signal catalog](references/probe-catalog.md) <br>
- [ARW config contract](references/config-contract.md) <br>
- [ClawHub skill page](https://clawhub.ai/wit-oc/assistant-reliability-watchtower) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown and shell-oriented operational guidance, with generated ARW JSON and Markdown artifacts from wrapper commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are repo-backed and commonly written under the configured artifacts/arw path.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
