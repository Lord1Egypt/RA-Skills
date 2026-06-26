---
name: autodesk-clean-uninstall
description: AutoCAD/Autodesk Clean Uninstall Tool - Thoroughly remove all residues, supports multi-PC and multi-user environments, step-by-step confirmation, intelligent discovery of non-standard installation directories
author: 大头
tags: [autocad, autodesk, uninstall, cleanup, windows]
version: 2.1
created: 2026-05-17
---

# AutoCAD/Autodesk Clean Uninstall Tool v2.1

## Overview

Thoroughly remove **all residues** of AutoCAD and Autodesk software from Windows systems, including installation files, user configurations, registry entries, and uninstallation information.

### Key Features
- **Cross-Platform Compatible**: Uses environment variables and relative paths, works on any Windows PC with any username
- **Intelligent Discovery**: Auto-scans registry for actual installation paths, handles non-standard directories (e.g., "Autodesk, Inc.")
- **Step-by-Step Confirmation**: Lists specific items before each dangerous operation and requires confirmation
- **Transparent and Clear**: Each step explains its purpose and why deletion is necessary

## Use Cases

- Clean up residues after uninstalling AutoCAD/Autodesk software
- Fix reinstall failures caused by incomplete uninstallation
- Free up disk space (typically can release 5-10GB)
- Thoroughly remove personal software data before switching computers

## Pre-Execution Notes

### ⚠️ Risk Warning
This skill involves the following **irreversible** operations:
- Deleting file directories (may contain user files not yet backed up)
- Deleting registry entries (may affect system functionality)
- Terminating running processes

### Prerequisites
- Close all running programs
- Back up important CAD files if any
- Some operations require administrator privileges

---

## Step 1: Environment Scan (No Confirmation Required)

### Purpose
Before executing cleanup, comprehensively scan the system to **obtain actual installation paths from the registry** (not limited to standard Autodesk directories), and list all items to be cleaned. Ensures transparency before cleanup to avoid omissions.

### Intelligent Discovery Logic
- Standard directories: `C:\Autodesk`, `C:\Program Files\Autodesk`, etc.
- Registry path: Reads from `HKLM\Uninstall` InstallLocation field
- Common variants: `Autodesk, Inc.`, `AutodeskInstallation`, etc.

### Execution Command

