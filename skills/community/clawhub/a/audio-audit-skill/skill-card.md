## Description:

Audits audio and video speech by transcribing it with SenseAudio ASR, scanning for sensitive terms, and producing structured content-review reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwerty0205](https://clawhub.ai/user/qwerty0205)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, reviewers, and content operations teams use this skill to audit audio or video speech for sensitive terms, risky content, speaker-specific issues, and optional semantic concerns before publication or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio or video content is uploaded to SenseAudio for transcription.

Mitigation: Process only recordings that are approved for the external transcription service, and avoid confidential or regulated content without consent and policy review.

Risk: Generated transcripts and audit reports may contain sensitive speech content and are stored locally.

Mitigation: Use a controlled output directory, restrict access to generated files, and delete transcripts and reports when they are no longer needed.

Risk: The SenseAudio API key can be exposed if passed on the command line or printed in logs.

Mitigation: Prefer an environment variable or credential store, avoid echoing or logging the key, and rotate the key if exposure is suspected.

Risk: Keyword-based scanning and ASR-derived text can produce false positives or miss context-dependent issues.

Mitigation: Use human review for medium and high risk findings and apply deeper semantic review where policy decisions depend on context.

## Reference(s):

- [Skill README](artifact/README.md)
- [Usage Guide](artifact/USAGE.md)
- [SenseAudio](https://senseaudio.cn)
- [SenseAudio transcription API endpoint](https://api.senseaudio.cn/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance plus generated JSON audit reports, text summaries, and transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include per-file audit JSON, human-readable audit text, full transcripts, and batch summary JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
