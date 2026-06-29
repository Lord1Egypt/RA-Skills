## Description: <br>
零配置即装即用，查询全球10大邮轮航线含价格与旺季，覆盖8大邮轮公司皇家加勒比MSC歌诗达等，支持按目的地和风格筛选。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel planners use this skill to search static Chinese-language cruise route information, compare destinations, cruise lines, seasons, starting prices, and read booking or onboard travel tips. It does not make bookings or check live inventory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cruise prices, schedules, availability, ports, and policies may differ from the static reference data. <br>
Mitigation: Verify current details with official cruise lines, OTAs, or travel providers before booking or spending money. <br>
Risk: Users may mistake the skill for a booking or live availability service. <br>
Mitigation: Treat results as planning guidance only; complete purchases and confirm inventory through official providers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/cruise-search) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [cruise_search.py](artifact/scripts/cruise_search.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese-language Markdown text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static local cruise reference data; no live booking, price, schedule, or inventory lookup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
