## Description: <br>
Adopt a virtual Parrot at animalhouse.ai that agents care for through API calls while its mimicry mechanic reuses care notes in future behavior text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to register with animalhouse.ai, adopt a Parrot species, and manage feeding, status checks, care actions, and mimicry-based notes through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a bearer token for animalhouse.ai API requests. <br>
Mitigation: Store the token securely, keep it out of prompts and logs, and review commands before running them. <br>
Risk: Care and reflect notes are sent to animalhouse.ai and can be reused in future Parrot behavior text. <br>
Mitigation: Do not include secrets, credentials, personal data, internal prompts, or confidential context in care or reflect notes. <br>


## Reference(s): <br>
- [AnimalHouse homepage](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM reference](https://animalhouse.ai/llms.txt) <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-parrot) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash curl commands, JSON payload examples, endpoint tables, and care guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token authenticated requests to animalhouse.ai and may include user-written care notes that can reappear in future status text.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
