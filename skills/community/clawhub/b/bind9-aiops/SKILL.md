---
name: bind9-aiops
slug: bind9-aiops
displayName: "BIND 9 AIops"
summary: "Governed BIND 9 DNS service, zone, DNSSEC and SOA diagnosis."
license: MIT
homepage: https://github.com/AIops-tools/BIND9-AIops
tags: [aiops, mcp, governance, bind9, dns]
description: >
  Use this skill when a user needs to inspect a BIND 9 DNS server, validate zones, diagnose SERVFAIL, inspect DNSSEC and stale-answer status, compare SOA serials, or request a zone reload, refresh, secondary retransfer, NOTIFY resend or name-specific cache flush. It requires local rndc, named-checkconf and dig utilities and appropriate server-side permissions.
installer:
  kind: uv
  package: bind9-aiops
argument-hint: "[DNS zone or record name]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["uvx"]},"optional":{"env":["BIND9_AIOPS_CONFIG"]},"homepage":"https://github.com/AIops-tools/BIND9-AIops","emoji":"🌐","os":["macos","linux"]}}
---

# BIND 9 AIops

Start with `bind9-aiops diagnose <zone>` to correlate service, config, zone, SOA and DNSSEC checks. Use `bind9-aiops compare-soa <zone> <secondary>` when a secondary may be stale. Run `bind9-aiops init` to configure a target and `bind9-aiops doctor` to test `rndc` access.

Check `rcode`, `error`, `complete`, `failedProbes` and `serialsMatch`. `serialsMatch: null` means the comparison could not be made. Do not report SERVFAIL as an empty zone or an equal serial. Use `fetch-limits`, `security-roots`, `tcp-timeouts` and `signing-status` for recursive and DNSSEC incidents. The MCP server has 16 DNS reads, five writes and two governance tools. Writes support dry-run and report `outcomeUnknown` on accepted-but-unproven or lost-response paths; inspect BIND before retrying. See [guardrails](references/agent-guardrails.md) and [capabilities](references/capabilities.md).
