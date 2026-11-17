---
name: apache-aiops
slug: apache-aiops
displayName: "Apache AIops"
summary: "Governed Apache HTTP Server config, virtual-host, module and HTTP diagnosis."
license: MIT
homepage: https://github.com/AIops-tools/Apache-AIops
tags: [aiops, mcp, governance, apache, httpd]
description: >
  Use this skill when a user needs to inspect or diagnose Apache HTTP Server, verify config syntax, inspect parsed virtual hosts and modules, read configured mod_status metrics, an error log or access-log status summary, or perform a guarded graceful reload. It requires local apachectl access.
installer:
  kind: uv
  package: apache-aiops
argument-hint: "[Apache target or vhost symptom]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["uvx"]},"optional":{"env":["APACHE_AIOPS_CONFIG"]},"homepage":"https://github.com/AIops-tools/Apache-AIops","emoji":"🪶","os":["macos","linux"]}}
---

# Apache AIops

Start with `apache-aiops diagnose` for version, syntax, virtual hosts, modules and optional HTTP status. Use `apache-aiops vhosts` when a request reaches the wrong site, and `apache-aiops config-check` when a reload fails. `apache-aiops init` configures a local target; `apache-aiops doctor` checks `apachectl` access.

Read `failedProbes`, `unhealthyProbes`, `complete` and `healthy` before summarizing results. A completed HTTP probe can report an unhealthy response without a probe error: then `unhealthyProbes` contains `http` and `healthy` is `false`. `healthy` is `null` when HTTP was not configured or the result is incomplete; `complete: true` alone does not mean the service is healthy. Use `config-includes`, `compiled-modules` and `static-directives` to inspect config sources and build features. The MCP server registers 14 Apache reads, one guarded reload and two governance tools. Reload has dry-run; a returned command is still `outcomeUnknown` until the target is checked. See [guardrails](references/agent-guardrails.md) and [capabilities](references/capabilities.md).
