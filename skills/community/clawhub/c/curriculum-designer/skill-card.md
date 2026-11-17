## Description:

Designs customized curricula for PODs with real resource links, staged checkpointing, YouTube link verification, and fallback logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarasinghrajput](https://clawhub.ai/user/tarasinghrajput)

### License/Terms of Use:


## Use Case:

Academic staff use this skill to design POD curricula by collecting learner requirements, finding and validating YouTube resources, structuring lessons, and preparing sheet-ready curriculum outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Google Sheets may be made public.

Mitigation: Confirm public sharing is intended before execution; use restricted sharing when curriculum data should remain private.

Risk: The optional cleanup job recursively deletes old checkpoint directories.

Mitigation: Add the cleanup job only after accepting the retention policy, and test the scoped checkpoint path with a dry run first.

Risk: YouTube resource selection depends on an API key and default language preferences.

Mitigation: Use a scoped YouTube API key and confirm the resource language defaults match the learners.

## Reference(s):

- [Curriculum Designer ClawHub release page](https://clawhub.ai/tarasinghrajput/skills/curriculum-designer)
- [Publisher profile](https://clawhub.ai/user/tarasinghrajput)
- [Google Cloud API credentials](https://console.cloud.google.com/apis/credentials)
- [YouTube oEmbed validation endpoint](https://www.youtube.com/oembed?url=https://youtube.com/watch?v=VIDEO_ID)
- [Curriculum Designer folder](https://drive.google.com/drive/folders/1upJQu-IVmZRJQsNGmJNRzq9IwL67MVL9)
- [Example curriculum](https://docs.google.com/spreadsheets/d/1hYC2Q2KlW8dM71biC97RPSvFnxTQa-zN)
- [SOP document](https://docs.google.com/document/d/1Y5qetW8S4RWsTg7hycIyujgTwTCFn9VV)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON checkpoints, CSV or Google Sheet curriculum data, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses staged checkpoint files for requirements, research results, validated resources, curriculum structure, and final sheet URL.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
