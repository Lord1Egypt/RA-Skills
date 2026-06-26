# AI短剧制作流程详细参考

## 一、项目启动

### 需求确认
与用户确认以下信息：
1. **主题**：科幻/悬疑/科普/剧情/搞笑/教育等
2. **风格**：写实/动画/赛博朋克/古风等
3. **时长**：30秒/60秒/2分钟/5分钟
4. **角色**：需要几个角色？是否有特定音色要求？
5. **参考素材**：用户是否提供文案/图片/参考视频？

### 脚本模板

```markdown
# 项目名称 · 分镜脚本

## 总览
- 总时长：XX秒
- 镜头数：XX个
- 角色数：XX个

## 分镜表
| # | 镜头ID | 画面描述 | 配音台词 | 角色 | 音色 | 时长 |
|---|--------|---------|---------|------|------|------|
| 1 | shot01_xxx | 画面描述 | 台词内容 | 角色名 | 音色ID | 10s |
| 2 | shot02_xxx | 画面描述 | 台词内容 | 角色名 | 音色ID | 10s |
```

---

## 二、视频生成

### Grok Imagine Prompt编写指南

**结构模板：**
```
[场景描述], [主体描述], [光线/氛围], [构图/镜头运动], [风格关键词]
```

**示例：**
```
"Deep space, Milky Way galaxy slowly rotating across a star-filled cosmos,
countless stars twinkling, nebulae in deep blue and purple hues,
cinematic wide shot, photorealistic, 4K quality, slow gentle rotation"
```

**各类型场景Prompt关键词：**

| 场景类型 | 关键词 |
|---------|--------|
| 太空/宇宙 | deep space, stars, nebula, galaxy, cosmic, celestial |
| 城市/街头 | city street, urban, bustling, modern, buildings |
| 室内/会议室 | conference room, modern, screens, professional |
| 人物特写 | close-up, portrait, expression, emotion, cinematic lighting |
| 自然/风景 | landscape, mountains, ocean, sunset, cinematic |
| 科技/实验室 | laboratory, technology, screens, equipment, futuristic |

### 批量提交策略

1. 25个镜头同时提交到API
2. 使用ThreadPoolExecutor(max_workers=10)
3. 每5秒轮询一次结果
4. 失败自动重试（最多5次）
5. 下载后检查文件完整性（ffprobe验证时长）

---

## 三、TTS配音生成

### 多角色音色分配策略

| 角色数量 | 分配策略 |
|---------|---------|
| 1-2个角色 | 旁白用jingying，对话角色用对应音色 |
| 3-5个角色 | 主要角色各分配独立音色，次要角色复用 |
| 6-10个角色 | 核心角色独立音色，路人/群演用通用音色 |

### 台词字数控制
- 每段TTS建议2-20字（太长影响听感）
- 10秒镜头配2-4秒台词最合适
- 留白时间给观众消化内容

---

## 四、音频驱动剪辑（核心节奏控制）

### 核心理念

**音频驱动剪辑 = 画面长度由语音旁白决定，而非固定时长。**

传统剪辑思维是"先定视频长度，再往里塞配音"，结果配音节奏被画面绑架。音频驱动反过来——先录制TTS配音，再让每段视频精确匹配对应配音的时长。这样：
- 观众听到的每句话都有完整的画面时长
- 叙事节奏由台词自然驱动
- 不会出现"话没说完画面就切了"

### 核心算法

```
对于每一段（镜头, TTS）：
  1. 获取TTS音频时长 tts_dur（ffprobe精确到毫秒）
  2. 获取源视频时长 src_dur
  3. 对比决策：
     ├── src_dur >= tts_dur + 0.5s  → 直接裁剪到tts_dur
     ├── src_dur ≈ tts_dur（差<0.5s）→ 直接裁剪
     └── src_dur < tts_dur           → stream_loop循环填充
  4. 输出：seg_NNN.mp4（时长精确=tts_dur）
```

### 逐段精确裁剪（避免累积漂移）

