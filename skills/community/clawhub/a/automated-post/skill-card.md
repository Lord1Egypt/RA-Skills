## Description: <br>
Automated Post coordinates text and image agents to prepare, publish, and archive image-and-text posts with either step-by-step confirmation or final approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yifeiwang1981](https://clawhub.ai/user/yifeiwang1981) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users invoke this skill to coordinate Chinese-language post copy, image generation, website publishing, and Feishu archiving. It supports confirmation checkpoints so generated content and images can be reviewed before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated posts or images could be published or archived before sensitive, incorrect, or unwanted material is caught. <br>
Mitigation: Use confirmation mode for sensitive topics and review the final copy, image, destination website account, and Feishu document permissions before publishing. <br>
Risk: Publishing and archiving commands can persist content to external services. <br>
Mitigation: Run the workflow only in the intended configured environment and avoid publishing or archiving confidential material unless that persistence is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yifeiwang1981/automated-post) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes generated post copy, image prompts or paths, timing records, and archive guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
