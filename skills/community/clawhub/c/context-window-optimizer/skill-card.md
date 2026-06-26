## Description: <br>
Optimizes context window usage by summarizing older conversation segments, extracting key facts and decisions to persistent notes, and keeping current context lean. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klemenska](https://clawhub.ai/user/klemenska) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep long OpenClaw conversations usable by analyzing session size, summarizing completed work, and extracting decisions or preferences into reviewable notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts read local OpenClaw session transcripts that may contain sensitive prompts, tool output, or secrets. <br>
Mitigation: Confirm which transcript will be used before running the scripts, avoid sessions containing secrets, and review generated outputs before retaining them. <br>
Risk: Extracted facts or preferences may be saved into memory or archive files with weak user control. <br>
Mitigation: Write outputs to explicit reviewable paths and keep only entries that are accurate, necessary, and appropriate for long-term retention. <br>


## Reference(s): <br>
- [Context Optimization Patterns](artifact/references/patterns.md) <br>
- [ClawHub Release Page](https://clawhub.ai/klemenska/context-window-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text and Markdown summaries or extracted decision notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write summaries or extracted decisions to explicit output paths when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
