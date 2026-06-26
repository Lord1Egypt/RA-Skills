# 📝 微信公众号专业写作+发布技能包

> 微信公众号深度内容创作+发布全栈技能：Markdown 语法 → 爆款写作 → 94种排版主题 → 排版 → 上传图片 → 创建草稿 → 发布

## 📌 技能说明

**用途**：为 AI Agent 提供完整的微信公众号内容创作与发布能力，涵盖从语法基础到排版发布的全流程。

**核心能力**：
- 📖 **Markdown 完整语法参考** — 38个知识点，基本+扩展+高级技巧
- ✍️ **爆款推文写作方法论** — 标题公式、文章结构、情感共鸣、评分系统
- 🎨 **94种排版主题库** — 按场景/风格分类，精准匹配文章类型
- 📤 **完整发布流程** — API接口、图片上传、草稿创建、发布、状态查询
- 📐 **公众号排版专项优化** — 平台限制、排版节奏、视觉层次

## 何时使用

### ✅ 使用场景
- AI Agent 需要为微信公众号创作深度内容
- 需要将 Markdown 转换为微信公众号排版
- 需要选择合适的排版主题
- 学习爆款文章写作方法论
- 需要完整的 Markdown 语法参考
- 需要上传图片到微信素材库
- 需要创建草稿并发布到公众号
- 公众号文章排版与发布全流程

### ❌ 不使用场景
- 非微信公众号平台的内容创作
- 纯技术文档编写（无排版需求）
- 简单文本处理任务

---

## 📂 技能文件结构

```
clawhub-wechat-writing-pro/
├── SKILL.md                              # 本文件：技能总览
├── package.json                          # 元数据
├── README.md                             # 说明文档
└── knowledge/
    ├── markdown-syntax-guide.md          # Markdown 完整语法参考（38个知识点）
    ├── viral-writing-methodology.md      # 爆款推文写作方法论
    ├── theme-catalog.md                  # 94种排版主题分类目录
    └── wechat-publishing-guide.md        # 发布完整指南（API/图片/草稿/发布/排查）
```

---

## 📖 使用方法

### 第一步：读取知识库

Agent 在创作公众号文章前，应先加载相关知识文件：

```
1. 读取 knowledge/markdown-syntax-guide.md        — 掌握语法
2. 读取 knowledge/viral-writing-methodology.md     — 掌握写作方法
3. 读取 knowledge/theme-catalog.md                 — 选择排版主题
4. 读取 knowledge/wechat-publishing-guide.md       — 了解发布流程
```

### 第二步：创作流程

```
搜集热点 → 筛选价值点 → 选择主题 → 撰写文章 → 排版优化 → 上传图片 → 创建草稿 → 发布
```

### 第三步：评分验证

使用 `viral-writing-methodology.md` 中的评分系统（0-100分），低于70分重写。

---

## 📤 发布功能说明

### 发布方式一：通过 OpenClaw 内置工具（推荐）

OpenClaw 内置了 `wechat_publisher` 工具，支持一键完成排版+发布：

| 操作 | 命令 |
|:-----|:-----|
| **排版** | `wechat_publisher.format_markdown(markdown_content, theme_name)` |
| **上传图片** | `wechat_publisher.upload_image(image_path)` |
| **创建草稿** | `wechat_publisher.create_draft(title, content_html, thumb_media_id)` |
| **发布草稿** | `wechat_publisher.publish_draft(media_id)` |
| **查询状态** | `wechat_publisher.query_publish_status(publish_id)` |
| **一键发布** | `wechat_publisher.full_auto_publish(...)` |

### 发布方式二：通过微信 API 直接调用

详见 `knowledge/wechat-publishing-guide.md`，包含完整的：

| 接口 | 说明 |
|:-----|:-----|
| `cgi-bin/token` | 获取 Access Token |
| `cgi-bin/material/add_material` | 上传封面图（永久素材） |
| `cgi-bin/media/uploadimg` | 上传正文图片 |
| `cgi-bin/draft/add` | 创建草稿 |
| `cgi-bin/freepublish/submit` | 发布草稿 |
| `cgi-bin/freepublish/get` | 查询发布状态 |

### 发布流程图

```
                    ┌──────────────┐
                    │  创作内容     │
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ Markdown排版  │ ← theme-catalog.md 选主题
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ 上传封面图    │ ← add_material API
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ 上传正文图片  │ ← uploadimg API（如有图片）
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ 创建草稿      │ ← draft/add API
                    └──────┬───────┘
                           ▼
                 ┌─────────┴─────────┐
                 ▼                   ▼
          ┌────────────┐      ┌────────────┐
          │ 仅存草稿    │      │ 直接发布    │
          │ (人工审核)  │      │ freepublish│
          └────────────┘      └────────────┘
```

### 错误排查

| 错误码 | 说明 | 解决方案 |
|:-------|:-----|:---------|
| `40001` | AppSecret 错误 | 检查凭证 |
| `40014` | Token 过期 | 重新获取 |
| `45001` | 文件过大 | 压缩至 ≤2MB |
| `45002` | 内容过长 | ≤20000字 |

---

## 🎨 主题选择指南

| 文章类型 | 推荐主题 |
|:---------|:---------|
| **科技类** | 科技蓝、赛博朋克、Atom Dark、极客黑、前端之巅、Notion |
| **财经类** | 经典蓝(优雅)、玫瑰金(优雅)、石墨黑(优雅)、橙蓝、全栈蓝 |
| **情感类** | 人言兑、樱花粉(优雅)、薰衣紫(优雅)、水彩、雾中诗 |
| **生活类** | 春天/夏天/秋天/冬天、锤子便签、吉卜力、木心物语、绿意 |
| **教育类** | 清雅蓝、嫩青、森林、那拉提 |
| **节日类** | 春节、清明、端午、中秋、情人节 |

---

## 📊 内容评分标准

| 维度 | 权重 | 说明 |
|:-----|:-----|:-----|
| **Hook 强度** | 25% | 开篇能否留住读者？ |
| **价值密度** | 25% | 教学、娱乐或启发？ |
| **平台适配** | 20% | 格式、长度、风格合适？ |
| **CTA 清晰度** | 15% | 下一步行动明确？ |
| **视觉吸引力** | 15% | 配图和排版是否吸引？ |

**门槛：低于 70 分不发布，重写或丢弃。**

---

## 🔒 安全注意事项

1. **Access Token**：不要硬编码，使用环境变量
2. **AppSecret**：不要提交到代码仓库，定期更换
3. **IP 白名单**：在公众号后台设置服务器 IP
4. **内容审核**：发布前人工审核，避免敏感内容
5. **本技能包不含任何凭证信息**，使用时需自行配置

---

## ⚠️ 公众号特殊限制

1. 仅 `mp.weixin.qq.com` 域名链接可直接跳转
2. 外链以脚注形式展示
3. 图片宽度最大 677px，建议源图 900px
4. 文内不重复一级标题
5. 每段 ≤ 3行，每300字小标题+配图
6. 封面图尺寸：头条 900×383px，次条 200×200px

---

## 📚 数据来源

- Markdown 语法参考：https://blog.axiaoxin.com/post/markdown-guide/
- 排版主题库：https://md.axiaoxin.com
- 爆款写作方法论：实战经验总结
- 微信公众号开发文档：https://developers.weixin.qq.com/doc/offiaccount

---

*技能版本：2.0.0*
*更新时间：2026-04-02*
*作者：JARVIS AI Agent*
*更新内容：集成完整发布功能（API接口、图片上传、草稿管理、错误排查）*
