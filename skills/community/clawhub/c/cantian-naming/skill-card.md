## Description: <br>
Chinese Name Generator - Cantian AI helps agents analyze Chinese names and generate personal, company, brand, pet, stage, screen, and bilingual naming candidates using favorable-element filtering, pronunciation, meaning, aesthetics, and secondary San Cai/Wu Ge references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianlinle](https://clawhub.ai/user/tianlinle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate and compare Chinese naming candidates for people, businesses, brands, shops, pets, stage names, screen names, and bilingual naming tasks. It can run local scripts to score candidates by favorable elements, character data, pronunciation, and optional San Cai/Wu Ge structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Traditional favorable-element and WuGe scoring may be interpreted as factual certainty. <br>
Mitigation: Present scores as advisory naming references and combine them with human judgment about pronunciation, meaning, culture, and personal preference. <br>
Risk: Using the tsx fallback can introduce an additional npm dependency. <br>
Mitigation: Prefer the documented Node 24 path; when tsx is needed, review or pin the dependency before use. <br>
Risk: Naming requests can include unnecessary personal details. <br>
Mitigation: Ask only for the naming details needed for the task and avoid retaining extra sensitive context. <br>


## Reference(s): <br>
- [Cantian AI](https://cantian.ai) <br>
- [Cantian BaZi companion skill](https://clawhub.ai/tianlinle/cantian-bazi) <br>
- [ClawHub release page](https://clawhub.ai/tianlinle/cantian-naming) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with optional JSON output from local scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Name analysis and candidate lists may include scores, score breakdowns, character attributes, pronunciation, elemental tags, and optional San Cai/Wu Ge results.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
