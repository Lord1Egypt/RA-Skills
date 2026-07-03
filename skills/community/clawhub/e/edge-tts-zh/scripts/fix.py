#!/usr/bin/env python3
with open('C:/Users/Administrator/.openclaw/workspace/skills/edge-tts-zh/scripts/speak.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到第 135 行并替换
for i, line in enumerate(lines):
    if 'subprocess.run' in line and 'Start-Process' in line:
        # 替换为正确的 f-string 语法
        lines[i] = '        subprocess.run(["powershell", "-Command", f\'Start-Process "{output_path}" -WindowStyle Hidden\'], capture_output=True, timeout=5)\n'
        break

with open('C:/Users/Administrator/.openclaw/workspace/skills/edge-tts-zh/scripts/speak.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed!")
