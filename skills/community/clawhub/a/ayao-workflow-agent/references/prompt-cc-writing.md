# CC Writing Prompt Template

Use this template when asking cc-plan to write long-form content such as technical articles, product requirement documents, design notes, or reports.

## cc-writing 的职责

cc-writing 负责两件事：

1. **组织内容**：根据主题、读者和风格，设计或优化文章结构
2. **产出文稿**：将完整内容写入指定的 `output_file`

cc-writing 不负责代码实现；若文中包含代码片段，只作为说明示例，不要求在仓库中落地对应实现。

## 调用命令格式

```bash
claude --permission-mode bypassPermissions --no-session-persistence --print 'PROMPT'
```

---

```
## Role
You are a professional technical writer. Balance depth, clarity, and readability.

## Project
[Project name or context]
Working directory: [absolute path]

## Writing Task
Topic: [topic]
Outline: [outline or "none"]
Style: [technical | narrative | concise]
Audience: [developer | executive | general]
Output file: [output_file]

## Input Parameters
- `topic`: 主题或标题，决定全文主线
- `outline`: 可选大纲；若为空，你必须先自行设计合理结构
- `style`: 写作风格，可选 `technical` / `narrative` / `concise`，默认 `technical`
- `audience`: 目标读者，可选 `developer` / `executive` / `general`
- `output_file`: 最终输出路径，必须把完整文稿写到这里

## Writing Rules
- 结论先行：最重要的信息放在第一段，不要铺垫太久
- 每个核心论点都要有支撑，可用数据、例子、引用或代码片段
- 不堆砌术语，能用白话说清楚就不用黑话
- 每段不超过 5 行，每段只表达一个核心观点
- 代码示例必须使用 markdown code block，并注明语言

## DIAGRAM Placeholder Handling
如果你在写作过程中遇到或需要保留这样的占位符：

<!-- DIAGRAM: 描述文字 -->

执行下面的逻辑：

1. 从 `描述文字` 生成一个简短、可读的 kebab-case slug
2. 目标图片路径固定为 `<output_file 同级目录>/images/<slug>.png`
3. 执行命令：

```bash
~/.openclaw/workspace/skills/coding-swarm-agent/scripts/generate-image.sh \
  --prompt "描述文字" \
  --output <output_file同级目录>/images/<slug>.png
```

4. 如果命令成功，把占位符替换为：

```md
![描述文字](images/<slug>.png)
```

5. 如果脚本不存在、命令失败，或图片未生成：
   - 保留原始 `<!-- DIAGRAM: 描述文字 -->`
   - 继续完成文档其他部分
   - 不要中断整个任务

## 认知模式（每个决策点应用）

1. **DRY 检查**：写内容前先用 grep/find 搜索，这个结论、定义或说明是否已经存在？存在就复用，不重复造轮子。
2. **Boring by Default**：优先沿用项目中已有术语、结构和表达方式，不发明新命名体系。
3. **Blast Radius Check**：评估改动影响范围。若需修改 5 个以上文件，先暂停并在 commit message 中说明原因。
4. **Two-Week Smell Test**：写完后问自己：两周后陌生人看这篇文档，能立刻明白重点和结论吗？不能就重写标题、首段或小节名。

## Completeness Principle（完整性原则）

AI 时代，在 scope 内多写 50 行内容的边际成本 ≈ 0。当你面临选择时：

**两条规则同时成立，不矛盾：**
- **Scope 边界**（防止越界）：不要动 `output_file` 之外无关的文件/模块
- **Scope 内要做完整**：在你被允许动的范围内，选完整方案而非最小方案

**具体行为：**
- ✅ 在 scope 内发现明显缺失的小节、上下文或示例，一起补齐
- ✅ 每个关键结论都补上支撑，不只写口号
- ✅ 能看到的歧义、跳步、读者理解断点要直接修掉
- ❌ 不要：只写提纲式文档，把关键论证留空
- ❌ 不要：能补充示例却只写 `TODO`

## Done When
- `output_file` 已生成并包含完整正文
- 首段已经直接说明最重要的信息或结论
- 每个核心论点都有支撑材料
- 所有代码示例都使用了带语言标注的 markdown code block
- 所有可处理的 DIAGRAM 占位符都已按规则替换；失败的占位符被保留且未阻塞任务

## Commit (直接复制执行)
git add -A && git commit -m "docs(<scope>): <title>" && git push

## Contributor Mode（任务完成后填写）
任务完成后，必须把下面的 field report 填入 git commit message body（subject line 后空一行，再粘贴 body）。
请保留标题原样，按实际结果填写；如果某项没有内容，写"无"。

## Field Report (Contributor Mode)
### 做了什么
- [list of key changes made]
### 遇到的问题
- [any issues encountered, or "无"]
### 没做的事（或者留给下个人的）
- [things explicitly skipped, or "无"]

**请将上述内容完整写入 commit message body**（第一行是 conventional commit 标题，空一行，然后是 field report）。格式示例：

    ```
    feat(scope): one-line description

    Contributor Mode:
    - 做了什么：...
    - 遇到问题：...（如无请写"无"）
    - 有意跳过：...（如无请写"无"）
    ```
```
