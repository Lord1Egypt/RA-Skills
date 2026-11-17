## Description:

Enrich Bear research notes tagged 「待整理」 with theme-matched GIFs for note cleanup workflows that use Bear, grizzly, and a GIF provider API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Bear users and automation agents use this skill to find notes tagged 「待整理」, append a topic-matched GIF, retag processed notes, and report enrichment failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and changes Bear notes tagged 「待整理」.

Mitigation: Review the matching tag scope before running the scripts and test on disposable notes or a backup first.

Risk: The scripts send note-derived titles or first lines to Tenor or Giphy.

Mitigation: Avoid using the skill on sensitive notes, or edit notes so the derived topic does not reveal private information.

Risk: Security evidence reports that the retagging behavior may create a new tagged note instead of tagging the original note as documented.

Mitigation: Review or fix the retagging script before use and verify the original note is updated as intended.

Risk: The skill depends on local Bear, grizzly, and GIF provider API credentials.

Mitigation: Use restricted API keys and consider pinning the grizzly version before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/bear-gif-enricher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can direct an agent to run local scripts that read and modify Bear notes and call Tenor or Giphy.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
