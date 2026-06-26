## Description: <br>
Beike Xiaoqu Research helps agents collect Beike housing community data through mcp-chrome, analyze single communities or regional candidate lists, and optionally produce consensus ranking reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddiexux](https://clawhub.ai/user/eddiexux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and real-estate researchers use this skill to gather Beike xiaoqu details, discover district-level housing candidates, and compare options against stated purchase requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a Chrome tab through mcp-chrome and may operate in a browser session that contains user state. <br>
Mitigation: Use a dedicated browser profile or Beike-only tab where possible, and review browser actions before relying on the results. <br>
Risk: The skill saves Beike-derived research files locally, which may include location preferences, candidate communities, and purchase criteria. <br>
Mitigation: Choose a controlled output directory, review generated files after each run, and remove sensitive outputs when they are no longer needed. <br>
Risk: Consensus mode can share budget, location preferences, and candidate data with the PAL/model provider configured by the user. <br>
Mitigation: Enable consensus mode only when sharing that information with the configured provider is acceptable. <br>


## Reference(s): <br>
- [mcp-chrome API reference](references/mcp-chrome-api.md) <br>
- [mcp-chrome project](https://github.com/hangwin/mcp-chrome) <br>
- [ClawHub skill page](https://clawhub.ai/eddiexux/beike-xiaoqu-research) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Files, Guidance] <br>
**Output Format:** [Terminal summaries, JSON data files, CSV candidate lists, and optional Markdown consensus reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Beike-derived files to a local output directory; consensus mode depends on the user's configured PAL/model provider.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
