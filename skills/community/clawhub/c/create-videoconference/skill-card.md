## Description: <br>
Creates Meetling video conference links for instant or scheduled calls, with share payloads for instant calls and email invite templates for scheduled calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bavxhack](https://clawhub.ai/user/bavxhack) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external collaborators, and agents use this skill to prepare secure Meetling invite links, recipient share payloads, and scheduled email invite text for video conferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads ./contacts.json from the current workspace to resolve recipients. <br>
Mitigation: Keep contacts.json trusted, minimal, and scoped to intended recipients before running the skill. <br>
Risk: Generated links, messages, and resolved recipients could be shared with unintended recipients if not reviewed. <br>
Mitigation: Review the Meetling URL, message text, resolved recipients, and unresolved recipients before using any sending path. <br>
Risk: Scheduled output does not create a Meetling dashboard meeting or Meetling-sent invitations. <br>
Mitigation: Use the generated /m link and email invite template, or create any dashboard-managed meeting separately when required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bavxhack/create-videoconference) <br>
- [Meetling application](https://app.meetling.de) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON containing a Meetling URL, share message, resolved and unresolved recipients, and scheduled email invite details when applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instant calls return a share payload for default sending; scheduled calls return an email invite template and limitations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter and package.json show 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
