#!/usr/bin/env bash
# Desktop Pilot - one CLI for Windows (incl. from WSL), macOS and Linux desktops.
# Usage: desktop.sh <action> [--process P] [--title T] [--name LABEL] [--text S] [--keys K] [--x N --y N] [--button left|right|double|move] [--out file.png]
# Actions: os | screenshot | windows | buttons | click | close | focus | type | key | mouse
#          overlay start|stop|status|text|clear|lock|unlock|selftest   (Windows: "agent is working" glow + Stop button; see SKILL.md)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACTION="${1:-help}"; shift || true
SUB=""; if [[ "$ACTION" == overlay ]]; then SUB="${1:-status}"; shift || true; fi
declare -A O=()
while [[ $# -gt 0 ]]; do
  case "$1" in --*) O["${1#--}"]="${2:-}"; shift 2 || shift ;; *) shift ;; esac
done
die() { echo "ERROR: $*" >&2; exit 1; }
has() { command -v "$1" >/dev/null 2>&1; }

detect_os() {
  case "$(uname -s)" in
    Darwin) echo macos ;;
    Linux) if grep -qi microsoft /proc/version 2>/dev/null && [[ -x /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe ]] || has powershell.exe; then echo wsl; else echo linux; fi ;;
    MINGW*|MSYS*|CYGWIN*) echo windows ;;
    *) echo unknown ;;
  esac
}
OS="$(detect_os)"
[[ "$ACTION" == os ]] && { echo "$OS"; exit 0; }

