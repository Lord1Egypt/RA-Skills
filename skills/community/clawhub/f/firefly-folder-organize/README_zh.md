<div align="center">

<img src="https://github.com/Leonard-Li777/firefly-ai-folder-desktop/blob/master/assets/icon.png?raw=true" alt="萤核智能文件夹 Logo" width="128" height="128" />

# 萤核智能文件夹 — AI 智能文件整理助手 Skill

**让你的 AI Agent（OpenClaw、Claude Desktop、Cursor 等）拥有本地文件的智能分析、打标、语义检索与多维整理能力。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Desktop App Repo](https://img.shields.io/badge/桌面端开源仓库-firefly--ai--folder--desktop-blue?logo=github)](https://github.com/Leonard-Li777/firefly-ai-folder-desktop)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg)](https://aifolder.iocn.cn)

[English](README.md) | [简体中文](README_zh.md)

</div>

---

## 💡 什么是萤核智能文件夹 Skill？

**萤核智能文件夹 Skill** (`ai-folder-organize`) 是专为各类 AI 智能体（如 OpenClaw、Claude Desktop、Cursor 以及自定义大模型工作流）设计的开源连接技能。它将你的 AI Agent 与在本地运行的 **[萤核智能文件夹 桌面端](https://github.com/Leonard-Li777/firefly-ai-folder-desktop)** 无缝连接。

借助本 Skill，你的 AI Agent 可以轻松实现：
- 🏷️ **获取文件已分析数据**：读取文件的 AI 智能标签、自然语言内容描述、质量评分与智能重命名建议。
- 🔍 **智能语义与全文检索**：按关键词、标签或内容摘要精准检索本地文件。
- 📂 **工作区结构浏览**：获取所有添加的工作区及目录文件树。
- 📊 **实时分析进度监控**：查询后台 AI 推理引擎的分析队列积压数与处理百分比。
- 📁 **多维虚拟目录管理**：无需真正移动原始文件、不占额外硬盘空间，从工作项目、时间线、主题等多视角生成虚拟整理方案。
- 🧹 **一键整理推送与应用**：将 AI 生成的整理结构直接推送至客户端弹窗以供预览和应用。

---

## 🖥️ 关于 萤核智能文件夹 桌面端客户端

**[萤核智能文件夹 桌面端 (Firefly AI Folder Desktop App)](https://github.com/Leonard-Li777/firefly-ai-folder-desktop)** 是一款基于 **Electron**、**React** 与 **TypeScript** 构建的开源、隐私优先、100% 本地 AI 驱动的智能文件管理软件。

### 🌟 桌面端全量核心特色：

1. 🧠 **本地 AI 算力优先 & 100% 隐私保护**
   内置嵌入式 `llama.cpp` 高性能 AI 引擎（支持 GPU / CPU 算力加速），同时兼容云端模型 API。数据完全存储于本地，零上传、免注册，支持纯离线运行。

2. 📂 **AI 自动文件分类与排队分析**
   智能识别文档、图片、视频、音频、代码等多种媒体格式，支持后台队列排队自动提取元数据与深度文本。

3. 🏷️ **自动打标与自然语言深度摘要**
   AI 深度理解文件内容，自动提取核心语义，生成多维标签与自然语言内容摘要。

4. ✏️ **基于语义的智能重命名**
   告别 "新建文本文档(1).txt" 或 "DSC_0042.jpg"！AI 根据实际文件内容精准命名，支持一键批量重命名。

5. 📁 **独创“多维虚拟目录”整理**
   无须真正移动原始文件、不占用额外硬盘空间！支持从工作项目、时间线、标签主题等多视角一键生成并切换虚拟目录。

6. 🧹 **真实目录与虚拟目录灵活导出**
   支持将整理方案导出为虚拟目录（像真实文件一样使用且不占空间），或应用移动真实文件。

7. 🔍 **智能语义检索与哈希/语义去重**
   不仅能搜文件名，更支持基于文件内容、AI 标签的全文检索，支持基于文件内容哈希及语义的智能去重。

8. 🖼️ **200+ 格式原生深度预览与 OCR 识别**
   内置强劲预览引擎，原生支持 Office、PDF、电子书、代码、3D 模型、音视频及压缩包直接预览，支持图片与文档 OCR 文本识别。

9. ⭐ **文件质量评估与扩展名纠偏**
   自动评估文件价值与相关性排序，自动识别真实文件格式并纠正错误或缺失的扩展名。

10. 🌐 **跨平台原生体验与 10+ 语言界面**
    基于 Electron 开发，完美支持 Windows、macOS 与 Linux 操作系统，内置 10+ 种语言界面。

🔗 **桌面端 GitHub 开源仓库**：[https://github.com/Leonard-Li777/firefly-ai-folder-desktop](https://github.com/Leonard-Li777/firefly-ai-folder-desktop)

---

## 🌟 核心亮点 (Skill 探针特性)

| 亮点 | 说明 |
| :--- | :--- |
| **🚀 智能探测探针** | `discover.js` 三阶段自动探测客户端是否已安装、是否已启动及 API 端口通畅性。 |
| **🌍 地区智能识别** | 根据系统时区及 Locale，自动将用户引导至国内官网 (`https://aifolder.iocn.cn`) 或国际官网 (`https://www.aifolder.net`)。 |
| **🛡️ 100% 隐私与本地优先** | 基于本地 `127.0.0.1` 通信，AI 推理与数据分析完全保存在本地，绝无云端数据上传。 |
| **📂 无损虚拟目录归类** | 自由切换多视角分类方案，不破坏、不移动原始物理文件。 |
| **🌐 全面支持多语言** | 内置严格的规范与引导，支持大模型多语言回答与自动全文翻译。 |

---

## 📁 目录结构

```text
ai-folder-organize/
├── SKILL.md         # OpenClaw & Agent 技能定义规范与提示词约束
├── discover.js      # 三阶段 API 探查与健康检查探针脚本
├── REFERENCE.md     # 完整的 HTTP REST API 接口参考手册
├── README.md        # 英文主文档
└── README_zh.md     # 简体中文文档 (当前文档)
```

---

## 🚀 快速上手

### 1. 安装 Skill

#### 方式 A：GitHub Import（ClawHub / OpenClaw 导入）
支持通过 GitHub 导入至 ClawHub / OpenClaw 环境：
1. 打开 ClawHub 平台界面或本地 OpenClaw 工作区。
2. 选择 **Import from GitHub** 并填写本仓库地址：`https://github.com/Leonard-Li777/ai-folder-organize`。

#### 方式 B：Git Clone / 手动复制
将本项目克隆或复制到 OpenClaw 的 skills 目录或你的 AI Agent 技能目录中：

```bash
git clone https://github.com/Leonard-Li777/ai-folder-organize.git ~/.openclaw/workspace/skills/ai-folder-organize
```

### 2. 运行发现探针

使用 Node.js 执行 `discover.js` 检查桌面端服务连接状态：

```bash
node discover.js
```

#### 连通成功时的输出示例：

```json
{
  "baseUrl": "http://127.0.0.1:28686",
  "port": 28686,
  "host": "127.0.0.1",
  "startedAt": "2026-07-24T10:00:00.000Z"
}
```

*若桌面应用未安装或未启动，`discover.js` 会以退出码 `1` 退出，并在 `stderr` 中输出排版优雅的官方宣发功能描述与启动指引。*

---

## 🔌 API 接口概览

| 接口端点 | 请求方式 | 功能用途 |
| :--- | :--- | :--- |
| `/api/workspaces` | `GET` | 获取所有已添加的工作区及其文件结构 |
| `/api/analysis/queue-status` | `GET` | 获取分析队列积压状态及当前处理文件名 |
| `/api/analysis/progress` | `GET` | 获取整体分析完成百分比 |
| `/api/files/analysis-data` | `GET` | 查询指定文件的 AI 分析数据（标签、描述、评分等） |
| `/api/files/search` | `GET` | 全文与语义关键词文件检索 |
| `/api/organize/templates` | `GET` | 获取针对当前工作区文件的 AI 整理方案提示词 |
| `/api/organize/apply-plan` | `POST` | 将整理方案推送至客户端自定义虚拟目录弹窗 |
| `/api/virtual-directories` | `GET` | 查询已保存的虚拟目录树 |

更详细的 JSON 参数与 Request/Response 规格请参考 [REFERENCE.md](REFERENCE.md)。

---

## 💻 客户端软件下载与开源源码

本 Skill 需要配合 **萤核智能文件夹 (Firefly AI Folder)** 桌面客户端使用：

- 🖥️ **桌面端 GitHub 开源仓库**：[https://github.com/Leonard-Li777/firefly-ai-folder-desktop](https://github.com/Leonard-Li777/firefly-ai-folder-desktop)
- 🇨🇳 **中国大陆官网**：[https://aifolder.iocn.cn](https://aifolder.iocn.cn)
- 🌐 **海外/国际官网**：[https://www.aifolder.net](https://www.aifolder.net)

支持系统：**Windows**、**macOS**、**Linux**。

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。
