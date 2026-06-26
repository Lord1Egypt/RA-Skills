# scan-usage.ps1 — 扫描 AppData 缓存占用，推荐可迁移目录
# 用法: powershell -File scan-usage.ps1 [-MinSizeMB 50] [-TopN 30]
#
# 参数:
#   -MinSizeMB   : 显示的最小目录大小（MB），默认 20
#   -TopN        : 最多显示多少条，默认 30

param(
    [int]$MinSizeMB = 20,
    [int]$TopN = 30
)

Write-Host "=== AppData 缓存占用扫描 ===" -ForegroundColor Cyan
Write-Host "阈值: >= $MinSizeMB MB  |  最多显示: $TopN 条"
Write-Host ""

# 已知可安全迁移的目录关键字（仅作标记，不自动操作）
$KnownMigratable = @(
    "Cache","CachedData","GPUCache","Code Cache","CachedExtension",
    "npm-cache","yarn","pnpm","pip","gradle","maven",".m2",".gradle",
    "JetBrains","IntelliJIdea","PyCharm","WebStorm","CLion","Rider","DataGrip","GoLand","RustRover",
    "Docker","Cursor","electron","Electron",
    "node_modules","ChromiumBased","CefSharp"
)

function Get-DirSizeMB([string]$Path) {
    $s = (Get-ChildItem $Path -Recurse -Force -ErrorAction SilentlyContinue |
          Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    if ($null -eq $s) { return 0 }
    return [math]::Round($s / 1MB, 1)
}

function Is-JunctionPoint([string]$Path) {
    $item = Get-Item $Path -Force -ErrorAction SilentlyContinue
    return ($item -and ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint))
}

function Is-Migratable([string]$Name) {
    foreach ($kw in $KnownMigratable) {
        if ($Name -like "*$kw*") { return $true }
    }
    return $false
}

$results = [System.Collections.Generic.List[PSCustomObject]]::new()

# 扫描根目录列表
$scanRoots = @(
    @{ Label="APPDATA (Roaming)"; Path=$env:APPDATA },
    @{ Label="LOCALAPPDATA (Local)"; Path=$env:LOCALAPPDATA },
    @{ Label="USERPROFILE (用户根)"; Path=$env:USERPROFILE },
    @{ Label="USERPROFILE/.cache"; Path="$env:USERPROFILE\.cache" },
    @{ Label="USERPROFILE/.gradle"; Path="$env:USERPROFILE\.gradle" },
    @{ Label="USERPROFILE/.m2"; Path="$env:USERPROFILE\.m2" },
    @{ Label="USERPROFILE/.nuget"; Path="$env:USERPROFILE\.nuget" },
    @{ Label="USERPROFILE/.pip"; Path="$env:USERPROFILE\.pip" },
    @{ Label="USERPROFILE/.cargo"; Path="$env:USERPROFILE\.cargo" }
)

foreach ($root in $scanRoots) {
    if (-not (Test-Path $root.Path)) { continue }

    # 只扫一层子目录（避免递归耗时过长）
    Get-ChildItem $root.Path -Directory -Force -ErrorAction SilentlyContinue |
    ForEach-Object {
        $dir = $_
        $sizeMB = Get-DirSizeMB $dir.FullName
        if ($sizeMB -lt $MinSizeMB) { return }

        $isJunction = Is-JunctionPoint $dir.FullName
        $migratable = Is-Migratable $dir.Name

        $results.Add([PSCustomObject]@{
            SizeMB    = $sizeMB
            Name      = $dir.Name
            FullPath  = $dir.FullName
            IsJunction= if ($isJunction) { "已迁移" } else { "" }
            Hint      = if ($isJunction) { "—" } elseif ($migratable) { "可迁移" } else { "?" }
        })
    }
}

# 排序并输出
$sorted = $results | Sort-Object SizeMB -Descending | Select-Object -First $TopN

Write-Host ("  {0,-8}  {1,-12}  {2}" -f "大小(MB)", "状态", "路径") -ForegroundColor White
Write-Host ("  " + "-"*80)

foreach ($r in $sorted) {
    $color = switch ($r.Hint) {
        "可迁移" { "Yellow" }
        "已迁移" { "Green"  }
        default  { "Gray"   }
    }
    $tag = if ($r.IsJunction) { "[已迁移]" } elseif ($r.Hint -eq "可迁移") { "[推荐迁移]" } else { "        " }
    Write-Host ("  {0,8:N1}  {1,-12}  {2}  {3}" -f $r.SizeMB, $tag, $r.FullPath, "") -ForegroundColor $color
}

Write-Host ""
Write-Host "--- 摘要 ---" -ForegroundColor Cyan
$total = ($sorted | Measure-Object -Property SizeMB -Sum).Sum
$migrated = ($sorted | Where-Object IsJunction -eq "已迁移" | Measure-Object -Property SizeMB -Sum).Sum
$recommended = ($sorted | Where-Object Hint -eq "可迁移" | Where-Object IsJunction -eq "" | Measure-Object -Property SizeMB -Sum).Sum

Write-Host ("  扫描总大小:   {0:N1} MB ({1:N2} GB)" -f $total, ($total/1024))
Write-Host ("  已迁移:       {0:N1} MB" -f $migrated) -ForegroundColor Green
Write-Host ("  推荐可迁移:   {0:N1} MB ({1:N2} GB)" -f $recommended, ($recommended/1024)) -ForegroundColor Yellow
Write-Host ""
Write-Host "提示: 对 [推荐迁移] 目录执行迁移，可使用 migrate-any.ps1：" -ForegroundColor White
Write-Host "  powershell -File migrate-any.ps1 -SourcePath '<路径>' -DstPath '<目标路径>'" -ForegroundColor DarkCyan
