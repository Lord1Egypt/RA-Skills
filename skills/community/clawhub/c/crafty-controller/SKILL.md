---
name: crafty_controller
description: "Use this skill whenever the user wants to interact with a Crafty Controller instance via its REST API. Triggers include: managing Minecraft servers, starting/stopping/restarting servers, sending console commands, checking server stats, managing users, handling backups, viewing logs, managing files, working with schedules, or any Crafty Controller-related task. Use for any request referencing 'Crafty', 'Crafty Controller', 'game server panel', or Minecraft server management through a web panel."
---

# Crafty Controller API Skill

---

## ⚙️ CONFIGURATION — SET THESE BEFORE ANYTHING ELSE

```python
# ============================================================
#  CRAFTY CONTROLLER CONNECTION SETTINGS
#  Edit these three values to match your Crafty instance
# ============================================================

CRAFTY_HOST    = "https://your-server-ip-or-domain"   # e.g. "https://192.168.1.50" or "https://crafty.myserver.com"
CRAFTY_PORT    = 8443                                   # Default Crafty port — change if you use a custom one
CRAFTY_API_KEY = "your_api_key_here"                   # Found in Crafty UI → Profile → API Key

# Derived base URL — do not edit
CRAFTY_BASE_URL = f"{CRAFTY_HOST}:{CRAFTY_PORT}/api/v2"

# Standard headers used on every request
HEADERS = {
    "Authorization": f"Bearer {CRAFTY_API_KEY}",
    "Content-Type": "application/json"
}
# ============================================================
```

> **Where to find your API key:**
> Log into Crafty Controller → click your username (top right) → **API Key** tab → copy the token.

---

## Overview

Crafty Controller exposes a REST API under `/api/v2`. All endpoints require Bearer token authentication. The API covers:

| Domain | What you can do |
|---|---|
| **Servers** | List, create, start, stop, restart, kill, delete |
| **Console** | Send commands, stream logs |
| **Stats** | CPU, RAM, player counts, ping, world size |
| **Backups** | List, trigger, restore, delete |
| **Schedules** | List, create, update, delete cron tasks |
| **Files** | Browse, read, write, upload, delete server files |
| **Users** | List, create, update, delete, assign roles |
| **Roles** | List, create, assign permissions |
| **Crafty Config** | Server-wide settings, announcements |

---

## Python Helper Setup

Install dependencies first:

```bash
pip install requests urllib3
```

Base client to reuse everywhere:

```python
import requests
import urllib3
import json

# Suppress SSL warnings if using self-signed cert (common on local Crafty installs)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def crafty_get(path, params=None):
    """GET request to Crafty API."""
    url = f"{CRAFTY_BASE_URL}{path}"
    resp = requests.get(url, headers=HEADERS, params=params, verify=False)
    resp.raise_for_status()
    return resp.json()

def crafty_post(path, payload=None):
    """POST request to Crafty API."""
    url = f"{CRAFTY_BASE_URL}{path}"
    resp = requests.post(url, headers=HEADERS, json=payload or {}, verify=False)
    resp.raise_for_status()
    return resp.json()

def crafty_patch(path, payload=None):
    """PATCH request to Crafty API."""
    url = f"{CRAFTY_BASE_URL}{path}"
    resp = requests.patch(url, headers=HEADERS, json=payload or {}, verify=False)
    resp.raise_for_status()
    return resp.json()

def crafty_delete(path):
    """DELETE request to Crafty API."""
    url = f"{CRAFTY_BASE_URL}{path}"
    resp = requests.delete(url, headers=HEADERS, verify=False)
    resp.raise_for_status()
    return resp.json()
```

---

## 1. Servers

### List All Servers
```python
def list_servers():
    """Returns all servers registered in Crafty."""
    data = crafty_get("/servers")
    for s in data.get("data", []):
        print(f"[{s['server_id']}] {s['server_name']} — Running: {s['running']}")
    return data
```

### Get Single Server Details
```python
def get_server(server_id: str):
    """Get full details for a specific server."""
    return crafty_get(f"/servers/{server_id}")
```

### Create a New Server
```python
def create_server(
    name: str,
    java_path: str = "java",
    jar_path: str = "server.jar",
    min_ram: int = 512,
    max_ram: int = 2048,
    port: int = 25565,
    crash_detection: bool = True,
    auto_start: bool = False,
):
    payload = {
        "name": name,
        "java_path": java_path,
        "jar_path": jar_path,
        "min_ram": min_ram,
        "max_ram": max_ram,
        "port": port,
        "crash_detection": crash_detection,
        "auto_start": auto_start,
    }
    return crafty_post("/servers", payload)
```

