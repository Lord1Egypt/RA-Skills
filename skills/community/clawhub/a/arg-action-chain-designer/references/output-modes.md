# 输出模式

按用户请求选择一个模式。输出要紧凑，但必须给出可执行下一步。

## 模式 A：设计新 ARG 链路

用户要求设计、构建或转换任务时使用。

```md
## 结论
适合 ARG / 适合 ARG 但需要人工门禁 / 不适合 ARG

## 任务边界
- 最终产物：
- 输入来源：
- Agent 可判断：
- 必须脚本化：
- 验收权威：

## 架构
Static Progressive Clue Chain / 静态渐进线索链

## 可靠性等级
Level 1 普通 ARG 链 / 建议 Level 2 外部门禁 ARG 链

## 链路草图
step-00-start -> step-01-name -> step-02-name -> TERMINAL

## Step Contracts
### step-00-start
- 输入：
- 任务：
- 输出：
- 验证命令：
- 验证失败处理：
- 下一步：

## 运行 Skill 骨架
- 触发方式：
- OUTPUT_DIR：
- PLANS_DIR：
- SCRIPTS_DIR：
- 当前步：
- 禁止行为：

## 风险和补强
- ...

## 文件级交付物
如果用户只是要求设计：询问是否继续生成 `SKILL.md`、`plans/step-*.md`、必要 scripts。

如果用户已经明确要求创建、生成、写入、落地或打包：不要再问，直接生成文件级交付物。
```

## 模式 B：诊断已有链路

用户提供 skill、plan、chain 或 Step Contract，并询问是否合理时使用。

```md
## 结论
可用 / 需补强 / 风险较高

## 主要缺口
- ...

## 逐步诊断
| Step | 问题 | 建议 |
| --- | --- | --- |

## 必须补的 ARG 细节
- ...

## 可以暂缓的改进
- ...
```

## 模式 C：把已有 skill 转成 arg-xxx

用户要优化或转换已有 skill 时使用。

```md
## 转换策略
- 原 skill：
- 新 skill：
- 是否覆盖原 skill：否，除非用户明确要求

## 保留能力
- ...

## ARG 化改造
- 薄 `SKILL.md` 引擎：
- `plans/` Step Contracts：
- `scripts/` 确定性处理：
- `output/` 产物：

## 下一步
如果用户只是要求转换策略：询问是否生成文件级 `arg-xxx` 交付物。

如果用户已要求生成、写入或落地：直接创建，不覆盖原 skill。
```

## 模式 D：把模糊想法变成需求

用户只有一个想法，还没有清晰任务时使用。

```md
## ARG 需求草案
- 目标：
- 最终产物：
- 输入：
- 不确定点：
- 可脚本化部分：
- 需要 LLM 判断的部分：
- 验证策略：
- 失败策略：

## 最小链路草图
step-00-start -> step-01-name -> TERMINAL

## 需要确认的一问
...
```

## 结尾标准

设计类请求：询问是否继续生成文件级交付物。

生成类请求：报告创建/修改了哪些文件，以及做过什么验证。

不要在用户已经明确要求生成文件时，再用“是否需要我继续”结束；这种结尾会让任务停在建议层。

好的结尾：

```text
我可以继续把它落成 `arg-competitor-monitor/`：薄 `SKILL.md`、4 个 step contracts、2 个验证脚本。你确认要文件级交付物的话，我下一步直接生成。
```

生成文件后的结尾：

```text
已生成 `skills/arg-foo/`。关键文件是 `SKILL.md`、`plans/step-00-start.md`、`plans/step-01-fetch.md`、`scripts/validate_step_01.py`。已检查每个 step 都包含六个必需 section，且终点为 `TERMINAL`。
```

不好的结尾：

```text
我们应该持续优化 agent 的可靠性。
```
