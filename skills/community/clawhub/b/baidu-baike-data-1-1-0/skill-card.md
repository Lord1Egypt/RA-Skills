## Description:

The Baidu Baike Component is a knowledge service tool designed to query authoritative encyclopedia explanations for various nouns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyingzhuangk](https://clawhub.ai/user/zhangyingzhuangk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Baidu Baike for encyclopedia entries about people, places, concepts, events, and other nouns. It supports direct title lookup and homonym resolution before returning structured entry data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API key exposure or unintended third-party data sharing when search terms are sent to Baidu's AppBuilder Baike API.

Mitigation: Install only when Baidu Baike is the intended source, provide BAIDU_API_KEY through environment configuration, and avoid submitting sensitive search terms unless appropriate for that service.

## Reference(s):

- [Baidu Baike](https://baike.baidu.com/)
- [Baidu AppBuilder Baike API](https://appbuilder.baidu.com/v2/baike)
- [ClawHub skill page](https://clawhub.ai/zhangyingzhuangk/skills/baidu-baike-data-1-1-0)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; queries send search terms and the API key to Baidu's AppBuilder Baike API.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
