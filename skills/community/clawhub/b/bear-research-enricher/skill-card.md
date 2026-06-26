## Description: <br>
Enrich Bear research notes tagged 「待整理」 with thematic GIFs, then retag processed notes as 「已整理」. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Bear users and personal knowledge-management workflows use this skill to batch enrich draft research notes with topical GIF embeds and move completed notes from the 「待整理」 tag to 「已整理」. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can batch edit Bear notes selected by the 「待整理」 tag. <br>
Mitigation: Confirm that only intended notes carry the 「待整理」 tag and back up important notes before running the workflow. <br>
Risk: Extracted note topics or keywords may be sent to Giphy for GIF search. <br>
Mitigation: Avoid running the skill on sensitive notes, or remove confidential material from notes before enrichment. <br>
Risk: The skill requires access to Bear through a grizzly token. <br>
Mitigation: Store the token in the expected local token file, limit access to the host account, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/bear-research-enricher) <br>
- [Giphy Search API endpoint](https://api.giphy.com/v1/gifs/search) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, markdown, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and GIF image embeds] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append GIF markdown to matching Bear notes and reports processed notes.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
