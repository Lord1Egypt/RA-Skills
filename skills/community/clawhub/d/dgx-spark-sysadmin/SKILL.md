---
name: dgx-spark-sysadmin
description: Administer DGX Spark hosts safely through remote access.
metadata:
  openclaw:
    requires:
      bins: [ssh]
---

# DGX Spark Remote Sysadmin

Administer NVIDIA DGX Spark / GB10 systems remotely. Keep management, ConnectX-7 fabric, and client service traffic distinct; discover live state before changes; preserve recovery access; verify every affected node and real workload path.

## When to Use

Use for SSH and Tailscale setup, multi-node administration, ConnectX-7 networking, monitoring, headless operation, workload/host restarts, reboot/shutdown, and coordinated DGX OS, driver, CUDA, firmware, or container-stack updates.

Do not improvise firmware/UEFI recovery without a console or operate systems outside the user's authorization.

## Operating Contract

Resolve rather than invent:

```text
<admin-user>  <ssh-key-path>
<node-a-management-name>  <node-b-management-name>
<node-a-fabric-address>   <node-b-fabric-address>
<node-a-fabric-interface> <node-b-fabric-interface>
<node-a-roce-device>      <node-b-roce-device>
<service-or-container>
```

For each additional rail, define another complete fabric tuple.

| Plane | Purpose |
|---|---|
| Management | LAN, Wi-Fi, or Tailscale for administration and recovery |
| Fabric | ConnectX-7 Ethernet/RoCE for node-to-node workloads |
| Service | Address clients use for the application/API |

The fabric must not become a default route or the only recovery path.

### Change rules

1. Read-only discovery may run in parallel. Preserve per-host stdout, stderr, duration, and exit code.
2. Obtain explicit maintenance authorization before persistent network changes, GUI disablement, updates, reboot, shutdown, or other disruption. State scope, interruption, success gates, and rollback.
3. Make one state change at a time during access/network recovery. Back up edited files and syntax-check before activation.
4. Never handle passwords, private keys, Tailscale auth keys, or tokens in prompts, command arguments, logs, or files. Transfer only public keys through trusted paths.
5. Never reboot both nodes together. Treat partial multi-host success as failure until reconciled.
6. Distinguish **started**, **ready**, and **functionally healthy**. A process, port, or health endpoint alone is not full verification.

## 1. Inventory and Parity

Collect the same timestamped manifest from every node and compare it programmatically:

```bash
hostnamectl; cat /etc/os-release; cat /etc/dgx-release 2>/dev/null || true
uname -a; uptime; who; systemctl is-system-running; systemctl get-default
ip -br link; ip -br address; ip route; ip rule
ibdev2netdev 2>/dev/null || true; rdma link show 2>/dev/null || true
nvidia-smi; cat /proc/driver/nvidia/version 2>/dev/null || true
free -h; cat /proc/pressure/memory; swapon --show
findmnt; lsblk; df -hT
systemctl --failed --no-pager; systemctl --type=service --state=running --no-pager
ss -lntup; docker ps --no-trunc 2>/dev/null || true
readlink -f /usr/local/cuda 2>/dev/null || true; nvcc --version 2>/dev/null || true
dpkg-query -W 'nvidia*' 'cuda*' 'linux-*nvidia*' 'libnccl*' 2>/dev/null || true
apt-mark showhold; dpkg --audit
fwupdmgr get-devices 2>/dev/null || true; tailscale status 2>/dev/null || true
```

List differences in OS, kernel, loaded/installed driver, firmware, CUDA, NCCL/RDMA, container runtime, fabric, package health, and workload artifacts. Matching containers do not compensate for divergent hosts.

## 2. Bootstrap SSH

Initial access needs a trusted path: local console, NVIDIA Sync, existing SSH, or enterprise provisioning. An agent cannot bypass first-login or password prompts.

Create a dedicated key only when an approved one does not exist:

```bash
ssh-keygen -t ed25519 -a 100 -f <ssh-key-path> -C dgx-spark-admin
```

Install only its public key through the trusted path. On each node:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

Verify noninteractive access and intended sudo policy:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 -i <ssh-key-path> \
  <admin-user>@<node-management-name> 'id; hostname; sudo -n true'
