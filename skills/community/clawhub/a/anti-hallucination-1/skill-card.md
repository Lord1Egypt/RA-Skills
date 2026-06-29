## Description: <br>
防止AI幻觉的分级检查机制。高风险任务走完整流程，低风险走快速路径。无证据不输出，有疑问必标注。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiyinli811-crypto](https://clawhub.ai/user/xiyinli811-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to apply a tiered fact-checking checklist before answering factual questions, especially API summaries, reports, lists, and answers involving people, roles, numbers, or dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make agents slower or more conservative on factual tasks. <br>
Mitigation: Apply the full checklist to high-risk factual tasks and use the skill's faster path for low-risk tasks. <br>
Risk: The artifact asks agents to record mistakes to memory, which may be inappropriate for sensitive conversations. <br>
Mitigation: Review or disable persistent-memory use when conversations include sensitive information, and avoid storing private facts in remediation notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiyinli811-crypto/anti-hallucination-1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown guidance with checklists, decision trees, confidence labels, and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Encourages confidence annotations and explicit uncertainty for factual outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