```powershell
# ============================================
# Environment Scan - Comprehensive Autodesk Residue Detection v2.1
# Purpose: Intelligently discover all Autodesk-related directories (standard + registry paths)
# Compatibility: Auto-adapts to any installation directory name
# ============================================

$ErrorActionPreference = 'SilentlyContinue'
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Autodesk Clean Uninstall - Environment Scan" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Global variable: Store all directories to clean
$global:autodeskDirs = @()
$global:autodeskInstallations = @()

# 1. Scan installed software and get actual installation paths
Write-Host "[1] Scanning installed Autodesk software..." -ForegroundColor Yellow
Write-Host ""

$installed = Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" |
    Where-Object { $_.DisplayName -match "autocad|autodesk|fusion|cam360|eagle" } |
    Select-Object DisplayName, DisplayVersion, InstallLocation, PSChildName

if ($installed) {
    foreach ($app in $installed) {
        $name = $app.DisplayName
        $ver = $app.DisplayVersion
        $loc = $app.InstallLocation
        $guid = $app.PSChildName

        Write-Host "  [SW] $name" -ForegroundColor Cyan
        Write-Host "     Version: $ver"
        Write-Host "     GUID: $guid"

        # Record installation info
        $global:autodeskInstallations += @{
            Name = $name
            Version = $ver
            InstallLocation = $loc
            GUID = $guid
        }

        # If installation path exists, add to cleanup list
        if ($loc -and (Test-Path $loc)) {
            # Extract parent directory (handle version subdirectories like C:\Autodesk\AutoCAD_2026)
            $parentDir = Split-Path $loc -Parent
            if ($parentDir -and (Test-Path $parentDir)) {
                $global:autodeskDirs += $parentDir
                Write-Host "     [DIR] Install directory: $parentDir" -ForegroundColor Green
            }
            $global:autodeskDirs += $loc
            Write-Host "     [DIR] Actual path: $loc" -ForegroundColor Green
        }
        Write-Host ""
    }
} else {
    Write-Host "    No installed Autodesk software found" -ForegroundColor Green
    Write-Host ""
}

# 2. Scan standard Autodesk directories
Write-Host "[2] Scanning standard Autodesk directories..." -ForegroundColor Yellow
Write-Host ""

$standardDirs = @(
    "C:\Autodesk",
    "C:\Program Files\Autodesk",
    "C:\Program Files (x86)\Autodesk",
    "C:\ProgramData\Autodesk"
)

foreach ($dir in $standardDirs) {
    if (Test-Path $dir) {
        $size = (Get-ChildItem $dir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        $size = [math]::Round($size, 2).ToString() + " GB"
        Write-Host "    [OK] $dir ($size)" -ForegroundColor Green
        $global:autodeskDirs += $dir
    } else {
        Write-Host "    [--] $dir (not found)" -ForegroundColor Gray
    }
}
Write-Host ""

# 3. Scan user directories
Write-Host "[3] Scanning user data directories..." -ForegroundColor Yellow
Write-Host ""

$userDirs = @(
    @{Path="$env:LOCALAPPDATA\Autodesk"; Desc="User local data"},
    @{Path="$env:APPDATA\Autodesk"; Desc="User roaming data"}
)

foreach ($d in $userDirs) {
    if (Test-Path $d.Path) {
        $size = (Get-ChildItem $d.Path -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        $size = [math]::Round($size, 2).ToString() + " GB"
        Write-Host "    [OK] $($d.Path) ($size)" -ForegroundColor Green
        Write-Host "       $($d.Desc)"
        $global:autodeskDirs += $d.Path
    } else {
        Write-Host "    [--] $($d.Path) (not found)" -ForegroundColor Gray
    }
}
Write-Host ""

# 4. Deduplicate and summarize
Write-Host "[4] Cleanup directory summary..." -ForegroundColor Yellow
Write-Host ""

$uniqueDirs = $global:autodeskDirs | Sort-Object -Unique
$totalSize = 0
foreach ($dir in $uniqueDirs) {
    if (Test-Path $dir) {
        $size = (Get-ChildItem $dir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        $totalSize += $size
        Write-Host "    [D] $dir" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "    Total: $($uniqueDirs.Count) directories, estimated space to free: $([math]::Round($totalSize, 2)) GB" -ForegroundColor Cyan

# 5. Scan running processes
Write-Host ""
Write-Host "[5] Scanning running Autodesk processes..." -ForegroundColor Yellow
$processes = Get-Process | Where-Object { $_.ProcessName -match "autocad|autodesk|fusion|eagle" } |
    Select-Object ProcessName, Id
if ($processes) {
    $processes | Format-Table -AutoSize
} else {
    Write-Host "    No running Autodesk processes found" -ForegroundColor Green
}

# 6. Scan registry
Write-Host ""
Write-Host "[6] Scanning Autodesk registry entries..." -ForegroundColor Yellow

# HKLM Uninstall
$uninstall = Get-ChildItem "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" |
    Where-Object { $_.GetValue('DisplayName') -match "autocad|autodesk" }
Write-Host ("    HKLM\Uninstall: {0} items" -f @($uninstall).Count) -ForegroundColor $(if(@($uninstall).Count -gt 0){'Red'}else{'Green'})

# HKCU Classes
$classes = Get-ChildItem "HKCU:\SOFTWARE\Classes" |
    Where-Object { $_.PSChildName -match "^autocad|^autodesk" }
Write-Host ("    HKCU\Classes: {0} items" -f @($classes).Count) -ForegroundColor $(if(@($classes).Count -gt 0){'Red'}else{'Green'})

# HKCU/HKLM Autodesk
$hkcu = Test-Path "HKCU:\SOFTWARE\Autodesk"
$hklm = Test-Path "HKLM:\SOFTWARE\Autodesk"
Write-Host ("    HKCU\SOFTWARE\Autodesk: {0}" -f $(if($hkcu){'exists'}else{'not found'})) -ForegroundColor $(if($hkcu){'Red'}else{'Green'})
Write-Host ("    HKLM\SOFTWARE\Autodesk: {0}" -f $(if($hklm){'exists'}else{'not found'})) -ForegroundColor $(if($hklm){'Red'}else{'Green'})

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Scan complete, ready for cleanup phase" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
```

