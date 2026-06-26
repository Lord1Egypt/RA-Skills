#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio Command Handler - Process audio files and execute commands

This script handles two scenarios:
1. Audio only: Transcribe audio -> use transcription as command -> execute
2. Audio + text: Transcribe audio -> execute the text command with transcription context

If result is > 58 chars, save to file and upload via uploader skill.
"""

import argparse
import html
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Skill paths
SKILL_DIR = Path(__file__).parent.parent
TRANSCRIBE_SCRIPT = Path.home() / ".openclaw/workspace/skills/ifly-speed-transcription/scripts/transcribe.py"
UPLOAD_SCRIPT = Path.home() / ".openclaw/workspace/skills/uploader/scripts/upload_media.py"
WORKSPACE_DIR = Path.home() / ".openclaw/workspace"


def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio file using ifly-speed-transcription skill."""
    if not TRANSCRIBE_SCRIPT.exists():
        raise FileNotFoundError(f"Transcription script not found: {TRANSCRIBE_SCRIPT}")
    
    # Run transcription
    result = subprocess.run(
        ["python3", str(TRANSCRIBE_SCRIPT), audio_path, "--output-format", "json"],
        capture_output=True,
        text=True,
        timeout=600  # 10 minutes max
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"Transcription failed: {result.stderr}")
    
    # Parse JSON output
    try:
        data = json.loads(result.stdout)
        text = data.get("text", "")
        if not text:
            raise RuntimeError("Transcription returned empty text")
        return text
    except json.JSONDecodeError:
        # Try to extract text from non-JSON output
        # The script might output the text directly
        lines = result.stdout.strip().split("\n")
        # Find the actual transcription text (after the separator)
        text_lines = []
        in_result = False
        for line in lines:
            if "Transcription Result:" in line or "====" in line:
                in_result = True
                continue
            if in_result and line and not line.startswith("===="):
                text_lines.append(line)
        
        if text_lines:
            return "\n".join(text_lines).strip()
        
        # Last resort: return the whole output
        return result.stdout.strip()


def save_and_upload(content: str, filename_prefix: str = "audio_result") -> dict:
    """Save content to HTML file and upload via uploader skill."""
    # Create temp file with HTML extension
    timestamp = subprocess.check_output(["date", "+%Y%m%d_%H%M%S"], text=True).strip()
    filename = f"{filename_prefix}_{timestamp}.html"
    temp_path = WORKSPACE_DIR / filename
    
    # Escape content for HTML
    escaped_content = html.escape(content)
    # Convert newlines to <br> tags for better display
    formatted_content = escaped_content.replace('\n', '<br>\n')
    
    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>音频处理结果</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 
                         'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1a1a1a;
            font-size: 24px;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 2px solid #e8e8e8;
        }}
        .content {{
            font-size: 15px;
            line-height: 1.8;
            color: #333;
        }}
        .content p {{
            margin-bottom: 12px;
        }}
        .timestamp {{
            color: #999;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 16px;
            border-top: 1px solid #e8e8e8;
        }}
        @media print {{
            body {{
                background: #fff;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                max-width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📝 音频处理结果</h1>
        <div class="content">
            {formatted_content}
        </div>
        <div class="timestamp">
            生成时间: {timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[9:11]}:{timestamp[11:13]}:{timestamp[13:]}
        </div>
    </div>
</body>
</html>"""
    
    # Write HTML file
    temp_path.write_text(html_content, encoding="utf-8")
    
    # Upload
    if not UPLOAD_SCRIPT.exists():
        raise FileNotFoundError(f"Upload script not found: {UPLOAD_SCRIPT}")
    
    result = subprocess.run(
        ["python3", str(UPLOAD_SCRIPT), str(temp_path)],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    # Parse upload result
    output = {}
    for line in result.stdout.strip().split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            output[key.strip()] = value.strip()
    
    return output


def main():
    parser = argparse.ArgumentParser(
        description="Handle audio commands: transcribe and prepare for execution"
    )
    parser.add_argument("audio_path", help="Path to audio file")
    parser.add_argument("--command", "-c", help="Text command to execute with transcription context")
    parser.add_argument("--output", "-o", help="Output file for transcription text")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Validate audio file
    audio_path = Path(args.audio_path)
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}", file=sys.stderr)
        sys.exit(1)
    
    # Transcribe
    print("Transcribing audio...", file=sys.stderr)
    try:
        transcription = transcribe_audio(str(audio_path))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Determine the command to execute
    if args.command:
        # Audio + command: use the provided command
        command = args.command
        context = transcription
    else:
        # Audio only: transcription IS the command
        command = transcription
        context = None
    
    # Output result
    if args.json:
        output = {
            "transcription": transcription,
            "command": command,
            "context": context,
            "mode": "audio+command" if args.command else "audio-only"
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"TRANSCRIPTION:\n{transcription}")
        if args.command:
            print(f"\nCOMMAND: {command}")
        else:
            print(f"\nCOMMAND (from transcription): {command}")
    
    # Save to file if requested
    if args.output:
        Path(args.output).write_text(transcription, encoding="utf-8")
        print(f"\nSaved to: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
