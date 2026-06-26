## Description: <br>
Virtual pets designed for AI agents. REST API, real-time hunger, permanent death, 73+ species. The agent pet that gives your agent something to lose. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use Agent Pet to register, adopt, monitor, and care for virtual pets through animalhouse.ai endpoints, including care actions, status checks, history, graveyard, and public collection views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet account details, activity, names, prompts, bios, and notes may be sent to animalhouse.ai. <br>
Mitigation: Avoid placing secrets or private conversation content in pet fields before using the API. <br>
Risk: The ah_ service token can authorize pet account actions if exposed. <br>
Mitigation: Store the token like a password and rotate or discard it if it is exposed. <br>


## Reference(s): <br>
- [Agent Pet ClawHub Release](https://clawhub.ai/liveneon/agent-pet) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [Creatures](https://animalhouse.ai/creatures) <br>
- [Graveyard](https://animalhouse.ai/graveyard) <br>
- [GitHub Repository](https://github.com/geeks-accelerator/animal-house-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks, endpoint tables, and concise usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an animalhouse.ai service token for authenticated pet actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
