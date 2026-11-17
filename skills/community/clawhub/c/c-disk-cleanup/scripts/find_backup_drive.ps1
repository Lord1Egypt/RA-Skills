# find_backup_drive.ps1 - 自动找非 C 盘的备份盘（不写死 D 盘）
# 用法: powershell -ExecutionPolicy Bypass -File find_backup_drive.ps1
# 输出可用磁盘列表，供助手向用户展示并让用户选择；找不到则提示用回收站兜底。

function FmtGB($bytes){
    if($bytes -eq $null){return "?"}
    $gb = $bytes/1GB
    if($gb -ge 1){return ("{0:N2} GB" -f $gb)}
    return ("{0:N0} MB" -f ($bytes/1MB))
}

Write-Host "=== 找一个放备份文件的盘 ===" -ForegroundColor Cyan
$drives = Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Name -ne 'C' -and $_.Free -gt 0 }
if($drives.Count -eq 0){
    Write-Host "没找到其他磁盘。兜底方案：把文件先送回收站（可恢复），" -ForegroundColor Yellow
    Write-Host "但注意：回收站在 C 盘上，不释放 C 盘空间，需你之后手动清空回收站。" -ForegroundColor Yellow
    exit 0
}
Write-Host "发现以下可用磁盘（请挑一个空间最够的）：" -ForegroundColor Green
$i=1
foreach($d in $drives){
    $total = $d.Used + $d.Free
    Write-Host ("  [{0}] {1}:  剩余 {2} / 共 {3}" -f $i, $d.Name, (FmtGB $d.Free), (FmtGB $total))
    $i++
}
Write-Host ""
Write-Host "建议助手：把上面列表念给用户听，让用户说用哪个盘（如用 D 盘）。" -ForegroundColor White
Write-Host "确定后，备份目录统一用 盘符:\C盘整理\备份_日期 ，文件都在那里，随时可找回。" -ForegroundColor White
