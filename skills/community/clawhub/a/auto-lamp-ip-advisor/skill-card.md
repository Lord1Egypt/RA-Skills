## Description:

Auto Lamp IP Advisor helps agents analyze automotive lamp designs or parts lists across module breakdown, make-or-buy decisions, patent risk, and procurement or design recommendations, then produce a tabbed HTML report packaged as a ZIP file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Automotive lighting engineers, sourcing teams, and IP reviewers use this skill to turn lamp design descriptions or parts lists into sourcing recommendations and preliminary patent-risk guidance. It is especially focused on optical, thermal, mechanical, electrical, and design-patent considerations for automotive lighting supply chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential automotive lamp designs or parts lists may be sent to an external patent lookup service.

Mitigation: Use the skill only in approved workspaces and PatSnap accounts for that data; avoid submitting confidential designs without authorization.

Risk: Generated patent-risk analysis can be incomplete or unsuitable as legal advice.

Mitigation: Treat outputs as preliminary guidance and obtain formal FTO review from qualified patent counsel before production or supplier decisions.

Risk: Generated reports are saved locally and packaged for sharing.

Mitigation: Review report content, footer attribution, and file location before distributing the HTML or ZIP externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/auto-lamp-ip-advisor)
- [Publisher profile](https://clawhub.ai/user/yuanzhian-patsnap)
- [PatSnap Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Tabbed HTML report packaged as a ZIP file, with advisory text, tables, inline CSS and JavaScript, and generated local file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may rely on PatSnap patent lookup services and asks the agent to save generated reports locally.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
