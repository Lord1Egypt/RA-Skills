## Description: <br>
Use Playwright via Bash exec to fetch GasBuddy fuel prices for a target city or area, especially Toronto and North York, and return top station prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mebusw](https://clawhub.ai/user/mebusw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run local Playwright browser automation for GasBuddy station-price lookups and to return sorted fuel-price results for a requested city or area. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Playwright browser automation against GasBuddy pages. <br>
Mitigation: Invoke it only for explicit GasBuddy or station-price lookup requests, review proposed scripts before execution, and avoid account credentials or browser profile data. <br>
Risk: Fuel-price results can be incomplete or stale if the page challenge, lazy loading, or unavailable price placeholders prevent full station extraction. <br>
Mitigation: Wait for the GasBuddy page title to indicate that loading has completed, scroll incrementally, and verify the sorted results before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mebusw/gasbuddy-browser) <br>
- [GasBuddy North York gas prices](https://www.gasbuddy.com/gasprices/ontario/north-york) <br>
- [GasBuddy Toronto gas prices](https://www.gasbuddy.com/gasprices/ontario/toronto) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with JavaScript and shell command guidance plus sorted station-price text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns brand, regular fuel price, and address for the cheapest available stations when page data loads successfully.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
