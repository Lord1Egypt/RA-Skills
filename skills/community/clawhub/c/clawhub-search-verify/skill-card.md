## Description: <br>
Safely search and review ClawHub skills by keyword, showing details and risk before asking for explicit approval to install. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ViktorBjorn](https://clawhub.ai/user/ViktorBjorn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and ClawHub users use this skill to search for skills by keyword, inspect basic release details, and decide whether to proceed with installation approval. It is a discovery and review aid, not a substitute for independent security review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill's safety claims do not match what its included script can do. <br>
Mitigation: Review the wrapper before installing or running it, and do not treat its Trusted or Suspicious labels as a real security review. <br>
Risk: The wrapper can run local ClawHub CLI commands using the user's logged-in ClawHub session. <br>
Mitigation: Use an account and environment appropriate for the target action, and independently inspect any target skill before approving installation. <br>
Risk: The wrapper writes search terms to a local log file. <br>
Mitigation: Avoid using sensitive search terms, or clear the generated log when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ViktorBjorn/clawhub-search-verify) <br>
- [Publisher profile](https://clawhub.ai/user/ViktorBjorn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text with suggested ClawHub CLI commands and approval prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Takes a search term as input and may write search terms to a local log file when the wrapper runs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
