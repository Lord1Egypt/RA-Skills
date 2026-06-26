## Description: <br>
Uses the JZ Data fuzzy VIN decoding API to look up standard OE part codes and names from a 17-character VIN and a list of part aliases when exact decoding is not available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polaris2013](https://clawhub.ai/user/polaris2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to query VIN-and-parts fuzzy decoding results, then summarize returned OE references, part names, aliases, and source fields for automotive parts workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VINs, part-name lists, and the API key are sent to the JZ/qipeidao service for lookup. <br>
Mitigation: Install only if you trust that service with this data, treat VINs as potentially sensitive, and use a scoped or dedicated API key where possible. <br>
Risk: One README usage example names the wrong script file. <br>
Mitigation: Use the included get_fuzzy_oe.py script path and verify commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/polaris2013/fuzzyoe) <br>
- [JZ fuzzy OE API endpoint](https://erp.qipeidao.com/jzOpenClaw/getFuzzyOe) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, shell commands] <br>
**Output Format:** [JSON response data and concise text summaries, with shell command examples for invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the JZ_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
