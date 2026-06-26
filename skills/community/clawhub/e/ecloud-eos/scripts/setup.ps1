# Mobile Cloud EOS Skill Auto Setup Script (Windows Version)
# Usage:
#   .\setup.ps1 -CheckOnly                     Check environment status only
#   .\setup.ps1 -AccessKey <ID> -SecretKey <KEY> -Region <REGION> -Bucket <BUCKET> -Endpoint <ENDPOINT>
#   .\setup.ps1 -ConfigFile <path>             Use config file for credentials (properties format)

param(
    [string]$AccessKey,
    [string]$SecretKey,
    [string]$Region,
    [string]$Bucket,
    [string]$Endpoint,
    [string]$ConfigFile,
    [string]$SetBucket,
    [string]$CopyConfigFile,
    [switch]$CheckOnly
)

# Color output functions
function log_info { Write-Host "[OK] $args" -ForegroundColor Green }
function log_error { Write-Host "[ERR] $args" -ForegroundColor Red }
function log_warn { Write-Host "[WARN] $args" -ForegroundColor Yellow }

# Get script directory (skill baseDir)
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$BASE_DIR = Split-Path -Parent $SCRIPT_DIR

# ========== Check Functions ==========

function check_node {
    if (Get-Command node -ErrorAction SilentlyContinue) {
        log_info "Node.js $(node --version)"
        return $true
    } else {
        log_error "Node.js not installed"
        return $false
    }
}

function check_npm {
    if (Get-Command npm -ErrorAction SilentlyContinue) {
        log_info "npm $(npm --version)"
        return $true
    } else {
        log_error "npm not installed"
        return $false
    }
}

function check_eos_sdk {
    $sdkCheck = node -e "try { require('@aws-sdk/client-s3'); require('@aws-sdk/s3-request-presigner'); require('@smithy/hash-node'); require('@smithy/protocol-http'); console.log('OK'); } catch(e) { console.log('FAIL'); }" 2>&1
    if ($sdkCheck -match 'OK') {
        log_info "Node.js SDK installed"
        return $true
    } else {
        log_error "Node.js SDK not installed"
        return $false
    }
}

function check_env_vars {
    $allSet = $true
    $bucketMissing = $false

    # 检查必要的环境变量
    $requiredVars = @{
        'EOS_ACCESS_KEY' = $env:EOS_ACCESS_KEY
        'EOS_SECRET_KEY' = $env:EOS_SECRET_KEY
        'EOS_REGION' = $env:EOS_REGION
        'EOS_ENDPOINT' = $env:EOS_ENDPOINT
    }

    foreach ($var in $requiredVars.Keys) {
        if ($requiredVars[$var] -and $requiredVars[$var] -ne '') {
            log_info "$var is set"
        } else {
            log_error "$var not set"
            $allSet = $false
        }
    }

    # 检查桶名环境变量（允许缺失，但会提示）
    if ($env:EOS_BUCKET -and $env:EOS_BUCKET -ne '') {
        log_info "EOS_BUCKET is set"
    } else {
        log_warn "EOS_BUCKET not set (但可以执行 list-buckets/create-bucket/delete-bucket 操作)"
        $bucketMissing = $true
    }

    return $allSet
}

# ========== Check Mode ==========

function do_check {
    Write-Host "=== Mobile Cloud EOS Skill Environment Check ===" -ForegroundColor Cyan
    Write-Host ""

    Write-Host "--- Basic Environment ---" -ForegroundColor Cyan
    check_node
    check_npm
    Write-Host ""

    Write-Host "--- Node.js SDK ---" -ForegroundColor Cyan
    check_eos_sdk
    Write-Host ""

    Write-Host "--- Environment Variables ---" -ForegroundColor Cyan
    if (check_env_vars) {
        log_info "EOS环境变量配置完成"
    } else {
        log_error "缺少必要的EOS环境变量"
    }
    Write-Host ""

    Write-Host "--- Skill Files ---" -ForegroundColor Cyan
    if (Test-Path "$BASE_DIR\SKILL.md") { log_info "SKILL.md" } else { log_error "SKILL.md not found" }
    if (Test-Path "$BASE_DIR\scripts\eos_node.mjs") { log_info "scripts/eos_node.mjs" } else { log_error "scripts/eos_node.mjs not found" }
    Write-Host ""
}

