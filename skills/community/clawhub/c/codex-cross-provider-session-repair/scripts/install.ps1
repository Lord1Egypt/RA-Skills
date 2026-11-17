[CmdletBinding()]
param(
    [string]$Destination = (Join-Path ([Environment]::GetFolderPath('UserProfile')) '.agents\skills')
)

$ErrorActionPreference = 'Stop'
$source = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$name = Split-Path $source -Leaf
$root = [IO.Path]::GetFullPath($Destination)
$target = Join-Path $root $name

if ([IO.Path]::GetFullPath($target).TrimEnd('\') -eq $source.TrimEnd('\')) {
    throw 'Destination is the source checkout; install from a separate clone or package.'
}

New-Item -ItemType Directory -Force -Path $root | Out-Null
if (Test-Path -LiteralPath $target) {
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    Move-Item -LiteralPath $target -Destination "$target.bak-$stamp"
}
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -LiteralPath (Join-Path $source '*') -Destination $target -Recurse -Force
Write-Output "Installed $name from $source to $target"
