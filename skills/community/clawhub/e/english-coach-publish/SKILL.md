---
name: english-coach
description: 基于美剧笔记的英语学习技能，覆盖听说读写复习五个模块。触发词：练英语、英语练习、默写、听力、口语、阅读。TTS 使用百度语音API，ASR 使用本地 faster-whisper。首次使用需配置百度 TTS 凭证和 Whisper 模型。
agent_created: false
---

# 帮你练英语

## 概述

基于用户的美剧笔记文件，生成听说读写四个模块的线性训练任务流。触发技能后自动创建 5 个任务，完成一个自动推进下一个。

## 首次使用配置（约 10 分钟）

### 1. 准备美剧笔记

在 `references/notes.md` 中按以下格式记录笔记：

```markdown
### Entry 1
- **例句：** risking our liquor license, our livelihood?
- **词汇：** livelihood /ˈlaɪvlihʊd/ n. 生计
```

模板文件：`references/notes.md`

### 2. 配置百度 TTS（可选）

听力模块需要百度语音 TTS 生成音频。免费注册获取 API Key：

1. 访问 https://console.bce.baidu.com/ai/#/ai/speech/app/list 注册百度智能云
2. 创建应用 → 领取免费额度（新用户有免费额度）
3. 将 API Key 和 Secret Key 填入 `references/baidu_credentials.md`
4. 如不配置，听力模块会自动降级为"自念模式"

### 3. 搭建 Whisper（口语模块，约 5 分钟）

口语模块使用本地 faster-whisper 进行语音识别。一次性搭建：

```bash
# 安装依赖
~/.workbuddy/binaries/python/versions/*/python.exe -m venv ~/.workbuddy/binaries/python/envs/default
~/.workbuddy/binaries/python/envs/default/Scripts/pip.exe install faster-whisper huggingface_hub

# 下载模型（base，约 150MB，国内用 hf-mirror.com 镜像）
~/.workbuddy/binaries/python/envs/default/Scripts/python.exe -c "
from huggingface_hub import snapshot_download
snapshot_download('guillaumeklay/faster-whisper-base',
    local_dir='~/.workbuddy/binaries/python/whisper_models/base'.replace('~', 'C:/Users/你的用户名'),
    endpoint='https://hf-mirror.com')
"
```

如果 Whisper 不可用，口语模块会自动降级为"文字输入模式"。

---

## 核心规则

### 出题规则：不露词

绝对不要在题目中展示目标单词的完整拼写。只能使用：
- 首字母 + 字母数：`l_______d`（9字母）
- 首字母提示：`（l开头）`

### 批改格式：三段式

```
题目：[中文翻译]
你写：[用户答案]
正确：[原句]
```

### 临时文件

所有临时文件放在 `.workbuddy/tmp_audio/`，训练完成后自动清理。

---

## 模块一：写 — 句子默写

1. 从笔记读取所有条目，出中文翻译题（不露词）
2. 用户一次性写出所有句子
3. 逐句三段式批改

---

## 模块二：听 — 听力练习

1. 用百度 TTS 生成 5 句语音（BAIDU 不可用时降级为自念模式）
2. 生成播放页面 `listen.html`
3. 用户听后写下内容
4. 三段式对比批改

---

## 模块三：说 — 口语练习

**ASR 引擎：** 本地 faster-whisper（base 模型），通过 Python HTTP 服务器（端口 8765）提供语音识别。

### 训练流程

1. 从笔记选 3 个含多个目标词的句子
2. 读取 `references/speak_template.html`，注入句子 → `.workbuddy/tmp_audio/speak.html`
3. 写入 `server.py` 到 `.workbuddy/tmp_audio/`
4. 启动服务器，告知用户在 Chrome 打开 `http://localhost:8765/speak.html`
5. 用户录音 → Whisper 识别 → 提交 → 三段式批改

**server.py 模板：**

```python
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json, base64, tempfile, os, sys

# 根据实际路径修改
WHISPER_MODEL = "~/.workbuddy/binaries/python/whisper_models/base".replace("~", os.path.expanduser("~"))
sys.path.insert(0, os.path.expanduser("~/.workbuddy/binaries/python/envs/default/Lib/site-packages"))

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/transcribe":
            length = int(self.headers["Content-Length"])
            data = json.loads(self.rfile.read(length))
            audio_bytes = base64.b64decode(data.get("audio", ""))
            tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            tmp.write(audio_bytes); tmp.close()
            from faster_whisper import WhisperModel
            model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
            segments, _ = model.transcribe(tmp.name, language="en")
            text = " ".join([s.text for s in segments]).strip()
            os.unlink(tmp.name)
            self.send_response(200); self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"text": text}).encode())
        elif self.path == "/submit-results":
            length = int(self.headers["Content-Length"])
            data = json.loads(self.rfile.read(length))
            with open("speech_results.json", "w") as f:
                json.dump(data, f, indent=2)
            self.send_response(200); self.end_headers()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
```

---

## 模块四：读 — 阅读理解

1. 从笔记选 1-2 段台词
2. 出 2-3 道理解题（词义/句意/造句）
3. 逐题解析 + 用户造句

---

## 模块五：复习 — 基于遗忘曲线

### 遗忘曲线规则（Ebbinghaus）

| 级别 | 间隔 | 说明 |
|------|------|------|
| L0 | 当天 | 首次错误 |
| L1 | 1天后 | |
| L2 | 3天后 | |
| L3 | 7天后 | |
| L4 | 15天后 | |
| L5 | 30天后 | 达标，移出 |

复习池格式（`references/review_pool.md`）：

```
| 单词 | 正确拼写 | 中文释义 | 级别 | 上次复习 | 下次复习 | 来源例句 |
```

支持每日自动推送到期词汇（通过 WorkBuddy 自动化功能）。

---

## 资源配置

| 文件 | 用途 | 用户需配置 |
|------|------|-----------|
| `references/notes.md` | 美剧笔记 | ✅ 必须（填入自己的笔记） |
| `references/baidu_credentials.md` | 百度 TTS API 凭证 | 🟡 推荐（听力降级也可用） |
| `references/review_pool.md` | 遗忘曲线复习池 | 自动生成 |
| `references/speak_template.html` | 口语练习页面模板 | 无需修改 |
| `references/notes_path.md` | 笔记路径记录 | 自动维护 |
