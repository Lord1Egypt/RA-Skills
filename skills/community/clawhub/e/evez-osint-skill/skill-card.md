## Description: <br>
Computes suspect networks and crime probabilities using eigenforensic spectral analysis to support OSINT investigations and prioritize interventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, OSINT analysts, and authorized reviewers use this skill to run suspect-network analysis, compute bounded crime-probability estimates, and generate JSON or Markdown reports for investigative review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-stakes suspect profiling outputs may be mistaken for evidence or used as a basis for action. <br>
Mitigation: Treat generated probabilities and priorities as speculative analysis only; require independent verification, documented provenance, bias review, and human oversight before any action. <br>
Risk: The skill may process sensitive investigative or civil-rights-related data. <br>
Mitigation: Install and use only within a lawful, audited process for handling sensitive investigative data. <br>
Risk: The security summary reports high-stakes suspect profiling without visible safeguards. <br>
Mitigation: Review the workflow and outputs before deployment, and add explicit oversight and review controls around any investigative use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evezart/skills/evez-osint-skill) <br>
- [Publisher profile](https://clawhub.ai/user/evezart) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline bash and Python code blocks; generated reports may be JSON or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Probability outputs are described as bounded between eta* and 0.95 in the artifact evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
