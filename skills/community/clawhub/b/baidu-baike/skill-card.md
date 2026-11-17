## Description:

The Baidu Baike Component is a knowledge service tool designed to query authoritative encyclopedia explanations for various nouns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiduqianfangroup](https://clawhub.ai/user/baiduqianfangroup)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to retrieve Baidu Baike encyclopedia entries for objectively existing nouns such as people, places, concepts, events, and things. It can search by title, search by Baike lemma ID, or list possible entries for a title.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime must have access to a Baidu API key and outbound network access to Baidu AppBuilder.

Mitigation: Install and run the skill only in environments where this credential and network access are approved.

Risk: Search terms are sent to Baidu as part of normal operation.

Mitigation: Avoid submitting sensitive, confidential, or regulated text as lookup terms unless that use is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baiduqianfangroup/skills/baidu-baike)
- [Baidu Baike](https://baike.baidu.com/)
- [Baidu AppBuilder Baike lemma content API](https://appbuilder.baidu.com/v2/baike/lemma/get_content)
- [Baidu AppBuilder Baike lemma list API](https://appbuilder.baidu.com/v2/baike/lemma/get_list_by_title)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON responses from the Baidu Baike API with Markdown setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a BAIDU_API_KEY environment variable; sends search terms to Baidu AppBuilder.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
