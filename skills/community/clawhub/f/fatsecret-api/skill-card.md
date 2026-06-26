## Description: <br>
Search foods, look up nutrition, log meals, track weight, browse recipes, and manage exercises via the FatSecret API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivanvmoreno](https://clawhub.ai/user/ivanvmoreno) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query FatSecret nutrition data and manage FatSecret food diary, exercise, weight, recipe, saved meal, favorite, and profile records through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change FatSecret health-account records, including food diary entries, saved meals, favorites, exercises, weight entries, and profile data. <br>
Mitigation: Require user confirmation before logging, editing, deleting, copying, or updating any FatSecret account record. <br>
Risk: FatSecret credentials and nutrition or health data are sent to FatSecret services through the pyfatsecret dependency. <br>
Mitigation: Install only if the user trusts FatSecret and pyfatsecret with this data, keep the FatSecret client secret private, and use a virtual environment with a pinned dependency version where practical. <br>
Risk: Incorrect food, serving, diary, recipe, exercise, or weight identifiers could cause inaccurate records or unintended changes. <br>
Mitigation: Look up identifiers before use, present meaningful summaries to the user, and prefer read-only operations until the user explicitly requests a change. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivanvmoreno/fatsecret-api) <br>
- [FatSecret API Platform](https://platform.fatsecret.com/api/) <br>
- [FatSecret API Terms of Use](https://platform.fatsecret.com/api/Default.aspx?screen=rapisd) <br>
- [FatSecret REST API endpoint](https://platform.fatsecret.com/rest/v2/server.api) <br>
- [FatSecret OAuth token endpoint](https://oauth.fatsecret.com/connect/token) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with JSON command output and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FATSECRET_CLIENT_ID, FATSECRET_CLIENT_SECRET, python3, and the pyfatsecret dependency; mutating account actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
