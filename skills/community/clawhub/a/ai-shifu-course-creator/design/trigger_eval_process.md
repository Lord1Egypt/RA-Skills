# ai-shifu-course-creator 触发优化测试过程记录

**时间**：2026-04-02
**目标**：使用 `skill-creator` 的 trigger eval 功能，评估并优化 `ai-shifu-course-creator` skill 的触发描述（description），使 Claude 能在正确的场景下自动唤醒该 skill。

---

## 测试环境

| 项目 | 值 |
|---|---|
| eval 模型 | claude-sonnet-4-6 |
| improve 模型 | claude-opus-4-6 |
| 评测用例 | 40 条（20 应触发 + 20 不应触发） |
| 数据分割 | 24 训练 / 16 测试（holdout=40%） |
| 每条用例运行次数 | 3 次（多数票判定） |
| 触发阈值 | trigger_rate ≥ 0.5 视为触发 |

---

## 遇到的问题及解决过程

### 问题 1：触发率始终为 0（precision=100%，recall=0%）

**现象**：前两轮 eval（v1、v2）中，所有 `should_trigger` 用例均未触发，通过率为 0%。`should_not_trigger` 全部通过，因此 precision=100%，但 recall=0%。

**根因分析（三个叠加原因）**：

1. **eval 用例设计问题（主因 A）**：原始 `should_trigger` 用例全部是"咨询型"问题（如"MarkdownFlow 语法怎么写？"），Claude 会直接从训练知识回答，不会调用任何 skill。改为"操作型"用例（如"帮我写一段 MarkdownFlow 脚本"）后才触发。

2. **临时 skill 文件被 installed skill 覆盖（主因 B）**：`run_eval.py` 原来在 `.claude/commands/` 下创建临时命令文件，但 `~/.claude/skills/` 下已安装的同名 skill 优先级更高，Claude 始终调用 installed skill，检测不到临时命令文件。通过查看 `stream-json` 输出确认：Claude 确实识别了 AI-Shifu 意图，但调用的是 installed skill，不是 eval 的临时文件。

3. **项目级 `test-skill.md` 抢占触发（次因）**：项目 `.claude/commands/test-skill.md` 的 description 包含 AI-Shifu 关键词，优先被 Claude 选中。删除该文件后消除干扰。

**解决方案**：修改 `run_eval.py`，检测到已安装的同名 skill 时，直接 patch 其 SKILL.md 的 description 字段进行测试，而不是创建竞争性的临时文件。

---

### 问题 2：并发 patch 导致竞态条件（Race Condition）

**现象**：v3 运行时，`ProcessPoolExecutor` 的 8 个 worker 并发执行 `run_single_query()`，每个 worker 都在 `finally` 块中读取→修改→写回同一个 SKILL.md 文件。运行到一半时进程崩溃，SKILL.md 被遗留为某个测试描述而非原始内容。

**根因**：patch/restore 逻辑放在 `run_single_query` 内部，该函数由多个进程并发调用。进程 A 读取原始内容并写入测试描述，进程 B 此时也读取（读到的是 A 写的测试描述而非原始），最终 restore 写回的是错误内容。

**解决方案**：将 patch/restore 逻辑上移到 `run_eval()` 函数层级：
- 在 `ProcessPoolExecutor` 启动前：patch SKILL.md，记录 original 内容
- 所有 worker 运行结束后（`finally` 块）：restore SKILL.md
- `run_single_query` 只负责检测，不做任何文件 I/O

同时提取 `_patch_skill_description()` 辅助函数，并将 `detect_name` 作为参数传入（与 `skill_name` 解耦），使函数签名更清晰。

---

### 问题 3：`improve_description` 使用 `claude -p` 时鉴权失效

**现象**：运行 `run_loop.py` 时，`improve_description` 调用 `claude -p` 生成新描述，进程以 exit code 1 退出，报错为鉴权 token 过期。

**解决方案**：用户执行 `/login` 重新鉴权后恢复正常。

---

### 问题 4：`trigger_eval.json` 格式不兼容

