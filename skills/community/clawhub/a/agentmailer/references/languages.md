# SDK language guide

The canonical generated sources live in the AgentMailer plugin monorepo:

| Language | Source | Primary client |
| --- | --- | --- |
| TypeScript | `sdk/typescript` | `AgentMailerClient` |
| Python | `sdk/python` | `AgentMailer` |
| Rust | `sdk/rust` | generated crate client |
| Ruby | `sdk/ruby` | generated gem client |
| Go | `sdk/go` | generated module client |
| Swift | `sdk/swift` | generated package client |

TypeScript and Python also export `AgentMailerWorkflows`, which provides complete inbox pagination, retry-safe inbox creation, explicit text sending, and public A2A discovery. Prefer generated resource clients when the maintained helper does not cover the required API.

Use `request_options` or the language-equivalent request configuration for bounded retries and timeouts. Only retry operations that are read-only or protected by a stable idempotency key. Preserve structured API errors so callers can distinguish authentication, authorization, validation, rate limiting, and delivery state.