# ========== Setup Mode ==========

function do_setup {
    # 如果用户提供了配置文件，从配置文件读取凭证
    if ($ConfigFile) {
        if (-not (Test-Path $ConfigFile)) {
            Write-Host "Error: Config file not found: $ConfigFile" -ForegroundColor Red
            exit 1
        }

        Write-Host "Reading config file: $ConfigFile" -ForegroundColor Cyan

        try {
            $config = @{}
            Get-Content $ConfigFile | ForEach-Object {
                if ($_ -match '^([^=]+)=(.*)$') {
                    $config[$matches[1].Trim()] = $matches[2].Trim()
                }
            }

            $AccessKey = $config['accessKey']
            $SecretKey = $config['secretKey']
            $Region = $config['region']
            $Bucket = $config['bucket']
            $Endpoint = $config['endpoint']

            Write-Host "Loaded credentials:" -ForegroundColor Cyan
            Write-Host "  AccessKey: $AccessKey" -ForegroundColor Gray
            Write-Host "  region: $Region" -ForegroundColor Gray
            Write-Host "  bucket: $Bucket" -ForegroundColor Gray
            Write-Host "  endpoint: $Endpoint" -ForegroundColor Gray

            if (-not $AccessKey -or -not $SecretKey -or -not $Region -or -not $Bucket -or -not $Endpoint) {
                Write-Host "Error: Config file is missing required fields" -ForegroundColor Red
                $missing = @()
                if (-not $AccessKey) { $missing += 'AccessKey' }
                if (-not $SecretKey) { $missing += 'SecretKey' }
                if (-not $Region) { $missing += 'region' }
                if (-not $Bucket) { $missing += 'bucket' }
                if (-not $Endpoint) { $missing += 'endpoint' }
                Write-Host "Missing: $($missing -join ', ')" -ForegroundColor Red
                exit 1
            }

            log_info "Credentials loaded from config file: $ConfigFile"
        } catch {
            Write-Host "Error: Failed to parse config file: $ConfigFile" -ForegroundColor Red
            Write-Host $_.Exception.Message -ForegroundColor Red
            exit 1
        }
    }

    if (-not $AccessKey -or -not $SecretKey -or -not $Region -or -not $Bucket -or -not $Endpoint) {
        Write-Host "Error: Missing required parameters" -ForegroundColor Red
        Write-Host "Usage: .\setup.ps1 -AccessKey <ID> -SecretKey <KEY> -Region <REGION> -Bucket <BUCKET> -Endpoint <ENDPOINT>" -ForegroundColor Yellow
        Write-Host "Or: .\setup.ps1 -ConfigFile <path>" -ForegroundColor Yellow
        exit 1
    }

    Write-Host "=== Mobile Cloud EOS Skill Auto Setup ===" -ForegroundColor Cyan
    Write-Host ""

    # 1. Check Node.js
    Write-Host "--- Step 1: Check Node.js ---" -ForegroundColor Cyan
    if (-not (check_node)) {
        log_error "Please install Node.js first: https://nodejs.org/"
        exit 1
    }

    # 2. Ensure package.json exists
    Write-Host ""
    Write-Host "--- Step 2: Initialize Project ---" -ForegroundColor Cyan
    if (-not (Test-Path "$BASE_DIR\package.json")) {
        Set-Location $BASE_DIR
        npm init -y | Out-Null
        log_info "Created package.json"
    } else {
        log_info "package.json already exists"
    }

    # Ensure package.json uses module type
    $packageJson = Get-Content "$BASE_DIR\package.json" -Raw | ConvertFrom-Json
    if ($packageJson.type -ne "module") {
        $packageJson.type = "module"
        $packageJson | ConvertTo-Json -Depth 10 | Set-Content "$BASE_DIR\package.json"
        log_info "Updated package.json to ES6 module"
    }

    # 3. Install Dependencies
    Write-Host ""
    Write-Host "--- Step 3: Install Dependencies ---" -ForegroundColor Cyan
    Set-Location $BASE_DIR
    $output = npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner @smithy/hash-node @smithy/protocol-http --no-progress 2>&1
    $output | Select-Object -Last 3
    log_info "Dependencies installation completed"

    # 4. Set Environment Variables
    Write-Host ""
    Write-Host "--- Step 4: Set Environment Variables ---" -ForegroundColor Cyan

    # Set environment variables for current session
    $env:EOS_ACCESS_KEY = $AccessKey
    $env:EOS_SECRET_KEY = $SecretKey
    $env:EOS_REGION = $Region
    $env:EOS_BUCKET = $Bucket
    $env:EOS_ENDPOINT = $Endpoint

    # Set environment variables for User level (persistent)
    [Environment]::SetEnvironmentVariable("EOS_ACCESS_KEY", $AccessKey, "User")
    [Environment]::SetEnvironmentVariable("EOS_SECRET_KEY", $SecretKey, "User")
    [Environment]::SetEnvironmentVariable("EOS_REGION", $Region, "User")
    [Environment]::SetEnvironmentVariable("EOS_BUCKET", $Bucket, "User")
    [Environment]::SetEnvironmentVariable("EOS_ENDPOINT", $Endpoint, "User")

    log_info "Environment variables set (current session and User level)"
    Write-Host "  EOS_ACCESS_KEY = $AccessKey" -ForegroundColor Gray
    Write-Host "  EOS_SECRET_KEY = ***" -ForegroundColor Gray
    Write-Host "  EOS_REGION = $Region" -ForegroundColor Gray
    Write-Host "  EOS_BUCKET = $Bucket" -ForegroundColor Gray
    Write-Host "  EOS_ENDPOINT = $Endpoint" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Note: Environment variables are set at User level and will persist across sessions." -ForegroundColor Green
    Write-Host "      New terminal sessions will automatically have these variables." -ForegroundColor Green

    # 5. Verify
    Write-Host ""
    Write-Host "--- Step 5: Verify Connection ---" -ForegroundColor Cyan
    $testOutput = node "$BASE_DIR\scripts\eos_node.mjs" list --max-keys 1 2>&1
    if ($testOutput -match '"success":\s*true') {
        log_info "EOS connection verified successfully"
    } else {
        log_warn "EOS connection verification failed, please check credentials and network"
    }

    Write-Host ""
    Write-Host "=== Setup Complete ===" -ForegroundColor Green
    Write-Host "You can now use EOS with the following methods:" -ForegroundColor Cyan
    Write-Host "  node $BASE_DIR\scripts\eos_node.mjs <action>" -ForegroundColor White
    Write-Host ""
    Write-Host "Note: Environment variables are set at User level and will persist across sessions." -ForegroundColor Green
    Write-Host "      OpenCLAW should update its process.env with the same values for immediate effect." -ForegroundColor Green
}

