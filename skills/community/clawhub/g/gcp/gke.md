# GKE — Autopilot, Standard, and Staying Upgraded

This file is the GCP-platform side of Kubernetes: cluster shape, node pools, networking, identity, upgrades and cost. Manifest authoring, pod debugging and RBAC are `k8s`.

**Contents:** [Autopilot or Standard](#autopilot-or-standard) · [Cluster Shape Decisions You Cannot Undo](#cluster-shape-decisions-you-cannot-undo) · [Workload Identity](#workload-identity) · [Node Pools](#node-pools) · [Upgrades Are Not Optional](#upgrades-are-not-optional) · [Autoscaling, Three Layers](#autoscaling-three-layers) · [Networking Inside the Cluster](#networking-inside-the-cluster) · [Cost](#cost) · [Production Checklist](#production-checklist)

**Before sizing or creating a cluster**, read `## Current Infrastructure` in `~/Clawic/data/gcp/memory.md` and the shared `~/Clawic/data/servers/servers.md` — an existing cluster's secondary ranges constrain what the next one can have.

## Autopilot or Standard

| | Autopilot | Standard |
|---|---|---|
| Billing | Per pod resource request | Per node, whether pods use it or not |
| Nodes | Managed and invisible; no SSH, no node pools to size | Yours, with all the sizing and upgrade work |
| Bin-packing | Google's problem | Yours, and it is where the savings are |
| Privileged pods, host network, host ports | Blocked (with a narrow allowlist for partner agents) | Allowed |
| DaemonSets | Supported, with constraints | Unconstrained |
| Custom kernel parameters, node-level tuning | No | Yes |
| GPUs | Supported, with fewer knobs | Full control over placement and sharing |

Choose Autopilot by default. Choose Standard when you need privileged workloads, node-level tuning, fine-grained GPU packing, or when a well-tuned bin-packed fleet at high steady utilization genuinely beats per-pod pricing — which requires measuring, not assuming.

**Autopilot rejects pod specs, which reads as a scheduling bug.** It rounds requests to allowed increments and enforces a CPU:memory ratio range per compute class. A pod asking for a shape outside that range stays `Unschedulable` with a message about the ratio, not about capacity. Set requests explicitly and inside the allowed band; missing requests get defaulted to something larger than intended, which is also how an Autopilot bill surprises people.

## Cluster Shape Decisions You Cannot Undo

Each of these is fixed at creation. Getting one wrong means building a new cluster and migrating.

- **Regional vs zonal control plane.** Regional replicates the control plane across zones and is the only option that survives a zonal outage without losing the API server. Zonal is cheaper only in the sense that a single zonal cluster may be covered by the free-tier cluster credit — the control plane is the thing you least want single-zoned in production.
- **Secondary ranges for pods and services.** Sized at creation, and they cap the maximum pods the cluster can ever run. The pod range is consumed per node by the maximum-pods-per-node setting, not by actual pod count — a cluster of 10 nodes at 110 max pods reserves address space for 1,100 pods on day one. Size against the three-year node count (`networking.md`).
- **VPC-native (alias IP) vs routes-based.** VPC-native is the only sensible choice and is required for most modern features.
- **Private cluster.** Nodes with no external IPs. Choose it at creation; the control plane's authorized networks and the private endpoint configuration are far easier to get right up front. A private cluster needs Private Google Access or a PSC endpoint to pull images, or every deploy fails with `ImagePullBackOff` (`networking.md`).
- **Dataplane V2 (eBPF)** for network policy and better observability. Switching later is a cluster rebuild.
- **Workload Identity.** Enable at creation. Retrofitting means re-plumbing every workload's authentication.

## Workload Identity

The mechanism that lets a pod authenticate as a GCP service account without a key and without borrowing the node's identity.

- A Kubernetes service account is bound to a GCP identity; pods using that KSA get short-lived credentials from the metadata server.
- **The point is the node service account.** Without Workload Identity, every pod on a node can reach the node's service account through the metadata endpoint, which means every pod has every permission the node has. With it enabled, strip the node service account down to logging, monitoring and Artifact Registry read — nothing else.
- Blocking pod access to the legacy metadata endpoint is part of the same change; leaving it reachable leaves the escalation path open.
- Bindings are per namespace plus KSA name, so two namespaces with the same KSA name are different principals. Namespace naming becomes a security decision.
- The common failure is a pod authenticating as the wrong identity and getting a confusing 403. Print the identity from inside the pod before touching IAM (`iam.md`).

## Node Pools

Standard clusters only. Each pool is a machine type, a disk, a set of labels and taints, and an autoscaling range.

- **One pool per workload shape**, not one pool for everything: a pool of large machines running small pods wastes the difference, and a single pool cannot serve both a memory-heavy and a CPU-heavy workload well.
- **Spot pools with an on-demand baseline** is the standard cost pattern: a small guaranteed pool plus a Spot pool that absorbs the variable load, with pod disruption budgets and 30-second-safe shutdown handling. Spot in GKE gives the same 30-second notice as any Spot VM (`services.md`).
- **Taints and tolerations keep the wrong workload off the wrong pool.** Without them, the scheduler will put your database pod on the Spot pool the first time the baseline is full.
- **Surge upgrade settings** decide how disruptive an upgrade is: max-surge adds temporary nodes, max-unavailable removes capacity. `max-surge 1, max-unavailable 0` is the safe default and costs one extra node for the duration.
- **Node auto-provisioning** creates pools automatically for pods that fit nowhere. Powerful and easy to surprise yourself with; bound it with resource limits.
- Register each pool as one row in the shared `~/Clawic/data/servers/servers.md`, named after the pool — never one row per ephemeral node (`memory-template.md`).

## Upgrades Are Not Optional

Kubernetes minor versions leave support on a schedule, and GKE will upgrade an unattended cluster rather than run an unsupported one.

- **Release channels**: Rapid (newest, shortest soak), Regular (the default and the right answer for most), Stable (slowest), Extended (longer support for a version, at a premium, for teams who cannot move). Being in a channel means auto-upgrade is on — that is the point, not a side effect.
- **Maintenance windows and exclusions** are the control you actually have. Set a window; add exclusions around a launch or a freeze, remembering that an exclusion cannot postpone an upgrade past the version's end of support.
- **Node upgrades are the disruptive half.** Surge settings, pod disruption budgets and a `terminationGracePeriodSeconds` that matches the app's real drain time are what make them uneventful. A PDB that allows zero disruption blocks the upgrade instead of protecting the app.
- **Deprecated APIs break on upgrade, not before.** GKE surfaces deprecation insights per cluster; read them before the version lands, not after the manifests fail to apply.
- Record every upgrade in `~/Clawic/data/gcp/deploys/<year>.md` under `## Cluster Upgrades`: date, cluster, from → to, channel, surge settings, and any incident. Put the next version-support check in `## Due` (`memory-template.md`).

## Autoscaling, Three Layers

They interact, and tuning one without the others produces the classic "it scaled but nothing got better".

1. **Horizontal Pod Autoscaler** — pod count from CPU, memory or a custom/external metric. For request-driven services, a per-pod requests metric beats CPU because CPU lags the queue.
2. **Cluster Autoscaler / Autopilot** — node count from pending pods. It only reacts to pods that cannot schedule, so a workload without resource requests never triggers it. Scale-down is deliberately conservative and is blocked by pods with no controller, local storage, or a restrictive PDB.
3. **Vertical Pod Autoscaler** — recommends or applies right-sized requests. Run it in recommendation mode first; in auto mode it restarts pods to apply changes, and combining it with HPA on the same resource metric makes the two fight.

The ordering that works: set correct requests (VPA recommendations), scale pods on a demand metric (HPA), let nodes follow (cluster autoscaler). Also check the downstream: an HPA that triples the pod count triples the database connections (`databases.md`).

## Networking Inside the Cluster

- **Services and Ingress** map to GCP load balancers. `Ingress` produces a classic external Application LB; the **Gateway API** is the current path and exposes far more of the load balancer's capabilities. Prefer Gateway for new work.
- **Container-native load balancing (NEGs)** sends traffic straight to pod IPs instead of hopping through a node. It removes a hop, makes health checks accurate per pod, and is the default with VPC-native clusters — verify it is on, because the node-port path masks unhealthy pods.
- **Network policy** requires Dataplane V2 or Calico enabled on the cluster. Default-deny per namespace plus explicit allows is the posture; without any policy, every pod can reach every other pod across namespaces.
- Health check firewall ranges apply here exactly as elsewhere: `35.191.0.0/16` and `130.211.0.0/22` must reach the backends (`networking.md`).
- Internal traffic between pods in the same cluster stays inside the VPC, but cross-zone pod-to-pod traffic is still cross-zone traffic and is billed (`costs.md`).

## Cost

- **Cluster management fee** per cluster per hour, with a credit that covers roughly one zonal cluster per billing account. Ten small clusters pay it ten times — a real argument for namespaces over clusters, up to the point where the blast radius argues back.
- **Autopilot bills pod requests**, so an over-requested pod is a permanently over-paid pod. This makes VPA recommendations a direct cost tool.
- **Standard bills nodes**, so the saving is bin-packing: right-sized requests, pools matched to workload shapes, and Spot for anything interruptible.
- Idle node pools with a minimum size above zero bill continuously. Set minimums to zero for pools that serve bursty work.
- Logging and monitoring from a busy cluster is a genuine line item. GKE's system logs are useful; application debug logs at full volume are the part to exclude (`costs.md`).

## Production Checklist

- Regional control plane; nodes across at least three zones
- Private cluster with authorized networks on the control plane endpoint; Private Google Access or PSC for image pulls
- Workload Identity enabled, node service account stripped to logging/monitoring/registry-read, legacy metadata endpoint blocked from pods
- Secondary ranges sized against the three-year node count and recorded in `## Current Infrastructure`
- Release channel chosen, maintenance window set, deprecation insights read before each upgrade
- Requests set on every workload (VPA in recommendation mode), PDBs that permit upgrades, `terminationGracePeriodSeconds` matched to real drain time
- Network policy default-deny per namespace
- Node auto-provisioning bounded, or off
- Backups for anything stateful — a PVC is not a backup, and Backup for GKE exists for exactly this
- Cluster registered in the shared `servers.md`; upgrades logged in `deploys/<year>.md`; next version-support check in `## Due`

Write every cluster and node pool into the shared `~/Clawic/data/servers/servers.md` (one row per cluster or pool, never per ephemeral node), every upgrade into `~/Clawic/data/gcp/deploys/<year>.md` under `## Cluster Upgrades`, and the secondary-range plan into `## Current Infrastructure` in `~/Clawic/data/gcp/memory.md`. Put the next version-support check in `## Due`. A cluster's range sizing is the one fact that cannot be recovered from the running cluster once you need to plan the next one (`memory-template.md`).