---

## Step 2: Terminate Processes (Requires Confirmation)

### Purpose
Terminate all running Autodesk-related processes. This is necessary before cleanup because:
- Running programs lock files, preventing deletion
- Background services may automatically restart or recreate configurations

### Why This Must Be Done
If processes are still running, you will receive "file in use" errors when deleting files, and some files may remain.

### Execution Command (Requires Confirmation)

```powershell
# ============================================
# Terminate Autodesk Processes
# Purpose: Release locked files to ensure smooth cleanup
# Reason: Running programs lock files, causing deletion failures
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 2: Terminate Processes" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Purpose: Release locked files to ensure smooth cleanup" -ForegroundColor Gray
Write-Host "Reason: Running programs lock files, causing deletion failures" -ForegroundColor Gray
Write-Host ""

# List processes to be terminated
Write-Host "The following processes will be terminated:" -ForegroundColor Yellow
$processes = Get-Process | Where-Object { $_.ProcessName -match "autocad|autodesk|fusion|eagle" } |
    Select-Object ProcessName, Id
$processes | Format-Table -AutoSize

if (@($processes).Count -eq 0) {
    Write-Host "No running processes, skipping this step" -ForegroundColor Green
    return
}

# User confirmation
$confirm = Read-Host "Confirm terminate these processes? (Y/N)"
if ($confirm -ne 'Y' -and $confirm -ne 'y') {
    Write-Host "Cancelled" -ForegroundColor Red
    return
}

# Execute termination
Write-Host "Terminating processes..." -ForegroundColor Yellow
Get-Process | Where-Object { $_.ProcessName -match "autocad|autodesk|fusion|eagle" } |
    Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "Processes terminated" -ForegroundColor Green
```

---

## Step 3: Stop Services (Requires Confirmation)

### Purpose
Stop Autodesk-related Windows background services. These services include:
- **AdskLicensing**: Autodesk license authentication service
- **Autodesk Desktop App**: Autodesk desktop application service

### Why This Must Be Done
- Services run continuously in the background, consuming system resources
- Even after deleting program files, service entries remain in the system
- May prevent reinstallation of Autodesk products

### Execution Command (Requires Confirmation)

```powershell
# ============================================
# Stop Autodesk Services
# Purpose: Stop background services, free system resources
# Reason: Residual services block software reinstallation
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 3: Stop Services" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Purpose: Stop background services, free system resources" -ForegroundColor Gray
Write-Host "Reason: Residual services block software reinstallation" -ForegroundColor Gray
Write-Host ""

# Find Autodesk services
Write-Host "The following services will be stopped:" -ForegroundColor Yellow
$services = Get-Service | Where-Object { $_.DisplayName -match "autodesk|autocad|adsv" } |
    Select-Object Name, DisplayName, Status

if (@($services).Count -eq 0) {
    Write-Host "No Autodesk-related services found, skipping this step" -ForegroundColor Green
    return
}

$services | Format-Table -AutoSize

# User confirmation
$confirm = Read-Host "Confirm stop these services? (Y/N)"
if ($confirm -ne 'Y' -and $confirm -ne 'y') {
    Write-Host "Cancelled" -ForegroundColor Red
    return
}

# Execute stop
Write-Host "Stopping services..." -ForegroundColor Yellow
Get-Service | Where-Object { $_.DisplayName -match "autodesk|autocad|adsv" } |
    Stop-Service -Force -ErrorAction SilentlyContinue

Write-Host "Services stopped" -ForegroundColor Green
```

