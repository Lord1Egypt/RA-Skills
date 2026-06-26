---
name: doc-publisher
description: 文档系列发布工具 - 将本地 Markdown 文档自动转换为微信公众号文章并发布
postInstall: |
  🎉 感谢安装 doc-publisher！

  ⚙️ 首次使用请配置公众号信息：

  1️⃣ 进入技能目录
     cd skills/doc-publisher

  2️⃣ 复制配置模板
     copy .env.example .env

  3️⃣ 编辑 .env 填入你的信息
     用记事本打开 .env，填入 APPID 和 SECRET

  4️⃣ 开始发布
     告诉助手：发布 D:\我的文档 到公众号

  📖 详细说明：查看 README.md
user-invocable: true
version: 1.0.0
author: 小蛋蛋
metadata:
  openclaw:
    homepage: https://docs.esupagent.com
    category: 公众号管理
---

# doc-publisher

> 文档系列发布工具 - 将本地 Markdown 文档自动发布到微信公众号
> 
> 版本：1.0.0 | 作者：小蛋蛋

---

## 技能信息

| 属性 | 内容 |
|------|------|
| 名称 | doc-publisher |
| 版本 | 1.0.0 |
| 作者 | 小蛋蛋 |
| 创建日期 | 2026-04-12 |
| 描述 | 将本地 Markdown 文档系列自动转换为微信公众号文章并发布 |
| 类型 | 工具类 |
| 平台 | Windows |

---

## 核心功能

### 1. Markdown 转微信公众号 HTML
- ✅ 标题转换（H1/H2/H3）
- ✅ 代码块高亮（带边框和背景）
- ✅ 表格转换（HTML 表格）
- ✅ 列表转段落（避免密集列表，提升可读性）
- ✅ 引用块转换
- ✅ 段落优化（连续文本合并，避免多余空行）

### 2. 智能过滤
- ✅ 自动过滤 `**`, `--`, `>` 等 Markdown 符号
- ✅ 自动过滤规划文件、脚本文件
- ✅ 自动跳过非 `.md` 文件

### 3. 系列导航
- ✅ 篇首导航（上一篇 | 进度 | 下一篇）
- ✅ 篇尾导航（下一篇链接 + 系列信息）
- ✅ 自动排序（按文件名序号）

### 4. 目录结构支持
- ✅ 扁平结构（所有文件在同一层）
- ✅ 子目录结构（chapters/ + appendix/）

---

## 📝 技术文章写作规范（重要！）

### 核心原则

**1. 基于官方资料**
- 所有内容必须基于用户提供的官方文档/资料
- 不添加推测性内容，不编造功能
- 引用官方链接时确保可访问

**2. 傻瓜式操作指导**
- 每一步都要明确：点击哪里、输入什么、保存到哪
- 避免"配置环境"、"设置参数"等模糊表述
- 示例：「复制这串字符，保存到记事本」而不是「保存 API Key」

**3. 段落化叙述**
- 避免密集列表（超过 5 项的列表要拆分）
- 用自然段落代替步骤列表
- 关键信息用**加粗**或颜色标注

**4. 排版整洁**
- 段落之间不空行（微信会自动换行）
- 代码块前后留白清晰
- 表格简洁，不超过 4 列

### 用户视角检查清单

写作完成后，问自己：
- [ ] 零基础用户能看懂吗？
- [ ] 用户需要动脑思考吗？
- [ ] 每一步都有明确操作吗？
- [ ] 有不必要的技术术语吗？
- [ ] 排版整洁无空行吗？

---

## 使用方法

### 方式 1：直接告诉助手（推荐）

在聊天中说：
```
发布 D:\你的文档目录 下的文档到公众号
```

### 方式 2：使用通用脚本

```bash
node "C:\Users\LIYONG\.openclaw\workspace\skills\doc-publisher\examples\publish-any.js" "D:\你的文档目录"
```

### 方式 3：使用专用脚本

```bash
# 发布 SGLang 系列
node "C:\Users\LIYONG\.openclaw\workspace\skills\doc-publisher\examples\publish-sglang.js"

# 发布其他系列（复制脚本，修改 config.rootDir）
```

---

## 支持的目录结构

### 结构 1：扁平结构

```
D:\你的文档目录\
├── assets/                 # 资源文件夹（自动跳过）
├── 00-规划文档.md          # 规划文件（自动跳过）
├── 01-简介.md              # ✅ 发布
├── 02-核心概念.md          # ✅ 发布
├── 03-技术原理.md          # ✅ 发布
└── collect-info.js         # 脚本文件（自动跳过）
```

### 结构 2：子目录结构

```
D:\你的文档目录\
├── chapters/
│   ├── 01-第一章.md
│   └── 02-第二章.md
└── appendix/
    ├── A-附录 A.md
    └── B-附录 B.md
```

