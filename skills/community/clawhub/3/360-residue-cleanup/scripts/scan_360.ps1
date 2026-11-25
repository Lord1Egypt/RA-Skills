<#
.SYNOPSIS
    360 残留只读扫描器 —— 扫出 C 盘常见位置的 360 痕迹，输出结构化清单。
.DESCRIPTION
    全程只读：不删任何文件、不停任何进程、不改注册表。
    输出 JSON（默认写到 $OutFile），供主流程据此生成清单、请求用户确认。
    每个命中项带 category / path / size / rationale，并标注是否需提权。

.PARAMETER OutFile
    JSON 输出路径。默认写到当前目录下的 scan-result.json。

.PARAMETER FullDisk
    加此开关则额外扫描所有本地磁盘（耗时较长）。默认只扫 C 盘常见位置。

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scan_360.ps1 -OutFile .\scan-result.json
#>
param(
    [string]$OutFile = ".\scan-result.json",
    [switch]$FullDisk
)

$ErrorActionPreference = 'SilentlyContinue'

function Get-DirSizeMB {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return 0 }
    $sum = (Get-ChildItem -LiteralPath $Path -Recurse -File -Force -ErrorAction SilentlyContinue |
            Measure-Object Length -Sum).Sum
    return [math]::Round($sum / 1MB, 2)
}

$findings = New-Object System.Collections.ArrayList

function Add-Finding {
    param(
        [string]$Category, [string]$Path, [string]$Kind,
        [double]$SizeMB, [string]$Rationale, [bool]$NeedsAdmin = $false,
        [string]$Confidence = 'confirmed'
    )
    [void]$findings.Add([pscustomobject]@{
        category     = $Category
        path         = $Path
        kind         = $Kind          # directory | file | registry | service | task | driver
        size_mb      = $SizeMB
        exists       = (Test-Path -LiteralPath $Path)
        needs_admin  = $NeedsAdmin
        confidence   = $Confidence    # confirmed | suspicious | false-positive
        rationale    = $Rationale
    })
}

# ============ 1. 目录 / 文件（C 盘常见位置）============
$dirRoots = @(
    'C:\Program Files',
    'C:\Program Files (x86)',
    'C:\ProgramData',
    "$env:APPDATA",
    "$env:LOCALAPPDATA"
)
$namePattern = '360|qihoo|qihu|kxescore|zhudongfangyu|kxe'
foreach ($root in $dirRoots) {
    if (-not (Test-Path -LiteralPath $root)) { continue }
    Get-ChildItem -LiteralPath $root -Directory -ErrorAction SilentlyContinue |
      Where-Object { $_.Name -match $namePattern } |
      ForEach-Object {
          $needsAdmin = $_.FullName -match 'Program Files|ProgramData|Windows'
          Add-Finding -Category 'directory' -Path $_.FullName -Kind 'directory' `
              -SizeMB (Get-DirSizeMB $_.FullName) `
              -Rationale '360 相关目录（按名称匹配）' -NeedsAdmin $needsAdmin
      }
}

# secoresdk 是特殊容器：名字不含 360，但里面是 360 浏览器数据
$secore = Join-Path $env:APPDATA 'secoresdk'
if (Test-Path -LiteralPath $secore) {
    Get-ChildItem -LiteralPath $secore -Directory -ErrorAction SilentlyContinue |
      Where-Object { $_.Name -match '360|se6' } |
      ForEach-Object {
          Add-Finding -Category 'browser-data' -Path $_.FullName -Kind 'directory' `
              -SizeMB (Get-DirSizeMB $_.FullName) `
              -Rationale '360 浏览器数据（藏在 secoresdk 容器内，名称不含 360）' `
              -Confidence 'confirmed'
      }
}

# 驱动残骸（System32\drivers）—— 被改成非法后缀失效的 360 驱动
Get-ChildItem 'C:\Windows\System32\drivers' -File -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match '^360' } |
  ForEach-Object {
      $active = $_.Extension -eq '.sys'
      Add-Finding -Category 'driver' -Path $_.FullName -Kind 'driver' `
          -SizeMB ([math]::Round($_.Length/1MB,2)) `
          -Rationale ("360 驱动文件（{0}）" -f $(if($active){'仍为 .sys，需谨慎'}else{'后缀已改，已失效'})) `
          -NeedsAdmin $true
  }

# 临时目录里的 360 清理脚本
Get-ChildItem "$env:TEMP" -File -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match '360|remove' } |
  ForEach-Object {
      Add-Finding -Category 'temp' -Path $_.FullName -Kind 'file' `
          -SizeMB ([math]::Round($_.Length/1MB,2)) `
          -Rationale '临时目录中的 360 相关脚本/文件' -Confidence 'suspicious'
  }

