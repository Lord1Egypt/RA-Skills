## Description: <br>
Local self-check of instructions and mask outputs (format/range/consistency) without using GT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill after generating interval instructions and mask outputs to check JSON key/value format, frame coverage, NPZ frame continuity, CSR integrity, and mask shape consistency before submission or hand-off. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validation failures surface as assertions and do not automatically fix malformed instruction or mask files. <br>
Mitigation: Run the checks on files you intentionally provide, then inspect assertion failures and correct the generated outputs before submission or hand-off. <br>
Risk: The checks validate format, range, and consistency, but they do not compare outputs against ground truth. <br>
Mitigation: Use this as a local pre-submission consistency check and apply task-specific quality review or ground-truth evaluation where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/dynamic-object-aware-egomotion-output-validation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code] <br>
**Output Format:** [Markdown with Python validation snippet] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Validates user-provided video, interval instruction JSON, and mask NPZ files locally; assertions report malformed outputs but do not repair them.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
