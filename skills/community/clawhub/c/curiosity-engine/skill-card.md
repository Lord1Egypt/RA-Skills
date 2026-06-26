## Description: <br>
Curiosity Engine adds structured curiosity behaviors to OpenClaw agents so they can explore open-ended questions, investigate anomalies, challenge assumptions, identify information gaps, and use tools for deeper analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luofulily1-cmyk](https://clawhub.ai/user/luofulily1-cmyk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to make OpenClaw agents more exploratory on research, investigation, anomaly analysis, and other tasks where depth matters more than speed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make agents more exploratory, which may add investigation steps when a user expects a quick answer. <br>
Mitigation: Use the documented /curious off setting or ask for a quick answer when extra investigation is not desired. <br>
Risk: Exploration may involve file reads, shell commands, web searches, or optional memory use depending on available tools. <br>
Mitigation: Keep approval prompts enabled for file reads and shell commands, and enable memory only for topics suitable for retention. <br>


## Reference(s): <br>
- [Curiosity Engine Examples](references/examples.md) <br>
- [Theoretical Foundations](references/theory.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and structured response sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include confidence ratings, surprises, and open threads when the full curiosity loop runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
