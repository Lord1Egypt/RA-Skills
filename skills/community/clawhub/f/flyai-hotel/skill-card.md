## Description: <br>
Searches and compares Fliggy hotel listings by destination, landmark proximity, lodging type, dates, star rating, bed type, sorting, and CNY nightly price cap, returning structured results with images and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuckonit](https://clawhub.ai/user/zuckonit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search and compare hotel, homestay, and inn options near destinations or landmarks, apply budget and stay filters, and produce a concise booking handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends hotel destinations, dates, budgets, and filters to the third-party FlyAI/Fliggy service. <br>
Mitigation: Use it only when comfortable sharing those travel search details with that service, and avoid adding sensitive personal information that is not needed for the search. <br>
Risk: Hotel detail links can lead to booking or purchase flows. <br>
Mitigation: Verify price, fees, dates, cancellation terms, and provider details on the linked page before paying. <br>
Risk: A FlyAI API key could be exposed if pasted into shared prompts or logs. <br>
Mitigation: Store API keys in local configuration or secret storage and redact them from logs and screenshots. <br>


## Reference(s): <br>
- [search-hotel reference](artifact/references/search-hotel.md) <br>
- [FlyAI homepage](https://open.fly.ai/) <br>
- [ClawHub skill page](https://clawhub.ai/zuckonit/flyai-hotel) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown responses with command snippets and structured JSON hotel data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hotel images from mainPic and booking links from detailUrl when returned by the service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