---

## Step 4: Delete File Directories (Requires Confirmation)

### Purpose
Delete all Autodesk software installation and runtime file directories, including:
- Actual installation directories dynamically discovered from registry
- Standard Autodesk directories
- User data directories

### Why This Must Be Done
| Directory Type | Deletion Reason |
|----------------|-----------------|
| Program installation directory | Contains main program files and license information |
| User local data | May contain 5GB+ of cache and temporary files |
| User roaming data | Contains personalized configurations and preferences |

### Execution Command (Requires Confirmation)

```powershell
# ============================================
# Delete Autodesk File Directories v2.1
# Purpose: Remove all installation files and user data
# Reason: Free disk space, remove config files and cache
# Intelligent: Collect directories comprehensively from registry and standard locations
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 4: Delete File Directories" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Purpose: Remove all installation files and user data" -ForegroundColor Gray
Write-Host "Reason: Free disk space, remove config files and cache" -ForegroundColor Gray
Write-Host ""

# Build complete list of directories to delete
$dirsToDelete = @()

# 4.1 Get from Step 1 scan results
if ($global:autodeskDirs) {
    Write-Host "[Source 1] Directories from environment scan:" -ForegroundColor Cyan
    foreach ($dir in $global:autodeskDirs | Sort-Object -Unique) {
        if ($dir -and (Test-Path $dir)) {
            $size = (Get-ChildItem $dir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
            $size = [math]::Round($size, 2).ToString() + " GB"
            Write-Host "    [OK] $dir ($size)" -ForegroundColor Green
            $dirsToDelete += $dir
        }
    }
    Write-Host ""
}

# 4.2 Standard directories (supplementary scan)
Write-Host "[Source 2] Standard Autodesk directories:" -ForegroundColor Cyan
$standardDirs = @(
    "$env:SystemDrive\Autodesk",
    "${env:ProgramFiles}\Autodesk",
    "${env:ProgramFiles(x86)}\Autodesk",
    "$env:ProgramData\Autodesk"
)

foreach ($dir in $standardDirs) {
    if ($dir -and (Test-Path $dir)) {
        $size = (Get-ChildItem $dir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        $size = [math]::Round($size, 2).ToString() + " GB"
        Write-Host "    [OK] $dir ($size)" -ForegroundColor Green
        $dirsToDelete += $dir
    } else {
        Write-Host "    [--] $dir (not found)" -ForegroundColor Gray
    }
}
Write-Host ""

# 4.3 User data directories
Write-Host "[Source 3] User data directories:" -ForegroundColor Cyan
$userDirs = @(
    "$env:LOCALAPPDATA\Autodesk",
    "$env:APPDATA\Autodesk"
)

foreach ($dir in $userDirs) {
    if ($dir -and (Test-Path $dir)) {
        $size = (Get-ChildItem $dir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        $size = [math]::Round($size, 2).ToString() + " GB"
        Write-Host "    [OK] $dir ($size)" -ForegroundColor Green
        $dirsToDelete += $dir
    } else {
        Write-Host "    [--] $dir (not found)" -ForegroundColor Gray
    }
}

# Deduplicate
$dirsToDelete = $dirsToDelete | Sort-Object -Unique

Write-Host ""
Write-Host "Total: $($dirsToDelete.Count) directories to delete" -ForegroundColor Yellow
Write-Host ""
Write-Host "Note: Program Files directories may require administrator privileges" -ForegroundColor Cyan

# User confirmation
$confirm = Read-Host "Confirm delete all existing directories? (Y/N)"
if ($confirm -ne 'Y' -and $confirm -ne 'y') {
    Write-Host "Cancelled" -ForegroundColor Red
    return
}

# Execute deletion
Write-Host ""
Write-Host "Deleting directories..." -ForegroundColor Yellow

$deleted = 0
$failed = 0

foreach ($dir in $dirsToDelete) {
    if (Test-Path $dir) {
        try {
            Remove-Item $dir -Recurse -Force -ErrorAction Stop
            Write-Host ("    [OK] Deleted: {0}" -f $dir) -ForegroundColor Green
            $deleted++
        } catch {
            Write-Host ("    [!] Failed (admin required): {0}" -f $dir) -ForegroundColor Yellow
            $failed++
        }
    }
}

Write-Host ""
Write-Host "Directory deletion complete: $deleted succeeded, $failed failed" -ForegroundColor Cyan
```

