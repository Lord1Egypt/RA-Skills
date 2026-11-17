# 级联更新三步流程

> 本文档在 LLM 处理 `changed` 文件（增量编译）时必读。

## 1. 何时触发级联

`diff.py` 输出三类：
- `new`：manifest 无记录 → 走正常建页流程。
- `changed`：hash 不同 → **触发级联**。
- `unchanged`：跳过。

schema_version 变更 → 全量重编译，不走级联（视为全 new）。

## 2. 受控三步

### 第一步：定位

`diff.py` 已自动完成。它查 `.graph.json` 的 `source_to_pages`，输出本次可能受影响的已有页清单：

```json
{
  "changed": ["raw/paper-a.pdf"],
  "affected_pages": ["pages/deep-learning/transformer.md", "pages/deep-learning/attention.md"]
}
```

LLM 不需要自己翻文件找受影响页，直接消费 `affected_pages`。

### 第二步：分类

LLM 对 `affected_pages` 中每个页判断三种动作之一：

| 动作 | 触发条件 | 执行 |
|---|---|---|
| `merge` | 新资料补充 / 修订该页内容 | 增量改写，保留章节结构，追加 / 修订内容；新增来源行 |
| `ref-only` | 新资料与该页有关但不补充实质内容 | 仅在 `## 证据 / 来源` 加一行，不改正文 |
| `conflict` | 新资料与该页已有结论矛盾 | **不自动覆盖**，标记为待裁决，写入 `wiki/.conflicts.md` |

#### conflict 处理（关键）

写入 `wiki/.conflicts.md`，格式：

```markdown
## 冲突：<page-slug>

- 涉及页：pages/<topic>/<slug>.md
- 涉及源：raw/<file> §<section>
- 旧结论：<原页中的断言>
- 新结论：<新资料中的断言>
- 状态：待裁决
- 建议：<LLM 的倾向性建议，可空>
```

**绝不静默覆盖旧结论**。等用户或下一次 lint 处理。

### 第三步：限流

单次编译受影响页更新上限 **20 页**。超出则分批：

- 处理前 20 页。
- 在编译报告末尾提示："还有 N 页待级联，请说'继续更新'"。
- 用户说"继续更新"后，处理下一批 20 页。
- 不在用户未确认前自动连续编译。

## 3. merge 操作的执行细则

1. 读取原页全文。
2. 读取新资料相关章节。
3. 在原章节结构内追加 / 修订：
   - `## 定义`：补充新视角，不删旧。
   - `## 关键论点`：追加新论点 bullet。
   - `## 证据 / 来源`：追加新来源行。
   - `## 关联`：追加新 wikilink。
4. 若新资料催生新子实体，按 SCHEMA 成页规则判定是否新建页（< 200 字并入子节，否则新建）。
5. 单页仍 < 1500 字；超出则考虑拆分。

## 4. ref-only 操作的执行细则

只改 `## 证据 / 来源`，新增一行：

```
- 出自 [[相关实体]]；原文见 raw/<file> §<section>
```

正文不动。manifest 记录该页被 ref-only 更新。

## 5. 冲突裁决流程

用户看到 `.conflicts.md` 后：

1. **接受旧结论**：忽略新资料，关闭冲突（在 `.conflicts.md` 标 `状态：已关闭-保留旧`）。
2. **接受新结论**：手动改页，或让 LLM 改页（用户说"按新资料更新 X 页"），关闭冲突。
3. **两者都不对**：用户手写正确结论，关闭冲突。

关闭的冲突条目保留在 `.conflicts.md` 作为审计记录。

## 6. 级联完成的标志

- 所有 `affected_pages` 都被分类处理（merge / ref-only / conflict）。
- `.conflicts.md` 中新增的 conflict 条目已在编译报告中提示。
- `build_index.py` 已刷新索引、反链、graph、manifest。
- 编译报告包含：更新页数、merge/ref-only/conflict 各几页、剩余待级联数。

## 7. 反模式（禁止）

- 自动覆盖矛盾结论 → 违反范式红线。
- 一次性无限级联 → 必须限流 20 页。
- 跳过 diff 直接重写 → 破坏 manifest 一致性。
- LLM 自行修改 `.graph.json` / `.backlinks.json` → 这些由脚本维护。
- 把反链写回页面正文 → LLM 与脚本互相覆盖。
