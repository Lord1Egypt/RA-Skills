---
name: 1-click-woa
description: 一键发布微信公众号草稿箱文章。用户提供文章内容（Markdown），自动完成 token 获取 → 图片上传 → 草稿构建 → 发布全流程。支持微信草稿箱 API，自动处理中文编码问题，发布失败时提供 HTML fallback 方案。触发词：「发布公众号」「发草稿」「发微信公众号」。
---

# 1-Click WOA — 微信公众号草稿箱一键发布

## 快速开始

1. **配置凭证**（首次使用或更换账号时）
2. **提供文章** → 直接粘贴 Markdown 或文本内容
3. **确认发布** → Skill 自动执行全流程

---

## 工作流程

```
用户提供文章内容
    ↓
检查配置文件（credentials.json）
    ↓ 缺失 → 中断，提示用户配置
获取 access_token
    ↓ 失败 → 报错退出
上传封面图 + 内容图片（最多5张）
    ↓ 失败 → 报错退出
构建草稿 JSON（UTF-8 + charset=utf-8）
    ↓
提交草稿箱
    ↓ 成功 → 报告 media_id 和预览链接
    ↓ 失败（中文乱码）→ 自动切换 HTML fallback
        → 生成可下载 HTML 文件
        → 提示用户手动复制发布
```

---

## 配置文件

**路径：** `~/.openclaw/agents/gzh-assistant/wechat/credentials.json`

**模板：**
```json
{
  "app_id": "你的AppID",
  "app_secret": "你的AppSecret",
  "image_dir": "~/wechat_images"
}
```

**获取方式：**
- AppID/AppSecret：微信公众平台 → 设置与开发 → 基本配置
- image_dir：封面图和内容图片存放目录（绝对路径）

---

## 图片要求

| 类型 | 数量 | 格式 | 尺寸建议 |
|------|------|------|---------|
| 封面图 | 1张 | PNG/JPG | 900×383 px |
| 内容图 | 最多4张 | PNG/JPG | 宽度≤1080px |

图片必须预先放入 `image_dir` 目录，命名规则：
- `cover.png` / `cover.jpg` — 封面图
- `layer1.png` / `layer1.jpg` — 内容图1
- `layer2.png` / `layer2.jpg` — 内容图2
- `layer3.png` / `layer3.jpg` — 内容图3
- `layer4.png` / `layer4.jpg` — 内容图4

---

## 文章格式要求

- 标题：不超过34字节（约17个中文）
- 摘要：不超过61字节（约30个中文）
- 正文：支持 HTML 格式（`<p>`/`<img>`/`<strong>` 等）
- 图片在正文中使用 `<img src="（media_id）" />` 引用

---

## 已知限制

1. **中文编码 bug**：微信草稿 API 对中文 content 有 `\uXXXX` 转义问题
   - 修复方案：UTF-8 编码 + charset=utf-8 header
   - Fallback：发布失败时自动生成 HTML 文件供手动发布

2. **access_token 有效期**：2小时，过期需重新获取

3. **永久素材数量**：每个账号最多10000个

---

## 参考文档

- [SETUP.md](references/SETUP.md) — 完整安装配置指南
- [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) — 常见问题排查
