## Description:

Generates Supabase magic links that land on a custom portal subpath and supplies bridge snippets for token_hash, PKCE, hash-fragment, and auth-error redirects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyagil](https://clawhub.ai/user/dyagil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement Supabase magic-link login flows that land on a custom portal subpath and recover older or fallback redirects that arrive at the site root.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Magic links and token_hash parameters are sensitive login credentials if exposed in logs, analytics, referrers, or shared URLs.

Mitigation: Use HTTPS, avoid logging full URLs, run URL cleanup before analytics or other scripts, and strip auth parameters after verification.

Risk: A Supabase service-role key used to generate links can compromise authentication if exposed outside the server.

Mitigation: Keep the service-role key strictly server-side and use only browser-appropriate credentials in client code.

Risk: Single-use tokens can be replayed on refresh or lost if query and hash parameters are not preserved during redirects.

Mitigation: Remove auth parameters after handling, preserve both query and hash during root redirects, and keep a fallback for older Supabase auth responses without hashed_token.

Risk: PKCE code flows depend on matching browser state and may fail when links are opened in a different browser or in-app WebView.

Mitigation: Use the token_hash magic-link path for cross-browser link delivery and reserve PKCE handling for compatible same-browser flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dyagil/skills/dyagil-magic-link-bridge)
- [portal-bridge.js](artifact/scripts/portal-bridge.js)
- [index-redirect.js](artifact/scripts/index-redirect.js)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with JavaScript snippets and implementation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes drop-in browser scripts and server-side Supabase magic-link guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
