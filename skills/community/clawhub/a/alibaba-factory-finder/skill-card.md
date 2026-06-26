## Description: <br>
Find and verify factories on Alibaba.com by building supplier search and profile URLs for verified suppliers, certifications, and factory audits; generated URLs include the traffic_type=ags_llm tracking parameter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zeyu426](https://clawhub.ai/user/Zeyu426) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and sourcing teams use this skill to construct Alibaba supplier searches, open supplier profiles, and compare manufacturer credentials before shortlisting potential factories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alibaba search terms and supplier profile paths may reveal sourcing intent when used in generated URLs. <br>
Mitigation: Review search queries before opening or sharing generated links, and avoid including confidential product names or supplier information. <br>
Risk: Generated links intentionally include the traffic_type=ags_llm analytics and attribution parameter. <br>
Mitigation: Disclose the attribution parameter to users and keep it only when attribution is expected for the workflow. <br>
Risk: The bundled release script is for publishing the skill package, not for normal supplier-search use. <br>
Mitigation: Do not run release.sh unless intentionally publishing this skill package to ClawHub. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Zeyu426/alibaba-factory-finder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Alibaba URLs and optional shell command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated Alibaba URLs include traffic_type=ags_llm, and user search queries are embedded in those URLs.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
