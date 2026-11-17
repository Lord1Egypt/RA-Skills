## Description:

Bilibili Up Master helps creators monitor Bilibili trends, analyze creator and video metrics, compare peer accounts, and generate content planning reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Bilibili creators, channel operators, and social-media analysts use this skill to track platform trends, analyze account or video performance, compare peers, and turn those signals into daily or weekly content operations guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the Python code weakens HTTPS certificate verification for the whole Python process.

Mitigation: Keep normal HTTPS certificate verification enabled before use and review any network access that collects Bilibili data.

Risk: The security evidence identifies unsafe local file helpers, and the artifact writes cache and report files under /tmp/bilibili-data/.

Mitigation: Constrain local filenames and paths, store only non-sensitive analytics data, and review generated files before sharing them.

Risk: The security guidance warns against unintended use of logged-in Bilibili sessions or creator publishing workflows.

Mitigation: Use least-privilege browsing sessions for analytics and avoid logged-in creator or publishing sessions unless that access is explicitly intended.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/onlyloveher/skills/bilibili-up-master)
- [Publisher profile](https://clawhub.ai/user/onlyloveher)
- [Bilibili ranking page](https://www.bilibili.com/ranking)
- [Bilibili ranking API endpoint](https://api.bilibili.com/x/web-interface/ranking/v2)
- [Bilibili user card API endpoint](https://api.bilibili.com/x/web-interface/card)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown reports, JSON analysis summaries, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save reports and cached analysis data under /tmp/bilibili-data/.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml; artifact _meta.json lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
