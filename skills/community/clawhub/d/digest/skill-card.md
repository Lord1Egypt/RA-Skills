## Description: <br>
Curate external information into personalized updates. Auto-learns format, timing, sources, and depth preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use Digest to curate news, industry updates, trends, competitors, and other external information into personalized updates that adapt to their preferred sources, timing, format, and depth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unapproved sources or delivery channels could expose personalized interests or send digests to unintended recipients. <br>
Mitigation: Confirm allowed sources and delivery channels before installation, especially for group chats or email. <br>
Risk: The preference file can accumulate inferred interests, schedules, source trust, and format preferences over time. <br>
Mitigation: Periodically review preferences.md and remove or correct preferences that should not be retained. <br>


## Reference(s): <br>
- [Digest Dimensions](dimensions.md) <br>
- [Digest Preferences](preferences.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Personalized digest in Markdown or the user's learned preferred delivery format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update preference guidance after observing user feedback and delivery signals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