# ============ 2. 注册表（只读查询，不用 reg.exe）============
$regKeys = @(
    'HKLM\SOFTWARE\WOW6432Node\360DrvMgr',
    'HKLM\SOFTWARE\WOW6432Node\360Safe',
    'HKCU\SOFTWARE\360X', 'HKCU\SOFTWARE\360ChromeXX', 'HKCU\SOFTWARE\360CleanProX',
    'HKCU\SOFTWARE\360DayPop', 'HKCU\SOFTWARE\360Game5', 'HKCU\SOFTWARE\360Newsld',
    'HKCU\SOFTWARE\360se6', 'HKCU\SOFTWARE\360SoftWareMgr', 'HKCU\SOFTWARE\360WallPaper'
)
foreach ($k in $regKeys) {
    $exists = Test-Path "Registry::$k"
    [void]$findings.Add([pscustomobject]@{
        category='registry'; path=$k; kind='registry'; size_mb=0; exists=$exists
        needs_admin=$true; confidence='confirmed'; rationale='360 注册表键'
    })
}

# ============ 3. 服务 ============
foreach ($svc in @('Q360AMPPL','ZhuDongFangYu','360Box64','360netmon')) {
    $s = Get-CimInstance Win32_Service -Filter "Name='$svc'" -ErrorAction SilentlyContinue
    [void]$findings.Add([pscustomobject]@{
        category='service'; path=$svc; kind='service'; size_mb=0
        exists=[bool]$s; needs_admin=$true; confidence='confirmed'
        rationale=$(if($s){"服务存在（状态=$($s.State), 启动=$($s.StartMode)）"}else{'服务项不存在'})
    })
}

# ============ 4. 卸载登记（用于三态判定）============
$uninstallEntries = @(Get-ItemProperty `
    HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*,`
    HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*,`
    HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\* -ErrorAction SilentlyContinue |
    Where-Object { $_.DisplayName -match '360|奇虎|Wukong|悟空' })

# ============ 5. 误报排除提示 ============
$falsePositives = @()
Get-ChildItem "$env:LOCALAPPDATA\GitHub CLI" -File -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -match '360' } |
  ForEach-Object { $falsePositives += $_.FullName }

# ============ 三态判定 ============
$activeFiles = @($findings | Where-Object { $_.kind -eq 'directory' -and $_.exists -and $_.category -eq 'directory' })
if ($uninstallEntries.Count -gt 0) {
    $state = 'active'   # 有卸载登记 —— 应走官方卸载
} elseif ($findings.Count -gt 0) {
    $state = 'residue'  # 无登记但有残留 —— 直接文件级清理
} else {
    $state = 'clean'
}

$result = [pscustomobject]@{
    scan_time        = (Get-Date).ToString('o')
    state            = $state
    state_rationale  = $(switch($state){
        'active'  { '注册表存在 360 卸载登记，应优先走官方卸载程序' }
        'residue' { '无卸载登记但有残留，直接文件级清理（不要拉起 uninst.exe）' }
        'clean'   { '未发现 360 痕迹' }
    })
    uninstall_entries = @($uninstallEntries | ForEach-Object { $_.DisplayName })
    findings         = @($findings)
    false_positives  = @($falsePositives)
    total_size_mb    = [math]::Round((($findings | Measure-Object size_mb -Sum).Sum), 2)
    needs_admin_count= @($findings | Where-Object { $_.needs_admin -and $_.exists }).Count
}

$json = $result | ConvertTo-Json -Depth 6
$json | Set-Content -LiteralPath $OutFile -Encoding UTF8
Write-Host "扫描完成：状态=$state，命中 $($findings.Count) 项，共 $($result.total_size_mb) MB，需提权 $($result.needs_admin_count) 项"
Write-Host "结果已写入：$OutFile"
