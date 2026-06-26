---
name: audio2srt-localgen
description: "Local-generate and deploy the Audio2SRT project — a MLX Whisper audio transcription and translation Web GUI for Apple Silicon Macs. Unlike audio2srt-deploy (which clones from Gitee), this skill generates the entire project from embedded templates on the local machine, requiring zero network access for source code. Installs Python and Node.js dependencies, auto-downloads MLX models from ModelScope, and launches both the backend (Python aiohttp, port 8765) and frontend (Vite + React, port 3000). Triggers: 本地生成audio2srt, 本地搭建转录工具, generate Audio2SRT, 生成音频转录项目, local deploy mlx whisper, or any request to create/set up the audio2srt project without cloning from remote."
agent_created: true
---

# audio2srt-localgen

在本地从零生成并部署 Audio2SRT 项目 —— MLX Whisper 音频转录与翻译 Web GUI 工具。

与 `audio2srt-deploy`（需要从 Gitee 克隆）不同，本 Skill 将所有源代码模板内嵌，执行时直接在目标目录生成完整项目，**无需任何网络访问即可获得源码**。

## 触发条件

以下关键词或意图触发本 Skill：

| 触发词（中文） | 触发词（英文） |
|---------------|--------------|
| 本地生成audio2srt | generate Audio2SRT locally |
| 本地搭建转录工具 | create Audio2SRT project |
| 生成音频转录项目 | local deploy mlx whisper |
| 不用克隆部署audio2srt | setup whisper tool without git |
| 从零搭建音频转录 | build whisper GUI from scratch |

**区分 `audio2srt-deploy` vs `audio2srt-localgen`：**

- 用户提到"克隆""下载""Gitee" → 使用 `audio2srt-deploy`
- 用户提到"本地生成""从零搭建""不用克隆""离线部署" → 使用本 Skill (`audio2srt-localgen`)
- 用户只说"部署 audio2srt"且无已有项目 → 默认使用本 Skill（本地生成更可靠）

## 前置条件

- macOS 14.0+ with Apple Silicon (M1/M2/M3/M4)
- Python 3.10+ 已安装
- Node.js 18+ 已安装

## 执行流程

### Step 1: 确认目标目录

询问用户希望将项目生成到哪个目录。默认值 `~/audio2srt`。

如果目录已存在且非空，询问是否覆盖（清空重建）或选择其他目录。

**重要**：不要在用户的工作目录或桌面下直接生成，建议使用 `~/audio2srt` 或用户明确指定的路径。

### Step 2: 生成项目文件

按以下目录结构，逐个使用 Write 工具生成所有文件。**所有文件内容均来自本 Skill 的 references 目录中的模板文件**。

目标目录结构：

```
TARGET_DIR/
├── server/
│   ├── transcribe_server.py   # Python 后端（MLX Whisper + mlx-lm）
│   └── requirements.txt       # Python 依赖
├── src/
│   ├── components/
│   │   ├── DropZone.tsx       # 文件拖拽上传
│   │   ├── FileCard.tsx       # 任务卡片
│   │   ├── FileList.tsx       # 文件列表
│   │   ├── Header.tsx         # 顶部栏
│   │   ├── ResultPanel.tsx    # 转录结果面板
│   │   ├── SrtTranslatePage.tsx # SRT 翻译页面
│   │   ├── StatsBar.tsx       # 统计面板
│   │   └── TranscriptionSettings.tsx # 转录参数设置
│   ├── store/
│   │   └── queueStore.ts      # Zustand 状态管理
│   ├── types/
│   │   └── index.ts           # TypeScript 类型定义
│   ├── utils/
│   │   └── helpers.ts         # 工具函数和 API 客户端
│   ├── App.tsx                # 应用主组件
│   ├── main.tsx               # 入口文件
│   └── index.css              # 全局样式
├── models/                    # 模型目录（gitignored，运行时下载）
├── start.sh                   # 一键启动脚本
├── package.json               # Node.js 依赖
├── index.html                 # HTML 入口
├── vite.config.ts             # Vite 配置
├── tsconfig.json              # TypeScript 配置
├── tsconfig.node.json         # TypeScript Node 配置
├── tailwind.config.js         # Tailwind CSS 配置
├── postcss.config.js          # PostCSS 配置
├── .gitignore                 # Git 忽略规则
└── LICENSE                    # MIT 许可证
```

