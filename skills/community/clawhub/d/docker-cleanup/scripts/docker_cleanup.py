#!/usr/bin/env python3
"""Docker Cleanup Toolkit — prune, analyze, and manage Docker resources.

Usage:
  python3 docker_cleanup.py
  python3 docker_cleanup.py --all
  python3 docker_cleanup.py --images --force
  python3 docker_cleanup.py --json
  python3 docker_cleanup.py --report
  python3 docker_cleanup.py --analyze
"""

import argparse
import json
import os
import subprocess
import sys
import shutil
from datetime import datetime, timezone


def run_docker(cmd, capture=True, timeout=60):
    """Run docker command, return (success, stdout, stderr)."""
    try:
        r = subprocess.run(
            ["docker"] + cmd,
            capture_output=capture,
            text=True,
            timeout=timeout,
        )
        return r.returncode == 0, r.stdout.strip(), r.stderr.strip()
    except FileNotFoundError:
        print("❌ Docker not found. Is Docker installed and in PATH?")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def check_docker():
    """Verify Docker is accessible."""
    ok, out, err = run_docker(["info", "--format", "{{.ServerVersion}}"])
    if not ok:
        print(f"❌ Docker daemon not running: {err}")
        sys.exit(1)
    return out


def get_size_human(bytes_val):
    """Convert bytes to human-readable string."""
    if bytes_val is None:
        return "0B"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(bytes_val) < 1024:
            return f"{bytes_val:.1f}{unit}" if unit != "B" else f"{bytes_val:.0f}{unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f}PB"


def format_timestamp(ts_str):
    """Parse and reformat docker timestamp."""
    try:
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = now - ts
        days = delta.days
        if days < 1:
            return "today"
        elif days < 7:
            return f"{days}d ago"
        elif days < 30:
            return f"{days // 7}w ago"
        elif days < 365:
            return f"{days // 30}m ago"
        else:
            return f"{days // 365}y ago"
    except (ValueError, AttributeError):
        return ts_str


def get_containers(status_filter="all"):
    """List containers with details."""
    ok, out, _ = run_docker([
        "ps", "-a",
        "--format", "{{.ID}}|{{.Image}}|{{.Status}}|{{.Names}}|{{.CreatedAt}}|{{.Ports}}|{{.Size}}",
        "--filter", f"status={status_filter}" if status_filter != "all" else "",
    ])
    if not ok or not out:
        return []

    containers = []
    for line in out.split("\n"):
        parts = line.split("|")
        if len(parts) >= 5:
            cid, image, status, name, created = parts[:5]
            ports = parts[5] if len(parts) > 5 else ""
            size = parts[6] if len(parts) > 6 else ""
            containers.append({
                "id": cid,
                "image": image,
                "status": status,
                "name": name,
                "created": created,
                "created_fmt": format_timestamp(created),
                "ports": ports,
                "size": size,
            })
    return containers


def get_images():
    """List images with details."""
    ok, out, _ = run_docker([
        "images", "--format",
        "{{.ID}}|{{.Repository}}|{{.Tag}}|{{.Size}}|{{.CreatedAt}}|{{.VirtualSize}}",
    ])
    if not ok or not out:
        return []

    images = []
    for line in out.split("\n"):
        parts = line.split("|")
        if len(parts) >= 4:
            iid, repo, tag, size = parts[:4]
            created = parts[4] if len(parts) > 4 else ""
            vsize = parts[5] if len(parts) > 5 else ""
            images.append({
                "id": iid,
                "repository": repo,
                "tag": tag,
                "size": size,
                "created": created,
                "created_fmt": format_timestamp(created),
                "virtual_size": vsize,
                "is_dangling": repo == "<none>" and tag == "<none>",
            })
    return images


def get_volumes():
    """List volumes with details."""
    ok, out, _ = run_docker([
        "volume", "ls", "--format",
        "{{.Name}}|{{.Driver}}|{{.Mountpoint}}|{{.CreatedAt}}",
    ])
    if not ok or not out:
        return []

    volumes = []
    for line in out.split("\n"):
        parts = line.split("|")
        if len(parts) >= 2:
            name = parts[0]
            driver = parts[1]
            mount = parts[2] if len(parts) > 2 else ""
            created = parts[3] if len(parts) > 3 else ""
            volumes.append({
                "name": name,
                "driver": driver,
                "mountpoint": mount,
                "created": created,
                "created_fmt": format_timestamp(created),
            })
    return volumes


