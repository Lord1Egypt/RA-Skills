# CDP Bridge MCP 调用脚本
# 用法: .\cdp-call.ps1 -Tool "browser_get_tabs" -ArgsJson "{}"

param(
    [Parameter(Mandatory=$true)]
    [string]$Tool,
    
    [Parameter(Mandatory=$false)]
    [string]$ArgsJson = "{}",
    
    [Parameter(Mandatory=$false)]
    [string]$McpUrl = "http://127.0.0.1:8000/mcp"
)

$ErrorActionPreference = "Stop"

# 初始化 MCP 会话
function InitializeSession {
    $headers = @{
        "Accept" = "application/json, text/event-stream"
        "Content-Type" = "application/json"
    }
    $body = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw-cdp","version":"1.0"}}}'
    
    try {
        $response = Invoke-WebRequest -Uri $McpUrl -Method POST -Headers $headers -Body $body -TimeoutSec 10
        $sessionId = $response.Headers["mcp-session-id"]
        if (-not $sessionId) {
            throw "Failed to get session-id from response"
        }
        return $sessionId
    } catch {
        throw "MCP service not available: $_"
    }
}

# 调用 MCP 工具
function CallTool($sessionId, $toolName, $argsJson) {
    $headers = @{
        "Accept" = "application/json, text/event-stream"
        "Content-Type" = "application/json"
        "mcp-session-id" = $sessionId
    }
    
    $body = @{
        jsonrpc = "2.0"
        id = 2
        method = "tools/call"
        params = @{
            name = $toolName
            arguments = $argsJson | ConvertFrom-Json
        }
    } | ConvertTo-Json -Depth 4
    
    try {
        $response = Invoke-WebRequest -Uri $McpUrl -Method POST -Headers $headers -Body $body -TimeoutSec 60
        return $response.Content
    } catch {
        throw "Tool call failed: $_"
    }
}

# 解析 SSE 响应
function ParseSseResponse($content) {
    # SSE 格式: "event: message\ndata: {...}\n\n"
    $lines = $content -split "\n"
    foreach ($line in $lines) {
        if ($line -match "^data: ") {
            $jsonStr = $line.Substring(6)
            return $jsonStr | ConvertFrom-Json
        }
    }
    return $null
}

# 主流程
try {
    $sessionId = InitializeSession
    Write-Host "Session initialized: $sessionId" -ForegroundColor Green
    
    $responseContent = CallTool $sessionId $Tool $ArgsJson
    $parsedResponse = ParseSseResponse $responseContent
    
    if ($parsedResponse.result) {
        $result = $parsedResponse.result.content[0].text | ConvertFrom-Json
        $result | ConvertTo-Json -Depth 10
    } elseif ($parsedResponse.error) {
        Write-Host "Error: $($parsedResponse.error.message)" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}