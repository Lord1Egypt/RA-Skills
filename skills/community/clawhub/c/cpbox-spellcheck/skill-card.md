## Description: <br>
Provides spell-corrected query suggestions for pre-search cleanup or a "Did you mean?" UI when a standalone spellcheck step is needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sprintmint](https://clawhub.ai/user/sprintmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check a user query for spelling corrections before search, or to present a corrected suggestion in a user-facing workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hosted spellcheck endpoint uses an automatic pay-per-use payment flow without clear cost limits or per-call approval controls. <br>
Mitigation: Use the skill only with x402 spending controls, reviewed payment setup, and operational monitoring appropriate for the environment. <br>
Risk: Queries sent to the hosted spellcheck service may contain sensitive text. <br>
Mitigation: Avoid sending confidential or regulated text unless the provider and data handling are approved for the use case. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sprintmint/cpbox-spellcheck) <br>
- [CPBox API Provider](https://www.cpbox.io) <br>
- [CPPay Facilitator](https://www.cppay.finance) <br>
- [x402 Payment Setup](https://github.com/springmint/cpbox-skills#prerequisites) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON] <br>
**Output Format:** [Markdown instructions with HTTP and shell examples; the spellcheck endpoint returns JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a paid x402 flow; accepts a required query string plus optional language and country parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
