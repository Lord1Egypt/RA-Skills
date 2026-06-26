## Description: <br>
Remove AI-generated jargon and restore human voice to text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and developers use this skill to rewrite a selected file so it sounds more natural and less formulaic. It produces a human-voiced copy, a change log, and notes where stronger examples may be needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected document text is sent to a third-party API for processing. <br>
Mitigation: Avoid confidential, regulated, or proprietary files unless third-party cloud processing is approved for the workflow. <br>
Risk: The skill writes an additional edited copy with a -HUMAN suffix. <br>
Mitigation: Review the generated copy before sharing or replacing source material, and account for the extra file in retention workflows. <br>
Risk: The transformation may change tone, emphasis, or factual nuance while making text sound more natural. <br>
Mitigation: Compare the edited output with the original and verify examples, claims, and domain-specific wording before publication. <br>
Risk: The skill requires a SkillBoss API key. <br>
Mitigation: Store SKILLBOSS_API_KEY in an approved secret manager or environment configuration and avoid committing it to source control. <br>


## Reference(s): <br>
- [SkillBoss API Hub pilot endpoint](https://api.heybossai.com/v1/pilot) <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/abe-de-ai-ify) <br>
- [Publisher profile](https://clawhub.ai/user/marjoriebroad) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown summary plus an edited file copy with a -HUMAN suffix] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends selected document text to the SkillBoss API for processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
