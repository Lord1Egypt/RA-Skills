## Description: <br>
Design and execute A/B testing experiments for LLM prompts, agent behaviors, and content production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[demo112](https://clawhub.ai/user/demo112) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt engineers, and content teams use this skill to design, run, analyze, and archive controlled A/B experiments for LLM prompts, agent behaviors, and content variants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may spawn subagents and persist experiment outputs or notes, which can expose confidential prompts, customer data, or proprietary outputs if used as test inputs. <br>
Mitigation: Use non-sensitive samples by default; ask the agent to confirm before spawning subagents or writing files, and request a planning-only or no-save run for confidential work. <br>
Risk: Small sample sizes or self-scoring can produce directional or biased results rather than reliable conclusions. <br>
Mitigation: Use at least 10 samples per group, prefer blind cross-scoring or external scoring, and label smaller tests as directional signals. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Text] <br>
**Output Format:** [Markdown guidance with JSON experiment manifests and result records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write experiment records and analysis under memory/experiments when the agent follows the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
