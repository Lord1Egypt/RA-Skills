## Description: <br>
Virtual pets for Gemini agents using a model-agnostic REST API with adoption, care, status, history, graveyard, evolution, and pixel art pet features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to connect an agent to animalhouse.ai, register for an API token, adopt a virtual pet, check pet status, and send care actions through REST endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an animalhouse.ai bearer token for authenticated API calls; exposed tokens can allow unauthorized pet actions. <br>
Mitigation: Store the ah_ token in a password manager, secrets manager, or environment variable; avoid sharing it in public chats, logs, screenshots, or repositories; rotate or revoke it if exposed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/leegitw/gemini-pet) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House creatures](https://animalhouse.ai/creatures) <br>
- [Animal House graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with curl command examples and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an animalhouse.ai bearer token for authenticated pet actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