# ---------- Overlay ("agent is working": glow + status pill + Stop button) ----------
# While an overlay is running, every action refreshes its heartbeat. The overlay closes by itself when the
# heartbeat goes stale. If the user presses Stop, every action aborts with exit code 3 until `overlay clear`.
overlay_hook() {  # $1 = overlay state dir as seen from this shell
  local d="$1"
  if [[ -f "$d/stop.flag" ]]; then
    echo "STOPPED_BY_USER: the user pressed Stop on the overlay. Stop acting and ask the user how to continue (run 'desktop.sh overlay clear' only after they agree)." >&2
    exit 3
  fi
  [[ -f "$d/pid" ]] && touch "$d/beat" 2>/dev/null || true
  return 0
}
overlay_paths() {  # sets OV_PS OV_WTEMP OV_L (state dir) OV_W (same dir, Windows path)
  [[ "$OS" == wsl || "$OS" == windows ]] || die "overlay is only available on Windows for now"
  if [[ "$OS" == wsl ]]; then OV_PS="$(command -v powershell.exe || echo /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe)"
  else OV_PS="$(command -v powershell.exe || command -v pwsh)"; fi
  local cache="${XDG_RUNTIME_DIR:-/tmp}/desktop-pilot.wtemp"
  if [[ -s "$cache" ]]; then OV_WTEMP="$(cat "$cache")"; else OV_WTEMP="$("$OV_PS" -NoProfile -Command '[IO.Path]::GetTempPath()' | tr -d '\r')"; printf %s "$OV_WTEMP" > "$cache"; fi
  local ltemp; if [[ "$OS" == wsl ]]; then ltemp="$(wslpath -u "$OV_WTEMP")"; else ltemp="$(cygpath -u "$OV_WTEMP")"; fi
  OV_L="$ltemp/desktop-pilot/overlay"; OV_W="${OV_WTEMP}desktop-pilot\\overlay"; mkdir -p "$OV_L"
}
overlay_alive() {
  [[ -f "$OV_L/pid" ]] || return 1
  local pid; pid="$(tr -d '\r\n ' < "$OV_L/pid")"; [[ -n "$pid" ]] || return 1
  [[ "$("$OV_PS" -NoProfile -Command "if (Get-Process -Id $pid -ErrorAction SilentlyContinue) { 'yes' }" | tr -d '\r\n')" == yes ]]
}
run_overlay() {
  overlay_paths
  case "$SUB" in
    start)
      cp "$HERE/windows/overlay.ps1" "$OV_L/../overlay.ps1"
      rm -f "$OV_L/stop.flag" "$OV_L/quit.flag"
      if [[ -n "${O[lock]:-}" && "${O[lock]}" != 0 ]]; then touch "$OV_L/lock.flag"; else rm -f "$OV_L/lock.flag"; fi
      printf '%s' "${O[text]:-${DESKTOP_PILOT_OVERLAY_TEXT:-Agent is working...}}" > "$OV_L/text.txt"
      touch "$OV_L/beat"
      if overlay_alive; then echo "OK overlay already running (text updated)"; return; fi
      rm -f "$OV_L/pid"
      local extra="'-IdleSeconds','${O[idle]:-120}'"; [[ -n "${O[capture]:-}" ]] && extra+=",'-VisibleInCapture'"
      [[ -n "${O[lock-idle]:-}" ]] && extra+=",'-LockIdleSeconds','${O[lock-idle]}'"
      "$OV_PS" -NoProfile -Command "Start-Process -WindowStyle Hidden powershell -ArgumentList '-NoProfile','-STA','-ExecutionPolicy','Bypass','-File','${OV_WTEMP}desktop-pilot\\overlay.ps1','-Dir','$OV_W',$extra" >/dev/null
      local i; for i in $(seq 1 30); do [[ -f "$OV_L/pid" ]] && break; sleep 0.3; done
      if overlay_alive; then echo "OK overlay started$([[ -f "$OV_L/lock.flag" ]] && echo ' (input lock requested: user input is ignored while you keep acting; hold Esc 1.5 s or press Stop to release)')"; else echo "ERROR overlay did not start; see $OV_L/log.txt" >&2; [[ -f "$OV_L/log.txt" ]] && tail -5 "$OV_L/log.txt" >&2; exit 1; fi ;;
    text)
      [[ -n "${O[text]:-}" ]] || die "Specify --text"
      printf '%s' "${O[text]}" > "$OV_L/text.txt"; touch "$OV_L/beat"; echo "OK overlay text updated" ;;
    stop)
      if overlay_alive; then touch "$OV_L/quit.flag"; local i; for i in $(seq 1 15); do overlay_alive || break; sleep 0.3; done
        overlay_alive && { "$OV_PS" -NoProfile -Command "Stop-Process -Id $(tr -d '\r\n ' < "$OV_L/pid") -Force" >/dev/null; rm -f "$OV_L/pid"; }
        echo "OK overlay stopped"
      else rm -f "$OV_L/pid"; echo "OK overlay not running"; fi
      rm -f "$OV_L/quit.flag" ;;
    clear) rm -f "$OV_L/stop.flag"; echo "OK stop flag cleared" ;;
    lock)
      overlay_alive || die "overlay is not running (overlay start first)"
      touch "$OV_L/lock.flag" "$OV_L/beat"; echo "OK input lock requested (engages with your next action, releases 8 s after the last one; Esc held 1.5 s or Stop releases it)" ;;
    unlock) rm -f "$OV_L/lock.flag"; echo "OK input lock released" ;;
    selftest)
      cp "$HERE/windows/overlay.ps1" "$OV_L/../overlay.ps1"
      "$OV_PS" -NoProfile -STA -ExecutionPolicy Bypass -File "${OV_WTEMP}desktop-pilot\\overlay.ps1" -Dir "$OV_W" -SelfTest | tr -d '\r' ;;
    status)
      if overlay_alive; then echo "running"; else echo "not running"; fi
      [[ -f "$OV_L/stop.flag" ]] && echo "stop requested by the user (actions abort until: overlay clear)"
      if [[ -f "$OV_L/lock.flag" ]]; then echo "input lock: requested ($(cat "$OV_L/lock.state" 2>/dev/null || echo unknown))"; else echo "input lock: off"; fi
      [[ -f "$OV_L/text.txt" ]] && echo "text: $(cat "$OV_L/text.txt")"; return 0 ;;
    *) die "overlay start|stop|status|text|clear|lock|unlock|selftest   [--text S] [--idle SECONDS] [--lock 1] [--lock-idle SECONDS] [--capture 1]" ;;
  esac
}

