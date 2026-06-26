## Description: <br>
Business card scanner and Google Contacts manager that auto-detects business card images, extracts contact details with OCR, confirms the result with the user, and saves contacts with configurable name formatting and a card photo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[project820](https://clawhub.ai/user/project820) <br>

### License/Terms of Use: <br>
CC BY-NC 4.0 <br>


## Use Case: <br>
External users and operators use Bizcard to turn business card photos, especially Korean business cards, into reviewed Google Contacts entries with normalized names, phone numbers, organization fields, and an optional card image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business card images and extracted contact details may be sent through configured AI and API providers. <br>
Mitigation: Install only if that data flow is acceptable for the intended contacts, and review extracted fields before saving. <br>
Risk: The skill can modify Google Contacts after the user approves saving or updating a contact. <br>
Mitigation: Use the confirmation flow, review duplicate matches, and consider a dedicated Google Contacts and Telegram setup for business-card intake. <br>
Risk: API keys and relationship history are sensitive operational data. <br>
Mitigation: Keep MATON_API_KEY and NANO_BANANA_API_KEY private, and periodically clear or protect any local bizcard logs. <br>


## Reference(s): <br>
- [Bizcard ClawHub page](https://clawhub.ai/project820/bizcard) <br>
- [Google People API field reference](references/people-api-fields.md) <br>
- [Google People API: Person resource](https://developers.google.com/people/api/rest/v1/people) <br>
- [OpenClaw install documentation](https://docs.openclaw.ai/install) <br>
- [Maton settings](https://maton.ai/settings) <br>
- [Google AI Studio API keys](https://aistudio.google.com/app/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON contact fields and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewed contact data, configuration guidance, and execution steps for OCR, image processing, duplicate checks, and Google Contacts updates.] <br>

## Skill Version(s): <br>
0.1.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
