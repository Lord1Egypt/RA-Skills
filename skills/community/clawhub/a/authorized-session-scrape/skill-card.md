## Description: <br>
Continues searching and extracting within a user-authorized local browser session after the user logs in, including pagination, site search, tab-by-tab extraction, and post-login discovery without bypassing access controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents supporting authorized users use this skill to continue browser-based extraction after the user completes login, especially for account-only pages, paginated dashboards, filtered search results, and content libraries. It is intended for workflows where plain fetching misses authenticated state and the agent must summarize what was searched, what was found, and what remains unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may view or summarize sensitive pages from a logged-in browser session. <br>
Mitigation: Keep tasks specific, use the skill only where the user has legitimate access, and do not provide passwords, exported cookies, or session tokens. <br>
Risk: The workflow could be misapplied to bypass login or session controls. <br>
Mitigation: Begin only after the user confirms the task, opens the login flow locally, and completes sign-in themselves; do not bypass access controls. <br>
Risk: Authenticated content may remain hidden, partial, or limited by the session. <br>
Mitigation: Verify that the target page, search box, filters, or results are actually visible before extracting, and distinguish authenticated findings from unavailable or manual-only areas. <br>


## Reference(s): <br>
- [Authorized Session Scrape on ClawHub](https://clawhub.ai/1477009639zw-blip/authorized-session-scrape) <br>
- [1477009639zw-blip publisher profile](https://clawhub.ai/user/1477009639zw-blip) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary with provenance notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes searched locations, filters or navigation paths used, strongest results, partial or unavailable areas, and the next click path if continuing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
