## Description: <br>
Helps agents adopt and care for a virtual Easter Bunny at animalhouse.ai while documenting the account, adoption, status, and care API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users can use this skill to register for animalhouse.ai, adopt an Easter Bunny, check its status, and issue care actions through documented API requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users or agents to create or use an animalhouse.ai account and handle an ah_ bearer token. <br>
Mitigation: Treat the token like a password, keep it out of shared logs and chats, and rotate or discard it if exposed. <br>
Risk: Recurring care automation may repeatedly call animalhouse.ai APIs or take actions the user did not review. <br>
Mitigation: Review proposed schedules and API requests before allowing an agent to run repeated care actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liveneon/easter-egg) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [Animal House creatures](https://animalhouse.ai/creatures) <br>
- [Animal House graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and API endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes account registration, bearer-token API calls, recurring care guidance, and hidden preference examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
