## Description:

Compare publicly visible Douyin product and shop pages through an existing browser and turn observed prices, labels, reviews, and product selling points into a structured research table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Content creators and commerce researchers can compare publicly visible Douyin product and shop information, then use the results to guide product selection and content ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser access may use the wrong account or environment, or expose account and browser data to an unsuitable bridge.

Mitigation: Review bridge installation and permissions, select the intended browserId, and stop if the page requests login or security verification.

Risk: Research may be mistaken for a quality endorsement or may report changing values as definitive.

Mitigation: Report only values visible on the page, preserve source links and collection times, and label sales or review signals as displayed rather than official quality conclusions.

## Reference(s):

- [EasyBR AI operation guide](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)
- [EasyBR download page](https://www.ebrower.com/down.html)
- [Easy WebBridge source repository (GitHub)](https://github.com/aiispower/easy-webbridge)
- [Easy WebBridge source repository (Gitee)](https://gitee.com/xxjrq/easy-webbridge)

## Skill Output:

**Output Type(s):** [Files, Analysis, Guidance]

**Output Format:** [JSON product data, CSV comparison table, and Markdown research report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes observed source links and collection times; unknown fields are marked rather than inferred.]

## Skill Version(s):

1.0.3 (source: package.json and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
