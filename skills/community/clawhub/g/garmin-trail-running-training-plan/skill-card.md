## Description:

Generates trail race roadmaps, dynamic training plans, and calendar sync guidance from Garmin activity data and race GPX tracks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtroymatt](https://clawhub.ai/user/mtroymatt)

### License/Terms of Use:

MIT-0

## Use Case:

Trail runners, coaches, and support teams use this skill to analyze Garmin activity data and race GPX tracks, produce race roadmaps, adjust taper training plans, and prepare calendar sync steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle Garmin credentials and local authentication tokens.

Mitigation: Use environment variables or an approved secrets store instead of committing credentials to config files, and restrict token storage permissions.

Risk: Garmin activity exports, GPX files, and generated reports can contain sensitive health and location history.

Mitigation: Store exports in protected locations, avoid sharing raw files publicly, and delete temporary files when analysis is complete.

Risk: Generated calendar sync code can write events to macOS Calendar.

Mitigation: Review generated scripts before execution, avoid untrusted race names or event text, and confirm calendar permissions are intentional.

## Reference(s):

- [Garmin Trail-Running Roadmap & Training Plan Standard](artifact/references/roadmap_standard.md)
- [ClawHub Skill Page](https://clawhub.ai/mtroymatt/skills/garmin-trail-running-training-plan)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with generated HTML, JSON data, Python or AppleScript snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local files containing Garmin activity exports, GPX-derived route data, HTML reports, and calendar sync scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
