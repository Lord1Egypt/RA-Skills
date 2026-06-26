## Description: <br>
目的地PK对比助手，帮助纠结于多个目的地的用户快速做出决策。输入2-3个候选目的地、出发城市、出行日期，自动生成机票、酒店、景点的多维度对比卡片。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel users use this skill to compare two or three candidate destinations by flights, hotels, attractions, estimated cost, and stated preferences, then receive a concise recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes setup and troubleshooting guidance that can weaken machine or network security, including global CLI installation, sudo use, and disabling TLS certificate verification. <br>
Mitigation: Install the FlyAI CLI only after review, prefer a pinned local or sandboxed install, avoid sudo, and do not use NODE_TLS_REJECT_UNAUTHORIZED=0. <br>
Risk: The skill can read or save travel preferences, budget, family details, and accessibility needs through memory or ~/.flyai/user-profile.md. <br>
Mitigation: Ask for user consent before saving preferences, and review or delete stored memory and ~/.flyai/user-profile.md when reuse is not desired. <br>
Risk: Travel prices, availability, and recommendation inputs can be incomplete or change after the comparison is generated. <br>
Mitigation: Treat generated comparisons as decision support and verify live flight, hotel, and attraction details before booking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hello-ahang/flyai-destination-pk) <br>
- [Core workflow](artifact/reference/core-workflow.md) <br>
- [Tools](artifact/reference/tools.md) <br>
- [Flight search](artifact/reference/search-flight.md) <br>
- [Hotel search](artifact/reference/search-hotel.md) <br>
- [POI search](artifact/reference/search-poi.md) <br>
- [Keyword search](artifact/reference/keyword-search.md) <br>
- [User profile storage](artifact/reference/user-profile-storage.md) <br>
- [Examples](artifact/reference/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with comparison tables, recommendation text, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include travel price ranges, route availability, hotel summaries, attraction counts, and next-step FlyAI commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
