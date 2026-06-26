## Description: <br>
行程体检员——验证已有行程方案，输出体检报告：价格/路线/时间/遗漏/风险诊断+优化建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to review an existing itinerary, compare prices and routes, identify schedule and booking risks, and produce a concise improvement report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install or update the global FlyAI CLI package before searching travel data. <br>
Mitigation: Install only if the FlyAI CLI is trusted; prefer a pinned, local, non-sudo installation instead of a global latest-version install. <br>
Risk: The artifact includes fallback guidance to disable TLS verification for SSL certificate problems. <br>
Mitigation: Do not allow TLS verification to be disabled; resolve certificate or network configuration problems before running travel-search commands. <br>
Risk: The skill can read or save travel preferences and may process sensitive itinerary, order, payment, or passport-related details. <br>
Mitigation: Review or opt out of saved travel profiles and redact sensitive order, payment, passport, or identity data before sharing itinerary inputs. <br>
Risk: Booking links are third-party Feizhu handoffs, so prices, availability, and purchase terms can change outside the skill. <br>
Mitigation: Verify prices, availability, refund rules, and booking terms directly on the third-party purchase page before buying. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hello-ahang/flyai-trip-checker) <br>
- [Output template](reference/output-template.md) <br>
- [Complete example](reference/example.md) <br>
- [User profile storage](reference/user-profile-storage.md) <br>
- [Scoring rules](reference/scoring-rules.md) <br>
- [Flight search reference](reference/references/search-flight.md) <br>
- [Hotel search reference](reference/references/search-hotel.md) <br>
- [POI search reference](reference/references/search-poi.md) <br>
- [Train search reference](reference/references/search-train.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown itinerary health-check report with diagnostic sections, recommendations, and booking links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include FlyAI CLI commands, current travel-price comparisons, saved preference prompts, and third-party Feizhu booking handoff links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
