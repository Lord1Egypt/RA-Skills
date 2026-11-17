## Description:

Turns user-provided product clips into short advertising videos with generated copy, voiceover, and subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yysws5566](https://clawhub.ai/user/yysws5566)

### License/Terms of Use:

MIT-0

## Use Case:

External users creating e-commerce and social-feed ads can turn authorized product clips into short video variants with advertising copy, voiceover, subtitles, and a local advertising-language check. Users should review asset rights, claims, and each final video before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment advises considering external processing of narration, copy, and campaign metadata.

Mitigation: Review the configured voice and language services before use, and avoid sending sensitive campaign information unless that processing is acceptable.

Risk: The security assessment flags local editing-project discovery.

Mitigation: Review the files available to the workflow and keep unrelated editing projects outside its working environment.

Risk: The security assessment flags a duplicate-detection evasion capability.

Mitigation: Check the destination platform's rules before using generated variants and do not publish them until their use is confirmed to comply.

Risk: The security assessment is incomplete: two of 122 components were partially inspected and tool-poisoning analysis was degraded.

Mitigation: Treat the scan as incomplete and arrange additional review of the remaining components and tool behavior before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yysws5566/skills/adflow-infoflow-video)
- [Copywriting playbook](artifact/references/copywriting-playbook.md)
- [Compliance guidance](artifact/references/compliance.md)
- [Voice setup guide](artifact/references/tts-setup.md)
- [Engine reference](artifact/references/engine-reference.md)

## Skill Output:

**Output Type(s):** [MP4 video files, Advertising copy and voiceover scripts, Subtitles, Compliance check results, Shell commands and setup guidance]

**Output Format:** [Rendered short videos with subtitles, plus text and compliance results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce multiple variants from user-provided campaign material.]

## Skill Version(s):

1.4.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
