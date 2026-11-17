param(
  [Parameter(Mandatory=$true)][string]$Url,
  [string]$JsRender,
  [string]$Country,
  [string]$Wait,
  [string]$WaitFor,
  [switch]$DryRun
)
if (-not $env:DATAIFY_API_TOKEN) { throw "DATAIFY_API_TOKEN is not set." }
$arguments = @("$PSScriptRoot/invoke-dataify-web-unlocker.py", "--url", $Url)
if ($JsRender) { $arguments += @("--js-render", $JsRender) }
if ($Country) { $arguments += @("--country", $Country) }
if ($Wait) { $arguments += @("--wait", $Wait) }
if ($WaitFor) { $arguments += @("--wait-for", $WaitFor) }
if ($DryRun) { $arguments += "--dry-run" }
& python3 @arguments
exit $LASTEXITCODE
