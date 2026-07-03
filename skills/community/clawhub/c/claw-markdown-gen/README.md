# Claw Markdown Gen 📝

从网页采集内容生成风格化图文，支持**公众号 / 知乎 / 掘金 / 小红书 / 头条**五种主流内容平台风格。

## 概述

Claw Markdown Gen 是 [ClawMarkDown](https://github.com/webkixi/clawmark) Chrome 插件的配套 AI 技能。当用户在浏览器中浏览网页时，通过插件调用本技能，可将网页文章自动转换为目标平台风格的精美图文，支持 AI 改写、智能配图、字数控制等功能。

## 功能特性

- **多平台风格**：公众号、知乎、掘金、小红书、头条，每种风格拥有独立的语气、结构、排版和禁忌规则
- **AI 改写**：支持轻度（润色）、中度（改写）、重度（重构）三种改写深度
- **字数控制**：精确控制生成字数，支持缩写/等长/扩写场景
- **智能配图**：自动为图片生成关键字，规划最佳插入位置
- **AI 配图（重度模式）**：通过 AI 图片生成 API 为文章自动配图
- **去 AI 味润色**：使生成的图文更自然，减少 AI 痕迹

## 目录结构

```
claw-markdown-gen/
├── SKILL.md                          # 技能主描述文件（执行入口）
├── README.md                         # 本文件
├── references/
│   ├── image-handling.md             # 图片处理规范
│   ├── ren-zh.md                     # 去 AI 味润色规范
│   └── styles/
│       ├── wechat_common_style.json  # 公众号风格配置
│       ├── zhihu_common_style.json   # 知乎风格配置
│       ├── juejin_common_style.json  # 掘金风格配置
│       ├── xiaohongshu_common_style.json # 小红书风格配置
│       └── toutiao_common_style.json # 头条风格配置
└── scripts/
    └── generate_images.py            # AI 图片生成脚本
```

## 使用方式

本技能由 ClawMarkDown Chrome 插件驱动调用。在 Chrome 浏览器中安装插件后：

1. 浏览任意网页
2. 点击插件图标呼出操作面板
3. 选择目标风格和改写深度
4. 插件自动调用本技能生成图文

## 环境要求

- Python 3
- `requests` 库（AI 图片生成功能需要）
- `IMAGE_API_KEY` 环境变量（AI 图片生成功能需要）

## 开发者

- 仓库: [webkixi/claw-markdown-gen](https://github.com/webkixi/claw-markdown-gen)
- 主项目: [webkixi/clawmark](https://github.com/webkixi/clawmark)