# ========== Load Config File ==========

function do_load_config_file {
    if (-not $CopyConfigFile) {
        Write-Host "Error: Missing config file path" -ForegroundColor Red
        Write-Host "Usage: .\setup.ps1 -CopyConfigFile <config-file-path>" -ForegroundColor Yellow
        exit 1
    }

    if (-not (Test-Path $CopyConfigFile)) {
        Write-Host "Error: Config file not found: $CopyConfigFile" -ForegroundColor Red
        exit 1
    }

    Write-Host "=== Load Config File ===" -ForegroundColor Cyan
    Write-Host "Source: $CopyConfigFile" -ForegroundColor White
    
    # 从配置文件中读取凭证
    try {
        $config = @{}
        Get-Content $CopyConfigFile | ForEach-Object {
            if ($_ -match '^([^=]+)=(.*)$') {
                $config[$matches[1].Trim()] = $matches[2].Trim()
            }
        }

        $script:AccessKey = $config['accessKey']
        $script:SecretKey = $config['secretKey']
        $script:Region = $config['region']
        $script:Bucket = $config['bucket']
        $script:Endpoint = $config['endpoint']

        # 验证是否包含必要的配置项
        $requiredKeys = @('AccessKey', 'SecretKey', 'region', 'bucket', 'endpoint')
        $missingKeys = @()
        
        foreach ($key in $requiredKeys) {
            if (-not $config[$key]) {
                $missingKeys += $key
            }
        }
        
        if ($missingKeys.Count -gt 0) {
            Write-Host "Warning: Config file is missing required keys: $($missingKeys -join ', ')" -ForegroundColor Yellow
            Write-Host "Required keys: $($requiredKeys -join ', ')" -ForegroundColor Yellow
            exit 1
        }

        Write-Host ""
        Write-Host "Credentials loaded from config file:" -ForegroundColor Cyan
        Write-Host "  AccessKey: $AccessKey" -ForegroundColor Gray
        Write-Host "  region: $Region" -ForegroundColor Gray
        Write-Host "  bucket: $Bucket" -ForegroundColor Gray
        Write-Host "  endpoint: $Endpoint" -ForegroundColor Gray
    } catch {
        Write-Host "Error: Failed to parse config file: $CopyConfigFile" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "=== Load Complete ===" -ForegroundColor Green
    # Don't return here, continue with setup process
}

# ========== Set Bucket ==========

function do_set_bucket {
    if (-not $SetBucket) {
        Write-Host "Error: Missing bucket name" -ForegroundColor Red
        Write-Host "Usage: .\setup.ps1 -SetBucket <bucket>" -ForegroundColor Yellow
        exit 1
    }

    Write-Host "=== Update Bucket Name ===" -ForegroundColor Cyan
    Write-Host "Updating bucket to: $SetBucket" -ForegroundColor White

    # 更新环境变量（当前会话和 User 级别）
    $env:EOS_BUCKET = $SetBucket
    [Environment]::SetEnvironmentVariable("EOS_BUCKET", $SetBucket, "User")
    log_info "EOS_BUCKET environment variable updated (current session and User level)"

    # 验证新桶是否可访问
    Write-Host ""
    Write-Host "--- Verify Bucket Access ---" -ForegroundColor Cyan
    $testOutput = node "$BASE_DIR\scripts\eos_node.mjs" list --max-keys 1 2>&1
    if ($testOutput -match '"success":\s*true') {
        log_info "Bucket access verified successfully"
    } else {
        log_warn "Bucket access verification failed, bucket may not exist or no permission"
    }

    Write-Host ""
    Write-Host "=== Bucket Update Complete ===" -ForegroundColor Green
    Write-Host "New bucket: $SetBucket" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Note: Bucket name is set at User level." -ForegroundColor Green
    Write-Host "      OpenCLAW should update its process.env.EOS_BUCKET with the same value for immediate effect." -ForegroundColor Green
}

# ========== Main Entry ==========

if ($CopyConfigFile) {
    do_load_config_file
    # After loading config file, continue with setup process
    do_setup
} elseif ($SetBucket) {
    do_set_bucket
} elseif ($CheckOnly) {
    do_check
} elseif ($AccessKey -or $SecretKey -or $Region -or $Bucket -or $Endpoint -or $ConfigFile) {
    do_setup
} else {
    Write-Host "Mobile Cloud EOS Skill Setup Tool (Windows Version)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\setup.ps1 -CheckOnly"
    Write-Host "    Check environment status only"
    Write-Host ""
    Write-Host "  .\setup.ps1 -AccessKey <ID> -SecretKey <KEY> -Region <REGION> -Bucket <BUCKET> -Endpoint <ENDPOINT>"
    Write-Host "    Auto setup environment (install dependencies + set environment variables + verify connection)"
    Write-Host ""
    Write-Host "  .\setup.ps1 -ConfigFile <path>"
    Write-Host "    Use config file for credentials (properties format)"
    Write-Host "    Config file template: references/config_template.properties"
    Write-Host ""
    Write-Host "  .\setup.ps1 -CopyConfigFile <path>"
    Write-Host "    Load credentials from config file and set environment variables"
    Write-Host ""
    Write-Host "  .\setup.ps1 -SetBucket <bucket>"
    Write-Host "    Update bucket name in environment variables (keep other settings)"
}
