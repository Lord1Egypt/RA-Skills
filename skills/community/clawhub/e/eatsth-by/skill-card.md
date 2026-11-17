## Description:

Personal health diet assistant that records and queries health and food inventory information, generates personalized dietary recommendations based on health status, prioritizes available foods, marks ingredients already in inventory, and reminds the user about items nearing expiration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biyaoshang](https://clawhub.ai/user/biyaoshang)

### License/Terms of Use:


## Use Case:

External users use this skill to maintain personal health and food inventory notes and receive diet recommendations that account for symptoms, restrictions, dislikes, habits, available foods, and expiration dates. Health-record features are intended for direct personal sessions only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive personal health details in plain local Markdown files.

Mitigation: Add explicit consent, review, correction, deletion, and protected-storage rules before collecting or retaining health records.

Risk: Diet recommendations may be based on incomplete or outdated health and food inventory records.

Mitigation: Ask users to confirm current health constraints and inventory status before relying on recommendations, and present recommendations as informational rather than medical advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biyaoshang/skills/eatsth-by)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain-language responses and Markdown record updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown files for health and food inventory records.]

## Skill Version(s):

1.0.3 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
