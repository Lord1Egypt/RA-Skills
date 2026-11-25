<#
.SYNOPSIS
  规范化 Windows 脚本/文本的编码与行尾，避免 .bat 乱码与 PowerShell 中文乱码。

.DESCRIPTION
  - .bat / .cmd  -> 纯 ASCII + CRLF（内容里不得含非 ASCII 字符）
  - .ps1 / .txt  -> UTF-8 带 BOM + CRLF
  - 其他文件不动

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File normalize-encoding.ps1 -Directory "D:\dist\FTA Studio"
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$Directory
)

$ErrorActionPreference = 'Stop'
$dir = (Resolve-Path $Directory).Path
$report = @()

function Convert-LineEndings([string]$text) {
  $t = $text
  $t = $t.TrimStart([char]0xFEFF)
  $t = $t -replace "`r`n", "`n" -replace "`r", "`n"
  $t = $t -replace "`n", "`r`n"
  if (-not $t.EndsWith("`r`n")) { $t += "`r`n" }
  return $t
}

# ---------- .bat / .cmd : ASCII + CRLF ----------
Get-ChildItem $dir -Recurse -File -Include '*.bat', '*.cmd' | ForEach-Object {
  $t = Convert-LineEndings ([IO.File]::ReadAllText($_.FullName))
  $bad = @($t.ToCharArray() | Where-Object { [int]$_ -gt 127 })
  [IO.File]::WriteAllText($_.FullName, $t, (New-Object System.Text.ASCIIEncoding))
  $report += [pscustomobject]@{
    File     = $_.Name
    Encoding = if ($bad.Count -eq 0) { 'ascii' } else { "ascii (dropped $($bad.Count) non-ASCII chars!)" }
  }
  if ($bad.Count -gt 0) {
    Write-Warning "$($_.Name) 含 $($bad.Count) 个非 ASCII 字符，已被丢弃。请改用英文文案。"
  }
}

# ---------- .ps1 / .txt : UTF-8 BOM + CRLF ----------
Get-ChildItem $dir -Recurse -File -Include '*.ps1', '*.txt' | ForEach-Object {
  $t = Convert-LineEndings ([IO.File]::ReadAllText($_.FullName))
  [IO.File]::WriteAllText($_.FullName, $t, (New-Object System.Text.UTF8Encoding($true)))
  $report += [pscustomobject]@{ File = $_.Name; Encoding = 'utf8-bom' }
}

# ---------- 校验 ----------
foreach ($f in (Get-ChildItem $dir -Recurse -File -Include '*.bat', '*.cmd')) {
  $b = [IO.File]::ReadAllBytes($f.FullName)
  $nonAscii = @($b | Where-Object { $_ -gt 127 }).Count
  $crlf = 0; $loneLF = 0
  for ($i = 0; $i -lt $b.Length; $i++) {
    if ($b[$i] -eq 13 -and $i + 1 -lt $b.Length -and $b[$i + 1] -eq 10) { $crlf++ }
    elseif ($b[$i] -eq 10 -and ($i -eq 0 -or $b[$i - 1] -ne 13)) { $loneLF++ }
  }
  if ($nonAscii -gt 0 -or $loneLF -gt 0) {
    throw "编码校验失败: $($f.Name) nonAscii=$nonAscii loneLF=$loneLF"
  }
}

$report | Format-Table -AutoSize | Out-String | Write-Host
Write-Host "编码规范化完成: $dir"
