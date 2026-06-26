## Description: <br>
Helps users examine potentially dubious beliefs through consent-based verification, Socratic questioning, and privacy-aware reasoning guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asgraf](https://clawhub.ai/user/asgraf) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and assistants use this skill to examine sensitive or controversial claims, trace reasoning chains, and identify logical gaps while preserving user autonomy and privacy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask the agent to retain sensitive belief discussions, claim stacks, and emotional context in memory. <br>
Mitigation: Disable or override memory persistence unless the user explicitly requests a specific note be saved. <br>
Risk: Consent-based external verification can still send user claims to web search, fact-checking tools, or other services if enabled. <br>
Mitigation: Confirm available tools before use, ask for explicit consent, and disclose what will be checked externally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asgraf/epistemic-guide) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Consent-based external verification may be offered when tools are available; the skill can also operate offline using Socratic questioning.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
