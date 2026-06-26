## Description: <br>
Bearing Search helps agents look up bearing model specifications, compare bearing brands and product lines, decode model codes and suffixes, and provide application-based bearing selection guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openfindbearings](https://clawhub.ai/user/openfindbearings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, maintenance engineers, and developers use this skill to answer bearing model, brand, specification, cross-reference, and selection questions. It can also use the bundled local Python helper to search expected local bearing model data files when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearing specifications or selection advice may be incorrect or incomplete for safety-critical mechanical applications. <br>
Mitigation: Verify dimensions, loads, speed limits, environmental suitability, and substitutions against manufacturer documentation before procurement, installation, or operation. <br>
Risk: The optional Python lookup helper reads local bearing data files, so unexpected or untrusted local data could affect search results. <br>
Mitigation: Use trusted local data files and review the data source before relying on returned bearing specifications. <br>


## Reference(s): <br>
- [Bearing Data Structure](references/data-structure.md) <br>
- [Bearing Model Code Rules](references/model-codes.md) <br>
- [Bearing Brand Reference](references/brands.md) <br>
- [SKF](https://www.skf.com) <br>
- [ClawHub Release Page](https://clawhub.ai/openfindbearings/bearing-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cite local bearing reference files and local model data when present; bearing specifications should be verified against manufacturer documentation for safety-critical use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
