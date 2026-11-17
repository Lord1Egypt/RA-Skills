# ============================================================
# 1688 Data Claw - Windows 环境变量（PowerShell）
# Source: . .\env.ps1
# ============================================================

$script:SCRIPTS_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$script:SKILL_DIR = Split-Path $SCRIPTS_DIR -Parent

$script:CHROME = "$SKILL_DIR\chromium\chrome-win64\chrome.exe"
$script:USER_DATA = "C:\isolated-profiles\1688-agent"
$script:EXT_DIR = "$SKILL_DIR\plugin"
$script:CDP_PORT = 9222
$script:OUTPUT_DIR = "$SKILL_DIR"
$script:PYTHON_EXE = "$SKILL_DIR\python3\python.exe"

# --- 飞书（部署时填入：实际使用的群聊 chat_id，oc_ 开头）---
$script:FEISHU_CHAT_ID = ""

# --- 飞书应用凭证（部署时填入，push_feishu_post.py 直接调飞书 open API 需要）---
$script:FEISHU_APP_ID = ""
$script:FEISHU_APP_SECRET = ""
