## Description: <br>
Local, offline AI-powered file type detection with no network use or API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pgeraghty](https://clawhub.ai/user/pgeraghty) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, security engineers, and operators use this skill to identify local files by content, verify extension and MIME-type consistency, and triage suspicious or unknown files without sending file bytes off the machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recursive scans may read more local files than intended if pointed at a broad directory. <br>
Mitigation: Run recursive scans only on directories the user explicitly intends to inspect. <br>
Risk: The default stdin spool mode can consume disk space for untrusted or very large streams. <br>
Mitigation: Use the documented head mode or apply upstream size limits before invoking the skill on untrusted streams. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pgeraghty/detect-file-type-local) <br>
- [Google Magika](https://github.com/google/magika) <br>
- [MITRE ATT&CK: Masquerading](https://attack.mitre.org/techniques/T1036/) <br>
- [Proofpoint: multistage polyglot threat analysis](https://www.proofpoint.com/us/blog/threat-insight/call-it-what-you-want-threat-actor-delivers-highly-targeted-multistage-polyglot) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON objects or arrays, human-readable text, bare MIME type strings, and CLI command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local read-only classification results include path, detected label, MIME type, confidence score, group, description, and text indicator.] <br>

## Skill Version(s): <br>
0.2.0 (source: SKILL.md frontmatter, pyproject.toml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
