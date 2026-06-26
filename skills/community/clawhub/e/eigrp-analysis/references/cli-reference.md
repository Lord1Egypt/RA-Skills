# EIGRP CLI Reference — IOS-XE / NX-OS

Quick-reference command tables for EIGRP analysis. Commands are organized by
diagnostic category. Classic mode commands are shown first; named mode
equivalents follow where they differ.

> **NX-OS note:** NX-OS uses named EIGRP exclusively (`router eigrp [tag]`).
> The `feature eigrp` command must be enabled before any EIGRP configuration.
> NX-OS always requires VRF context — use `vrf default` for the global table.

## Instance and Process

| Purpose | IOS-XE | NX-OS |
|---------|--------|-------|
| EIGRP process summary | `show ip protocols \| section eigrp` | `show ip eigrp vrf default` |
| EIGRP traffic statistics | `show ip eigrp traffic` | `show ip eigrp traffic vrf default` |
| Verify AS number and K-values | `show ip protocols` | `show ip eigrp vrf default` |
| Named mode process info | `show eigrp address-family ipv4 vrf default` | `show ip eigrp vrf default` |
| EIGRP events log | `show eigrp address-family ipv4 events` | `show ip eigrp events vrf default` |

## Neighbor

| Purpose | IOS-XE | NX-OS |
|---------|--------|-------|
| List all neighbors | `show ip eigrp neighbors` | `show ip eigrp neighbors vrf all` |
| Neighbor detail (SRTT, RTO, Q) | `show ip eigrp neighbors detail` | `show ip eigrp neighbors detail vrf default` |
| Named mode neighbors | `show eigrp address-family ipv4 neighbors` | `show ip eigrp neighbors vrf default` |
| Neighbor uptime and hold time | `show ip eigrp neighbors` | `show ip eigrp neighbors vrf default` |

## Topology Table

| Purpose | IOS-XE | NX-OS |
|---------|--------|-------|
| Full topology table | `show ip eigrp topology` | `show ip eigrp topology vrf default` |
| Specific prefix detail | `show ip eigrp topology [prefix/len]` | `show ip eigrp topology [prefix/len] vrf default` |
| Active routes only | `show ip eigrp topology active` | `show ip eigrp topology active vrf default` |
| All paths (successors + FS) | `show ip eigrp topology all-links` | `show ip eigrp topology all-links vrf default` |
| Zero successors (unreachable) | `show ip eigrp topology zero-successors` | `show ip eigrp topology zero-successors vrf default` |
| Named mode topology | `show eigrp address-family ipv4 topology` | `show ip eigrp topology vrf default` |

## Interface

| Purpose | IOS-XE | NX-OS |
|---------|--------|-------|
| EIGRP-enabled interfaces | `show ip eigrp interfaces` | `show ip eigrp interfaces vrf default` |
| Interface detail (timers, BW) | `show ip eigrp interfaces detail` | `show ip eigrp interfaces detail vrf default` |
| Passive interfaces | `show ip protocols \| section Passive` | `show ip eigrp interfaces vrf default` |
| Interface bandwidth/delay | `show interfaces [intf]` | `show interface [intf]` |
| EIGRP stub status | `show ip eigrp neighbors detail \| include stub` | `show ip eigrp neighbors detail vrf default \| include stub` |

## Redistribution and Filtering

| Purpose | IOS-XE | NX-OS |
|---------|--------|-------|
| External EIGRP routes | `show ip route eigrp \| include EX` | `show ip route eigrp vrf default \| include EX` |
| Redistribute config | `show run \| section router eigrp` | `show run \| section router eigrp` |
| Distribute-list config | `show ip protocols \| section distribute` | `show run \| section router eigrp` |
| Route-map detail | `show route-map [name]` | `show route-map [name]` |
| Prefix-list detail | `show ip prefix-list [name]` | `show ip prefix-list [name]` |
| Offset-list verification | `show ip protocols \| section offset` | `show run \| section router eigrp` |

## Metric and Wide Metric

| Purpose | IOS-XE | NX-OS |
|---------|--------|-------|
| Classic composite metric | `show ip eigrp topology [prefix/len]` | `show ip eigrp topology [prefix/len] vrf default` |
| Wide metric (named mode) | `show eigrp address-family ipv4 topology [prefix/len]` | `show ip eigrp topology [prefix/len] vrf default` |
| RIB-scale factor | `show eigrp address-family ipv4 \| include rib-scale` | `show ip eigrp vrf default` |
| Interface delay in picoseconds | `show eigrp address-family ipv4 interfaces detail` | `show ip eigrp interfaces detail vrf default` |
