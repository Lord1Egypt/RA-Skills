# Desktop Pilot - Windows "agent is working" overlay (PowerShell 5.1+, WPF, no installs).
# Started detached by `desktop.sh overlay start`. Two topmost windows on the primary screen:
#   1. a glow around the screen edges that lets every click pass through (never blocks the user's work),
#   2. a small pill with a status text and a Stop button (never takes keyboard focus).
# Optional input lock (lock.flag present): a low-level keyboard+mouse hook swallows the user's PHYSICAL input
# (events flagged as injected - i.e. the agent's own SendInput/mouse_event - always pass). Safety nets:
# mouse moves are never blocked and clicks on the pill (Stop) always work; holding Esc 1.5 s releases everything;
# the lock lapses 8 s after the agent's last action and never lasts more than 10 minutes in a row;
# Ctrl+Alt+Del cannot be intercepted by Windows; if this process dies the OS removes the hooks.
# State lives in -Dir:  text.txt (status text), beat (heartbeat), stop.flag (user pressed Stop),
#                       lock.flag (input lock wanted), lock.state (engaged|released),
#                       quit.flag (close request), pid, log.txt
# It closes itself when the heartbeat goes stale (agent crashed or finished), so it can never get stuck.
param(
  [Parameter(Mandatory = $true)][string]$Dir,
  [int]$IdleSeconds = 120,
  [int]$MaxMinutes = 30,
  [switch]$VisibleInCapture,  # keep the overlay in screenshots/recordings (demos); default: hidden from captures
  [int]$LockIdleSeconds = 8,  # input lock releases itself this long after the agent's last action
  [int]$LockMaxMinutes = 10,  # input lock never stays engaged longer than this in one go
  [switch]$SelfTest           # run the lock decision tests and exit (no UI)
)
$ErrorActionPreference = 'Stop'
function Log($m) { try { Add-Content -Path (Join-Path $Dir 'log.txt') -Value ("{0:HH:mm:ss} {1}" -f (Get-Date), $m) } catch {} }
try {
  Add-Type -AssemblyName PresentationFramework, PresentationCore, WindowsBase
  Add-Type @"
using System; using System.Runtime.InteropServices;
using System.Diagnostics;
public static class OvNative {
  [DllImport("user32.dll")] public static extern int GetWindowLong(IntPtr h, int i);
  [DllImport("user32.dll")] public static extern int SetWindowLong(IntPtr h, int i, int v);
  [DllImport("user32.dll")] public static extern bool SetWindowDisplayAffinity(IntPtr h, uint a);
}
// Input lock. Callbacks are compiled C# (no PowerShell in the hook path) and return immediately.
public static class OvLock {
  delegate IntPtr HookProc(int nCode, IntPtr wParam, IntPtr lParam);
  [DllImport("user32.dll", SetLastError = true)] static extern IntPtr SetWindowsHookEx(int id, HookProc fn, IntPtr mod, uint tid);
  [DllImport("user32.dll")] static extern bool UnhookWindowsHookEx(IntPtr h);
  [DllImport("user32.dll")] static extern IntPtr CallNextHookEx(IntPtr h, int n, IntPtr w, IntPtr l);
  [DllImport("kernel32.dll")] static extern IntPtr GetModuleHandle(string name);
  [DllImport("user32.dll")] static extern bool GetWindowRect(IntPtr h, out RECT r);
  [StructLayout(LayoutKind.Sequential)] struct RECT { public int L, T, R, B; }
  static HookProc kProc = KbProc, mProc = MsProc;   // keep delegates alive for the lifetime of the hooks
  static IntPtr kHook = IntPtr.Zero, mHook = IntPtr.Zero, pillHwnd = IntPtr.Zero;
  static int pl, pt, pr, pb; static int escDown = 0;
  public static volatile bool Active;      // true while physical input is being swallowed
  public static volatile bool Emergency;   // Esc held 1.5 s
  public static int BlockedKeys, BlockedClicks, SeenKeys, SeenMouse, SeenPhysicalKeys, SeenPhysicalMouse;
  public static bool Installed { get { return kHook != IntPtr.Zero; } }
  public static bool Install() {
    if (Installed) return true;
    IntPtr mod = GetModuleHandle(Process.GetCurrentProcess().MainModule.ModuleName);
    kHook = SetWindowsHookEx(13, kProc, mod, 0); mHook = SetWindowsHookEx(14, mProc, mod, 0);
    if (kHook == IntPtr.Zero || mHook == IntPtr.Zero) { Uninstall(); return false; }
    return true;
  }
  public static void Uninstall() {
    Active = false;
    if (kHook != IntPtr.Zero) UnhookWindowsHookEx(kHook);
    if (mHook != IntPtr.Zero) UnhookWindowsHookEx(mHook);
    kHook = IntPtr.Zero; mHook = IntPtr.Zero;
  }
  public static void SetPill(IntPtr h) { pillHwnd = h; }
  public static void RefreshPill() { RECT r; if (pillHwnd != IntPtr.Zero && GetWindowRect(pillHwnd, out r)) { pl = r.L; pt = r.T; pr = r.R; pb = r.B; } }
  public static void SetPillRect(int l, int t, int r, int b) { pl = l; pt = t; pr = r; pb = b; }
  // true = swallow the event. Pure functions so they can be unit-tested (-SelfTest).
  public static bool DecideKey(int flags, int vk, bool isDown, int nowMs) {
    if (!Active) return false;
    if ((flags & 0x10) != 0) return false;                       // LLKHF_INJECTED: the agent -> let it through
    if (vk == 0x1B) {                                            // Esc held 1.5 s = emergency release
      if (isDown) { if (escDown == 0) escDown = nowMs | 1; else if (unchecked(nowMs - escDown) >= 1500) Emergency = true; }
      else escDown = 0;
    }
    BlockedKeys++; return true;
  }
  public static bool DecideMouse(int msg, int x, int y, int flags) {
    if (!Active) return false;
    if ((flags & 1) != 0) return false;                          // LLMHF_INJECTED: the agent -> let it through
    if (msg == 0x0200) return false;                             // WM_MOUSEMOVE is never blocked: the user can always reach Stop
    if (x >= pl && x < pr && y >= pt && y < pb) return false;    // clicks on the pill (Stop button) always work
    BlockedClicks++; return true;                                // buttons, wheel
  }
  static IntPtr KbProc(int n, IntPtr w, IntPtr l) {
    if (n >= 0) {
      int fl = Marshal.ReadInt32(l, 8); SeenKeys++; if ((fl & 0x10) == 0) SeenPhysicalKeys++;
      if (DecideKey(fl, Marshal.ReadInt32(l, 0), (int)w == 0x100 || (int)w == 0x104, Environment.TickCount)) return (IntPtr)1;
    }
    return CallNextHookEx(kHook, n, w, l);
  }
  static IntPtr MsProc(int n, IntPtr w, IntPtr l) {
    if (n >= 0) {
      int fl = Marshal.ReadInt32(l, 12); SeenMouse++; if ((fl & 1) == 0) SeenPhysicalMouse++;
      if (DecideMouse((int)w, Marshal.ReadInt32(l, 0), Marshal.ReadInt32(l, 4), fl)) return (IntPtr)1;
    }
    return CallNextHookEx(mHook, n, w, l);
  }
  public static void ResetEmergency() { Emergency = false; escDown = 0; }
}
"@
  if ($SelfTest) {
    $fail = @(); function T($name, $cond) { if (-not $cond) { $script:fail += $name } }
    [OvLock]::Active = $false;  T 'inactive passes keys' (-not [OvLock]::DecideKey(0, 65, $true, 1000))
    [OvLock]::Active = $true;   [OvLock]::SetPillRect(100, 900, 500, 960)
    T 'physical key blocked' ([OvLock]::DecideKey(0, 65, $true, 1000))
    T 'injected key passes' (-not [OvLock]::DecideKey(0x10, 65, $true, 1000))
    T 'physical click blocked' ([OvLock]::DecideMouse(0x201, 50, 50, 0))
    T 'physical wheel blocked' ([OvLock]::DecideMouse(0x20A, 50, 50, 0))
    T 'injected click passes' (-not [OvLock]::DecideMouse(0x201, 50, 50, 1))
    T 'mouse move never blocked' (-not [OvLock]::DecideMouse(0x200, 50, 50, 0))
    T 'click on pill passes' (-not [OvLock]::DecideMouse(0x201, 300, 930, 0))
    T 'click just outside pill blocked' ([OvLock]::DecideMouse(0x201, 300, 961, 0))
    [OvLock]::ResetEmergency()
    [void][OvLock]::DecideKey(0, 0x1B, $true, 5000); [void][OvLock]::DecideKey(0, 0x1B, $true, 6000)
    T 'Esc short press is no emergency' (-not [OvLock]::Emergency)
    [void][OvLock]::DecideKey(0, 0x1B, $false, 6100)
    [void][OvLock]::DecideKey(0, 0x1B, $true, 7000); [void][OvLock]::DecideKey(0, 0x1B, $true, 8600)
    T 'Esc held 1.5 s is emergency' ([OvLock]::Emergency)
    [OvLock]::ResetEmergency(); [OvLock]::Active = $false
    $ok = [OvLock]::Install(); T 'hooks install' $ok
    T 'hooks report installed' ([OvLock]::Installed)
    [OvLock]::Uninstall(); T 'hooks uninstall' (-not [OvLock]::Installed)
    if ($fail.Count) { Write-Output ("SELFTEST FAIL: " + ($fail -join '; ')); exit 1 } else { Write-Output 'SELFTEST PASS (11 decisions + hook install/uninstall)'; exit 0 }
  }
  Set-Content -Path (Join-Path $Dir 'pid') -Value $PID -Encoding ascii
  $textFile = Join-Path $Dir 'text.txt'; $beatFile = Join-Path $Dir 'beat'
  $stopFile = Join-Path $Dir 'stop.flag'; $quitFile = Join-Path $Dir 'quit.flag'
  $lockFile = Join-Path $Dir 'lock.flag'; $lockState = Join-Path $Dir 'lock.state'
  $started = Get-Date

  function Color($a, $r, $g, $b) { [Windows.Media.Color]::FromArgb($a, $r, $g, $b) }
  function Brush($c) { New-Object Windows.Media.SolidColorBrush $c }
  $cyan = Color 255 0 229 255; $blue = Color 255 45 123 255; $violet = Color 255 139 92 246

  # Color cycle cyan -> blue -> violet -> cyan, shifted per element so the glow looks like it flows.
  function New-CycleAnimation($offsetSec, $alpha) {
    $k = New-Object Windows.Media.Animation.ColorAnimationUsingKeyFrames
    $k.Duration = (New-Object Windows.Duration ([TimeSpan]::FromSeconds(6)))
    $k.RepeatBehavior = [Windows.Media.Animation.RepeatBehavior]::Forever
    $k.BeginTime = [TimeSpan]::FromSeconds(-$offsetSec)
    $cols = @($cyan, $blue, $violet, $cyan)
    for ($i = 0; $i -lt 4; $i++) {
      $c = $cols[$i]; $c = Color $alpha $c.R $c.G $c.B
      $kt = [Windows.Media.Animation.KeyTime]::FromTimeSpan([TimeSpan]::FromSeconds($i * 2))
      [void]$k.KeyFrames.Add((New-Object Windows.Media.Animation.LinearColorKeyFrame -ArgumentList $c, $kt))
    }
    $k
  }
  function Set-ExStyle($win, [bool]$clickThrough, [bool]$hideFromCapture) {
    $h = (New-Object Windows.Interop.WindowInteropHelper $win).EnsureHandle()
    $ex = [OvNative]::GetWindowLong($h, -20)
    $ex = $ex -bor 0x08000000 -bor 0x00000080          # NOACTIVATE | TOOLWINDOW (no focus, no Alt-Tab)
    if ($clickThrough) { $ex = $ex -bor 0x00000020 -bor 0x00080000 }   # TRANSPARENT | LAYERED
    [void][OvNative]::SetWindowLong($h, -20, $ex)
    if ($hideFromCapture) { [void][OvNative]::SetWindowDisplayAffinity($h, 0x11) }   # EXCLUDEFROMCAPTURE
  }
  function New-BaseWindow {
    $w = New-Object Windows.Window
    $w.WindowStyle = 'None'; $w.AllowsTransparency = $true; $w.Background = [Windows.Media.Brushes]::Transparent
    $w.Topmost = $true; $w.ShowInTaskbar = $false; $w.ShowActivated = $false; $w.ResizeMode = 'NoResize'
    $w
  }

  # ---------- 1. glow (click-through) ----------
  $sw = [Windows.SystemParameters]::PrimaryScreenWidth; $sh = [Windows.SystemParameters]::PrimaryScreenHeight
  $glow = New-BaseWindow
  $glow.Title = 'Desktop Pilot glow'; $glow.Left = 0; $glow.Top = 0; $glow.Width = $sw; $glow.Height = $sh
  $grid = New-Object Windows.Controls.Grid; $grid.IsHitTestVisible = $false
  $thick = 120.0
  function Add-Edge($ha, $va, $w, $h, $x0, $y0, $x1, $y1, $offset) {
    $r = New-Object Windows.Shapes.Rectangle
    $r.HorizontalAlignment = $ha; $r.VerticalAlignment = $va; $r.IsHitTestVisible = $false
    if ($w -gt 0) { $r.Width = $w }; if ($h -gt 0) { $r.Height = $h }
    $b = New-Object Windows.Media.LinearGradientBrush
    $b.StartPoint = New-Object Windows.Point $x0, $y0; $b.EndPoint = New-Object Windows.Point $x1, $y1
    $s0 = New-Object Windows.Media.GradientStop -ArgumentList (Color 150 0 229 255), 0.0
    $s1 = New-Object Windows.Media.GradientStop -ArgumentList (Color 0 0 229 255), 1.0
    [void]$b.GradientStops.Add($s0); [void]$b.GradientStops.Add($s1)
    $r.Fill = $b
    [void]$grid.Children.Add($r)
    $s0.BeginAnimation([Windows.Media.GradientStop]::ColorProperty, (New-CycleAnimation $offset 150))
    $s1.BeginAnimation([Windows.Media.GradientStop]::ColorProperty, (New-CycleAnimation $offset 0))
  }
  Add-Edge 'Stretch' 'Top'    0 $thick 0.5 0 0.5 1 0
  Add-Edge 'Right'   'Stretch' $thick 0 1 0.5 0 0.5 1.5
  Add-Edge 'Stretch' 'Bottom' 0 $thick 0.5 1 0.5 0 3
  Add-Edge 'Left'    'Stretch' $thick 0 0 0.5 1 0.5 4.5
  # thin bright line right at the screen edge, with its own halo
  $line = New-Object Windows.Controls.Border
  $line.BorderThickness = New-Object Windows.Thickness 3; $line.IsHitTestVisible = $false
  $line.BorderBrush = Brush (Color 230 0 229 255)
  $fx = New-Object Windows.Media.Effects.DropShadowEffect; $fx.BlurRadius = 40; $fx.ShadowDepth = 0; $fx.Color = (Color 255 0 229 255); $fx.Opacity = 0.9
  $line.Effect = $fx
  [void]$grid.Children.Add($line)
  $line.BorderBrush.BeginAnimation([Windows.Media.SolidColorBrush]::ColorProperty, (New-CycleAnimation 0 230))
  $pulse = New-Object Windows.Media.Animation.DoubleAnimation -ArgumentList 0.6, 1.0, (New-Object Windows.Duration ([TimeSpan]::FromSeconds(1.6)))
  $pulse.AutoReverse = $true; $pulse.RepeatBehavior = [Windows.Media.Animation.RepeatBehavior]::Forever
  $grid.BeginAnimation([Windows.UIElement]::OpacityProperty, $pulse)
  $glow.Content = $grid

  # ---------- 2. pill with status + Stop (clickable, never focused) ----------
  $pill = New-BaseWindow
  $pill.Title = 'Desktop Pilot status'; $pill.SizeToContent = 'WidthAndHeight'
  $root = New-Object Windows.Controls.Border
  $root.CornerRadius = New-Object Windows.CornerRadius 24
  $root.Background = Brush (Color 238 12 38 42)
  $root.BorderBrush = Brush (Color 110 0 229 255); $root.BorderThickness = New-Object Windows.Thickness 1
  $root.Padding = New-Object Windows.Thickness 16, 8, 8, 8; $root.Margin = New-Object Windows.Thickness 24
  $sfx = New-Object Windows.Media.Effects.DropShadowEffect; $sfx.BlurRadius = 24; $sfx.ShadowDepth = 4; $sfx.Opacity = 0.45
  $root.Effect = $sfx
  $sp = New-Object Windows.Controls.StackPanel; $sp.Orientation = 'Horizontal'
  $dot = New-Object Windows.Shapes.Ellipse; $dot.Width = 10; $dot.Height = 10
  $dot.Fill = Brush $cyan; $dot.VerticalAlignment = 'Center'; $dot.Margin = New-Object Windows.Thickness 0, 0, 10, 0
  $dotAnim = New-Object Windows.Media.Animation.DoubleAnimation -ArgumentList 0.25, 1.0, (New-Object Windows.Duration ([TimeSpan]::FromSeconds(0.9)))
  $dotAnim.AutoReverse = $true; $dotAnim.RepeatBehavior = [Windows.Media.Animation.RepeatBehavior]::Forever
  $dot.BeginAnimation([Windows.UIElement]::OpacityProperty, $dotAnim)
  $label = New-Object Windows.Controls.TextBlock
  $label.FontFamily = 'Segoe UI'; $label.FontSize = 14; $label.Foreground = [Windows.Media.Brushes]::White
  $label.VerticalAlignment = 'Center'; $label.Margin = New-Object Windows.Thickness 0, 0, 16, 0
  $label.Text = 'Agent is working...'
  $stopBtn = New-Object Windows.Controls.Border
  $stopBtn.Width = 30; $stopBtn.Height = 30; $stopBtn.CornerRadius = New-Object Windows.CornerRadius 15
  $stopBtn.Background = Brush (Color 255 34 211 238); $stopBtn.Cursor = [Windows.Input.Cursors]::Hand
  $stopBtn.ToolTip = 'Stop'
  $sq = New-Object Windows.Shapes.Rectangle; $sq.Width = 10; $sq.Height = 10; $sq.RadiusX = 2; $sq.RadiusY = 2
  $sq.Fill = Brush (Color 255 12 38 42); $sq.HorizontalAlignment = 'Center'; $sq.VerticalAlignment = 'Center'
  $stopBtn.Child = $sq
  [void]$sp.Children.Add($dot); [void]$sp.Children.Add($label); [void]$sp.Children.Add($stopBtn)
  $root.Child = $sp; $pill.Content = $root

  $script:quitAt = $null
  $stopBtn.Add_MouseLeftButtonUp({
    try { Set-Content -Path $stopFile -Value 'stop' -Encoding ascii } catch {}
    $label.Text = 'Stopping...'
    $script:quitAt = (Get-Date).AddSeconds(1.2)
  })
  function Place-Pill {
    $wa = [Windows.SystemParameters]::WorkArea
    $pill.Left = $wa.Left + ($wa.Width - $pill.ActualWidth) / 2
    $pill.Top = $wa.Bottom - $pill.ActualHeight - 8
  }
  $pill.Add_ContentRendered({ Place-Pill })

  # ---------- timer: status text, heartbeat watchdog, quit ----------
  $script:lastText = [datetime]::MinValue; $script:baseText = ''; $script:engaged = $false; $script:lockSince = $null
  $timer = New-Object Windows.Threading.DispatcherTimer; $timer.Interval = [TimeSpan]::FromMilliseconds(250)
  $closeAll = {
    try { [OvLock]::Uninstall() } catch {}
    try { Remove-Item (Join-Path $Dir 'pid') -Force -ErrorAction SilentlyContinue } catch {}
    try { Set-Content -Path $lockState -Value 'released' -Encoding ascii } catch {}
    $timer.Stop(); $glow.Close(); $pill.Close()
  }
  function Show-Label { $t = $script:baseText; if ($script:engaged) { $t = [string][char]0xD83D + [char]0xDD12 + ' ' + $t }; $label.Text = $t; $pill.UpdateLayout(); Place-Pill }
  $timer.Add_Tick({
    try {
      $now = Get-Date
      if (Test-Path $quitFile) { & $closeAll; return }
      if ($script:quitAt -and $now -ge $script:quitAt) { & $closeAll; return }
      if (($now - $started).TotalMinutes -ge $MaxMinutes) { Log 'max lifetime'; & $closeAll; return }
      if (Test-Path $beatFile) {
        if (($now - (Get-Item $beatFile).LastWriteTime).TotalSeconds -ge $IdleSeconds) { Log 'heartbeat stale'; & $closeAll; return }
      }
      if ((Test-Path $textFile) -and -not $script:quitAt) {
        $mt = (Get-Item $textFile).LastWriteTime
        if ($mt -ne $script:lastText) {
          $script:lastText = $mt
          $t = (Get-Content -Path $textFile -Encoding UTF8 -Raw).Trim()
          if ($t) { $script:baseText = $t; Show-Label }
        }
      }
      # ----- input lock engagement -----
      $beatAge = if (Test-Path $beatFile) { ($now - (Get-Item $beatFile).LastWriteTime).TotalSeconds } else { 9999 }
      $want = (Test-Path $lockFile) -and -not $script:quitAt -and -not [OvLock]::Emergency -and ($beatAge -lt $LockIdleSeconds)
      if ($want -and -not $script:lockSince) { $script:lockSince = $now }
      if ($want -and ($now - $script:lockSince).TotalMinutes -ge $LockMaxMinutes) { $want = $false; Log 'lock max duration reached'; Remove-Item $lockFile -Force -ErrorAction SilentlyContinue }
      if (-not $want) { $script:lockSince = $null }
      if ($want -and -not [OvLock]::Installed) { if (-not [OvLock]::Install()) { Log 'hook install failed'; $want = $false; Remove-Item $lockFile -Force -ErrorAction SilentlyContinue } }
      if ($want) { [OvLock]::RefreshPill() }
      [OvLock]::Active = $want
      if ($want -ne $script:engaged) {
        $script:engaged = $want; Show-Label
        try { Set-Content -Path $lockState -Value $(if ($want) { 'engaged' } else { 'released' }) -Encoding ascii } catch {}
        Log "input lock $(if ($want) { 'engaged' } else { 'released' }) (blocked keys=$([OvLock]::BlockedKeys) clicks=$([OvLock]::BlockedClicks); hook saw keys=$([OvLock]::SeenKeys) [physical $([OvLock]::SeenPhysicalKeys)] mouse=$([OvLock]::SeenMouse) [physical $([OvLock]::SeenPhysicalMouse)])"
      }
      if ([OvLock]::Emergency) {
        Log 'EMERGENCY: Esc held, releasing everything'
        [OvLock]::Active = $false; [OvLock]::Uninstall()
        try { Set-Content -Path $stopFile -Value 'esc' -Encoding ascii } catch {}
        $script:baseText = 'Lock released (Esc)'; $script:engaged = $false; Show-Label
        $script:quitAt = $now.AddSeconds(1.2); [OvLock]::ResetEmergency()
      }
    } catch { Log "tick error: $_" }
  })

  $glow.Show(); $pill.Show()
  Set-ExStyle $glow $true (-not $VisibleInCapture)
  Set-ExStyle $pill $false (-not $VisibleInCapture)
  [OvLock]::SetPill((New-Object Windows.Interop.WindowInteropHelper $pill).Handle)
  $timer.Start()
  Log "started pid=$PID visibleInCapture=$($VisibleInCapture.IsPresent)"
  $app = New-Object Windows.Application; $app.ShutdownMode = 'OnLastWindowClose'
  [void]$app.Run()
} catch {
  Log "fatal: $_"
} finally {
  try { Remove-Item (Join-Path $Dir 'pid') -Force -ErrorAction SilentlyContinue } catch {}
}
