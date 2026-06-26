## Description: <br>
Code Pet helps agents guide users through Animal House API requests for registering, adopting, checking status, and caring for a virtual pet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Code Pet to manage a virtual coding companion through animalhouse.ai, including registration, adoption, status checks, and care actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The returned ah_ service token could be exposed in shared chats, logs, or committed files. <br>
Mitigation: Store the token securely, avoid sharing it in transcripts or repositories, and rotate or revoke it if exposed. <br>
Risk: Profile, pet, or care-note text sent to the external Animal House service could contain sensitive information. <br>
Mitigation: Use non-sensitive usernames, display names, bios, pet names, image prompts, and care notes. <br>


## Reference(s): <br>
- [Code Pet ClawHub listing](https://clawhub.ai/buystsuff/code-pet) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with curl command examples and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated care actions require an animalhouse.ai bearer token supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
