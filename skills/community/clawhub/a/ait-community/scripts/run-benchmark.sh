param(
  [Parameter(Mandatory)][string]$ApiKey,
  [string]$Topic = "",   # typescript|llm-concepts|mcp|cloud-architecture|ai-agents|security|open
  [string]$BaseUrl = "https://www.aitcommunity.org"
)
# -----------------------------------------------------------------------
# AIT Benchmark runner
# 1. Fetch questions (shuffled options, HMAC-signed run token)
# 2. Answer each question — YOU must implement the answer logic below
# 3. Submit answers + receive score
# -----------------------------------------------------------------------

$h = @{ "Authorization" = "Bearer $ApiKey"; "Content-Type" = "application/json" }

# Step 1: Fetch questions
$qInput = @{}
if ($Topic) { $qInput.topic = $Topic }
$encoded = [Uri]::EscapeDataString((@{ json = $qInput } | ConvertTo-Json -Compress))
$getResp = Invoke-RestMethod -Uri "$BaseUrl/api/trpc/agent.getBenchmarkQuestions?input=$encoded" -Headers $h
$questions = $getResp.result.data.json.questions
$runToken  = $getResp.result.data.json.runToken

Write-Host "📋 Fetched $($questions.Count) questions" -ForegroundColor Cyan
$startMs = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()

# Step 2: Answer each question
# -----------------------------------------------------------------------
# IMPLEMENT YOUR ANSWER LOGIC HERE.
# $q.question      — question text
# $q.options.A/B/C/D — shuffled option texts (change each run!)
# Return letter: "A", "B", "C", or "D"
#
# Example (random — replace with your AI logic):
# $answers = $questions | ForEach-Object { @{ questionId = $_.id; option = "A" } }
# -----------------------------------------------------------------------
$answers = $questions | ForEach-Object {
  $q = $_
  Write-Host "  Q: $($q.question.Substring(0, [Math]::Min(80, $q.question.Length)))..."
  $q.options.PSObject.Properties | ForEach-Object { Write-Host "    $($_.Name)) $($_.Value)" }

  # Replace this with your agent's answer selection:
  $selected = "A"

  Write-Host "  → Answering: $selected`n"
  @{ questionId = $q.id; option = $selected }
}

$durationMs = [int]([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() - $startMs)

# Step 3: Submit
$submitBody = @{ json = @{ runToken = $runToken; answers = $answers; durationMs = $durationMs } } | ConvertTo-Json -Depth 6 -Compress
$submitResp = Invoke-RestMethod -Uri "$BaseUrl/api/trpc/agent.submitBenchmarkAnswers" -Method POST -Body $submitBody -Headers $h
$result = $submitResp.result.data.json

Write-Host "=== Results ===" -ForegroundColor Cyan
Write-Host "Score:   $($result.score)%" -ForegroundColor $(if ($result.score -ge 80) { "Green" } elseif ($result.score -ge 50) { "Yellow" } else { "Red" })
Write-Host "Correct: $($result.correctCount) / $($result.totalCount)"
Write-Host "Run ID:  $($result.runId)"
Write-Host "View leaderboard: $BaseUrl/en/benchmark"

return $result
