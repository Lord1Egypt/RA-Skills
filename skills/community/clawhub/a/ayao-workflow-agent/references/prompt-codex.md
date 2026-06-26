# Codex Backend Coding Prompt Template

Use this template when dispatching tasks to Codex (codex-1, codex-2, etc.).

## 调用命令格式

```bash
PROMPT_FILE=/tmp/codex-task-prompt.txt

cat > "$PROMPT_FILE" << 'PROMPT'
[完整任务 prompt]
PROMPT

scripts/dispatch.sh codex-1 T001 --prompt-file "$PROMPT_FILE" \
  codex exec --dangerously-bypass-approvals-and-sandbox
```

> 推荐把 prompt 单独写文件，再通过 `dispatch.sh --prompt-file` 走 stdin。这样长 markdown、多行文本、引号都更稳。
> YOLO 模式：无沙盒、无确认提示，agent 可直接执行任意 shell 命令。仅在受信任环境中使用。

## 重要原则

1. **引用实际文件，不描述技术栈** — 不要写"使用 pg 连接数据库"，而是写"参考 `src/persistence/db.ts` 中的 `getPool()` 模式"
2. **commit 命令写死** — 不要让 agent 自己决定 commit message，直接给出完整命令
3. **scope 列出具体文件路径** — 不是"改 providers 目录"，而是"创建 `src/providers/clob-auth.ts`"
4. **禁止事项要具体** — 不要泛泛说"不要改其他文件"，列出可能被误改的关键文件

## 模板

```
## Project
[Project name] — [one-line description]
Working directory: [absolute path]

## Task
[ID]: [One sentence]

## 认知模式（每个决策点应用）

1. **DRY 检查**：写代码前先用 grep/find 搜索，这个逻辑是否已经存在？存在就复用，不重复实现。
2. **Boring by Default**：优先使用项目中已有的库、工具函数和模式，不发明新方案。
3. **Blast Radius Check**：评估改动影响范围。若需修改 5 个以上文件，先暂停并在 commit message 中说明原因。
4. **Two-Week Smell Test**：写完后问自己：两周后陌生人看这段代码，能立刻明白它在做什么吗？不能就加注释或重命名。

## Completeness Principle（完整性原则）

AI 时代，在 scope 内多写 50 行代码的边际成本 ≈ 0。当你面临选择时：

**两条规则同时成立，不矛盾：**
- **Scope 边界**（防止越界）：不要动 scope 之外的文件/模块
- **Scope 内要做完整**：在你被允许动的范围内，选完整方案而非最小方案

**具体行为：**
- ✅ 在 scope 内发现明显的同类问题，一起修掉
- ✅ 新增函数必须有对应的错误处理（不只是 happy path）
- ✅ 能看到的 edge case 要处理，不要留 TODO
- ❌ 不要：只修报错那一行，旁边明显的同类问题跳过
- ❌ 不要：能看到 edge case 但写 `// TODO: handle this`

## Scope (strict — ONLY touch these files)
- Create: [full relative paths]
- Modify: [full relative paths]
- 禁止修改: [列出容易被误改的关键文件，如 package.json, tsconfig.json, 共享 types]

## Technical Requirements
[具体技术要求]

## Reference Code (必填 — 让 agent 自己看代码而不是靠你描述)
请先阅读以下文件了解项目模式：
- `[path/to/similar-module.ts]` — [说明这个文件展示了什么模式]
- `[path/to/types.ts]` — [需要用到的类型定义]
- `[path/to/config.ts]` — [配置加载方式]

## Do NOT
- 修改 scope 以外的任何文件
- 不要修改: [具体列出，如 src/daemon/game-runner.ts, package.json]
- 不要添加 npm 依赖（除非下面明确列出）
- 不要修改 .env 或包含密钥的配置
- 不要重构已有代码

## Allowed Dependencies (如果需要新依赖)
- [package-name]: [为什么需要]

## Commit (直接复制执行)
git add -A && git commit -m "[预写好的 conventional commit message]" && git push

## Done When
[具体完成标准]

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

## 常见错误与预防

| 错误 | 原因 | 预防 |
|------|------|------|
| Agent 用了错误的 DB 驱动 | Prompt 说"使用 SQLite"但项目用 pg | Reference Code 指向实际 db.ts |
| Agent 改了 package.json | 自己决定加依赖 | 禁止修改列表明确包含 package.json |
| Agent 不 commit | 忘了或被其他输出打断 | commit 命令写在最后，加粗强调 |
| Agent 改了共享 types | 觉得需要扩展类型定义 | 禁止修改列表包含 types/index.ts |
| Commit message 不规范 | Agent 自由发挥 | 直接给出完整 git commit 命令 |
