# Prevention Scripts Setup

## Shutdown Flush Script

Flushes write cache before Windows shuts down.

### Create the script

Save as `C:\Users\<user>\backups\safe_shutdown.ps1`:

```powershell
$logPath = "C:\Users\$env:USERNAME\backups\shutdown_log.txt"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
try {
    Write-VolumeCache -DriveLetter H -ErrorAction Stop
    "$timestamp : Flushed write cache for H:" | Out-File $logPath -Append
} catch {
    "$timestamp : ERROR flushing cache - $($_.Exception.Message)" | Out-File $logPath -Append
}
```

### Register as Group Policy shutdown script

Run as Administrator:

```powershell
$shutdownScript = "C:\Users\$env:USERNAME\backups\safe_shutdown.ps1"

foreach ($basePath in @(
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Group Policy\Scripts\Shutdown\0",
    "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Group Policy\State\Machine\Scripts\Shutdown\0"
)) {
    $scriptKey = "$basePath\0"
    if (-not (Test-Path $basePath)) { New-Item -Path $basePath -Force | Out-Null }
    Set-ItemProperty -Path $basePath -Name "GPO-ID" -Value "LocalGPO" -Type String
    Set-ItemProperty -Path $basePath -Name "SOM-ID" -Value "Local" -Type String
    Set-ItemProperty -Path $basePath -Name "FileSysPath" -Value "C:\Windows\System32\GroupPolicy\Machine" -Type String
    Set-ItemProperty -Path $basePath -Name "DisplayName" -Value "Local Group Policy" -Type String
    Set-ItemProperty -Path $basePath -Name "GPOName" -Value "Local Group Policy" -Type String
    Set-ItemProperty -Path $basePath -Name "PSScriptOrder" -Value 1 -Type DWord
    if (-not (Test-Path $scriptKey)) { New-Item -Path $scriptKey -Force | Out-Null }
    Set-ItemProperty -Path $scriptKey -Name "Script" -Value $shutdownScript -Type String
    Set-ItemProperty -Path $scriptKey -Name "Parameters" -Value "" -Type String
    Set-ItemProperty -Path $scriptKey -Name "IsPowershell" -Value 1 -Type DWord
    Set-ItemProperty -Path $scriptKey -Name "ExecTime" -Value ([byte[]](0x00 * 16)) -Type Binary
}
```

## Boot Region Backup (Weekly)

### Create the backup script

Save as `C:\Users\<user>\backups\backup_boot_region.ps1`:

```powershell
$ErrorActionPreference = "Stop"
# Find your disk number: Get-Partition -DriveLetter H | Select DiskNumber
# Find offset: Get-Partition -DriveLetter H | Select Offset
$disk = "\\.\PhysicalDrive3"
$offset = 16777216  # partition offset in bytes
$size = 24 * 512    # 24 sectors (12 main + 12 backup boot region)
$outDir = "C:\Users\$env:USERNAME\backups\exfat_boot"
$outPath = "$outDir\exfat_boot_region_$(Get-Date -Format 'yyyyMMdd').bin"
$logPath = "$outDir\backup_log.txt"

if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }

try {
    $fs = [System.IO.File]::Open($disk, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
    [void]$fs.Seek($offset, [System.IO.SeekOrigin]::Begin)
    $buf = New-Object byte[] $size
    $read = $fs.Read($buf, 0, $size)
    $fs.Close()
    [System.IO.File]::WriteAllBytes($outPath, $buf)
    "$(Get-Date): Backed up $read bytes to $outPath" | Out-File $logPath -Append
} catch {
    "$(Get-Date): ERROR - $_" | Out-File $logPath -Append
}
```

### Create scheduled task

```powershell
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -File `"C:\Users\$env:USERNAME\backups\backup_boot_region.ps1`""
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At "3:00AM"
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -RunLevel Highest -LogonType ServiceAccount
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "BackupExFATBootRegion" -Action $action -Trigger $trigger `
    -Principal $principal -Settings $settings -Description "Weekly backup of exFAT boot region"
```
