## Description: <br>
Plans travel for live events by confirming event details and combining Xiaohongshu guide research with Fliggy/FlyAI ticket, flight, hotel, and attraction search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chgufan](https://clawhub.ai/user/chgufan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to plan trips around concerts, conventions, sports events, performances, and similar offline events. It helps confirm event timing and venue, gather timely venue and local tips, compare ticket and travel options, and produce an itinerary with booking links when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can change the local environment by installing or upgrading command-line dependencies. <br>
Mitigation: Review the setup steps before running them, or perform installation manually in an isolated environment. <br>
Risk: Xiaohongshu login can reuse browser session cookies. <br>
Mitigation: Prefer QR login when possible and do not paste raw cookies into chat or logs. <br>
Risk: FlyAI search and booking results can include prices, availability, and purchase links that may change. <br>
Mitigation: Verify prices, availability, and booking links directly before purchasing, and do not paste API keys into chat. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chgufan/event-travel-planner) <br>
- [Xiaohongshu CLI reference](artifact/references/xhs_cli.md) <br>
- [FlyAI CLI reference](artifact/references/flyai_cli.md) <br>
- [Setup guide](artifact/references/setup_guide.md) <br>
- [xiaohongshu-cli project](https://github.com/jackwener/xiaohongshu-cli) <br>
- [FlyAI console](https://flyai.open.fliggy.com/console) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, HTML, shell commands, configuration] <br>
**Output Format:** [Markdown travel plan with booking links, optional HTML file, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live search results, images, booking URLs, itinerary tables, setup checks, and authentication guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
