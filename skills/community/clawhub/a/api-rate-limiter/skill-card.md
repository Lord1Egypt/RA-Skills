## Description: <br>
Manages API request rates with configurable delays, request-type policies, status checks, and retry-oriented rate-limit controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[monline-code](https://clawhub.ai/user/monline-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to add a local command-line delay helper before API calls, inspect rate-limit settings, and adjust request pacing policies for light, medium, heavy, or custom request types. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer may create or replace a system-wide api-rate-limiter command link in /usr/local/bin using sudo. <br>
Mitigation: Review install.sh before running it and install only in environments where a system-wide command link is acceptable. <br>
Risk: The skill is a local command-line delay helper and should not be assumed to automatically intercept every API request. <br>
Mitigation: Call api-rate-limiter explicitly from integrations before API requests and verify behavior with check-status and show-config. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/monline-code/api-rate-limiter) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [default_config.json](artifact/default_config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local CLI usage guidance and configuration changes; no network output is indicated by the evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