# ---------- Windows (native Git Bash/MSYS or WSL) ----------
run_windows() {
  local ps ps1 winps1 args=() out="${O[out]:-}" ovdir=""
  if [[ "$OS" == wsl ]]; then
    ps="$(command -v powershell.exe || echo /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe)"
    # powershell.exe cannot reliably run scripts from \\wsl$: stage it in the Windows temp folder.
    local wtemp; wtemp="$("$ps" -NoProfile -Command '[IO.Path]::GetTempPath()' | tr -d '\r')"
    local ltemp; ltemp="$(wslpath -u "$wtemp")"
    mkdir -p "$ltemp/desktop-pilot"; cp "$HERE/windows/desktop.ps1" "$ltemp/desktop-pilot/desktop.ps1"
    ovdir="$ltemp/desktop-pilot/overlay"; overlay_hook "$ovdir"
    winps1="${wtemp}desktop-pilot\\desktop.ps1"
  else
    ps="$(command -v powershell.exe || command -v pwsh)"; winps1="$HERE/windows/desktop.ps1"
  fi
  args=("$ACTION")
  for k in process title name keys button; do [[ -n "${O[$k]:-}" ]] && args+=("-${k^}" "${O[$k]}"); done
  [[ -n "${O[text]:-}" ]] && args+=(-TextB64 "$(printf %s "${O[text]}" | base64 -w0)")
  [[ -n "${O[x]:-}" ]] && args+=(-X "${O[x]}"); [[ -n "${O[y]:-}" ]] && args+=(-Y "${O[y]}")
  local winout=""
  if [[ "$ACTION" == screenshot ]]; then
    if [[ "$OS" == wsl ]]; then winout="${wtemp}desktop-pilot\\shot.png"; args+=(-Out "$winout")
    elif [[ -n "$out" ]]; then args+=(-Out "$out"); fi
  fi
  "$ps" -NoProfile -ExecutionPolicy Bypass -File "$winps1" "${args[@]}" | tr -d '\r'
  [[ -n "$ovdir" && -f "$ovdir/pid" ]] && touch "$ovdir/beat" || true   # heartbeat at the END too: PowerShell startup takes ~3 s
  if [[ -n "$winout" ]]; then
    out="${out:-/tmp/desktop-pilot.png}"; cp "$(wslpath -u "$winout")" "$out"; echo "Linux path: $out"
  fi
}

# ---------- macOS ----------
run_macos() {
  local args=("$ACTION")
  for k in process title name text keys x y button out; do [[ -n "${O[$k]:-}" ]] && args+=("--$k" "${O[$k]}"); done
  osascript -l JavaScript "$HERE/macos/desktop.js" "${args[@]}"
}

