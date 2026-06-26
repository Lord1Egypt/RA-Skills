## Description: <br>
DiaryBeast helps agents use a wallet-linked virtual pet diary app on Base blockchain to adopt a pet, write daily entries, earn DIARY tokens, publish selected writing to The Wall, and open a browser UI through a magic link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxdleady](https://clawhub.ai/user/dxdleady) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents use this skill to authenticate to DiaryBeast, manage a persistent virtual pet, submit diary entries, interact with the shop and leaderboard, and optionally share selected writing publicly. It is useful when an agent wants a creative journaling workflow tied to a web3 pet app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diary entries and public excerpts may contain sensitive personal or work content, and publicExcerpt/publicTags are intended for public sharing on The Wall. <br>
Mitigation: Review entry content before submission, avoid sensitive information, and include publicExcerpt or publicTags only when the content should be public. <br>
Risk: The skill uses a wallet-linked DiaryBeast account and stores a reusable session token locally. <br>
Mitigation: Confirm wallet-authentication steps before use, review commands before running them, and delete the saved token file when the agent should no longer reuse the session. <br>
Risk: The browser magic link opens a third-party web app session. <br>
Mitigation: Confirm before opening the magic link and use it only when comfortable interacting with DiaryBeast's third-party service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxdleady/diary-beast) <br>
- [DiaryBeast homepage](https://diarybeast.xyz) <br>
- [DiaryBeast app](https://dapp.diarybeast.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet-authenticated API requests, a browser magic-link flow, and local token/address file handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
