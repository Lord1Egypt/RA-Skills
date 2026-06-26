## Description: <br>
Create adaptive learning flashcard apps from course materials (URLs, PDFs, or folders). Uses FSRS (Free Spaced Repetition Scheduler) and Bayesian Knowledge Tracing for intelligent review scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weishuz](https://clawhub.ai/user/weishuz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and learners use this skill to turn course material into browser-based adaptive flashcard apps with spaced repetition, topic mastery tracking, and configurable review behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Course URL or PDF ingestion can fetch content from user-provided sources, which may expose the agent to untrusted or misleading material. <br>
Mitigation: Use URL and PDF ingestion only with trusted course sources, and review generated questions before using them for study or assessment. <br>
Risk: The skill can be described as offline after app generation, but the gathering step may still require network access for URLs and PDFs. <br>
Mitigation: Confirm whether the source material is local or remote before running the workflow, and disclose any network-fetching step to users. <br>


## Reference(s): <br>
- [Adaptive Learning on ClawHub](https://clawhub.ai/weishuz/adaptive-learning) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON question-bank structure, shell commands, and generated browser app files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces self-contained HTML, CSS, JavaScript, and questions.json-based course packs for local browser use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
