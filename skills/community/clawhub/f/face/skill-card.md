## Description: <br>
Put a human face on your agent with fast avatar shortlists, gender control, transparent options, and reusable profile links. Use when the user wants an avatar, profile face, or group image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to shortlist synthetic human-looking avatar faces, present a small set of options for approval, and reuse the approved detail link for an agent, persona, group, or profile surface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make third-party web requests to Generated Photos when avatar-like prompts match. <br>
Mitigation: Limit requests to the disclosed Generated Photos endpoints and present fetched options to the user before any avatar is chosen or reused. <br>
Risk: A selected face link could be reused later as part of an agent or profile identity. <br>
Mitigation: Only save or reuse the chosen detail link after explicit user approval. <br>


## Reference(s): <br>
- [Face on ClawHub](https://clawhub.ai/ivangdavila/face) <br>
- [Generated Photos](https://generated.photos) <br>
- [Generated Photos Face Listing Pattern](https://generated.photos/faces/beautified/{gender}/young-adult) <br>
- [Generated Photos Image Endpoint](https://images.generated.photos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with numbered avatar options and preview, transparent image, and detail links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keeps selection under user control and recommends storing the detail page link rather than only an image preview URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
