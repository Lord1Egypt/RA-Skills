## Description:

Converts AutoCAD DWG drawing files to DXF format on Windows by invoking a local ODA File Converter through a Python script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lialia691691-alt](https://clawhub.ai/user/lialia691691-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert DWG drawings, or folders of DWG drawings, into DXF files before downstream parsing or CAD-processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The converter lookup can run an unverified executable from the system PATH.

Mitigation: Use a fixed trusted ODA File Converter path, verify the converter binary before installation, and remove or constrain PATH-based fallback lookup.

Risk: Broad activation instructions may trigger local conversion on untrusted DWG files or ambiguous DWG-processing requests.

Mitigation: Require explicit user confirmation before execution and handle DWG files only in a controlled environment.

## Reference(s):

- [ODA File Converter](https://www.opendesign.com/guestfiles/oda_file_converter)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Command-line invocation and generated DXF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local ODA File Converter installation; the workflow is Windows-oriented and uses a 180-second conversion timeout.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
