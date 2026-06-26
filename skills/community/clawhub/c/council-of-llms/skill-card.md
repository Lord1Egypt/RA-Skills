## Description: <br>
Real multi-model council deliberation for OpenClaw subagents that spawns three parallel subagents with different LLMs and analytical perspectives, then synthesizes their outputs into a unified verdict with consensus points, disagreements, and action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wahajahmed010](https://clawhub.ai/user/wahajahmed010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run multi-model deliberation for reviews, stress tests, decisions, and analytical verdicts. It is intended to produce a synthesized council review from three independent subagent perspectives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch multiple long-running subagents for an ordinary review or analysis request. <br>
Mitigation: Confirm that a council run is intended before invoking it, review the configured models, and monitor timeout settings for the task size. <br>
Risk: The skill can write a council-review-[topic].md file that may overwrite or clutter a sensitive workspace. <br>
Mitigation: Choose the output filename or location explicitly and check for existing council-review-* files before writing the synthesis. <br>
Risk: Council subagents do not receive conversation history or web access, so incomplete context can produce misleading analysis. <br>
Mitigation: Provide only necessary verified context inline, summarize large inputs, and keep task descriptions within the documented limits. <br>


## Reference(s): <br>
- [Council Of Llms on ClawHub](https://clawhub.ai/wahajahmed010/council-of-llms) <br>
- [Subagent Orchestration companion skill](https://github.com/wahajahmed010/subagent-orchestration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown synthesis with consensus points, disagreements, blind spots, a final verdict, and action items.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May spawn three long-running subagents and write a council-review-[topic].md file in the workspace.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
