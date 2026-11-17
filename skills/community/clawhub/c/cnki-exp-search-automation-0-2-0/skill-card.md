## Description:

Cnki Exp Search Automation helps agents use browser automation to run CNKI advanced searches, extract result lists, and collect article metadata and abstracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyingzhuangk](https://clawhub.ai/user/zhangyingzhuangk)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, developers, and agents use this skill to search CNKI, gather literature result lists, extract article metadata and abstracts, and export those results for academic review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a browser on CNKI and may rely on an existing browser profile or CNKI session.

Mitigation: Use an appropriate browser profile, keep manual control available for verification prompts, and avoid exposing unrelated session data.

Risk: Automated CNKI searches can trigger anti-robot verification or conflict with site access rules if run too quickly.

Mitigation: Use a headful browser when needed, complete verification manually, keep request rates reasonable, and follow CNKI's terms and access rules.

Risk: Extracted literature metadata can be saved locally.

Mitigation: Save exports only to approved locations and review generated JSON or CSV before sharing or reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangyingzhuangk/skills/cnki-exp-search-automation-0-2-0)
- [CNKI advanced search](https://kns.cnki.net/kns8s/AdvSearch?type=expert)
- [CNKI professional search fields](references/cnki-fields.md)
- [CNKI professional search query examples](references/query-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with browser-action examples, JavaScript snippets, and JSON or CSV data-shape examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local literature metadata exports when the agent follows the skill's file-writing guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata also lists 0.2.0 and skill frontmatter lists 0.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
