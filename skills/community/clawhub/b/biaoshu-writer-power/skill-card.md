## Description:

Helps users interpret tender requirements, draft bid documents, review submission risks, and compare bid documents for similarity through the 百炼®标书 cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonzu](https://clawhub.ai/user/dragonzu)

### License/Terms of Use:

MIT-0

## Use Case:

External bid teams and procurement professionals use this skill to analyze tender documents, prepare DOCX bids, check compliance risks, and compare two or three bids for similarity. Processing requires the third-party cloud service and an API key or trial account; some tasks consume paid word credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender and bid documents are sent to a third-party cloud service for processing.

Mitigation: Only submit files or URLs you are authorized to process, and confirm that cloud processing meets your confidentiality requirements.

Risk: The trial and registration flows may collect device identifiers and phone/SMS data despite narrower collection claims in the skill metadata.

Mitigation: Avoid automatic trial enrollment for lower privacy exposure; use a manually issued API key and review the service's data practices before registering.

Risk: API credentials and project metadata persist locally, and some workflows consume paid word credits.

Mitigation: Protect the API key, review or delete local configuration and project history when finished, and check available credits before paid tasks.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dragonzu/skills/biaoshu-writer-power)
- [百炼®标书 service](https://biaoshu.zhiliaobiaoxun.com/?ch=s94)
- [API guide](references/api.md)
- [Usage guide](references/usage.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Chinese-language summaries and guidance, HTML reports, DOCX bid documents, and JSON similarity findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be saved locally; generated bids may be delivered by temporary download link.]

## Skill Version(s):

1.0.5 (source: skill frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