def get_networks():
    """List networks (excluding default ones)."""
    ok, out, _ = run_docker([
        "network", "ls", "--format",
        "{{.ID}}|{{.Name}}|{{.Driver}}|{{.Scope}}",
    ])
    if not ok or not out:
        return []

    networks = []
    for line in out.split("\n"):
        parts = line.split("|")
        if len(parts) >= 3:
            nid, name, driver = parts[:3]
            scope = parts[3] if len(parts) > 3 else ""
            if name not in ("bridge", "host", "none"):
                networks.append({
                    "id": nid,
                    "name": name,
                    "driver": driver,
                    "scope": scope,
                })
    return networks


def get_disk_usage():
    """Get Docker disk usage summary."""
    ok, out, _ = run_docker(["system", "df", "--format", "{{.Type}}|{{.TotalCount}}|{{.Size}}|{{.Reclaimable}}"])
    if not ok:
        return {}

    usage = {}
    for line in out.split("\n"):
        parts = line.split("|")
        if len(parts) >= 4:
            usage[parts[0].lower()] = {
                "count": int(parts[1]) if parts[1].isdigit() else parts[1],
                "size": parts[2],
                "reclaimable": parts[3],
            }
    return usage


def prune_containers(force=False):
    """Remove stopped containers."""
    print("🧹 Pruning stopped containers...")
    cmd = ["container", "prune", "-f"] if force else ["container", "prune"]
    ok, out, err = run_docker(cmd, timeout=120)
    if ok:
        reclaimed = "0B"
        for line in out.split("\n"):
            if "reclaimed" in line.lower() or "Total reclaimed space" in line:
                reclaimed = line.split(":")[-1].strip() if ":" in line else line
        print(f"  ✅ Done. Reclaimed: {reclaimed}")
        return reclaimed
    else:
        print(f"  ❌ Failed: {err}")
        return "0B"


def prune_images(force=False, all_=False):
    """Remove dangling/unused images."""
    label = "all dangling images" if not all_ else "ALL unused images"
    print(f"🧹 Pruning {label}...")
    cmd = ["image", "prune", "-f"] if force else ["image", "prune"]
    if all_:
        cmd.append("-a")
    ok, out, err = run_docker(cmd, timeout=120)
    if ok:
        reclaimed = "0B"
        for line in out.split("\n"):
            if "reclaimed" in line.lower() or "Total reclaimed space" in line:
                reclaimed = line.split(":")[-1].strip() if ":" in line else line
        print(f"  ✅ Done. Reclaimed: {reclaimed}")
        return reclaimed
    else:
        print(f"  ❌ Failed: {err}")
        return "0B"


def prune_volumes(force=False):
    """Remove unused volumes."""
    print("🧹 Pruning unused volumes...")
    cmd = ["volume", "prune", "-f"] if force else ["volume", "prune"]
    ok, out, err = run_docker(cmd, timeout=120)
    if ok:
        reclaimed = "0B"
        for line in out.split("\n"):
            if "reclaimed" in line.lower() or "Total reclaimed space" in line:
                reclaimed = line.split(":")[-1].strip() if ":" in line else line
        print(f"  ✅ Done. Reclaimed: {reclaimed}")
        return reclaimed
    else:
        print(f"  ❌ Failed: {err}")
        return "0B"


def prune_networks(force=False):
    """Remove unused networks."""
    print("🧹 Pruning unused networks...")
    cmd = ["network", "prune", "-f"] if force else ["network", "prune"]
    ok, out, err = run_docker(cmd, timeout=120)
    if ok:
        reclaimed = "0B"
        for line in out.split("\n"):
            if "reclaimed" in line.lower() or "Total reclaimed space" in line:
                reclaimed = line.split(":")[-1].strip() if ":" in line else line
        print(f"  ✅ Done. Reclaimed: {reclaimed}")
        return reclaimed
    else:
        print(f"  ❌ Failed: {err}")
        return "0B"


def prune_system(force=False):
    """Prune everything."""
    print("🧹 Running full system prune...")
    cmd = ["system", "prune", "-f"] if force else ["system", "prune"]
    ok, out, err = run_docker(cmd, timeout=180)
    if ok:
        reclaimed = "0B"
        for line in out.split("\n"):
            if "reclaimed" in line.lower() or "Total reclaimed space" in line:
                reclaimed = line.split(":")[-1].strip() if ":" in line else line
        print(f"  ✅ Done. Reclaimed: {reclaimed}")
        return reclaimed
    else:
        print(f"  ❌ Failed: {err}")
        return "0B"


def show_overview(usage):
    """Print disk usage overview table."""
    print(f"\n{'Type':<15} {'Count':<10} {'Size':<15} {'Reclaimable':<15}")
    print("-" * 55)
    for rtype in ("images", "containers", "volumes", "build cache"):
        if rtype in usage:
            u = usage[rtype]
            print(f"{rtype:<15} {str(u['count']):<10} {u['size']:<15} {u['reclaimable']:<15}")


