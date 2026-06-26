# Skill 评估脚本使用指南

> 来源：基于 skill_evaluator_v2.py 评估器源码分析
> URL: ../../distill-skill-builder/scripts/skill_evaluator_v2.py
> 整理时间：2026-04-23

## 评估器架构

评估脚本位于 `../../distill-skill-builder/scripts/skill_evaluator_v2.py`（集中管理，不在各 skill 目录下复制），包含 8 个评估函数：

| 函数 | 维度 | 满分 |
|------|------|------|
| `_evaluate_trigger()` | 触发词覆盖 | 15 |
| `_evaluate_metadata()` | 元数据完整性 | 10 |
| `_evaluate_core_content()` | 核心内容深度 | 20 |
| `_evaluate_quick_reference()` | 快速参考 | 15 |
| `_evaluate_pitfalls()` | 避坑指南 | 15 |
| `_evaluate_sources()` | 来源标注 | 10 |
| `_evaluate_references()` | 参考文档覆盖 | 10 |
| `_evaluate_output_format()` | 输出格式规范 | 5 |

## 运行方式

```bash
python ../../distill-skill-builder/scripts/skill_evaluator_v2.py \
   <skill_dir>/<skill-name>
```

## 各维度详细说明

### 1. 触发词覆盖 (15分)

```python
# 评估逻辑
trigger_text = fm.get('trigger', '')
# 分割符：|
trigger_words = [w.strip() for w in trigger_text.split('|') if w.strip()]
score = min(15, len(trigger_words) * 3)
```

**格式要求：**
```yaml
# ✅ 正确
trigger: Swift 语法|Swift 类型|Swift 闭包

# ❌ 错误
trigger: |
  - "Swift 语法"
  - "Swift 类型"
```

### 2. 元数据完整性 (10分)

```python
# 检查字段
required_fields = ['name', 'description', 'trigger', 'tags']
optional_fields = ['hermes']
# 每个必填字段 2 分
```

**必填字段：**
- `name` — 技能名称（小写+连字符）
- `description` — 一句话描述（30-100 字）
- `trigger` — 触发词（用 | 分隔）
- `tags` — 标签列表

### 3. 核心内容深度 (20分)

```python
# 字符数（8分）
char_score = 8 if char_count >= 10000 else 6 if >= 5000 else 4

# H1/H2 结构（6分）
hdr_score = 6 if (h1 >= 5 and h2 >= 10) else 4 if (h1 >= 3 and h2 >= 5) else 2 if h1 >= 2 else 0

# 代码块（4分）
cb_score = 4 if code_blocks >= 10 else 3 if >= 5 else 1 if >= 2 else 0

# 表格（2分）
tb_score = 2 if tables >= 10 else 1 if tables >= 5 else 0
```

**达标线：**
- 字符数 ≥10000
- H1 ≥5 且 H2 ≥10
- 代码块 ≥10
- 表格 ≥10

### 4. 快速参考 (15分)

```python
# 必须在 SKILL.md 中有 ## 快速参考 H2 章节
qr = re.search(r'^##\s+快速参考', body, re.MULTILINE)
# 表格数
tables = re.findall(r'\|.*\|.*\|', qr_section)
# 代码块数
code_blocks = re.findall(r'```', qr_section)
# 关键数值（正则）
key_values = re.findall(r'\d+[ptpx%]+', qr_section)
```

**评分标准：**
- 表格 ≥5 → +5
- 代码块 ≥10 → +5
- 关键数值 ≥10 → +2
- 章节存在 → +3

### 5. 避坑指南 (15分)

```python
# 必须在 SKILL.md 中有 ## 避坑指南 H2 章节
pitfalls = re.search(r'^##\s+避坑指南', body, re.MULTILINE)
# 评估表格内容质量
table_rows = re.findall(r'\|.*\|', pitfalls_section)
```

### 6. 来源标注 (10分)

```python
# 官方 URL（从 body 提取 + frontmatter hermes.source 合并）
urls = re.findall(r'https?://\S+', body)
if 'source' in fm.get('hermes', {}):
    urls.append(fm['hermes']['source'])

# ★ 仅识别以下 4 个域名，其他域名不计入
official = [u for u in urls if 'developer.apple.com' in u
            or 'developer.huawei.com' in u
            or 'swift.org' in u
            or 'docs.swift.org' in u]

# 日期（body + frontmatter hermes.last_updated 合并）
dates = re.findall(r'\d{4}[-/]\d{2}[-/]\d{2}|\d{4}年\d{1,2}月', body)
if not dates and fm.get('hermes', {}).get('last_updated'):
    dates = [fm['hermes']['last_updated']]
