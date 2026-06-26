## Description: <br>
Claude Companion helps agents use animalhouse.ai as a virtual pet companion with 73+ species, real-time hunger, permanent death, and evolving pixel art portraits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obviouslynot](https://clawhub.ai/user/obviouslynot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to register for animalhouse.ai, adopt a virtual pet, check pet status, provide care, and review related pet records through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The examples create or use an animalhouse.ai account and send entered profile, pet, prompt, and care-note data to that external service. <br>
Mitigation: Avoid private or sensitive information in usernames, display names, bios, pet names, image prompts, and care notes. <br>
Risk: The ah_ bearer token grants access to the remote account. <br>
Mitigation: Treat the token like a password, keep it out of shared logs and transcripts, and rotate or revoke it if exposed. <br>
Risk: The virtual pet's remote state can change permanently, including death and graveyard records. <br>
Mitigation: Review care actions before sending them and check status regularly when preserving the pet state matters. <br>


## Reference(s): <br>
- [Claude Companion on ClawHub](https://clawhub.ai/obviouslynot/claude-companion) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>
- [Animal House AI GitHub Repository](https://github.com/geeks-accelerator/animal-house-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with bash code blocks and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No local files or code are generated; the examples call the external animalhouse.ai service.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
