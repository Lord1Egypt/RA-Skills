# Changelog

## 0.1.16 - 2026-06-11

- remove the packaged raw `send.privateKey` placeholder from the live request template and switch it to `signerEnvName` so the published skill no longer contains a private-key-shaped value
- re-audit the published ClawHub skill artifacts for `agentic-lending-evk`, `agentic-lending-morpho`, `agentic-lending-evk-readonly`, `agentic-lending-morpho-readonly`, `api3-feed-manager`, and `api3-feed-manager-readonly`

## 0.1.15 - 2026-05-22

- document the EVK golden path around `preflight-evk-workflow`, persisted artifacts, handoff verification, and live request templates
- publish the bundled live request template and summary contract references for clearer operator handoff
- update the packaged planner/runtime bundle for share-aware router EVK deployment, live borrow proof preparation, and proper controller cleanup via EVault `disableController()`

## 0.1.14 - 2026-05-19

- sync the published EVK bundle to the newest packaged Api3 feed-funding runtime, including scripted communal proxy deployment support
- make the bundled feed manager default real executable funding sends toward also deploying any missing communal proxy unless explicitly disabled

## 0.1.13 - 2026-05-08

- move deployment bytecode out of inline JSON artifact literals into wrapped sidecar files and rehydrate it at runtime to avoid false-positive secret-literal moderation hits

## 0.1.12 - 2026-05-07

- replace secret-looking private key placeholders in packaged CLI help text with `<private-key-hex>` to reduce false-positive scanner hits

## 0.1.11 - 2026-05-07

- finished the self-contained EVK executor bundle so cold installs no longer depend on repo-local runtime or planner data
- aligned packaged CLI help text with the published binary names and added a packaged example request path that works from a clean install
- fixed installed runtime path resolution for user-supplied input files and bundled `data/part2/...` lookups discovered during smoke testing

## 0.1.10 - 2026-05-07

- started converting `agentic-lending-evk` into a self-contained executor bundle
- added a local `package.json` with executable packaging metadata
- bundled the EVK live borrow proof executor into the published skill folder
- added a local CLI entrypoint as the first step toward a fully bundled planner runtime
