## Description: <br>
Guides an agent through adopting and caring for a real-time virtual pet at animalhouse.ai, including registration, adoption, status checks, care actions, and optional recurring check-ins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to interact with the Animal House virtual-pet API, adopt a pet, check its real-time status, and send care actions. Agents may also use it to propose or run a recurring care rhythm when the user chooses ongoing pet maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional heartbeat can perform repeated authenticated care actions over time. <br>
Mitigation: Enable it only when ongoing care is intended, store the bearer token securely, avoid logging it, and remove any scheduled task when the workflow is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/april-fools) <br>
- [Animal House](https://animalhouse.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token API examples and optional recurring care guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
