# 仅结束钉钉自动回复监控的 python 进程（按脚本路径精确匹配，不动其它 python）
$proc = Get-CimInstance Win32_Process -Filter "Name='python.exe' AND CommandLine LIKE '%dingtalk_unread_monitor.py%'"
if ($proc) {
    $proc | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
    Write-Host "已结束 $($proc.Count) 个监控进程"
} else {
    Write-Host "未发现运行中的监控进程（可能未启动）"
}
