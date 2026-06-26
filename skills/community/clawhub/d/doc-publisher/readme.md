# doc-publisher 技能

> 文档系列发布工具 - 将本地 Markdown 文档自动转换为微信公众号文章并发布

---

## 🚀 快速开始

### 1. 安装技能

在 OpenClaw 中运行：
`ash
clawhub install doc-publisher
`

### 2. 配置公众号信息（首次使用）

**步骤 1：复制配置文件**
`ash
cd skills/doc-publisher
copy .env.example .env
`

**步骤 2：获取公众号信息**

登录 [微信公众号后台](https://mp.weixin.qq.com)：

| 配置项 | 获取路径 | 是否必填 |
|--------|----------|----------|
| **APPID** | 设置与开发 → 基本配置 → 开发者 ID | ✅ 必填 |
| **SECRET** | 设置与开发 → 基本配置 → 开发者 ID | ✅ 必填 |
| **THUMB_MEDIA_ID** | 素材管理 → 图片 → 上传后获取 | ⚠️ 可选 |
| **QRCODE_URL** | 设置与开发 → 公众号二维码 | ⚠️ 可选 |

**步骤 3：编辑 .env 文件**

用记事本打开 .env 文件，填入你的信息：
`env
WECHAT_APPID=wxebff9eadface1489
WECHAT_SECRET=44c10204ceb1bfb3f7ac09675497654
WECHAT_THUMB_MEDIA_ID=bEleejFU9wv67FJfDm4w_xxx
WECHAT_QRCODE_URL=https://mmbiz.qpic.cn/xxx
`

### 3. 发布文档

**方式 1：告诉助手（推荐）**
`
发布 D:\我的文档 下的文档到公众号
`

**方式 2：运行脚本**
`ash
node examples/publish-any.js "D:\我的文档"
`

---

## 📁 支持的目录结构

### 扁平结构
`
D:\我的文档\
├── 01-简介.md
├── 02-核心概念.md
└── 03-实战指南.md
`

### 子目录结构
`
D:\我的文档\
├── chapters/
│   ├── 01-第一章.md
│   └── 02-第二章.md
└── appendix/
    └── A-附录.md
`

---

## 📝 功能特性

- ✅ Markdown 转微信公众号 HTML
- ✅ 代码块高亮（带边框和背景）
- ✅ 系列导航（上一篇/下一篇）
- ✅ 智能过滤（规划文件、脚本文件）
- ✅ 段落优化（提升可读性）

---

## ⚠️ 注意事项

1. **敏感信息** - .env 文件包含公众号密钥，不要上传到公开仓库
2. **草稿箱链接** - 编辑模式下无法点击，需发布后测试
3. **图片处理** - 图片链接需要是公网可访问的 URL

---

## 📄 文件说明

| 文件/目录 | 说明 |
|----------|------|
| .env | ⭐ 公众号配置（自己创建） |
| .env.example | 配置模板 |
| skill.md | 技能详细说明 |
| src/ | 核心程序 |
| examples/ | 使用示例 |
| scripts/ | 辅助脚本 |

---

## 💡 常见问题

### Q: 如何获取 THUMB_MEDIA_ID？
A: 在公众号后台 → 素材管理 → 图片 → 上传任意图片 → 复制返回的 media_id

### Q: 发布后在哪里查看？
A: 公众号后台 → 草稿箱 → 查看已发布的文章

### Q: 可以批量发布吗？
A: 可以，脚本会自动按序号发布整个系列的文档

---

_作者：小蛋蛋 🦞 | 版本：1.0.0_
