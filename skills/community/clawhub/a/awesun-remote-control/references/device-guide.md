# Device Management Guide

Detailed device listing, searching, metadata management, permissions, and remote power control in `awesun-cli`.

---

## 1. Device Discovery & Query

### List Devices
Lists bound devices on the current account with paging support:

```bash
# Default listing (first 100 devices)
awesun-cli device ls

# Paged listing
awesun-cli device ls --limit 20 --page 1
```

### Search Devices
Fuzzy search across device names:

```bash
awesun-cli device search "office" --limit 10 --page 1
```

### Device Details
Query detailed system, hardware, and network status using the numeric `remote-id`:

```bash
awesun-cli device info 1738789907
```
Output returns:
- Device Name, Alias, Group
- Online status (`online` / `offline`)
- Internal and External IP addresses
- Operating System & AweSun client version

---

## 2. Device Metadata Management

### Add Device
Register a new device into the account list:
```bash
awesun-cli device add --name "Dev-Server-01" --desc "Build server in rack A"
```

### Update Device
Update device name or description:
```bash
awesun-cli device update 1738789907 --name "Dev-Server-01-Renamed" --desc "Updated description"
```

### Remove Device
Unbind and remove a device from the account:
```bash
awesun-cli device rm 1738789907
```

---

## 3. Credential & Grant Management (`device grant`)

Store access passwords locally to enable automated connections without repeated password prompts:

```bash
# Save host access password
awesun-cli device grant --remote-id 1738789907 --password "MySecretPass"

# Save system user password
awesun-cli device grant --remote-id 1738789907 --username "admin" --password "SysSecretPass"

# Remove saved credentials for a device
awesun-cli device grant --remote-id 1738789907 --remove

# Clear all saved device credentials
awesun-cli device grant --remove-all

# Batch import credentials from CSV (format: remote_id,password[,username])
awesun-cli device grant --file /path/to/credentials.csv
```

---

## 4. Remote Power Operations

### Remote Shutdown & Restart
Power operations require authentication (ACCESS password or SYSTEM username/password):

```bash
# Shutdown with interactive password prompt (or cached grant)
awesun-cli device shutdown 1738789907

# Shutdown specifying access password directly
awesun-cli device shutdown 1738789907 --password "MyPass"

# Shutdown specifying system user credentials
awesun-cli device shutdown 1738789907 --username "admin" --password "SysPass"

# Restart device
awesun-cli device restart 1738789907 --password "MyPass"
```

### Remote Wake-on-LAN (WoL)
Wake up sleeping or powered-off devices (requires target device and network WoL support):

```bash
awesun-cli device wakeup 1738789907
```
