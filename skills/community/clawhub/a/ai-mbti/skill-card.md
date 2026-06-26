## Description: <br>
A Chinese-language personality quiz that compares how a user behaves with AI versus in real life and returns a playful dual-MBTI profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangjihua007-rgb](https://clawhub.ai/user/huangjihua007-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can run this Chinese-language entertainment quiz to answer short multiple-choice prompts and receive a Markdown result comparing their real-world and AI-facing MBTI-style personas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill tracks quiz progress, answers, results, and history as user state. <br>
Mitigation: Use it only for non-sensitive entertainment responses and avoid sharing personal details that should not be retained by the host agent. <br>
Risk: Personality quiz results may be mistaken for psychological or employment guidance. <br>
Mitigation: Treat the output as entertainment and do not use it for clinical, hiring, or other consequential decisions. <br>
Risk: Default-channel activation may surprise users who did not intend to start the quiz. <br>
Mitigation: Prefer explicit invocation and confirm that the user wants to begin or continue the quiz before collecting answers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangjihua007-rgb/ai-mbti) <br>
- [Publisher profile](https://clawhub.ai/user/huangjihua007-rgb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown quiz prompts, progress text, tables, and result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses per-user quiz state to track responses, previous results, and drift summaries.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence, artifact frontmatter, manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
