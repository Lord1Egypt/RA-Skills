## Description:

Generates original Chinese social media copy in a fictional ex-partner clapback style, using a romantic setup, ironic reversal, and absurd everyday details while avoiding real names, identifiable events, and source-text copying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent users use this skill to draft fictional Chinese social media posts in an ex-partner irony style for breakup writing, persona deconstruction, and dark-humor relationship copy. It is intended for generalized fictional subjects and should not target real people or identifiable events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release package includes private maintainer memory and local development metadata.

Mitigation: Remove .workbuddy/ and local workflow notes, then rebuild the release from an explicit allowlist before installing or redistributing.

Risk: Generated copy could become defamatory, personally targeted, or based on fabricated claims if aimed at a real person.

Mitigation: Use only fictional or generalized subjects, replace real names with generic labels, and refuse requests that ask for identifiable people or unverifiable events.

Risk: Generated text could copy protected source phrasing instead of using only the style pattern.

Mitigation: Keep outputs original, use the anonymization boundary in artifact/references/origin.md, and revise any direct source-text echoes.

## Reference(s):

- [Source and Anonymization Notes](artifact/references/origin.md)
- [Runtime Judgment Loop](artifact/runtime.md)
- [Style Fingerprint](artifact/style/fingerprint.md)
- [Golden Set](artifact/tests/golden-set.md)
- [ClawHub Skill Page](https://clawhub.ai/qomob/skills/ex-clapback-writing-style)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown/text with a title or opening hook, body copy, reversal tagline, irony tags, and a brief scoring report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is 300-1200 Chinese characters and uses an internal critique, judge, and revision loop before finalization.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence); artifact frontmatter reports 1.2.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
