## Description: <br>
Creates and revises WeChat public-account long-form article drafts from a topic card or spoken topic, applying configured audience, tone, and writing-style constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content writers and operators use this skill to draft, rewrite, or polish WeChat public-account articles. It is intended for article workflows that rely on local article files, account configuration, and an optional user-configured LLM endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article inputs, article configuration, and prompts may be sent to the user-configured LLM endpoint. <br>
Mitigation: Use a trusted endpoint, use a dedicated API key, and avoid submitting sensitive drafts or configuration values unless that data can be shared with the selected provider. <br>
Risk: The artifact describes execution through write.py, but this package does not include that script. <br>
Mitigation: Verify which write.py will run in the target environment before enabling execution, and review that script under the same security expectations as the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/aws-wechat-article-writing-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown draft content with configuration checks and optional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates draft.md for the selected article directory when the runtime workflow is available.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
