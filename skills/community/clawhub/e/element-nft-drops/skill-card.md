## Description: <br>
Guides agents through Element NFT drop lifecycle work, including listing and previewing drops, creating and configuring collections, updating settings or media, and publishing, pausing, or resuming drops after preview and confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[element-som](https://clawhub.ai/user/element-som) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and developers use this skill to create, configure, preview, update, publish, pause, and resume Element NFT drops while preserving confirmation gates for wallet and transaction actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires wallet authority through ELEMENT_WALLET_PRIVATE_KEY and can create, update, publish, pause, or resume NFT drops. <br>
Mitigation: Use a dedicated low-risk wallet, provide the private key only through the documented environment variable, and review the preview before any state-changing command. <br>
Risk: Confirmed create, update, or publish flows can broadcast blockchain transactions or mutate Element data. <br>
Mitigation: Confirm the exact chain, slug, symbol, and transaction summary before execution; treat preview mode as the required checkpoint. <br>
Risk: Advanced utilities may authenticate, expose sensitive authorization material in output, mutate Element data, or broadcast transactions. <br>
Mitigation: Avoid verify-ref-graphql, create-token, and post-create-collection unless the code and intended action have been reviewed. <br>
Risk: Media upload paths could accidentally target sensitive local files if user input is careless. <br>
Mitigation: Upload only user-provided NFT media images and keep the documented upload guard restrictions for absolute paths, image extensions, file type checks, and symlink rejection. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/element-som/element-nft-drops) <br>
- [Create Stage Reference](artifact/references/create.md) <br>
- [List Stage Reference](artifact/references/list.md) <br>
- [Preview Stage Reference](artifact/references/preview.md) <br>
- [Update Stage Reference](artifact/references/update.md) <br>
- [Publish Stage Reference](artifact/references/publish.md) <br>
- [Element Drop Web Editor](https://element.market/collections/your-slug/edit/drop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [State-changing flows require preview output and explicit confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
