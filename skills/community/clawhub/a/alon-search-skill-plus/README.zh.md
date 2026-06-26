[English](./README.md)

# Alon Search Skill Plus

用于跨可信技能目录、ClawHub 和 GitHub 适配候选仓库搜索 agent skill，并带有明确的来源分级、排序和安全过滤。

## 快速安装

```bash
npx skills add alondotsh/alon-skills --skill alon-search-skill-plus
```

## 适用场景

当用户想先找现成 skill，而不是立刻从零创建时，适合使用这个 skill。

典型触发语：

- `帮我找一个前端设计 skill`
- `有没有生成 changelog 的 skill`
- `找一下浏览器自动化 skill`
- `找一个把 Markdown 发布到微信的 skill`

## 核心能力

- 先搜索高可信 skill 目录
- 仅在必要时扩展到 ClawHub 和 GitHub
- 明确区分“可直接使用的 skill”和“可改造成 skill 的 GitHub 仓库”
- 在推荐前应用最低质量和安全过滤
- 当结果有限时明确说明，不伪造确定性

## 安全边界与限制

- 不把整个互联网当作通用搜索目标
- 对 ClawHub 和低信任聚合源保持谨慎
- 不会把普通 GitHub 代码仓库伪装成可直接安装的 skill，除非它已具备标准 skill 打包形态
- 对低信任来源会提示用户先做代码审查

## 输出结果

输出通常包括：

- 使用的搜索关键词
- 来源标签
- star 数和最近更新时间（如适用）
- 低信任来源的安全提示
- 单独列出的 GitHub 适配候选仓库

## 关于 Alon

这些公开 skills 来自 Alon 日常高频使用的真实工作流。

我长期看好 agent skills，也愿意和对 skill 制作感兴趣的人交流。

- GitHub：https://github.com/alondotsh
- ClawHub：https://clawhub.ai/u/alondotsh
- X：https://x.com/alondotsh
- 公众号：alondotsh

## License

MIT
