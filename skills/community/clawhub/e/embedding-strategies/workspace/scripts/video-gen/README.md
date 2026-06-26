# 🎬 AI 视频自动化工厂 - 使用手册

**作者**: Xiabi (40 岁大叔 AI 创业)  
**日期**: 2026-03-03  
**目标**: 用 OpenClaw + Seedance 自动生成无水印 AI 视频

---

## 📂 **目录结构**

```
workspace/
├── inputs/
│   ├── photos/           # 照片素材（头像、截图等）
│   ├── videos/           # 原始视频片段
│   ├── audio/            # 配音/背景音乐
│   └── scenes/           # AI 生成的场景图
│
├── outputs/
│   ├── video/            # 生成的成品视频
│   └── thumbnails/       # 视频封面
│
├── scripts/video-gen/    # 自动化脚本
│   ├── 01-prepare-workspace.ps1
│   ├── 02-generate-video.ps1
│   └── README.md         # 本文件
│
└── knowledge/ai-agents/templates/script/  # 剧本模板
```

---

## 🚀 **快速启动流程**

### **Step 1: 准备工作区（仅第一次）**

```powershell
# 打开 PowerShell，执行：
cd C:\Users\Xiabi\.openclaw\workspace\scripts\video-gen
.\01-prepare-workspace.ps1
```

这会为你创建所有必要的输入/输出目录。

---

### **Step 2: 放入素材**

把以下文件放到对应文件夹：

| 目录 | 放什么 | 示例 |
|------|--------|------|
| `inputs/photos/` | 你的照片、产品图、截图 | `avatar.jpg`, `dify-screenshot.png` |
| `inputs/videos/` | 你拍摄的视频片段 | `intro-clip.mp4` |
| `inputs/audio/` | 旁白配音、BGM | `narration.wav`, `bgm-inspire.mp3` |

---

### **Step 3: 编写剧本**

参考 `knowledge/ai-agents/templates/script/template-scene-script.md` 

或者直接用我给你的 Day-001 脚本：

```markdown
[Scene 1]: "我突然意识到一件事……我已经 40 岁了。"
[Scene 2]: "今早刷到一条新闻：AI 数字人主播已经能取代 80% 的传统客服岗位了。"
...
```

保存为 `workflows/scenes/day-001-scene1.md`

---

### **Step 4: 配置 Seedance API Key**

你需要先注册 Seedance 账号：

1. 访问 https://seedance.io/signup
2. 完成验证
3. 进入开发者中心 → 生成 API Key
4. Basic 计划 $19.9/月 ≈ ¥145（包含商业使用权，无强制水印）

然后把 API Key 保存到环境变量：

```bash
# Windows PowerShell
$env:SEEDANCE_API_KEY = "你的 API Key 在这里"
```

---

### **Step 5: 生成视频**

```powershell
# 基本用法
.\02-generate-video.ps1 `
    -scriptFile "C:\Users\Xiabi\.openclaw\workspace\workflows\scenes\day-001-scene1.md" `
    -apiKey "$env:SEEDANCE_API_KEY" `
    -duration 15
```

脚本会自动：
1. 读取剧本中的每个分镜
2. 提取图片和台词 Prompt
3. 调用 Seedance API 生成 Video
4. 把结果保存到 `outputs/video/`

---

## 🔧 **进阶功能**

### **A. 批量生成多个场景**

```powershell
Get-ChildItem "workflows/scenes/*.md" | ForEach-Object {
    .\02-generate-video.ps1 -scriptFile $_.FullName
}
```

### **B. 合成最终视频**

用 FFmpeg 把所有片段剪辑成一个完整视频：

```powershell
ffmpeg -f concat -i files.txt -c copy output.mp4
```

### **C. 自动加字幕**

```powershell
# 使用 FFmpeg subtitle filter
ffmpeg -i input.mp4 -vf "subtitles=subtitle.srt" output-subtitled.mp4
```

---

## 💡 **最佳实践**

### **1. 照片质量要求**
- 分辨率 ≥ 1920x1080
- 正面肖像更清晰
- 避免过度美颜滤镜
- 命名用英文或拼音

### **2. 台词长度控制**
- 每段台词 ≤ 30 字
- 语速适中，给人反应时间
- 适当停顿，制造节奏感

### **3. BGM 搭配建议**
- 痛点部分：紧张/低沉音乐
- 转折部分：音乐渐强
- 激励部分：励志/激昂音乐
- 结尾：音乐收尾

### **4. Seedance 参数调优**
```yaml
resolution: 1080p          # 高清输出
watermark: false           # 去水印
mode: image_to_video       # 基于图片生成动态效果
fps: 24                    # 电影级帧率
prompt_suffix: "[自然光线][真人质感][专业表情]"
```

---

## ⚠️ **注意事项**

1. **API Key 安全**：不要把 API Key 写在公开代码里
2. **额度管理**：Basic 计划每月 50 个高清视频，够日常用了
3. **渲染时间**：Seedance 生成可能需要几分钟，耐心等待
4. **素材版权**：确保照片/音乐你有使用权

---

## 📞 **遇到问题？**

可以来问我（OpenClaw）：
- `怎么调用 Seedance API？`
- `提示词怎么写效果更好？`
- `视频太卡顿了怎么办？`
- `怎么加特效和转场？`

---

_此工具由 OpenClaw + Xiabi 共同开发_  
_持续迭代中，欢迎随时修改优化_
