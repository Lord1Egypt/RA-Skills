## Description: <br>
Optimizes skills, prompts, articles, workflows, and systems through iterative single-change mutation testing, scoring, and regression discard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcjl](https://clawhub.ai/user/0xcjl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to improve text-based skills, prompts, documentation, workflows, and system descriptions through checklist-based iteration. It is best suited for artifacts that can be evaluated with concrete criteria and reviewed after each batch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can iteratively edit local prompts, skills, plugins, or other text artifacts after confirmation. <br>
Mitigation: Use explicit target paths, confirm activation only for intended optimization tasks, and review proposed changes before continuing long runs. <br>
Risk: Long optimization loops may move content in an unintended direction if checklist criteria or test cases are weak. <br>
Mitigation: Use at least five checklist questions, prefer realistic test cases, and use the documented 30-round human review pause to decide whether to continue or stop. <br>
Risk: It is not suitable for code with runtime behavior, binary content, or subjective creative work without clear criteria. <br>
Mitigation: Use runtime tests for executable code and limit this skill to text artifacts that can be scored against concrete review criteria. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xcjl/cjl-autoresearch-cc) <br>
- [Publisher profile](https://clawhub.ai/user/0xcjl) <br>
- [Mutation Strategies Reference](artifact/references/mutation_strategies.md) <br>
- [README](artifact/README.md) <br>
- [SKILL](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown progress summaries, checklists, test cases, diffs or edited text, and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs up to 100 iterative rounds in 30-round batches, pausing for user review between batches.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
