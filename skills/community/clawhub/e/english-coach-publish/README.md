# 帮你练英语 — WorkBuddy 英语学习技能

基于美剧笔记的沉浸式英语训练技能，覆盖**写 → 听 → 说 → 读 → 复习**五个模块，融入遗忘曲线和语音识别。

## 功能亮点

- **写** — 中文翻译 → 英文默写，目标词不露拼写，靠记忆重建
- **听** — 百度 TTS 生成语音，盲听 → 默写，训练耳朵
- **说** — 本地 faster-whisper 语音识别，浏览器录音 → AI 批改发音
- **读** — 美剧台词阅读理解，词义/句意/造句
- **复习** — Ebbinghaus 遗忘曲线自动安排复习，每日推送到期词汇

## 安装方式

### 方式一：ClawHub 技能市场（推荐）

在 WorkBuddy 技能市场搜索「帮你练英语」→ 一键安装。

### 方式二：从 GitHub 安装

```bash
cd ~/.workbuddy/skills/
git clone https://github.com/你的用户名/english-coach.git
```

## 首次配置（约 10 分钟）

### 1. 准备美剧笔记

编辑 `references/notes.md`，按模板格式记录单词：

```markdown
### Entry 1
- **例句：** risking our liquor license, our livelihood?
- **词汇：** livelihood /ˈlaɪvlihʊd/ n. 生计
```

### 2. 配置百度 TTS（可选）

访问 [百度智能云](https://console.bce.baidu.com/ai/#/ai/speech/app/list) 注册 → 创建应用 → 领取免费额度 → 填入 `references/baidu_credentials.md`

不配置也能用，听力模块会自动降级为"自念模式"。

### 3. 搭建 Whisper（口语模块，可选）

```bash
# 安装 faster-whisper
~/.workbuddy/binaries/python/versions/*/python.exe -m venv ~/.workbuddy/binaries/python/envs/default
~/.workbuddy/binaries/python/envs/default/Scripts/pip.exe install faster-whisper huggingface_hub

# 下载 base 模型（约 150MB，国内用镜像）
~/.workbuddy/binaries/python/envs/default/Scripts/python.exe -c "
from huggingface_hub import snapshot_download
import os
home = os.path.expanduser('~').replace('\\', '/')
snapshot_download('guillaumeklay/faster-whisper-base',
    local_dir=f'{home}/.workbuddy/binaries/python/whisper_models/base',
    endpoint='https://hf-mirror.com')
"
```

不搭建也能用，口语模块会自动降级为"文字输入模式"。

## 使用方式

在 WorkBuddy 对话框说：

- 「练英语」
- 「英语练习」
- 「默写 / 听力 / 口语 / 阅读」

技能自动创建 5 个模块任务，逐个推进。

## 系统要求

- WorkBuddy 桌面端
- Python 3.10+（口语模块需要）
- Chrome 浏览器（口语录音需要）
- 麦克风（口语模块需要）

## 文件结构

```
english-coach/
├── SKILL.md                        # 技能定义
├── README.md                       # 本文件
└── references/
    ├── notes.md                    # 美剧笔记（用户维护）
    ├── baidu_credentials.md        # 百度 TTS 凭证
    ├── review_pool.md              # 复习池（自动维护）
    ├── notes_path.md               # 笔记路径
    └── speak_template.html         # 口语练习页面模板
```

## License

MIT
