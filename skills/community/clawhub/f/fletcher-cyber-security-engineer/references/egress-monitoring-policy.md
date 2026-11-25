# Egress Monitoring Policy

## Objective

Ensure OpenClaw only opens outbound connections to destinations that have been
reviewed and approved.

## What Is Checked

`scripts/egress_monitor.py` lists established TCP connections and evaluates the
ones that are genuine egress from OpenClaw:

| Filter | Rule |
| --- | --- |
| Scope | Only OpenClaw's own processes: the gateway, processes named `openclaw` / `openclaw-*`, and their child processes. `--scope all` evaluates every process on the host. |
| Direction | Connections accepted on a port the process listens on are inbound and are skipped. |
| Destination | Loopback, link-local, multicast and unspecified addresses are skipped (`--include-local` keeps them). Private LAN addresses are evaluated. |

Every remaining connection must match a rule in
`~/.openclaw/security/egress_allowlist.json`, or it is reported as an
`unapproved-egress` finding.

## Allowlist Format

A JSON array of rules. Every field given in a rule must match.

| Field | Meaning |
| --- | --- |
| `protocol` | `tcp` (default). |
| `port` / `ports` | Remote port, or a list of ports. Omit to allow any port. |
| `command` | Process name, case-insensitive. Omit to allow any OpenClaw process. |
| `host` / `hosts` | Hostname or IP address, or a list. Hostnames are resolved through DNS. |
| `cidr` | Network in CIDR notation, or a list. Use for providers that publish address ranges. |
| `host_regex` | Regular expression tested against the remote IP and the allowlisted hostnames that resolve to it. |
| `comment` | Business justification. Shown as the matched rule in reports. |

A rule with no `host`, `hosts`, `cidr` or `host_regex` allows any destination
on its port, so always include one of them.

Start from `references/egress-allowlist.template.json`.

## Hostname Resolution

The operating system reports remote IP addresses, not names. The monitor
resolves each allowlisted hostname through the system DNS resolver and compares
the answers with the connection's address.

- Answers are remembered for 7 days in
  `~/.openclaw/security/egress-dns-cache.json`, so providers that rotate
  addresses do not cause false findings.
- `--no-resolve` makes no DNS queries and relies on remembered answers only.
- Wildcard hostnames cannot be resolved. Use `cidr` for a provider's published
  ranges instead.

## Reading The Report

`--json` output includes:

- `summary`: connections seen, out of scope, ignored (inbound, local),
  evaluated, allowed and unapproved.
- `processes`: the OpenClaw processes that were in scope.
- `connections`: every evaluated connection, whether it was allowed, and the
  rule that allowed it.
- `findings`: unapproved connections with process, destination and
  recommendation.
- `warnings`: anything that limited the scan (for example, OpenClaw not
  running, a hostname that did not resolve, or an invalid rule).

An empty result when OpenClaw is not running, or is idle, means nothing was
evaluated. It is not evidence that egress is controlled. Check
`summary.evaluated`.

`--fail-on-findings` exits with status 3 when unapproved connections exist, for
use in scheduled jobs and CI.

## Handling Findings

1. Identify the process and destination from the finding.
2. If the destination is expected, add a rule with a `comment` giving the
   business justification.
3. If it is not expected, stop the connection and investigate before approving
   anything.

## Limitations

- The scan is a point-in-time snapshot. Short-lived connections between scans
  are not seen.
- Only TCP is covered.
- Approval is by resolved address. Other services hosted on the same shared
  address as an allowlisted hostname are indistinguishable from it.
