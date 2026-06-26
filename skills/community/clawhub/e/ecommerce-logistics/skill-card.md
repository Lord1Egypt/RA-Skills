## Description: <br>
Aggregates ecommerce order logistics from Taobao and Pinduoduo with QR login, persistent cookie storage, in-transit filtering, and command-line queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charles-lpf](https://clawhub.ai/user/charles-lpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query shopping-platform order logistics, reuse authenticated sessions, and view currently in-transit shipments from supported ecommerce accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill logs into shopping accounts, reuses stored sessions, and writes cookie data and QR screenshots locally. <br>
Mitigation: Use a dedicated data directory with restricted file permissions, treat the directory as sensitive, and remove stored session files and QR images when they are no longer needed. <br>
Risk: Stealth browser automation and all-platform or headless runs can create account, privacy, and platform-policy risk. <br>
Mitigation: Run only against accounts and platforms where this automation is acceptable, prefer explicit platform selection, and review the site terms and operational impact before use. <br>
Risk: Douyin debug output may write shopping-page screenshots or HTML to disk. <br>
Mitigation: Remove the Douyin debug file writes before using that adapter or avoid running Douyin queries. <br>


## Reference(s): <br>
- [Selector Reference](references/selectors.md) <br>
- [ClawHub skill page](https://clawhub.ai/charles-lpf/ecommerce-logistics) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Terminal text with command examples and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local cookie JSON files and QR-code screenshots in the configured data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
