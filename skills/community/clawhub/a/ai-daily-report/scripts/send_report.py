#!/usr/bin/env python3
"""Send the generated PNG report to a Feishu chat.
Requires the environment variable FEISHU_CHAT_ID (e.g. "chat:xxxxxxxx")
Uses the OpenClaw feishu_doc tool to upload the file and then prints a short message.
"""
import os, sys, pathlib, subprocess, json

CHAT_ID = os.getenv('FEISHU_CHAT_ID')
if not CHAT_ID:
    sys.stderr.write('Error: FEISHU_CHAT_ID not set in environment\n')
    sys.exit(1)

# Assume this script is run from the skill root
skill_root = pathlib.Path(__file__).parent.parent
png_path = skill_root / 'report.png'
if not png_path.is_file():
    sys.stderr.write(f'PNG report not found: {png_path}\n')
    sys.exit(1)

# Use the OpenClaw tool `feishu_doc` via subprocess
def feishu_upload(file_path):
    # Build a JSON payload for the tool call
    payload = {
        "action": "upload_file",
        "file_path": str(file_path),
        "folder_token": None,  # Let Feishu decide (default folder)
        "grant_to_requester": True,
    }
    # The OpenClaw CLI provides a subcommand `openclaw tool feishu_doc`? 
    # We can invoke via `openclaw tool feishu_doc` passing JSON via stdin.
    cmd = ['openclaw', 'tool', 'feishu_doc']
    proc = subprocess.run(cmd, input=json.dumps(payload).encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        sys.stderr.write(f'feishu_doc error: {proc.stderr.decode()}\n')
        sys.exit(1)
    return json.loads(proc.stdout.decode())

result = feishu_upload(png_path)
file_token = result.get('file_token')
if not file_token:
    sys.stderr.write('Failed to get file token from upload response\n')
    sys.exit(1)

# Send a message with the uploaded file as an attachment
msg_payload = {
    "action": "send",
    "chat_id": CHAT_ID,
    "message": "🗞️ 今日 AI 报告已生成，请查看附件。",
    "file_token": file_token,
}
# Using the generic message tool
cmd = ['openclaw', 'tool', 'message']
proc = subprocess.run(cmd, input=json.dumps(msg_payload).encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if proc.returncode != 0:
    sys.stderr.write(f'message send error: {proc.stderr.decode()}\n')
    sys.exit(1)
print('Report sent to Feishu chat')