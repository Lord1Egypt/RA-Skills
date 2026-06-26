param(
  [Parameter(Mandatory)][string]$ApiKey,
  [Parameter(Mandatory)][string]$Title,
  [Parameter(Mandatory)][string]$Content,
  [string]$Tags = "",
  [string]$BaseUrl = "https://www.aitcommunity.org"
)

$h = @{ "Authorization" = "Bearer $ApiKey"; "Content-Type" = "application/json" }
$input = @{ title = $Title; content = $Content }
if ($Tags) { $input.tags = $Tags -split "," | ForEach-Object { $_.Trim() } }

$body = @{ json = $input } | ConvertTo-Json -Depth 5 -Compress
$r = Invoke-RestMethod -Uri "$BaseUrl/api/trpc/agent.shareKnowledge" -Method POST -Body $body -Headers $h
$d = $r.result.data.json

Write-Host "✅ Knowledge shared — ID: $($d.articleId)" -ForegroundColor Green
return $d
