#Requires -Version 7.0
<#
.SYNOPSIS
    通用静态构建产物远程部署：打包 -> SCP -> 远程原子替换。

.EXAMPLE
    ./deploy-dist.ps1 -Source .\dist -Server root@192.0.2.10 -Target /var/www/app/dist

.EXAMPLE
    ./deploy-dist.ps1 -Source .\dist -Server deploy@host -Port 2222 -Key ~/.ssh/id_ed25519 `
        -Target /opt/app/dist -Owner www-data:www-data -PostCommand "systemctl reload nginx"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Source,
    [Parameter(Mandatory)][string]$Server,
    [Parameter(Mandatory)][string]$Target,
    [int]$Port = 22,
    [string]$Key,
    [string]$Owner,
    [switch]$Fresh,
    [int]$KeepBackups = 3,
    [string]$PostCommand,
    [switch]$DryRun,
    # 仅调试：把远端 sh 脚本导出到指定路径后退出（便于无服务器时本地验证）
    [string]$DumpScriptPath
)

$ErrorActionPreference = 'Stop'

function Fail($msg) { Write-Host "[ERROR] $msg" -ForegroundColor Red; exit 1 }
function Step($msg) { Write-Host "[deploy] $msg" -ForegroundColor Cyan }

# 单引号包裹一个值，供远端 sh 解析
function Quote-Sh([string]$s) {
    if ($null -eq $s) { return "''" }
    return "'" + ($s -replace "'", "'\''") + "'"
}

foreach ($cmd in 'ssh', 'scp', 'tar') {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) { Fail "缺少命令: $cmd" }
}

$srcFull = (Resolve-Path -LiteralPath $Source -ErrorAction SilentlyContinue)
if (-not $srcFull) { Fail "Source 不存在: $Source" }
if (-not (Test-Path -LiteralPath $srcFull -PathType Container)) { Fail "Source 不是目录: $srcFull" }
$srcFull = $srcFull.Path.TrimEnd('\', '/')

if (-not $Target.StartsWith('/')) { Fail "Target 必须是远程绝对路径: $Target" }

$id = [guid]::NewGuid().ToString('N').Substring(0, 8)
$localArchive = Join-Path ([System.IO.Path]::GetTempPath()) "dist-deploy-$id.tgz"
$remoteArchive = "/tmp/dist-deploy-$id.tgz"
$remoteScript = "/tmp/dist-deploy-$id.sh"
$localScript = Join-Path ([System.IO.Path]::GetTempPath()) "dist-deploy-$id.sh"

$sshBase = @('-p', "$Port")
$scpBase = @('-P', "$Port")
if ($Key) {
    $keyPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Key)
    if (-not (Test-Path -LiteralPath $keyPath)) { Fail "私钥不存在: $keyPath" }
    $sshBase += @('-i', $keyPath)
    $scpBase += @('-i', $keyPath)
}

$mode = if ($Fresh) { 'fresh' } else { 'backup' }

# 远端执行脚本（参数: archive target keep mode owner postcmd）
$remoteCode = @'
#!/bin/sh
set -eu
ARCHIVE="$1"; TGT="$2"; KEEP="$3"; MODE="$4"; OWNER="$5"; POSTCMD="${6:-}"
PARENT=$(dirname "$TGT")
NEW="$PARENT/.deploy-tmp-$$"
trap 'rm -rf "$NEW"' EXIT

mkdir -p "$PARENT"
rm -rf "$NEW"
mkdir -p "$NEW"
tar -xzf "$ARCHIVE" -C "$NEW"
[ -n "$OWNER" ] && chown -R "$OWNER" "$NEW"

if [ "$MODE" = "fresh" ]; then
    rm -rf "$TGT"
else
    if [ -e "$TGT" ] || [ -L "$TGT" ]; then
        BAK="$TGT.bak.$(date +%Y%m%d%H%M%S)"
        mv "$TGT" "$BAK"
        echo "backup: $BAK"
    fi
fi
mv "$NEW" "$TGT"
rm -f "$ARCHIVE"

# 清理多余历史备份
if [ "$MODE" != "fresh" ] && [ "${KEEP:-3}" -gt 0 ] 2>/dev/null; then
    ls -1dt "$TGT".bak.* 2>/dev/null | tail -n +"$((KEEP + 1))" | while read -r old; do rm -rf "$old"; done
fi

if [ -n "$POSTCMD" ]; then
    echo "post: $POSTCMD"
    sh -c "$POSTCMD"
fi
echo "deployed: $TGT"
'@

$remoteCmd = @(
    "bash $(Quote-Sh $remoteScript)",
    (Quote-Sh $remoteArchive), (Quote-Sh $Target), (Quote-Sh "$KeepBackups"),
    (Quote-Sh $mode), (Quote-Sh $Owner), (Quote-Sh $PostCommand)
) -join ' '

$teardown = "rm -f $(Quote-Sh $remoteArchive) $(Quote-Sh $remoteScript)"

try {
    if ($DumpScriptPath) {
        Set-Content -LiteralPath $DumpScriptPath -Value ($remoteCode -replace "`r`n", "`n") -Encoding utf8NoBOM -NoNewline
        Write-Host "remote script -> $DumpScriptPath"
        return
    }
    if ($DryRun) {
        Write-Host "--- DRY RUN ---" -ForegroundColor Yellow
        Write-Host "tar -czf $localArchive -C $srcFull ."
        Write-Host "scp $($scpBase -join ' ') <archive> $($Server):$remoteArchive"
        Write-Host "scp $($scpBase -join ' ') <script> $($Server):$remoteScript"
        Write-Host "ssh $($sshBase -join ' ') $Server $remoteCmd"
        return
    }

    Step "1/5 打包 $srcFull"
    & tar -czf $localArchive -C $srcFull .
    if ($LASTEXITCODE -ne 0) { Fail "打包失败" }

    Set-Content -LiteralPath $localScript -Value $remoteCode -Encoding utf8NoBOM -NoNewline
    # 统一为 LF，避免远端 sh 解析 CRLF 失败
    $body = (Get-Content -LiteralPath $localScript -Raw) -replace "`r`n", "`n"
    Set-Content -LiteralPath $localScript -Value $body -Encoding utf8NoBOM -NoNewline

    Step "2/5 上传部署脚本与压缩包"
    & scp @scpBase $localScript "${Server}:$remoteScript"
    if ($LASTEXITCODE -ne 0) { Fail "上传脚本失败" }
    & scp @scpBase $localArchive "${Server}:$remoteArchive"
    if ($LASTEXITCODE -ne 0) { Fail "上传压缩包失败" }

    Step "3/5 远程解压并切换目录"
    & ssh @sshBase $Server $remoteCmd
    if ($LASTEXITCODE -ne 0) {
        & ssh @sshBase $Server $teardown 2>$null
        Fail "远程部署失败（退出码 $LASTEXITCODE）"
    }

    Step "4/5 清理远程临时文件"
    & ssh @sshBase $Server $teardown 2>$null

    Step "5/5 完成"
    Write-Host "[deploy] 成功 -> $($Server):$Target" -ForegroundColor Green
    if (-not $Fresh) {
        Write-Host "[deploy] 回滚: ssh $($sshBase -join ' ') $Server 'rm -rf $Target && mv $Target.bak.<时间戳> $Target'" -ForegroundColor DarkGray
    }
}
finally {
    if (Test-Path -LiteralPath $localArchive) {
        [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile(
            $localArchive, 'OnlyErrorDialogs', 'SendToRecycleBin')
    }
    if (Test-Path -LiteralPath $localScript) {
        [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile(
            $localScript, 'OnlyErrorDialogs', 'SendToRecycleBin')
    }
}
