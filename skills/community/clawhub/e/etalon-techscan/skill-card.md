## Description: <br>
Detects a domain's technology stack with the local ETALON CLI and returns detected frameworks, CDNs, CMS platforms, analytics, hosting providers, confidence scores, and detection methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rednix](https://clawhub.ai/user/rednix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to inspect websites, compare competitor or vendor stacks, support due diligence, and gather evidence for migration or technology decisions after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or running the wrong local ETALON CLI package could expose the user to untrusted code. <br>
Mitigation: Verify that the etalon-cli package and repository are the intended trusted sources before installing or running the command. <br>
Risk: Technology scans contact target websites and batch scans can create unwanted traffic or policy issues. <br>
Mitigation: Run scans only for user-approved domains where there is permission or a legitimate reason, and use batch mode carefully. <br>


## Reference(s): <br>
- [ETALON homepage](https://etalon.nma.vc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Human-readable Markdown summaries with inline shell commands and grouped scan findings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes technology categories, confidence scores, and detection methods when available.] <br>

## Skill Version(s): <br>
0.9.5 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
