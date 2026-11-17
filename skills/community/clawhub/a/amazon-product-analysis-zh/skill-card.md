## Description:

把一个亚马逊商品链接变成可执行的中文社媒短视频脚本，提炼 Listing 卖点、挖掘评论区真实用户语言，并按用户选定方向产出带依据的分镜脚本。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengyu-xixihaha](https://clawhub.ai/user/chengyu-xixihaha)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and commerce operators use this skill to turn a public Amazon product link into Chinese short-form video strategy notes and a traceable storyboard script. It is intended for product listing analysis, buyer-language mining, and campaign script drafting, not for generating the final video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may browse public Amazon product pages and can be affected by regional page variants, anti-bot pages, or incomplete product data.

Mitigation: Use rendered browser access where available, note uncertain pricing or limited review samples, and avoid presenting unavailable data as verified.

Risk: Using login-required Amazon data or private account information could expose sensitive user data.

Mitigation: Use only public product-page listing and review information, and do not request or operate with Amazon account credentials.

Risk: Generated marketing scripts can overstate product claims if the evidence trail is weak.

Mitigation: Tie each script line to a listing claim or buyer-review phrase and keep unsupported claims out of the final script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengyu-xixihaha/skills/amazon-product-analysis-zh)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance and files such as insights.md and script.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts should preserve the evidence trail from product listing details and review language to each storyboard line.]

## Skill Version(s):

1.0.0 (source: release evidence and config.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
