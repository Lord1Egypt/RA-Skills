#!/bin/bash
# cc-sticky-notify — main notification script
# Usage:
#   arg mode:   notify.sh "title line" ["line 2" ...]   (Notification / PostToolUse hook)
#   stdin mode: echo '{"session_id":"..."}' | notify.sh   (Stop hook)

# Resolve the skill scripts directory; all dependencies live here
SKILL_SCRIPTS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BINARY="$SKILL_SCRIPTS/sticky-notify.app/Contents/MacOS/sticky-notify-app"
TIMESTAMP=$(date '+%H:%M:%S')
PROJECT=$(basename "$(pwd)")

# Always read session_id from hook JSON (piped via stdin by Claude Code for all hook types)
SESSION_SHORT=""
if [ ! -t 0 ]; then
    HOOK_JSON=$(cat)
    SESSION_SHORT=$(printf '%s' "$HOOK_JSON" | sed -nE 's/.*"session_id":"([a-zA-Z0-9]{8}).*/\1/p' 2>/dev/null || echo "")
fi
SESSION_KEY="${SESSION_SHORT:-default}"

if [ $# -gt 0 ]; then
    # Arg mode: use provided text, append timestamp (Project appended after Source detection)
    LINES=("$@" "Time: $TIMESTAMP")
else
    # Stdin mode: Stop hook — show completion message
    LINES=("✅ Claude Code task completed" "Time: $TIMESTAMP")
fi

# One window per session — use SESSION_KEY alone so cd mid-session doesn't change the path
# PROJECT is used for display only (updated on every notification)
TMP_DIR="/tmp/cc-sticky-notify"
mkdir -p "$TMP_DIR"
CONTENT_FILE="$TMP_DIR/${SESSION_KEY}.txt"
PID_FILE="$TMP_DIR/${SESSION_KEY}.pid"
FOCUS_FILE="$TMP_DIR/${SESSION_KEY}.focus"

# Walk process tree (pure ps calls, fast, synchronous)
_pid=$$
_ancestors=""
for _i in 1 2 3 4 5 6 7 8 9 10 11 12; do
    _pid=$(ps -p "$_pid" -o ppid= 2>/dev/null | tr -d ' ')
    if [ -z "$_pid" ] || [ "$_pid" = "0" ] || [ "$_pid" = "1" ]; then break; fi
    _ancestors="${_ancestors:+$_ancestors,}$_pid"
done

# Detect parent GUI app and front window via System Events (synchronous single call)
SOURCE_APP=""
if [ -n "$_ancestors" ]; then
    _wf="${FOCUS_FILE%.focus}.window"
    _posf="${FOCUS_FILE%.focus}.pos"
    _result=$(osascript -e "tell application \"System Events\"
set pids to {$_ancestors}
repeat with p in pids
    try
        set proc to first application process whose unix id is p
        if (background only of proc) is false and (bundle identifier of proc) is not missing value then
            set _n to name of proc
            set _w to \"\"
            set _px to \"\"
            set _py to \"\"
            try
                set _w to name of front window of proc
                set _pos to position of front window of proc
                set _px to (item 1 of _pos) as text
                set _py to (item 2 of _pos) as text
            end try
            return _n & \"|\" & _w & \"|\" & _px & \",\" & _py
        end if
    end try
end repeat
end tell" 2>/dev/null)
    if [ -n "$_result" ]; then
        SOURCE_APP=$(printf '%s' "${_result%%|*}" | tr -d '\r\n')
        _rest="${_result#*|}"
        _win=$(printf '%s' "${_rest%%|*}" | tr -d '\r\n')
        _pos=$(printf '%s' "${_rest#*|}" | tr -d '\r\n')
        [ -n "$SOURCE_APP" ] && printf '%s\n' "$SOURCE_APP" > "$FOCUS_FILE"
        # 窗口标题和位置只写一次（首次通知捕获）：
        # 防止用户切换到其他窗口后，后续 hook（如 Stop）用 front window
        # 覆盖掉最初正确的目标窗口信息。
        [ -n "$_win" ] && [ ! -f "$_wf" ] && printf '%s\n' "$_win" > "$_wf"
        [[ "$_pos" == *,* ]] && [ ! -f "$_posf" ] && printf '%s\n' "$_pos" > "$_posf"
        # Capture CGWindowID — unique per window, reliable for multi-window matching
        _widFile="$TMP_DIR/${SESSION_KEY}.wid"
        if [ ! -f "$_widFile" ]; then
            _wid=$(osascript -l JavaScript -e "
ObjC.import('CoreGraphics');ObjC.import('Foundation');
var target='$SOURCE_APP'.toLowerCase();
var cfArr=\$.CGWindowListCopyWindowInfo(1,0);
var nsArr=ObjC.castRefToObject(cfArr);var r='';
for(var i=0;i<nsArr.count;i++){var info=nsArr.objectAtIndex(i);
var owner=ObjC.unwrap(info.objectForKey('kCGWindowOwnerName'));
if(owner.toLowerCase()===target&&ObjC.unwrap(info.objectForKey('kCGWindowLayer'))===0){
r=''+ObjC.unwrap(info.objectForKey('kCGWindowNumber'));break;}}r;" 2>/dev/null)
            [ -n "$_wid" ] && printf '%s\n' "$_wid" > "$_widFile"
        fi
    fi
fi

# Append Source (Time → Source → Project order)
[ -n "$SOURCE_APP" ] && LINES+=("Source: $SOURCE_APP")
LINES+=("Project: $PROJECT")

# Dedup: compute content signature excluding the Time: line
SIG=""
for _line in "${LINES[@]}"; do
    [[ "$_line" == Time:* ]] && continue
    SIG="${SIG}${_line}\n"
done
LAST_SIG_FILE="$TMP_DIR/${SESSION_KEY}.sig"
if [ -f "$LAST_SIG_FILE" ]; then
    PREV_SIG=$(cat "$LAST_SIG_FILE" 2>/dev/null)
    if [ "$PREV_SIG" = "$SIG" ]; then
        exit 0  # Same content as last notification, skip
    fi
fi
printf '%s' "$SIG" > "$LAST_SIG_FILE"

printf '%s\n' "${LINES[@]}" > "$CONTENT_FILE"

if [ -f "$PID_FILE" ]; then
    EXISTING_PID=$(cat "$PID_FILE" 2>/dev/null)
    if [ -n "$EXISTING_PID" ] && kill -0 "$EXISTING_PID" 2>/dev/null; then
        exit 0  # Window is alive; DispatchSource watcher refreshes content automatically
    fi
fi

# No running instance — launch new floating sticky note
if [ -f "$BINARY" ]; then
    "$BINARY" "$CONTENT_FILE" </dev/null >/dev/null 2>&1 &
    disown $!
fi
