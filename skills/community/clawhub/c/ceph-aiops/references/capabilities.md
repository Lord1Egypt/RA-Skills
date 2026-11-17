# ceph-aiops capabilities

> 37 MCP tools (17 read, 18 write, 2 undo) over the **ceph-mgr
> Dashboard REST API** (`https://<host>:8443`, JWT via `POST /api/auth`).
> Multi-node rebalance behaviour and the write ops need live verification
> (see `docs/VERIFICATION.md`).

## Read tools (17)

| Tool | API path | Returns |
|------|----------|---------|
| `cluster_health` | `GET /api/health/full` | **flagship RCA** — per active HEALTH_WARN/ERR check: code, plain-language meaning, likely cause, suggested action |
| `cluster_status` | `GET /api/health/minimal` | `ceph -s` summary: health status, mon/mgr/osd/pg counts |
| `osd_tree` | `GET /api/osd` | OSD tree: up/in, CRUSH weight, host, device class |
| `osd_df` | `GET /api/osd` | per-OSD utilization %, **most-full first**, near-full / backfill-full flags |
| `osd_perf` | `GET /api/osd` | commit/apply latency per OSD, **slowest first** |
| `pg_summary` | `GET /api/pg` (+ `/api/health/full`) | PG **state histogram** + list of non-active+clean PGs |
| `pg_dump_stuck` | `GET /api/pg` | stuck PGs (inactive/unclean/stale/undersized) + implicated OSDs |
| `scrub_status` | `GET /api/health/full` | PGs overdue for scrub / deep-scrub |
| `pool_ls` | `GET /api/pool` | pools: name, id, size, pg_num, autoscale mode, application |
| `pool_df` | `GET /api/pool` | per-pool usage; **usable capacity = raw ÷ size** |
| `rbd_ls` | `GET /api/block/image` | RBD images (optionally filtered by pool): name, size, pool |
| `cephfs_status` | `GET /api/cephfs` | MDS ranks + **"behind on trimming"** + client count |
| `rgw_status` | `GET /api/rgw/daemon` + `GET /api/rgw/bucket` | RGW daemons + buckets + **LARGE_OMAP / unsharded-index** findings |
| `mon_status` | `GET /api/monitor` | monitors: in-quorum vs **out-of-quorum** |
| `mgr_status` | `GET /api/health/full` | active mgr, standbys, enabled modules |
| `slow_ops` | `GET /api/health/full` | blocked / slow requests grouped **by OSD** |
| `capacity_forecast` | `GET /api/osd` (+ df) | raw/used/avail + **days-to-nearfull** projection |

## Write tools (18)

| Tool | Risk | API path | Undo / safety |
|------|------|----------|---------------|
| `cluster_flag_set` | medium | `GET`+`PUT /api/osd/flags` | set/unset noout/noscrub/nobackfill/norecover; captures prior flag set (undo) |
| `osd_reweight` | medium | `POST /api/osd/{id}/reweight` | 0.0 = drain; captures prior weight (undo) |
| `osd_mark_in` | medium | `POST /api/osd/{id}/mark` | captures prior up/in state (undo) |
| `osd_mark_out` | **high** | `POST /api/osd/{id}/mark` | drains data; CLI double-confirm + dry-run; captures prior state |
| `osd_purge` | **high** | `DELETE /api/osd/{id}` | destroy + crush rm + auth del; **irreversible**; dry-run + double-confirm |
| `trigger_scrub` | medium | `POST /api/pg/{pgid}/scrub` | schedule a shallow scrub; no prior state |
| `trigger_deep_scrub` | medium | `POST /api/pg/{pgid}/deep_scrub` | schedule a deep (data-integrity) scrub |
| `set_pool_quota` | medium | `PUT /api/pool/{name}` | captures prior max_bytes/max_objects (undo) |
| `set_pool_pg_num` | medium | `PUT /api/pool/{name}` | captures prior pg_num (undo) |
| `set_pool_autoscale` | medium | `PUT /api/pool/{name}` | captures prior autoscale mode (undo) |
| `pool_create` | medium | `POST /api/pool` | create a new pool |
| `set_pool_size` | **high** | `PUT /api/pool/{name}` | replica change **forces data movement**; dry-run + double-confirm; captures prior size |
| `pool_delete` | **high** | `DELETE /api/pool/{name}` | **destroys all data**; dry-run + double-confirm |
| `rbd_image_create` | medium | `POST /api/block/image` | create an RBD image |
| `rbd_snapshot_create` | medium | `POST /api/block/image/{spec}/snap` | reversible → delete the snapshot |
| `rbd_image_delete` | **high** | `DELETE /api/block/image/{spec}` | **irreversible**; dry-run + double-confirm |
| `rbd_snapshot_delete` | **high** | `DELETE /api/block/image/{spec}/snap/{snap}` | **irreversible**; dry-run + double-confirm |
| `throttle_recovery` | medium | `GET`+`POST /api/cluster_conf` | tunes `osd_max_backfills` / `osd_recovery_max_active`; captures prior values (undo) |

## Out of scope (by design)

- RGW **multisite** replication and zone/zonegroup management
- **NFS-Ganesha** exports
- **cephadm orchestrator** host/daemon management (add/remove hosts, deploy daemons)
- Per-daemon config sprawl beyond the recovery-tuning keys above

The ceph-mgr Dashboard API has no ETag / pagination, so this tool exposes none.

Want one of these? Open an issue or PR — feedback and contributions welcome.