### Update Server Settings
```python
def update_server(server_id: str, changes: dict):
    """
    Patch any combination of server fields.
    Example changes: {"max_ram": 4096, "auto_start": True}
    """
    return crafty_patch(f"/servers/{server_id}", changes)
```

### Delete a Server
```python
def delete_server(server_id: str):
    """Permanently delete a server from Crafty (does NOT delete files by default)."""
    return crafty_delete(f"/servers/{server_id}")
```

---

## 2. Server Power Actions

All power actions POST to `/servers/{server_id}/action/{action}`.

```python
def server_action(server_id: str, action: str):
    """
    Valid actions:
      start_server    — start the server
      stop_server     — graceful stop
      restart_server  — stop then start
      kill_server     — force-kill (SIGKILL)
      backup_server   — trigger a backup immediately
    """
    return crafty_post(f"/servers/{server_id}/action/{action}")

# Convenience wrappers
def start_server(server_id):   return server_action(server_id, "start_server")
def stop_server(server_id):    return server_action(server_id, "stop_server")
def restart_server(server_id): return server_action(server_id, "restart_server")
def kill_server(server_id):    return server_action(server_id, "kill_server")
```

---

## 3. Console & Commands

### Send a Console Command
```python
def send_command(server_id: str, command: str):
    """
    Send any console command to a running server.
    Examples: "say Hello!", "op PlayerName", "weather clear", "stop"
    """
    return crafty_post(f"/servers/{server_id}/action/send_command", {"command": command})
```

### Common Command Shortcuts
```python
def op_player(server_id, player):     return send_command(server_id, f"op {player}")
def deop_player(server_id, player):   return send_command(server_id, f"deop {player}")
def kick_player(server_id, player, reason=""):
    cmd = f"kick {player}" + (f" {reason}" if reason else "")
    return send_command(server_id, cmd)
def ban_player(server_id, player, reason=""):
    cmd = f"ban {player}" + (f" {reason}" if reason else "")
    return send_command(server_id, cmd)
def say_message(server_id, message):  return send_command(server_id, f"say {message}")
def set_time(server_id, time):        return send_command(server_id, f"time set {time}")
def set_weather(server_id, weather):  return send_command(server_id, f"weather {weather}")
def give_item(server_id, player, item, amount=1):
    return send_command(server_id, f"give {player} {item} {amount}")
def teleport(server_id, player, x, y, z):
    return send_command(server_id, f"tp {player} {x} {y} {z}")
```

### Get Server Logs
```python
def get_logs(server_id: str):
    """Retrieve recent console log output for a server."""
    return crafty_get(f"/servers/{server_id}/logs")
```

---

## 4. Server Stats

```python
def get_server_stats(server_id: str):
    """
    Returns live stats:
      - running (bool)
      - online_players (int)
      - max_players (int)
      - cpu (float, %)
      - mem (float, MB)
      - world_size (str)
      - server_port (int)
      - version (str)
      - desc (str, MOTD)
    """
    return crafty_get(f"/servers/{server_id}/stats")

def print_server_stats(server_id: str):
    stats = get_server_stats(server_id)
    d = stats.get("data", {})
    status = "🟢 Online" if d.get("running") else "🔴 Offline"
    print(f"""
  Status  : {status}
  Players : {d.get('online_players', 0)}/{d.get('max_players', 0)}
  CPU     : {d.get('cpu', 0):.1f}%
  RAM     : {d.get('mem', 0):.1f} MB
  Version : {d.get('version', 'N/A')}
  World   : {d.get('world_size', 'N/A')}
    """)
```

### Get Stats for All Servers
```python
def get_all_stats():
    """Snapshot stats for every registered server."""
    return crafty_get("/servers/stats")
```

---

## 5. Backups

### List Backups for a Server
```python
def list_backups(server_id: str):
    return crafty_get(f"/servers/{server_id}/backups")
```

### Trigger a Manual Backup
```python
def trigger_backup(server_id: str):
    """Immediately run a backup for the given server."""
    return server_action(server_id, "backup_server")
```

### Get Backup Config
```python
def get_backup_config(server_id: str):
    return crafty_get(f"/servers/{server_id}/backups/config")
```

### Update Backup Config
```python
def update_backup_config(server_id: str, changes: dict):
    """
    Example changes:
    {
      "backup_path": "/backups/myserver",
      "max_backups": 5,
      "compress": True,
      "shutdown_server": False
    }
    """
    return crafty_patch(f"/servers/{server_id}/backups/config", changes)
```

