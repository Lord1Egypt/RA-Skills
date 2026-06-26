# AI 资讯小红书创作技能

🤖 AI 行业资讯专家 + 小红书内容创作者 + 移动端视觉设计师

## 功能

- 🔍 检索 24 小时内最新 AI 资讯
- 📝 梳理汇总生成摘要
- ✍️ 创作小红书文案
- 🎨 设计 3:4 比例移动端 HTML 封面
- 📁 自动输出到 `output/日期` 目录并打开

## 快速开始

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/ai-news-xiaohongshu

# 运行创作脚本
node scripts/create-xiaohongshu-content.js
```

## 输出文件

运行后会在 `output/日期/` 目录下生成：

| 文件 | 说明 |
|------|------|
| `xiaohongshu-copy.md` | 小红书文案（可直接复制发布） |
| `cover.html` | 3:4 比例 HTML 封面（浏览器打开截图） |
| `news-summary.md` | 资讯汇总表格 |
| `sources.md` | 原始来源链接 |

## 自定义配置

编辑 `references/user-config.md`：

```markdown
# 引流话术
📌 关注我，每日更新 AI 前沿资讯
👉 评论区留言"资料"获取 AI 工具包

# 核心资讯数量
5

# HTML 屏数
2
```

## 重点关注

### 领域
- 大模型发布
- OpenClaw 相关
- Skill 技能工具
- Agent 智能体
- VibeCoding
- 企业突破

### 公司
阿里千问、MiniMax、OpenAI、Anthropic、Google Gemini、智谱 GLM、腾讯、字节、百度、科大讯飞、Moonshot、DeepSeek 等

## 搜索集成

本技能使用 `tavily-search` 进行网络搜索。在 OpenClaw 环境中：

```bash
# 使用 tavily-search 技能
npx skills tavily-search "AI 大模型 24 小时 新闻"
```

## 目录结构

```
ai-news-xiaohongshu/
├── SKILL.md              # 技能说明（OpenClaw 加载）
├── README.md             # 使用说明
├── scripts/
│   └── create-xiaohongshu-content.js  # 主脚本
├── references/
│   ├── user-config.md    # 用户配置
│   └── search-queries.md # 搜索关键词参考
└── output/
    └── YYYY-MM-DD/       # 每日输出目录
        ├── xiaohongshu-copy.md
        ├── cover.html
        ├── news-summary.md
        └── sources.md
```

## 质量检查

发布前自检：
- [ ] 所有资讯均在 24 小时内
- [ ] 核心事实准确，来源可靠
- [ ] 文案有网感，非 AI 风格
- [ ] emoji 使用适度（每段 2-3 个）
- [ ] HTML 比例 3:4，可滑动
- [ ] 引流话术已替换

---

📌 技能作者：AGI舰长
🌍 联系微信：LHYYH0001
📝 作者博客：https://www.yuque.com/lhyyh
🔗 联系作者：https://www.yuque.com/lhyyh/ai/conactus
📅 创建日期：2026-03-25
