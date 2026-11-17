# scan_cdrive.ps1 - C 盘只读体检（不修改任何文件）
# 用法: powershell -ExecutionPolicy Bypass -File scan_cdrive.ps1
# 输出一份给小白看的体检报告：C盘空间 + 占空间大户 + 可清理候选菜单

function FmtGB($bytes){
    if($bytes -eq $null){return "?"}
    $gb = $bytes/1GB
    if($gb -ge 1){return ("{0:N2} GB" -f $gb)}
    return ("{0:N0} MB" -f ($bytes/1MB))
}

$ErrorActionPreference = 'SilentlyContinue'
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "        C 盘只读体检报告（未改动任何文件）" -ForegroundColor Cyan
Write-Host ("        时间: {0:yyyy-MM-dd HH:mm}" -f (Get-Date)) -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# 1) C 盘总空间
$c = Get-PSDrive C -ErrorAction SilentlyContinue
if($c){
    $used = $c.Used; $free = $c.Free; $total = $used+$free
    $pct = if($total -gt 0){[math]::Round($used/$total*100)}else{0}
    Write-Host ""
    Write-Host "[1/4] C 盘总容量" -ForegroundColor Yellow
    Write-Host ("    共 {0} ，已用 {1}（{2}%），剩余 {3}" -f (FmtGB $total),(FmtGB $used),($pct+""),(FmtGB $free))
    if($pct -ge 90){ Write-Host "    >> 已爆红！建议尽快清理。" -ForegroundColor Red }
    elseif($pct -ge 75){ Write-Host "    >> 比较紧张，可以理一理。" -ForegroundColor Yellow }
    else { Write-Host "    >> 还比较宽裕。" -ForegroundColor Green }
}

# 2) 顶层目录大户
Write-Host ""
Write-Host "[2/4] C 盘顶层占空间大户 Top10" -ForegroundColor Yellow
$top = Get-ChildItem "C:\" -Directory | ForEach-Object {
    $sz = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    [pscustomobject]@{Name=$_.Name; Size=$sz}
} | Sort-Object Size -Descending | Select-Object -First 10
$top | ForEach-Object { Write-Host ("    {0,-28} {1}" -f $_.Name,(FmtGB $_.Size)) }

# 3) 用户目录大户
$user = $env:USERPROFILE
Write-Host ""
Write-Host "[3/4] 你的用户目录大户 Top10" -ForegroundColor Yellow
$uTop = Get-ChildItem $user -Directory | Where-Object {$_.Name -ne 'AppData'} | ForEach-Object {
    $sz = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    [pscustomobject]@{Name=$_.Name; Size=$sz}
} | Sort-Object Size -Descending | Select-Object -First 10
$uTop | ForEach-Object { Write-Host ("    {0,-28} {1}" -f $_.Name,(FmtGB $_.Size)) }

# 4) 常见可清理候选（只读统计，不动）
Write-Host ""
Write-Host "[4/4] 常见可清理候选（仅统计，未清理）" -ForegroundColor Yellow
Write-Host "  —— 可重建的安全项（可放心搬） ——" -ForegroundColor Green
$cands = @(
    @{Label="系统临时文件 Windows\Temp"; Path="C:\Windows\Temp"},
    @{Label="用户临时文件 TEMP"; Path=$env:TEMP},
    @{Label=" Windows 更新缓存 Download"; Path="C:\Windows\SoftwareDistribution\Download"}
)
foreach($c in $cands){
    if(Test-Path $c.Path){
        $sz = (Get-ChildItem $c.Path -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        Write-Host ("    {0,-46} {1}" -f $c.Label,(FmtGB $sz))
    }
}
Write-Host ""
Write-Host "  —— 应用缓存：只搬 Cache/Temp 子目录，绝不整体搬 AppData ——" -ForegroundColor Cyan
Write-Host "    缓存分散在各软件目录下的 Cache/Temp 子目录，建议逐项确认后搬对应子目录。" -ForegroundColor White
Write-Host "    切勿把整个 AppData\Local 当成一个整体搬走（会搬走软件主程序导致打不开）。" -ForegroundColor White

# IM / 聊天数据：提示走官方迁移，不要手动搬
Write-Host ""
Write-Host "  —— 聊天软件数据（请用软件内『更改存储位置』迁移，不要手动搬） ——" -ForegroundColor Magenta
$imPaths = @(
    @{Label="微信(4.x) xwechat_files"; Path="$user\Documents\xwechat_files"},
    @{Label="微信(3.x) WeChat Files"; Path="$user\Documents\WeChat Files"},
    @{Label="QQ"; Path="$user\Documents\Tencent Files"},
    @{Label="企业微信"; Path="$user\Documents\WXWork"}
)
foreach($c in $imPaths){
    if(Test-Path $c.Path){
        $sz = (Get-ChildItem $c.Path -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        Write-Host ("    {0,-46} {1}" -f $c.Label,(FmtGB $sz))
    }
}

$hiber = if(Test-Path C:\hiberfil.sys){(Get-Item C:\hiberfil.sys).Length}else{0}
$page = if(Test-Path C:\pagefile.sys){(Get-Item C:\pagefile.sys).Length}else{0}
Write-Host ("    休眠文件 hiberfil.sys                       {0} (关闭休眠可释放，需你确认)" -f (FmtGB $hiber))
Write-Host ("    虚拟内存 pagefile.sys                      {0} (系统需要，一般不动)" -f (FmtGB $page))

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "  下一步：我会把上面这些整理成清理菜单，" -ForegroundColor White
Write-Host "  用大白话告诉你每项是什么、清了能省多少、有没有风险，" -ForegroundColor White
Write-Host "  你点头我才会动手。任何不清楚的都可以先问我。" -ForegroundColor White
Write-Host "==============================================" -ForegroundColor Cyan
