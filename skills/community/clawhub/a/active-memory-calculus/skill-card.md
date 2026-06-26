## Description: <br>
Automatically remembers and analyzes calculus students' learning preferences, concept mastery, and error patterns to adapt tutoring and generate learning summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daigxok](https://clawhub.ai/user/daigxok) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Educators, tutors, and learning-agent developers use this skill to personalize higher-mathematics tutoring by tracking student preferences, concept mastery, recurring mistakes, and learning gaps. It can also generate session summaries, knowledge graph updates, and recommendations for follow-up study. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically profiles student learning behavior and can persist profiles, memories, transcripts, dream summaries, and knowledge graphs. <br>
Mitigation: Use it only with student consent, store data in a protected CALCULUS_MEMORY_PATH, and define inspection, correction, deletion, and retention procedures before deployment. <br>
Risk: Transcript persistence and dream generation can store sensitive learning interactions beyond the immediate tutoring session. <br>
Mitigation: Disable transcript persistence or dreaming when they are not needed, minimize retained data, and restrict access to the storage directory. <br>
Risk: Personalized warnings and study recommendations may be based on incomplete or incorrect memory extraction. <br>
Mitigation: Review generated summaries and recommendations before using them for high-stakes tutoring decisions, and allow students or educators to correct saved profiles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daigxok/active-memory-calculus) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Quickstart](artifact/QUICKSTART.md) <br>
- [System prompt](artifact/prompts/system.md) <br>
- [Basic usage example](artifact/examples/example_basic_usage.md) <br>
- [Integration example](artifact/examples/example_integration.md) <br>
- [Dream output example](artifact/examples/example_dream_output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON records, configuration snippets, Python API examples, and agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write student profiles, recent memories, dream summaries, and knowledge graph files under the configured CALCULUS_MEMORY_PATH.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact metadata lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
