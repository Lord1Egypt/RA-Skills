## Description: <br>
Compresses conversation and memory logs into structured summaries that preserve key decisions, lessons, and next actions while reducing token usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to turn Markdown conversation logs into shorter long-term memory summaries for files such as MEMORY.md. It is intended for reviewed local memory maintenance, not unattended replacement of original logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced context-compressor.js script may be missing or may come from a source the user has not reviewed. <br>
Mitigation: Confirm that the script is present and trusted before installing or running the workflow. <br>
Risk: Compressed summaries can omit or distort important context if used without review. <br>
Mitigation: Keep original logs and review compressed output before appending it to MEMORY.md or replacing source material. <br>
Risk: Recurring maintenance rules could repeatedly add unreviewed summaries to long-term memory. <br>
Mitigation: Review the workflow before adding automated or recurring maintenance instructions. <br>


## Reference(s): <br>
- [Context Compressor Free on ClawHub](https://clawhub.ai/thcjp/skills/context-compressor-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local compression of Markdown memory logs and recommends preserving originals and reviewing compressed output before appending it to long-term memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
