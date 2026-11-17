## Description:

An interactive English reading coach that teaches and drills seven core reading strategies using level-appropriate ESL texts, guided practice, feedback, vocabulary work, and session summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cngvc](https://clawhub.ai/user/cngvc)

### License/Terms of Use:

MIT-0

## Use Case:

External English learners and exam-prep users use this skill to run structured reading-comprehension sessions, practice specific strategies, and receive guided feedback, vocabulary work, and follow-up challenges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad English-reading prompts and start an interactive tutoring flow when the user wanted a simpler answer.

Mitigation: Confirm the learner's goal and desired depth before starting a full session.

Risk: Scheduled drill framing may switch to Vietnamese when the agent thinks it is helpful.

Mitigation: Ask the learner to confirm the preferred instruction language and keep framing in that language.

Risk: Live source pages may be unavailable or unsuitable for the learner's level.

Mitigation: Use the documented fallback source order, show source URLs when available, and label original fallback passages as generated.

## Reference(s):

- [Strategy Teaching Guide](references/strategies.md)
- [Source Library](references/sources.md)
- [Linguapress](https://linguapress.com)
- [Breaking News English](https://breakingnewsenglish.com)
- [Listen A Minute](https://listenaminute.com)
- [Dream Reader](https://dreamreader.net)
- [Project Gutenberg](https://gutenberg.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-structured tutoring responses with reading passages, questions, feedback, vocabulary notes, and session summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source URLs and timed reading prompts; scheduled daily drills avoid markdown tables.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
