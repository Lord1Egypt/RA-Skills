[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Technique,
    [Parameter(Mandatory = $true)][string]$Subject,
    [string]$Direction = "screen-right",
    [string]$Speed = "slow, constant",
    [string]$Duration = "5 seconds",
    [string]$ShotSize = "medium shot",
    [string]$Angle = "eye level",
    [string]$Lens = "50mm, shallow depth of field",
    [string]$Composition = "rule of thirds",
    [string]$Light = "soft directional light",
    [string]$Continuity = "same wardrobe and props; consistent screen direction",
    [string]$Negative = "no cuts, no text, no morphing, no extra limbs, no camera shake"
)

$prompt = @(
    "$ShotSize, $Angle, $Lens, $Composition.",
    "Camera: $Technique $Direction at $Speed over $Duration.",
    "Subject: $Subject.",
    "Light: $Light.",
    "Continuity: $Continuity.",
    "Negative: $Negative."
) -join "`n"

[pscustomobject]@{
    technique = $Technique
    prompt = $prompt
} | ConvertTo-Json -Compress
