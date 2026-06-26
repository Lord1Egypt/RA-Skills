## Description: <br>
AI SkillHub helps an agent extract content from supported URLs, classify it, generate raw-content and skill markdown files, and publish the result to GitHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eeyan2025-art](https://clawhub.ai/user/eeyan2025-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content curators and agent operators use this skill to turn a URL into a categorized knowledge skill by extracting source content, summarizing key facts, saving markdown files, and publishing them to a configured GitHub repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can extract and store full raw content from external sources, including potentially sensitive or copyrighted material. <br>
Mitigation: Use it only on content the operator is permitted to process, and manually review generated files before publishing. <br>
Risk: The workflow can use local GitHub credentials to publish generated files without a clearly documented approval step. <br>
Mitigation: Use a dedicated private repository and least-privilege GitHub token, then inspect generated files and the git diff before allowing any push. <br>
Risk: The artifact depends on local extraction and transcription scripts whose implementation is not included in the artifact. <br>
Mitigation: Inspect and pin the referenced local scripts and tools before enabling automated use. <br>


## Reference(s): <br>
- [AI SkillHub ClawHub Page](https://clawhub.ai/eeyan2025-art/ai-skillhub) <br>
- [eeyan2025-art ClawHub Publisher Profile](https://clawhub.ai/user/eeyan2025-art) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON prompt blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create raw content and skill markdown files and publish them to GitHub when configured.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
