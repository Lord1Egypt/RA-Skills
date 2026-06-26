# BGP CLI Reference — Cisco / JunOS / EOS

Commands organized by diagnostic category with all three vendors side by side.
All commands are read-only (show/display only). Cisco commands validated against
IOS-XE 17.3+ and NX-OS 10.2+; JunOS 21.x+; EOS 4.28+.

## Session Management

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Peer summary | `show bgp ipv4 unicast summary` | `show bgp summary` | `show ip bgp summary` |
| Peer detail | `show bgp ipv4 unicast neighbors [addr]` | `show bgp neighbor [addr]` | `show ip bgp neighbors [addr]` |
| Peer state/errors | `show bgp ipv4 unicast neighbors [addr] \| include state\|error\|reset` | `show bgp neighbor [addr] \| match "State\|Error"` | `show ip bgp neighbors [addr] \| include state\|error\|reset` |
| Peer timers | `show bgp ipv4 unicast neighbors [addr] \| include timer\|hold\|keepalive` | `show bgp neighbor [addr] \| match "Holdtime\|Keepalive"` | `show ip bgp neighbors [addr] \| include timer\|hold\|keepalive` |
| Peer capabilities | `show bgp ipv4 unicast neighbors [addr] \| section capabilities` | `show bgp neighbor [addr] \| find "Options"` | `show ip bgp neighbors [addr] \| section capabilities` |
| Message statistics | `show bgp ipv4 unicast neighbors [addr] \| section Message` | `show bgp neighbor [addr] \| match "Messages"` | `show ip bgp neighbors [addr] \| section Message` |

### Session Notes

- **Cisco (IOS-XE vs NX-OS):** IOS-XE uses `show bgp ipv4 unicast`; older IOS uses `show ip bgp`. NX-OS uses `show bgp ipv4 unicast` as well but some outputs differ in format.
- **JunOS:** The `show bgp summary` output lists peer state as text ("Established", "Active", etc.). Prefix count appears as "Accepted" prefixes.
- **EOS:** Output format closely resembles Cisco IOS-XE. `show ip bgp summary` works identically to Cisco's `show ip bgp summary`.

## Route Table

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Full BGP table | `show bgp ipv4 unicast` | `show route protocol bgp` | `show ip bgp` |
| Specific prefix | `show bgp ipv4 unicast [prefix]` | `show route [prefix] detail` | `show ip bgp [prefix]` |
| Best path detail | `show bgp ipv4 unicast [prefix] bestpath` | `show route [prefix] detail` | `show ip bgp [prefix] detail` |
| Received routes (per peer) | `show bgp ipv4 unicast neighbors [addr] routes` | `show route receive-protocol bgp [addr]` | `show ip bgp neighbors [addr] received-routes` |
| Advertised routes (per peer) | `show bgp ipv4 unicast neighbors [addr] advertised-routes` | `show route advertising-protocol bgp [addr]` | `show ip bgp neighbors [addr] advertised-routes` |
| Route count summary | `show bgp ipv4 unicast summary` (PfxRcd column) | `show bgp summary` (Accepted column) | `show ip bgp summary` (PfxRcd column) |
| RIB failure | `show bgp ipv4 unicast rib-failure` | `show route resolution unresolved` | `show ip bgp rib-failure` |

### Route Table Notes

- **Cisco:** `PfxRcd` column in summary shows received prefix count; a text state name means the peer is not Established.
- **JunOS:** `show route protocol bgp` shows active routes only. Use `show route protocol bgp all` to see hidden/rejected routes. The `receive-protocol`/`advertising-protocol` syntax is unique to JunOS.
- **EOS:** Supports `received-routes` only when `soft-reconfiguration inbound` is enabled or with `neighbor [addr] route-reflector-client`.