# ---------- Linux (X11 via xdotool/wmctrl; Wayland partial via grim/wtype/ydotool) ----------
win_id() {
  local id=""
  if [[ -n "${O[title]:-}" ]] && has xdotool; then id="$(xdotool search --onlyvisible --name "${O[title]}" | head -1)"; fi
  if [[ -z "$id" && -n "${O[process]:-}" ]] && has xdotool; then id="$(xdotool search --onlyvisible --class "${O[process]}" | head -1)"; fi
  [[ -n "$id" ]] || die "No window matches (needs xdotool on X11; on Wayland focus the window manually)"
  echo "$id"
}
run_linux() {
  local wayland=""; [[ -n "${WAYLAND_DISPLAY:-}" ]] && wayland=1
  case "$ACTION" in
    screenshot)
      local out="${O[out]:-/tmp/desktop-pilot.png}"
      if [[ -n "$wayland" ]] && has grim; then grim "$out"
      elif has gnome-screenshot; then gnome-screenshot -f "$out"
      elif has spectacle; then spectacle -b -n -f -o "$out"
      elif has scrot; then scrot -o "$out"
      elif has import; then import -window root "$out"
      else die "Install one of: grim (Wayland), gnome-screenshot, scrot, imagemagick"; fi
      echo "OK screenshot $out" ;;
    windows)
      if has wmctrl; then wmctrl -lp | awk '{pid=$3; $1=$2=$3=$4=""; sub(/^ +/,""); print pid"\t"$0}'
      elif has xdotool; then for w in $(xdotool search --onlyvisible --name .); do echo "$(xdotool getwindowpid "$w" 2>/dev/null)	$(xdotool getwindowname "$w")"; done
      else die "Install wmctrl or xdotool"; fi ;;
    buttons|click)
      python3 "$HERE/linux/atspi.py" "$ACTION" ${O[process]:+--app "${O[process]}"} ${O[title]:+--title "${O[title]}"} ${O[name]:+--name "${O[name]}"} ;;
    close)
      if has wmctrl && [[ -n "${O[title]:-}" ]]; then wmctrl -c "${O[title]}" && echo "OK closed '${O[title]}'"
      elif has xdotool; then xdotool windowclose "$(win_id)" 2>/dev/null || xdotool windowactivate --sync "$(win_id)" key alt+F4; echo "OK closed"
      else python3 "$HERE/linux/atspi.py" close ${O[process]:+--app "${O[process]}"} ${O[title]:+--title "${O[title]}"}; fi ;;
    focus)
      if has wmctrl && [[ -n "${O[title]:-}" ]]; then wmctrl -a "${O[title]}"; else xdotool windowactivate --sync "$(win_id)"; fi; echo "OK focused" ;;
    type)
      [[ -n "${O[text]:-}" ]] || die "Specify --text"
      [[ -n "${O[process]:-}${O[title]:-}" ]] && has xdotool && xdotool windowactivate --sync "$(win_id)"
      if [[ -n "$wayland" ]] && has wtype; then wtype "${O[text]}"; elif has xdotool; then xdotool type --delay 20 -- "${O[text]}"; elif has ydotool; then ydotool type "${O[text]}"; else die "Install xdotool (X11) or wtype/ydotool (Wayland)"; fi
      echo "OK typed ${#O[text]} chars" ;;
    key)
      [[ -n "${O[keys]:-}" ]] || die "Specify --keys (ctrl+c, alt+f4, enter...)"
      [[ -n "${O[process]:-}${O[title]:-}" ]] && has xdotool && xdotool windowactivate --sync "$(win_id)"
      local k="${O[keys]}"; k="${k//enter/Return}"; k="${k//esc/Escape}"; k="${k//backspace/BackSpace}"; k="${k//pageup/Prior}"; k="${k//pagedown/Next}"
      has xdotool || die "Install xdotool"; xdotool key -- "$k"; echo "OK keys ${O[keys]}" ;;
    mouse)
      [[ -n "${O[x]:-}" && -n "${O[y]:-}" ]] || die "Specify --x and --y"
      has xdotool || die "Install xdotool (X11) or use ydotool on Wayland"
      xdotool mousemove "${O[x]}" "${O[y]}"
      case "${O[button]:-left}" in left) xdotool click 1 ;; right) xdotool click 3 ;; double) xdotool click --repeat 2 1 ;; move) ;; esac
      echo "OK mouse ${O[button]:-left} at ${O[x]},${O[y]}" ;;
    *) sed -n '2,4p' "$0" ;;
  esac
}

[[ "$ACTION" == overlay ]] && { run_overlay; exit 0; }
case "$OS" in
  wsl|windows) run_windows ;;
  macos) run_macos ;;
  linux) run_linux ;;
  *) die "Unsupported OS: $(uname -s)" ;;
esac
