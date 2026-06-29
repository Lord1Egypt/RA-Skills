## Description: <br>
Guides agents through AARRR Pirate Metrics funnel audits to define product-specific growth stages, compare conversion rates against benchmarks, identify the bottleneck, and propose the next experiment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, founders, growth teams, product managers, and operators use this skill to audit a product's Acquisition, Activation, Retention, Referral, and Revenue funnel, build shared instrumentation, identify the load-bearing growth bottleneck, and choose one measurable follow-up experiment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce misleading growth recommendations if funnel stages, activation events, or benchmark comparisons are based on incomplete or low-volume data. <br>
Mitigation: Validate that each stage has a product-specific measurable event, compare rates against relevant domain benchmarks, and treat the proposed experiment as a hypothesis to re-measure. <br>
Risk: The security scan notes no hidden destructive behavior, exfiltration, or persistence, but generated recommendations may still influence business decisions. <br>
Mitigation: Review recommendations before acting on them and use the skill's pre-committed metric, threshold, and time-window checks before scaling changes. <br>


## Reference(s): <br>
- [Sources - aarrr-pirate-metrics](references/sources.md) <br>
- [Dropbox Referral Program Example](examples/dropbox-referral-program-2009.md) <br>
- [Startup Metrics for Pirates](https://www.slideshare.net/dmc500hats/startup-metrics-for-pirates-long-version) <br>
- [Dropbox Form S-1](https://www.sec.gov/Archives/edgar/data/1467623/000119312518055809/d451946ds1.htm) <br>
- [Sequoia Capital Dropbox Case Studies](https://www.sequoiacap.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown funnel audit with stage definitions, conversion comparisons, bottleneck identification, and experiment recommendation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask step-by-step questions before producing the audit when the user's funnel inputs are incomplete.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
