## Description: <br>
Deep Research Agent guides an agent through multi-phase research planning, source gathering, fact verification, and structured report synthesis for comprehensive investigations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericn26-star](https://clawhub.ai/user/ericn26-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and researchers use this skill to plan broad investigations, gather and classify many sources, verify claims, and synthesize cited research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broad research trigger may activate for generic research wording and drive heavy web or source extraction. <br>
Mitigation: Review and narrow the trigger language or source targets before deploying it in constrained environments. <br>
Risk: Generated reports can include outdated, duplicated, or weakly verified claims if source review is incomplete. <br>
Mitigation: Require citation checks, source diversity review, and explicit confidence labels for uncertain findings before relying on the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericn26-star/eric-deep-research-agent) <br>
- [Research template](artifact/references/research_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown reports with inline citations and JSON research plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets 100 unique sources and inline references; supports Japanese and English research workflows.] <br>

## Skill Version(s): <br>
11.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
