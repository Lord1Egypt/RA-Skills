## Description: <br>
Build or improve a bilingual email translation and notification workflow that converts raw emails into Chinese-friendly bilingual output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huacius](https://clawhub.ai/user/huacius) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product engineers use this skill to design or maintain prompt-driven bilingual email translation workflows for inbox notifications and mail assistants. It helps define formatting contracts for subject, date, body, recipients, quoted-history summaries, duplicate-line suppression, and signatures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connecting the workflow to a live mailbox or LLM provider can expose credentials or sensitive email content. <br>
Mitigation: Review any added scripts before deployment, keep credentials narrowly scoped, and avoid sending sensitive email content to third-party services without user consent and appropriate privacy controls. <br>


## Reference(s): <br>
- [Mail Translation Contracts](references/contracts.md) <br>
- [Commands](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-layer contract guidance for bilingual formatting, recipient truncation, quoted-history summarization, duplicate suppression, signature handling, and pass-through postprocessing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