```

Before SSH configuration changes, keep an independent session and recovery path open. Inspect `sudo sshd -T`, back up the active configuration, run `sudo sshd -t`, then `sudo systemctl reload ssh`. Disable older authentication only after the replacement succeeds independently. Treat changed host keys as a security/reimage event; verify fingerprints out of band rather than deleting records blindly.

## 3. Tailscale Management

Use Tailscale as an alternate management plane, not the distributed data plane.

1. Follow current official Linux instructions for the installed DGX OS release; prefer reviewed repository/package steps over piping an unreviewed script into a privileged shell.
2. Enable `tailscaled` and authenticate interactively or through an approved secret channel. Never expose auth keys.
3. Prefer standard OpenSSH over Tailscale/MagicDNS. Enable Tailscale SSH only after separate tailnet-policy review.
4. Verify:

```bash
systemctl is-active tailscaled
tailscale status
tailscale ip
tailscale ping --until-direct <peer-management-name>
```

Record direct versus relayed connectivity. Do not advertise the fabric as a subnet route unless the topology and ACLs require it. Confirm MagicDNS does not break local cluster resolution. Prove both primary management and Tailscale access before risky work.

## 4. Connect Two Systems over ConnectX-7

Prefer NVIDIA Sync Cluster Assistant or NVIDIA's current topology-specific playbook. Use manual setup only when needed and remain connected through the management plane.

### 4.1 Discover mappings

Never guess interface names: one physical QSFP port can expose multiple Ethernet/RoCE devices.

```bash
ibdev2netdev
ip -br link
rdma link show
lspci -nn | grep -i -E 'ethernet|network|mellanox|nvidia'
ethtool <fabric-interface>
```

For every rail, record physical port/cable, Ethernet interface, RoCE device, PCIe identity, link speed/state, MTU, addresses, and routes. Use recommended cables and the supplied power adapter.

### 4.2 Configure both endpoints

Back up the authoritative NetworkManager/netplan configuration. Each endpoint needs:

```text
interface = discovered ConnectX Ethernet interface
address/prefix = approved unique fabric endpoint
method = manual
never-default = true
autoconnect = true
MTU = identical at both ends
DNS = none unless explicitly required
```

Do not mix persistent NetworkManager/netplan ownership with undocumented ad-hoc `ip` configuration. Syntax-check netplan before applying. Apply one endpoint at a time through management access and retain rollback commands. Give separate rails unambiguous layer-3 prefixes unless the supported playbook specifies another topology.

### 4.3 Prove two-way layer-3 traffic

On A:

```bash
ip route get <node-b-fabric-address>
ping -I <node-a-fabric-interface> -c 3 <node-b-fabric-address>
```

On B:

```bash
ip route get <node-a-fabric-address>
ping -I <node-b-fabric-interface> -c 3 <node-a-fabric-address>
```

Each route must select the intended interface and local fabric source. An unbound ping can silently use management networking.

For asymmetry, compare both nodes rather than weakening security globally:

```bash
ip address show dev <fabric-interface>; ip route; ip rule
ip neigh show dev <fabric-interface>
sysctl net.ipv4.conf.all.rp_filter
sysctl net.ipv4.conf.<fabric-interface>.rp_filter
sudo nft list ruleset 2>/dev/null || true
sudo ufw status verbose 2>/dev/null || true
ip -s link show dev <fabric-interface>
ethtool -S <fabric-interface>
```

Correct the exact route, reverse-path, or firewall cause.

### 4.4 Prove two-way SSH and application traffic

Controller-to-node SSH does not prove node-to-node launch capability. Use NVIDIA Sync's cluster-key workflow or create dedicated cluster keys on both nodes and exchange only public keys.

```bash
# From A
ssh -o BatchMode=yes -o ConnectTimeout=10 \
  <admin-user>@<node-b-fabric-address> 'hostname'
# From B
ssh -o BatchMode=yes -o ConnectTimeout=10 \
  <admin-user>@<node-a-fabric-address> 'hostname'
