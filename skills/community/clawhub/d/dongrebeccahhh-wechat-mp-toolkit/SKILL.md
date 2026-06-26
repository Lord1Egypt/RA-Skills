---
name: wechat-mp-toolkit
description: 微信公众号完整工具包，包括文章创作、封面生成、自动发布、热点分析等功能。适用于公众号运营者。
version: 1.0.0
author: 猪猪助手
grade: A
category: office
tags: [wechat, 公众号, 运营, 自动化, 内容创作]
---

# 微信公众号工具包

完整的微信公众号运营工具集，覆盖内容创作、封面设计、自动发布全流程。

## 核心功能

### 1. 文章创作
- 热点追踪：自动抓取今日热点
- 内容生成：基于热点创作文章
- 排版优化：段落分明，结构清晰
- 极简风格：无emoji，无图片，纯文字

### 2. 封面设计
- 白底手绘黑白极简风格
- 黑白科技风设计
- 自动尺寸适配（900x500）
- 支持PNG/JPG格式

### 3. 自动发布
- 一键发布到草稿箱
- 自动上传封面到素材库
- 自动清理旧草稿
- 完整发布流程管理

### 4. 热点分析
- 实时热点抓取
- 关键词提取
- 趋势分析
- 选题建议

## 使用方法

### 创作并发布文章

```bash
# 完整工作流（推荐）
node scripts/full-workflow.js

# 仅生成文章
node scripts/create-article.js

# 仅生成封面
node scripts/generate-cover.js

# 仅发布文章
node scripts/publish-article.js
```

### 自定义参数

```bash
# 指定文章主题
node scripts/create-article.js --topic "AI技术"

# 指定封面风格
node scripts/generate-cover.js --style "minimal"

# 定时发布
node scripts/schedule-publish.js --time "18:00"
```

## 配置说明

### 微信公众号配置

编辑 `config/wechat-config.json`：

```json
{
  "appID": "your_app_id",
  "appSecret": "your_app_secret",
  "apiBase": "https://api.weixin.qq.com"
}
```

### 封面设计配置

编辑 `config/cover-config.json`：

```json
{
  "style": "minimal-black-white",
  "width": 900,
  "height": 500,
  "format": "png"
}
```

## 目录结构

```
wechat-mp-toolkit/
├── SKILL.md                 # 技能说明文档
├── scripts/                 # 核心脚本
│   ├── full-workflow.js     # 完整工作流
│   ├── create-article.js    # 文章创作
│   ├── generate-cover.js    # 封面生成
│   ├── publish-article.js   # 文章发布
│   ├── hotspot-analyzer.js  # 热点分析
│   └── schedule-publish.js  # 定时发布
├── config/                  # 配置文件
│   ├── wechat-config.json   # 微信配置
│   └── cover-config.json    # 封面配置
├── templates/               # 文章模板
│   ├── tech-article.md      # 科技文章模板
│   ├── news-article.md      # 新闻文章模板
│   └── opinion-article.md   # 评论文章模板
└── examples/                # 示例文件
    ├── example-article.md   # 示例文章
    └── example-cover.png    # 示例封面
```

## 依赖要求

### 系统依赖
- Node.js 14+
- ImageMagick（用于图片处理）
- curl（用于API调用）

### Node.js 包
- axios - HTTP请求
- form-data - 文件上传
- cheerio - HTML解析（可选）

### 安装依赖

```bash
# 安装Node.js包
npm install axios form-data

# 安装ImageMagick（Ubuntu/Debian）
sudo apt-get install imagemagick

# 安装ImageMagick（CentOS/RHEL）
sudo yum install imagemagick
```

## 工作流程

### 标准流程

1. **热点抓取** → 获取今日热点
2. **文章创作** → 基于热点创作内容
3. **封面生成** → 设计白底手绘黑白封面
4. **文章发布** → 自动上传并创建草稿

### 自定义流程

根据需要组合使用各个独立脚本：

```bash
# 只创作文章（不发布）
node scripts/create-article.js --topic "科技" --output article.md

# 只生成封面
node scripts/generate-cover.js --title "文章标题" --output cover.png

# 手动发布已有文章
node scripts/publish-article.js --article article.md --cover cover.png
```

## 输出规范

### 文章格式

- 标题：简洁有力，不超过30字
- 摘要：100-150字，概括核心内容
- 正文：1500-2000字，段落分明
- 格式：Markdown格式，无emoji，无图片

### 封面规格

- 尺寸：900x500像素
- 格式：PNG（推荐）或 JPG
- 大小：10-50KB
- 风格：白底手绘黑白极简

## 高级功能

### 1. 定时发布

设置定时任务，自动在指定时间发布：

```bash
# 每天早上8点发布
0 8 * * * cd /path/to/wechat-mp-toolkit && node scripts/schedule-publish.js
```

### 2. 批量操作

批量创作和发布多篇文章：

```bash
node scripts/batch-publish.js --count 5 --interval 3600
```

### 3. 数据统计

查看发布统计和分析：

```bash
node scripts/stats.js --period week
```

## 注意事项

1. **API限制**：微信公众号API有调用频率限制
2. **网络要求**：需要稳定的网络连接
3. **封面格式**：仅支持PNG和JPG，不支持SVG
4. **草稿管理**：建议定期清理旧草稿
5. **内容审核**：确保内容符合平台规范

## 故障排除

### 问题：封面上传失败

**原因**：格式不支持或文件过大

**解决**：
- 确保使用PNG或JPG格式
- 压缩图片到50KB以内
- 检查图片尺寸是否为900x500

### 问题：文章发布失败

**原因**：API参数错误或权限不足

**解决**：
- 检查appID和appSecret是否正确
- 确认IP白名单已配置
- 验证access_token是否有效

### 问题：热点抓取失败

**原因**：网络问题或源站限制

**解决**：
- 检查网络连接
- 尝试更换热点源
- 使用代理（如需要）

## 更新日志

### v1.0.0 (2026-03-15)
- ✅ 初始版本发布
- ✅ 支持完整工作流程
- ✅ 白底手绘黑白封面生成
- ✅ 极简风格文章创作
- ✅ 自动发布到草稿箱

## 贡献指南

欢迎提交问题和改进建议！

## 许可证

MIT License

---

**关键词**：微信公众号、内容创作、自动化、封面设计、热点分析

**适用场景**：公众号运营、内容营销、自动化发布

**技能等级**：A级 - 生产可用