# 免费工具·平替雷达 · WorkBuddy Skill

"付费软件太贵想找免费替代品？怕免费版功能阉割、怕换工具踩坑、更怕盲目自研做半年才发现不值得？免费工具平替雷达是输入驱动的一站式平替调研技能：丢一个网站链接、名称或截图，16 个渠道并发扫描（AlternativeTo 替代品库、awesome-selfhosted 自托管金榜、GitHub、HackerNews、Reddit、Product Hunt、DuckDuckGo/Bing 全网搜索 + 10 个 Agent 技能向渠道），自动去重、GitHub 相关性过滤（核心词命中 name/description，拦截无关仓库），按 免费开源 > 免费额度 > 未验证 > 付费 四级硬排序，每个候选标注付费属性与来源渠道。核心差异：内置 AI 自研可行性评估（S 直接制作 / A 简易开发 / B 直接开发 / C 不建议自研），告诉你"抄它的核心功能自己搓一个"到底值不值，最终输出含选型建议的完整 Markdown 调研报告。Use when: 找 Notion/Obsidian 平替、有没有免费的 PS/Office、某 SaaS 订阅太贵想换、开源替代品推荐、自托管知识库选型、白嫖免费版、软件去重调研、free alternative、open source replacement、SaaS 降本替代方案。"

## 解决什么问题

- 请参考 SKILL.md 中的详细说明

## 安装

### WorkBuddy 技能市场（推荐）

在 WorkBuddy 中搜索「免费工具·平替雷达」一键安装。

### 手动安装

```bash
git clone https://github.com/guipi888/free-tool-radar.git \
  ~/.workbuddy/skills/免费工具平替雷达
```

### 环境依赖

请参考 SKILL.md 中的环境要求章节

## 使用

```bash
python3 scripts/pipeline.py <参数>
```

详细参数请参考 SKILL.md

## 输出

请参考 SKILL.md

## 项目结构

```
.gitignore
LICENSE
references
references\report-template.md
references\search-strategy.md
references\self-build-assessment.md
scripts
scripts\alt_search.py
SKILL.md
```

## 关于作者

**桂皮 Guipi** — AI Agent 开发者 · 超级个体践行者
专注 AI 效率工具与一人公司方法论，帮普通人用 AI 成为超级个体

| 平台 | 账号 |
|------|------|
| 📱 小红书 | [桂皮AI实战](https://www.xiaohongshu.com/user/profile/5a409dda44363b313b9d7e15) |
| 🎬 抖音 | [桂皮AI实战](https://v.douyin.com/QJRjHGAtrvA/) |
| 📺 视频号 | 微信内搜「桂皮AI实战」 |
| 💬 公众号 | 微信搜「桂皮AI实战」 |
| 🌟 知识星球 | [AI超级个体](https://t.zsxq.com/guSUk) — AI工具 · 创作 · 产品 · 流量 · 变现 |
| 🐙 GitHub | [guipi888](https://github.com/guipi888) |
| 💬 微信 | guipi996（注明来意） |

## License

MIT License — 详见 [LICENSE](./LICENSE)
