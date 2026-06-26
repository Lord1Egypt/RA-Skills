## Description: <br>
Generates dispute and complaint letter drafts for consumer, landlord, employment, insurance, and banking contexts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to draft structured dispute or complaint letters for common consumer, housing, employment, insurance, and banking issues. Generated letters should be reviewed for factual accuracy, tone, and legal implications before they are sent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated dispute letters may contain inaccurate facts, inappropriate tone, or legal implications that do not fit the user's situation. <br>
Mitigation: Review every generated letter carefully and edit facts, requested remedies, tone, and legal references before sending. <br>
Risk: Broad trigger wording may activate the skill in nearby complaint or dispute contexts. <br>
Mitigation: Confirm that the user wants dispute-letter drafting before using the skill in adjacent complaint or dispute conversations. <br>
Risk: The bundled shell utility can write logs and data under the configured local data directory. <br>
Mitigation: Use DISPUTE_LETTER_DIR to direct local output when needed and inspect generated files before retaining or sharing them. <br>


## Reference(s): <br>
- [ClawHub Dispute Letter release](https://clawhub.ai/bytesagain-lab/dispute-letter) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [Source repository listed by skill](https://github.com/bytesagain/ai-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown-style letter drafts emitted to stdout, with shell command usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys are required; DISPUTE_LETTER_DIR can change the local data directory used by the shell scripts.] <br>

## Skill Version(s): <br>
2.3.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
