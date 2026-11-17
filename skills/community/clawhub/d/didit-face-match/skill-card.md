## Description:

Integrate Didit Face Match standalone API to compare two facial images, verify face identity, and return a similarity score with configurable threshold, rotation, and multi-face handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:


## Use Case:

Developers and external teams use this skill to add Didit-powered facial image comparison, biometric identity verification, or selfie-to-document matching workflows. It helps agents explain request parameters, authentication, response handling, thresholds, warnings, and the included face-matching utility script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads facial images and derived biometric metadata to an external Didit service.

Mitigation: Use it only with explicit permission to process the images and after confirming Didit's retention and deletion terms.

Risk: Artifact behavior may expose more biometric detail than a user needs, including raw JSON fields such as age, gender, face bounding boxes, and detection confidence.

Mitigation: Minimize output to the decision status and similarity score unless the additional fields are necessary and authorized.

Risk: Request retention defaults may save face-match requests in Didit systems.

Mitigation: Prefer setting request-retention options to disabled where supported and document any retention choice before upload.

## Reference(s):

- [Didit documentation](https://docs.didit.me)
- [Didit Face Match API reference](https://docs.didit.me/standalone-apis/face-match)
- [Didit Face Match feature guide](https://docs.didit.me/core-technology/face-match/overview)
- [ClawHub skill page](https://clawhub.ai/rosasalberto/skills/didit-face-match)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with code examples, shell commands, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DIDIT_API_KEY. The utility script prints the raw Didit JSON response and a status and score summary.]

## Skill Version(s):

1.3.0 (source: server release evidence; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
