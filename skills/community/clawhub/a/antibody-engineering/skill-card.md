## Description: <br>
Antibody engineering workflow combining ANARCI, BioPhi, IgFold, FoldX, and Rosetta tools through SciMiner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, computational biologists, and antibody engineers use this skill to plan and run sequence de-risking, humanization, structure prediction, relaxation, developability profiling, mutation analysis, and candidate ranking workflows through SciMiner tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SciMiner tool calls may submit antibody sequences, structures, or other user-provided research data to an external service. <br>
Mitigation: Confirm data-sharing expectations before submitting jobs and review returned share URLs before distributing them. <br>
Risk: Credential handling mistakes could expose the SciMiner API key. <br>
Mitigation: Keep the key only in ~/.config/sciminer/credentials.json, do not print or persist it, and stop if the credential file is missing or malformed. <br>
Risk: Candidate-ranking or mutation guidance may be incorrect or incomplete for wet-lab, regulatory, or clinical decisions. <br>
Mitigation: Treat outputs as computational decision support and have qualified domain experts review candidate changes before experimental or downstream use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sciminer/antibody-engineering) <br>
- [SciMiner tool API files](https://sciminer.tech/tool_api_files/) <br>
- [SciMiner API key utility](https://sciminer.tech/utility) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown summaries with JSON snippets, code examples, and SciMiner share URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SciMiner API key stored outside the repository and may return long-running task identifiers with share URLs.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
