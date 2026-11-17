# Artifact Presentation

Read this whenever creating an artifact for user review. Creating a file is not presentation. Complete presentation only when the user has an immediately usable review surface.

## Choose The Transport

Determine whether the agent and user share the same desktop and filesystem before opening anything.

- **Shared local desktop:** Automatically open standalone HTML and return immediately.
- **Shared desktop, HTTP required:** Start the managed background server, then open its URL.
- **Remote, container, SSH, or headless:** Do not present agent-side `127.0.0.1` or `file://` URLs as user-accessible. Use a host-provided forwarded URL, attach rendered screenshots, or provide an artifact link exposed by the AIDE.
- **Unknown environment:** Treat it as remote until access is demonstrated.

Request tool approval when opening a browser requires it. Do not silently skip the attempt merely because the host may prompt. Do not automatically open imported or otherwise untrusted HTML; render it in an isolated browser or use screenshots.

## Open Standalone HTML

Resolve the script path relative to the loaded `design-guide` skill directory. Pass every direction in one invocation:

```bash
python3 <design-guide-skill-dir>/scripts/present-design.py open \
  ".codex/design/<design-id>/direction-a.html" \
  ".codex/design/<design-id>/direction-b.html"
```

The command opens each artifact in a browser tab and exits. It always prints absolute paths and file URLs as diagnostics. Browser-open success means only that the request was accepted; still ask the user to inspect and confirm.

## Serve HTTP Artifacts

Use HTTP only when modules, fetch calls, routing, or browser security rules prevent `file://` operation. The command starts a managed background process and returns:

```bash
python3 <design-guide-skill-dir>/scripts/present-design.py serve \
  ".codex/design/<design-id>/direction-a.html" \
  ".codex/design/<design-id>/direction-b.html"
```

Manage the server from the project root:

```bash
python3 <design-guide-skill-dir>/scripts/present-design.py status
python3 <design-guide-skill-dir>/scripts/present-design.py stop
```

The server binds only to loopback, records state under `.codex/design/presentation.json`, and serves multiple artifacts from one directory. Stop it after review unless the approved implementation still needs it. If the project already has a development server, open its host-accessible URL instead.

## Present Other Artifacts

- Attach images or screenshots when the host supports image output.
- Show the rendered reference board or diagram instead of only its source file.
- Provide playable motion output in a supported format.
- Label every direction so artifacts map unambiguously to the direction descriptions.

## Apply Fallbacks

Use the first fallback that the user can actually access:

1. A host-provided or forwarded HTTP URL.
2. An AIDE artifact link or a clickable absolute path on a shared filesystem.
3. Attached desktop and mobile screenshots.
4. A concise explanation of the limitation and one exact manual opening action.

Never provide only a relative path. Never treat an agent-local loopback URL as usable in a remote session. Never claim the user saw an artifact merely because an open command succeeded.

## Verify Before Confirmation

Before asking for approval:

- Confirm that the chosen review surface is accessible from the user's environment.
- Inspect the rendered artifact at the required viewports.
- Check local assets and primary interactions.
- State what was opened or attached and retain an accessible fallback.
- Keep the background server reachable until confirmation, then stop it.

Only then ask the user to approve, choose, or propose changes. If no usable presentation path exists, report the blocker instead of treating the confirmation gate as active.
