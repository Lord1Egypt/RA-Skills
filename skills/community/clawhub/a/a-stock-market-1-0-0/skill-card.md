## Description: <br>
Provides real-time A-share stock market quotes for individual stocks and indices by code using a public finance API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niceNASA](https://clawhub.ai/user/niceNASA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can query A-share stock and index symbols from the command line to retrieve current price, open, high, low, previous close, volume, and turnover information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried stock symbols are sent to a public Tencent Finance endpoint. <br>
Mitigation: Install only if that network disclosure is acceptable, and avoid querying sensitive watchlists in environments where symbol disclosure is a concern. <br>
Risk: The optional installation flow creates a persistent system-wide command with sudo. <br>
Mitigation: Inspect the script first, or run the Python file directly when a persistent command is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/niceNASA/a-stock-market-1-0-0) <br>
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text terminal output with stock quote fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts one or more Shanghai or Shenzhen stock or index symbols.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
