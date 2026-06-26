## Description: <br>
Formora Survey helps agents create, edit, publish, distribute, and export Formora surveys, polls, and forms, with optional Telegram, Email, QR, X, Google Ads, and Meta Ads distribution guarded by preview, confirmation, and budget controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davideuler](https://clawhub.ai/user/davideuler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and developers use this skill to manage the full lifecycle of Formora surveys: draft questions, preview and edit content, publish only after confirmation, distribute survey links, run guarded ad plans or launches, and export responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured messaging and social credentials can let the agent broadcast survey links to recipients or channels. <br>
Mitigation: Review recipients, generated copy, and channel configuration before broadcast; use least-privilege credentials and only configure channels that should be used. <br>
Risk: Paid ads commands can create live Google Ads or Meta Ads campaigns when credentials are configured and ads are enabled. <br>
Mitigation: Keep FORMORA_ADS_ENABLED=false unless live ads are intended, inspect ads-plan first, require explicit budgets, keep paused creation enabled, and enforce shared daily and weekly caps. <br>
Risk: QR generation may use a third-party QR fallback that receives the published survey URL when local QR support is unavailable. <br>
Mitigation: Install local QR generation support for sensitive links or avoid QR generation when the fallback is not acceptable. <br>


## Reference(s): <br>
- [ClawHub Formora Survey release page](https://clawhub.ai/davideuler/formora-survey) <br>
- [Formora application](https://formora.dev) <br>
- [Formora API endpoint](https://api.formora.dev) <br>
- [Google Ads geo target reference](https://developers.google.com/google-ads/api/reference/data/geotargets) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown guidance, shell commands, JSON summaries, exported CSV or XLSX files, QR images, and distribution copy.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FORMORA_API_KEY; optional credentials enable Telegram, Email, X, Google Ads, and Meta Ads actions.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
