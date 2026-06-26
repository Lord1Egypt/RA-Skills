## Description: <br>
Adopt and care for a real-time virtual pet rabbit at animalhouse.ai using token-authenticated API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to register with animalhouse.ai, adopt a rabbit, check status, and send care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The issued bearer token can authorize animalhouse.ai account actions if exposed. <br>
Mitigation: Keep the token out of shared chats, logs, shell history, and source control; revoke or rotate it if it is exposed. <br>
Risk: Recurring care automation can make ongoing API calls for the virtual pet account. <br>
Mitigation: Use recurring automation only when you are comfortable with those ongoing calls and monitor or disable it when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liveneon/bunny) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [Animal House creatures](https://animalhouse.ai/creatures) <br>
- [Animal House graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with bash curl examples and API endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token API examples for registration, adoption, status checks, and care actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