### Delete a Backup
```python
def delete_backup(server_id: str, backup_filename: str):
    return crafty_delete(f"/servers/{server_id}/backups/{backup_filename}")
```

---

## 6. Schedules

### List Schedules
```python
def list_schedules(server_id: str):
    return crafty_get(f"/servers/{server_id}/schedules")
```

### Create a Schedule
```python
def create_schedule(
    server_id: str,
    name: str,
    action: str,         # "command", "start", "stop", "restart", "backup"
    interval: int,       # how often (in the unit below)
    interval_type: str,  # "hours", "minutes", "days", "weeks" or a cron string
    command: str = "",   # only needed for action="command"
    enabled: bool = True,
    one_time: bool = False,
    cron_string: str = "",
):
    payload = {
        "name": name,
        "action": action,
        "interval": interval,
        "interval_type": interval_type,
        "command": command,
        "enabled": enabled,
        "one_time": one_time,
        "cron_string": cron_string,
    }
    return crafty_post(f"/servers/{server_id}/schedules", payload)

# Example: restart every 6 hours
# create_schedule(server_id, "6hr restart", "restart", 6, "hours")

# Example: daily backup
# create_schedule(server_id, "Daily Backup", "backup", 24, "hours")

# Example: broadcast message every 30 minutes
# create_schedule(server_id, "30min broadcast", "command", 30, "minutes", command="say Server has been running for 30 more minutes!")
```

### Update a Schedule
```python
def update_schedule(server_id: str, schedule_id: str, changes: dict):
    return crafty_patch(f"/servers/{server_id}/schedules/{schedule_id}", changes)
```

### Delete a Schedule
```python
def delete_schedule(server_id: str, schedule_id: str):
    return crafty_delete(f"/servers/{server_id}/schedules/{schedule_id}")
```

---

## 7. File Management

### List Files / Browse Directory
```python
def list_files(server_id: str, path: str = ""):
    """
    Browse the server's file system.
    path is relative to the server's root directory.
    Leave empty to list the root.
    """
    return crafty_get(f"/servers/{server_id}/files", params={"path": path})
```

### Read a File
```python
def read_file(server_id: str, file_path: str):
    """
    Read the contents of a text file (e.g. server.properties, ops.json).
    file_path is relative to server root.
    """
    return crafty_get(f"/servers/{server_id}/files", params={"path": file_path, "file": "true"})
```

### Write / Update a File
```python
def write_file(server_id: str, file_path: str, content: str):
    """
    Overwrite a file with new content.
    Useful for editing server.properties, whitelist.json, etc.
    """
    return crafty_post(f"/servers/{server_id}/files/save", {
        "path": file_path,
        "content": content
    })
```

### Create a Directory
```python
def create_directory(server_id: str, dir_path: str):
    return crafty_post(f"/servers/{server_id}/files/create", {"path": dir_path})
```

### Delete a File or Directory
```python
def delete_file(server_id: str, file_path: str):
    return crafty_post(f"/servers/{server_id}/files/delete", {"path": file_path})
```

### Upload a File
```python
def upload_file(server_id: str, local_file_path: str, upload_dir: str = ""):
    """Upload a local file into the server's directory."""
    url = f"{CRAFTY_BASE_URL}/servers/{server_id}/files/upload"
    with open(local_file_path, "rb") as f:
        files = {"file": f}
        data = {"path": upload_dir}
        # Note: don't pass Content-Type header for multipart
        auth_headers = {"Authorization": f"Bearer {CRAFTY_API_KEY}"}
        resp = requests.post(url, headers=auth_headers, files=files, data=data, verify=False)
    resp.raise_for_status()
    return resp.json()
```

---

## 8. Users

### List All Users
```python
def list_users():
    return crafty_get("/users")
```

### Get a User
```python
def get_user(user_id: str):
    return crafty_get(f"/users/{user_id}")
```

### Create a User
```python
def create_user(
    username: str,
    password: str,
    email: str = "",
    enabled: bool = True,
    superuser: bool = False,
):
    return crafty_post("/users", {
        "username": username,
        "password": password,
        "email": email,
        "enabled": enabled,
        "superuser": superuser,
    })
```

### Update a User
```python
def update_user(user_id: str, changes: dict):
    """
    Example changes:
    {"password": "newpass", "enabled": False}
    """
    return crafty_patch(f"/users/{user_id}", changes)
```

### Delete a User
```python
def delete_user(user_id: str):
    return crafty_delete(f"/users/{user_id}")
```

