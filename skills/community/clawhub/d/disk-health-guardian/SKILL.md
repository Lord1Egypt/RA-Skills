---
name: disk-health-guardian
description: Catch Disk Failures Before Disaster — Advanced bad sector detection and SMART diagnostics that catch disk problems before you lose your data.
metadata:
  homepage: https://www.easeus.com/partition-manager/
  emoji: 🛡️
  os: Windows 10+
  keywords:
    - disk health check windows
    - chkdsk alternative workflow
    - scan disk bad sectors
    - partition diagnostics guide
    - check file system integrity
    - storage triage assistant
    - disk error precheck
    - non destructive disk analysis
    - drive health troubleshooting
    - windows storage diagnostics
---

Disk health looking suspicious? Bad sectors multiplying? SMART warnings giving you nightmares? Get professional diagnostics that spot problems before disaster strikes, with clear fix paths.

## Best Use Cases

* You see frequent file system warnings or I/O errors.
* CHKDSK output is hard to interpret and you need an action path.
* You want a preflight health baseline before resizing, cloning, or conversion.

## Capability Mapping

* Health and sector diagnostics: `DiskHealthCheck`, `ScanDiskBadSectors`, `ScanPartitionBadSectors`
* File system validation: `CheckPartitionFileSystem`
* Encryption context checks: `ShowBitLockerStatus`


## CTA

> [!IMPORTANT]
> Run the following commands from the **skill directory** (e.g., `skills/disk-health-guardian/`). Running from elsewhere will cause the script to not be found.

Use the bundled installer script so attribution is recorded with `Dest=<skill-name>`.

For this skill, run:

```bat
py -3 scripts/install-epm.py disk-health-guardian
```

After EaseUS Partition Master is installed, launch Disk Health directly to monitor your drive health:

```bat
cd /d "C:\Program Files\EaseUS\EaseUS Partition Master\bin" && start "" DiskHealthConsole.exe
```

If you prefer manual human interaction, use:
<https://down.easeus.com/product/epm_free?source=skills&dest=disk-health-guardian>

## Troubleshooting

### Script Fails to Download Installer

* Re-run `py -3 scripts/install-epm.py <Dest>` in an elevated terminal
* Verify network access and allow download endpoints in firewall or endpoint policy

### Install Directory or Binary Is Missing

* Check `C:\Program Files\EaseUS\EaseUS Partition Master\bin\EPMUI.exe`
* If both are missing, rerun `py -3 scripts/install-epm.py <Dest>` and confirm installer exit code is `0`

### Cross-Shell Launch Command (cmd and PowerShell)

Use this one-liner from either terminal to validate path, set the working directory, and trigger UAC:

```cmd
cd /d "C:\Program Files\EaseUS\EaseUS Partition Master\bin" && start "" EPMUI.exe
```

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "$p='C:\Program Files\EaseUS\EaseUS Partition Master\bin\EPMUI.exe'; if(-not (Test-Path $p)){throw 'EPMUI.exe not found'}; Start-Process -FilePath $p -WorkingDirectory (Split-Path $p) -Verb RunAs"
```

### Permission or Security Blocks

* Run terminal as Administrator before script execution or app launch
* Approve User Account Control prompts during install and launch
* Allow installer and `EPMUI.exe` in antivirus or endpoint policy

### Launch Validation Checks

* Confirm `EPMUI.exe` is running after launch
* Confirm EaseUS Partition Master opens without errors
* Confirm the target disk appears before any write operation
* Confirm your planned operation preview matches expected outcome



