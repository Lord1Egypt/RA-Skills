## Description:

Enrich Bear research notes tagged "待整理" with thematic GIFs by extracting note topics, searching GIFs, appending matching GIF links, and retagging processed notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to batch enrich draft Bear research notes tagged "待整理" with topical GIF links and move completed notes to the "已整理" tag.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically reads and edits private Bear notes tagged "待整理".

Mitigation: Back up notes first, run it only on non-sensitive notes, and review the script before execution.

Risk: Note-derived keywords are sent to Giphy when GIFs are searched.

Mitigation: Use the skill only when sharing those keywords with Giphy is acceptable.

Risk: The workflow can append remote GIF links and retag notes without a preview step.

Mitigation: Test on a small set of notes and inspect results before applying it broadly.

Risk: The documented prerequisite installs the grizzly dependency at latest.

Mitigation: Pin and review the grizzly dependency version before running the batch script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/bear-research-enricher)
- [Giphy search API endpoint](https://api.giphy.com/v1/gifs/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and a completion summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append remote GIF image links to local Bear notes and retag processed notes.]

## Skill Version(s):

0.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
