# Cavepony hook installer for Windows (PowerShell)

Write-Host "🏍️ Installing Cavepony hooks for Claude Code..." -ForegroundColor Green

# Claude Code config directory on Windows
$ConfigDir = "$env:APPDATA\Claude Code"
$HooksDir = Join-Path $ConfigDir "hooks"
$CaveponyHook = Join-Path $HooksDir "cavepony.js"

# Create hooks directory if it doesn't exist
if (-Not (Test-Path $HooksDir)) {
    New-Item -ItemType Directory -Path $HooksDir -Force
}

# Check if cavepony hook already exists
if (Test-Path $CaveponyHook) {
    $response = Read-Host "⚠️  Cavepony hook already exists. Overwrite? (y/N)"
    if ($response -notmatch '^[Yy]$') {
        Write-Host "❌ Aborting." -ForegroundColor Red
        exit 1
    }
}

# Create the hook file
$HookContent = @'
// Cavepony hook for Claude Code
// Auto-activates cavepony mode on session start

module.exports = {
  name: 'Cavepony',
  description: 'Auto-activate cavepony mode on session start',
  
  onSessionStart: async (context) => {
    // Add cavepony rules to the session
    await context.addSystemPrompt(`
Terse like cavepony. Technical substance exact. Only fluff die.
Drop: articles, filler (just/really/basically), pleasantries, hedging.
Fragments OK. Short synonyms. Code unchanged.
Pattern: [thing] [action] [reason]. [next step].
Pony substitutions: human/people -> pony/ponies, man/woman -> stallion/mare, boy/girl -> colt/filly, child/children -> foal/foals, hand/foot -> hoof/hooves, hey -> hay, hell/heck -> hay, Christmas -> Heartswarming, New York -> Manehattan, Philadelphia -> Fillydelphia, etc.
ACTIVE EVERY RESPONSE. No revert after many turns. No filler drift.
Code/commits/PRs: normal. Off: "stop cavepony" / "normal mode".
    `);
    
    // Set status line indicator
    context.setStatusLine('[CAVEPONY]');
    
    console.log('🏍️ Cavepony mode activated!');
  }
};
'@

Set-Content -Path $CaveponyHook -Value $HookContent -Encoding UTF8

Write-Host "✅ Cavepony hook installed at: $CaveponyHook" -ForegroundColor Green
Write-Host ""
Write-Host "To enable cavepony in Claude Code:" -ForegroundColor Yellow
Write-Host "1. Restart Claude Code"
Write-Host "2. Check status line shows [CAVEPONY]"
Write-Host ""
Write-Host "Commands:" -ForegroundColor Yellow
Write-Host "  /cavepony pony    - Activate pony mode (with substitutions)"
Write-Host "  /cavepony full    - Standard compression"
Write-Host "  /cavepony lite    - Light compression"
Write-Host "  /cavepony ultra   - Maximum compression"
Write-Host "  /normal           - Return to normal mode"
Write-Host ""
Write-Host "🐴 Happy hoofing!" -ForegroundColor Cyan