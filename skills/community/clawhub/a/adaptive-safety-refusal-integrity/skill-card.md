## Description: <br>
Helps evaluate whether an agent maintains refusal integrity when harmful requests are disguised through role-play, slang, technical framing, or persuasive pressure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tzwwww](https://clawhub.ai/user/tzwwww) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, safety evaluators, and red-team reviewers use this skill to create and select adversarial safety-evaluation QA pairs that test whether an agent refuses harmful requests despite role-play, obfuscation, or persuasion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for safety testing but can create reusable, persuasion-shaped harmful prompt sets. <br>
Mitigation: Use only in controlled red-team or safety-evaluation environments, and access-control any generated unsafe prompt libraries. <br>
Risk: Browsing or broad corpora could enrich adversarial prompts with current or private details. <br>
Mitigation: Disable or explicitly approve web browsing, use vetted non-private corpora, and review outputs before reuse. <br>


## Reference(s): <br>
- [Phase 1: Environment Exploration Guide](references/EXPLORATION.md) <br>
- [Phase 2: Trajectory Selection Criteria](references/SELECTION.md) <br>
- [Phase 3: Data Synthesis Instructions](references/SYNTHESIS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown guidance and JSON QA pairs with trajectory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces safety-evaluation prompts, refusal answers, and trajectory notes for reviewer-controlled use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
