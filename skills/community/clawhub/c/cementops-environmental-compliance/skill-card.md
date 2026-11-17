## Description:

CementOps Environmental Compliance helps cement plant environmental teams navigate EPA NESHAP Subpart LLL limits, CEMS QA/QC, Title V permits, alternative fuels emissions, exceedance response, and NOV procedures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larkinjoshuad](https://clawhub.ai/user/larkinjoshuad)

### License/Terms of Use:

MIT-0

## Use Case:

External environmental managers, compliance officers, plant managers, and CEMS technicians use this skill for cement plant emissions compliance guidance, reporting obligation triage, Title V permit questions, alternative fuels impacts, CEMS troubleshooting, and NOV response planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run a reporting checker with user-supplied event text.

Mitigation: Run the checker without shell interpolation, using an executable plus literal argument array or stdin, and review checker output before acting on reporting deadlines.

Risk: Regulatory guidance may be incomplete, outdated, or in tension with site-specific permit and state requirements.

Mitigation: Verify guidance against current federal rules, the facility Title V permit, state requirements, and qualified counsel before making compliance or reporting decisions.

Risk: Environmental field work can involve toxic calibration gases, elevated stack platforms, confined spaces, and chemical handling hazards.

Mitigation: Require site safety procedures, SDS review, PPE, gas detection, fall protection, confined-space controls, and qualified personnel before using guidance for field work.

## Reference(s):

- [CementOps AI homepage](https://cementops.ai)
- [ClawHub skill page](https://clawhub.ai/larkinjoshuad/skills/cementops-environmental-compliance)
- [Cement Kiln Emissions Knowledge Base](artifact/knowledge-bases/cement-kiln-emissions.json)
- [CEMS Requirements Knowledge Base](artifact/knowledge-bases/cems-requirements.json)
- [Title V Permits Knowledge Base](artifact/knowledge-bases/title-v-permits.json)
- [Alternative Fuels Emissions Knowledge Base](artifact/knowledge-bases/alternative-fuels-emissions.json)
- [Startup, Shutdown, Bypass, and Malfunction Provisions](artifact/knowledge-bases/startup-shutdown-bypass.json)
- [Environmental Reporting Obligation Rules](artifact/reporting-rules.json)
- [Environmental Compliance Safety Hazards](artifact/safety/environmental-safety.json)
- [NOV Response Guide](artifact/guidance-templates/nov-response-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with occasional shell command examples and JSON checker output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes federal compliance references, safety cautions, and reporting triage; users must verify against current rules, permits, state requirements, and counsel.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact/SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
