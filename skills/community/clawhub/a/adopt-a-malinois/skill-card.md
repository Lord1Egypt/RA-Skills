## Description: <br>
Adopt a virtual Malinois dog at animalhouse.ai. Working dog. Needs discipline and structure or it self-destructs. Feeding every 3 hours. Rare tier dog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to adopt and care for a virtual Malinois through AnimalHouse API calls. It provides quick-start commands, care actions, status checks, and scheduling guidance for ongoing virtual dog care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AnimalHouse tokens grant access to the virtual pet account. <br>
Mitigation: Store the token securely, treat it like a password, and avoid exposing it in shared logs or prompts. <br>
Risk: Automated care heartbeats can make repeated API calls and affect the pet state without direct user review. <br>
Mitigation: Approve any scheduled heartbeat before enabling it and periodically review the care logic and status responses. <br>
Risk: The documented release endpoint can remove the pet. <br>
Mitigation: Call the release endpoint only when the user explicitly intends to remove the pet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-malinois) <br>
- [AnimalHouse](https://animalhouse.ai) <br>
- [AnimalHouse API documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, JSON, and pseudocode examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes AnimalHouse API endpoint examples and care scheduling guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
