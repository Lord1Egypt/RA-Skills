## Description: <br>
Access the user's biohub across wearable biometrics, continuous glucose, blood panels, supplements, nutrition, body composition, physiological age, and tracking phases to answer wellness and health-status questions grounded in local biometric data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxnau89](https://clawhub.ai/user/maxnau89) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query local biometric and wellness databases, summarize recovery, sleep, glucose, blood-marker, supplement, nutrition, and body-composition trends, and provide non-medical wellness coaching grounded in the user's own data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to read sensitive local biometric and health data. <br>
Mitigation: Use explicit prompts for biohub data access, avoid sharing unnecessary identifiers, and choose a local model or privacy-appropriate LLM provider for sensitive health discussions. <br>
Risk: Wellness summaries may be mistaken for clinical advice. <br>
Mitigation: Treat outputs as non-medical wellness guidance and defer diagnosis, treatment, or disease-related decisions to qualified clinicians. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/maxnau89/skills/biohub) <br>
- [Project Homepage](https://github.com/maxnau89/openclaw-biohub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and SQL query examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces non-medical wellness analysis from local user-controlled data sources.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