def show_containers(containers):
    """Print containers table."""
    if not containers:
        print("  No containers found.")
        return
    print(f"\n{'CONTAINER ID':<15} {'NAME':<25} {'IMAGE':<25} {'STATUS':<20} {'CREATED':<12}")
    print("-" * 97)
    for c in containers:
        name = c["name"][:23]
        image = c["image"][:23]
        status = c["status"][:18]
        print(f"{c['id'][:12]:<15} {name:<25} {image:<25} {status:<20} {c['created_fmt']:<12}")


def show_images(images):
    """Print images table."""
    if not images:
        print("  No images found.")
        return

    dangling = [i for i in images if i["is_dangling"]]
    active = [i for i in images if not i["is_dangling"]]

    if active:
        print(f"\n{'IMAGE ID':<15} {'REPOSITORY':<30} {'TAG':<15} {'SIZE':<12} {'CREATED':<12}")
        print("-" * 84)
        for i in active:
            print(f"{i['id'][:12]:<15} {i['repository'][:28]:<30} {i['tag'][:13]:<15} {i['size']:<12} {i['created_fmt']:<12}")

    if dangling:
        print(f"\n⚠ Dangling images: {len(dangling)}")
        for i in dangling:
            print(f"  {i['id'][:12]} → {i['size']}")
        total_dangling = sum(parse_size(i["size"]) for i in dangling)
        print(f"  Total reclaimable: {get_size_human(total_dangling)}")


def show_volumes(volumes):
    """Print volumes table."""
    if not volumes:
        print("  No volumes found.")
        return
    print(f"\n{'VOLUME NAME':<30} {'DRIVER':<10} {'CREATED':<12}")
    print("-" * 52)
    for v in volumes:
        print(f"{v['name'][:28]:<30} {v['driver']:<10} {v['created_fmt']:<12}")


def show_networks(networks):
    """Print networks table."""
    if not networks:
        print("  No custom networks found.")
        return
    print(f"\n{'NETWORK ID':<15} {'NAME':<25} {'DRIVER':<10} {'SCOPE':<10}")
    print("-" * 60)
    for n in networks:
        print(f"{n['id'][:12]:<15} {n['name'][:23]:<25} {n['driver']:<10} {n['scope']:<10}")


def parse_size(size_str):
    """Parse size string to bytes."""
    if not size_str:
        return 0
    size_str = size_str.strip()
    multiplier = {"B": 1, "KB": 2**10, "MB": 2**20, "GB": 2**30, "TB": 2**40, "KiB": 2**10, "MiB": 2**20, "GiB": 2**30, "TiB": 2**40}
    for suffix, mult in multiplier.items():
        if size_str.endswith(suffix):
            try:
                return int(float(size_str[: -len(suffix)]) * mult)
            except ValueError:
                return 0
    return 0


def analyze_unused():
    """Find unused resources."""
    print("\n🔍 Analyzing unused resources...")

    # Stopped containers
    stopped = get_containers("exited")
    if stopped:
        print(f"\n  💤 Stopped containers ({len(stopped)}):")
        for c in stopped[:10]:
            print(f"    {c['name']} ({c['id'][:12]}) — {c['status']}")
        if len(stopped) > 10:
            print(f"    ... and {len(stopped) - 10} more")

    # Dangling images
    images = get_images()
    dangling = [i for i in images if i["is_dangling"]]
    if dangling:
        total = sum(parse_size(i["size"]) for i in dangling)
        print(f"\n  🗑 Dangling images ({len(dangling)}): ~{get_size_human(total)} reclaimable")
        for i in dangling:
            print(f"    {i['id'][:12]} → {i['size']}")

    # Unused volumes
    volumes = get_volumes()
    ok, out, _ = run_docker(["volume", "ls", "-qf", "dangling=true"])
    if ok and out:
        unused_vols = out.strip().split("\n")
        print(f"\n  📦 Unused volumes ({len(unused_vols)})")

    # Build cache
    usage = get_disk_usage()
    if "build cache" in usage:
        bc = usage["build cache"]
        print(f"\n  🏗 Build cache: {bc['size']} (reclaimable: {bc['reclaimable']})")


