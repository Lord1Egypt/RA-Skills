---
name: disk-doctor
description: Diagnose and safely reclaim disk space on an OpenClaw host
---

# Disk Doctor

Use this when the user asks why their OpenClaw box is filling up, reports a full
disk, sees the gateway misbehaving after weeks of uptime, or asks what is safe to
delete.

A long-running OpenClaw host fills up quietly. The agent's own tooling caches
aggressively, and none of it is cleaned automatically. On a 15 GB VPS the base
install plus caches can reach 80% without the user creating a single large file
of their own.

## Step 1: measure before you touch anything

Never delete based on a guess. Run these first and show the user the output:

```bash
df -h /
du -x -h -d1 / 2>/dev/null | sort -hr | head -15
du -x -h -d1 /root 2>/dev/null | sort -hr | head -15
find / -xdev -type f -size +50M -printf '%s\t%p\n' 2>/dev/null \
  | sort -rn | head -20 | awk -F'\t' '{printf "%.0f MB\t%s\n", $1/1048576, $2}'
```

`du` and `df` will disagree by a few percent. That is normal: `df` excludes the
filesystem's reserved blocks, `du` does not. Neither is wrong. Report the `df`
number, because that is the one that runs out.

## Step 2: check nothing is running

Cleaning a cache while a package install is in flight can fail that install.

```bash
uptime
ps -eo pcpu,pmem,etime,args --sort=-pcpu | head -12
```

If load is high or you see `npm`, `apt`, `pip` or a build running, wait.

## Step 3: reclaim, safest first

These three are safe on any host. The first two are pure caches that regenerate
on demand. The third trims archived logs and keeps the recent ones. Nothing the
user created is touched.

```bash
npm cache clean --force        # commonly the single biggest win
apt-get clean                  # package archives, already installed
journalctl --vacuum-size=64M   # keeps recent logs, drops the archive
```

Measured on two independent production OpenClaw hosts: a cleanup pass took one
from 78% to 67% used, reclaiming 1.6 GB, with the npm cache alone accounting for
1.4 GB.

## Step 4: the big offenders, with judgement

Report these to the user and let them decide. Do not delete them unprompted.

**Docker.** Docker cleanup belongs here, with the user's explicit approval. A
stopped container keeps its own writable layer, and whatever was written there
exists nowhere else unless it lives in a named volume or a bind mount. Removing
the container removes that data for good. Show the state first:

```bash
docker system df
docker ps -a
docker image ls
docker network ls
```

Name the exact containers, images and networks you propose to remove, explain
which ones hold data outside a volume, and wait for a clear yes. When the goal is
only to reclaim build cache, use the narrow command and let Docker ask for its
own confirmation:

```bash
docker builder prune
```

**Browser engines.** `~/.cache/ms-playwright` holds a full Chromium per version,
and versions accumulate: each new one lands next to the old. Measured on a live
host: 389 MB and 364 MB for two Chromium builds, plus 262 MB and 254 MB for their
headless shells, about 1.27 GB in total. Dropping one superseded version pair
frees roughly 620 MB. Old versions are only safe to remove if no installed
package pins them. Check before advising:

```bash
du -sh ~/.cache/ms-playwright/* 2>/dev/null | sort -hr
```

**Multi-platform binaries.** Some npm packages vendor prebuilt binaries for every
platform they support. On one measured host, a single dependency carried Windows,
macOS Intel, macOS ARM, Linux ARM and Linux x64 builds: about 1.65 GB total on a
machine that can only ever execute one of them. Removing the foreign-platform
directories is usually safe but will be undone by the next `npm install`, and can
break package integrity checks. Prefer reinstalling the package with
`--omit=optional` where the package supports it.

**Electron downloads.** `~/.cache/electron` keeps the downloaded installer zip
after extraction, 110 MB on the measured host. That copy is dead weight.

## What to leave alone

- The workspace, and anything under it. That is the user's work.
- `~/.openclaw` config, credentials and session state.
- Docker volumes, and any stopped container the user has not cleared for removal.
- Anything you cannot explain to the user in one sentence.

## Prevention

Suggest a monthly cache pass. It costs far less than a rescue at 95%. If the host
is persistently above 80% after cleaning caches, the disk is genuinely too small
for the workload, and cleaning is treating a symptom.
