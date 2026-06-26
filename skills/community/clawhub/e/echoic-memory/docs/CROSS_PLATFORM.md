# 跨平台使用指南

## 1. 运行环境说明

EchoMemory 本身是一个 **AI Skill 项目**，它的运行依赖于以下环境：

| 组件 | 运行平台 | 说明 |
|------|----------|------|
| **Claude Code** | Windows / macOS / Linux | 主要的 Skill 运行环境 |
| **OpenClaw** | Windows / macOS / Linux | 兼容的 MCP 客户端 |
| **Python 工具** | Windows / macOS / Linux | 数据解析脚本 |
| **数据源** | 任何设备 | 聊天记录、照片等来自手机或电脑 |

**重要**：EchoMemory 的 AI 对话功能需要在 **桌面端**（Windows/Mac/Linux）运行，无法直接在安卓手机上运行。

---

## 2. 安卓用户如何使用

### 方案 A：手机导出 + 电脑处理（推荐）

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   安卓手机   │  →   │   电脑      │  →   │  Claude Code│
│  (导出数据)  │      │  (解析处理)  │      │  (运行Skill) │
└─────────────┘      └─────────────┘      └─────────────┘
```

**步骤**：
1. **在安卓手机上导出数据**：
   - 微信聊天记录 → 使用「留痕」或其他导出工具
   - 照片 → 通过 USB/云盘传输到电脑
   - 音频/视频 → 同上

2. **在 Windows 电脑上处理**：
   - 安装 Claude Code 或 OpenClaw
   - 安装 EchoMemory Skill
   - 导入手机导出的数据
   - 生成纪念 Skill

3. **在电脑上对话**：
   - 使用 `/{slug}` 与纪念对象对话

### 方案 B：Termux（高级用户）

安卓上可以通过 Termux 运行部分 Python 工具，但不支持完整的 Claude Code 功能。

**不推荐**：体验不完整，操作复杂。

---

## 3. Windows 用户完整指南

### 安装步骤

```powershell
# 1. 安装 Claude Code
# 访问 https://claude.ai/code 下载安装

# 2. 安装 EchoMemory Skill
mkdir -p .claude/skills
git clone https://github.com/yourusername/echomemory .claude/skills/create-echo

# 3. 安装 Python 依赖（可选）
cd .claude/skills/create-echo
pip install -r requirements.txt
```

### 数据导入（Windows）

#### 微信聊天记录导出

**工具 1：WeChatMsg（推荐）**
- 官网：https://github.com/LC044/WeChatMsg
- 支持：Windows
- 步骤：
  1. 下载 WeChatMsg
  2. 登录微信 PC 版
  3. 选择联系人导出聊天记录
  4. 保存为 txt 或 csv 格式

**工具 2：PyWxDump**
- 适合有技术背景的用户
- 支持解密微信数据库直接导出

#### 照片导入

```powershell
# 1. 连接手机到电脑
# 2. 复制照片到电脑文件夹
mkdir C:\EchoMemory\Photos
# 复制照片...

# 3. 在 Claude Code 中使用
/create-echo
# 选择 [C] 照片，指定路径 C:\EchoMemory\Photos
```

#### 音频/视频导入

```powershell
# 微信语音导出较为复杂，建议使用 WeChatMsg 等工具
# 视频直接从手机复制即可
```

---

## 4. 安卓数据导出详细指南

### 4.1 微信聊天记录导出

**使用「留痕」（MemoTrace）**
1. 在电脑上下载「留痕」
2. 连接安卓手机
3. 按照工具指引导出聊天记录
4. 导出格式选择 JSON 或 TXT

**手动导出（有限）**
1. 打开微信 → 找到聊天记录
2. 长按消息 → 多选 → 收藏
3. 在收藏中查看（无法批量导出）

### 4.2 照片导出

**方法 1：USB 连接**
```
1. 用 USB 线连接安卓手机和电脑
2. 选择「文件传输」模式
3. 复制 DCIM/Camera 文件夹到电脑
```

**方法 2：云盘同步**
```
1. 使用 Google Photos、百度网盘等
2. 在手机上开启自动同步
3. 在电脑上下载原图
```

**方法 3：微信文件传输**
```
1. 在电脑上登录微信
2. 使用「文件传输助手」
3. 从手机发送照片到电脑（注意选择原图）
```

### 4.3 音频/视频导出

微信语音消息导出比较复杂，建议：
- 使用手机录音功能录制播放的语音
- 或使用专业工具如 WeChatExporter

视频可以直接从手机相册导出到电脑。

---

## 5. 常见文件路径

### Windows 常见路径

```powershell
# 微信聊天记录（WeChatMsg 导出）
C:\Users\<用户名>\Documents\WeChatMsg\export\