```python
import subprocess
from pathlib import Path

FFPROBE = '/opt/homebrew/bin/ffprobe'
FFMPEG = '/opt/homebrew/bin/ffmpeg'

def get_duration(filepath):
    """获取媒体文件精确时长"""
    result = subprocess.run(
        [FFPROBE, '-v', 'quiet', '-show_entries', 'format=duration',
         '-of', 'csv=p=0', str(filepath)],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())

def process_segment(tts_file, shot_file, output_file):
    """处理单段：按TTS时长裁剪/循环视频"""
    tts_dur = get_duration(tts_file)
    src_dur = get_duration(shot_file)
    
    cmd = [FFMPEG, '-y']
    
    if src_dur >= tts_dur:
        # 视频够长，直接裁剪
        cmd.extend(['-t', str(tts_dur), '-i', str(shot_file)])
    else:
        # 视频不够长，循环填充
        cmd.extend(['-stream_loop', '-1', '-i', str(shot_file),
                     '-t', str(tts_dur)])
    
    cmd.extend(['-c:v', 'libx264', '-preset', 'fast', str(output_file)])
    subprocess.run(cmd, check=True)
    
    # 验证输出时长
    out_dur = get_duration(output_file)
    diff = abs(out_dur - tts_dur)
    if diff > 0.5:
        print(f"⚠️ 时长偏差 {diff:.2f}s: {output_file.name}")
    
    return tts_dur

# 批量处理所有段
total = 0.0
for i, (tts_file, shot_file) in enumerate(segments):
    dur = process_segment(tts_file, shot_file, f"seg_{i:03d}.mp4")
    total += dur

print(f"总时长: {total:.2f}s")
```

### 短镜头循环填充策略

当源视频短于TTS时，用stream_loop让视频循环播放：

```bash
/opt/homebrew/bin/ffmpeg -y -stream_loop -1 -i shot.mp4 -t {tts_dur} -c:v libx264 -preset fast seg.mp4
```

**循环填充的视觉容忍度：**
| 循环次数 | 观众感知 | 建议 |
|---------|---------|------|
| 1次（补0-5s） | 几乎察觉不到 | ✅ 可用 |
| 2次（补5-10s） | 部分观众能察觉 | ⚠️ 谨慎使用 |
| 3次以上（补>10s） | 明显重复感 | ❌ 建议换镜头或补新素材 |

### 音画同步验证

合成后必须逐段验证：

```python
def verify_sync(segments_dir, tts_dir):
    """验证所有段的音画同步"""
    issues = []
    for i in range(25):
        seg = Path(segments_dir) / f"seg_{i:03d}.mp4"
        tts = Path(tts_dir) / f"tts_{i:03d}.mp3"
        
        seg_dur = get_duration(seg)
        tts_dur = get_duration(tts)
        diff = seg_dur - tts_dur
        
        if abs(diff) > 0.5:
            issues.append(f"#{i}: 偏差{diff:+.2f}s")
    
    if issues:
        print("⚠️ 同步问题:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("✅ 全部同步")
```

---

## 五、字幕生成

### Pillow字幕生成模板

```python
from PIL import Image, ImageDraw, ImageFont

def create_subtitle(text, role="", output_path="sub.png"):
    """生成字幕PNG"""
    WIDTH, HEIGHT = 1920, 160
    img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype('/System/Library/Fonts/PingFang.ttc', 48)
    
    full_text = f"{role}：{text}" if role else text
    
    # 黑色描边 + 白色填充
    draw.text((WIDTH//2, HEIGHT//2), full_text, 
              fill='white', font=font, anchor='mm',
              stroke_width=3, stroke_fill='black')
    
    img.save(output_path)
```

### FFmpeg叠加字幕

```bash
/opt/homebrew/bin/ffmpeg -y -i {video}.mp4 -i {subtitle}.png \
  -filter_complex "overlay=0:H-h" \
  -c:v libx264 -preset fast {output}.mp4
```

---

## 六、最终合成

### 视频拼接

```python
import subprocess
from pathlib import Path

def concat_videos(seg_dir, output_path):
    """拼接所有分段视频"""
    segs = sorted(Path(seg_dir).glob("seg_*.mp4"))
    
    # 生成file list
    list_path = Path(seg_dir) / "video_list.txt"
    with open(list_path, 'w') as f:
        for seg in segs:
            f.write(f"file '{seg.absolute()}'\n")
    
    cmd = [
        '/opt/homebrew/bin/ffmpeg', '-y',
        '-f', 'concat', '-safe', '0',
        '-i', str(list_path),
        '-c', 'copy',
        str(output_path)
    ]
    subprocess.run(cmd, check=True)
```

### 音频拼接