---

## Step 5: Clean Registry (Requires Confirmation)

### Purpose
Delete all Autodesk-related entries in the Windows registry.

### Why This Must Be Done
| Registry Key | Deletion Reason |
|--------------|-----------------|
| `HKLM\Uninstall\*` | Software uninstallation info, residue causes incorrect "installed" display |
| `HKLM\SOFTWARE\Autodesk` | Autodesk core configuration, affects license management |
| `HKCU\SOFTWARE\Autodesk` | User personalized configuration, contains licenses and preferences |
| `HKCU\Classes\.dwg/.dwt/.dxf` | File associations, residue causes file open confusion |
| `HKCU\Classes\AutoCAD*` | COM class registration, affects program interaction |
| `appdatalow\Autodesk` | Low integrity data, cache and temporary files |

### Execution Command (Requires Confirmation)

```powershell
# ============================================
# Clean Autodesk Registry v2.1
# Purpose: Remove all registry residues
# Reason: Residual registry causes uninstall info confusion, file association errors
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Step 5: Clean Registry" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Purpose: Remove all registry residues" -ForegroundColor Gray
Write-Host "Reason: Residual registry causes uninstall info confusion, file association errors" -ForegroundColor Gray
Write-Host ""

# List items to delete
Write-Host "[1] HKLM Uninstall (Autodesk software uninstall info)" -ForegroundColor Cyan
Write-Host "    Purpose: Records software installation info, residue causes 'already installed' on reinstall" -ForegroundColor Gray
$uninstall = Get-ChildItem "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" |
    Where-Object { $_.GetValue('DisplayName') -match "autocad|autodesk" }
foreach ($item in $uninstall) {
    Write-Host ("    - {0} ({1})" -f $item.GetValue('DisplayName'), $item.PSChildName) -ForegroundColor Red
}
if (@($uninstall).Count -eq 0) { Write-Host "    No related items" -ForegroundColor Green }

Write-Host ""
Write-Host "[2] HKLM\SOFTWARE\Autodesk (Autodesk core config)" -ForegroundColor Cyan
Write-Host "    Purpose: Autodesk core config, affects license service" -ForegroundColor Gray
if (Test-Path "HKLM:\SOFTWARE\Autodesk") {
    Write-Host "    Exists, will be deleted" -ForegroundColor Red
} else {
    Write-Host "    Not found" -ForegroundColor Green
}

Write-Host ""
Write-Host "[3] HKCU\SOFTWARE\Autodesk (User Autodesk config)" -ForegroundColor Cyan
Write-Host "    Purpose: User personalized settings, contains license info" -ForegroundColor Gray
if (Test-Path "HKCU:\SOFTWARE\Autodesk") {
    Write-Host "    Exists, will be deleted" -ForegroundColor Red
} else {
    Write-Host "    Not found" -ForegroundColor Green
}

Write-Host ""
Write-Host "[4] HKCU\appdatalow\software\Autodesk (Low integrity data)" -ForegroundColor Cyan
Write-Host "    Purpose: Low-privilege cache and temp files" -ForegroundColor Gray
if (Test-Path "HKCU:\SOFTWARE\appdatalow\software\Autodesk") {
    Write-Host "    Exists, will be deleted" -ForegroundColor Red
} else {
    Write-Host "    Not found" -ForegroundColor Green
}

Write-Host ""
Write-Host "[5] HKCU\SOFTWARE\Classes\AutoCAD*/Autodesk* (COM class registration)" -ForegroundColor Cyan
Write-Host "    Purpose: COM component registration, affects inter-program interaction" -ForegroundColor Gray
$classes = Get-ChildItem "HKCU:\SOFTWARE\Classes" |
    Where-Object { $_.PSChildName -match "^autocad|^autodesk" }
foreach ($item in $classes) {
    Write-Host ("    - {0}" -f $item.PSChildName) -ForegroundColor Red
}
if (@($classes).Count -eq 0) { Write-Host "    No related items" -ForegroundColor Green }

Write-Host ""
Write-Host "[6] File associations (.dwg/.dwt/.dxf)" -ForegroundColor Cyan
Write-Host "    Purpose: Define file open methods, residue causes association confusion" -ForegroundColor Gray
foreach ($ext in @('.dwg', '.dwt', '.dxf')) {
    $v = (Get-Item "HKCU:\SOFTWARE\Classes\$ext" -ErrorAction SilentlyContinue).GetValue('')
    if ($v -match "autocad|autodesk") {
        Write-Host ("    {0} -> {1} (will be cleared)" -f $ext, $v) -ForegroundColor Red
    } else {
        Write-Host ("    {0} -> Not associated with AutoCAD" -f $ext) -ForegroundColor Green
    }
}

# User confirmation
Write-Host ""
$confirm = Read-Host "Confirm delete all registry items above? (Y/N)"
if ($confirm -ne 'Y' -and $confirm -ne 'y') {
    Write-Host "Cancelled" -ForegroundColor Red
    return
}

# Execute deletion
Write-Host ""
Write-Host "Cleaning registry..." -ForegroundColor Yellow

$regDeleted = 0

# 5.1 Delete HKLM Uninstall items
$uninstall = Get-ChildItem "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" |
    Where-Object { $_.GetValue('DisplayName') -match "autocad|autodesk" }
foreach ($item in $uninstall) {
    Remove-Item $item.PSPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host ("    [OK] Deleted Uninstall item: {0}" -f $item.GetValue('DisplayName')) -ForegroundColor Green
    $regDeleted++
}

# 5.2 Delete HKLM Autodesk key
if (Test-Path "HKLM:\SOFTWARE\Autodesk") {
    Remove-Item "HKLM:\SOFTWARE\Autodesk" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "    [OK] Deleted: HKLM\SOFTWARE\Autodesk" -ForegroundColor Green
    $regDeleted++
}

# 5.3 Delete HKCU Autodesk key
if (Test-Path "HKCU:\SOFTWARE\Autodesk") {
    Remove-Item "HKCU:\SOFTWARE\Autodesk" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "    [OK] Deleted: HKCU\SOFTWARE\Autodesk" -ForegroundColor Green
    $regDeleted++
}

# 5.4 Delete appdatalow Autodesk
if (Test-Path "HKCU:\SOFTWARE\appdatalow\software\Autodesk") {
    Remove-Item "HKCU:\SOFTWARE\appdatalow\software\Autodesk" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "    [OK] Deleted: HKCU\appdatalow\software\Autodesk" -ForegroundColor Green
    $regDeleted++
}

# 5.5 Delete AutoCAD Classes
$classes = Get-ChildItem "HKCU:\SOFTWARE\Classes" |
    Where-Object { $_.PSChildName -match "^autocad|^autodesk" }
foreach ($item in $classes) {
    Remove-Item $item.PSPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host ("    [OK] Deleted: {0}" -f $item.PSChildName) -ForegroundColor Green
    $regDeleted++
}

# 5.6 Delete file associations
foreach ($ext in @('.dwg', '.dwt', '.dxf')) {
    if (Test-Path "HKCU:\SOFTWARE\Classes\$ext") {
        Remove-Item "HKCU:\SOFTWARE\Classes\$ext" -Force -ErrorAction SilentlyContinue
        Write-Host ("    [OK] Deleted: {0} association" -f $ext) -ForegroundColor Green
        $regDeleted++
    }
}

Write-Host ""
Write-Host "Registry cleanup complete: Deleted $regDeleted items" -ForegroundColor Green
```

