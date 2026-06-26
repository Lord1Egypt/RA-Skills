## Description: <br>
1688 Shopkeeper helps OpenClaw agents search 1688 products, review bound downstream shops, configure a 1688 access key, and publish selected items to Douyin, Pinduoduo, Xiaohongshu, and Taobao stores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yclovebf-stack](https://clawhub.ai/user/yclovebf-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External merchants and store operators use this skill to source products from 1688, compare candidate listings, inspect bound downstream stores, and publish selected products to supported commerce platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive 1688 access key that can query shops and authorize store operations. <br>
Mitigation: Use a dedicated low-privilege AK where possible, rely on safe secret handling, and rotate the key after testing or if it is pasted into chat. <br>
Risk: Publish commands can create real downstream store listings. <br>
Mitigation: Verify the target shop, selected item IDs, and publish preview before approving a publish command. <br>
Risk: Persisted configuration may keep the AK available beyond the current session. <br>
Mitigation: Avoid production credentials for evaluation, remove stored credentials when no longer needed, and reauthorize or rotate keys after testing. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/yclovebf-stack/1688-shopkeeper) <br>
- [Configure AK guide](references/configure.md) <br>
- [Search workflow guide](references/search.md) <br>
- [Publish workflow guide](references/publish.md) <br>
- [Operations FAQ index](references/FAQ.md) <br>
- [1688 AI app setup](https://air.1688.com/kapp/1688-ai-app/pages/home?from=1688-shopkeeper) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command results containing a markdown field, plus direct Markdown guidance from reference files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and ALI_1688_AK; search results may be stored as local JSON for later publish commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
