---
name: codex-image-server
description: Use when a user wants to turn local Codex image_generation capability into a local HTTP image server for apps such as Photoshop plugins, design tools, or internal image workflows. Covers adding routes, multi-image generation, cancellation, original reference images, gpt-image-2 size limits, and validation.
---

# Codex Image Server

Use this skill to help a user expose local Codex image generation as a local HTTP API that another app can call.

## Workflow

1. Inspect the target Codex installation or source repo.
2. Prefer a wrapper service around `codex exec` when the installed Codex package should stay untouched.
3. Add a local HTTP server with these routes:
   - `GET /healthz`
   - `GET /v1/capabilities`
   - `POST /v1/images/generate`
   - `GET /v1/images/:id/file`
4. Keep authentication optional by default for loopback use. Do not require an API key unless the target app explicitly needs one.
5. Pass references as original image files through Codex image inputs. Avoid sampling or screenshot downscaling.
6. Support up to 4 images per request. Run workers concurrently, and make each candidate distinct.
7. Wire cancellation through `AbortSignal`. If the HTTP client disconnects or cancels, terminate the full `codex exec` process group.
8. Validate gpt-image-2 custom sizes:
   - longest edge <= 3840
   - total pixels between 655360 and 8294400
   - width and height multiples of 16
   - aspect ratio <= 3:1
9. Store generated files in a stable output directory and return both metadata and file URLs.
10. Run the verification checklist before reporting completion.

## References

- Read `references/http-contract.md` before implementing the API surface.
- Use `templates/codex-image-server.js` as a concrete Node server template when the target repo has no implementation.
- Use `scripts/smoke-test.mjs` to check health, capabilities, and cancellation after the server starts.

## Verification

Run these checks against the local server:

```bash
node scripts/smoke-test.mjs http://127.0.0.1:17341
```

Then test the consuming app:

```bash
curl -sS http://127.0.0.1:17341/v1/capabilities
curl -sS -m 3 http://127.0.0.1:17341/v1/images/generate \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"cancel test","count":4,"size":"1024x1024","quality":"low"}' || true
ps aux | rg -i 'codex exec|codex-image-server'
```

The process check should not show leftover `codex exec` workers after cancellation.
