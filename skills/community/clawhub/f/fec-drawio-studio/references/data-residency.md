# Data Residency

Use this checklist when a diagram contains private architecture, unreleased product details, customer data or regulated information.

## Local First

- A `.drawio` file written in the workspace is the safest default artifact because it can be inspected, versioned and opened locally.
- draw.io Desktop export runs on the local machine when the CLI is installed. If the CLI is missing, keep the source file and offer a URL fallback instead of sending the diagram to a cloud converter.
- `diagram-lint.mjs`, `diagram-url.mjs`, `layout-graph.mjs`, `png-embed-fix.mjs` and code scanners run locally. Graphviz is optional and local when installed.

## URL Modes

- Viewer/editor `#R` URLs and `#create=` URLs place compressed diagram content in the URL fragment.
- URL fragments are not sent to ordinary HTTP servers as request paths, but the browser still loads application code from the chosen diagrams.net host.
- Very large diagrams can exceed practical browser URL limits. Fall back to a local `.drawio` file when the URL becomes unwieldy.
- On Windows, open long diagram URLs through a `.url` shortcut file or use the JSON `windowsShortcut` output from `diagram-url.mjs`; passing the URL directly through `cmd start` can lose the fragment.

## External Requests

- Brand CDN symbols require network access when rendered unless embedded as data URIs.
- diagrams.net web editor/viewer loads editor code and assets from the configured host.
- A self-hosted diagrams.net base URL can be passed with `--base-url` when the environment requires a controlled endpoint.
- Existing draw.io MCP App or Tool servers may be useful as preview surfaces, but they are optional and governed by the user's configured host and model provider.

## Handoff Rule

For sensitive diagrams, deliver the local `.drawio` source plus lint results first. Add PNG/SVG/PDF or URL outputs only when the user explicitly needs them and the data boundary is acceptable.
