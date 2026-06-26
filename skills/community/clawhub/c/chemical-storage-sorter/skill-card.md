## Description: <br>
Sort chemicals by compatibility for safe laboratory storage, segregating acids, bases, oxidizers, flammables, and related hazard groups while providing storage recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Lab staff, EHS reviewers, and developers use this skill to sort chemical inventories into compatibility groups, check proposed storage pairings, and draft storage plans. Its output should be treated as a planning aid and verified against current SDS documents and institutional safety rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides high-stakes chemical storage guidance using simple keyword heuristics that may miss or misclassify hazardous materials. <br>
Mitigation: Use it only as a rough planning aid; verify every classification against current SDS documents, institutional EHS rules, and qualified lab safety review. <br>
Risk: Unknowns, mixtures, concentrated reagents, oxidizers, cyanides, sulfides, peroxide formers, pyrophorics, and water-reactive chemicals may require controls beyond the generated storage plan. <br>
Mitigation: Escalate these cases to qualified lab safety personnel and apply chemical-specific handling, segregation, and storage requirements before use. <br>
Risk: The security evidence notes incomplete file-access disclosure. <br>
Mitigation: Review any file reads or generated outputs before granting file permissions or using the results operationally. <br>


## Reference(s): <br>
- [Chemical Storage Sorter on ClawHub](https://clawhub.ai/AIPOCH-AI/chemical-storage-sorter) <br>
- [OSHA Chemical Storage Guidelines](https://www.osha.gov/chemical-storage) <br>
- [SDS Search (MSDSOnline)](https://www.msdsonline.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Python examples and CLI commands; script output is plain text storage plans.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No network calls are described; local execution uses a Python standard-library script.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
