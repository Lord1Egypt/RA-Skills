## Description: <br>
酒店聚合助手整合分贝通、携程、美团、同程、华住会、锦江等酒店数据源，帮助用户统一搜索酒店、查看房型和比较价格。 <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search hotels across multiple providers, compare source-specific prices, and format aggregated hotel results. Current evidence indicates the provider search methods are scaffolded, so users should verify availability and prices directly with the provider before relying on results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel prices, availability, and provider results may be incomplete or stale because the provider-specific search methods are scaffolded. <br>
Mitigation: Verify prices and availability directly with the hotel or travel provider before booking or making travel decisions. <br>
Risk: The skill describes booking support, but evidence indicates booking is not actually implemented. <br>
Mitigation: Do not submit payment, account, traveler, or booking details through this skill; complete booking only through the provider's official channel. <br>
Risk: Searches may send city, date, and keyword information to third-party travel providers. <br>
Mitigation: Avoid entering sensitive personal data in search fields and review provider data-handling requirements before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ryan-zry/easy-travel-booking) <br>
- [Fenbeitong Open API](https://openapiv2.fenbeitong.com) <br>
- [Ctrip API Endpoint](https://api.ctrip.com) <br>
- [Meituan API Endpoint](https://api.meituan.com) <br>
- [Tongcheng API Endpoint](https://api.tongcheng.com) <br>
- [Huazhu API Endpoint](https://api.huazhu.com) <br>
- [Jinjiang API Endpoint](https://api.jinjiang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, API Calls, guidance] <br>
**Output Format:** [Markdown tables and JSON-like API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Formats aggregated hotel search results and exposes OpenAI function-call schemas for hotel search, hotel detail lookup, and result formatting.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
