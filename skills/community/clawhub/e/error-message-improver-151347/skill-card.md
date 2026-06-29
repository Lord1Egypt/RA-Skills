## Description: <br>
Helps developers, support teams, SaaS operators, and users turn vague errors into clearer messages that explain what failed, why it failed, and what action to take next. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support teams, SaaS operators, and users use this skill to rewrite or plan clearer error messages, troubleshooting workflows, checklists, and validation notes when vague failures block action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may cause the skill to be invoked for general debugging or support requests. <br>
Mitigation: Use the workflow when the user is asking to improve error messages, troubleshooting communication, support guidance, or a closely related deliverable. <br>
Risk: Generated error messages or troubleshooting steps may be incomplete when the user provides little context. <br>
Mitigation: State assumptions, ask only for missing information that materially changes the output, and include a validation note or follow-up checks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/error-message-improver-151347) <br>
- [Requirement Plan](references/requirement-plan.md) <br>
- [Classify prose/empty LLM generation output separately from architecture regressions](https://github.com/promptdriven/pdd/issues/1649) <br>
- [Endpoint Authoring with Better Autocomplete and Actionable Error Messages](https://github.com/VoidenHQ/voiden/issues/448) <br>
- [Error message improvements](https://github.com/jump-dev/JuMP.jl/issues/4175) <br>
- [SegmentFault error-messages](https://segmentfault.com/t/error-messages) <br>
- [Typst 0.15.0](https://news.ycombinator.com/item?id=48545698) <br>
- [CS 6120: Advanced Compilers: The Self-Guided Online Course](https://news.ycombinator.com/item?id=48595469) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with optional code blocks, checklists, workflow steps, and validation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include assumptions, remaining risks, and next-step notes when useful.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
