## Description: <br>
Compresses long content into structured 4D vectors to reduce token use by about 60-80% while preserving core information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[largetool](https://clawhub.ai/user/largetool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can trigger the skill to compress pasted text into structured summaries for review, knowledge preservation, or retrieval. It is intended for text content and does not directly process EPUB or PDF files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broad triggers, including ordinary terms such as "compress" and "压缩", may activate the skill more often than expected. <br>
Mitigation: Review the agent's selected skill before acting on compressed output, especially in workflows where ordinary compression requests may have another meaning. <br>
Risk: The artifact describes local-only and privacy-preserving behavior, but the scanner guidance notes that sensitive-text handling depends on the OpenClaw runtime's guarantees. <br>
Mitigation: Avoid relying on the local-only claim for highly sensitive text unless the deployed runtime independently guarantees local processing and data handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/largetool/4d-compression-core) <br>
- [VERSION_PROTOCOL.md](artifact/VERSION_PROTOCOL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown text with structured 4D sections and optional JSON-style structured output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Compression rate and semantic retention vary by text type; EPUB and PDF inputs must be converted to text first.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
