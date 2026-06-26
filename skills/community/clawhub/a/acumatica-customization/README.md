# acumatica-customization

A Claude skill + bash helper for managing **Acumatica ERP customization projects**
via the official `CustomizationApi` web API.

---

## What's Included

| File                      | Purpose                                                       |
|---------------------------|---------------------------------------------------------------|
| `acumaticahelper.sh`      | Main script — all API calls live here                        |
| `acumatica.conf.example`  | Template config — copy to `acumatica.conf` and fill in       |
| `acumatica.conf`          | Your live config (gitignore this — contains credentials)      |
| `SKILL.md`                | Claude skill definition — loaded when the skill triggers      |

---

## Quick Start

### 1. Configure

```bash
cp acumatica.conf.example acumatica.conf
# Edit acumatica.conf:
#   ACUMATICA_URL=http://yourhost/instance
#   ACUMATICA_USERNAME=admin
#   ACUMATICA_PASSWORD=secret
```

> The config file must live in the **same directory** as `acumaticahelper.sh`.

### 2. Make executable

```bash
chmod +x acumaticahelper.sh
```

### 3. Run

```bash
./acumaticahelper.sh help
./acumaticahelper.sh list
```

---

## Commands at a Glance

```
./acumaticahelper.sh list
./acumaticahelper.sh export   <project-name> [output-dir]
./acumaticahelper.sh import   <file.zip> [project-name] [description]
./acumaticahelper.sh validate <project-name> [project-name2 ...]
./acumaticahelper.sh publish  <project-name> [project-name2 ...]
./acumaticahelper.sh unpublish [Current|All]
./acumaticahelper.sh delete   <project-name>
./acumaticahelper.sh status
./acumaticahelper.sh maintenance-on
./acumaticahelper.sh maintenance-off
```

Full documentation for every command: see **SKILL.md**.

---

## Configuration Reference

**Required** (in `acumatica.conf`):

| Key                  | Description                                            |
|----------------------|--------------------------------------------------------|
| `ACUMATICA_URL`      | Base URL of the instance, no trailing slash            |
| `ACUMATICA_USERNAME` | Login — must have the **Customizer** role              |
| `ACUMATICA_PASSWORD` | Password                                               |

**Optional tuning:**

| Key                    | Default | Description                               |
|------------------------|---------|-------------------------------------------|
| `PUBLISH_POLL_INTERVAL`| `30`    | Seconds between `publishEnd` polls        |
| `PUBLISH_MAX_ATTEMPTS` | `10`    | Max polls before timeout (default: 5 min) |

---

## Requirements

- `bash` 4+
- `curl`
- `jq`
- `base64`
- `python3` (standard library only — used for ZIP validation on export)

> **Note:** OAuth 2.0 is not supported by the `CustomizationApi`. The script
> uses cookie-based session auth (`/entity/auth/login`). The session is always
> cleaned up via a `trap '_logout' EXIT`.

---

## Security Note

`acumatica.conf` contains plaintext credentials. Add it to `.gitignore` and
restrict file permissions:

```bash
chmod 600 acumatica.conf
```

---

## Common Workflows

**Backup a project:**
```bash
./acumaticahelper.sh export MyProject ./backups
```

**Promote dev → prod:**
```bash
# dev
./acumaticahelper.sh export MyProject ./release

# prod
./acumaticahelper.sh import ./release/MyProject.zip
./acumaticahelper.sh publish MyProject
```

**Publish with maintenance window:**
```bash
./acumaticahelper.sh maintenance-on
./acumaticahelper.sh publish MyProject
./acumaticahelper.sh maintenance-off
```

---

## API Reference

All endpoints used are from Acumatica's official
*"Managing Customization Projects by Using the Web API"* documentation.

| Command          | Endpoint                                             | Method |
|------------------|------------------------------------------------------|--------|
| `list`           | `/CustomizationApi/getPublished`                     | POST   |
| `export`         | `/CustomizationApi/getProject`                       | POST   |
| `import`         | `/CustomizationApi/import`                           | POST   |
| `validate`       | `/CustomizationApi/publishBegin` + `publishEnd`      | POST   |
| `publish`        | `/CustomizationApi/publishBegin` + `publishEnd`      | POST   |
| `unpublish`      | `/CustomizationApi/unpublishAll`                     | POST   |
| `delete`         | `/CustomizationApi/delete`                           | POST   |
| `status`         | `/CustomizationApi/publishEnd`                       | POST   |
| `maintenance-on` | `/entity/Lock/1/ApplyUpdate/scheduleLockoutCommand`  | PUT    |
| `maintenance-off`| `/entity/Lock/1/ApplyUpdate/stopLockoutCommand`      | PUT    |
