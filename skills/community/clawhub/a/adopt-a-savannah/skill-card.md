## Description: <br>
Adopt a virtual Savannah cat at animalhouse.ai with a rare-tier care routine built around a four-hour feeding window, slow trust, and real-time status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to register with animalhouse.ai, adopt a virtual Savannah cat, and guide ongoing care through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens grant access to animalhouse.ai account actions if exposed. <br>
Mitigation: Store the token securely, avoid logging it, and pass it only in the Authorization header for intended API calls. <br>
Risk: The release/delete endpoint can remove a virtual pet account state. <br>
Mitigation: Require explicit user confirmation before any DELETE /api/house/release request. <br>
Risk: Scheduled care automation can repeatedly call external API endpoints without direct review. <br>
Mitigation: Review the proposed schedule and care actions before enabling automation, and keep automated calls limited to the documented care routine. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/twinsgeeks/adopt-a-savannah) <br>
- [AnimalHouse Homepage](https://animalhouse.ai) <br>
- [AnimalHouse API Documentation](https://animalhouse.ai/docs/api) <br>
- [AnimalHouse LLM Reference](https://animalhouse.ai/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides bearer-token API use for animalhouse.ai and does not generate local files by itself.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