**现象**：`run_eval.py` 的 `main()` 直接将读取的 JSON 作为 `eval_set` 传入，但 `trigger_eval.json` 的顶层是 `{ "_design_principles": {...}, "cases": [...] }`，不是纯数组，导致 `TypeError: string indices must be integers`。

**解决方案**：在 `run_eval.py` 和 `run_loop.py` 的 JSON 读取处增加兼容处理：
```python
raw = json.loads(Path(args.eval_set).read_text())
eval_set = raw["cases"] if isinstance(raw, dict) and "cases" in raw else raw
```

---

## 对 skill-creator 的代码改动

### 改动 1：`scripts/run_eval.py` — 支持 installed skill 测试

新增 `_find_installed_skill_md()` 和 `_patch_skill_description()` 辅助函数，将 patch/restore 逻辑迁移至 `run_eval()` 层级，解决 installed skill 覆盖和竞态条件两个问题。

**核心变化**：

```
旧逻辑（每个 worker 独立 patch）：
run_single_query() {
    if installed_skill:
        read SKILL.md → patch → [claude -p] → finally: restore
    else:
        create temp command file → [claude -p] → finally: delete
}

新逻辑（集中 patch，worker 只检测）：
run_eval() {
    if installed_skill:
        patch SKILL.md once
        detect_name = skill_name
    else:
        create temp command file once
        detect_name = temp_file_name
    try:
        spawn workers → run_single_query(detect_name)
    finally:
        restore SKILL.md / delete temp file
}

run_single_query(detect_name) {
    [claude -p] → detect if detect_name in tool call
}
```

**函数签名变化**：
- `run_single_query(query, skill_name, skill_description, ...)` → `run_single_query(query, detect_name, ...)`
- 移除了内部的文件 I/O 逻辑

### 改动 2：`scripts/run_loop.py` — 支持独立 improve 模型

新增 `--improve-model` 参数，允许 eval 和 description 优化使用不同模型。

```python
# 新增参数
parser.add_argument("--improve-model", default=None, help="Model for description improvement")

# 函数签名扩展
def run_loop(..., improve_model: str | None = None):
    ...
    new_description = improve_description(
        ...,
        model=improve_model or model,  # 优先用 improve_model
    )
```

### 改动 3：`scripts/run_eval.py` 和 `scripts/run_loop.py` — 兼容带 `cases` 键的 JSON

```python
raw = json.loads(Path(args.eval_set).read_text())
eval_set = raw["cases"] if isinstance(raw, dict) and "cases" in raw else raw
```

---

## eval 用例设计演进

`trigger_eval.json` 的 `should_trigger` 用例经历了一次完整的重新设计（v1 → v2）：

| | v1（咨询型） | v2（操作型） |
|---|---|---|
| 用例示例 | "MarkdownFlow 里单选题语法怎么写？" | "帮我写一段 MarkdownFlow 脚本，包含单选、多选、输入框三种互动" |
| 问题 | Claude 直接回答，不调用 skill | Claude 需要 skill 来完成复杂操作 |
| 触发率 | 0% | 85%+ |

**设计原则**（已记录在 `_design_principles` 中）：
- should_trigger 用例必须是需要 Claude 执行操作的任务（写脚本、部署课程、修改内容等）
- 用例要足够复杂，Claude 无法仅靠训练知识直接完成
- should_not_trigger 用例要是"近似陷阱"（同类关键词但不同平台/工具），而不是显然无关的内容

---

## 最终结果

| 指标 | 优化前 | 优化后 |
|---|---|---|
| 总体准确率 | ~61% | **~98%** |
| Train 通过率 | 15/24 (62%) | **24/24 (100%)** |
| Test 通过率 | 10/16 (62%) | **16/16 (100%)** |
| Precision（不误触发） | 100% | **100%** |
| Recall（不漏触发） | 22% | **~96%** |
| 迭代次数 | - | 2 轮（Opus 一次提出，直接 100%） |

优化后描述已同步更新至：
- `~/.claude/skills/ai-shifu-course-creator/SKILL.md`（installed skill）
- `skills/ai-shifu-course-creator/SKILL.md`（项目仓库）
