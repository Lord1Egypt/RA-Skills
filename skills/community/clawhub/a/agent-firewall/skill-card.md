## Description: <br>
Provides real-time input/output filtering for agent communications to help block prompt injection, data exfiltration, and unauthorized commands before they reach the model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arhadnane](https://clawhub.ai/user/arhadnane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill as a helper filter around agent input and output to detect or redact prompt injections, encoded payloads, secrets, PII, internal paths, and other risky content before it is passed onward. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain or return raw sensitive content through originalData and full-context logs. <br>
Mitigation: Make integrations consume processedData only, avoid sending secrets or full prompts in context, restrict access to .security/firewall-logs, and prefer redacted metadata in logs. <br>
Risk: Users may treat the skill as a hard security boundary even though the security guidance frames it as a helper filter. <br>
Mitigation: Use it as one layer in a reviewed defense-in-depth workflow, and test blocked, redacted, and pass-through cases before relying on it. <br>
Risk: Artifact behavior indicates external YAML rules are not parsed and default rules are used instead. <br>
Mitigation: Verify the effective rules loaded at runtime and add a real YAML parser or deployment test before assuming custom rule files are enforced. <br>


## Reference(s): <br>
- [Agent Firewall on ClawHub](https://clawhub.ai/arhadnane/agent-firewall) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration, Guidance] <br>
**Output Format:** [JSON result with processed text, action metadata, success status, and retained original input; documentation includes Markdown and YAML configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write filter action logs under .security/firewall-logs; consumers should use processedData rather than originalData when enforcing filtered output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, skill.json, and index.js) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
