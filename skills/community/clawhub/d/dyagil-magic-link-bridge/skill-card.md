## Description: <br>
Generate Supabase magic-links that land directly on a custom portal subpath instead of being silently rewritten to the project Site URL by Supabase's redirect whitelist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyagil](https://clawhub.ai/user/dyagil) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to implement Supabase magic-link flows that land on a portal subpath, preserve auth state across redirects, and recover older links that arrive at the site root. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The flow involves login links and a Supabase service-role key. <br>
Mitigation: Keep the service-role key only on a trusted backend and protect, rate-limit, and audit the link-generation endpoint. <br>
Risk: Auth tokens or one-time token parameters can remain visible to analytics, third-party scripts, or browser refreshes if the snippets are installed late or incompletely. <br>
Mitigation: Place the redirect and portal snippets before analytics or third-party scripts, then remove token parameters promptly after handling them. <br>
Risk: PKCE code flows can fail when the link is opened in a different browser from the one that initiated auth. <br>
Mitigation: Use the token_hash magic-link path for links that may be opened in another browser or in-app WebView. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dyagil/dyagil-magic-link-bridge) <br>
- [Portal Bridge Script](scripts/portal-bridge.js) <br>
- [Index Redirect Script](scripts/index-redirect.js) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with JavaScript code snippets and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces drop-in browser scripts and server-side link-generation guidance for Supabase auth flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
