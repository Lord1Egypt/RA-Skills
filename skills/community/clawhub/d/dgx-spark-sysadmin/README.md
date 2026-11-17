# DGX Spark Remote Sysadmin

## Short description

Safely administer single- and multi-node NVIDIA DGX Spark systems from a remote OpenClaw agent.

## Overview

DGX Spark Remote Sysadmin gives an OpenClaw agent a disciplined operating procedure for managing NVIDIA DGX Spark / GB10 systems without assuming a particular hostname, address range, topology, username, workload, or deployment stack.

It covers the full remote-administration lifecycle: establishing SSH and Tailscale access, configuring a dedicated ConnectX-7 fabric between systems, monitoring unified memory and performance, reducing unnecessary resource use, restarting distributed workloads, performing rolling reboots, and applying coordinated DGX OS, driver, CUDA, firmware, and container-stack updates.

The skill emphasizes evidence-led operations. It separates **started**, **ready**, and **functionally healthy** states; requires verification on every participating node; and preserves management access and rollback paths before disruptive changes.

## Highlights

- Bootstrap and harden key-based SSH access without exposing credentials.
- Add Tailscale as an independent remote-management path.
- Inventory and compare OS, kernel, driver, CUDA, firmware, RDMA, container, and workload state across nodes.
- Operate multiple systems safely with per-host evidence and rolling changes.
- Discover live ConnectX-7 Ethernet and RoCE interface mappings instead of guessing device names.
- Configure a dedicated fabric without replacing the management default route.
- Establish true two-way traffic between nodes.
- Validate bound routing, ICMP, SSH, TCP payloads, `iperf3`, RDMA, and NCCL in both directions.
- Test every physical fabric rail independently before enabling multi-rail workloads.
- Monitor CPU, unified memory, swap activity, PSI, storage, thermals, containers, and fabric counters.
- Temporarily or persistently disable the desktop to reclaim unified-memory headroom.
- Distinguish ordinary page cache from retained or pinned CUDA/UVM memory.
- Restart services, containers, distributed workloads, and hosts using the smallest safe scope.
- Perform worker-first rolling reboots with boot-identity and post-boot verification.
- Apply DGX OS, driver, CUDA, and firmware updates through the supported DGX update path.
- Verify host-stack parity and real application behavior after updates.

## ConnectX-7 and multi-node support

A link reporting `up` is not enough to prove a usable cluster fabric. This skill requires validation at every relevant layer:

1. Physical link and negotiated speed.
2. Ethernet-to-RoCE device mapping.
3. Symmetric endpoint and MTU configuration.
4. Correct forward and reverse route selection.
5. Interface-bound traffic in both directions.
6. Node-to-node SSH initiated from both systems.
7. Bidirectional TCP and `iperf3` testing.
8. RDMA tests with each endpoint acting as server and client.
9. A real NCCL collective through the intended devices.
10. Continued separation between management and fabric traffic.

This avoids common false positives where unbound traffic silently uses the management network, only one direction works, or an API appears healthy while a worker rank or RDMA path has failed.

## Safety model

The skill groups work into read-only, reversible, and disruptive operations. Before persistent networking changes, GUI disablement, updates, reboot, shutdown, or similar disruption, the agent must establish:

- explicit authorization and scope;
- expected interruption;
- success criteria;
- a tested management or recovery path;
- backups and rollback commands;
- the required order of operations across nodes.

It never instructs the agent to expose passwords, private keys, Tailscale auth keys, tokens, or other credentials. It also prevents simultaneous multi-node reboots and discourages broad firewall, reverse-path, driver, or package changes made without evidence.

## DGX Spark-specific guidance

DGX Spark uses unified CPU/GPU memory, so conventional discrete-GPU monitoring can be misleading. The skill combines:

- `MemAvailable` and page-cache state;
- fresh swap-in and swap-out activity;
- Pressure Stall Information;
- process and cgroup accounting;
- CUDA/UVM ownership;
- workload-level cache or reservation metrics.

It also includes procedures for operating headless, diagnosing memory that remains unavailable after CUDA exits, avoiding unsupported generic NVIDIA driver installation methods, and maintaining parity across distributed systems.

## Requirements

- OpenClaw with permission to use SSH.
- The `ssh` client installed on the OpenClaw host.
- An existing trusted first-access or recovery path to each DGX Spark.
- An authorized administrator account on each target.
- `sudo` access appropriate to the requested operation.
- NVIDIA-supported cabling and topology for ConnectX-7 fabric work.
- Explicit user approval before disruptive actions.

Optional tools used when present include Tailscale, NVIDIA Sync, NetworkManager or netplan, `iperf3`, RDMA utilities, NCCL tests, Docker, and standard Linux monitoring utilities.

## Example requests

- “Set up key-based SSH access to these two DGX Spark systems and verify noninteractive administration.”
- “Add Tailscale as a backup management path without changing workload routing.”
- “Configure the direct ConnectX-7 link and prove traffic works in both directions.”
- “Check whether the distributed job is actually using the fabric instead of the management network.”
- “Compare the software and driver stack across both systems.”
- “Measure memory pressure and identify what can be stopped safely for more inference headroom.”
- “Switch both systems to headless operation with a tested rollback.”
- “Restart the distributed service and verify every rank plus a functional request.”
- “Perform a rolling reboot without losing remote access.”
- “Plan and apply DGX Spark updates one node at a time, then verify parity and performance.”

## What this skill does not do

- Bypass first-login, password, or physical-access requirements.
- Invent hostnames, addresses, credentials, interface mappings, or workload configuration.
- Turn the high-bandwidth fabric into a default management route.
- Treat a running process, open port, or health endpoint as complete verification.
- Perform simultaneous multi-node reboots.
- Apply generic NVIDIA runfile drivers over the DGX OS package stack.
- Attempt unsupported firmware or UEFI recovery without a console and recovery plan.

## Suggested ClawHub tags

`dgx-spark`, `nvidia`, `gb10`, `sysadmin`, `ssh`, `tailscale`, `connectx`, `roce`, `rdma`, `nccl`, `multi-node`, `gpu`, `linux`, `monitoring`, `infrastructure`

## Recommended category

**Infrastructure / System Administration**

## Source documentation

The skill directs agents to consult current official documentation at execution time:

- NVIDIA DGX Spark User Guide
- DGX Spark OS and Component Update Guide
- DGX Spark ConnectX-7 Networking Guide
- NVIDIA Connect Two Sparks playbook
- NVIDIA NCCL for DGX Spark playbook
- Tailscale Linux, MagicDNS, and Tailscale SSH documentation
