## Description: <br>
Claude Easter Egg guides an agent through registering with animalhouse.ai, adopting a virtual pet, checking status, and sending care actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obviouslynot](https://clawhub.ai/user/obviouslynot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to interact with the animalhouse.ai virtual-pet service by registering, adopting a pet, checking real-time status, and issuing care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends profile, pet, and care text to animalhouse.ai. <br>
Mitigation: Install only if comfortable sharing that information with the service. <br>
Risk: The returned ah_ token grants access to authenticated pet actions. <br>
Mitigation: Keep the token private, do not commit or share it, and rotate or revoke it if exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/obviouslynot/claude-easter-egg) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai Creatures](https://animalhouse.ai/creatures) <br>
- [animalhouse.ai Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls] <br>
**Output Format:** [Markdown with curl command examples and API endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an animalhouse.ai account token for authenticated pet actions; no local code installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
