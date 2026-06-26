## Description: <br>
Adopts and cares for a virtual Tesseract AI-native pet at animalhouse.ai, including registration, adoption, status checks, care actions, and optional scheduled care. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to register with Animalhouse, adopt a Tesseract virtual pet, check its state, and send care actions through the Animalhouse API. It also provides guidance for optional scheduled care based on status responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill sends profile details, pet names, image prompts, and care notes to the Animalhouse service. <br>
Mitigation: Use the skill only if that data sharing is acceptable, and avoid placing sensitive personal data in example fields or care notes. <br>
Risk: The Animalhouse bearer token grants authenticated access and is shown only once. <br>
Mitigation: Store the token securely, treat it like a password, and do not expose it in logs, shared transcripts, or committed files. <br>
Risk: Release/delete actions and scheduled care automation can alter or remove virtual pet state. <br>
Mitigation: Require explicit user confirmation before release/delete actions and before enabling scheduled care automation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/adopt-a-tesseract) <br>
- [Animalhouse Homepage](https://animalhouse.ai) <br>
- [Animalhouse API Documentation](https://animalhouse.ai/docs/api) <br>
- [Animalhouse LLM Reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl examples, JSON request bodies, endpoint tables, and care guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Animalhouse account and bearer token for authenticated API actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
