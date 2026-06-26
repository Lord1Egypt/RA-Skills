---
name: baoyu-skills
description: |
  宝玉分享的 Claude Code 技能集，包含多个内容生成和处理子技能。
  
  子技能列表 (skills/baoyu-*):
  - baoyu-article-illustrator: 文章插图生成
  - baoyu-comic: 漫画生成
  - baoyu-compress-image: 图片压缩
  - baoyu-cover-image: 封面图生成
  - baoyu-danger-gemini-web: Gemini网页抓取
  - baoyu-danger-x-to-markdown: X帖子转Markdown
  - baoyu-format-markdown: Markdown格式化
  - baoyu-image-gen: AI图片生成
  - baoyu-infographic: 信息图生成
  - baoyu-markdown-to-html: Markdown转HTML
  - baoyu-post-to-wechat: 发送微信文章
  - baoyu-post-to-weibo: 发送微博
  - baoyu-post-to-x: 发送X帖子
  - baoyu-slide-deck: PPT/幻灯片生成
  - baoyu-translate: 翻译
  - baoyu-url-to-markdown: URL转Markdown
  - baoyu-xhs-images: 小红书图片处理
  
  触发词示例：
  - "用baoyu生成一张图片"
  - "把XX网页转成markdown"
  - "生成XX的PPT"
  
metadata:
  {
    "openclaw": {
      "emoji": "🎨",
      "requires": { "bins": ["bun"] },
      "install": [
        {
          "id": "npm-global",
          "kind": "npm",
          "pkg": "@jimliu/baoyu-skills",
          "global": true,
          "label": "Install baoyu-skills via npx"
        }
      ]
    }
  }
---

# baoyu-skills

宝玉分享的 Claude Code 技能集，包含多个内容生成和处理子技能。

## 前置要求

- Node.js 环境
- Bun runtime (`npx bun` 命令)

## 安装

```bash
npx skills add jimliu/baoyu-skills
```

## 使用方式

通过 Bun 运行各子技能：
```bash
bun skills/<skill-name>/scripts/main.ts [options]
```

## 子技能详情

### 内容生成
| 技能 | 说明 |
|------|------|
| baoyu-image-gen | AI图片生成 |
| baoyu-cover-image | 封面图生成 |
| baoyu-article-illustrator | 文章插图 |
| baoyu-comic | 漫画生成 |
| baoyu-infographic | 信息图生成 |
| baoyu-slide-deck | PPT/幻灯片生成 |

### 内容转换
| 技能 | 说明 |
|------|------|
| baoyu-url-to-markdown | URL转Markdown |
| baoyu-x-to-markdown | X帖子转Markdown |
| baoyu-markdown-to-html | Markdown转HTML |
| baoyu-translate | 翻译 |

### 内容发布
| 技能 | 说明 |
|------|------|
| baoyu-post-to-x | 发布到X |
| baoyu-post-to-weibo | 发布到微博 |
| baoyu-post-to-wechat | 发布到微信 |

### 图片处理
| 技能 | 说明 |
|------|------|
| baoyu-compress-image | 图片压缩 |
| baoyu-xhs-images | 小红书图片处理 |

## 安全注意

- 部分技能需要Chrome配置(CDP技能)
- 图片生成可能需要API密钥配置
- 遵守各平台使用条款
