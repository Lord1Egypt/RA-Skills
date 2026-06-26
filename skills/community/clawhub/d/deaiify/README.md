# deAIify

An OpenClaw plugin that removes em-dashes and en-dashes from assistant prose before delivery.

Instead of doing a naive character replacement, deAIify asks an embedded model run to rewrite the affected sentence so the output still reads naturally. If the rewrite fails, the plugin fails open and delivers the original response unchanged.

## What it does

- detects Unicode em-dashes (`\u2014`) and en-dashes (`\u2013`) in assistant replies
- ignores fenced code blocks, inline code, and normal hyphen-minus usage (`-`)
- rewrites only when needed, using `before_agent_reply`
- verifies the rewrite before delivery
- falls back safely if the embedded rewrite does not succeed

## Hooks

- `before_agent_reply`: primary rewrite path
- `message_sending`: last-resort cleanup fallback

## Safety properties

- fail-open on every error path
- no config-driven code execution
- no external network calls beyond the configured model provider
- temporary rewrite session files are removed immediately after use

## Install

```bash
openclaw plugin install deaiify
```

## Optional config

```json
{
  "plugins": {
    "entries": {
      "deaiify": {
        "enabled": true,
        "config": {
          "rewriteTimeoutMs": 15000
        }
      }
    }
  }
}
```

## Development

```bash
npm install
npm run build
npm test
npm run stage-package
```

`npm run stage-package` creates a minimal publishable artifact under `.release/package/` that contains only the runtime files and manifests needed by ClawHub.

## License

MIT
