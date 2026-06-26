## Description: <br>
Searches local knowledge and insight-history records for Chuwi Minibook-related items, although the artifact documentation describes a system monitoring skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users can use this skill to query local Chuwi Minibook knowledge and insight-history records. Review the release before installation because server security evidence reports that the documented monitoring behavior does not match the current code behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release appears mislabeled because documentation describes hardware monitoring while the code searches local knowledge and insight-history files. <br>
Mitigation: Review the artifact before installing, align the documentation with the implemented behavior, and disclose the local data sources the skill reads. <br>
Risk: Broad trigger phrases may invoke the skill for general system or Chuwi queries even though the implemented behavior is local data search. <br>
Mitigation: Narrow trigger phrases to the actual local-search behavior or update the code to match the documented monitoring workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/chuwi-minibook) <br>
- [Publisher profile](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON object containing status, query metadata, result summaries, sources, optional URLs, and timestamp] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are deduplicated and limited to local knowledge and insight-history matches.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