### Update User Server Permissions
```python
def set_user_server_permissions(user_id: str, server_id: str, permissions: list):
    """
    Permissions list can contain any of:
      "Commands", "Terminal", "Logs", "Schedule", "Backup",
      "Files", "Config", "Players"
    """
    return crafty_patch(f"/users/{user_id}", {
        "server_permissions": {server_id: permissions}
    })
```

---

## 9. Roles

### List Roles
```python
def list_roles():
    return crafty_get("/roles")
```

### Get Role Details
```python
def get_role(role_id: str):
    return crafty_get(f"/roles/{role_id}")
```

### Create a Role
```python
def create_role(name: str, servers: dict = None):
    """
    servers = {
      "server_id_1": {"permissions": "1111111"},  # bitmask string
      ...
    }
    """
    return crafty_post("/roles", {
        "role_name": name,
        "servers": servers or {}
    })
```

### Update a Role
```python
def update_role(role_id: str, changes: dict):
    return crafty_patch(f"/roles/{role_id}", changes)
```

### Delete a Role
```python
def delete_role(role_id: str):
    return crafty_delete(f"/roles/{role_id}")
```

### Assign Role to User
```python
def assign_role_to_user(user_id: str, role_id: str):
    return crafty_patch(f"/users/{user_id}", {"roles": [role_id]})
```

---

## 10. Crafty System Info

### Get Crafty Version & System Stats
```python
def get_crafty_info():
    """Returns Crafty version, uptime, OS info, Python version, etc."""
    return crafty_get("/server/stats")
```

### Get All Audit Log Entries
```python
def get_audit_log():
    return crafty_get("/crafty/audit-log")
```

---

## Error Handling

All functions can raise `requests.HTTPError`. Wrap calls for production use:

```python
def safe_call(fn, *args, **kwargs):
    try:
        result = fn(*args, **kwargs)
        if result.get("status") == "ok":
            return result.get("data")
        else:
            print(f"Crafty API error: {result.get('error')} — {result.get('data')}")
            return None
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Crafty at {CRAFTY_BASE_URL}. Check HOST and PORT.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP {e.response.status_code}: {e.response.text}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    return None
```

---

## Common Patterns

### Full Server Status Dashboard
```python
def dashboard():
    servers = crafty_get("/servers").get("data", [])
    print(f"{'Name':<25} {'Status':<10} {'Players':<12} {'CPU':<8} {'RAM'}")
    print("-" * 70)
    for s in servers:
        sid = s["server_id"]
        stats = get_server_stats(sid).get("data", {})
        status  = "Online " if stats.get("running") else "Offline"
        players = f"{stats.get('online_players',0)}/{stats.get('max_players',0)}"
        cpu     = f"{stats.get('cpu', 0):.1f}%"
        ram     = f"{stats.get('mem', 0):.0f}MB"
        print(f"{s['server_name']:<25} {status:<10} {players:<12} {cpu:<8} {ram}")
```

### Restart All Running Servers
```python
def restart_all():
    servers = crafty_get("/servers").get("data", [])
    for s in servers:
        if s.get("running"):
            print(f"Restarting {s['server_name']}...")
            restart_server(s["server_id"])
```

### Edit server.properties Value
```python
def set_property(server_id: str, key: str, value: str):
    """
    Read server.properties, change one key, write it back.
    Example: set_property(sid, "max-players", "50")
    """
    result = read_file(server_id, "server.properties")
    content = result.get("data", {}).get("content", "")
    lines = content.splitlines()
    new_lines = []
    found = False
    for line in lines:
        if line.startswith(f"{key}="):
            new_lines.append(f"{key}={value}")
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f"{key}={value}")
    write_file(server_id, "server.properties", "\n".join(new_lines))
    print(f"✅ Set {key}={value}")
```

---

## API Response Structure

Every Crafty API response follows this envelope:

```json
{
  "status": "ok",       // "ok" or "error"
  "data": { ... },      // payload (dict, list, or string)
  "error": null         // error message if status is "error"
}
```

Always check `response["status"] == "ok"` before using `response["data"]`.

---

## Notes

- **SSL:** Crafty uses a self-signed certificate by default. The helpers above pass `verify=False`. In production, provide your real cert path: `verify="/path/to/cert.pem"`.
- **API version:** This skill targets Crafty Controller **v4** (`/api/v2` routes). Crafty 3 uses a different API.
- **Permissions:** Your API key inherits the permissions of the user it belongs to. For full access, generate the key from a superuser account.
- **Rate limiting:** Crafty does not enforce rate limiting by default, but avoid hammering the stats endpoint — poll at most once per 5 seconds.
