## Description: <br>
Looks up Compass real-estate listings, property details, photos, price history, comparable rentals, agent listings, and address resolutions through an MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and real-estate workflows use this skill to query Compass listing information, compare properties, inspect price history and photos, and run local mortgage or affordability calculations from an agent interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the user's signed-in Compass browser session to fetch listing data. <br>
Mitigation: Install and use it only when that session-powered access is acceptable, and keep the browser session scoped to the account intended for the lookup. <br>
Risk: Compass access may be subject to site restrictions, WAF challenges, or terms that limit bulk or commercial use. <br>
Mitigation: Confirm Compass permits the intended use before bulk or commercial workflows, and expect network tools to fail until browser sign-in or WAF challenges are resolved. <br>
Risk: Network-backed listing tools depend on compass-mcp and the fetchproxy browser extension being active. <br>
Mitigation: Run the healthcheck before relying on results; use the local mortgage and affordability tools when Compass session access is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/compass-mcp) <br>
- [npm package: compass-mcp](https://www.npmjs.com/package/compass-mcp) <br>
- [Source: chrischall/compass-mcp](https://github.com/chrischall/compass-mcp) <br>
- [Fetchproxy browser extension](https://github.com/chrischall/fetchproxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown and structured MCP tool responses with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network-backed Compass tools require compass-mcp, the fetchproxy browser extension, and a signed-in Compass browser session; local mortgage and affordability calculators do not require Compass sign-in.] <br>

## Skill Version(s): <br>
0.11.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
