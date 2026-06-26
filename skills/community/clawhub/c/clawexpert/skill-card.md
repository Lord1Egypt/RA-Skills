## Description: <br>
EverClaw turns an OpenClaw agent into a persistent domain research assistant that can build and reuse a local, citable knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edgepro001](https://clawhub.ai/user/edgepro001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use EverClaw to research a topic, organize web and PDF source material into an indexed local knowledge base, and answer later questions with citations from that stored knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad autonomous web and PDF collection and retain raw source material locally. <br>
Mitigation: Review the configured knowledge directory before use, set storage boundaries, and avoid confidential, regulated, or copyrighted material unless rights and retention limits are clear. <br>
Risk: The skill can keep cross-session learning state and inferred research interests. <br>
Mitigation: Use the documented master switch and proactive-mode controls, and periodically review or delete stored topics and proactive queues. <br>
Risk: Scheduled or proactive learning can run without direct per-topic interaction when enabled. <br>
Mitigation: Keep proactive mode and cron entries disabled unless intentionally configured, and review generated source collections before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/edgepro001/clawexpert) <br>
- [Project homepage](https://github.com/EdgePro001/ClawExpert) <br>
- [README](README.md) <br>
- [Subagent Prompt Template](references/subagent-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, structured knowledge-base files, and concise status reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write persistent local knowledge-base files and source extracts under the configured knowledge directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
