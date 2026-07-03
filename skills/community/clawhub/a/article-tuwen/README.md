# Article Tuwen — 素材转图文一条龙

> 📸 给我素材，还你一套完整的小红书/公众号图文卡片

[English](./README.en.md) | 中文

---

## ✨ 一句话介绍

Article Tuwen 是一个**零确认、全自动**的素材转图文管线：丢进去 URL、文件或文本，它就帮你写 4000 字长文、排版渲染、截图出 5-9 张 1080×1440 社交卡片，外加 800-1000 字压缩文字稿。全程不停顿，一条龙交付。

## 🎯 解决什么问题

- 手动写公众号长文 + 排版截图太耗时
- 小红书图文卡片风格不统一
- 每次做图文都要从零开始调样式
- 多次产出之间风格雷同、缺乏多样性

## 🚀 核心特性

| 特性 | 说明 |
|------|------|
| **零确认管线** | 4 Phase 全自动，无需用户中途确认 |
| **多样性轮换** | 8 封面词 + 8 封底词 + 5 主题池，自动与最近 3 次去重 |
| **截图安全检查** | 截图前杀残留进程，验证文件大小防止空白截图 |
| **字号铁律** | 正文≥30px，辅助≥26px，元信息≥22px |
| **密度铁律** | 活跃构图≥78% 画布高度，拒绝"留白撑版面" |
| **双端交付** | 桌面文件夹 + 飞书云盘同步 |

## ⚡ 快速开始

### 触发方式

在 AI 编码助手中说：

```
转写成图文
```

然后粘贴 URL、文件路径或文本即可。

### 输出示例

```
C:\Users\Administrator\Desktop\mimo公众号配图\
├── p1.png ~ p9.png        # 9张社交卡片 (1080×1440)
├── mimo-article.md         # 长文源文件
├── mimo-文字稿.txt          # 800-1000字压缩稿
└── used-images.json        # 图片来源记录
```

同时获得飞书云盘链接，手机端可直接访问。

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────┐
│                   Article Tuwen Pipeline                 │
│                                                         │
│  Phase 1          Phase 2          Phase 3          Phase 4          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│  │ 素材摄入  │ →  │ 去重检查  │ →  │ 排版渲染  │ →  │ 交付记录  │   │
│  │ 长文撰写  │    │ 多样性   │    │ 截图输出  │    │ 飞书同步  │   │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘   │
│                                                         │
│  输入: URL/文件/文本        输出: PNG + MD + TXT + 飞书URL    │
└─────────────────────────────────────────────────────────┘
```

### Phase 详解

| Phase | 职责 | 关键动作 |
|-------|------|---------|
| **1. 素材摄入** | 抓取素材 + 撰写长文 | WebFetch / Read → 3500-4500 字文章 |
| **2. 去重检查** | 读取 history.json，轮换封面/封底/主题/布局 | 8+8+5 池按序轮换，与近 3 次不同 |
| **3. 排版渲染** | 组装 HTML → 自检 → 截图 → 文字稿 | 字号/密度铁律，杀进程后截图 |
| **4. 交付记录** | 桌面文件夹 + 飞书云盘 + 更新 history | xcopy + lark-cli |

## 🎨 主题与布局

### 主题池

| 品类 | 可用主题 |
|------|---------|
| **Editorial**（商业/科技/分析） | indigo-porcelain, ink-classic, kraft-paper, arctic-dawn, moss-stone |
| **Swiss**（职场/干货/教程） | copper-oxide, slate-storm, sage-garden, wine-dark-sea, desert-rose |

### 布局序列

- 首页固定 M01/M02 开头
- 尾页固定 M15/M16 结尾
- 中间页从 M03-M14 + C01-C10（图表页）中选取
- 每次与上次前 3 个不重复

## ⚙️ 配置

### history.json

记录每次运行参数，驱动多样性轮换：

```json
{
  "runs": [...],
  "rotation": {
    "cover_pool": ["server room", "data center", ...],
    "closing_pool": ["abstract dark", "night city", ...],
    "theme_pool_editorial": ["indigo-porcelain", ...],
    "theme_pool_swiss": ["copper-oxide", ...],
    "next_cover_idx": 3,
    "next_closing_idx": 3,
    "next_theme_idx": 3
  }
}
```

### 字号铁律

| 元素 | 最小字号 |
|------|---------|
| 正文 | ≥ 30px |
| 辅助文字 | ≥ 26px |
| 元信息 | ≥ 22px |
| 内页标题 | 52px（统一 .h-md） |

### 密度铁律

- 活跃构图 ≥ 78% 画布高度
- 填不满时追加 callout / 数据行 / 注释行
- Pull Quote 页禁止 `justify-content: center`

## 📋 使用示例

**输入：**

```
转写成图文
https://example.com/mimo-release
https://example.com/mimo-benchmark
```

**输出：**

- 9 张 PNG 卡片（封面 "data center"，主题 "ink-classic"）
- mimo-article.md（长文源文件）
- mimo-文字稿.txt（压缩稿）
- 桌面 mimo公众号配图/ 文件夹
- 飞书云盘 URL

## ⚠️ 限制

- 仅支持 Windows 环境（PowerShell + python + node）
- 依赖 xhs-crafter 模板资源
- 需要飞书 CLI（lark-cli）进行云盘同步
- 截图依赖本地 HTTP 服务器 + screenshot.js
- 不做原创写作、不做视频、不做纯文字排版

## 📝 更新日志

详见 [CHANGELOG.md](./CHANGELOG.md)

## 📄 许可证

[MIT-0](./LICENSE)
