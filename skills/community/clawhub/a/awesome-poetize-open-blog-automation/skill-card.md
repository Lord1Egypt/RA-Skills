## Description: <br>
Poetize Blog Automation helps an agent draft, publish, update, hide, and manage POETIZE blog content, taxonomy, themes, analytics, and SEO for the open-source awesome-poetize-open release. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leapya](https://clawhub.ai/user/leapya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and blog operators use this skill to operate a POETIZE blog as a personal publishing and maintenance system. It supports article creation and updates, article hiding, category and tag management, theme switching, analytics review, SEO configuration, and OpenClaw agent setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or change content on a live POETIZE blog. <br>
Mitigation: Run the smoke test and use a staging blog before first production use; review every mutating command and strategy brief before execution. <br>
Risk: The skill requires a POETIZE API key with administrative blog access. <br>
Mitigation: Keep the API key out of source control and chat transcripts, scope or rotate it where possible, and install only when the publisher is trusted. <br>
Risk: Local Markdown image paths can be uploaded automatically during publish flows. <br>
Mitigation: Inspect image paths before publishing or set uploadLocalImages:false when local file upload is not intended. <br>
Risk: Payment configuration support can affect monetized publishing settings. <br>
Mitigation: Avoid paymentConfigFile unless intentionally configuring payments and confirm payment plugin readiness before paid publishing. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/leapya/awesome-poetize-open-blog-automation) <br>
- [Publisher Profile](https://clawhub.ai/user/leapya) <br>
- [Poetize Blog API Reference](references/poetize-api.md) <br>
- [Agent Skills Setup Guide](references/agent-setup.md) <br>
- [Strategy Playbook](references/strategy-playbook.md) <br>
- [Decision Matrix](references/decision-matrix.md) <br>
- [Evaluation Scenarios](references/evaluation-scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON briefs, YAML-like front matter, and shell commands for the bundled CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call POETIZE admin APIs, upload local image files referenced by Markdown, and require POETIZE_BASE_URL and POETIZE_API_KEY.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
