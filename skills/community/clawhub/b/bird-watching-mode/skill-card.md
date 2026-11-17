## Description:

Bird Watching Mode helps an agent initialize a local birding session, resolve an eBird region, record text or photo-based bird sightings, and export the sighting log as CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoshino-s](https://clawhub.ai/user/yoshino-s)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to keep a local bird-watching log, add sightings from field notes or BirdID photo identification, and export observations or per-species summaries for review or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local birding log can contain place, time, species, notes, image paths, and raw BirdID output.

Mitigation: Use the skill only in workspaces where that local data is acceptable, and avoid sharing the log unless those fields have been reviewed.

Risk: CSV exports can expose the same sighting and location details when attached, emailed, or opened in spreadsheets.

Mitigation: Review generated CSV files before sharing them and remove fields that should not leave the workspace.

Risk: Photo identification relies on a separate SuperPicky CLI and BirdID setup.

Mitigation: Install and trust that dependency separately, and confirm uncertain species suggestions before recording them.

## Reference(s):

- [Bird log schema](scripts/bird_log_schema.md)
- [ClawHub skill page](https://clawhub.ai/yoshino-s/skills/bird-watching-mode)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, CSV files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus workspace JSON and optional CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes workspace/bird.json and optional CSV exports; photo identification depends on the separate SuperPicky CLI and BirdID components.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
