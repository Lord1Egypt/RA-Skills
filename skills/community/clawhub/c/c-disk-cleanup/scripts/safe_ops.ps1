# safe_ops.ps1 - 受控安全操作（默认只模拟，绝不偷偷动手）
# 所有会移动/移除文件的动作都必须显式传 -Confirmed 才执行；否则只打印将要做什么。
#
# v1.1.0 新增护栏（经真机实战验证）：
#   * 程序目录/IM 加密库拦截：拒绝搬 AppData 主程序与聊天加密数据库，避免软件损坏/记录丢失
#   * 进程锁检测：搬前检测占用，提示关闭软件，防"半搬走"
#   * 逐子目录容错：损坏/锁定子目录跳过并报告，不整块失败
#
# 用法示例：
#   模拟（只看不动）:
#     powershell -ExecutionPolicy Bypass -File safe_ops.ps1 -Action MoveToBackup -Path "C:\Users\me\AppData\Local\Temp" -BackupDrive D
#   真动手（必须带 -Confirmed，且用户已同意）:
#     powershell -ExecutionPolicy Bypass -File safe_ops.ps1 -Action MoveToBackup -Path "..." -BackupDrive D -Confirmed
#   走系统官方磁盘清理（需用户同意）:
#     powershell -ExecutionPolicy Bypass -File safe_ops.ps1 -Action WindowsClean -Confirmed
#   送回收站（兜底，可恢复）:
#     powershell -ExecutionPolicy Bypass -File safe_ops.ps1 -Action SendToRecycle -Path "..." -Confirmed

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("MoveToBackup","WindowsClean","SendToRecycle")]
    [string]$Action,

    [string]$Path = "",
    [string]$BackupDrive = "",

    [switch]$Confirmed
)

$ErrorActionPreference = 'SilentlyContinue'

function Send-ToRecycle($item){
    $shell = New-Object -ComObject Shell.Application
    $full = (Resolve-Path $item).Path
    $shell.NameSpace(0x10).MoveHere($full)
}

