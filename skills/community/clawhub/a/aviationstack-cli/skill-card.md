## Description: <br>
Manage AviationStack via CLI - flights, airports, airlines, routes. Use when user mentions 'aviationstack', 'flight search', 'airport lookup', 'airline search', or wants to interact with the AviationStack API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Melvynx](https://clawhub.ai/user/Melvynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install, authenticate, and call an AviationStack CLI for flight, airport, airline, and route lookups with filtering, pagination, and selectable output formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow installs or bundles command-line tooling and may execute code from external installation sources. <br>
Mitigation: Review the api2cli and Bun installation sources before running the setup commands. <br>
Risk: The AviationStack token is a secret and could be exposed through shared terminals, logs, or copied command history. <br>
Mitigation: Only use a token you are comfortable giving to the CLI, avoid pasting real tokens into shared logs or terminals, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [Aviationstack Cli on ClawHub](https://clawhub.ai/Melvynx/aviationstack-cli) <br>
- [Bun installer](https://bun.sh/install) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Programmatic CLI calls should use the --json flag; commands may emit text, JSON, CSV, or YAML.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
