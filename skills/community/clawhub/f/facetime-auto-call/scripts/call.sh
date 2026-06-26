#!/usr/bin/env bash
# FaceTime Auto-Call Script v4.1 (Public)
# Programmatically trigger FaceTime calls and click the confirmation notification.
# Usage: call.sh <mode> <target>

set -euo pipefail

CMD="${1:-help}"
shift 2>/dev/null || true

clean_number() {
  echo "$1" | tr -d ' ()-'
}

cleanup_environment() {
  echo "   Cleaning environment..."
  killall FaceTime 2>/dev/null || true
  sleep 1
}

auto_click_call_button() {
  osascript <<'APSCRIPT'
tell application "System Events"
    tell process "NotificationCenter"
        repeat 20 times
            if exists window "Notification Center" then
                exit repeat
            end if
            delay 0.5
        end repeat

        if not (exists window "Notification Center") then
            error "Notification Center window did not appear"
        end if

        tell window "Notification Center"
            repeat 10 times
                try
                    set allGroups to every group of scroll area 1 of group 1 of group 1
                    if (count of allGroups) > 0 then
                        exit repeat
                    end if
                end try
                delay 0.5
            end repeat

            try
                set btn to button 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of scroll area 1 of group 1 of group 1
                click btn
                return "success"
            end try

            try
                set btn to button 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of scroll area 1 of group 1 of group 1
                click btn
                return "success"
            end try

            try
                set btn to button 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of scroll area 1 of group 1 of group 1
                click btn
                return "success"
            end try

            error "Call button not found"
        end tell
    end tell
end tell
APSCRIPT
}

case "$CMD" in
  video)
    TARGET="${1:?Target phone/email is required}"
    CLEAN=$(clean_number "$TARGET")
    echo "📹 Starting FaceTime video → $TARGET"
    cleanup_environment
    open "facetime://$CLEAN" &
    sleep 2
    echo "   Clicking call button..."
    if auto_click_call_button; then
        echo "✅ FaceTime video call started"
    else
        echo "⚠️ Auto click failed"
        exit 1
    fi
    ;;

  audio)
    TARGET="${1:?Target phone/email is required}"
    CLEAN=$(clean_number "$TARGET")
    echo "🎙️ Starting FaceTime audio → $TARGET"
    cleanup_environment
    open "facetime-audio://$CLEAN" &
    sleep 2
    echo "   Clicking call button..."
    if auto_click_call_button; then
        echo "✅ FaceTime audio call started"
    else
        echo "⚠️ Auto click failed"
        exit 1
    fi
    ;;

  find-contact)
    QUERY="${1:?Contact name is required}"
    echo "🔍 Searching contacts: $QUERY"
    osascript <<APSCRIPT
tell application "Contacts"
    set matches to every person whose name contains "$QUERY"
    set output to ""
    repeat with p in matches
        set pName to name of p
        set output to output & pName & ":\n"
        try
            set phones to value of phones of p
            repeat with ph in phones
                set output to output & "  📞 " & ph & "\n"
            end repeat
        end try
        try
            set emails to value of emails of p
            repeat with em in emails
                set output to output & "  📧 " & em & "\n"
            end repeat
        end try
    end repeat
    if output = "" then
        return "❌ Contact not found: $QUERY"
    else
        return output
    end if
end tell
APSCRIPT
    ;;

  test)
    echo "🧪 Test mode"
    cleanup_environment
    open "facetime-audio://test@icloud.com" &
    sleep 2
    echo "   Clicking call button..."
    if auto_click_call_button; then
        echo "✅ Test succeeded"
    else
        echo "❌ Test failed"
        exit 1
    fi
    ;;

  help|*)
    cat <<'HELP'
FaceTime Auto-Call v4.1 (Public)

Usage: call.sh <mode> <target>

Modes:
  audio <phone/email>     FaceTime audio call
  video <phone/email>     FaceTime video call
  find-contact <name>     Search contacts
  test                    Test mode

Examples:
  call.sh audio "user@example.com"
  call.sh video "+1234567890"
  call.sh find-contact "John"

Features:
  ✅ Multi-depth fallback (7-10 layers, prioritizing common depths)
  ✅ Environment cleanup
  ✅ Contact search

Prerequisite:
  bash /path/to/facetime-auto-call/scripts/setup.sh
HELP
    ;;
esac
