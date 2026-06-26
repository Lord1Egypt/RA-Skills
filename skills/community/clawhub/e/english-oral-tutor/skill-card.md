## Description: <br>
English Oral Tutor is an OpenClaw agent skill for structured 30-minute English speaking practice with B1 middle-school learners, including topic selection, grammar correction, vocabulary teaching, session timing, and continuity notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhiyicom](https://clawhub.ai/user/zhiyicom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners, tutors, and agent operators use this skill to run structured English oral-practice sessions for a B1 middle-school learner. It helps the agent lead timed conversations, rotate age-appropriate topics, correct grammar, introduce vocabulary, and maintain session history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores full tutoring conversations for a minor in local transcript and history files without clear consent, retention, deletion, or access-control rules. <br>
Mitigation: Define consent, retention, deletion, and access controls before deployment; for a minor, prefer opt-in summaries over verbatim logging. <br>
Risk: Hard-coded local paths can write sensitive lesson records into an unintended location or fail during installation. <br>
Mitigation: Replace local paths with deployment-specific paths and review storage locations before enabling the timing plugin or transcript workflow. <br>
Risk: The optional voice userscript uses microphone and browser speech features. <br>
Mitigation: Disclose microphone and voice-script behavior before sessions and require explicit opt-in. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhiyicom/english-oral-tutor) <br>
- [Share Bundle README](artifact/README.md) <br>
- [Skill Design](artifact/SKILL.md) <br>
- [Tutor Timing Plugin Manifest](artifact/plugin/tutor-timing/openclaw.plugin.json) <br>
- [Topic Library](artifact/topic-library/topic-library.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Conversational text, Markdown session records, shell commands, and JSON configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-stream tutoring responses with optional local voice input/output support.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
