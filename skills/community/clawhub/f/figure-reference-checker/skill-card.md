## Description: <br>
Check figure references in manuscripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, researchers, and publishing teams use this skill to check manuscript figure references for missing citations, orphaned references, and figure-label consistency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised manuscript-file workflow may produce misleading results because the script appears to inspect the command-line argument text rather than reading the document file. <br>
Mitigation: Verify output on a known sample before relying on results, or update the script to read and parse the supplied manuscript file. <br>
Risk: The skill runs local Python code against user-provided manuscript input. <br>
Mitigation: Run it in a sandboxed workspace with non-sensitive sample files when evaluating the release. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AIPOCH-AI/figure-reference-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, analysis, shell commands] <br>
**Output Format:** [Plain text CLI output with a sorted list of detected figure reference numbers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a --manuscript value; current implementation scans the provided argument text.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