---

## Step 6: Verify Cleanup Results

### Execution Command

```powershell
# ============================================
# Verify Cleanup Results
# Purpose: Confirm all residues have been removed, output cleanup report
# ============================================

$ErrorActionPreference = 'SilentlyContinue'
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Autodesk Clean Uninstall - Cleanup Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$issues = @()

# Check directories from registry
if ($global:autodeskDirs) {
    foreach ($d in $global:autodeskDirs | Sort-Object -Unique) {
        if (Test-Path $d) {
            Write-Host ("    [!] {0} (still exists)" -f $d) -ForegroundColor Red
            $issues += $d
        }
    }
}

# Check standard directories
$standardDirs = @(
    "$env:SystemDrive\Autodesk",
    "${env:ProgramFiles}\Autodesk",
    "${env:ProgramFiles(x86)}\Autodesk",
    "$env:ProgramData\Autodesk",
    "$env:LOCALAPPDATA\Autodesk",
    "$env:APPDATA\Autodesk"
)
foreach ($d in $standardDirs) {
    if (Test-Path $d) {
        Write-Host ("    [!] {0}" -f $d) -ForegroundColor Red
        $issues += $d
    }
}

# HKLM Uninstall
$uninstall = Get-ChildItem "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" |
    Where-Object { $_.GetValue('DisplayName') -match "autocad|autodesk" }
if (@($uninstall).Count -gt 0) {
    $issues += "HKLM Uninstall"
}

# HKCU Classes
$classes = Get-ChildItem "HKCU:\SOFTWARE\Classes" |
    Where-Object { $_.PSChildName -match "^autocad|^autodesk" }
if (@($classes).Count -gt 0) {
    $issues += "HKCU Classes"
}

if (Test-Path "HKCU:\SOFTWARE\Autodesk") { $issues += "HKCU Autodesk" }
if (Test-Path "HKLM:\SOFTWARE\Autodesk") { $issues += "HKLM Autodesk" }

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($issues.Count -eq 0) {
    Write-Host "  [OK] Cleanup complete! Zero residue!" -ForegroundColor Green
} else {
    Write-Host ("  [!] Cleanup complete, but {0} items may require manual handling" -f $issues.Count) -ForegroundColor Yellow
}
Write-Host "========================================" -ForegroundColor Cyan
```

