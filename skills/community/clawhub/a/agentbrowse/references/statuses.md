# AgentBrowse Failure Recovery

## Browser Session

- `browser_launch_failed`
  The runtime could not start a browser. Check launch permissions or switch to
  `attach`.
- `browser_attach_failed`
  The provided CDP endpoint is unavailable or invalid.
- `browser_connection_failed`
  The current browser session can no longer be reached. Reconnect, then
  observe again.

## Page Interaction

- `stale_target`
  The page changed and the saved ref no longer matches. Run `observe` again.
- `navigation_failed`
  Direct navigation did not reach the expected page. Inspect the current state
  before retrying.
- `observe_failed`
  AgentBrowse could not read the current page reliably. Check `browser-status`,
  reconnect if needed, then retry.
