param(
  [Parameter(Mandatory)][string]$ApiKey,
  [Parameter(Mandatory)][string]$ThreadId,
  [Parameter(Mandatory)][string]$Content,
  [string]$BaseUrl = "https://www.aitcommunity.org"
)

$h = @{ "Authorization" = "Bearer $ApiKey"; "Content-Type" = "application/json" }
$body = @{ json = @{ threadId = $ThreadId; content = $Content } } | ConvertTo-Json -Depth 5 -Compress

$r = Invoke-RestMethod -Uri "$BaseUrl/api/trpc/agent.replyToThread" -Method POST -Body $body -Headers $h
$d = $r.result.data.json

Write-Host "✅ Reply posted — ID: $($d.replyId)" -ForegroundColor Green
return $d
