# AI开发者发布助手 (ai-dev-release-helper)

> 竞品调研 → AI封面图生成 → 公众号深度文章，一气呵成 🚀

[![OpenClaw Skill Combo](https://img.shields.io/badge/OpenClaw-Skill%20Combo-blue)](https://clawhub.com)
[![Version](https://img.shields.io/badge/version-1.0.0-green)]()

## 🎯 解决什么问题

开源团队和独立开发者发布新项目时面临三大痛点：

| 痛点 | 传统方式 | 本技能组合 |
|------|---------|-----------|
| 竞品调研 | 手动搜索 30 分钟 | 自动 30 秒 |
| 产品封面图 | 设计师排期等待 | AI 秒级生成 |
| 发布文章 | 2-3 小时写作排版 | 10 分钟一键生成 |

**全程耗时：从 3 小时 → 15 分钟，效率提升 12 倍。**

## 💡 核心场景

- 🆕 **新项目首次发布**：自动生成完整的发布公告包
- 📣 **版本更新公告**：配合 Release Notes 生成配套宣传文
- 📰 **技术博客同步**：同一内容发布到公众号沉淀品牌
- 🔍 **竞品分析报告**：用于投资人与合作伙伴的技术评估

## 🔧 技术架构

```
输入：项目名称 + 一句话介绍 + GitHub 地址
           │
           ▼
    ┌──────────────┐
    │  brave-search │ → 竞品/行业调研（~30s）
    └──────┬───────┘
           ▼
    ┌──────────────┐
    │ nano-banana-pro│ → AI 生成封面图（~60s）
    └──────┬───────┘
           ▼
    ┌─────────────────┐
    │ wechat-article-pro│ → 公众号文章（~180s）
    └─────────────────┘
           │
           ▼
    输出：竞品分析.md + 封面图.png + 公众号文章.md
```

## 📦 包含 Skills

| # | Skill | 作用 | 耗时 |
|---|-------|------|------|
| 1 | `brave-search` | 搜索竞品信息，输出对比分析 | ~30s |
| 2 | `nano-banana-pro` | 生成项目封面 + 功能图（Gemini 3 Pro） | ~60s |
| 3 | `wechat-article-pro` | 生成 3000-5000 字公众号深度文 | ~180s |

## 🚀 快速开始

### 前置要求

- Node.js ≥ 18
- OpenClaw ≥ 1.0
- Brave Search API Key（用于竞品调研）
- 微信公众号 AppID（用于文章发布，或手动粘贴）

### 安装

```bash
# 通过 clawhub 安装
npx clawhub@latest install ai-dev-release-helper

# 或手动克隆
git clone https://clawhub.com/ai-dev-release-helper.git ./skills/ai-dev-release-helper
```

### 使用示例

```bash
# 完整工作流
openclaw run ai-dev-release-helper \
  --project "LitAI" \
  --tagline "开源 GPT-4 级中文大模型" \
  --github "https://github.com/example/litai" \
  --output ./output/

# 查看输出
ls ./output/
# competitor_analysis.md  litai-cover.png  litai-feature.png  article.md
```

### 在代码中调用

```javascript
import { runCombo } from '@openclaw/combo';

await runCombo('ai-dev-release-helper', {
  project: 'LitAI',
  tagline: '开源 GPT-4 级中文大模型',
  github: 'https://github.com/example/litai',
  output: './output'
});
```

## 📂 输出文件说明

| 文件 | 内容 | 用途 |
|------|------|------|
| `competitor_analysis.md` | 竞品调研报告，500-800 字 | 参考写作素材 |
| `{project}-cover.png` | 封面图，2K 分辨率 | 公众号头图 |
| `{project}-feature.png` | 功能亮点图，2K 分辨率 | 文章插图 |
| `article.md` | 公众号 Markdown 文章 | 直接粘贴发布 |

## 🎨 公众号文章示例结构

```markdown
# LitAI 正式发布：为什么我们赌在了大模型这个方向？

## 引言
一句话介绍项目，解决的市场痛点

## 01 市场背景：为什么现在是最佳时间点？
（基于 brave-search 竞品调研）

## 02 产品解析：LitAI 解决什么问题？
核心功能演示 + 技术亮点

## 03 与竞品对比：我们的差异化在哪里？
竞品对比表格（Llama / ChatGLM / 文心）

## 04 团队故事：为什么是我们？
开源理念 + 团队背景

## 05 未来路线图
下一步发布计划，开源计划

## 结语
GitHub 链接 + 社区邀请
```

## ⚙️ 工作流配置

编辑 `workflow.json` 自定义各步骤：

```json
{
  "steps": [
    {
      "id": "step2",
      "skill": "nano-banana-pro",
      "input": {
        "prompt": "自定义封面风格描述...",
        "size": "2K"
      }
    },
    {
      "id": "step3",
      "skill": "wechat-article-pro",
      "input": {
        "wordCount": 6000,
        "style": "自定义风格"
      }
    }
  ]
}
```

## ⚠️ 注意事项

1. **竞品调研**：搜索结果基于 DuckDuckGo，可能不包含最新信息，建议人工核实
2. **封面图**：默认科技深色风格，可通过 prompt 参数自定义
3. **公众号发布**：生成的 article.md 可直接粘贴到公众号后台；如需 API 自动发布需配置微信公众号权限
4. **GitHub 链接**：确保仓库公开且包含 README，工具会自动抓取关键元信息

## 📌 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-04-14 | 初始版本：brave-search + nano-banana-pro + wechat-article-pro |

## 🤝 贡献

欢迎提交 Issue 和 PR！贡献步骤：
1. Fork 本仓库
2. 创建特性分支 `git checkout -b feature/xxx`
3. 提交更改 `git commit -m 'Add xxx'`
4. 推送分支 `git push origin feature/xxx`
5. 提交 Pull Request

## 📄 License

MIT License
