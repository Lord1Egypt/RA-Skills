# ARG Action Chain Designer Skill

当前版本：`1.2.4`

这是给 Agent 安装使用的 Skill，用来辅助创建、诊断和补强 ARG 行动链路。

它的定位类似 `skill-creator`：不是只解释 ARG 是什么，而是引导 Agent 把一个模糊任务变成可复用的链路资产，包括 `SKILL.md` 运行骨架、`plans/step-NN-name.md`、验证门禁和失败策略。

`SKILL.md` 采用渐进式披露：主文件保留核心流程，详细模板在 `references/` 中按需读取。

可靠性模型只保留 Level 1 普通 ARG 链和 Level 2 外部门禁 ARG 链。默认 Level 1；当用户担心跳步、伪造输出或自我验收时，引导升级到 Level 2。

## 安装到 Codex

```powershell
Copy-Item -Recurse skills\arg-action-chain-designer "$env:USERPROFILE\.codex\skills\arg-action-chain-designer"
```

## 安装到 agents skills

```powershell
Copy-Item -Recurse skills\arg-action-chain-designer "$env:USERPROFILE\.agents\skills\arg-action-chain-designer"
```

## 典型调用

```text
用 arg-action-chain-designer 帮我把这个 Agent 任务拆成 ARG 行动链路。
```

```text
把这个普通 skill 优化成 ARG 任务链路，让它按 Step Contract 执行。
```

```text
把这个已有 skill 转成 arg-xxx，不覆盖原 skill，并生成薄 SKILL.md + plans/step-*.md + scripts/ 交付物。
```

```text
检查这个 step contract 有没有缺少 ARG 细节。
```

```text
我想限制这个 Agent 的发散和自我验收，帮我设计验证门禁。
```
