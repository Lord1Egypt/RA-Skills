## Description: <br>
Humanize murine antibody sequences using CDR grafting and framework optimization to reduce immunogenicity while preserving antigen binding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and antibody engineering teams use this skill to analyze murine VH/VL sequences, identify CDRs, select human framework candidates, and generate humanized sequence recommendations for experimental follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Potentially proprietary antibody sequences may be processed in the current workspace. <br>
Mitigation: Use the skill only in trusted workspaces and avoid exposing sensitive sequences to unrelated tools or shared storage. <br>
Risk: The patent-landscape example is inconsistent with the shipped artifact and references an unavailable patent-checking component. <br>
Mitigation: Do not rely on patent-analysis examples unless the publisher supplies and documents the component, contacted databases, and sequence-data handling. <br>
Risk: Computational humanization results may not preserve binding, stability, or immunogenicity in experimental settings. <br>
Mitigation: Use outputs to prioritize candidates and require binding, stability, and immunogenicity validation before therapeutic decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/antibody-humanizer) <br>
- [AIPOCH-AI publisher profile](https://clawhub.ai/user/AIPOCH-AI) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; the included local script can emit JSON, FASTA, or CSV reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes VH/VL sequence inputs, optional JSON input files, numbering scheme, output format, and top-N framework count.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
