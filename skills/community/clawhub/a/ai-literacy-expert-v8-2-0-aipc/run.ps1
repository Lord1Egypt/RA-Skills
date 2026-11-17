<#
.SYNOPSIS
    ai-literacy-expert-v8.1.0-aipc fixed entry point (never rename).

.DESCRIPTION
    Flow:
      1. $ErrorActionPreference = 'Stop'
      2. Parse arguments (subcommand routing)
      3. Hardware detection (Intel AIPC / MTL·LNL·ARL·PTL iGPU / dGPU whitelist)
      4. Ensure Python environment (install-env.ps1)
      5. Route to pipeline script (bootstrap / prepare / analyze / select / compose / exchange)

.USAGE
    .\run.ps1 bootstrap <course_dir>              # 一键准备 + 4 阶段流水线
    .\run.ps1 prepare   <course_dir>              # 阶段 1: 工作区初始化
    .\run.ps1 analyze   <workspace_dir>           # 阶段 2: 本地文本推理
    .\run.ps1 select    <workspace_dir>           # 阶段 3: 知识点筛选
    .\run.ps1 compose   <workspace_dir>           # 阶段 4: 合成课件
    .\run.ps1 exchange  <request.json>            # 端云协议交换
    .\run.ps1 validate  <request.json>            # 协议 schema 校验
    .\run.ps1 check                                # 硬件 + Python 预检
    .\run.ps1 --continue                           # 断点续传（恢复中断的下载）

.EXIT CODES
    0  Success
    1  General error (bad args / unsupported hardware / env install failed)
    2  Communication error (edge-cloud exchange failure)
    3  Model downloading — rerun with --continue
#>
$ErrorActionPreference = 'Stop'

# run.ps1 位于 <SKILL_DIR>/run.ps1，$PSScriptRoot 即为 skill 根目录。
# 修复：原代码使用 `Split-Path -Parent $PSScriptRoot` 多走了一级，
# 会导致 $Scripts 指向 <SKILL_DIR>/../scripts（错）。
$Root    = $PSScriptRoot
$Scripts = Join-Path $Root 'scripts'

# --- 1. Parse subcommand ----------------------------------------------------
if ($args.Count -eq 0) {
    Write-Output "Usage: .\run.ps1 <command> [args]"
    Write-Output "  bootstrap <course_dir>   一键准备 + 4 阶段流水线"
    Write-Output "  prepare   <course_dir>   阶段 1: 工作区初始化"
    Write-Output "  analyze   <workspace>    阶段 2: 本地文本推理"
    Write-Output "  select    <workspace>    阶段 3: 知识点筛选"
    Write-Output "  compose   <workspace>    阶段 4: 合成课件"
    Write-Output "  exchange  <req.json>     端云协议交换"
    Write-Output "  validate  <req.json>     协议 schema 校验"
    Write-Output "  check                    硬件 + Python 预检"
    Write-Output "  --continue               断点续传（恢复下载）"
    exit 1
}

$cmd = $args[0]
$cmdArgs = $args[1..($args.Count - 1)]
if (-not $cmdArgs) { $cmdArgs = @() }

# --- 2. Hardware detection (only for pipeline commands) ---------------------
$hardwareCmds = @('bootstrap', 'prepare', 'analyze', 'select', 'compose', 'check')
if ($hardwareCmds -contains $cmd) {
    & (Join-Path $Scripts 'check_platform.ps1')
    if ($LASTEXITCODE -ne 0) {
        Write-Error "[run.ps1] Hardware check failed. Exit 1."
        exit 1
    }
}

# 'check' command stops here after hardware + python verification
if ($cmd -eq 'check') {
    Write-Output "[run.ps1] ✓ All preflight checks passed."
    exit 0
}

# --- 3. Ensure Python environment -------------------------------------------
& (Join-Path $Scripts 'install-env.ps1')
if ($LASTEXITCODE -ne 0) {
    Write-Error "[run.ps1] Environment install failed. Exit 1."
    exit 1
}

# --- 4. Resolve venv python -------------------------------------------------
$VenvPython = Join-Path $Root '.venv\Scripts\python.exe'
if (-not (Test-Path $VenvPython)) {
    Write-Error "[run.ps1] venv python not found: $VenvPython"
    exit 1
}

# --- 5. Route to pipeline script --------------------------------------------
switch ($cmd) {
    'bootstrap' {
        & $VenvPython (Join-Path $Scripts 'bootstrap.py') @cmdArgs
        exit $LASTEXITCODE
    }
    'prepare' {
        & $VenvPython (Join-Path $Scripts 'prepare_workspace.py') @cmdArgs
        exit $LASTEXITCODE
    }
    'analyze' {
        & $VenvPython (Join-Path $Scripts 'analyze_courseware.py') @cmdArgs
        exit $LASTEXITCODE
    }
    'select' {
        & $VenvPython (Join-Path $Scripts 'select_knowledge.py') @cmdArgs
        exit $LASTEXITCODE
    }
    'compose' {
        & $VenvPython (Join-Path $Scripts 'compose_lesson.py') @cmdArgs
        exit $LASTEXITCODE
    }
    'exchange' {
        & $VenvPython (Join-Path $Scripts 'edge_cloud_dispatch.py') exchange @cmdArgs
        $code = $LASTEXITCODE
        if ($code -eq 0) { exit 0 }
        if ($code -eq 2) { exit 2 }
        exit 1
    }
    'validate' {
        & $VenvPython (Join-Path $Scripts 'edge_cloud_dispatch.py') validate @cmdArgs
        exit $LASTEXITCODE
    }
    '--continue' {
        & $VenvPython (Join-Path $Scripts 'setup_text_model.py') --continue @cmdArgs
        $code = $LASTEXITCODE
        if ($code -eq 3) {
            Write-Output "[run.ps1] 下载未完成，请再次运行 --continue 继续下载。"
            exit 3
        }
        exit $code
    }
    default {
        Write-Error "[run.ps1] Unknown command: $cmd"
        Write-Output "Run '.\run.ps1' without args to see usage."
        exit 1
    }
}
