# Test-only observer: latch cancellation after text appears in our scratch window.
param([string]$WindowTitle,[string]$StopFile)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName UIAutomationClient,UIAutomationTypes
$a=[Windows.Automation.AutomationElement];$s=[Windows.Automation.TreeScope]
$deadline=(Get-Date).AddSeconds(20)
while ((Get-Date) -lt $deadline) {
  $w=$a::RootElement.FindFirst($s::Children,(New-Object Windows.Automation.PropertyCondition($a::NameProperty,$WindowTitle)))
  if($w) {
    $el=$w.FindFirst($s::Descendants,(New-Object Windows.Automation.PropertyCondition($a::NameProperty,'Audit editor')))
    if($el -and $el.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).Current.Value.Length -ge 50) {
      Set-Content -LiteralPath $StopFile 'cancel during typing';exit 0
    }
  }
  Start-Sleep -Milliseconds 20
}
throw 'No long typing observed'
