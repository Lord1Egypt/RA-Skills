## Description: <br>
EcomSeer helps agents search TikTok Shop products, find trending items, analyze influencers, explore shops, track video performance, and review ad insights through EcomSeer APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fly0pants](https://clawhub.ai/user/fly0pants) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce analysts, marketplace operators, and agent users use this skill to retrieve TikTok Shop product, creator, shop, video, and ad data and turn it into bilingual summaries, rankings, comparisons, and research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles an EcomSeer API key and sends research prompts to hosted EcomSeer services. <br>
Mitigation: Use a dedicated or limited API key, avoid submitting confidential business strategy, and install only if you trust EcomSeer with these inputs. <br>
Risk: Deep Research results may be returned as hosted, shareable report links. <br>
Mitigation: Ask the publisher how report links are protected and deleted before using the skill for sensitive work. <br>
Risk: The security review flagged the embedded Deep Research bearer token as something users should review. <br>
Mitigation: Confirm the publisher's rationale for the token and review network behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fly0pants/ecomseer) <br>
- [EcomSeer website](https://www.ecomseer.com) <br>
- [README](README.md) <br>
- [Goods API reference](references/api-goods.md) <br>
- [Product detail API reference](references/api-product-detail.md) <br>
- [Influencer API reference](references/api-influencer.md) <br>
- [Video API reference](references/api-video.md) <br>
- [Shop API reference](references/api-shop.md) <br>
- [Ads API reference](references/api-ad.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with tables, summaries, links, and inline shell or curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce hosted Deep Research report links; API key values should not be printed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
