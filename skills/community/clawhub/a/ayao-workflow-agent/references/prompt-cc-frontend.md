# CC Frontend Coding Prompt Template

Use this template when dispatching frontend tasks to Claude Code (cc-frontend).
All frontend code is written by Claude Code, never Codex.

## 重要原则

1. **引用实际文件** — 指向现有页面/组件让 agent 学习项目模式，不要凭空描述
2. **commit 命令写死** — 直接给出完整命令，不让 agent 自由发挥
3. **明确禁止超额完成** — cc-frontend 有"顺手多做"的倾向，要明确只做当前任务
4. **scope 列具体路径** — 不是"改 app 目录"，而是"创建 `src/app/orders/page.tsx`"

## 调用命令格式

```bash
PROMPT_FILE=/tmp/cc-frontend-prompt.txt

cat > "$PROMPT_FILE" << 'PROMPT'
[完整任务 prompt]
PROMPT

scripts/dispatch.sh cc-frontend T010 --prompt-file "$PROMPT_FILE" \
  claude --permission-mode bypassPermissions --no-session-persistence \
  --print --output-format json
```

> `--no-session-persistence`：每次任务独立上下文，不写磁盘，节省 token 和空间。
> 推荐统一用 `dispatch.sh --prompt-file`，避免 shell quoting 地狱。

## 模板

```
## Project
[Project name] — [one-line description]
Working directory: [absolute path]

## Task
[ID]: [One sentence]

⚠️ 只做这一个任务，不要顺手修改或创建其他页面/组件。

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
- 禁止修改: [列出容易被误改的文件，如 layout.tsx, globals.css, 其他页面]

## UI Requirements
[外观、交互、响应式要求]

## Reference Code (必填)
请先阅读以下文件了解项目模式：
- `[path/to/existing-page.tsx]` — [展示页面结构和数据获取模式]
- `[path/to/existing-component.tsx]` — [展示组件风格]
- `[path/to/lib/data-layer.ts]` — [数据层调用方式]
- `[path/to/route.ts]` — [API route 模式]

## Technical Requirements
[框架细节：Next.js App Router, React Server Components, 等]
[API endpoints, 数据格式, 状态管理]

## Do NOT
- 修改 scope 以外的任何文件
- 不要修改: [具体列出，如 layout.tsx, globals.css, 其他页面文件]
- 不要修改后端代码或 API routes（除非 scope 明确包含）
- 不要创建本任务未要求的页面或组件
- 不要添加 npm 依赖
- 不要修改 tailwind.config 或全局样式

## Commit (直接复制执行)
git add -A && git commit -m "[预写好的 conventional commit message]" && git push

## Done When
[用户应该看到什么，哪些交互应该工作]

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
| Agent 顺手做了其他页面 | CC 看到项目有占位页面就自己补 | 加 ⚠️ 只做当前任务 |
| Agent 改了 globals.css | 觉得需要新样式 | 禁止修改列表包含 globals.css |
| Agent 改了 layout.tsx | 想加导航链接 | 禁止修改列表包含 layout.tsx |
| 数据获取方式不一致 | 没看现有页面的模式 | Reference Code 指向现有页面 |
| Commit message 不规范 | 自由发挥 | 直接给出完整 git commit 命令 |
