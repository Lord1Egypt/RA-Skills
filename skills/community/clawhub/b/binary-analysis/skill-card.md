## Description: <br>
Dr.Binary helps agents upload binary files to a Dr. Binary sandbox, analyze them with Ghidra-backed tools, decompile executables, and report maliciousness or behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deepbitstech](https://clawhub.ai/user/deepbitstech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and reverse engineers use this skill to inspect binaries, gather file metadata, identify suspicious imports or strings, decompile functions, and produce a structured binary analysis report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected binaries are uploaded to an external Dr. Binary/Deepbits sandbox for analysis. <br>
Mitigation: Submit only files you are authorized to share, and avoid proprietary, regulated, or personal binaries unless the provider's retention and privacy terms are acceptable. <br>
Risk: The upload workflow uses DRBINARY_API_KEY to authenticate with the remote analysis service. <br>
Mitigation: Store the key outside source control, use a scoped key when available, and rotate it if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deepbitstech/binary-analysis) <br>
- [Dr. Binary upload endpoint](https://mcp.deepbits.com/workspace/upload) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown report with inline command examples, analysis findings, threat assessment, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DRBINARY_API_KEY and uploads selected binaries to an external Dr. Binary sandbox.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
