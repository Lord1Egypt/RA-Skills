# ARG 可靠性等级

本 skill 只使用两级可靠性模型。默认 Level 1，用户明确关心跳步、伪造、自我验收或不可信 Agent 时，再建议 Level 2。

## Level 1：普通 ARG 链

默认基础模式。

```text
当前 step 文件包含【下一步】
Agent 执行当前 step
Agent 运行验证命令
验证通过后进入下一步
```

适合：

- 个人工具。
- 低风险日常自动化。
- 主要目标是防发散、防遗漏、让任务结构化。
- 用户没有明确要求防伪造或外部门禁。

能解决：

- 当前步骤没做完就发散。
- 忘记输出结构。
- 忘记验证。
- 自我感觉完成但没有证据。

局限：

- 不能防止 Agent 故意跳步。
- 不能防止 Agent 伪造 output。
- 不能防止 Agent 不跑验证。
- 不能防止 Agent 自己宣布验证通过。

设计 Level 1 时要明确提醒：它是工程约束，不是安全边界。

## Level 2：外部门禁 ARG 链

当用户担心执行 Agent 会跳步、伪造输出、不跑验证、自我验收时，建议 Level 2。

```text
执行 Agent 只产出当前 step 的 output
外部门禁读取 source/output/rubric
外部门禁判断是否通过
通过后才生成或发放下一步启动线索
失败时返回问题和修复要求
```

Level 2 的关键不是“必须脚本验证”，而是“门禁主体不是执行当前 step 的同一个 Agent”。

## 门禁类型

### 1. 脚本门禁

适合结构化、可程序判断的内容：

- JSON schema。
- 文件存在和非空。
- 数量一致。
- 字段非空。
- 枚举合法。
- hash / source 字段未改写。
- 报告包含指定 section。

优先使用脚本门禁，因为它稳定、便宜、可重复。

### 2. 人工门禁

适合不可逆、高风险或主观判断：

- 发邮件前确认。
- 发布前确认。
- 法务、医疗、财务、安全判断。
- 品牌语气或主观质量。

人工门禁可以输出 `pass/fail/issues/required_fix/next_clue`。

### 3. 独立 Agent 门禁

适合脚本难判断，但可以用 rubric 判断的内容：

- 摘要是否忠实。
- 分类是否合理。
- 报告是否漏掉关键风险。
- 文案是否符合业务口径。
- 多条 evidence 是否支持结论。

独立 Agent 门禁规则：

- 不能是执行当前 step 的同一个 Agent。
- 只读取 source、output、rubric 和当前 step 要求。
- 不直接修改 output。
- 不继续执行下一步。
- 输出通过/失败/问题定位/修复建议。

推荐输出：

```json
{
  "passed": false,
  "issues": [
    "第 3 条摘要和原文不一致",
    "漏掉了 1 条负面风险"
  ],
  "required_fix": "回到 step-02，只重写 summary 和 risk 字段",
  "next_clue": null
}
```

通过时：

```json
{
  "passed": true,
  "issues": [],
  "required_fix": "",
  "next_clue": "plans/step-03-render-report.md"
}
```

## 选择规则

- 默认用 Level 1。
- 能脚本判断，优先脚本门禁。
- 脚本判断不了且风险高，用人工门禁。
- 脚本判断不了但可以用 rubric 判断，用独立 Agent 门禁。
- 不要把 Level 2 强加给普通任务；先指出风险，再询问用户是否需要升级。

## 设计输出时怎么写

如果选择 Level 1：

```text
可靠性等级：Level 1 普通 ARG 链
说明：适合当前低风险/日常自动化场景。它能防发散和遗漏，但不防恶意跳步或伪造输出。
```

如果建议 Level 2：

```text
可靠性等级：建议 Level 2 外部门禁 ARG 链
原因：用户明确担心 Agent 跳步/伪造输出/自我验收。
门禁类型：脚本 / 人工 / 独立 Agent
门禁输入：source + output + rubric
门禁输出：pass/fail/issues/required_fix/next_clue
```
