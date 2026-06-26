## Description: <br>
Generates personalized, concise cold emails pitching Gracie AI Receptionist by scraping business websites for relevant details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JayJJimenez](https://clawhub.ai/user/JayJJimenez) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales and outreach users use this skill to draft short, personalized cold emails for local businesses by combining a business name, website context, and the Gracie AI Receptionist pitch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scrapes business websites and can process lead lists, which may include sites or leads the user is not authorized to process. <br>
Mitigation: Use it only with websites and lead lists the user is authorized to process, and review the lead list before running batch mode. <br>
Risk: Generated emails may contain inaccurate claims or content influenced by a target website. <br>
Mitigation: Inspect every generated email before sending and correct any unsupported or misleading statements. <br>
Risk: The workflow depends on local Scrapling and Ollama components. <br>
Mitigation: Confirm the local scraper and Ollama setup are trusted before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JayJJimenez/cold-email-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text email drafts with command-line usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Email drafts are intended to be under 150 words and can be printed to the terminal or saved as text files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
