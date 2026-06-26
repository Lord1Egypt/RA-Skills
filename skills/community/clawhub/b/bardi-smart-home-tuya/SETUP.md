# Setup — Bardi Smart Home - Tuya Devices Compatible

## Install Dependencies

```bash
pip install tinytuya
```

If your system blocks pip installs (PEP 668), use a virtual environment:

```bash
python3 -m venv ~/tuya-env
source ~/tuya-env/bin/activate
pip install tinytuya
```

## Configure Credentials

Set these environment variables (add to `~/.bashrc` or `~/.zshrc`):

```bash
export TUYA_ACCESS_ID="your-access-id"
export TUYA_ACCESS_SECRET="your-access-secret"
export TUYA_API_REGION="sg"
```

### Required Variables

| Variable | Description |
|----------|-------------|
| `TUYA_ACCESS_ID` | Cloud project Access ID from Tuya IoT Platform |
| `TUYA_ACCESS_SECRET` | Cloud project Access Secret from Tuya IoT Platform |
| `TUYA_API_REGION` | Data center region (default: `sg`) |

### Where to Get Credentials

1. Go to [https://iot.tuya.com](https://iot.tuya.com) (international) or [https://tuyasmart.com](https://tuyasmart.com) (China)
2. Create a cloud project
3. Copy the **Access ID** and **Access Secret** from the project overview
4. Enable the "Smart Home Devices" API group

### Region Selection

| Region Code | Data Center |
|-------------|-------------|
| `sg` | Singapore (default) |
| `us` | US West |
| `eu` | Central Europe |
| `cn` | China mainland |
| `in` | India |

## Verify Installation

```bash
python3 scripts/devices_control.py discover
```

Should list all devices linked to your Tuya account.

## Local Network Discovery

```bash
python3 scripts/devices_scan.py
```

Requires devices to be on the same network.

## Notes

- Cloud API requires internet connection
- Local scan works without cloud credentials
- Device must be linked to your Tuya account for cloud control
- Local scanner sends UDP broadcast packets (255.255.255.255) — this is normal for device discovery but may be visible on your network and could be blocked by firewalls
- Keep TUYA_ACCESS_ID and TUYA_ACCESS_SECRET scoped to a dedicated Tuya cloud project with least-privilege access
