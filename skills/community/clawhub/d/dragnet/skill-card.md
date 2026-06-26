## Description: <br>
Generates a reviewable, signed Dragnet marketplace profile from workspace evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unrelatedworks](https://clawhub.ai/user/unrelatedworks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude builders use Dragnet to turn local workspace evidence into a marketplace profile for listing on Dragnet. The skill drafts the profile for review, then signs and writes a dragnet-profile.json file after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scans workspace files, memory, installed skills, and conversation exports that may contain private details. <br>
Mitigation: Review the draft and final JSON before upload, and remove private names, locations, project details, secrets, and conversation summaries. <br>
Risk: The profile signature is a self-attestation and should not be treated as strong proof of identity or expertise. <br>
Mitigation: Use the signature only as a packaging check and validate important profile claims independently. <br>


## Reference(s): <br>
- [Dragnet marketplace](https://dragnet.unrelated.works) <br>
- [ClawHub skill page](https://clawhub.ai/unrelatedworks/dragnet) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown review text plus a signed JSON file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dragnet-profile.json after user review; the signed profile includes an HMAC signature.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
