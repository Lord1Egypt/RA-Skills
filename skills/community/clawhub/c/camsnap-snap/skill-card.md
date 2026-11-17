## Description:

Take webcam snapshots with path validation, safe resource handling, and flexible output options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Camsnap to capture local webcam images from the command line or Python code, with configurable camera selection and output location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a local webcam and save captured images.

Mitigation: Install and run it only in environments where webcam access and local image storage are expected and approved.

Risk: The security scan reports that path protection is not enforced and output paths may save or overwrite files outside the expected folder.

Mitigation: Avoid untrusted output_path or output_dir values, especially absolute paths or values containing '..'; prefer a dedicated snapshot directory.

Risk: Existing files may be overwritten when a caller provides an output path.

Mitigation: Use unique filenames or review the destination before execution when preserving existing files matters.

## Reference(s):

- [Camsnap on ClawHub](https://clawhub.ai/terrycarter1985/skills/camsnap-snap)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill saves image files locally when webcam access is available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
