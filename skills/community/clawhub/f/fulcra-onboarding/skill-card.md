## Description: <br>
Guides a new user or agent through Fulcra setup, CLI authentication, and next-step options for using Fulcra as a data and memory platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fulcra](https://clawhub.ai/user/fulcra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Onboard users to Fulcra by introducing the service, checking prerequisites with consent, guiding Fulcra CLI authentication, and offering follow-on paths for tracking, memory backup, agent coordination, the iOS app, and the web portal. <br>

### Deployment Geography for Use: <br>
Global, subject to the user's environment, network access, Fulcra service availability, and any local requirements for handling personal data. <br>

## Known Risks and Mitigations: <br>
Risk: Fulcra accounts may contain sensitive personal data, including health, location, calendar, activity, memory, and agent log information. <br>
Mitigation: Use the skill only when intentionally connecting to Fulcra, review each optional data path before enabling it, and decline tracking, uploads, or follow-on skills that are not wanted. <br>
Risk: Fulcra CLI login stores refreshable credentials on the local machine. <br>
Mitigation: Authenticate only on trusted devices and protect or remove local credentials when the environment is shared, temporary, or no longer trusted. <br>
Risk: The onboarding flow can install or check required tooling and initiate authentication commands. <br>
Mitigation: Require explicit user consent before installation, prerequisite checks, or login, and show the user any authorization URL and device code directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fulcra/fulcra-onboarding) <br>
- [Publisher profile](https://clawhub.ai/user/fulcra) <br>
- [Fulcra website](https://www.fulcradynamics.com/) <br>
- [Fulcra REST API documentation](https://fulcradynamics.github.io/developer-docs/api-reference/) <br>
- [Fulcra Python SDK and CLI source](https://github.com/fulcradynamics/fulcra-api-python/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational onboarding instructions, consent-gated command guidance, authentication prompts, and a menu of follow-on setup paths.] <br>
**Output Parameters:** [User consent for prerequisite checks and authentication, local uv and Fulcra CLI availability, Fulcra authentication state, and the user's selected next-step path.] <br>
**Other Properties Related to Output:** [The skill may ask the agent to run local CLI checks, present a Fulcra login URL and code, and recommend related Fulcra skills or apps after core onboarding.] <br>

## Skill Version(s): <br>
0.1.4 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
