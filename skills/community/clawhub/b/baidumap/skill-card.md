## Description:

Baidumap is an alias entry for the baidu-map skill that gives agents a quick reference for Baidu Maps Open Platform, including BD-09 coordinates, API domains, and key application guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when selecting or integrating Baidu Maps, checking Baidu Maps Open Platform basics, or diagnosing coordinate-offset issues caused by mixing BD-09, GCJ-02, and WGS-84 coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coordinate-system mixups can cause Baidu Maps locations to appear hundreds of meters away from the intended position.

Mitigation: Confirm whether coordinates are BD-09, GCJ-02, or WGS-84, and use Baidu's official coordinate conversion service when sending external coordinates to Baidu Maps.

Risk: The source skill is Chinese-first, which may make key integration caveats harder for non-Chinese readers to apply correctly.

Mitigation: Use translation, consult the main baidu-map skill for fuller guidance, and verify details against Baidu Maps Open Platform documentation.

## Reference(s):

- [Baidu Maps Open Platform](https://lbsyun.baidu.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reference guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable behavior; provides quick-reference guidance and links.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
