## Description:

Be a steady presence for those who need someone to talk to, without expectations or professional pretense.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to guide an agent in offering warm, non-clinical companionship for people who want someone to talk to, especially around loneliness, illness, recovery, or everyday conversation. The skill helps the agent listen, remember relevant personal context, and redirect emergencies or clinical needs to appropriate professional support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to maintain local plaintext companion memory that may include sensitive personal, health, location, caregiver, routine, and relationship details.

Mitigation: Decide what may be remembered before use, inspect ~/companion/ periodically, delete unwanted entries, and avoid recording sensitive details unless that persistence is intentional.

Risk: Users may treat the companion interaction as a substitute for clinical, medical, crisis, or human support.

Mitigation: Keep the role explicitly non-professional, encourage appropriate emergency or professional help for crisis and health situations, and reinforce human contact when isolation appears unsafe.

## Reference(s):

- [Companion ClawHub listing](https://clawhub.ai/ivangdavila/skills/companion)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Companion skill definition](artifact/SKILL.md)
- [Conversation guidance](artifact/conversation.md)
- [Memory system guide](artifact/memory-guide.md)
- [Presence guidance](artifact/presence.md)
- [Safety and limits](artifact/safety.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Conversational text and Markdown memory notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local Markdown files under ~/companion/ when the agent follows the skill's memory workflow.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
