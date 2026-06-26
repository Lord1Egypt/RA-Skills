## Description: <br>
Adopt a virtual Bengal cat at animalhouse.ai. Athletic, intense. Needs play more than food. Bored easily. Feeding every 3 hours. Rare tier cat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register with animalhouse.ai, adopt a Bengal virtual cat, check its real-time status, and issue care actions through the AnimalHouse API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AnimalHouse API care actions require a bearer token that could be exposed if copied into logs, prompts, or shared notes. <br>
Mitigation: Keep the token private, store it securely, and use non-sensitive profile text and care notes. <br>
Risk: The skill documents release/delete behavior that can remove or alter a virtual pet state. <br>
Mitigation: Require explicit user confirmation before any release or delete action. <br>


## Reference(s): <br>
- [AnimalHouse](https://animalhouse.ai) <br>
- [AnimalHouse API Documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM Reference](https://animalhouse.ai/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-bengal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with curl examples, JSON request bodies, endpoint tables, and care guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent through AnimalHouse registration, adoption, status checks, care actions, scheduling suggestions, and release/delete caution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
