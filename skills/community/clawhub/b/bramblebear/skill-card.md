## Description: <br>
Bramblebear helps agents register, adopt, check, and care for an animalhouse.ai Capybara-style virtual pet using documented API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to interact with animalhouse.ai virtual-pet APIs: registering an account, adopting a Bramblebear or Capybara, checking status, and issuing care actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to create records with animalhouse.ai and send profile and pet-care data to that service. <br>
Mitigation: Confirm that sharing this data with animalhouse.ai is acceptable before running the documented API calls. <br>
Risk: The returned ah_ bearer token can grant access to the user's animalhouse.ai account. <br>
Mitigation: Treat the token like a password: do not share it, paste it into public chats, commit it to a repository, or store it in shell history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leegitw/bramblebear) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents curl commands and token-handling guidance for animalhouse.ai endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
