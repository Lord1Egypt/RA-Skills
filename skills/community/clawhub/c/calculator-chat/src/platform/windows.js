const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const getBaseDir = () => {
  if (require.main && require.main.filename) {
    return path.dirname(require.main.filename);
  }
  return process.cwd();
};

async function launchCalculator() {
}

async function typeNumber(number) {
  if (!number) {
    throw new Error('Number parameter is required');
  }

  const baseDir = getBaseDir();
  const scriptPath = path.join(baseDir, 'temp_calc.ps1');
  const psScript = `
param($Num)

Add-Type -AssemblyName System.Windows.Forms

# Step 1: Check if Calculator is running
$calc = Get-Process -Name "CalculatorApp" -ErrorAction SilentlyContinue

# Step 2: If not running, start it
if (-not $calc) {
    Start-Process calc.exe -WindowStyle Normal
    Start-Sleep -Seconds 3
}

# Step 3: Find and activate Calculator window
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@

$hwnd = [Win32]::FindWindow("ApplicationFrameWindow", "Calculator")
if ($hwnd -eq [IntPtr]::Zero) {
    $hwnd = [Win32]::FindWindow("CalcFrame", "Calculator")
}
if ($hwnd -eq [IntPtr]::Zero) {
    $hwnd = [Win32]::FindWindow($null, "Calculator")
}

# Step 4: Activate to foreground
if ($hwnd -ne [IntPtr]::Zero) {
    [Win32]::ShowWindow($hwnd, 9) | Out-Null
    Start-Sleep -Milliseconds 100
    [Win32]::SetForegroundWindow($hwnd) | Out-Null
    Start-Sleep -Milliseconds 300
}

# Step 5: Send number
$shell = New-Object -ComObject WScript.Shell
$shell.AppActivate("Calculator")
Start-Sleep -Milliseconds 200
$shell.SendKeys("{ESC}")
Start-Sleep -Milliseconds 100
$shell.SendKeys($Num)
`;

  fs.writeFileSync(scriptPath, psScript, 'utf8');
  
  try {
    execSync(`powershell -ExecutionPolicy Bypass -File "${scriptPath}" -Num "${number}"`, { 
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe']
    });
  } catch (error) {
    throw error;
  }
  
  if (fs.existsSync(scriptPath)) {
    fs.unlinkSync(scriptPath);
  }
}

module.exports = { launchCalculator, typeNumber };
