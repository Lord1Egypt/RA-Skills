## Browser and non-DCC route

Browser work remains inside DCC-CUA. Use the Host's typed browser surface and
`browser_dom` capabilities, not an in-app Browser or Chrome plugin.

- Bind the exact browser PID and window handle first.
- Bind the exact tab/target returned by DCC-CUA; do not infer it from a title
  alone when an exact target identifier exists.
- Keep connection-scoped sessions and capabilities on one Host connection.
- Use DOM/semantic references from the latest observation rather than stale
  coordinates.
- `browser_prepare` and existing-profile attachment require both the Host grant
  and the session task grant advertised by the runtime contract.
- Authentication challenges, CAPTCHAs, purchases, account/security changes,
  and unexpected permission prompts remain trusted human boundaries.

