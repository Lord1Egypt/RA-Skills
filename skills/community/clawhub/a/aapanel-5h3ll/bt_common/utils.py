# /// script
# dependencies = []
# ///
"""
Utility Functions Module
Provides formatted output, threshold checks, and alert generation
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class Alert:
    """Alert info"""

    level: str  # warning, critical
    type: str  # cpu, memory, disk, service, ssl, security
    message: str
    value: Optional[float] = None
    extra: dict = field(default_factory=dict)


def format_bytes(bytes_value: int, decimals: int = 2) -> str:
    """
    Format byte size to human-readable format

    Args:
        bytes_value: Number of bytes
        decimals: Number of decimal places

    Returns:
        Formatted string
    """
    if bytes_value == 0:
        return "0 B"

    k = 1024
    sizes = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    value = float(bytes_value)

    while value >= k and i < len(sizes) - 1:
        value /= k
        i += 1

    return f"{value:.{decimals}f} {sizes[i]}"


def format_uptime(seconds: int) -> str:
    """
    Format uptime

    Args:
        seconds: Number of seconds

    Returns:
        Formatted string
    """
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60

    if days > 0:
        return f"{days}d {hours}h"
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def format_timestamp(ts: Optional[str] = None) -> str:
    """
    Format timestamp

    Args:
        ts: ISO format timestamp, uses current time if None

    Returns:
        Formatted timestamp string
    """
    if ts:
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, AttributeError):
            return ts
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_system_monitor_data(data: dict, server_name: str) -> dict:
    """
    Parse system monitor data (from GetNetWork API response)

    Args:
        data: Raw API response
        server_name: Server name

    Returns:
        Formatted system monitor data
    """
    result = {
        "server": server_name,
        "timestamp": datetime.now().isoformat(),
        "version": data.get("version", "unknown"),
        "hostname": data.get("title", "unknown"),
        "system": data.get("simple_system", data.get("system", "unknown")),
        "uptime": data.get("time", "unknown"),
        "docker_running": data.get("docker_run", False),
    }

    # Parse CPU data
    # cpu format: [usage_rate%, core_count, [user_mode%, system_mode%], CPU_model, ?, ?]
    cpu_data = data.get("cpu", [])
    if isinstance(cpu_data, list) and len(cpu_data) >= 4:
        result["cpu"] = {
            "usage": round(cpu_data[0], 2) if isinstance(cpu_data[0], (int, float)) else 0,
            "cores": cpu_data[1] if isinstance(cpu_data[1], int) else 1,
            "user_usage": round(cpu_data[2][0], 2) if isinstance(cpu_data[2], list) and len(cpu_data[2]) > 0 else 0,
            "system_usage": round(cpu_data[2][1], 2) if isinstance(cpu_data[2], list) and len(cpu_data[2]) > 1 else 0,
            "model": cpu_data[3] if isinstance(cpu_data[3], str) else "Unknown",
        }
    else:
        result["cpu"] = {"usage": 0, "cores": 1, "model": "Unknown"}

    # Parse CPU time distribution
    cpu_times = data.get("cpu_times", {})
    if cpu_times:
        result["cpu"]["times"] = {
            "user": round(cpu_times.get("user", 0), 2),
            "system": round(cpu_times.get("system", 0), 2),
            "idle": round(cpu_times.get("idle", 0), 2),
            "iowait": round(cpu_times.get("iowait", 0), 2),
        }
        # Process count
        result["processes"] = {
            "total": cpu_times.get("total_processes", 0),
            "active": cpu_times.get("active_processes", 0),
        }

    # Parse load data
    load_data = data.get("load", {})
    if load_data:
        result["load"] = {
            "one_minute": round(load_data.get("one", 0), 2),
            "five_minute": round(load_data.get("five", 0), 2),
            "fifteen_minute": round(load_data.get("fifteen", 0), 2),
            "cpu_count": load_data.get("max", 1),
            "safe_limit": load_data.get("safe", 1),
        }

    # Parse memory data (unit: MB)
    mem_data = data.get("mem", {})
    if mem_data:
        mem_total = mem_data.get("memTotal", 0)
        mem_free = mem_data.get("memFree", 0)
        mem_cached = mem_data.get("memCached", 0)
        mem_buffers = mem_data.get("memBuffers", 0)
        mem_available = mem_data.get("memAvailable", 0)
        mem_used = mem_data.get("memRealUsed", mem_total - mem_free)

        result["memory"] = {
            "total_mb": mem_total,
            "total_gb": round(mem_total / 1024, 2),
            "used_mb": mem_used,
            "used_gb": round(mem_used / 1024, 2),
            "free_mb": mem_free,
            "available_mb": mem_available,
            "cached_mb": mem_cached,
            "buffers_mb": mem_buffers,
            "percent": round((mem_used / mem_total * 100), 2) if mem_total > 0 else 0,
            "available_percent": round((mem_available / mem_total * 100), 2) if mem_total > 0 else 0,
        }

    # Parse disk data
    disk_list = data.get("disk", [])
    disks = []
    total_size = 0
    total_used = 0

    for disk in disk_list:
        if isinstance(disk, dict):
            byte_size = disk.get("byte_size", [0, 0, 0])
            size_info = disk.get("size", ["0", "0", "0", "0%"])

            disk_total = byte_size[0] if isinstance(byte_size, list) and len(byte_size) > 0 else 0
            disk_used = byte_size[1] if isinstance(byte_size, list) and len(byte_size) > 1 else 0
            disk_free = byte_size[2] if isinstance(byte_size, list) and len(byte_size) > 2 else 0

            # Skip mounted remote storage (e.g., ossfs)
            filesystem = disk.get("filesystem", "")
            if "fuse" in filesystem.lower() or "ossfs" in filesystem.lower():
                continue

            disk_entry = {
                "path": disk.get("path", "/"),
                "filesystem": filesystem,
                "type": disk.get("type", "unknown"),
                "total_bytes": disk_total,
                "used_bytes": disk_used,
                "free_bytes": disk_free,
                "total_human": size_info[0] if len(size_info) > 0 else "0",
                "used_human": size_info[1] if len(size_info) > 1 else "0",
                "free_human": size_info[2] if len(size_info) > 2 else "0",
                "percent": float(size_info[3].replace("%", "").strip()) if len(size_info) > 3 and isinstance(size_info[3], str) else 0,
                "name": disk.get("rname", disk.get("path", "/")),
            }
            disks.append(disk_entry)
            total_size += disk_total
            total_used += disk_used

    result["disk"] = {
        "disks": disks,
        "total_bytes": total_size,
        "used_bytes": total_used,
        "free_bytes": total_size - total_used,
        "total_human": format_bytes(total_size),
        "used_human": format_bytes(total_used),
        "free_human": format_bytes(total_size - total_used),
        "percent": round((total_used / total_size * 100), 2) if total_size > 0 else 0,
    }

    # Parse network data
    result["network"] = {
        "total_up": format_bytes(data.get("upTotal", 0)),
        "total_down": format_bytes(data.get("downTotal", 0)),
        "current_up": round(data.get("up", 0), 2),  # KB/s
        "current_down": round(data.get("down", 0), 2),  # KB/s
        "up_packets": data.get("upPackets", 0),
        "down_packets": data.get("downPackets", 0),
        "interfaces": {},
    }

    # Per NIC data
    network_ifaces = data.get("network", {})
    for iface, stats in network_ifaces.items():
        if isinstance(stats, dict):
            result["network"]["interfaces"][iface] = {
                "up_total": format_bytes(stats.get("upTotal", 0)),
                "down_total": format_bytes(stats.get("downTotal", 0)),
                "current_up": round(stats.get("up", 0), 2),
                "current_down": round(stats.get("down", 0), 2),
            }

    # Resource statistics
    result["resources"] = {
        "sites": data.get("site_total", 0),
        "databases": data.get("database_total", 0),
        "ftp_accounts": data.get("ftp_total", 0),
    }

    # IO statistics
    iostat = data.get("iostat", {})
    if iostat and "ALL" in iostat:
        all_io = iostat["ALL"]
        result["io"] = {
            "read_count": all_io.get("read_count", 0),
            "write_count": all_io.get("write_count", 0),
            "read_bytes": format_bytes(all_io.get("read_bytes", 0)),
            "write_bytes": format_bytes(all_io.get("write_bytes", 0)),
        }

    return result


def parse_system_status_legacy(data: dict, server_name: str) -> dict:
    """
    Parse legacy system status response (GetSystemTotal API)

    Args:
        data: Raw API response
        server_name: Server name

    Returns:
        Formatted system status
    """
    mem_total = data.get("mem_total", 0)
    mem_used = data.get("mem_used", 0)
    disk_total = data.get("disk_total", 0)
    disk_used = data.get("disk_used", 0)

    # Convert to GB
    mem_total_gb = mem_total / 1024 / 1024 / 1024 if mem_total else 0
    mem_used_gb = mem_used / 1024 / 1024 / 1024 if mem_used else 0
    disk_total_gb = disk_total / 1024 / 1024 / 1024 if disk_total else 0
    disk_used_gb = disk_used / 1024 / 1024 / 1024 if disk_used else 0

    # Calculate percentage
    mem_percent = (mem_used / mem_total * 100) if mem_total > 0 else 0
    disk_percent = (disk_used / disk_total * 100) if disk_total > 0 else 0

    return {
        "server": server_name,
        "timestamp": datetime.now().isoformat(),
        "metrics": {
            "cpu": {
                "usage": float(data.get("cpu_usage", 0) or 0),
                "cores": int(data.get("cpu_core", 1) or 1),
                "model": data.get("cpu_model", "Unknown") or "Unknown",
            },
            "memory": {
                "used": round(mem_used_gb, 2),
                "total": round(mem_total_gb, 2),
                "percent": round(mem_percent, 2),
            },
            "disk": {
                "used": round(disk_used_gb, 2),
                "total": round(disk_total_gb, 2),
                "percent": round(disk_percent, 2),
            },
            "system": {
                "hostname": data.get("host_name", "Unknown") or "Unknown",
                "os": data.get("system", "Unknown") or "Unknown",
                "uptime": format_uptime(int(data.get("up_time", 0) or 0)),
            },
        },
    }


def check_thresholds(metrics: dict, thresholds: dict) -> list[Alert]:
    """
    Check threshold alerts

    Args:
        metrics: Formatted metrics data (from parse_system_monitor_data)
        thresholds: Threshold config

    Returns:
        Alert list
    """
    alerts = []

    cpu_threshold = thresholds.get("cpu", 80)
    memory_threshold = thresholds.get("memory", 85)
    disk_threshold = thresholds.get("disk", 90)

    # CPU alert
    cpu_data = metrics.get("cpu", {})
    cpu_usage = cpu_data.get("usage", 0)
    if cpu_usage >= cpu_threshold:
        alerts.append(
            Alert(
                level="warning",
                type="cpu",
                message=f"CPU usage too high: {cpu_usage}% (threshold: {cpu_threshold}%)",
                value=cpu_usage,
            )
        )

    # Memory alert
    mem_data = metrics.get("memory", {})
    mem_percent = mem_data.get("percent", 0)
    if mem_percent >= memory_threshold:
        alerts.append(
            Alert(
                level="warning",
                type="memory",
                message=f"Memory usage too high: {mem_percent}% (threshold: {memory_threshold}%)",
                value=mem_percent,
                extra={
                    "used_mb": mem_data.get("used_mb"),
                    "total_mb": mem_data.get("total_mb"),
                },
            )
        )

    # Disk alert
    disk_data = metrics.get("disk", {})
    disk_percent = disk_data.get("percent", 0)
    if disk_percent >= disk_threshold:
        alerts.append(
            Alert(
                level="critical",
                type="disk",
                message=f"Disk usage too high: {disk_percent}% (threshold: {disk_threshold}%)",
                value=disk_percent,
                extra={
                    "used_human": disk_data.get("used_human"),
                    "total_human": disk_data.get("total_human"),
                },
            )
        )

    # Check individual disk partitions
    for disk in disk_data.get("disks", []):
        disk_p = disk.get("percent", 0)
        if disk_p >= disk_threshold:
            alerts.append(
                Alert(
                    level="critical" if disk_p >= 95 else "warning",
                    type="disk",
                    message=f"Disk partition {disk.get('path', '/')} usage too high: {disk_p}%",
                    value=disk_p,
                    extra={"path": disk.get("path")},
                )
            )

    # Load alert
    load_data = metrics.get("load", {})
    if load_data:
        one_min_load = load_data.get("one_minute", 0)
        cpu_count = load_data.get("cpu_count", 1)
        # Alert when load exceeds CPU core count
        if one_min_load >= cpu_count:
            alerts.append(
                Alert(
                    level="warning",
                    type="load",
                    message=f"System load too high: {one_min_load} (CPU cores: {cpu_count})",
                    value=one_min_load,
                )
            )

    return alerts


def format_security_report(data: dict, server_name: str) -> dict:
    """
    Format security report

    Args:
        data: Raw security data
        server_name: Server name

    Returns:
        Formatted security report
    """
    return {
        "server": server_name,
        "timestamp": datetime.now().isoformat(),
        "security": {
            "firewall": {
                "status": data.get("firewall_status", "unknown"),
                "rules": data.get("firewall_rules", 0),
            },
            "ssh": {
                "failedAttempts": data.get("ssh_failed", 0),
                "lastLogin": data.get("last_login"),
                "lastLoginIp": data.get("last_login_ip"),
            },
            "suspiciousIps": data.get("suspicious_ips", []),
            "recentAlerts": data.get("security_alerts", []),
        },
    }


def format_service_status(services: list, server_name: str) -> dict:
    """
    Format service status

    Args:
        services: Service list
        server_name: Server name

    Returns:
        Formatted service status
    """
    formatted_services = []
    running_count = 0
    stopped_count = 0

    for svc in services:
        status = svc.get("status", "unknown")
        if status == "running":
            running_count += 1
        else:
            stopped_count += 1

        formatted_services.append(
            {
                "name": svc.get("name"),
                "status": status,
                "enabled": svc.get("enabled", True),
                "uptime": format_uptime(svc["uptime"]) if svc.get("uptime") else None,
            }
        )

    return {
        "server": server_name,
        "timestamp": datetime.now().isoformat(),
        "services": formatted_services,
        "summary": {
            "total": len(services),
            "running": running_count,
            "stopped": stopped_count,
        },
    }


def check_ssl_status(ssl_data) -> dict:
    """
    Check SSL certificate status

    Args:
        ssl_data: SSL data (can be dict, -1, or None)

    Returns:
        SSL status info
    """
    if ssl_data == -1 or ssl_data is None:
        return {"status": "none", "enabled": False, "message": "SSL not configured", "days_remaining": None}

    if not isinstance(ssl_data, dict):
        return {"status": "unknown", "enabled": False, "message": "SSL status unknown", "days_remaining": None}

    endtime = ssl_data.get("endtime", 0)
    if endtime is None:
        endtime = 0

    if endtime < 0:
        return {
            "status": "expired",
            "enabled": True,
            "message": f"Expired {-endtime} days ago",
            "days_remaining": endtime,
            "issuer": ssl_data.get("issuer_O", "Unknown"),
            "not_after": ssl_data.get("notAfter", ""),
        }
    elif endtime <= 7:
        return {
            "status": "critical",
            "enabled": True,
            "message": f"Expires in {endtime} days",
            "days_remaining": endtime,
            "issuer": ssl_data.get("issuer_O", "Unknown"),
            "not_after": ssl_data.get("notAfter", ""),
        }
    elif endtime <= 30:
        return {
            "status": "warning",
            "enabled": True,
            "message": f"Expires in {endtime} days",
            "days_remaining": endtime,
            "issuer": ssl_data.get("issuer_O", "Unknown"),
            "not_after": ssl_data.get("notAfter", ""),
        }
    else:
        return {
            "status": "valid",
            "enabled": True,
            "message": f"{endtime} days remaining",
            "days_remaining": endtime,
            "issuer": ssl_data.get("issuer_O", "Unknown"),
            "not_after": ssl_data.get("notAfter", ""),
        }


def parse_php_site(site: dict, server_name: str) -> dict:
    """
    Parse PHP site data

    Args:
        site: Site data
        server_name: Server name

    Returns:
        Formatted site info
    """
    # Determine running status
    status = "running" if site.get("status") == "1" and not site.get("stop") else "stopped"

    # Parse SSL
    ssl_info = check_ssl_status(site.get("ssl"))

    # Parse PHP version
    php_version = site.get("php_version", "")
    if php_version in ["static", "Static", "other", "Other"]:
        php_version = "static"

    return {
        "name": site.get("name", ""),
        "server": server_name,
        "type": "PHP",
        "status": status,
        "path": site.get("path", ""),
        "domains": site.get("domain", 0),
        "php_version": php_version,
        "proxy": site.get("proxy", False),
        "redirect": site.get("redirect", False),
        "waf_enabled": site.get("waf", {}).get("status", False),
        "backup_count": site.get("backup_count", 0),
        "ssl": ssl_info,
        "process": None,  # PHP projects have no process info
        "addtime": site.get("addtime", ""),
        "ps": site.get("ps", ""),
    }


def parse_project_site(project: dict, server_name: str) -> dict:
    """
    Parse project-type site data (Java/Node/Go/Python/.NET/Other)

    Args:
        project: Project data
        server_name: Server name

    Returns:
        Formatted project info
    """
    project_type = project.get("project_type", "Unknown")

    # Determine running status
    # Java: pid_info exists and pid > 0, starting=True means starting up
    # Node/Go/NET: load_info exists with pid, run=True
    # Python: run=True, pids not empty
    # Other: run=True, load_info not empty
    status = "stopped"
    process_info = None

    # Check process info
    load_info = project.get("load_info", {})
    pid_info = project.get("pid_info", {})
    pids = project.get("pids", [])

    if project_type == "Java":
        if pid_info and pid_info.get("pid"):
            status = "running"
            process_info = {
                "pid": pid_info.get("pid"),
                "status": pid_info.get("status", "unknown"),
                "memory_used": format_bytes(pid_info.get("memory_used", 0)),
                "cpu_percent": pid_info.get("cpu_percent", 0),
                "threads": pid_info.get("threads", 0),
                "running_time": pid_info.get("running_time", 0),
            }
        elif project.get("starting"):
            status = "starting"
    elif project_type == "Python":
        if project.get("run") or pids:
            status = "running"
            if pids:
                process_info = {"pids": pids}
    else:  # Node, Go, net, Other
        if project.get("run") or load_info:
            status = "running"
            if load_info:
                # load_info may have multiple processes
                first_pid = list(load_info.values())[0] if load_info else {}
                process_info = {
                    "pid": first_pid.get("pid"),
                    "status": first_pid.get("status", "unknown"),
                    "memory_used": format_bytes(first_pid.get("memory_used", 0)),
                    "cpu_percent": first_pid.get("cpu_percent", 0),
                    "threads": first_pid.get("threads", 0),
                    "connects": first_pid.get("connects", 0),
                }

    # Parse SSL
    ssl_info = check_ssl_status(project.get("ssl"))

    # Get domains
    project_config = project.get("project_config", {})
    domains = project_config.get("domains", [])

    # Get port
    port = project_config.get("port", "")

    return {
        "name": project.get("name", ""),
        "server": server_name,
        "type": project_type,
        "status": status,
        "path": project.get("path", ""),
        "domains": len(domains) if domains else 0,
        "domain_list": domains,
        "port": port,
        "ssl": ssl_info,
        "process": process_info,
        "addtime": project.get("addtime", ""),
        "ps": project.get("ps", ""),
    }


def parse_proxy_site(proxy: dict, server_name: str) -> dict:
    """
    Parse reverse proxy project data

    Args:
        proxy: Reverse proxy project data
        server_name: Server name

    Returns:
        Formatted reverse proxy project info
    """
    # Reverse proxy project status determined by status field and healthy field
    # status: "1" = running, "0" = stopped
    # healthy: 1 = healthy, 0 = unhealthy
    status = "running" if proxy.get("status") == "1" else "stopped"
    healthy = proxy.get("healthy", 1) == 1

    # Parse SSL
    ssl_info = check_ssl_status(proxy.get("ssl"))

    return {
        "name": proxy.get("name", ""),
        "server": server_name,
        "type": "Proxy",
        "status": status,
        "path": proxy.get("path", ""),
        "proxy_pass": proxy.get("proxy_pass", ""),
        "healthy": healthy,
        "waf_enabled": proxy.get("waf", {}).get("status", False),
        "ssl": ssl_info,
        "conf_path": proxy.get("conf_path", ""),
        "process": None,  # Reverse proxy projects have no process info
        "addtime": proxy.get("addtime", ""),
        "ps": proxy.get("ps", ""),
    }


def parse_html_site(html: dict, server_name: str) -> dict:
    """
    Parse HTML static project data

    Args:
        html: HTML project data
        server_name: Server name

    Returns:
        Formatted HTML project info
    """
    # HTML static project status determined by status field
    # status: "1" = running, "0" = stopped
    status = "running" if html.get("status") == "1" else "stopped"

    # Parse SSL
    ssl_info = check_ssl_status(html.get("ssl"))

    return {
        "name": html.get("name", ""),
        "server": server_name,
        "type": "HTML",
        "status": status,
        "path": html.get("path", ""),
        "ssl": ssl_info,
        "process": None,  # HTML static projects have no process info
        "addtime": html.get("addtime", ""),
        "ps": html.get("ps", ""),
    }


def parse_all_sites(sites_data: list, server_name: str) -> dict:
    """
    Parse all site/project data

    Args:
        sites_data: Site data list (from get_all_sites)
        server_name: Server name

    Returns:
        Formatted site summary info
    """
    sites = []
    alerts = []
    ssl_expiring = []
    ssl_expired = []

    for site in sites_data:
        source = site.get("_source", "PHP")

        if source == "PHP":
            parsed = parse_php_site(site, server_name)
        elif source == "Proxy":
            parsed = parse_proxy_site(site, server_name)
        elif source == "HTML":
            parsed = parse_html_site(site, server_name)
        else:
            parsed = parse_project_site(site, server_name)

        sites.append(parsed)

        # Check SSL alerts
        ssl_info = parsed.get("ssl", {})
        if ssl_info.get("status") == "expired":
            ssl_expired.append(parsed["name"])
            alerts.append({
                "level": "critical",
                "type": "ssl",
                "message": f"Site {parsed['name']} SSL certificate has expired",
                "site": parsed["name"],
            })
        elif ssl_info.get("status") == "critical":
            ssl_expiring.append(parsed["name"])
            alerts.append({
                "level": "critical",
                "type": "ssl",
                "message": f"Site {parsed['name']} SSL certificate expires in {ssl_info.get('days_remaining', 0)} days",
                "site": parsed["name"],
            })
        elif ssl_info.get("status") == "warning":
            ssl_expiring.append(parsed["name"])
            alerts.append({
                "level": "warning",
                "type": "ssl",
                "message": f"Site {parsed['name']} SSL certificate expires in {ssl_info.get('days_remaining', 0)} days",
                "site": parsed["name"],
            })

        # Check running status alerts
        if parsed["status"] == "stopped":
            alerts.append({
                "level": "warning",
                "type": "site",
                "message": f"Site {parsed['name']} has stopped",
                "site": parsed["name"],
            })

        # Check reverse proxy project health status
        if source == "Proxy" and not parsed.get("healthy", True):
            alerts.append({
                "level": "warning",
                "type": "proxy",
                "message": f"Reverse proxy project {parsed['name']} backend is unhealthy",
                "site": parsed["name"],
            })

    # Statistics
    by_type = {}
    by_status = {"running": 0, "stopped": 0, "starting": 0}
    for site in sites:
        site_type = site.get("type", "Unknown")
        by_type[site_type] = by_type.get(site_type, 0) + 1
        by_status[site.get("status", "stopped")] = by_status.get(site.get("status", "stopped"), 0) + 1

    return {
        "server": server_name,
        "timestamp": datetime.now().isoformat(),
        "sites": sites,
        "summary": {
            "total": len(sites),
            "by_type": by_type,
            "by_status": by_status,
            "ssl_expired": len(ssl_expired),
            "ssl_expiring": len(ssl_expiring),
        },
        "alerts": alerts,
    }


def print_table(data: list[dict], headers: Optional[list[str]] = None) -> str:
    """
    Generate table-formatted output

    Args:
        data: Data list
        headers: Column headers, extracted from data if None

    Returns:
        Formatted table string
    """
    if not data:
        return "No data"

    if headers is None:
        headers = list(data[0].keys())

    # Calculate column widths
    widths = [len(str(h)) for h in headers]
    for row in data:
        for i, h in enumerate(headers):
            value = row.get(h, "")
            widths[i] = max(widths[i], len(str(value)))

    # Build table
    lines = []

    # Header
    header_line = " | ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers))
    lines.append(header_line)
    lines.append("-+-".join("-" * w for w in widths))

    # Data rows
    for row in data:
        line = " | ".join(str(row.get(h, "")).ljust(widths[i]) for i, h in enumerate(headers))
        lines.append(line)

    return "\n".join(lines)


def output_result(data: Any, output_format: str = "json", output_file: Optional[str] = None) -> str:
    """
    Output result

    Args:
        data: Data to output
        output_format: Output format (json/table)
        output_file: Output file path

    Returns:
        Formatted output string
    """
    import json

    if output_format == "json":
        # Handle dataclass objects
        if hasattr(data, "__dataclass_fields__"):
            from dataclasses import asdict

            output = json.dumps(asdict(data), ensure_ascii=False, indent=2)
        elif isinstance(data, dict):
            output = json.dumps(data, ensure_ascii=False, indent=2)
        elif isinstance(data, list):
            output = json.dumps(data, ensure_ascii=False, indent=2)
        else:
            output = str(data)
    else:
        output = str(data)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)

    return output


def generate_summary_report(results: dict, report_type: str) -> str:
    """
    Generate summary report

    Args:
        results: Inspection results
        report_type: Report type (system/security/health)

    Returns:
        Formatted report string
    """
    lines = []
    timestamp = format_timestamp()

    if report_type == "system":
        lines.append("=" * 50)
        lines.append(f"System Resource Monitor Report - {timestamp}")
        lines.append("=" * 50)

        for server in results.get("servers", []):
            name = server.get("server", "Unknown")
            if "error" in server:
                lines.append(f"\n[{name}] Connection failed: {server['error']}")
                continue

            # New format data
            cpu = server.get("cpu", {})
            memory = server.get("memory", {})
            disk = server.get("disk", {})

            lines.append(f"\n[{name}]")
            lines.append(f"  System: {server.get('system', 'Unknown')} ({server.get('hostname', 'Unknown')})")
            lines.append(f"  Uptime: {server.get('uptime', 'Unknown')}")
            lines.append(f"  CPU: {cpu.get('usage', 0):.1f}% ({cpu.get('cores', 1)} cores - {cpu.get('model', 'Unknown')})")
            lines.append(f"  Memory: {memory.get('percent', 0):.1f}% ({memory.get('used_mb', 0)}/{memory.get('total_mb', 0)} MB)")
            lines.append(f"  Disk: {disk.get('percent', 0):.1f}% ({disk.get('used_human', '0')}/{disk.get('total_human', '0')})")

            # Resource statistics
            resources = server.get("resources", {})
            if resources:
                lines.append(f"  Resources: {resources.get('sites', 0)} sites, {resources.get('databases', 0)} databases")

            alerts = server.get("alerts", [])
            if alerts:
                lines.append(f"  Alerts: {len(alerts)}")
                for alert in alerts[:3]:
                    lines.append(f"    - [{alert['level']}] {alert['message']}")

        summary = results.get("summary", {})
        lines.append(f"\nSummary: Normal {summary.get('healthy', 0)}, Warning {summary.get('warning', 0)}, Error {summary.get('critical', 0)}")

    elif report_type == "security":
        lines.append("=" * 50)
        lines.append(f"Security Inspection Report - {timestamp}")
        lines.append("=" * 50)

        for server in results.get("servers", []):
            name = server.get("server", "Unknown")
            risk = server.get("riskLevel", "unknown")

            risk_emoji = {"low": "✅", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(risk, "❓")
            lines.append(f"\n[{name}] Risk Level: {risk_emoji} {risk.upper()}")

            if "error" in server:
                lines.append(f"  Check failed: {server['error']}")
                continue

            ssh = server.get("ssh", {})
            if ssh:
                lines.append(f"  SSH port: {ssh.get('port', 'N/A')}")

            firewall = server.get("firewall", {})
            if firewall:
                fw_status = "Running" if firewall.get("status") == "running" else "Stopped"
                lines.append(f"  Firewall: {fw_status}")

            alerts = server.get("alerts", [])
            if alerts:
                lines.append(f"  Alerts: {len(alerts)}")

        summary = results.get("summary", {})
        lines.append(
            f"\nSummary: Low risk {summary.get('low', 0)}, Medium risk {summary.get('medium', 0)}, "
            f"High risk {summary.get('high', 0)}, Critical {summary.get('critical', 0)}"
        )

    elif report_type == "health":
        lines.append("=" * 50)
        lines.append(f"Health Check Report - {timestamp}")
        lines.append("=" * 50)

        for server in results.get("servers", []):
            name = server.get("server", "Unknown")
            status = server.get("overallStatus", "unknown")

            status_emoji = {"healthy": "✅", "warning": "🟡", "critical": "🔴"}.get(status, "❓")
            lines.append(f"\n[{name}] Status: {status_emoji} {status.upper()}")

            if "error" in server:
                lines.append(f"  Check failed: {server['error']}")
                continue

            services = server.get("services", {})
            if services:
                lines.append(f"  Services: {services.get('running', 0)}/{services.get('total', 0)} running")

            sites = server.get("sites", {})
            if sites:
                lines.append(f"  Sites: {sites.get('running', 0)}/{sites.get('total', 0)} running")

            databases = server.get("databases", {})
            if databases:
                lines.append(f"  Databases: {databases.get('total', 0)}")

            alerts = server.get("alerts", [])
            if alerts:
                lines.append(f"  Alerts: {len(alerts)}")

        summary = results.get("summary", {})
        lines.append(
            f"\nSummary: Healthy {summary.get('healthy', 0)}, Warning {summary.get('warning', 0)}, "
            f"Error {summary.get('critical', 0)}"
        )

    lines.append("\n" + "=" * 50)
    return "\n".join(lines)
