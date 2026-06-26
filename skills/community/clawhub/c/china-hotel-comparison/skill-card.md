## Description: <br>
中国酒店比价 - 专门针对美团、去哪儿、携程、飞猪、途牛等中国本土平台的酒店搜索、价格比较、套餐分析和个性化推荐。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FENGJIANLI0721](https://clawhub.ai/user/FENGJIANLI0721) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to compare China hotel options across Meituan, Qunar, Ctrip, Fliggy, and Tuniu, including price checks, package value analysis, and personalized recommendations. It is intended for travelers planning hotels in China, including family, business, independent, and vacation travel. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill may remember sensitive travel behavior across sessions. <br>
Mitigation: Keep history learning off unless needed, and require clear controls for opt-in, review, deletion, and disabling remembered history before using it with real bookings. <br>
Risk: Family sharing can expose preferences, search history, or travel plans to other users. <br>
Mitigation: Keep family sharing off unless clearly needed, review sharing scope before use, and require user controls for review, deletion, and sharing changes. <br>
Risk: Travel searches can involve payment details, contacts, health needs, or private travel plans. <br>
Mitigation: Avoid entering payment details, contact information, health needs, or private travel plans into the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FENGJIANLI0721/china-hotel-comparison) <br>
- [README](artifact/README.md) <br>
- [Search strategy guide](artifact/search-strategy.md) <br>
- [Price calculation guide](artifact/price-calculation.md) <br>
- [Package value analysis](artifact/package-value-analysis.md) <br>
- [Multi-user management and family sharing](artifact/multi-user-management.md) <br>
- [User history learning](artifact/user-history-learning.md) <br>
- [Shanghai Disney Resort tickets](https://www.shanghaidisneyresort.com/tickets/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown recommendations, comparison tables, analysis templates, and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill normally returns at least five hotel options with prices, platform comparison, total cost, pros and cons, suitability notes, and booking guidance.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
