## Description: <br>
BestCoffer AI Redaction helps an agent upload a user-selected document with natural language redaction instructions and return a BestCoffer task link for progress tracking and result download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marsxh](https://clawhub.ai/user/marsxh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to redact sensitive information from a single uploaded PDF, Word, Excel, TXT, PNG, JPG, or JPEG file. The user supplies the redaction instruction, confirms execution, and receives a task URL for status and result download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marsxh/bestcoffer-ai-redaction) <br>
- [BestCoffer API console](https://apiconsole.bestcoffer.com.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON result with taskUrl and errorMessage fields, plus concise user-facing status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and npm, an API key configured as a secret or environment variable, a single input file up to 10MB, and a user-provided redaction instruction. Review before installing because selected documents and instructions are uploaded to BestCoffer, returned task URLs are sensitive, and debug logs may persist local paths, instructions, and task links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
