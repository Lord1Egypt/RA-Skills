# cad-file-reader Windows 跨平台安装器（PowerShell 入口）。
# 用法：
#   powershell -ExecutionPolicy Bypass -File scripts\setup_windows.ps1            # 正常安装
#   powershell -ExecutionPolicy Bypass -File scripts\setup_windows.ps1 -DryRun    # 只打印检测与依赖清单
# 功能：
#   - 找 python（优先 py 启动器，回退 python / python3）；
#   - 调用 scripts/setup.py 安装/校验 vendor（公共 PyPI --target vendor）；
#   - 打印 ODA / poppler / tesseract 的 Windows 安装指引（winget/choco/官方页）；
#   - 结尾调用 scripts/run_cad.py doctor 做环境摘要（可通过 -SkipDoctor 跳过）。
param(
    [switch]$DryRun,
    [switch]$SkipDoctor
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillDir = Split-Path -Parent $ScriptDir

function Find-Python {
    foreach ($candidate in @($env:CAD_PYTHON, (Get-Command py -ErrorAction SilentlyContinue).Source,
                             (Get-Command python -ErrorAction SilentlyContinue).Source,
                             (Get-Command python3 -ErrorAction SilentlyContinue).Source)) {
        if ($candidate -and (Test-Path $candidate)) { return $candidate }
    }
    # py 启动器常以别名形式存在但 Powershell 里通过 Get-Command 找不到
    $py = "$env:ProgramFiles\PythonLauncher\py.exe"
    if (Test-Path $py) { return $py }
    throw "未找到 python/py，请先安装 Python 3.10+（可从 https://www.python.org/downloads/windows/ 安装并勾选 Add to PATH）。"
}

$python = Find-Python
Write-Host "python = $python"

if ($DryRun) {
    & $python "$ScriptDir\setup.py" --dry-run
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} else {
    & $python "$ScriptDir\setup.py" @args
    if ($LASTEXITCODE -ne 0) { Write-Error "scripts/setup.py 安装失败（错误码 $LASTEXITCODE）"; exit $LASTEXITCODE }
}

Write-Host "`n[外部后端指引 - 仅按需安装]"
Write-Host "1) DWG/DXF 解析：本技能自带 ezdwg/ezdxf，不需要外部转换；如需阅后转换，可装 ODAFileConverter：winget install ODA.ODAFileConverter  或 https://www.opendesign.com/guestfiles/oda_file_converter"
Write-Host "2) PDF 转图片（矢量层读取）：winget install poppler.poppler"
Write-Host "3) 扫描/图片 OCR：winget install UB-Mannheim.TesseractOCR  或 choco install tesseract（中文包需在安装器里勾选 chi_sim 或手工放入 tessdata）"

if (-not $SkipDoctor) {
    Write-Host "`n[doctor 摘要]"
    & $python "$ScriptDir\run_cad.py" doctor --no-write
    exit $LASTEXITCODE
}
