#!/usr/bin/env python3
import re

# 读取文件
with open('C:/Users/Administrator/.openclaw/workspace/skills/edge-tts-zh/scripts/speak.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找并替换
old_code = '        print(output_path)  # stdout 输出文件路径\n        return True'
new_code = '''        # 自动播放（后台静默播放，不弹窗）
        try:
            subprocess.run(
                ["powershell", "-Command", f'Start-Process "{output_path}" -WindowStyle Hidden'],
                capture_output=True,
                timeout=5
            )
            print(f"🔊 正在播放...", file=sys.stderr)
        except Exception as e:
            print(f"⚠️  播放失败：{e}", file=sys.stderr)
        
        print(output_path)  # stdout 输出文件路径
        return True'''

content = content.replace(old_code, new_code)

# 写回文件
with open('C:/Users/Administrator/.openclaw/workspace/skills/edge-tts-zh/scripts/speak.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 修改完成！")
