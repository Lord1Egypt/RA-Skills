## Description: <br>
Ingests user-provided media links or files, asks for intent when needed, and saves a structured note in a personal Obsidian library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EaRu723](https://clawhub.ai/user/EaRu723) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn URLs or files into concise, tagged Obsidian notes that preserve source metadata, key ideas, structure, emotional register, and intended follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided links or files may be persisted into local Obsidian notes, including source URLs, filenames, summaries, and inferred intent. <br>
Mitigation: Use the skill only with content that is acceptable to save locally, and review generated library notes before sharing or syncing the workspace. <br>
Risk: X post handling uses the FxTwitter third-party service for tweet retrieval. <br>
Mitigation: Avoid private, sensitive, or confidential X links unless third-party retrieval is acceptable for the use case. <br>
Risk: Fetched content may be incomplete for sources such as YouTube videos without transcripts, paywalled articles, or podcast audio. <br>
Mitigation: Treat generated notes as summaries of available source material and provide transcripts or pasted content when deeper analysis is required. <br>


## Reference(s): <br>
- [Media Type Fetch Strategies](references/media-types.md) <br>
- [ClawHub skill page](https://clawhub.ai/EaRu723/digital-librarian) <br>
- [Publisher profile](https://clawhub.ai/user/EaRu723) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown Obsidian note plus a brief text confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local notes under library/YYYY-MM-DD-[slug].md and may include source URLs or filenames.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