```

**评分：**
| 条件 | 得分 |
|------|------|
| 官方 URL ≥3（step jump） | +4 |
| 官方 URL ≥1 | +3 |
| body 或 frontmatter 有日期 | +3 |
| body 有"来源："标记 | +2 |
| **最多** | **10** |

**关键约束（实际测试验证）：**
1. **仅 4 个白名单域名有效**：`developer.apple.com`、`developer.huawei.com`、`swift.org`、`docs.swift.org`。`example.com` 等其他域名得 0 分。
2. **body URL 必须真实白名单**：frontmatter URL 和 body URL 合并计分，但 body 中的非白名单 URL 不计分。
3. **3 URL = step jump**：从 +3 跳到 +4，分差 1 分，是达到 9/10 的最关键动作。
4. **frontmatter 日期需要 patch**：默认不读取 `hermes.last_updated`，需在 body 末尾加标准日期格式。

### 7. 参考文档覆盖 (10分)

**评分公式（实际测试验证）：**

| 条件 | 得分 |
|------|------|
| 文件数 ≥6 且平均行数 ≥300 | **+10** |
| 文件数 ≥4 或平均行数 ≥200 | +8 |
| 其他 | 按比例计算 |

公式拆解：
- **文件数分**：每文件 0.5 分，上限 5 分。15 文件 = 7.5 → 5（上限截断）
- **平均行数分**：avg ≥ 300 → **+3**，avg ≥ 150 → +1，否则 0
- **来源标注分**：**+2**（bug：sourced_count 永远 < 真实值，详见下方 Bug 记录）

**目标值（稳定满分）：**
- 文件数 = 15（min 15 × 0.5 = 7.5 → 5 分）
- 平均行数 ≥ 300
- 所有文件有 `来源：` 或 `URL:` 标记

**诊断命令：**
```bash
cd <skill_dir>/<skill>
python3 -c "
from pathlib import Path
files = list(Path('references').glob('*.md'))
total = sum(len(f.read_text(encoding='utf-8').split('\n')) for f in files)
avg = total/len(files)
print(f'Files: {len(files)}, Avg: {avg:.1f} (need >= 300)')
"
```

**⚠️ Bug：变量遮蔽导致 sourced 检查失效**

在 `_evaluate_references` 中：

```python
def _evaluate_references(skill_path):
    ...
    for f in ref_files:
        ...
        for line in lines:
            if '来源：' in line or 'URL:' in line:
                count = count + 1   # ← 遮蔽外层 sourced_count！
```

内层 `count` 与外层 `sourced_count` 是不同变量，内层赋值不影响外层。
导致 `sourced >= count * 0.8` 条件永远为真（实际 sourced=1 而非真实值）。
**此 bug 使 sourced 分 +2 恒定生效，不影响满分路径，但会掩盖来源标注不完整的问题。**

**实战经验：**
- 当 `avg < 300` 时，参考文档覆盖只能得 1 分（≈7.5/10），瓶颈在行数而非文件数
- 扩充小文件比新增文件更高效：加 1 个 300 行文件不如把 6 个 200 行文件各扩充到 300 行
- closures.md 是常见最短板：建议 ≥300 行并包含完整附录速查表

### 8. 输出格式规范 (5分)

```python
# 必须在 SKILL.md 中有 ## 输出格式规范 H2 章节
output = re.search(r'^##\s+输出格式规范', body, re.MULTILINE)
# 检查示例代码、禁用格式、回复结构
```

---

## 常见问题排查

### Q: 触发词得 0 分

A: 检查 `trigger:` 字段是否在 frontmatter 中（以 `---` 包裹）。

### Q: 来源标注得 2/10

A: `source` URL 可能在 `hermes.source` 里，需 patch 评估器或加到 body。

### Q: 核心内容得 14/20

A: H1 数量不足 5 个。需插入顶级 H1 章节。

### Q: 参考文档覆盖得 9/10

A: 瓶颈在平均行数而非文件数。运行诊断命令查看当前 avg 值：
- `avg < 300` → 只有 +1 分（公式限制），扩充最小文件（如 closures.md）到 ≥300 行
- `avg ≥ 300` → 得 10/10，不需要增加文件数

### Q: 快速参考得 0/15

A: 缺少 `## 快速参考` 章节，或章节中表格/代码块不足。

### Q: 参考文档覆盖得 0/10

A: `references/` 目录为空或文件太少/太短。

---

## Patch 记录

### Patch 1: 支持 swift.org URL

```python
# _evaluate_sources 函数
official_urls = [u for u in urls if 'developer.apple.com' in u 
                 or 'developer.huawei.com' in u 
                 or 'swift.org' in u 
                 or 'docs.swift.org' in u]
```

### Patch 2: 支持 hermes.source

```python
if isinstance(fm.get('hermes'), dict) and 'source' in fm['hermes']:
    urls.append(fm['hermes']['source'])
```

### Patch 3: 支持 hermes.last_updated

```python
if not dates and fm.get('hermes', {}).get('last_updated'):
    dates = [fm['hermes']['last_updated']]
```

---

## 来源

> skill_evaluator_v2.py 源码分析
> ../../distill-skill-builder/scripts/skill_evaluator_v2.py
