## Description: <br>
Starts 1688 supply-chain procurement inquiry instances from complete purchase requirements and retrieves instance data by instanceId through the documented file-output path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External procurement operators and agents use this skill to start a 1688 supplier inquiry from complete purchase requirements and query returned inquiry data by instanceId. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires 1688 procurement API credentials and can fall back to locally configured credentials. <br>
Mitigation: Install it only in environments approved to use those credentials, rotate credentials if exposure is suspected, and limit access to users who need procurement API access. <br>
Risk: Procurement requirements, images, and usage metadata may be sent to the 1688 skills gateway. <br>
Mitigation: Submit only data appropriate for that service and avoid including unnecessary confidential or regulated information in purchase requirements or images. <br>
Risk: Untrusted image URLs can trigger remote fetching behavior. <br>
Mitigation: Prefer trusted local image files and avoid passing untrusted HTTP(S) image URLs. <br>
Risk: Instance data queries can expose large result data directly into the agent context if file mode is not used. <br>
Mitigation: Use the documented file-mode query path and stream the output file instead of pasting, summarizing, or reformatting the JSON in the final response. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/1688-supplychain-api-procurement) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands] <br>
**Output Format:** [Raw JSON passthrough for inquiry creation; file-path JSON followed by streamed JSON file output for instance data queries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final responses must not wrap, summarize, or reformat the returned JSON; instance data queries use file mode to keep large results out of the model context.] <br>

## Skill Version(s): <br>
0.0.6 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
