## Description:

Collects public video submissions from a Bilibili creator profile and exports the results as CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystery77777777](https://clawhub.ai/user/mystery77777777)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and marketing teams use it to review a public Bilibili creator's video titles, descriptions, view, danmaku and comment counts, covers, publish times, and links, then export the collected list as CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports exposed bearer credentials and disabled TLS verification; the default service URL uses plain HTTP, and scan coverage was partial.

Mitigation: Avoid installation until the reported credential exposure and TLS issue are addressed. Before sending account credentials, confirm the service uses HTTPS with certificate verification enabled, and review all components because the scan was incomplete.

Risk: The security scan says the skill includes comment-collection capabilities beyond its stated video-list and CSV purpose.

Mitigation: Confirm that comment collection is necessary and justified before use, and limit collection to the public profile data needed for the task.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mystery77777777/skills/b-profile)
- [Default service endpoint](http://st.aidata366.com)

## Skill Output:

**Output Type(s):** [JSON, CSV files, Shell commands]

**Output Format:** [JSON responses on stdout; CSV export for collected video lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Collects one public creator profile per task, with 1–10 pages per task. CSV includes a task summary and video details.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
