param([switch]$Once)
$ErrorActionPreference = 'SilentlyContinue'
try { [Console]::OutputEncoding = [Text.Encoding]::UTF8 } catch { }
$DIR = 'D:\Tools\mylike-fav-import'
$Q = Join-Path $DIR 'douyin-queue'
$STATE = Join-Path $Q 'state.json'
$LOCK = Join-Path $Q '.run.lock'
$LOG = Join-Path $DIR 'log.csv'
$ROUNDS = Join-Path $DIR 'rounds.jsonl'
$PER_DAY = 600

function Show-Bar([int]$fill, [int]$len) {
  $f = [Math]::Min([Math]::Max($fill, 0), $len)
  return ('#' * $f) + ('-' * ($len - $f))
}

function Render {
  if (-not (Test-Path $STATE)) { Write-Host '找不到 state.json：' $STATE -ForegroundColor Red; return }
  try { $st = Get-Content $STATE -Raw -Encoding UTF8 | ConvertFrom-Json } catch { Write-Host 'state.json 读取失败（可能正在写入），稍后刷新' -ForegroundColor Yellow; return }

  $total = 0; $done = 0; $doneFolders = 0; $failed = 0
  foreach ($f in $st.folders) {
    $total += [int]$f.total
    $done += [int]$f.cursor
    $failed += [int]$f.failed
    if ($f.status -eq 'done') { $doneFolders++ }
  }
  $rem = $total - $done
  $pct = if ($total -gt 0) { [Math]::Round(100.0 * $done / $total, 2) } else { 0 }

  $running = $false; $runPid = 0; $runStart = $null
  if (Test-Path $LOCK) {
    try {
      $j = Get-Content $LOCK -Raw -Encoding UTF8 | ConvertFrom-Json
      if (Get-Process -Id ([int]$j.pid) -ErrorAction SilentlyContinue) {
        $running = $true; $runPid = [int]$j.pid
        $runStart = [DateTimeOffset]::FromUnixTimeMilliseconds([int64]$j.ts).LocalDateTime
      }
    } catch { }
  }

  Cls
  Write-Host ''
  Write-Host '  抖音收藏夹批量入夹 - 进度看板' -ForegroundColor Cyan
  if ($Once) {
    Write-Host ('  ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + '   单次输出') -ForegroundColor DarkGray
  } else {
    Write-Host ('  ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + '   每 5 秒自动刷新，按 Ctrl+C 退出') -ForegroundColor DarkGray
  }
  Write-Host ''

  if ($running) {
    $elapsed = [int]((Get-Date) - $runStart).TotalMinutes
    Write-Host ('  状态: 正在执行   进程 PID ' + $runPid + '   已运行 ' + $elapsed + ' 分钟') -ForegroundColor Green
  } else {
    Write-Host '  状态: 空闲（每天 09:00 / 15:00 / 21:00 自动开跑）' -ForegroundColor Yellow
  }
  Write-Host ''
  Write-Host ('  [' + (Show-Bar ([int](40.0 * $done / [Math]::Max($total, 1))) 40) + ']  ' + $pct + '%')
  Write-Host ''
  Write-Host ('  已入夹  ' + $done + ' / ' + $total + ' 条') -ForegroundColor White
  Write-Host ('  剩余    ' + $rem + ' 条   已完成收藏夹 ' + $doneFolders + ' / ' + $st.folders.Count) -ForegroundColor White
  Write-Host ('  失败    ' + $failed + ' 条') -ForegroundColor $(if ($failed -gt 0) { 'Red' } else { 'DarkGray' })

  $days = [int][Math]::Ceiling($rem / [double]$PER_DAY)
  $eta = (Get-Date).Date.AddDays($days).ToString('yyyy-MM-dd')
  Write-Host ('  节奏    每天 ' + $PER_DAY + ' 条（09:00 / 15:00 / 21:00 各 200）   预计完成 ' + $eta + '（还需 ' + $days + ' 天）')
  Write-Host ''

  $cur = $st.folders | Where-Object { [int]$_.cursor -lt [int]$_.total } | Select-Object -First 1
  if ($cur) {
    Write-Host '  当前收藏夹' -ForegroundColor Cyan
    Write-Host ('    ' + $cur.name + '   ' + $cur.cursor + ' / ' + $cur.total + '   [' + (Show-Bar ([int](20.0 * [int]$cur.cursor / [Math]::Max([int]$cur.total, 1))) 20) + ']')
    $next = $st.folders | Where-Object { [int]$_.cursor -lt [int]$_.total } | Select-Object -Skip 1 -First 2
    foreach ($n in $next) { Write-Host ('    待跑: ' + $n.name + '   ' + $n.cursor + ' / ' + $n.total) -ForegroundColor DarkGray }
  }
  Write-Host ''

  Write-Host '  最近入夹' -ForegroundColor Cyan
  if (Test-Path $LOG) {
    $head = Get-Content $LOG -TotalCount 1 -Encoding UTF8
    $tail = Get-Content $LOG -Tail 4 -Encoding UTF8
    foreach ($row in (ConvertFrom-Csv -InputObject $tail -Header @($head -split ','))) {
      $t = ''
      try { $t = ([DateTime]$row.at).ToLocalTime().ToString('HH:mm:ss') } catch { }
      $ok = ($row.verified -eq 'yes')
      $mark = if ($ok) { 'OK ' } else { 'ERR' }
      $title = $row.title
      if ($title.Length -gt 22) { $title = $title.Substring(0, 22) + '…' }
      $line = '    ' + $mark + ' ' + $t + '  ' + $row.folder + '  ' + $title
      if ($ok) { Write-Host $line -ForegroundColor Gray } else { Write-Host ($line + '  [' + $row.note + ']') -ForegroundColor Red }
    }
  } else {
    Write-Host '    暂无日志' -ForegroundColor DarkGray
  }

  if (Test-Path $ROUNDS) {
    try { $r = Get-Content $ROUNDS -Tail 1 -Encoding UTF8 | ConvertFrom-Json } catch { $r = $null }
    if ($r) {
      $rt = ''
      try { $rt = ([DateTime]$r.started).ToLocalTime().ToString('MM-dd HH:mm') } catch { $rt = $r.started }
      Write-Host ''
      Write-Host ('  上一轮  ' + $rt + '   成功 ' + $r.ok + ' 条，失败 ' + $r.failed + ' 条') -ForegroundColor DarkGray
    }
  }
  Write-Host ''
}

if ($Once) {
  $running = $false
  Render
} else {
  while ($true) { Render; Start-Sleep -Seconds 5 }
}
