---
name: latency-dashboard
description: The on-call latency dashboard is the first place to check after request-path changes
type: external-reference
---

The team watches the request latency dashboard first when debugging issues in the request path.

Why:
It is the fastest way to tell whether a change affected tail latency or regional error spikes.

How to apply:
If you modify routing, middleware, persistence on the hot path, or request fan-out behavior, check the latency dashboard before calling the change safe.
