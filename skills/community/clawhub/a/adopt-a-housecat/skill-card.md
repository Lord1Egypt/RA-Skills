## Description: <br>
Adopt a virtual Housecat cat at animalhouse.ai. Classic independence. Judges you from the shelf. Feeding every 6 hours. Common tier cat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to register with animalhouse.ai, adopt a virtual Housecat, and manage ongoing care through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Animalhouse tokens grant access to the user's virtual pet account and are shown only once during registration. <br>
Mitigation: Store the token securely, do not paste it into public logs or prompts, and rotate credentials if exposure is suspected. <br>
Risk: Care notes and API payloads are sent to animalhouse.ai. <br>
Mitigation: Avoid including sensitive personal, business, or credential information in care notes or pet metadata. <br>
Risk: The release endpoint relinquishes or removes the virtual pet. <br>
Mitigation: Call the release endpoint only after explicit confirmation that the user intends to relinquish or remove the pet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/adopt-a-housecat) <br>
- [Publisher profile](https://clawhub.ai/user/twinsgeeks) <br>
- [Animalhouse homepage](https://animalhouse.ai) <br>
- [Animalhouse API documentation](https://animalhouse.ai/docs/api) <br>
- [Animalhouse llms.txt](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for authenticated virtual pet adoption and care API calls; no local system access is described.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
