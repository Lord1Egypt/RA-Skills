<#
.SYNOPSIS
    Doubao CLI Toolkit - based on opencli doubao
.DESCRIPTION
    Wrapper for opencli doubao commands with interactive usage.
    Requires Edge login at https://www.doubao.com/chat

    Usage:
        .\doubao_toolkit.ps1 status             Check login status
        .\doubao_toolkit.ps1 ask "question"      Ask Doubao
        .\doubao_toolkit.ps1 chat               Interactive chat mode
        .\doubao_toolkit.ps1 image "prompt"      Image generation (auto-download)
        .\doubao_toolkit.ps1 podcast "topic"    AI Podcast generation (auto-download)
        .\doubao_toolkit.ps1 ppt "topic"        PPT generation (auto-download)
        .\doubao_toolkit.ps1 meetings           List meetings
        .\doubao_toolkit.ps1 summary <id>       Get meeting summary
        .\doubao_toolkit.ps1 backup             Backup all conversations
        .\doubao_toolkit.ps1 batch <file.txt>   Batch questions
#>

param(
    [Parameter(Position = 0)]
    [ValidateSet('ask', 'chat', 'meetings', 'summary', 'backup', 'batch', 'status', 'image', 'podcast', 'ppt', 'help')]
    [string]$Action = 'help',

    [Parameter(Position = 1, ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

# -- Config --
$scriptDir = Split-Path $MyInvocation.MyCommand.Path -Parent
$parentDir = Split-Path $scriptDir -Parent
$OUTPUT_DIR = $parentDir + '\output\doubao'
if (-not (Test-Path $OUTPUT_DIR)) { New-Item -ItemType Directory -Path $OUTPUT_DIR -Force | Out-Null }

# -- Helpers --
function Write-Result {
    param([string]$Title, [string]$Content)
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host $Content
    Write-Host "----------------------------------------" -ForegroundColor DarkGray
}

# -- Actions --

function Invoke-Ask {
    param([string]$Question)
    if (-not $Question) {
        $Question = Read-Host 'Enter your question'
    }
    Write-Host '`n>> Asking Doubao...' -ForegroundColor Green
    $reply = opencli doubao ask "$Question" 2>$null
    if ($reply) { Write-Result -Title 'Doubao Reply' -Content $reply }
    else { Write-Host 'Ask failed' -ForegroundColor Red }
}

function Invoke-Chat {
    Write-Host '`n>> Doubao interactive mode (type exit to quit)' -ForegroundColor Green
    Write-Host '----------------------------------' -ForegroundColor DarkGray
    while ($true) {
        $q = Read-Host '`nYou'
        if ($q -eq 'exit' -or $q -eq 'quit') { break }
        $r = opencli doubao ask "$q" -f json 2>&1 | ConvertFrom-Json
        Write-Host '`nDoubao: ' -NoNewline
        Write-Host $r.Response -ForegroundColor Cyan
    }
}

function Invoke-Status {
    $raw = opencli doubao status -f json 2>$null
    if ($raw) { $s = $raw | ConvertFrom-Json; Write-Result -Title 'Doubao Connection Status' -Content ($s | Format-List | Out-String) }
    else { Write-Host 'Status fetch failed' -ForegroundColor Red }
}

function Invoke-Meetings {
    Write-Host '`n>> Fetching meeting list...' -ForegroundColor Green
    $history = opencli doubao history -f json 2>&1 | ConvertFrom-Json
    $meetings = $history | Where-Object { $_.Title -match 'meeting|Meeting|summary|transcript' }
    if ($meetings) {
        Write-Result -Title 'Meetings' -Content ($meetings | Format-Table Id, Title -AutoSize | Out-String)
    } else {
        Write-Host 'No meeting conversations found' -ForegroundColor Yellow
    }
}

function Invoke-Summary {
    param([string]$Id)
    if (-not $Id) {
        Write-Host 'Please provide a conversation ID, e.g.: summary abc123' -ForegroundColor Red
        return
    }
    Write-Host '`n>> Fetching meeting summary...' -ForegroundColor Green
    $summary = opencli doubao meeting-summary "$Id" -f json 2>&1 | ConvertFrom-Json
    Write-Result -Title 'Meeting Summary' -Content ($summary | Format-List | Out-String)

    $file = $OUTPUT_DIR + '\meeting_summary_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.md'
    $summary | ConvertTo-Json -Depth 5 | Out-File $file -Encoding utf8
    Write-Host 'Saved to: ' -NoNewline; Write-Host $file -ForegroundColor Green
}

function Invoke-Backup {
    Write-Host '`n>> Backing up Doubao conversations...' -ForegroundColor Green
    $history = opencli doubao history -f json 2>&1 | ConvertFrom-Json
    $backupFile = $OUTPUT_DIR + '\doubao_backup_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.json'

    $backup = @()
    $total = $history.Count
    $i = 0

    foreach ($item in $history) {
        $i = $i + 1
        $id = $item.Id
        if (-not $id) { continue }

        Write-Progress -Activity 'Backup' -Status ('Conversation ' + $i + '/' + $total) -PercentComplete (($i/$total)*100)
        try {
            $detail = opencli doubao detail "$id" -f json 2>&1 | ConvertFrom-Json
            $backup = $backup + @{
                Id = $id
                Title = $item.Title
                Detail = $detail
            }
        } catch {
            Write-Warning ('Skipping ' + $id + ' (fetch failed)')
        }
    }

    $backup | ConvertTo-Json -Depth 10 | Out-File $backupFile -Encoding utf8
    Write-Progress -Activity 'Backup' -Completed
    Write-Host ('Backup complete! ' + $backup.Count + ' conversations') -ForegroundColor Green
    Write-Host '  File: ' -NoNewline; Write-Host $backupFile -ForegroundColor Green
}

function Invoke-Batch {
    param([string]$FilePath)
    if (-not $FilePath -or -not (Test-Path $FilePath)) {
        Write-Host 'Please provide a question file path (one question per line)' -ForegroundColor Red
        return
    }

    $questions = Get-Content $FilePath | Where-Object { $_.Trim() -ne '' }
    $results = @()
    $i = 0

    Write-Host ('`n>> Batch processing ' + $questions.Count + ' questions...') -ForegroundColor Green

    foreach ($q in $questions) {
        $i = $i + 1
        Write-Progress -Activity 'Batch' -Status ('[' + $i + '/' + $questions.Count + '] ' + $q) -PercentComplete (($i/$questions.Count)*100)
        try {
            $r = opencli doubao ask "$q" -f json 2>&1 | ConvertFrom-Json
            $results = $results + @{ Question = $q; Response = $r.Response }
            Write-Host ('  [' + $i + '/' + $questions.Count + '] Done') -ForegroundColor DarkGreen
        } catch {
            $results = $results + @{ Question = $q; Response = '[FAIL] ' + $_.Exception.Message }
            Write-Host ('  [' + $i + '/' + $questions.Count + '] Failed') -ForegroundColor Red
        }
    }

    Write-Progress -Activity 'Batch' -Completed

    $outFile = $OUTPUT_DIR + '\batch_results_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.md'
    $md = '# Batch Results' + "`r`n"
    $md = $md + "`r`n"
    $md = $md + '| # | Question | Response |' + "`r`n"
    $md = $md + '|---|----------|----------|' + "`r`n"
    $j = 0
    while ($j -lt $results.Count) {
        $resp = $results[$j].Response -replace '\|', '\|'
        $num = $j + 1
        $trunc = $resp
        if ($trunc.Length -gt 100) { $trunc = $trunc.Substring(0, 100) + '...' }
        $md = $md + ('| ' + $num + ' | ' + $results[$j].Question + ' | ' + $trunc + ' |') + "`r`n"
        $j = $j + 1
    }
    [System.IO.File]::WriteAllText($outFile, $md, [System.Text.Encoding]::UTF8)
    Write-Host 'Batch complete! Results saved: ' -NoNewline; Write-Host $outFile -ForegroundColor Green
}

function Show-Help {
    Write-Host ''
    Write-Host '========================================' -ForegroundColor Cyan
    Write-Host '    Doubao Automation Toolkit' -ForegroundColor Yellow
    Write-Host '========================================' -ForegroundColor Cyan
    Write-Host ''
    Write-Host 'Usage:'
    Write-Host '  .\doubao_toolkit.ps1 status             Check login status'
    Write-Host '  .\doubao_toolkit.ps1 ask "question"      Ask Doubao'
    Write-Host '  .\doubao_toolkit.ps1 chat               Interactive chat mode'
    Write-Host '  .\doubao_toolkit.ps1 image "prompt"      Image generation (auto-download)'
    Write-Host '  .\doubao_toolkit.ps1 podcast "topic"    AI Podcast generation (auto-download)'
    Write-Host '  .\doubao_toolkit.ps1 ppt "topic"        PPT generation (auto-download)'
    Write-Host '  .\doubao_toolkit.ps1 meetings           List meetings'
    Write-Host '  .\doubao_toolkit.ps1 summary <id>       Get meeting summary'
    Write-Host '  .\doubao_toolkit.ps1 backup             Backup all conversations'
    Write-Host '  .\doubao_toolkit.ps1 batch <file.txt>   Batch questions'
    Write-Host ''
    Write-Host 'Prerequisites:'
    Write-Host '  Edge logged into https://www.doubao.com/chat'
    Write-Host '  opencli installed'
    Write-Host ''
}

# -- Main --
switch ($Action) {
    'ask'     { Invoke-Ask -Question ($Args -join ' ') }
    'chat'    { Invoke-Chat }
    'status'  { Invoke-Status }
    'meetings' { Invoke-Meetings }
    'summary' { Invoke-Summary -Id ($Args[0]) }
    'backup'  { Invoke-Backup }
    'batch'   { Invoke-Batch -FilePath ($Args[0]) }
    'image'   { $imgPrompt = $Args -join ' '; $imgScript = $scriptDir + '\doubao_image_gen.ps1'; & $imgScript $imgPrompt -download }
    'podcast' { $podcastText = $Args -join ' '; $podcastScript = $scriptDir + '\doubao_podcast_gen.ps1'; & $podcastScript -Text $podcastText }
    'ppt'     { $pptArg = $Args -join ' '; $pptScript = $scriptDir + '\doubao_ppt_gen.ps1'; & $pptScript -Topic $pptArg }
    default   { Show-Help }
}