```python
def concat_audios(audio_dir, output_path):
    """拼接所有TTS音频"""
    audios = sorted(Path(audio_dir).glob("*.mp3"))
    
    list_path = Path(audio_dir) / "audio_list.txt"
    with open(list_path, 'w') as f:
        for audio in audios:
            f.write(f"file '{audio.absolute()}'\n")
    
    cmd = [
        '/opt/homebrew/bin/ffmpeg', '-y',
        '-f', 'concat', '-safe', '0',
        '-i', str(list_path),
        '-c', 'copy',
        str(output_path)
    ]
    subprocess.run(cmd, check=True)
```

### 音视频合并

```python
def merge_av(video_path, audio_path, output_path):
    """合并视频和音频"""
    cmd = [
        '/opt/homebrew/bin/ffmpeg', '-y',
        '-i', str(video_path),
        '-i', str(audio_path),
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-shortest',
        str(output_path)
    ]
    subprocess.run(cmd, check=True)
```

---

## 七、素材导出

### 桌面文件夹结构

```python
import os, shutil

def export_to_desktop(project_name, segments_data, desktop_path):
    """导出结构化素材到桌面"""
    base = os.path.join(desktop_path, project_name)
    
    dirs = {
        "01_字幕": "subtitle_pngs",
        "02_配音": "tts_mp3s",
        "03_主图": "thumbnails",
        "04_视频": "seg_videos",
        "05_矩阵表": "matrix"
    }
    
    for name in dirs:
        os.makedirs(os.path.join(base, name), exist_ok=True)
    
    # 生成矩阵表HTML
    generate_matrix_html(segments_data, os.path.join(base, "05_矩阵表", "矩阵表.html"))
    
    # 生成JSON
    generate_json(segments_data, os.path.join(base, "05_矩阵表", "素材结构.json"))
```

---

## 八、成本核算

### 完整成本模型

```python
def calculate_cost(params):
    """
    params = {
        'shot_seconds': 234,      # 镜头总时长
        'retry_times': 3,          # 平均重试次数
        'tts_chars': 350,          # TTS总字数
        'dialog_rounds': 250,      # WorkBuddy对话轮次
        'project_days': 2,         # 项目天数
    }
    """
    grok = params['shot_seconds'] * 0.05 * params['retry_times']
    tts = params['tts_chars'] * 0.0006 * 1.5  # 含重试
    wb = params['dialog_rounds'] * 0.0022 * 1.5  # 含隐性消耗
    hw = 3.65 * params['project_days']  # 硬件折旧
    power = 0.62 * params['project_days']  # 电费
    
    return {
        'Grok Imagine': grok,
        'TTS配音': tts,
        'WorkBuddy算力': wb,
        '硬件折旧': hw,
        '电费': power,
        '总计': grok + tts + wb + hw + power
    }
```

### 参考成本（基于三体EP1实战）

| 项目规模 | 预估成本 | 制作周期 |
|---------|---------|---------|
| 30秒 / 6镜头 | ¥10-15 | 0.5天 |
| 60秒 / 12镜头 | ¥20-30 | 1天 |
| 128秒 / 25镜头 | ¥40-50 | 2天 |
| 5分钟 / 50镜头 | ¥80-120 | 3-4天 |

---

## 九、常见问题排查

### 视频生成失败
- **症状**: API返回错误或超时
- **排查**: 检查API Key是否有效、余额是否充足
- **解决**: 重试（换IP节点）、切换模型

### TTS卡住
- **症状**: status一直=0
- **排查**: 检查参数格式（扁平JSON）
- **解决**: 重新提交任务

### 音画不同步
- **症状**: 画面和声音对不上
- **排查**: 检查每段TTS时长和视频裁剪时长
- **解决**: 逐段精确裁剪，不要整体缩放

### 字幕不显示
- **症状**: 视频没有字幕
- **排查**: 检查FFmpeg版本是否支持drawtext
- **解决**: 用Pillow生成PNG + overlay叠加

### 视频拼接报错
- **症状**: concat失败
- **排查**: 检查所有分段视频编码是否一致
- **解决**: 统一用libx264编码重新转码

---

## 十、专业审核与迭代流程

AI生成的第一版几乎从来不是最终版。必须经过"制作→审核→修改"的迭代循环。

### 10.1 六维审核检查表

| 维度 | 检查方法 | 判定标准 |
|------|---------|---------|
| **① 音画同步** | 逐段播放，对比画面内容与配音台词 | 角色A说话时画面必须是角色A |
| **② 时长匹配** | ffprobe对比每段视频和TTS时长 | 偏差 < 0.5s |
| **③ 视觉重复** | 检查stream_loop循环次数 | 不超过2次循环 |
| **④ 字幕准确** | 逐句对照字幕文本和TTS台词 | 无错别字、标点正确 |
| **⑤ 节奏感** | 整体观看，标记拖沓或仓促段落 | 每段TTS时长占镜头60-80%最佳 |
| **⑥ 画面质量** | 检查AI生成瑕疵 | 无变形、闪烁、分辨率异常 |

