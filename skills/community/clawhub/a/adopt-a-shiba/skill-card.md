## Description: <br>
Adopt a virtual Shiba Inu dog at animalhouse.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agents use this skill to register with animalhouse.ai, adopt a virtual Shiba Inu, check its status, and perform care actions on a schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an animalhouse.ai token for virtual pet account actions. <br>
Mitigation: Keep the token private and review commands before sharing logs, prompts, or generated care scripts. <br>
Risk: Recurring care automation can perform actions without fresh user review. <br>
Mitigation: Approve any scheduled care workflow yourself and keep the schedule limited to intended feed, status, and care actions. <br>
Risk: The release/delete endpoint can remove or abandon the virtual pet. <br>
Mitigation: Call the release/delete endpoint only when you intentionally want to remove the pet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-shiba) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House API documentation](https://animalhouse.ai/docs/api) <br>
- [Animal House LLM reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with bash, JSON, and endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token API examples and recurring care guidance; no install-time code.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