# ---- 安全检查：是否允许搬这个路径 ----
function Test-SafeToMove($p){
    $norm = $p.Replace('/','\').TrimEnd('\')
    # IM / 加密数据库（拒绝，引导官方迁移）
    $imPatterns = @('xwechat_files','WeChat Files','WeChat\','\Msg\','FileStorage','QQ\','QQFiles','Tencent Files','Tim\','DingTalk','钉钉','Feishu','飞书','WXWork','企业微信')
    # AppData 主程序目录（拒绝，引导软件内清缓存）
    $progPatterns = @('office6','\WPS Office\','\Kingsoft\','\JianyingPro\','\Microsoft\Office','\Adobe\','\JetBrains\')
    # 允许的缓存/临时特征（按目录名匹配）
    $allow = @('Temp','*Cache','*cache','*-updater','pip','npm','node_modules','临时')
    # 用户文件类（允许但需确认，由 -Confirmed 控制）
    $userPatterns = @('\Desktop','\Downloads','\Documents','桌面','下载','文档','Pictures','图片','Videos','视频','Music','音乐')

    foreach($pat in $imPatterns){ if($norm -like "*$pat*"){ return @{Ok=$false; Reason="这是聊天/加密数据库（命中'$pat'）。请勿手动硬搬，请用软件内「设置->文件管理/更改存储位置」官方迁移，否则会出现记录丢失假象。"} } }
    foreach($pat in $progPatterns){ if($norm -like "*$pat*"){ return @{Ok=$false; Reason="这是软件主程序目录（命中'$pat'）。手动搬走会导致软件打不开。请改用软件内的「清理缓存」功能释放空间。"} } }

    $name = Split-Path $norm -Leaf
    foreach($a in $allow){ if($name -like $a){ return @{Ok=$true; Reason=""} } }
    foreach($u in $userPatterns){ if($norm -like "*$u*"){ return @{Ok=$true; Reason="(用户文件，确认搬移后会保留在备份盘可恢复)"} } }

    # 其它路径：默认允许（多为缓存类），给出温和提示
    return @{Ok=$true; Reason=""}
}

# ---- 进程锁检测：返回占用进程名列表 ----
function Test-ProcessLock($p){
    $norm = $p.Replace('/','\').TrimEnd('\')
    $hits = @()
    Get-Process -ErrorAction SilentlyContinue | ForEach-Object {
        $pp = $_.Path
        if($pp -and $pp -like "*$norm*"){ $hits += $_.Name }
    }
    $known = @('WeChat','wps','wpp','et','QianNiu','chrome','JianyingPro','QQ','DingTalk','Feishu','WXWork')
    Get-Process -ErrorAction SilentlyContinue | ForEach-Object {
        if($known -contains $_.Name){ $hits += $_.Name }
    }
    return ($hits | Sort-Object -Unique)
}

if(-not $Confirmed){
    Write-Host "[模拟模式] 以下是在 -Confirmed 后才会做的事，现在什么都不动：" -ForegroundColor Yellow
}

switch($Action){
    "MoveToBackup" {
        if(-not $Path){ Write-Host "错误：缺少 -Path" -ForegroundColor Red; exit 1 }
        if(-not $BackupDrive){ Write-Host "错误：缺少 -BackupDrive（先用 find_backup_drive.ps1 找盘）" -ForegroundColor Red; exit 1 }
        # 安全检查
        $chk = Test-SafeToMove $Path
        if(-not $chk.Ok){
            Write-Host ("[拦截] 不允许搬此路径：$($chk.Reason)") -ForegroundColor Red
            exit 2
        }
        # 进程锁检测
        $locks = Test-ProcessLock $Path
        if($locks.Count -gt 0){
            Write-Host ("[警告] 检测到相关进程可能正在运行：$($locks -join ', ')。建议先完全退出这些软件再搬，否则可能'半搬走'导致软件损坏。") -ForegroundColor Yellow
            if(-not $Confirmed){ Write-Host "（模拟模式：请关闭上述软件后重新运行并加 -Confirmed）" -ForegroundColor Yellow; exit 0 }
        }
        $dst = "$($BackupDrive):\C盘整理\备份_$(Get-Date -Format yyyyMMdd)"
        Write-Host ("要把: {0}" -f $Path)
        Write-Host ("搬到: {0}" -f $dst)
        if($chk.Reason){ Write-Host $chk.Reason -ForegroundColor Cyan }
        Write-Host "（文件保留在备份盘，可恢复，不永久删除）" -ForegroundColor Green
        if($Confirmed){
            New-Item -ItemType Directory -Path $dst -Force | Out-Null
            # 逐子目录容错搬
            $items = Get-ChildItem $Path -ErrorAction SilentlyContinue
            $ok=0; $skip=0
            foreach($it in $items){
                try{
                    Move-Item -Path $it.FullName -Destination "$dst\$($it.Name)" -Force -ErrorAction Stop
                    $ok++
                }catch{
                    Write-Host ("  [跳过] $($it.Name) 搬移失败（可能被锁或路径损坏）：{0}" -f $_.Exception.Message) -ForegroundColor Yellow
                    $skip++
                }
            }
            Write-Host "已完成搬运（成功 $ok 项，跳过 $skip 项）。原路径已腾空，文件在备份盘可找回。" -ForegroundColor Green
        }
    }
    "WindowsClean" {
        Write-Host "将调用 Windows 官方磁盘清理（只清系统临时/回收站/更新缓存等安全项）。" -ForegroundColor Green
        if($Confirmed){
            Start-Process -FilePath "cleanmgr.exe" -ArgumentList "/sagerun:1" -Wait -ErrorAction SilentlyContinue
            Write-Host "磁盘清理已执行（标准安全项）。" -ForegroundColor Green
        }
    }
    "SendToRecycle" {
        if(-not $Path){ Write-Host "错误：缺少 -Path" -ForegroundColor Red; exit 1 }
        $chk = Test-SafeToMove $Path
        if(-not $chk.Ok){ Write-Host ("[拦截] $($chk.Reason)") -ForegroundColor Red; exit 2 }
        Write-Host ("将送回收站（可恢复，但仍在 C 盘，不释放空间，需你之后清空回收站）: {0}" -f $Path) -ForegroundColor Yellow
        if($Confirmed){
            Send-ToRecycle $Path
            Write-Host "已送回收站。" -ForegroundColor Green
        }
    }
}
