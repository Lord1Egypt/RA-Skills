---
name: baoyu-skills-wrapper
description: 宝玉技能集包装器 - 提供宝玉分享的高效工作技能集，包含内容生成、AI后端和日常效率工具
---

# 宝玉技能集包装器

宝玉分享的Claude Code技能集，提升日常工作效率。包含18个强大技能，分为三大类：

## 📦 安装完成

✅ **宝玉技能集已成功安装** - 版本 1.89.1

## 🎯 技能分类

### 📝 内容技能 (Content Skills)
内容生成和发布技能

1. **baoyu-xhs-images** - 小红书信息图系列生成器
   - 将内容拆解为1-10张卡通风格信息图
   - 支持风格×布局二维系统
   - 9种风格：cute、fresh、warm、bold、minimal、retro、pop、notion、chalkboard
   - 6种布局：sparse、balanced、dense、list、comparison、flow

2. **baoyu-infographic** - 专业信息图生成器
   - 支持20种布局和17种视觉风格
   - 自动分析内容推荐最佳组合
   - 生成可发布的信息图

3. **baoyu-cover-image** - 文章封面图生成器
   - 五维定制系统：类型×配色×渲染×文字×氛围
   - 9种配色方案与6种渲染风格组合
   - 提供54种独特效果

4. **baoyu-slide-deck** - 幻灯片生成器
   - 从内容生成专业幻灯片图片
   - 支持16种预设风格
   - 自动创建大纲并逐页生成

5. **baoyu-comic** - 知识漫画创作器
   - 支持画风×基调灵活组合
   - 5种画风：ligne-claire、manga、realistic、ink-brush、chalk
   - 7种基调：neutral、warm、dramatic、romantic、energetic、vintage、action

6. **baoyu-article-illustrator** - 智能文章插图
   - 类型×风格二维系统
   - 6种类型：infographic、scene、flowchart、comparison、framework、timeline
   - 8种风格：notion、elegant、warm、minimal、blueprint、watercolor、editorial、scientific

7. **baoyu-post-to-x** - X (Twitter) 发布工具
   - 支持普通帖子和X文章
   - 使用真实Chrome绕过反自动化检测
   - 支持图片和Markdown文章

8. **baoyu-post-to-wechat** - 微信公众号发布工具
   - 支持贴图模式和文章模式
   - API和浏览器两种发布方式
   - 支持多账号管理

9. **baoyu-post-to-weibo** - 微博发布工具
   - 支持文字、图片、视频发布
   - 支持头条文章
   - 使用真实Chrome绕过检测

### 🤖 AI生成技能 (AI Generation Skills)
AI驱动的生成后端

10. **baoyu-imagine** - 图像生成器
    - 支持9个服务商：OpenAI、Azure OpenAI、Google、OpenRouter、DashScope、MiniMax、即梦、豆包、Replicate
    - 支持文生图、参考图、自定义尺寸
    - 批量生成和质量预设

11. **baoyu-danger-gemini-web** - Gemini Web交互
    - 与Gemini Web交互生成文本和图片
    - 需要浏览器登录认证

### 🛠️ 工具技能 (Utility Skills)
内容处理工具

12. **baoyu-youtube-transcript** - YouTube字幕下载
    - 下载字幕/转录文本和封面图片
    - 支持多语言、翻译、章节分段
    - 支持说话人识别

13. **baoyu-url-to-markdown** - URL转Markdown
    - 通过Chrome CDP抓取任意URL
    - 转换为Markdown格式
    - 支持等待模式

14. **baoyu-danger-x-to-markdown** - X内容转Markdown
    - 将X推文和文章转换为markdown
    - 支持推文串和X文章
    - 需要身份验证

15. **baoyu-compress-image** - 图片压缩
    - 压缩图片减小文件大小
    - 保持质量优化

16. **baoyu-format-markdown** - Markdown格式化
    - 自动格式化纯文本或Markdown文件
    - 添加frontmatter、标题、摘要
    - 层级标题、加粗、列表优化

17. **baoyu-markdown-to-html** - Markdown转HTML
    - 转换为样式化HTML
    - 支持微信公众号兼容主题
    - 代码高亮和外链引用

18. **baoyu-translate** - 翻译工具
    - 三模式翻译：快速、标准、精翻
    - 支持多语言
    - 面向受众的翻译

## 🚀 使用方法

由于宝玉技能集是为Claude Code设计的，需要通过Bun运行时来使用：

### 基础用法
```bash
# 检查是否安装bun
bun --version

# 如果没有，安装bun
npm install -g bun

# 进入宝玉技能集目录
cd ~/.openclaw/skills/baoyu-skills

# 使用示例（需要具体技能脚本）
bun run skills/<skill-name>/main.ts [options]
```

### 环境配置

部分技能需要API密钥，创建配置文件：

```bash
mkdir -p ~/.baoyu-skills
cat > ~/.baoyu-skills/.env << 'EOF'
# OpenAI
OPENAI_API_KEY=你的OpenAI密钥

# Google
GOOGLE_API_KEY=你的Google密钥

# 其他服务商...
EOF
```

## 📚 详细文档

每个技能都有详细的使用说明，请参考：
- `/home/openclaw/.openclaw/skills/baoyu-skills/README.md` - 英文文档
- `/home/openclaw/.openclaw/skills/baoyu-skills/README.zh.md` - 中文文档

## ⚠️ 注意事项

1. **运行时依赖**：需要安装Bun (`npm install -g bun`)
2. **浏览器依赖**：部分技能需要Chrome浏览器
3. **API密钥**：图像生成等技能需要配置相应的API密钥
4. **身份验证**：部分社交发布技能需要登录认证

## 🔧 技能维护

这是宝玉技能集的OpenClaw包装器，原始技能集位于：
`~/.openclaw/skills/baoyu-skills/`

原始技能集包含完整的TypeScript源码和详细的文档。

## 📞 支持

如需了解更多宝玉技能集的用法，请查看原始仓库：
https://github.com/JimLiu/baoyu-skills
