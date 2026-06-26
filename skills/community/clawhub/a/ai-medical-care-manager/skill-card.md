## Description: <br>
面向C端门诊就医全流程。先做症状分流和挂号科室判断，再推荐医院/医生 Top 3，并继续完成挂号引导、就医准备卡、提醒、诊后解释，以及基于高德地图的到院路线规划。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunlinlin-aragon](https://clawhub.ai/user/sunlinlin-aragon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to plan and manage an outpatient medical visit, from symptom triage and department selection through hospital or doctor recommendations, appointment preparation, reminders, route planning, and post-visit explanation. It is intended as visit workflow support and plain-language interpretation, not as a replacement for clinician diagnosis or emergency care. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Medical and appointment details are sensitive, and route planning can share location data with AMap. <br>
Mitigation: Use routing only when needed, configure a restricted AMap key, and prefer a manually provided rough starting point instead of IP-based location. <br>
Risk: Users may mistake workflow support or plain-language explanations for medical diagnosis. <br>
Mitigation: Keep outputs framed as triage and visit support, prioritize emergency guidance for high-risk symptoms, and defer clinical decisions to qualified medical professionals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunlinlin-aragon/ai-medical-care-manager) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/skills) <br>
- [flow_playbook.md](references/flow_playbook.md) <br>
- [response_templates.md](references/response_templates.md) <br>
- [triage_rules.md](references/triage_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured text with optional JSON outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AMap route links when routing is configured with an AMap Web Service key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
