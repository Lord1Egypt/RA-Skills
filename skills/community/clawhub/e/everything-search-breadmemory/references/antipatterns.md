# 反模式收录

> 本文件收录 everything-search-breadmemory 技能的常见反模式。
> AI 执行时应避免这些做法。

---

## 反模式列表

### AP-01：滥用 es.exe 搜索网络路径

**错误做法：**
```bash
# 搜索网络映射盘（性能极差）
python scripts/es_search.py search "\\server\share\*.txt"
```

**正确做法：**
- Everything 仅索引本地 NTFS 卷
- 网络路径请用其他工具（如 `dir /s` 或 PowerShell）

---

### AP-02：面包屑条目内容过大

**错误做法：**
```bash
# 把整个文件内容塞进面包屑
python scripts/breadcrumb.py add --title "某 PDF" --content "$(cat huge.pdf)"
```

**正确做法：**
- 面包屑条目应 ≤ 500 字
- 只记录关键结论，不记录全文
- 用 `--source` 指向原始文件

---

### AP-03：忽略艾宾浩斯复习间隔

**错误做法：**
```bash
# 每天强制复习所有条目（违背遗忘曲线）
python scripts/ebbinghaus.py daily-review --count 999
```

**正确做法：**
- 尊重 `next_review_at` 字段
- 只复习到期条目（`daily-review` 默认行为）
- 手动 `mark-reviewed` 更新间隔

---

## 渐进式说明

本技能采用渐进式 MD 体系，详细反模式说明见本文件。
SKILL.md 仅概述核心能力，不展开反模式细节。
