## Description: <br>
Gejun Math Coach is a Chinese Gaokao math tutoring skill that uses Socratic questioning, seven tutoring scenarios, a Three-One reflection protocol, GO-ON variation strategies, and calculation checks to help students work through math problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abill6688](https://clawhub.ai/user/abill6688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students preparing for Chinese Gaokao mathematics and tutors supporting them use this skill for problem decomposition, full solutions, multiple methods, variations, general methods, error diagnosis, and Socratic guided practice. It can work from built-in seed problems or optional knowledge-base retrieval and includes a post-problem reflection loop to strengthen transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Important math answers or worked examples may be incorrect. <br>
Mitigation: Verify important answers independently and rely on the skill's calculation-checking workflow before using results for study decisions. <br>
Risk: The optional voice feature can run local TTS and playback commands for current tutoring text. <br>
Mitigation: Use the text-only mode unless the user is comfortable with the displayed local commands and the installed voice-coach dependency. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abill6688/gejun-math-coach) <br>
- [SKILL.md](SKILL.md) <br>
- [Three-One Reflection Protocol](references/reflection-protocol.md) <br>
- [Workflow Templates](references/workflow-templates.md) <br>
- [Scenario Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tutoring responses with worked math, Socratic questions, reflection prompts, checklists, and optional bash snippets for local voice playback.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only core behavior; optional knowledge-base IDs can extend retrieval, and optional voice playback depends on local voice-coach tooling.] <br>

## Skill Version(s): <br>
5.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
