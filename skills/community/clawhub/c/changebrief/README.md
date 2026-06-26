# ChangeBrief

不是再读一遍所有资料，而是每天 30 秒知道真正变化了什么。

`ChangeBrief` 是“变化简报官”这条产品线的第一版可发布仓库。它承接 `Knowledge Connector` 之后的下一步，但不再强调“接更多资料”，而是强调“最近到底变了什么”。

它解决的是更真实的一层问题：
- 这周新增了哪些重要信息
- 哪几份文档的说法变了
- 哪些旧结论已经不成立了
- 哪些冲突已经需要拍板
- 哪 3 个变化最值得现在行动

## 为什么这条线值得做

知识线很容易走到一个尴尬状态：
- 连接了很多资料
- 也能做总结
- 但不知道最近真正变化了什么

ChangeBrief 补的就是这个“增量变化层”。

它不是新的知识仓库，也不是长摘要器，而是一个管理者会愿意每天打开的变化工作台。

## 默认输出什么

它默认不产出长摘要，而是产出这种结构：
- `变化一句话`
- `这周新增了哪些重要信息`
- `哪几处说法变了`
- `哪些旧结论可能失效`
- `哪些冲突需要拍板`
- `最值得立刻行动的 3 个变化`

## 适合的输入

- 上周版 / 本周版文档
- 上一轮 / 当前轮会议纪要
- 两个时间点的研究摘要
- 旧版 / 新版政策、定价、路线图
- Knowledge Connector 导出的两次结果
- 用户自己整理的 before / after bullet points

## 核心命令

```bash
cb brief --before-file last-week.md --after-file this-week.md
cb changes --before-file v1.md --after-file v2.md
cb invalidations --before-file previous.md --after-file current.md
cb conflicts --before-file previous.md --after-file current.md
cb priorities --before-file previous.md --after-file current.md
cb analyze --before-file previous.md --after-file current.md --json
```

这些命令分别对应：
- 默认变化简报
- 重要新增变化
- 旧结论失效提示
- 需要拍板的冲突
- 最值得马上行动的变化优先级
- 原始结构化分析结果

## 和相邻 skill 的边界

- `Knowledge Connector`：负责导入、连接、搜索、关系理解
- `DecisionDeck`：负责把资料压缩成一页式决策 brief
- `NextFromKnowledge`：负责把知识推进成下一步动作
- `ChangeBrief`：负责告诉你“和上次相比，真正重要的变化是什么”

如果用户说的是“不要再总结背景，只告诉我最近变了什么”，更适合 `ChangeBrief`。

## 典型问题

- “帮我做本周变化简报”
- “这几份文档跟上周比哪里变了”
- “哪些旧结论已经不安全了”
- “什么变化最值得我现在处理”
- “哪些冲突已经需要老板拍板”
- “不要重读所有资料，只看增量”

## 建议安装名

```bash
clawhub install changebrief
```

## 仓库结构

```text
changebrief/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── RELEASE.md
├── clawhub.json
├── package.json
├── .gitignore
├── agents/openai.yaml
├── references/change-signals.md
├── bin/cli.js
├── src/index.js
├── test/test.js
└── scripts/
    ├── publish.sh
    └── verify.js
```

## 本地验证

```bash
npm test
npm run verify
node bin/cli.js brief --before-file before.md --after-file after.md
```

## 发布

```bash
npm run publish:clawhub
```

或直接执行：

```bash
sh ./scripts/publish.sh
```

## 一句话卖点

给知识仓库补上一层“增量变化 intelligence”：新增、变更、失效、冲突和立即行动，一次讲清楚。
