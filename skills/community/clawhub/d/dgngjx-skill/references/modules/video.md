# 🎬 模块 8：视频工具

---

#### 8.1 视频格式转换 / 8.2 视频编辑 / 8.3 在线录屏

📦 **需 FFmpeg**

> 详见下方「📦 依赖管理」章节。

<details>
<summary>📋 视频格式转换命令</summary>

```python
import subprocess, os
f = input("文件:").strip().strip('"').replace("\\","/") or "video.mp4"
o = input("格式(gif/mp4/avi/mov/webm):").strip() or "gif"
out = f"{os.path.splitext(f)[0]}.{o}"
if not os.path.exists(f): print(f"❌ 文件不存在: {f}")
else:
    size = os.path.getsize(f)/1024/1024
    if size>500: print(f"⚠️ {size:.0f}MB 可能需5-30分钟")
    r = subprocess.run(["ffmpeg","-i",f,"-y"]
        + (["-vf","scale=480:-1"] if o=="gif" and size>50 else [])
        + [out], capture_output=True, text=True, timeout=1800)
    if r.returncode==0: print(f"✅ {out} ({os.path.getsize(out)/1024:.0f}KB)")
    else: print(f"❌ {r.stderr[:300]}")
```

</details>

<details>
<summary>📋 视频编辑命令（6功能菜单）</summary>

```python
import subprocess, os, json

def _fix(p): return p.strip().strip('"').strip("'").replace("\\","/").replace("//","/")

def _info(f):
    r = subprocess.run(["ffprobe","-v","quiet","-print_format","json","-show_format","-show_streams",f], capture_output=True, text=True, timeout=30)
    return json.loads(r.stdout) if r.returncode==0 else None

act = input("操作(1裁剪/2拼接/3提取音频/4水印/5截图/6信息):").strip() or "1"
if act=="6":
    f = _fix(input("文件:") or "video.mp4")
    info = _info(f)
    if info:
        dur = float(info.get("format",{}).get("duration",0))
        print(f"时长: {int(dur//3600):02d}:{int((dur%3600)//60):02d}:{int(dur%60):02d}")
        print(f"大小: {int(info.get('format',{}).get('size',0))/1024/1024:.1f}MB")
        for s in info.get("streams",[]):
            if s.get("codec_type")=="video": print(f"视频: {s.get('codec_name','?')} {s.get('width','?')}x{s.get('height','?')}")
            elif s.get("codec_type")=="audio": print(f"音频: {s.get('codec_name','?')} {s.get('sample_rate','?')}Hz")
```

</details>
