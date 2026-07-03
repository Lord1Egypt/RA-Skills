## Description: <br>
Allows the user to record custom data annotations and agent visibility metrics, and generates simple HTML dashboards for visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fulcra](https://clawhub.ai/user/fulcra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to model custom Fulcra annotations, store selected personal or agent activity records with consent, and generate simple HTML dashboards from the recorded data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store personal records, including sensitive sources such as health, location, calendar, prior chat context, or agent activity summaries, in a Fulcra datastore. <br>
Mitigation: Ask for explicit permission before enabling sensitive data sources or Agent Visibility logging, explain what will be persisted, and honor any declined sources. <br>
Risk: The skill uses API access to create schemas, send records, and retrieve data for dashboards. <br>
Mitigation: Use Fulcra authentication through the documented CLI flow, keep tokens out of files and chat output, and request consent before transmitting user-provided data. <br>
Risk: Generated dashboards may visualize incomplete or user-selected records and could be mistaken for a comprehensive live dashboard. <br>
Mitigation: Present the generated HTML as a static demonstration, include all retrieved records used for that demonstration, and hand off to the durable dashboard skill for live interactive dashboards. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fulcra/skills/fulcra-tracking) <br>
- [Fulcra agent skills repository](https://github.com/fulcradynamics/agent-skills) <br>
- [Fulcra CLI for Tracking & Dashboards](references/fulcra-tracking-cli.md) <br>
- [Fulcra Onboarding: Discovery](references/fulcra-tracking-discovery.md) <br>
- [Fulcra Record Annotations](references/fulcra-tracking-record-annotations.md) <br>
- [Fulcra Onboarding: Demonstration](references/fulcra-tracking-demonstration.md) <br>
- [Fulcra High-Impact Use Cases](references/fulcra-tracking-usecases.md) <br>
- [Fulcra CLI documentation](https://raw.githubusercontent.com/fulcradynamics/agent-skills/main/skills/fulcra-onboarding/references/fulcra-cli.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus generated HTML dashboard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Fulcra schemas, record selected data through Fulcra API access, retrieve records for visualization, and write a local HTML dashboard file after user consent and theme selection.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
