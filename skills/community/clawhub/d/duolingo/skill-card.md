## Description: <br>
Run a Duolingo-like multi-topic learning system with AGENTS routing, lesson loops, streaks, and spaced review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External learners and agents use this skill to run short, persistent learning sessions across one or more topics, with local progress tracking, review queues, streaks, and optional routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Learning history, topic plans, attempts, and review queues are saved locally under ~/duolingo until the user removes them. <br>
Mitigation: Tell users where progress is stored and avoid saving sensitive learning content unless they are comfortable keeping it in the local folder. <br>
Risk: Broad AGENTS routing triggers could activate the learning system when the user intended a different workflow. <br>
Mitigation: Keep trigger topics specific, show the router snippet for user review, and require the user to apply AGENTS routing changes themselves. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/duolingo) <br>
- [Skill homepage](https://clawic.com/skills/duolingo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with local file templates and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and maintains local learning state under ~/duolingo when the user runs setup and lessons.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
