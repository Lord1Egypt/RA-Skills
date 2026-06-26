## Description: <br>
Helps measure the concentration of trust roots in a skill's attestation graph, identifying monoculture risk where a single compromised root invalidates an entire chain that appears to have multiple validators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and marketplace operators use this skill to evaluate whether a skill's attestation roots are truly distributed or concentrated around a small number of organizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Root diversity conclusions can be approximate when the full attestation graph or organizational relationships between validators are unavailable. <br>
Mitigation: Provide complete validator chains, root identifiers, and known organizational relationships, and treat inferred independence as review input rather than proof. <br>
Risk: The skill declares curl and python3 as required tools, so related workflows may involve network requests or local file processing. <br>
Mitigation: Review any curl or python3 command before execution and provide only attestation metadata or skill identifiers intended for analysis. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/andyxinweiminicloud/attestation-root-diversity-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown root diversity report with text-based trust graph analysis, verdicts, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires attestation metadata, a trust graph, or two skills to compare; no files are created by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