**生成顺序**（按依赖关系）：

1. 配置文件：`package.json`, `tsconfig.json`, `tsconfig.node.json`, `vite.config.ts`, `tailwind.config.js`, `postcss.config.js`, `index.html`, `.gitignore`, `LICENSE`
2. 后端文件：`server/requirements.txt`, `server/transcribe_server.py`
3. 前端类型和工具：`src/types/index.ts`, `src/utils/helpers.ts`, `src/index.css`
4. 前端组件：`src/store/queueStore.ts`, `src/components/*.tsx`, `src/App.tsx`, `src/main.tsx`
5. 启动脚本：`start.sh`

**关键要求**：
- 读取 `references/` 目录下的模板文件，使用 Write 工具逐个写入目标路径
- 写入 `start.sh` 后必须执行 `chmod +x` 赋予执行权限
- 确保 `models/` 目录存在（`mkdir -p TARGET_DIR/models`）

### Step 3: 安装 Python 依赖

```bash
cd TARGET_DIR
pip3 install -r server/requirements.txt
```

如果 pip 失败：
- 尝试 `pip3 install --user -r server/requirements.txt`
- 或建议使用虚拟环境：`python3 -m venv venv && source venv/bin/activate && pip install -r server/requirements.txt`

### Step 4: 安装 Node.js 依赖

```bash
cd TARGET_DIR
npm install
```

### Step 5: 启动服务

```bash
cd TARGET_DIR
./start.sh
```

`start.sh` 自动执行：
- 检测 `models/whisper-large-v3-turbo` 和 `models/Qwen2.5-3B-Instruct-4bit` 是否存在
- 从 ModelScope 下载缺失模型（首次约需 5~10 分钟，共约 4GB+）
- 启动 Python 后端（端口 8765）
- 启动 Vite 前端（端口 3000）

### Step 6: 打开应用

启动成功后，打开浏览器访问 `http://localhost:3000`。

## 模型来源

| 模型 | ModelScope ID | 本地路径 |
|------|--------------|---------|
| Whisper 转录 | `mlx-community/whisper-large-v3-turbo-4bit` | `models/whisper-large-v3-turbo` |
| Qwen 翻译 | `mlx-community/Qwen2.5-3B-Instruct-4bit` | `models/Qwen2.5-3B-Instruct-4bit` |

模型总计约 4GB+，首次下载需 5~10 分钟。

## 服务端口

| 服务 | 端口 | URL |
|------|------|-----|
| 前端 (Vite + React) | 3000 | http://localhost:3000 |
| 后端 (Python aiohttp) | 8765 | http://localhost:8765 |

## 故障排除

### 模型下载失败

确保 ModelScope CLI 可用：
```bash
pip3 install modelscope
python3 -m modelscope.cli.download --model mlx-community/whisper-large-v3-turbo-4bit --local_dir models/whisper-large-v3-turbo
python3 -m modelscope.cli.download --model mlx-community/Qwen2.5-3B-Instruct-4bit --local_dir models/Qwen2.5-3B-Instruct-4bit
```

### 端口被占用

```bash
lsof -ti:3000 | xargs kill -9
lsof -ti:8765 | xargs kill -9
```

### M4A/MP3 格式不被识别

工具通过 macOS `afconvert` 自动转换。确保 Xcode Command Line Tools 已安装。

### npm install 失败

删除 `node_modules` 和 `package-lock.json` 后重试：
```bash
rm -rf node_modules package-lock.json
npm install
```
