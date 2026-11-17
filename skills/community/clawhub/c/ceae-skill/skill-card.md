## Description:

ceae-skill helps hardware engineers perform parameter root-cause analysis using a four-role TRIZ collaboration workflow, first-principles decomposition, 5 Why analysis, and causal-tree outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Hardware product optimization engineers use this skill to turn vague parameter targets into quantified engineering problems, coordinate mechanical, materials, electrical, and manufacturing analysis, and produce key issue lists, Mermaid causal diagrams, and optional PNG archive images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use a third-party MCP service under the user's account for database-backed conclusions.

Mitigation: Keep MCP access disabled for offline analysis, enable it only after account authorization is understood, and review database-backed conclusions before relying on them.

Risk: The PNG exporter can process causal-tree JSON into image files and may fail or behave poorly on untrusted or very large inputs.

Mitigation: Run the exporter only after user confirmation, use trusted bounded causal-tree JSON, and review the causal tree before export.

## Reference(s):

- [ceae-skill ClawHub release page](https://clawhub.ai/yuanzhian-patsnap/skills/ceae-skill)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown with Mermaid code blocks and optional PNG file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require user-confirmed quantified inputs and enabled Zhihuiya MCP access for database-backed conclusions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
