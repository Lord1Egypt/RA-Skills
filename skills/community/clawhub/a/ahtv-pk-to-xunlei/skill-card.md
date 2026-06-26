## Description: <br>
Find 安徽网络电视台《快乐无敌大PK》 full-episode pages from a user-provided date expression, extract each episode's real video URL, and save the episodes into 迅雷云盘. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volumexxx](https://clawhub.ai/user/volumexxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent to resolve one or more 快乐无敌大PK episode dates, extract the matching AHTV media URLs, and add those files to the user's Xunlei Cloud account with deterministic filenames. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may require an SMS login and can add, move, or rename files in a logged-in Xunlei Cloud account. <br>
Mitigation: Verify the browser is on the real Xunlei domain before entering SMS codes, and review the final added, skipped, moved, and renamed file list. <br>
Risk: AHTV page structure or episode availability can change, causing missing or ambiguous episode resolution. <br>
Mitigation: Use the resolver status values as authoritative for each date and report unresolved items instead of fabricating episode or media URLs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/volumexxx/ahtv-pk-to-xunlei) <br>
- [AHTV 快乐无敌大PK channel](https://www.ahtv.cn/pindao/ahzh/pk) <br>
- [Xunlei Cloud](https://pan.xunlei.com/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, markdown, guidance] <br>
**Output Format:** [Compact Markdown containing a JSON-like summary of resolved dates, add outcomes, URLs, filenames, and messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses resolver JSON as the source of truth and reports added, skipped, not-found, and failed items.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