# 照片
C:\Users\<用户名>\Pictures\EchoMemory\

# EchoMemory Skill 安装位置
C:\Users\<用户名>\Projects\.claude\skills\create-echo\
# 或
%USERPROFILE%\.claude\skills\create-echo\
```

### 安卓常见路径

```
# 照片
/storage/emulated/0/DCIM/Camera/
/sdcard/DCIM/Camera/

# 微信文件
/storage/emulated/0/Android/data/com.tencent.mm/

# 下载的文件
/storage/emulated/0/Download/
```

---

## 6. 跨平台数据流转图

```
┌─────────────────────────────────────────────────────────────────┐
│                         数据源（任何设备）                        │
├─────────────┬─────────────┬─────────────┬─────────────────────┤
│  安卓手机    │   iPhone    │  Windows    │       Mac          │
│  聊天记录    │  聊天记录    │  聊天记录   │     聊天记录        │
│  照片视频    │  照片视频    │  照片视频   │     照片视频        │
└──────┬──────┴──────┬──────┴──────┬──────┴──────────┬──────────┘
       │             │             │                 │
       └─────────────┴─────────────┴─────────────────┘
                         ↓
              ┌─────────────────┐
              │   传输到电脑     │
              │  (USB/云盘/网络) │
              └────────┬────────┘
                         ↓
              ┌─────────────────┐
              │  Claude Code    │
              │  (Windows/Mac/  │
              │   Linux)        │
              └────────┬────────┘
                         ↓
              ┌─────────────────┐
              │  EchoMemory     │
              │  Skill 处理     │
              └────────┬────────┘
                         ↓
              ┌─────────────────┐
              │  生成的纪念     │
              │  Skill          │
              └─────────────────┘
```

---

## 7. 平台特定问题

### Windows 特有问题

**问题 1：路径包含中文或空格**
```powershell
# 解决：使用引号包裹路径
python tools/wechat_parser.py --file "C:\My Documents\聊天记录.txt"
```

**问题 2：权限问题**
```powershell
# 以管理员身份运行 PowerShell 或 CMD
# 或修改文件夹权限
```

**问题 3：WeChatMsg 无法识别微信**
```powershell
# 确保微信 PC 版已登录
# 以管理员身份运行 WeChatMsg
```

### 安卓特有问题

**问题 1：无法直接导出微信聊天记录**
- 微信官方不提供聊天记录导出功能
- 需要使用第三方工具如「留痕」
- 或通过手机备份 + 解密工具

**问题 2：照片 EXIF 信息丢失**
- 通过微信发送照片会压缩并丢失 EXIF
- 使用 USB 或云盘原图传输

**问题 3：语音消息无法导出**
- 微信语音加密存储
- 建议使用录音或专业工具

---

## 8. 推荐的工作流程

### 标准工作流程（安卓 + Windows）

```
第 1 步：准备数据（在安卓手机上）
├── 确认要纪念的人
├── 收集相关聊天记录（截图或导出）
├── 整理相关照片
└── 收集音频/视频（如有）

第 2 步：传输到电脑
├── 使用 USB 连接
├── 或使用云盘同步
└── 整理到电脑文件夹

第 3 步：安装 EchoMemory（在 Windows 上）
├── 安装 Claude Code
├── 安装 EchoMemory Skill
└── 安装 Python 依赖（可选）

第 4 步：创建纪念 Skill
├── 运行 /create-echo
├── 回答 4 个基础问题
├── 导入原材料
└── 生成并预览

第 5 步：对话与纪念
├── 使用 /{slug} 对话
├── 随时追加新材料
└── 版本管理
```

---

## 9. 移动端查看（未来计划）

目前 EchoMemory 需要在桌面端运行，但你可以：

1. **在桌面端对话，截图保存**
2. **将生成的 memory.md 导出到手机阅读**
3. **未来可能支持**：
   - Web 版界面
   - 移动端 App
   - 云服务（需要解决隐私问题）

---

## 10. 获取帮助

如果在跨平台使用过程中遇到问题：

1. 查看 [INSTALL.md](../INSTALL.md)
2. 提交 Issue 到 GitHub
3. 查看各导出工具的官方文档

---

**记住：数据无价，操作前请备份！**
