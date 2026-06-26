$ErrorActionPreference = "Stop"

$SkillDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DefaultFosunEnvPath = Join-Path (Split-Path -Parent $SkillDir) "fosun.env"
$env:FOSUN_ENV_PATH = if ($env:FOSUN_ENV_PATH) { $env:FOSUN_ENV_PATH } else { $DefaultFosunEnvPath }

$VenvDir = if ($env:REAL_VENV) { $env:REAL_VENV } else { Join-Path $HOME ".openclaw\workspace\.venv-real" }
$PinPythonVersion = if ($env:REAL_PYTHON_VERSION) { $env:REAL_PYTHON_VERSION } else { "3.13" }
$SdkVersion = if ($env:REAL_SDK_VERSION) { $env:REAL_SDK_VERSION } else { "v1.2.0" }
$SdkZipUrlPrimary = if ($env:REAL_SDK_URL) { $env:REAL_SDK_URL } else { "https://hk.gh-proxy.org/https://github.com/fosunwealth/openapi-python-sdk/archive/refs/tags/v1.2.0.zip" }
$SdkZipUrl = $SdkZipUrlPrimary
$DefaultCacheRoot = if ($env:LOCALAPPDATA) { Join-Path $env:LOCALAPPDATA "fw-trade-skill\cache" } else { Join-Path $HOME ".cache\fw-trade-skill" }
$SdkCacheRoot = if ($env:REAL_CACHE_DIR) { $env:REAL_CACHE_DIR } else { $DefaultCacheRoot }
$SdkCacheDir = Join-Path $SdkCacheRoot "openapi-python-sdk-$SdkVersion"

function Log([string]$msg) { Write-Host "[real-trade] $msg" -ForegroundColor Cyan }
function Fail([string]$msg) { Write-Host "[real-trade ERROR] $msg" -ForegroundColor Red; exit 1 }

function Ensure-Uv {
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        Log "检测到 uv：$((Get-Command uv).Source)"
        return
    }
    Log "未检测到 uv，自动安装..."
    try {
        Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    } catch {
        Fail "uv 自动安装失败，请手动安装后重试。文档：https://docs.astral.sh/uv/getting-started/installation/"
    }
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Fail "uv 安装后仍不可用，请重启终端后重试。"
    }
    Log "uv 安装完成：$((Get-Command uv).Source)"
}

Ensure-Uv

$VenvPy = Join-Path $VenvDir "Scripts\python.exe"
if (-not (Test-Path $VenvPy)) {
    Log "创建独立环境（uv 会按需下载 Python $PinPythonVersion）：$VenvDir"
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $VenvDir) | Out-Null
    uv venv --python $PinPythonVersion "$VenvDir"
} else {
    Log "复用已有独立环境：$VenvDir"
}

if (-not (Test-Path $VenvPy)) {
    Fail "独立环境创建失败，未找到解释器：$VenvPy"
}

function Resolve-SdkFallbackUrl {
    if ($env:REAL_SDK_FALLBACK_URL) {
        return $env:REAL_SDK_FALLBACK_URL
    }
    $ensureScript = Join-Path (Join-Path (Split-Path -Parent $SkillDir) "fosun-env-setup\code") "ensure_fosun_env.py"
    if (-not (Test-Path $ensureScript)) {
        return ""
    }
    $py = @'
import importlib.util
import sys
from pathlib import Path

module_path = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("ensure_fosun_env", module_path)
if spec is None or spec.loader is None:
    raise SystemExit(0)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
value = getattr(module, "DEFAULT_SDK_ZIP_FALLBACK_URL", "")
print(str(value).strip())
'@
    try {
        return (& $VenvPy -c $py $ensureScript).Trim()
    } catch {
        return ""
    }
}

$SdkZipUrlFallback = Resolve-SdkFallbackUrl

$TmpBuildDir = Join-Path ([System.IO.Path]::GetTempPath()) ("real-trade-build-" + [guid]::NewGuid().ToString("N"))
$SdkZipPath = Join-Path $TmpBuildDir "openapi-python-sdk.zip"
$SdkExtractDir = Join-Path $TmpBuildDir "src"
New-Item -ItemType Directory -Force -Path $SdkExtractDir | Out-Null

try {
    Log "下载官方 SDK 源码（主源）：$SdkZipUrlPrimary"
    try {
        Invoke-WebRequest -Uri $SdkZipUrlPrimary -OutFile $SdkZipPath
        $SdkZipUrl = $SdkZipUrlPrimary
    } catch {
        if ($SdkZipUrlFallback -and ($SdkZipUrlFallback -ne $SdkZipUrlPrimary)) {
            Log "主源下载失败，尝试备用源：$SdkZipUrlFallback"
            Invoke-WebRequest -Uri $SdkZipUrlFallback -OutFile $SdkZipPath
            $SdkZipUrl = $SdkZipUrlFallback
        } else {
            throw
        }
    }

    Log "解压 SDK 源码包"
    Expand-Archive -Path $SdkZipPath -DestinationPath $SdkExtractDir -Force

    $SdkExtractedDir = Get-ChildItem -Path $SdkExtractDir -Recurse -File |
        Where-Object { $_.Name -in @("setup.py", "pyproject.toml") } |
        Select-Object -First 1 |
        ForEach-Object { $_.Directory.FullName }

    if (-not $SdkExtractedDir) {
        Fail "未在解压目录中找到 setup.py / pyproject.toml"
    }

    New-Item -ItemType Directory -Force -Path $SdkCacheRoot | Out-Null
    if (Test-Path $SdkCacheDir) {
        Remove-Item -Recurse -Force $SdkCacheDir
    }
    Copy-Item -Path $SdkExtractedDir -Destination $SdkCacheDir -Recurse
    $SdkSrcDir = $SdkCacheDir

    Log "SDK 源码目录：$SdkSrcDir"
    Log "安装 fsopenapi SDK（editable 模式）"
    uv pip install --python "$VenvPy" --reinstall --editable "$SdkSrcDir"

    Log "自检 import fsopenapi"
    & $VenvPy -c "import fsopenapi; print('  fsopenapi @', fsopenapi.__file__)"
} finally {
    if (Test-Path $TmpBuildDir) {
        Remove-Item -Recurse -Force $TmpBuildDir
    }
}

Write-Host ""
Write-Host "✅ 安装完成。"
Write-Host "🐍 Python 解释器：$VenvPy"
Write-Host "📁 Skill 目录：$SkillDir"
Write-Host "🔐 共享凭证路径：$($env:FOSUN_ENV_PATH)"
Write-Host "📦 SDK 来源：$SdkZipUrl"
Write-Host "📂 SDK 缓存：$SdkSrcDir"
