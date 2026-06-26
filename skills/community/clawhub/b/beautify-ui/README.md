# beautify-ui 技能

## 🎨 功能说明
基于 DESIGN.md 规范自动美化网站 UI，支持 30 种知名设计风格（含中国厂商风格和电商风格）。

## 🚀 快速开始

### 方式 1：直接调用脚本
```bash
# Windows PowerShell
py C:\Users\sys\.openclaw\workspace\skills\beautify-ui\scripts\beautify.py <项目路径> <风格>

# 示例 - 语文网站用 Notion 风格
py C:\Users\sys\.openclaw\workspace\skills\beautify-ui\scripts\beautify.py C:\Users\sys\Desktop\jiangsu-grade3-poems notion
```

### 方式 2：用自然语言调用
直接对我说：
- "帮我把语文网站改成 Notion 风格"
- "用 Figma 风格美化英语网站"
- "把数学网站改成 Linear 风格"

## 🎭 支持的样式（30 种）

| 类别 | 风格 | 效果 | 适用场景 |
|------|------|------|----------|
| 教育文档 | `notion` | 温暖简约 | 语文、文学、教育类 |
| 教育文档 | `cursor` | 暗黑编辑器风 | 开发工具 |
| 创意设计 | `figma` | 活泼多彩 | 英语、互动、创意类 |
| 创意设计 | `bytedance` | 字节跳动渐变 | 社交、短视频 |
| 工具效率 | `linear` | 极简精准 | 数学、工具、效率类 |
| 技术文档 | `vercel` | 黑白科技感 | 技术文档、开发者工具 |
| 商务金融 | `stripe` | 专业优雅 | 商务、金融、企业服务 |
| 商务金融 | `apple` | 高级留白 | 高端零售、科技 |
| 商务金融 | `antdesign` | 蚂蚁企业级 | 企业后台、中台系统 |
| 社交娱乐 | `telegram` | 简洁快速 | 通讯、消息类 |
| 社交娱乐 | `discord` | 社交娱乐 | 社区、聊天类 |
| 中国厂商 | `alibaba` | 阿里云橙色 | 云服务、企业 |
| 中国厂商 | `huawei` | 华为红色 | 企业、云服务 |
| 中国厂商 | `xiaomi` | 小米橙色 | 科技、硬件 |
| 电商生活 | `shopify` | 简洁专业 | 在线商店 |
| 电商生活 | `amazon` | 橙黑电商风 | 零售、市场 |

## 📦 输出内容

执行后会生成：
1. **DESIGN.md** - 完整设计规范文档
2. **styles/theme-override.css** - 可直接引用的 CSS 变量覆盖
3. **preview-{style}.html** - 实时预览页（使用 --preview）
4. **tokens.json/js** - Design Tokens（使用 --tokens）
5. **snippets/** - 组件代码片段（使用 --snippets）

## 🔧 高级用法

### 查看可用风格
```bash
py skills/beautify-ui/scripts/beautify.py --help
```

### 生成预览页
```bash
py beautify.py <项目路径> <风格> --preview
```

### A/B 风格对比
```bash
py beautify.py <项目路径> --compare notion linear
```

### 导出 Design Tokens
```bash
py beautify.py <项目路径> <风格> --tokens
```

### DRY-RUN 模式
```bash
py beautify.py <项目路径> <风格> --dry-run
```

### 自定义风格
编辑 `scripts/beautify.py` 中的 `DESIGN_TEMPLATES` 字典，添加自己的配色方案。

## 🛠️ 技术细节

- **零依赖**：仅需 Python 3.8+ 标准库
- **非侵入式**：生成独立 CSS 文件，不影响原代码
- **可逆**：删除生成的文件即可恢复原样
- **可扩展**：支持自定义风格模板
- **框架支持**：Vite/Next.js/Nuxt.js/Remix/SvelteKit/CRA

---

**创建时间**：2026-04-14
**最后更新**：2026-04-22
**版本**：3.3.0