### 10.2 问题分级与修复优先级

```
P0（必须修复）—— 影响观看体验的根本问题
├── 音画不匹配：画面内容与台词无关
├── 字幕错误：错别字、台词与字幕不一致
├── 画面截断：话没说完画面就切了
└── 时长严重偏差：偏差 > 1s
→ 优先级：最高，不修不能交付

P1（建议修复）—— 影响观看体验但可接受
├── 节奏拖沓：某段画面太长，观众失去耐心
├── 视觉重复感：循环超过2次
├── 转场生硬：相邻镜头切换突兀
└── 音色不匹配：角色音色与形象不符
→ 优先级：中，尽量修

P2（可优化）—— 锦上添花
├── 画面色调不统一
├── 字幕样式可美化
├── 背景音效可丰富
└── 片头片尾可添加
→ 优先级：低，有时间再修
```

### 10.3 迭代工作流

```python
def review_and_fix(version, issues):
    """
    version: 当前版本号
    issues: 审核发现的问题列表
    
    返回: 是否需要继续迭代
    """
    p0_count = sum(1 for i in issues if i['level'] == 'P0')
    p1_count = sum(1 for i in issues if i['level'] == 'P1')
    
    print(f"版本 {version} 审核结果:")
    print(f"  P0(必须修): {p0_count}")
    print(f"  P1(建议修): {p1_count}")
    print(f"  P2(可优化): {len(issues) - p0_count - p1_count}")
    
    if p0_count > 0:
        print("→ 进入下一轮迭代")
        return True
    elif p1_count > 2:
        print("→ 建议再修一轮")
        return True
    else:
        print("→ 达到交付标准 ✅")
        return False
```

### 10.4 实战案例：三体EP1迭代记录

| 版本 | 时长 | 问题发现 | 修复内容 | 审核结论 |
|------|------|---------|---------|---------|
| v5min | 252s | 视频总长252s但TTS仅127s，大量空白段落 | 重新按TTS时长裁剪 | ❌ P0: 节奏断裂 |
| v6 | — | 音频驱动剪辑，3个短镜头被截断 | 修复中 | ❌ 未完成 |
| v7 | 127s | 3个短镜头截断：火鸡演讲缺9s | stream_loop循环填充 | ❌ P0: 画面截断 |
| v7.1 | 127.9s | 循环修复完成，但无字幕 | 加字幕 | ⚠️ P1: 缺字幕 |
| v8 | 127.9s | 字幕+音画同步修复+矩阵表 | 全部修复 | ✅ 交付 |

### 10.5 审核工具脚本

```python
#!/usr/bin/env python3
"""一键审核脚本：检查所有段的音画同步和时长匹配"""

import subprocess
from pathlib import Path

FFPROBE = '/opt/homebrew/bin/ffprobe'

def get_duration(p):
    r = subprocess.run([FFPROBE,'-v','quiet','-show_entries','format=duration',
                        '-of','csv=p=0',str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())

def audit(segments_dir, tts_dir, num_segments=25):
    issues = []
    print(f"{'#':>3} {'角色':<20} {'TTS':>7} {'视频':>7} {'偏差':>7} {'状态'}")
    print("-" * 55)
    
    for i in range(num_segments):
        seg = Path(segments_dir) / f"seg_{i:03d}.mp4"
        tts = sorted(Path(tts_dir).glob("*.mp3"))[i]
        
        seg_dur = get_duration(seg) if seg.exists() else 0
        tts_dur = get_duration(tts)
        diff = seg_dur - tts_dur
        
        status = "✅" if abs(diff) < 0.5 else "⚠️"
        if abs(diff) > 0.5:
            issues.append(f"#{i}: 偏差{diff:+.2f}s")
        
        print(f"{i:3d} {tts.stem:<20s} {tts_dur:>6.2f}s {seg_dur:>6.2f}s {diff:>+6.2f}s {status}")
    
    print(f"\n问题段: {len(issues)}")
    for issue in issues:
        print(f"  {issue}")
    
    return issues

if __name__ == '__main__':
    audit(Path('v7_assets'), Path('ep1_tts'))
```
