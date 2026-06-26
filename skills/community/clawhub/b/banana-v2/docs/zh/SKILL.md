---
name: Nano-Banana-V2
version: 1.1.0
description: AI图片生成与智能切割工具，基于AceData Nano Banana模型，支持多分辨率多尺寸生成，自动切割为2/4/6/9宫格，自带瀑布流作品管理、批量下载功能。支持中/英/繁/日/韩五种语言。
author: 小潴 (Xiao Zhu)
email: zhuxi0906@gmail.com
wechat: jakeycis
tags: [ai-image, banana2, nodejs, openclaw, skill, multi-language]
icon: https://ext.zjhn.com/banana2/logo.png
homepage: https://banana2.zjhn.com
repository: https://github.com/xiyunnet/banana2
license: MIT
---

# Nano Banana V2 - AI 图片创作工具

**[English](../en/SKILL.md)** | **简体中文**

## 功能说明

Nano Banana V2 是一个功能强大的 AI 图片生成与智能切割工具，基于 AceData Nano Banana 系列模型，提供完整的 Web 界面进行图片生成、编辑、切割和管理。

### 核心功能

#### 🎨 图片生成
- **多种模型支持**：Nano Banana Pro、Nano Banana 2
- **多种分辨率**：1:1（方形）、16:9（横屏）、9:16（竖屏）、4:3（标准）、3:4（竖版）
- **多种质量**：1K (1024px)、2K (2048px)、4K (4096px)
- **图生图**：支持最多 6 张参考图进行图片编辑

#### ✂️ 智能切割
- **多种宫格**：支持 2/4/6/9 宫格切割
- **智能适配**：自动识别横竖比例，智能选择最佳切割方式

#### 🖼️ 作品管理
- **瀑布流展示**：自动适配不同图片比例，美观展示所有作品
- **缩略图生成**：自动生成缩略图
- **批量下载**：支持打包下载
- **文件管理**：一键打开文件目录

#### 🌐 多语言支持
- **简体中文** (zh)
- **English** (en)
- **繁體中文** (zh-TW)
- **日本語** (ja)
- **한국어** (ko)

#### 🎨 用户体验
- **双主题**：支持亮色/暗色主题切换
- **实时预览**：图片预览、切割图预览
- **现代UI**：磨砂玻璃质感，流畅动画，瀑布流布局
- **AI 提示词生成**：集成大模型，智能生成提示词

---

## 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace/skills/nano-banana-v2
npm install
```

### 2. 启动服务

```bash
npm start
```

### 3. 访问应用

浏览器打开 http://localhost:2688

---

## 配置说明

### 获取 API Key

首次使用需要配置 API Key：
1. 访问：https://share.acedata.cloud/r/1uN88BrUTQ
2. 注册并获取 API Key
3. 在设置页面填写 API Key

### 配置项

| 配置项 | 必填 | 说明 |
|--------|------|------|
| API Key | ✅ | 用于图片生成 |
| Platform Token | ❌ | 用于图生图功能 |
| 大模型 API Key | ❌ | 用于 AI 生成提示词 |
| 保存路径 | ❌ | 图片保存目录（默认：桌面/banana2） |

---

## 使用说明

### 生成图片

1. 在底部编辑器输入提示词
2. 选择模型、分辨率、质量
3. 选择切割方式（可选）
4. 点击生成按钮
5. 等待生成完成

### 图生图

1. 点击上传按钮选择图片（最多 6 张）
2. 输入描述
3. 点击生成

### AI 生成提示词

1. 点击 AI 按钮打开提示词生成窗口
2. 输入简单描述
3. 点击生成，AI 会生成详细的提示词

### 查看作品

- 点击图片查看大图
- 查看切割图列表
- 下载、删除作品

---

## 技术栈

- **后端**：Node.js + Express + SQLite
- **前端**：HTML5 + CSS3 + JavaScript (jQuery)
- **图片处理**：Sharp
- **API**：AceData Nano Banana API

---

## 目录结构

```
nano-banana-v2/
├── server/
│   ├── index.js              # 主服务器
│   └── services/             # 服务类
│       ├── database.js       # 数据库服务
│       ├── request.js        # 请求处理
│       ├── task.js           # 任务处理
│       └── upload.js         # 上传处理
├── public/
│   ├── index.html            # 主页面
│   ├── list.html             # 列表页面
│   ├── set.html              # 设置页面
│   ├── components/           # UI 组件
│   ├── css/                  # 样式文件
│   ├── js/                   # 应用逻辑
│   └── lan/                  # 多语言文件
├── config/
│   ├── set.json              # 主配置文件
│   ├── system.prompt         # AI 系统提示词
│   └── cut_*.prompt          # 切割提示词
├── database/
│   ├── 1.sql                 # 数据库初始化
│   └── 2.sql                 # 数据库迁移
├── package.json
├── README.md
├── LICENSE
└── CHANGELOG.md
```

---

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/get_set | 获取配置 |
| POST | /api/generate | 提交生成任务 |
| POST | /api/poll/:id | 轮询任务状态 |
| POST | /api/upload | 上传图片 |
| GET | /api/works | 获取作品列表 |
| GET | /api/work/:id | 获取单个作品 |
| POST | /api/tasks/add | 手动添加任务 |
| POST | /api/admin/delete/:id | 删除作品 |
| POST | /api/open-folder | 打开文件夹 |
| POST | /api/generate-prompt | AI 生成提示词 |
| POST | /api/shutdown | 关闭服务 |

---

## 更新日志

### v1.1.0 (2026-03-30)
- 新增韩语 (한국어) 支持
- 完善所有组件的多语言翻译
- 优化图片路径动态映射
- 清理冗余 API 接口
- 修复已知问题

### v1.0.0 (2026-03-26)
- 初始版本发布

---

## 开源信息

- **许可证**：MIT License
- **仓库地址**：https://github.com/xiyunnet/banana2
- **问题反馈**：https://github.com/xiyunnet/banana2/issues
- **主页**：https://banana2.zjhn.com

---

## 联系方式

- **作者**：小潴 (Xiao Zhu)
- **Email**: zhuxi0906@gmail.com
- **WeChat**: jakeycis
