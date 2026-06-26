## Description: <br>
Cn LLM helps agents use AIsa for model routing, provider setup, Chinese LLM access, and model operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure AIsa-backed Chinese LLM workflows, inspect supported models, and route chat or comparison requests through the bundled client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-requested prompts and message content to the remote AIsa API. <br>
Mitigation: Avoid sending confidential, regulated, or proprietary prompts unless AIsa is approved for that data. <br>
Risk: AISA_API_KEY is a sensitive credential used for remote provider access. <br>
Mitigation: Use a scoped or quota-limited API key where possible and keep it in the environment rather than embedding it in prompts or files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baofeng-tech/cn-llm) <br>
- [AIsa API endpoint](https://api.aisa.one/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; the bundled CLI returns JSON or streamed text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY for AIsa-backed chat and compare operations; model listing does not require the API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
