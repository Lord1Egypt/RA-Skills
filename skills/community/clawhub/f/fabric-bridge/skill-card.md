## Description: <br>
Fabric Bridge helps agents use Fabric AI CLI patterns for text transformation, analysis, content creation, writing improvement, code review, threat modeling, and structured extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koriyoshi2041](https://clawhub.ai/user/koriyoshi2041) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and other agent users use this skill to select and run Fabric AI patterns through the fabric-ai CLI for summarization, extraction, writing improvement, code review, threat modeling, and related text workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fabric AI usage can involve external AI providers, API keys, and user-supplied content. <br>
Mitigation: Use a dedicated or revocable API key where possible and avoid sending secrets or regulated data. <br>
Risk: Community patterns, saved sessions, contexts, and custom pattern files may affect prompts and outputs. <br>
Mitigation: Review community patterns, saved sessions, contexts, and custom pattern files before relying on them. <br>
Risk: Sensitive workflows may send data to an external model provider if run normally. <br>
Mitigation: Use fabric-ai --dry-run to inspect what will be sent before making API calls. <br>


## Reference(s): <br>
- [Fabric AI GitHub Repository](https://github.com/danielmiessler/fabric) <br>
- [Popular Fabric Patterns](references/popular-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/koriyoshi2041/fabric-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional Fabric AI text or markdown output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can stream Fabric AI output, save output to a file, copy output to the clipboard, or dry-run prompts before API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
