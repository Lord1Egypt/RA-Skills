## Description:

Use when a bike might be stolen (locking up in a city, buying a lock) or HAS been stolen. Grades lock setups against theft-area risk, builds a serial/photo registry BEFORE theft, and prints the first-72-hours stolen-bike playbook: police report, registry flags, marketplace sting searches, insurance claim.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT-0

## Use Case:

Cyclists, city commuters, and used-bike buyers use this skill to assess bike-lock setups, prepare a local serial and photo registry, and follow a theft-response checklist. It also provides guidance for checking a used bike's serial and documenting insurance claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local registry can contain bike serial numbers, value, and identifying details. Sharing serials or other personal information through external registries or community posts can affect privacy.

Mitigation: Keep the local registry in a private location and share only the details needed for a registry listing or recovery post.

Risk: The registration workflow writes a local JSON file, and the scanner did not verify the script's runtime file-writing permissions.

Mitigation: Review the registry path and contents, and run the skill where creating or updating that file is expected.

Risk: The skill includes an additional used-bike serial check workflow.

Mitigation: Review the check workflow before use and choose deliberately whether to look up a serial with external registries.

## Reference(s):

- [Bike Theft Field Guide](references/bike-theft-field-guide.md)
- [BikeIndex](https://bikeindex.org/)
- [ClawHub release page](https://clawhub.ai/voronindenis5/skills/bike-theft-shield)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Terminal text and a local JSON bike registry]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The registry is stored locally as JSON; command output includes checklists, lock assessments, and theft-response steps.]

## Skill Version(s):

1.0.0 (source: frontmatter; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