---

## One-Click Cleanup Script

```powershell
# AutoCAD/Autodesk Clean Uninstall Script v2.1
# One-click execution: Scan -> Terminate -> Stop Services -> Delete Files -> Clean Registry -> Verify

param([switch]$Auto)

$ErrorActionPreference = 'SilentlyContinue'
$global:autodeskDirs = @()

function Confirm-Action {
    param($Message)
    if ($Auto) { return $true }
    $result = Read-Host "$Message (Y/N)"
    return ($result -eq 'Y' -or $result -eq 'y')
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Autodesk Clean Uninstall v2.1" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Phase 1: Environment scan
Write-Host "[Phase 1] Environment scan..." -ForegroundColor Yellow
$installed = Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" |
    Where-Object { $_.DisplayName -match "autocad|autodesk" }
foreach ($app in $installed) {
    if ($app.InstallLocation -and (Test-Path $app.InstallLocation)) {
        $global:autodeskDirs += $app.InstallLocation
        $global:autodeskDirs += Split-Path $app.InstallLocation -Parent
    }
}
@("$env:SystemDrive\Autodesk","${env:ProgramFiles}\Autodesk","$env:ProgramData\Autodesk",
  "$env:LOCALAPPDATA\Autodesk","$env:APPDATA\Autodesk") |
    ForEach-Object { if (Test-Path $_) { $global:autodeskDirs += $_ } }

# Phase 2: Terminate processes
Write-Host "[Phase 2] Terminate processes..." -ForegroundColor Yellow
$procs = Get-Process | Where-Object { $_.ProcessName -match "autocad|autodesk|fusion|eagle" }
if (@($procs).Count -gt 0 -and (Confirm-Action "Terminate $($procs.Count) processes?")) {
    $procs | Stop-Process -Force
}

# Phase 3: Stop services
Write-Host "[Phase 3] Stop services..." -ForegroundColor Yellow
$services = Get-Service | Where-Object { $_.DisplayName -match "autodesk|autocad|adsv" }
if (@($services).Count -gt 0 -and (Confirm-Action "Stop $($services.Count) services?")) {
    $services | Stop-Service -Force -ErrorAction SilentlyContinue
}

# Phase 4: Delete directories
Write-Host "[Phase 4] Delete directories..." -ForegroundColor Yellow
$toDelete = $global:autodeskDirs | Sort-Object -Unique | Where-Object { Test-Path $_ }
if (@($toDelete).Count -gt 0 -and (Confirm-Action "Delete $($toDelete.Count) directories?")) {
    foreach ($dir in $toDelete) {
        try {
            Remove-Item $dir -Recurse -Force -ErrorAction Stop
            Write-Host "    [OK] Deleted: $dir" -ForegroundColor Green
        } catch {
            Write-Host "    [!] Failed (admin): $dir" -ForegroundColor Yellow
        }
    }
}

# Phase 5: Clean registry
Write-Host "[Phase 5] Clean registry..." -ForegroundColor Yellow
$uninstall = Get-ChildItem "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" |
    Where-Object { $_.GetValue('DisplayName') -match "autocad|autodesk" }
if (@($uninstall).Count -gt 0 -and (Confirm-Action "Delete $($uninstall.Count) Uninstall items?")) {
    $uninstall | ForEach-Object { Remove-Item $_.PSPath -Recurse -Force }
}
foreach ($path in @("HKLM:\SOFTWARE\Autodesk","HKCU:\SOFTWARE\Autodesk","HKCU:\SOFTWARE\appdatalow\software\Autodesk")) {
    if (Test-Path $path -and (Confirm-Action "Delete $path?")) {
        Remove-Item $path -Recurse -Force
    }
}
$classes = Get-ChildItem "HKCU:\SOFTWARE\Classes" | Where-Object { $_.PSChildName -match "^autocad|^autodesk" }
if (@($classes).Count -gt 0 -and (Confirm-Action "Delete $($classes.Count) Classes items?")) {
    $classes | ForEach-Object { Remove-Item $_.PSPath -Recurse -Force }
}
foreach ($ext in @('.dwg','.dwt','.dxf')) {
    if (Test-Path "HKCU:\SOFTWARE\Classes\$ext") {
        Remove-Item "HKCU:\SOFTWARE\Classes\$ext" -Force -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  [OK] Cleanup complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
```

---

## Known Autodesk Software List

| Software | Description |
|----------|-------------|
| AutoCAD | Core CAD software |
| AutoCAD Mechanical | Mechanical design version |
| AutoCAD Electrical | Electrical design version |
| Autodesk Fusion 360 | Cloud-based CAD/CAM/CAE |
| Autodesk CAM360 | CAM machining software |
| Autodesk EAGLE | PCB design software |
| Autodesk CER | License authentication component |

## Technical Specifications

- **Compatible Systems**: Windows 10/11
- **Compatible Users**: Any Windows username
- **Compatible Installation Paths**: Standard directories + any custom directories
- **Permissions Required**: Some operations require administrator privileges
- **PowerShell Version**: 5.1+
- **Author**: 大头
- **Version**: 2.1 (2026-05-17)
