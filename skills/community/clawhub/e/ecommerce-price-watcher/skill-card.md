## Description: <br>
Track product prices across ecommerce sites and alert on offers or target-price hits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pbalajiips](https://clawhub.ai/user/pbalajiips) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to add ecommerce product URL or item-query watches, check prices over time, and generate alert-ready JSON for price drops or target-price hits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Item-query mode sends product search terms to DuckDuckGo. <br>
Mitigation: Use direct product URLs when query disclosure matters, or use --trusted-only with a low --max-results value for tighter control. <br>
Risk: Watched URLs, queries, and price history remain in the local watcher state file until removed. <br>
Mitigation: Remove stale watches and manage or delete the local state file according to the user's retention expectations. <br>
Risk: Price extraction is best-effort and ecommerce sites may block requests or expose changed markup. <br>
Mitigation: Review alert JSON before forwarding notifications, and add store-specific adapters for production monitoring where precision matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pbalajiips/ecommerce-price-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [CLI commands and structured JSON alert payloads, with local watcher state stored as a JSON file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Alert output includes product id, title, old and new price, drop percent when available, URL, and timestamp.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
