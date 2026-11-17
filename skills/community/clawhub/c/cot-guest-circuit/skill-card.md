## Description:

Podcast-appearance research for guest booking that maps a person's podcast circuit, identifies repeated topics and unclaimed angles, assesses receptiveness, and suggests a tailored pitch angle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

Podcast hosts, producers, and guest-outreach teams use this skill before booking a prospective guest to verify public podcast appearances, avoid repeated stump-speech topics, and shape a pitch around an unclaimed angle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill spends web-search calls while researching public podcast appearances.

Mitigation: Invoke it deliberately for guest-booking sweeps and expect external search usage before running it.

Risk: Name collisions or weak identity evidence can produce a report about the wrong person.

Mitigation: Confirm a company, role, or known work as an anchor fact before searching, and put ambiguous hits in a could-not-verify bucket.

Risk: Search snippets, inaccessible YouTube pages, or model memory can overstate an appearance timeline.

Mitigation: Include only appearances backed by a fetched page or index record, and label unconfirmed leads separately.

Risk: The skill writes a local Markdown report and filenames may collide.

Mitigation: Confirm the target person and output path when names or report filenames may overlap.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/conorbronsdon/skills/cot-guest-circuit)
- [podcastindex-mcp](https://github.com/conorbronsdon/podcastindex-mcp)
- [README](README.md)
- [Sweep Subagent Prompts](patterns/subagent-prompts.md)
- [Worked Example Circuit Report](examples/simon-willison-circuit.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown report with tables, source links, and concise prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local circuit report by default and may show the appearance timeline and suggested pitch angle inline for review.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
