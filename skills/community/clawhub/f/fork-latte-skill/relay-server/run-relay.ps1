# ForkLatte relay-server 保活启动器
# 由 OpenClaw exec 用 Start-Process 拉起（脱离交互），内部循环保证 node 崩溃后自动重启。
# 注意：本机用户目录含中文（C:\Users\聿），不能把路径写死在 .ps1 里（PowerShell 5.1 按 GBK 读会乱码）。
# 目录用脚本自身位置推导；node 路径用环境变量 RELAY_NODE 传入。
$ErrorActionPreference = 'Continue'
$dir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $dir

$node = $env:RELAY_NODE
if (-not $node -or -not (Test-Path $node)) {
    try {
        $n = Get-Command node -ErrorAction Stop
        if (Test-Path $n.Source) { $node = $n.Source }
    } catch {}
}
if (-not $node) { $node = 'node' }

while ($true) {
    try {
        Write-Output "$(Get-Date) [relay] starting $node --env-file=.env server.js"
        $proc = Start-Process -FilePath $node -ArgumentList '--env-file=.env server.js' -WindowStyle Hidden -WorkingDirectory $dir -PassThru -RedirectStandardOutput "$dir\node.out" -RedirectStandardError "$dir\node.err"
        $proc.WaitForExit()
        Write-Output "$(Get-Date) [relay] exited code $($proc.ExitCode)"
    } catch {
        Write-Output "$(Get-Date) [relay] error: $_"
    }
    Start-Sleep -Seconds 3
}