---

## 发布规则

| 规则 | 说明 |
|------|------|
| ✅ 保留序号 | `01-SGLang 简介` → `01-SGLang 简介` |
| ✅ 使用文件名 | 以文件名为准，不提取 Markdown 标题 |
| ✅ 去掉.md | 自动移除 `.md` 扩展名 |
| ✅ 段落优化 | 连续文本自动合并，避免多余空行 |
| ✅ 代码转义 | 代码块内特殊字符自动转义 |
| ⚠️ 草稿箱链接不可点击 | 微信限制，发布后可点击 |

---

## ⚙️ 配置步骤（首次使用必读）

### 1. 复制配置文件

在技能目录下执行：
```bash
cd skills/doc-publisher
copy .env.example .env
```

### 2. 获取公众号信息

登录 [微信公众号后台](https://mp.weixin.qq.com)：

| 配置项 | 获取路径 |
|--------|----------|
| **APPID** | 设置与开发 → 基本配置 → 开发者 ID |
| **SECRET** | 设置与开发 → 基本配置 → 开发者 ID（需生成） |
| **THUMB_MEDIA_ID** | 素材管理 → 图片 → 上传后获取 media_id |
| **QRCODE_URL** | 设置与开发 → 公众号二维码 → 复制图片链接 |

### 3. 编辑 .env 文件

用记事本打开 `.env` 文件，填入你的信息：
```env
WECHAT_APPID=wxebff9eadface1489
WECHAT_SECRET=44c10204ceb1bfb3f7ac09675497654
WECHAT_THUMB_MEDIA_ID=bEleejFU9wv67FJfDm4w_xxx
WECHAT_QRCODE_URL=https://mmbiz.qpic.cn/xxx
```

### 4. 测试配置

运行任意发布脚本，如配置正确即可正常发布。

---

## 配置选项

```javascript
const config = {
  rootDir: 'D:\\你的文档目录',    // 文档根目录
  chaptersDir: 'chapters',        // 章节目录（可选）
  appendixDir: 'appendix',        // 附录目录（可选）
  outputDir: 'D:\\published',     // 输出目录（可选）
  
  publish: {
    author: '技术团队',            // 作者名称
    prefix: '[系列名称]',          // 标题前缀
    addSeriesInfo: true,          // 是否添加系列信息
  }
};
```

---

## 文件结构

```
doc-publisher/
├── SKILL.md                      # 技能说明（本文件）
├── README.md                     # 快速入门
├── 结构说明.md                   # 目录结构说明
├── .env                          # ⭐ 微信配置（敏感信息）
├── src/
│   ├── doc-publisher.js          # 核心程序
│   └── wechat-api.js             # ⭐ 微信公众号 API（独立）
└── examples/
    ├── publish-sglang.js         # SGLang 发布脚本
    ├── publish-any.js            # 通用发布脚本
    └── check-wechat-format.js    # 格式校验工具
```

---

## 工具说明

### publish-any.js

**用途：** 发布任意目录的文档

**用法：**
```bash
node publish-any.js "D:\你的文档目录"
```

### publish-sglang.js

**用途：** 发布 SGLang 系列文档

**用法：**
```bash
node publish-sglang.js
```

### check-wechat-format.js

**用途：** 格式校验和预览

**用法：**
```bash
node check-wechat-format.js "D:\文档.md"
```

**输出：**
- `xxx-wechat.html` - 纯 HTML
- `xxx-preview.html` - 可预览文件（浏览器查看）

---

## 依赖

- 无（完全独立，内置微信公众号 API）

## 微信配置

**位置：** `skills/doc-publisher/.env`

**配置项：**
```env
WECHAT_APPID=你的公众号 APPID
WECHAT_SECRET=你的公众号 SECRET
WECHAT_THUMB_MEDIA_ID=封面图片 ID
WECHAT_QRCODE_URL=公众号二维码 URL
```

**获取方式：**
1. APPID/SECRET - 公众号后台 → 设置与开发 → 基本配置
2. THUMB_MEDIA_ID - 公众号素材库上传图片后获取
3. QRCODE_URL - 公众号二维码链接

---

## 注意事项

1. **草稿箱链接** - 编辑模式下无法点击，需发布后测试
2. **预览方法** - 使用 `check-wechat-format.js` 在浏览器模拟手机效果
3. **目录结构** - 支持扁平结构和子目录结构
4. **文件过滤** - 自动跳过规划文件、脚本、非 `.md` 文件

---

## 更新日志

### v1.0.0 (2026-04-12)
- ✅ 初始版本
- ✅ Markdown 转微信公众号 HTML
- ✅ 智能过滤 Markdown 符号
- ✅ 系列导航生成
- ✅ 支持扁平目录结构
- ✅ 格式校验工具

---

_维护者：小蛋蛋 🦞_


