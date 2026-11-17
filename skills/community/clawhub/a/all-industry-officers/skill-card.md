## Description:

All-Industry Officers routes business-operations requests across 15 functional domains, 125 capability units, and supporting reference templates to produce structured organizational deliverables for HR, finance, administration, IT, compliance, customers, supply chain, analytics, content, events, knowledge, and related workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operators, and business teams use this skill to plan, route, and draft functional work products across common organizational domains. It is best suited for structured business deliverables such as plans, reports, checklists, risk maps, policies, process documents, and role-based operational guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers sensitive HR, finance, customer, compliance, and operational workflows.

Mitigation: Use only authorized data, redact unnecessary personal or confidential information, and require qualified human review before acting on legal, tax, finance, HR, security, or compliance outputs.

Risk: Server security evidence warns that the skill's multi-agent-style narration may obscure how execution actually works.

Mitigation: Treat role and team narration as presentation unless the runtime explicitly provides and uses independent agent tools; do not rely on narration as proof that separate agents or reviewers ran.

Risk: The skill can create or modify workspace files when granted write access.

Mitigation: Start in read-only mode unless file creation is explicitly needed, review generated files or diffs before use, and keep source reference updates separate from user-provided calibration data.

Risk: Business, regulatory, tax, labor, privacy, and security guidance can become outdated or vary by jurisdiction.

Mitigation: Confirm current authoritative requirements for the user's jurisdiction and organization before relying on outputs, and mark uncertain or stale facts as needing verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/skills/all-industry-officers)
- [AIO catalog](references/AIO-catalog.md)
- [AIO requirements](references/AIO-requirements.md)
- [AIO exemplars](references/AIO-exemplars.md)
- [AIO X0 routing and orchestration exemplar](references/AIO-X0-路由编排域范本.md)
- [AIO N1 human resources exemplar](references/AIO-N1-人力资源域范本.md)
- [AIO N2 finance and accounting exemplar](references/AIO-N2-财务会计域范本.md)
- [AIO N3 administration exemplar](references/AIO-N3-行政办公域范本.md)
- [AIO N4 information technology exemplar](references/AIO-N4-信息技术域范本.md)
- [AIO B1 intelligence collection and monitoring exemplar](references/AIO-B1-情报采集与监测域范本.md)
- [AIO B2 certification and regulatory exemplar](references/AIO-B2-资质认证与监管域范本.md)
- [AIO B3 content production and distribution exemplar](references/AIO-B3-内容生产与传播域范本.md)
- [AIO B4 event operations exemplar](references/AIO-B4-活动运营与执行域范本.md)
- [AIO B5 customer and partner operations exemplar](references/AIO-B5-客户与伙伴运营域范本.md)
- [AIO B6 supply chain and operations support exemplar](references/AIO-B6-供应链与运营保障域范本.md)
- [AIO B7 data analysis and decision-making exemplar](references/AIO-B7-数据分析与决策域范本.md)
- [AIO B8 process collaboration and project management exemplar](references/AIO-B8-流程协同与项目管理域范本.md)
- [AIO B9 compliance review and risk control exemplar](references/AIO-B9-合规审核与风控域范本.md)
- [AIO B10 knowledge management and training exemplar](references/AIO-B10-知识管理与培训域范本.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown deliverables, structured tables, checklists, plans, reports, and optional workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can operate in read-only or no-write modes; some outputs require human confirmation for sensitive business, legal, tax, finance, HR, or compliance decisions.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