```

Also bind an approved temporary TCP listener to each fabric endpoint in turn and verify a real payload from the peer. Remove test listeners and temporary firewall rules afterward.

### 4.5 Benchmark both directions and every rail

Run `iperf3` bound to fabric addresses. Measure A-to-B and B-to-A separately (`--reverse` may test the return direction). Record sender/receiver throughput, retransmits, CPU, MTU, and link errors/drops before and after. Repeat with explicit source binding for every rail. Advertised link speed is not measured throughput.

Verify RoCE/GID state, then run supported RDMA bandwidth tests with each endpoint in server and client roles:

```bash
rdma link show
ibdev2netdev
show_gids 2>/dev/null || true
```

Finally run an NCCL collective using the real CUDA/container stack. Pin only devices already validated:

```text
NCCL_SOCKET_IFNAME=<fabric-interface>
NCCL_IB_HCA=<roce-device>
NCCL_IB_DISABLE=0
```

Validate every rail independently before multi-rail use. NCCL `INFO` plugin probes are not failures without a failed collective, fallback, timeout, or error evidence.

Fabric acceptance requires **both directions** for bound ICMP, SSH, TCP payload, `iperf3`, RDMA, and NCCL, while management traffic still selects the management plane.

## 5. Multi-Node Operations

Read-only fan-out may be parallel. Aggregate in code and fail if any host is missing or nonzero.

For state changes:

1. Quiesce/drain the distributed workload.
2. Change the worker/non-coordinator first.
3. Verify its boot, driver, memory, management, fabric, and workload readiness.
4. Change the coordinator/head.
5. Verify every rank and an end-to-end functional request.

Use the deployment's supported launcher/supervisor and rank order. Before relaunch, prove no stale ranks/containers/CUDA processes remain, ports are free, memory recovered, and both nodes match on image digest, artifact identity, launch parameters, driver, and fabric selection. Inspect every rank's logs; a ready API can conceal a failed worker or transport fallback.

## 6. Performance Monitoring

DGX Spark uses unified CPU/GPU DRAM; `nvidia-smi` may report framebuffer memory as unsupported. Corroborate rather than relying on one counter.

```bash
# Unified memory and pressure
free -h
grep -E 'MemAvailable|SwapFree|SwapTotal|HugePages' /proc/meminfo
cat /proc/pressure/memory
vmstat 1 5
swapon --show
nvidia-smi
nvidia-smi pmon -c 1 2>/dev/null || true

# CPU, storage, thermals, cgroups
uptime
mpstat 1 5 2>/dev/null || true
iostat -xz 1 5 2>/dev/null || true
pidstat 1 5 2>/dev/null || true
systemd-cgtop -b -n 1
sensors 2>/dev/null || true
nvidia-smi dmon -d 1 -c 5 2>/dev/null || true

