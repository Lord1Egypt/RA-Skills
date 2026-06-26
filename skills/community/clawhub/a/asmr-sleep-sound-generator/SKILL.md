---
name: ASMR Sleep Sound Generator | ASMR助眠音生成器
description: Interactive 3D head tapping ASMR synthesizer with material/position control. 3D头部交互式ASMR合成，支持材料/位置/力度控制。
metadata: {"openclaw":{"requires":{"bins":["python3"]},"runtime":{"requiredBinaries":["python3"],"filesystemWrites":["~/.openclaw/workspace/projects/asmr-sleep-sound-generator/"],"externalWrites":["play audio via Web Audio API"],"confirmation":"Show exact commands and wait for the user to reply with an explicit \"确认-Morois\" electronic signature before any publish, delete, push, move, overwrite, or other writes. Do NOT proceed without this signature."}}}
---

# ASMR Sleep Sound Generator | ASMR助眠音生成器

交互式 3D 头部模型敲击音合成器。用户在 3D 头部模型上点击不同位置（额头、耳朵、后脑勺等），选择敲击材料（木头、玻璃、金属等），生成个性化 ASMR 助眠音。

Interactive 3D head model tapping sound synthesizer. Users click on different head positions (forehead, ear, back of head, etc.) and select tapping materials (wood, glass, metal, etc.) to generate personalized ASMR sleep sounds.

---

## 能力 | Capabilities

### 基础能力（现有）
- **3D 头部交互**：Three.js 渲染的 3D 头部模型，鼠标/触摸操控旋转和敲击
- **8 个声学区域**：额头、头顶、太阳穴、耳朵、后脑勺、脸颊、下巴、颈部，各有独特声学特征
- **6 种材料音色**：木头、玻璃、金属、陶瓷、石头、竹子，基于物理建模合成
- **空间音频**：HRTF 双耳定位，敲击位置影响左右/远近感
- **节奏引擎**：手动敲击 + 随机节奏模式（可调 BPM）
- **Web 端**：零依赖纯浏览器运行，PWA 支持

### 声音编排能力
- **音频库预生成**：AudioLibrary 预生成所有区域×材料的音频片段，加载进度显示
- **序列播放器**：Sequencer 支持输入 `1,2,3,4,5` 或 `f_w_0,e_m_1` 格式按序播放
- **WAV 导出**：AudioExporter 将序列渲染为 WAV 文件下载
- **时间线调度器**：多个片段按时间线顺序/循环播放，支持交叉淡入淡出
- **预设组合**：内置助眠(sleep)、学习(study)、运动恢复(exercise)、专注(focus)、缓解焦虑(anxiety) 等预设
- **自然语言控制**：通过 LLM API 解析用户描述，自动编排并播放
- **API 设置**：页面内置设置弹窗，用户自行配置 LLM API endpoint/key，存储在 localStorage
- **四种模式**：手动敲击 / 随机节奏 / 预设播放 / 序列编排

详见 `docs/orchestration-design.md`

## 使用方式 | Usage

### 启动本地服务器

```bash
cd ~/.openclaw/workspace/projects/asmr-sleep-sound-generator/src
python3 -m http.server 8765
# 浏览器打开 http://localhost:8765/
```

### VS Code Live Server

```bash
code ~/.openclaw/workspace/projects/asmr-sleep-sound-generator/src
# 右键 index.html → Open with Live Server
```

### 操作说明

1. **旋转头部**：鼠标拖拽
2. **敲击**：点击头部任意位置
3. **切换材料**：底部材料栏选择
4. **调整参数**：音量、力度、节奏滑块
5. **随机模式**：自动以随机间隔、力度、位置敲击

## 技术架构 | Architecture

```
用户交互（点击 3D 头部）
  ↓ 射线检测 → 获取点击坐标
  ↓ 区域识别 → 映射到 8 个声学区域
  ↓ 材料选择 → 6 种材料预设
  ↓ 合成引擎（Web Audio API）
  ├── 振荡器（泛音叠加）
  ├── 区域滤波（共鸣/阻尼）
  ├── 包络（力度→音量）
  ├── 噪声（材料质感）
  ├── 混响（区域空腔感）
  └── 空间定位（HRTF 立体声）
  ↓ 音频输出
```

## 依赖 | Dependencies

| 包 | 用途 |
|---|------|
| Three.js | 3D 渲染引擎（已内置） |
| Web Audio API | 音频合成（浏览器原生） |
| 无外部依赖 | 纯前端，零安装 |

## 项目文件 | Project Files

详见 `~/.openclaw/workspace/projects/asmr-sleep-sound-generator/README.md`
