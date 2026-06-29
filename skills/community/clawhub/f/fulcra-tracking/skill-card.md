## Description: <br>
Allows the user to record custom data annotations and agent visibility metrics, and generates simple HTML dashboards for visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fulcra](https://clawhub.ai/user/fulcra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to create Fulcra data schemas, record custom personal or agent-visibility annotations, and generate static HTML dashboards from the recorded data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may store selected personal tracking data in Fulcra. <br>
Mitigation: Ask for explicit user consent before recording each personal data item and avoid health, location, messaging, calendar, sleep, or other sensitive streams unless the user deliberately opts in. <br>
Risk: Agent visibility logging may persist summaries of the agent's work. <br>
Mitigation: Enable agent visibility only after user consent, and avoid logging work that may contain secrets or private third-party information. <br>
Risk: The skill requires Fulcra authentication and may use sensitive access credentials. <br>
Mitigation: Use the Fulcra CLI token flow without printing tokens or storing credentials in files. <br>


## Reference(s): <br>
- [Fulcra Tracking on ClawHub](https://clawhub.ai/fulcra/fulcra-tracking) <br>
- [Fulcra CLI for Tracking & Dashboards](references/fulcra-tracking-cli.md) <br>
- [Fulcra Onboarding: Discovery](references/fulcra-tracking-discovery.md) <br>
- [Fulcra Record Annotations](references/fulcra-tracking-record-annotations.md) <br>
- [Fulcra Onboarding: Demonstration](references/fulcra-tracking-demonstration.md) <br>
- [Fulcra High-Impact Use Cases](references/fulcra-tracking-usecases.md) <br>
- [Fulcra CLI documentation](https://raw.githubusercontent.com/fulcradynamics/agent-skills/main/skills/fulcra-onboarding/references/fulcra-cli.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated HTML dashboard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local static dashboard assets after user consent and theme selection.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
