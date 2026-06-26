## Description: <br>
Helps surgical pathologists, pathology trainees, pathology assistants, and LIS report-builders draft CAP Cancer Protocol-conformant synoptic cancer reports with protocol selection, Required Data Elements, AJCC 8th Edition pTNM staging, biomarker fields, and attending review labeling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External pathology professionals and LIS report-builders use this skill to prepare draft CAP-style synoptic cancer report text for attending pathologist review and electronic sign-out workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft pathology report text may be clinically incomplete, inconsistent, or wrong if source case details are missing or ambiguous. <br>
Mitigation: Treat every output as a draft and require attending pathologist review before LIS sign-out or clinical release. <br>
Risk: Case inputs may contain patient identifiers or other protected health information. <br>
Mitigation: Use the minimum necessary case details and an accession number only; avoid patient name, MRN, DOB, and other direct identifiers in the working draft. <br>
Risk: Using the wrong CAP protocol version can make a synoptic report nonconformant. <br>
Mitigation: Confirm the applicable protocol version against the institution's LIS/CAP materials before drafting Required Data Elements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/cap-cancer-synoptic-report-drafter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown draft pathology report packet with synoptic report text, comment block, final diagnosis line, open questions, and evidence index.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft only; requires attending pathologist review before clinical use or release.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
