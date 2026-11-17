## Description:

Look up word etymology, historical sound changes, language family trees, and word evolution through the dr.eamer.dev etymology and diachronic linguistics API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukeslp](https://clawhub.ai/user/lukeslp)

### License/Terms of Use:


## Use Case:

Developers, writers, and language researchers use this skill to query word origins, historical forms, etymology chains, cognates, language family context, and documented sound changes through the dr.eamer.dev API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup terms, language parameters, and any configured DREAMER_API_KEY are shared with api.dr.eamer.dev.

Mitigation: Avoid submitting sensitive private text as lookup terms and handle the API key as a secret.

Risk: The skill depends on a third-party external API for results.

Mitigation: Confirm that using api.dr.eamer.dev is acceptable for the intended workflow before deployment.

## Reference(s):

- [Geepers Etymology ClawHub Page](https://clawhub.ai/lukeslp/skills/geepers-etymology)
- [dr.eamer.dev Etymology API](https://api.dr.eamer.dev)
- [Word Etymology Endpoint Example](https://api.dr.eamer.dev/v1/etymology/word?word=serendipity)
- [Explore Word History Endpoint Example](https://api.dr.eamer.dev/v1/etymology/explore?word=knight&lang=en)
- [Sound Change Rules Endpoint Example](https://api.dr.eamer.dev/v1/etymology/sound-changes?from=proto-indo-european&to=english)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands]

**Output Format:** [Markdown with inline HTTP request examples and bash environment configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DREAMER_API_KEY for authenticated API access; lookup terms and language parameters are sent to api.dr.eamer.dev.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
