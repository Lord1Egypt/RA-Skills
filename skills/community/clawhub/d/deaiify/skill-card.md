## Description: <br>
Ban LLM em-dashes and en-dashes before delivery, rewrite via embedded LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnpetros](https://clawhub.ai/user/shawnpetros) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this OpenClaw plugin to automatically detect en dashes and em dashes in assistant replies and rewrite affected prose before delivery while preserving code formatting and normal hyphen-minus usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assistant replies may pass through an additional configured model rewrite step, which can be inappropriate for exact wording, legal or compliance text, secrets, or highly sensitive content. <br>
Mitigation: Avoid or disable the plugin for conversations where exact wording must be preserved or where sensitive content should not enter an additional model rewrite step. <br>
Risk: A rewrite can fail, return empty text, still contain banned dash characters, or drift too far from the original reply. <br>
Mitigation: The plugin rejects empty rewrites, rewrites that still contain banned dashes, and rewrites with excessive word-count or length drift, then delivers the original reply unchanged. <br>
Risk: The embedded rewrite uses temporary local session storage during processing. <br>
Mitigation: Temporary rewrite session files are removed immediately after the rewrite run, and the embedded rewrite disables tools and message sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shawnpetros/deaiify) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [Plain text assistant replies rewritten when banned Unicode dash characters are detected] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the active session model for rewrites, ignores code spans and fenced code blocks for detection, and fails open to the original reply when rewriting or validation does not succeed.] <br>

## Skill Version(s): <br>
3.4.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
