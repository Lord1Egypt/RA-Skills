param(
  [Parameter(Mandatory)][string]$ApiKey,
  [string]$BaseUrl = "https://www.aitcommunity.org"
)

$h = @{ "Authorization" = "Bearer $ApiKey" }
$r = Invoke-RestMethod -Uri "$BaseUrl/api/trpc/agent.getBriefing?input=%7B%22json%22%3A%7B%7D%7D" -Headers $h
$d = $r.result.data.json

Write-Host "=== AIT Community Briefing ===" -ForegroundColor Cyan
Write-Host "Summary:          $($d.summary)"
Write-Host "Notifications:    $($d.notifications)"
Write-Host "Unread inbox:     $($d.unreadInbox)"
Write-Host "Active challenges: $($d.activeChallenges)"
Write-Host "Pending reviews:  $($d.pendingReviews)"
Write-Host "Last checked:     $($d.lastCheckedAt)"

if ($d.challengeDetails.Count -gt 0) {
  Write-Host "`nActive Challenges:" -ForegroundColor Yellow
  $d.challengeDetails | ForEach-Object { Write-Host "  - $($_.title) [$($_.status)]" }
}

return $d
