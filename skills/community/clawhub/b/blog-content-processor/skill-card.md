## Description:

Process blog content to extract videos and generate GIF previews. Works with blogwatcher, video-frames, and gifgrep skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation users use this skill to process blog or RSS feeds, extract embedded video URLs, and generate GIF preview clips for downstream publishing or review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted RSS feeds or embedded videos may supply unsafe or misleading media inputs.

Mitigation: Use feeds and embedded videos from trusted sources and review extracted media before publishing or further processing.

Risk: Video and GIF processing can consume CPU and disk space.

Mitigation: Run the skill in a controlled environment and direct output to a monitored folder with appropriate storage limits.

Risk: Runtime dependencies may change behavior or introduce vulnerabilities if installed loosely.

Mitigation: Pin and review dependencies before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/blog-content-processor)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration]

**Output Format:** [GIF files and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written to a user-selected folder.]

## Skill Version(s):

10.0.0 (source: evidence.json release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