# Fabric and services
ip -s link show dev <fabric-interface>
ethtool <fabric-interface>
ethtool -S <fabric-interface>
rdma link show; ss -s
docker stats --no-stream 2>/dev/null || true
systemctl --failed --no-pager
journalctl -p warning..alert --since '<approved-window>' --no-pager
```

Report the measurement window and workload state. Distinguish free memory, `MemAvailable`, page cache, swap allocated versus fresh `si`/`so`, reserved cache capacity versus active use, and process/cgroup memory versus CUDA/UVM allocation. Stable swap occupancy with no I/O is not active thrashing; PSI shows recent contention. Compare network counters at both ends before and after a bounded workload.

## 7. Reclaim Headroom and Run Headless

Inventory first:

```bash
systemctl --type=service --state=running --no-pager
systemctl status display-manager --no-pager
docker ps --no-trunc
ps -eo pid,ppid,%cpu,%mem,rss,comm,args --sort=-rss
```

Identify desktop sessions, browsers, remote desktop, notebooks, indexers, containers, compilers, and model servers by exact identity. Do not blindly stop SSH, NetworkManager, Tailscale, time sync, required container runtime, or NVIDIA platform services.

Before stopping the GUI, verify two management paths, no active desktop user, current default target, display-manager identity, memory/PSI baseline, and restore command. With authorization:

```bash
sudo systemctl stop display-manager      # temporary
sudo systemctl start display-manager     # restore
sudo systemctl set-default multi-user.target  # persistent after validated test
sudo systemctl set-default graphical.target   # restore desktop boot
```

Measure actual `MemAvailable`/PSI improvement. Persistent target changes require a maintenance reboot to prove remote access, CUDA, networking, and workloads.

After a large CUDA workload stops, prove all ranks/containers/CUDA processes are gone on every node, then recheck memory, swap activity, and PSI. Page-cache reclamation requires authorization and `sync`; it does not fix pinned/unowned UVM memory. If memory stays unavailable without an owner, preserve driver/kernel logs and perform a rolling reboot rather than repeatedly launching into allocation failure.

## 8. Restart, Reboot, and Shutdown

Prefer the smallest scope: application reload → service/container → distributed workload → host.

For a service:

```bash
sudo systemctl restart <service>
systemctl is-active <service>
journalctl -u <service> --since '<restart-time>' --no-pager
```

Use the deployment's compose/launcher contract for containers; verify image digest, mounts, environment, devices, network, and restart policy before replacement.

### Rolling reboot

Preflight each node:

```bash
who; systemd-inhibit --list; systemctl --failed --no-pager
docker ps --no-trunc
cat /proc/sys/kernel/random/boot_id
sync
```

Drain workloads and reboot the worker/non-coordinator:

```bash
sudo systemctl reboot
```

Require the management endpoint to disappear and return with a changed boot ID. Then verify:

```bash
uptime; systemctl is-system-running; systemctl --failed --no-pager
nvidia-smi; free -h
ip -br address; ip route
ibdev2netdev; rdma link show
tailscale status 2>/dev/null || true
docker ps --no-trunc 2>/dev/null || true
```

Reprove fabric traffic in both directions. Only then reboot the coordinator/head. Restart the workload in required rank order and run a functional request. Ping alone is not readiness.

Before `sudo systemctl poweroff`, state and verify the recovery mechanism (physical access, tested wake-on-LAN, smart power, or out-of-band management).

## 9. DGX OS, Driver, CUDA, and Firmware Updates

Treat DGX Spark as a coordinated appliance stack. Read current release notes and the official update guide. Prefer DGX Dashboard. Require stable power, backup, recovery access, stopped workloads, a maintenance window, and before-manifests from every node.

Preflight:

```bash
dpkg --audit
apt-mark showhold
sudo apt-get -s dist-upgrade
fwupdmgr get-updates
```

Stop if simulation removes platform packages, changes driver/kernel families unexpectedly, or exposes broken package state. Never layer a generic NVIDIA `.run` driver over DGX OS packages or casually mix package sources/driver branches.

When manual updates are required, NVIDIA's documented sequence is:

```bash
sudo apt update
sudo apt dist-upgrade
sudo fwupdmgr refresh
sudo fwupdmgr upgrade
sudo reboot
```

Inspect each step; do not hide errors in a command chain. Update and fully validate one node before its peer.

Post-update, compare peer/before manifests and verify package health, DGX release, kernel, loaded driver, CUDA realpath/compiler, firmware, container runtime, SSH/Tailscale, ConnectX mapping and two-way traffic, RoCE/RDMA/NCCL, CUDA initialization in the intended runtime, and real application performance.

## Gotchas

| Symptom | Required distinction/action |
|---|---|
| GPU memory unsupported in `nvidia-smi` | Use OS unified-memory, PSI, swap, process/cgroup, and workload counters together |
| Memory remains used after CUDA exit | Separate page cache from pinned/unowned UVM; prove no owner; collect logs; rolling reboot if unrecovered |
| `nvidia-smi` works but build/runtime fails | Compare loaded driver, installed packages, kernel modules, CUDA toolkit, container runtime, and noninteractive PATH |
| Fabric works one way | Bind source/interface in both directions; inspect routes, neighbors, reverse-path filtering, firewall, and counters |
| Jumbo MTU configured | Prove do-not-fragment payloads both ways and benchmark before/after; preserve rollback |
| API/head appears healthy | Inspect every rank and run a functional workload |
| NCCL logs plugin probes | Distinguish informational probes from collective failure, fallback, timeout, or error |
| SSH disconnects during reboot | Require endpoint down/up plus changed boot ID |
| Host key changes | Verify fingerprint out of band; never delete blindly |
| Update succeeds on one node | Restore host-stack parity and functional fabric/application tests before closure |

## Verification and Report

Applicable gates:

- primary and alternate management paths;
- noninteractive SSH and intended sudo behavior;
- complete before/after manifests with no unexplained divergence;
- discovered ConnectX Ethernet/RoCE mapping;
- bound routes, ICMP, SSH, TCP payload, `iperf3`, RDMA, and NCCL in both directions and every intended rail;
- management/fabric route separation;
- unified memory, swap activity, PSI, storage, thermals/power when available, and fabric counters;
- measured headless/service effect plus restore commands;
- changed boot ID and post-boot platform checks;
- every distributed rank plus a functional application request;
- removal of temporary listeners, firewall rules, files, and test processes;
- usable rollback.

Return:

```text
Scope and authorization:
Systems reached:
Management paths:
Changes and rollback:
Per-node effective state/parity:
ConnectX forward/reverse route evidence:
Ethernet/RDMA/NCCL bidirectional results:
Unified-memory/PSI results:
Service state: started | ready | functionally healthy
Errors, warnings, and unverified gates:
Recommended next action:
```

Never report secrets or claim totals, speeds, capacity, or health without current real output.

## Authoritative References

Check at execution time:

- https://docs.nvidia.com/dgx/dgx-spark/
- https://docs.nvidia.com/dgx/dgx-spark/os-and-component-update.html
- https://docs.nvidia.com/dgx/dgx-spark/spark-clustering.html
- https://build.nvidia.com/spark/connect-two-sparks
- https://build.nvidia.com/spark/nccl
- https://tailscale.com/docs/install/linux
- https://tailscale.com/docs/features/magicdns
- https://tailscale.com/docs/features/tailscale-ssh