def generate_html_report(usage, containers, images, volumes, networks):
    """Generate HTML report of Docker cleanup analysis."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Usage rows
    usage_rows = ""
    for rtype in ("images", "containers", "volumes", "build cache"):
        if rtype in usage:
            u = usage[rtype]
            usage_rows += f"<tr><td>{rtype}</td><td>{u['count']}</td><td>{u['size']}</td><td>{u['reclaimable']}</td></tr>"

    container_rows = ""
    for c in containers[:20]:
        cls = "table-warning" if "exited" in c["status"].lower() else ""
        container_rows += f"<tr class='{cls}'><td>{c['id'][:12]}</td><td>{c['name']}</td><td>{c['image']}</td><td>{c['status']}</td><td>{c['created_fmt']}</td></tr>"

    image_rows = ""
    for i in images[:20]:
        cls = "table-danger" if i["is_dangling"] else ""
        image_rows += f"<tr class='{cls}'><td>{i['id'][:12]}</td><td>{i['repository']}</td><td>{i['tag']}</td><td>{i['size']}</td><td>{i['created_fmt']}</td></tr>"

    volume_rows = ""
    for v in volumes[:20]:
        volume_rows += f"<tr><td>{v['name']}</td><td>{v['driver']}</td><td>{v['created_fmt']}</td></tr>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Docker Cleanup Report</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>body {{ font-family: 'Segoe UI', sans-serif; padding: 2rem; background: #1a1a2e; color: #e0e0e0; }}
h1 {{ color: #00d4ff; }} .badge {{ font-size: 0.85rem; }}
</style></head>
<body>
<div class="container">
<h1>🐳 Docker Cleanup Report</h1>
<p class="text-muted">Generated: {now} | Host: {os.uname().nodename}</p>
<h3>📊 Disk Usage</h3>
<table class="table table-dark table-striped"><thead><tr><th>Type</th><th>Count</th><th>Size</th><th>Reclaimable</th></tr></thead><tbody>{usage_rows}</tbody></table>
<h3>📋 Containers ({len(containers)})</h3>
<table class="table table-dark table-sm"><thead><tr><th>ID</th><th>Name</th><th>Image</th><th>Status</th><th>Created</th></tr></thead><tbody>{container_rows}</tbody></table>
<h3>🖼 Images ({len(images)})</h3>
<table class="table table-dark table-sm"><thead><tr><th>ID</th><th>Repository</th><th>Tag</th><th>Size</th><th>Created</th></tr></thead><tbody>{image_rows}</tbody></table>
<h3>💾 Volumes ({len(volumes)})</h3>
<table class="table table-dark table-sm"><thead><tr><th>Name</th><th>Driver</th><th>Created</th></tr></thead><tbody>{volume_rows}</tbody></table>
<p class="text-muted mt-4"><small>Docker Cleanup Tool • ssl-report</small></p>
</div></body></html>"""

    fname = f"docker-cleanup-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"
    with open(fname, "w") as f:
        f.write(html)
    print(f"📄 HTML report saved: {fname}")
    return fname


def main():
    parser = argparse.ArgumentParser(
        description="Docker Cleanup Toolkit — clean & analyze Docker resources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--all", "-a", action="store_true", help="Full system prune (containers, images, volumes, networks)")
    parser.add_argument("--containers", action="store_true", help="Prune stopped containers")
    parser.add_argument("--images", action="store_true", help="Prune dangling images")
    parser.add_argument("--volumes", action="store_true", help="Prune unused volumes")
    parser.add_argument("--networks", action="store_true", help="Prune unused networks")
    parser.add_argument("--analyze", action="store_true", help="Analyze unused resources (dry-run)")
    parser.add_argument("--force", "-f", action="store_true", help="Force (no confirmation prompts)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--report", "-r", action="store_true", help="Generate HTML report")
    parser.add_argument("--no-header", action="store_true", help="Skip overview header")

    args = parser.parse_args()

    version = check_docker()
    if not args.no_header:
        print(f"🐳 Docker Engine v{version}")

    if not any([args.all, args.containers, args.images, args.volumes, args.networks, args.analyze, args.json, args.report]):
        args.analyze = True  # default: show analysis

    # Gather data
    usage = get_disk_usage()
    containers = get_containers()
    images = get_images()
    volumes = get_volumes()
    networks = get_networks()

    if args.analyze:
        show_overview(usage)
        show_containers(containers)
        show_images(images)
        show_volumes(volumes)
        show_networks(networks)
        analyze_unused()

    if args.containers:
        prune_containers(args.force)

    if args.images:
        prune_images(args.force)

    if args.volumes:
        prune_volumes(args.force)

    if args.networks:
        prune_networks(args.force)

    if args.all:
        prune_system(args.force)

    if args.json:
        output = {"version": version, "disk_usage": usage, "containers": containers, "images": images, "volumes": volumes, "networks": networks}
        print(json.dumps(output, indent=2, ensure_ascii=False))

    if args.report:
        generate_html_report(usage, containers, images, volumes, networks)


if __name__ == "__main__":
    main()
