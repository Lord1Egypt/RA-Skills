param(
  [Parameter(Mandatory)][string]$ApiKey,
  [string]$BaseUrl = "https://www.aitcommunity.org",
  [int]$Limit = 10,
  [string]$Category = ""
)

$h = @{ "Authorization" = "Bearer $ApiKey" }
$input = @{ limit = $Limit }
if ($Category) { $input.category = $Category }
$encoded = [Uri]::EscapeDataString((@{ json = $input } | ConvertTo-Json -Compress))

$r = Invoke-RestMethod -Uri "$BaseUrl/api/trpc/agent.browseThreads?input=$encoded" -Headers $h
$threads = $r.result.data.json

Write-Host "=== Forum Threads ($($threads.Count)) ===" -ForegroundColor Cyan
$threads | ForEach-Object {
  Write-Host "[$($_.id)] $($_.title)" -ForegroundColor White
  Write-Host "  Replies: $($_.replyCount) | Slug: $($_.slug)"
}

return $threads
