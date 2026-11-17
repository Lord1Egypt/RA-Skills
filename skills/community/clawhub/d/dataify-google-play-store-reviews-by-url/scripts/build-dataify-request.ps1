param([Parameter(Mandatory=$true)][string]$ToolSign,[Parameter(Mandatory=$true)][string]$ValuesFile)
if (-not $env:DATAIFY_API_TOKEN) { throw "DATAIFY_API_TOKEN is not set." }
& python3 "$PSScriptRoot/build-dataify-request.py" --tool-sign $ToolSign --values-file $ValuesFile
exit $LASTEXITCODE
