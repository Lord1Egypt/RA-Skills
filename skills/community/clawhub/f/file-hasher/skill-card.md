## Description: <br>
Compute, verify, and compare file hashes using MD5, SHA-1, SHA-256, SHA-512, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compute checksums, verify downloaded files against expected hashes, compare files for equality, hash directories or strings, and validate checksum files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recursive directory hashing can process many local files, including sensitive locations, and can print file paths and hashes. <br>
Mitigation: Run it only on files or directories you intend to hash, and avoid broad recursive scans of sensitive locations unless that processing is intentional. <br>
Risk: MD5 and SHA-1 are available for compatibility but are weak choices for new integrity workflows. <br>
Mitigation: Use SHA-256 or SHA-512 for new verification workflows unless matching a legacy checksum requires another algorithm. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON] <br>
**Output Format:** [Plain text checksum lines, BSD-style checksum lines, verification summaries, or JSON records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external dependencies; uses Python hashlib and local filesystem reads] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
