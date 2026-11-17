# Export a DOCX to PDF through Word, then kill Word.
# Word 2007-2019 sometimes throws "The remote procedure call failed. (0x800706BE)"
# from Close()/Quit() *after* a successful export, so the script exports, waits,
# and force-stops WINWORD instead of calling Close().
#
#   powershell -File export_pdf.ps1 -Source report.docx -Pdf report.pdf

param(
    [Parameter(Mandatory = $true)][string]$Source,
    [Parameter(Mandatory = $true)][string]$Pdf
)

$src = (Resolve-Path $Source).Path
$pdf = [System.IO.Path]::GetFullPath($Pdf)
if (Test-Path $pdf) { Remove-Item $pdf -Force }

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($src, $false, $true)
    $doc.ExportAsFixedFormat($pdf, 17)   # 17 = wdExportFormatPDF
    Start-Sleep -Milliseconds 800
} finally {
    Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force
}

if (Test-Path $pdf) {
    "exported: {0} ({1} bytes)" -f $pdf, (Get-Item $pdf).Length
} else {
    Write-Error "export failed: $pdf"
    exit 1
}
