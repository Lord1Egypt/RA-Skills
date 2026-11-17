'use strict';

const { spawn } = require('child_process');

// Recipient and text arrive as argv, so nothing is ever spliced into the script.
const SEND_SCRIPT = `on run argv
  set target to item 1 of argv
  set body to item 2 of argv
  set kind to item 3 of argv
  tell application "Messages"
    if kind is "chat" then
      send body to chat id target
    else if kind is "sms" then
      send body to participant target of (1st account whose service type = SMS)
    else
      send body to participant target of (1st account whose service type = iMessage)
    end if
  end tell
end run`;

/** A chat guid looks like `iMessage;-;+15555550123` or `any;+;chat123...`. */
function sendPlan(to, text, service = 'imessage') {
  const kind = to.includes(';') ? 'chat' : service.toLowerCase() === 'sms' ? 'sms' : 'imessage';
  return { kind, to, text, args: ['-e', SEND_SCRIPT, to, text, kind] };
}

function runSend(plan) {
  return new Promise((resolve, reject) => {
    const proc = spawn('osascript', plan.args);
    let stderr = '';
    proc.stderr.on('data', (d) => (stderr += d));
    proc.on('error', reject);
    proc.on('close', (code) => (code === 0 ? resolve() : reject(new Error(stderr.trim() || `osascript exited ${code}`))));
  });
}

module.exports = { SEND_SCRIPT, sendPlan, runSend };
