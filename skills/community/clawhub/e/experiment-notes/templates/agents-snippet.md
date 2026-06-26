# 实验笔记集成片段
# 将以下内容添加到你的 AGENTS.md 中

## Experiment Notes / 实验笔记

使用 experiment-notes skill 记录和查询实验经验。

EXPNOTE = python <skill_dir>/scripts/expnote.py

### 何时记录

**必须记录：**
- 遇到错误并成功修复 → `outcome: partial` 或 `success`
- 尝试了多种方案才搞定 → 每种方案分别记录
- 踩了一个坑（API 限制、环境问题等）→ `outcome: failure` + `lesson`

**可选记录：**
- 顺利完成的标准操作 → `outcome: success`（低优先级，可不记）

### 记录模板

```bash
$EXPNOTE log \
  --task "简短描述你要做什么" \
  --outcome success|failure|partial \
  --tags tag1,tag2,tag3 \
  --cmd "实际执行的命令" \
  --error "报错信息（如有）" \
  --fix "怎么解决的（如有）" \
  --lesson "一句话总结关键教训"
```

### 查询模板

```bash
# 开始任务前，先查历史
$EXPNOTE similar "任务描述"

# 找不到？试全文搜索
$EXPNOTE search "关键词"

# 查看某个领域的所有教训
$EXPNOTE lessons --tag docker
```

### 定期维护

每周或每 20 条记录后：
1. 运行 `$EXPNOTE stats` 看看模式
2. 把重复出现的教训用 `$EXPNOTE distill` 提炼
3. 更新 AGENTS.md 中的最佳实践
