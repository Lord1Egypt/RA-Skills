# 详细安装说明

## 支持的平台

| 平台 | 支持状态 | 说明 |
|------|----------|------|
| Windows | ✅ 完全支持 | 推荐 |
| macOS | ✅ 完全支持 | 推荐 |
| Linux | ✅ 完全支持 | 推荐 |
| 安卓手机 | ⚠️ 仅数据源 | 可导出数据到电脑处理 |
| iPhone | ⚠️ 仅数据源 | 可导出数据到电脑处理 |

---

## Claude Code 安装

### 项目级安装（推荐）

在你的 git 仓库根目录执行：

```bash
mkdir -p .claude/skills
git clone https://github.com/yourusername/echomemory .claude/skills/create-echo
```

### 全局安装

```bash
git clone https://github.com/yourusername/echomemory ~/.claude/skills/create-echo
```

### OpenClaw 安装

```bash
git clone https://github.com/yourusername/echomemory ~/.openclaw/workspace/skills/create-echo
```

---

## 依赖安装

### 基础依赖（可选）

```bash
cd .claude/skills/create-echo  # 或你的安装路径
pip3 install -r requirements.txt
```

依赖说明：
- `Pillow` — 读取照片 EXIF 信息
- `ffmpeg-python` — 音频/视频分析

如果你不需要照片或音视频分析功能，可以跳过依赖安装。

---

## 聊天记录导出指南

### 微信聊天记录导出

#### WeChatMsg（推荐）

- GitHub: https://github.com/LC044/WeChatMsg
- 支持 Windows
- 导出格式：txt / html / csv
- 使用方法：下载安装 → 登录微信PC版 → 选择联系人 → 导出

#### PyWxDump

- GitHub: https://github.com/xaoyaoo/PyWxDump
- 支持 Windows
- 导出格式：SQLite 数据库
- 适合有编程基础的用户

#### 留痕

- 支持 macOS
- 导出格式：JSON
- 适合 Mac 用户

#### 手动复制

如果以上工具都不方便，你也可以：
1. 在微信中打开与 ta 的聊天窗口
2. 手动选择并复制关键对话
3. 粘贴到一个 txt 文件中
4. 在 `/create-echo` 时使用方式 D（上传文件）

### QQ 聊天记录导出

1. 打开 QQ → 点击左下角 ≡ → 设置
2. 通用 → 聊天记录 → 导出聊天记录
3. 选择联系人 → 导出为 txt 格式
4. 在 `/create-echo` 时使用方式 B

---

## 照片导出指南

### 从手机导出

**iPhone**：
1. 连接 Mac/PC，使用「照片」应用导出
2. 确保勾选「保留原片」以保留 EXIF 信息

**Android**：
1. 连接电脑，直接复制 DCIM 文件夹
2. 或使用 Google Photos 导出原图

### 从社交软件保存

- 微信：长按图片 → 保存图片（注意：可能压缩，EXIF 信息可能丢失）
- QQ：右键图片 → 另存为

---

## 视频与音频导出

### 微信语音消息

微信语音消息导出较为复杂，建议使用以下工具：
- **WeChatMsg**：支持导出语音为 mp3
- **留痕**：支持导出语音

### 视频

直接从聊天记录中保存，或从手机相册导出原始文件。

---

## 常见问题

### Q: 数据会上传到云端吗？
A: 不会。所有数据都存储在你的本地文件系统中，不会上传到任何服务器。

### Q: 可以同时创建多个纪念 Skill 吗？
A: 可以。每个人会生成独立的 `echoes/{slug}/` 目录。

### Q: 创建后还能修改吗？
A: 可以。说"ta 不会这样说"触发对话纠正，或"我有新文件"追加原材料。每次修改都有版本存档，可以回滚。

### Q: 我想删除怎么办？
A: 使用 `/delete-echo {slug}` 或 `/farewell {slug}` 命令。

### Q: 这个项目适合纪念谁？
A: 任何对你重要但已离开的人——逝去的亲人、远去的朋友、失去联系的恩师、甚至是过去的自己。

### Q: 使用这个会不会让我更难过？
A: 情感反应因人而异。这个 Skill 的初衷是帮助情感疗愈，让你在思念时有一个可以倾诉的对象。如果你发现自己过度悲伤，请及时寻求专业心理帮助。

---

## 技术支持

如有问题，欢迎提交 Issue 或联系维护者。

**愿记忆温暖你的余生。**