## Path Attributes

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| AS path | `show bgp ipv4 unicast [prefix]` (AS Path line) | `show route [prefix] detail \| match "AS path"` | `show ip bgp [prefix]` (AS Path line) |
| Local preference | `show bgp ipv4 unicast [prefix]` (localpref line) | `show route [prefix] detail \| match "Local"` | `show ip bgp [prefix]` (localpref line) |
| MED | `show bgp ipv4 unicast [prefix]` (metric line) | `show route [prefix] detail \| match "MED"` | `show ip bgp [prefix]` (metric line) |
| Weight | `show bgp ipv4 unicast [prefix]` (weight line) | *(not applicable — JunOS has no weight)* | `show ip bgp [prefix]` (weight line) |
| Communities | `show bgp ipv4 unicast [prefix]` (community line) | `show route [prefix] detail \| match "Communities"` | `show ip bgp [prefix]` (community line) |
| Extended communities | `show bgp ipv4 unicast [prefix]` | `show route [prefix] extensive` | `show ip bgp [prefix] detail` |
| Origin | `show bgp ipv4 unicast [prefix]` (Origin line) | `show route [prefix] detail` | `show ip bgp [prefix]` (Origin line) |
| Next-hop | `show bgp ipv4 unicast [prefix]` (next hop line) | `show route [prefix] detail \| match "Next hop"` | `show ip bgp [prefix]` (next hop line) |

### Path Attribute Notes

- **Weight:** Cisco and EOS support weight (local to the router, not propagated). JunOS does not implement weight — use local-preference or policy instead.
- **MED comparison:** By default, MED is compared only between paths from the same neighbor AS. Enable `always-compare-med` (Cisco/EOS) or set `path-selection med-always` (JunOS) for cross-AS comparison.
- **Communities:** All three vendors display standard communities. Large communities (RFC 8092) require explicit configuration to display in output.

## Filtering and Policy

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Applied route-map | `show bgp ipv4 unicast neighbors [addr] policy` | `show bgp neighbor [addr] \| match "Import\|Export"` | `show ip bgp neighbors [addr] \| include route-map` |
| Route-map detail | `show route-map [name]` | `show policy [name]` | `show route-map [name]` |
| Prefix-list | `show ip prefix-list [name]` | `show policy-options prefix-list [name]` | `show ip prefix-list [name]` |
| AS-path filter | `show ip as-path-access-list [name]` | `show policy-options as-path [name]` | `show ip as-path-access-list [name]` |
| Community list | `show ip community-list [name]` | `show policy-options community [name]` | `show ip community-list [name]` |
| Filtered routes (inbound) | `show bgp ipv4 unicast neighbors [addr] received-routes` vs `routes` | `show route receive-protocol bgp [addr] all` (includes rejected) | `show ip bgp neighbors [addr] received-routes` (if soft-reconfig enabled) |

### Filtering Notes

- **JunOS default export policy:** JunOS requires an explicit export policy to advertise routes to a BGP peer. Without one, zero prefixes are sent. This is the most common vendor-specific gotcha.
- **Cisco/EOS:** Without an outbound route-map, all routes in the BGP table are advertised (subject to next-hop reachability).
- **Comparing filtered vs unfiltered:** On Cisco/EOS, compare `received-routes` (pre-filter) vs `routes` (post-filter). On JunOS, use `all` flag to see rejected routes alongside accepted ones.

## Convergence and Dampening

| Function | Cisco | JunOS | EOS |
|----------|-------|-------|-----|
| Dampened routes | `show bgp ipv4 unicast dampening dampened-paths` | `show route damping suppressed` | `show ip bgp dampening dampened-paths` |
| Dampening params | `show bgp ipv4 unicast dampening parameters` | `show route damping parameters` | `show ip bgp dampening parameters` |
| Flap statistics | `show bgp ipv4 unicast dampening flap-statistics` | `show route damping history` | `show ip bgp dampening flap-statistics` |
| Update activity | `show bgp ipv4 unicast update-group` | `show bgp group [name] detail` | `show ip bgp update-group` |
| Soft reset (inbound) | `show bgp ipv4 unicast neighbors [addr] received-routes` | `show route receive-protocol bgp [addr]` | `show ip bgp neighbors [addr] received-routes` |
| BGP event log | `show bgp ipv4 unicast neighbors [addr] \| section Event` | `show log messages \| match bgp` | `show ip bgp neighbors [addr] \| section Event` |

### Convergence Notes

- **MRAI (Minimum Route Advertisement Interval):** Cisco and EOS default to 30s for eBGP, 5s for iBGP. JunOS defaults to 0s (immediate advertisements). Lower MRAI = faster convergence but more update churn.
- **Dampening:** Enabled per address-family. Default parameters differ across vendors. Check if dampening is even configured before investigating suppressed routes.
- **Update groups:** Cisco and EOS group peers with identical outbound policy into update groups for efficiency. JunOS uses BGP groups similarly. Update-group churn indicates frequent policy changes.
