## Description:

AI image geolocation via visual analysis - no GPS or EXIF needed. Requires GEOINFER_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samtin0x](https://clawhub.ai/user/samtin0x)

### License/Terms of Use:


## Use Case:

External users, investigators, OSINT analysts, digital forensics teams, journalists, and security practitioners use this skill to submit local images to GeoInfer and receive likely location predictions for visual geolocation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The prediction script can upload any readable local file path supplied to it to an external GeoInfer API without strong MIME/type validation, size enforcement, or an explicit upload warning.

Mitigation: Only run predictions on intentionally selected, non-sensitive image files; do not let untrusted prompts choose file paths, and prefer adding MIME/type checks, size enforcement, and upload confirmation before broader deployment.

## Reference(s):

- [GeoInfer API Access](https://app.geoinfer.com/en/api)
- [ClawHub Skill Page](https://clawhub.ai/samtin0x/skills/geoinfer-image-geolocation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown usage guidance and shell commands; prediction, model, and credit tools return JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEOINFER_API_KEY and local image files; predict.sh accepts image_path, model_id, and top_n.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
