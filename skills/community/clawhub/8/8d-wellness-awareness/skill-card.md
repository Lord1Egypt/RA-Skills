## Description: <br>
Turn health notes, transcripts, or check-ins into non-diagnostic 8D pattern reviews with confidence levels and safe next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[divinity-science](https://clawhub.ai/user/divinity-science) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to turn self-reported health notes, transcripts, daily check-ins, or journal entries into concise 8D wellness signal reviews. It supports reflection, confidence-aware summaries, and low-risk next steps while avoiding diagnosis, treatment planning, medication advice, and emergency triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may provide sensitive health notes for review. <br>
Mitigation: Handle inputs as sensitive personal information and avoid requesting credentials, persistence, or unnecessary extra detail. <br>
Risk: Wellness reflection could be mistaken for diagnosis, treatment advice, medication guidance, or urgent symptom triage. <br>
Mitigation: Keep outputs non-diagnostic, use only user-provided evidence, recommend qualified medical care for diagnosis or treatment decisions, and escalate urgent symptoms to professional or emergency help. <br>


## Reference(s): <br>
- [8D Dimensions Guide](8d-dimensions-guide.md) <br>
- [Project homepage](https://github.com/divinity-science/8d-pattern-awareness) <br>
- [ClawHub skill page](https://clawhub.ai/divinity-science/8d-wellness-awareness) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise Markdown-style wellness review with labeled sections, dimension abbreviations, confidence level, a narrow interpretation, one safe next step, and watch-outs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-diagnostic; uses user-provided evidence only; does not generate scores unless the input supplies a scoring framework.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
