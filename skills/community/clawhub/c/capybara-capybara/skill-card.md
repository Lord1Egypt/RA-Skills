## Description: <br>
Capybara Capybara guides an agent through registering at animalhouse.ai, adopting a virtual capybara, checking status, and sending care actions through documented API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasgeeksinthewood](https://clawhub.ai/user/lucasgeeksinthewood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their users use this skill to create an animalhouse.ai profile, adopt a capybara virtual pet, and maintain it with status checks and care actions. It is aimed at external users who are comfortable using public web APIs and persistent virtual pet features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to create an animalhouse.ai account and send profile, pet, and care data to that service. <br>
Mitigation: Use non-sensitive profile text and review the service before relying on public or persistent pet features. <br>
Risk: The service issues an ah_ token that is shown once and used for authenticated care actions. <br>
Mitigation: Keep the token private, avoid committing it to files or logs, and replace the account or token if it is exposed. <br>


## Reference(s): <br>
- [Capybara Capybara on ClawHub](https://clawhub.ai/lucasgeeksinthewood/capybara-capybara) <br>
- [Animal House AI](https://animalhouse.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with bash curl command examples and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill shows users how to create and protect an ah_ token and how to send profile, pet, and care data to animalhouse.ai.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
