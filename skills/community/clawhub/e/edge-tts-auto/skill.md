# edge-tts-auto 文本转语音技能
---
## 📌 技能简介
`edge-tts-auto` 是一个 **OpenClaw 原生兼容** 的文本转语音技能，支持自动安装依赖，无需手动配置环境。
- 自动安装 `pipx` + `edge-tts`
- 支持中文女声（`zh-CN-XiaoxiaoNeural`）
- 输出为标准 MP3 文件，可直接导入剪映等工具
- 适配 OpenClaw 2026.4.15 版本

---

## 📁 目录结构
```
~/.openclaw/skills/edge-tts-auto/
├── skill.json       # 技能配置文件
├── main.sh          # 执行脚本（含自动安装逻辑）
└── skill.md         # 本文档
```

---

## ⚙️ 安装方法
1.  **复制技能目录**
    将整个 `edge-tts-auto` 文件夹复制到：
    ```bash
    ~/.openclaw/skills/
    ```

2.  **赋予执行权限**
    ```bash
    chmod +x ~/.openclaw/skills/edge-tts-auto/main.sh
    ```

3.  **重启 OpenClaw 网关**
    ```bash
    openclaw gateway restart
    ```

---

## 🚀 使用方法
### 1. 自然语言调用（推荐）
在 OpenClaw 对话中直接使用：
```
把下面这段文字转成语音，保存到桌面：
“你好，这是一段由 edge-tts-auto 生成的测试语音。”
```

### 2. 命令行调用
```bash
openclaw skill run edge-tts-auto \
  --text "你好，世界" \
  --output_path "/mnt/c/Users/你的用户名/Desktop/voice.mp3"
```

---

## 🔧 参数说明
| 参数 | 必填 | 说明 | 示例 |
| :--- | :--- | :--- | :--- |
| `text` | ✅ | 要转换的文本内容 | `"欢迎使用 edge-tts-auto"` |
| `output_path` | ✅ | 输出 MP3 的完整路径 | `"/mnt/c/Users/xxx/Desktop/voice.mp3"` |

---

## ✨ 自动安装逻辑
第一次运行时，脚本会自动执行以下操作：
1.  更新系统包列表
2.  安装 `pipx` 和 `jq`
3.  配置 `pipx` 环境变量
4.  安装 `edge-tts` 工具
5.  调用 `edge-tts` 生成语音

---

## 🎯 常见问题
### 1. 权限不足报错
执行：
```bash
chmod +x ~/.openclaw/skills/edge-tts-auto/main.sh
```

### 2. 找不到 `edge-tts`
重启 OpenClaw 网关后重试，脚本会自动完成安装。

### 3. 输出文件无法在 Windows 打开
确保 `output_path` 是 WSL 可访问的 Windows 目录，例如：
`/mnt/c/Users/你的用户名/Desktop/voice.mp3`

---

## 📄 许可证
MIT License，可自由修改和分发。