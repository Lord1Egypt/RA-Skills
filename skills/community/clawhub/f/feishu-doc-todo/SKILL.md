# feishu-doc-todo 技能

## 描述

飞书文档待办自动识别与日历创建工具。自动读取飞书文档中的待办表格（时间节点 + 里程碑 + 负责人），解析模糊时间，创建飞书日历日程并设置 deadline 提醒。

## 触发词

- "创建日历"
- "设置日程"
- "待办提醒"
- "deadline 提醒"
- "飞书文档待办"
- "文档待办转日历"

## 执行流程

### 步骤 1：读取飞书文档内容

使用 `feishu_doc read` 读取文档内容，提取待办表格。

```bash
# 读取文档
feishu_doc read --doc_token <文档 token>
```

**待办表格格式识别：**
```markdown
| 时间节点 | 里程碑 | 负责人 |
|---------|--------|--------|
| 下周 | xxx | xxx |
| 4 月 8 日 | xxx | xxx |
| 4 月份 | xxx | xxx |
```

---

### 步骤 2：解析待办事项

**Python 解析脚本：**

```python
import re
from datetime import datetime, timedelta

def parse_todo_table(markdown_table):
    """解析待办表格，返回待办事项列表"""
    todos = []
    
    # 解析表格行
    lines = markdown_table.strip().split('\n')
    headers = []
    data_rows = []
    
    for i, line in enumerate(lines):
        if i == 0:  # 表头
            headers = [h.strip() for h in line.split('|')[1:-1]]
        elif i == 1:  # 分隔线
            continue
        else:  # 数据行
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if len(cells) >= 3:
                data_rows.append({
                    'time': cells[0],
                    'task': cells[1],
                    'owner': cells[2]
                })
    
    return data_rows

def parse_fuzzy_time(time_str, reference_date=None):
    """解析模糊时间为具体日期"""
    if reference_date is None:
        reference_date = datetime.now()
    
    time_str = time_str.strip()
    
    # 精确日期：4 月 8 日
    match = re.match(r'(\d{1,2}) 月 (\d{1,2}) 日？', time_str)
    if match:
        month, day = int(match.group(1)), int(match.group(2))
        year = reference_date.year
        return datetime(year, month, day)
    
    # 模糊时间：下周
    if '下周' in time_str:
        return reference_date + timedelta(days=7)
    
    # 月份：4 月份
    match = re.match(r'(\d{1,2}) 月份', time_str)
    if match:
        month = int(match.group(1))
        # 取月中
        return datetime(reference_date.year, month, 15)
    
    # 默认：返回参考日期 +7 天
    return reference_date + timedelta(days=7)

# 使用示例
todos = parse_todo_table(table_markdown)
for todo in todos:
    deadline = parse_fuzzy_time(todo['time'])
    print(f"任务：{todo['task']}")
    print(f"负责人：{todo['owner']}")
    print(f"截止日期：{deadline.strftime('%Y-%m-%d')}")
    print("---")
```

---

### 步骤 3：创建飞书日历日程

使用 `feishu_calendar create` 创建日程。

```bash
# 创建单个日程
feishu_calendar create \
    --title "【待办】xxx" \
    --start_time "2026-04-05T09:00:00+08:00" \
    --end_time "2026-04-05T18:00:00+08:00" \
    --attendees "XXX" \
    --description "里程碑：xxx\n负责人：XXX\n来源文档：https://XXX" \
    --reminder_minutes 1440
```

**参数说明：**

| 参数 | 值 | 说明 |
|------|-----|------|
| `--title` | 【待办】+ 里程碑 | 日程标题 |
| `--start_time` | ISO8601 格式 | 日程开始时间（全天则为 09:00） |
| `--end_time` | ISO8601 格式 | 日程结束时间（全天则为 18:00） |
| `--attendees` | 负责人列表 | 日程参与者 |
| `--description` | 详细信息 | 包含里程碑、负责人、来源文档 |
| `--reminder_minutes` | 1440 | 提前 1440 分钟（1 天）提醒 |

---

### 步骤 4：批量创建日程

**批量处理脚本：**

```python
import subprocess
import json
from datetime import datetime

def create_calendar_event(todo, source_doc_url):
    """创建单个日历事件"""
    deadline = parse_fuzzy_time(todo['time'])
    
    # 构建命令
    cmd = [
        'feishu_calendar', 'create',
        '--title', f'【待办】{todo["task"]}',
        '--start_time', deadline.strftime('%Y-%m-%dT09:00:00+08:00'),
        '--end_time', deadline.strftime('%Y-%m-%dT18:00:00+08:00'),
        '--attendees', todo['owner'],
        '--description', f'里程碑：{todo["task"]}\n负责人：{todo["owner"]}\n来源文档：{source_doc_url}',
        '--reminder_minutes', '1440'  # 提前 1 天提醒
    ]
    
    # 执行命令
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ 创建成功：{todo['task']}")
        return json.loads(result.stdout)
    else:
        print(f"❌ 创建失败：{todo['task']}")
        print(result.stderr)
        return None

# 批量创建
source_doc = "https://XXX"
for todo in todos:
    create_calendar_event(todo, source_doc)
```

---

## 完整示例

### 输入

**Thomas 消息：**
```
创建日历，从以下文档提取待办：
https://XXX
```

### 执行过程

**1. 读取文档：**
```bash
feishu_doc read --doc_token XXX
```

**2. 解析待办表格：**
```python
todos = [
    {
        'time': '下周',
        'task': 'xxx',
        'owner': 'xxx'
    },
    {
        'time': '4 月 8 日',
        'task': 'xxx',
        'owner': 'xxx'
    },
    {
        'time': '4 月份',
        'task': 'xxx',
        'owner': 'xxx'
    },
    {
        'time': '5 月或 6 月底',
        'task': 'xxx',
        'owner': '全体'
    }
]
```

**3. 解析时间：**
```python
parse_fuzzy_time('下周') → 2026-04-05
parse_fuzzy_time('4 月 8 日') → 2026-04-08
parse_fuzzy_time('4 月份') → 2026-04-15
parse_fuzzy_time('5 月或 6 月底') → 2026-06-30
```

**4. 创建日历：**
```bash
# 待办 1
feishu_calendar create \
    --title "【待办】xxx" \
    --start_time "2026-04-05T09:00:00+08:00" \
    --end_time "2026-04-05T18:00:00+08:00" \
    --attendees "xxx" \
    --description "里程碑：xxx\n负责人：xxx\n来源文档：https://XXX" \
    --reminder_minutes 1440

# 待办 2
feishu_calendar create \
    --title "【待办】xxx" \
    --start_time "2026-04-08T09:00:00+08:00" \
    --end_time "2026-04-08T18:00:00+08:00" \
    --attendees "xxx" \
    --description "里程碑：xxx\n负责人：xxx\n来源文档：https://XXX" \
    --reminder_minutes 1440

# ... 其他待办
```

### 输出

**创建结果：**
```
✅ 创建成功：xxx (2026-04-05)
✅ 创建成功：xxx (2026-04-08)
✅ 创建成功：xxx (2026-04-15)
✅ 创建成功：xxx (2026-06-30)

总计：4 个日程已创建
```

---

## 技术配置

### 前置条件

1. **飞书应用权限**
   - 飞书文档读取权限
   - 飞书日历创建权限
   - 飞书联系人读取权限（解析负责人）

2. **依赖**
   - Python 3.8+
   - OpenClaw 2026.3.13+

---

## 错误处理

### 常见错误及解决方案

**错误 1：文档无待办表格**
```
错误：未找到待办表格
解决：检查文档是否包含"时间节点 | 里程碑 | 负责人"格式的表格
```

**错误 2：时间解析失败**
```
错误：无法解析时间"下个月"
解决：添加更多模糊时间解析规则，或手动指定日期
```

**错误 3：负责人不在通讯录**
```
错误： attendees "XXX" 不在通讯录
解决：使用飞书用户 ID 或 open_id 代替姓名
```

**错误 4：日历创建失败**
```
错误：权限不足
解决：检查飞书应用是否有日历创建权限
```

---

## 最佳实践

### 1. 时间解析规则优先级

| 优先级 | 时间格式 | 解析规则 |
|--------|---------|---------|
| 1 | 精确日期（4 月 8 日） | 直接使用 |
| 2 | 模糊范围（下周） | 当前日期 +7 天 |
| 3 | 月份（4 月份） | 取月中（15 日） |
| 4 | 相对时间（下周） | 当前日期 +7 天 |

### 2. 日程标题规范

```
【待办】+ 里程碑内容

示例：
✅ 【待办】xxx
✅ 【待办】xxx
```

### 3. 提醒设置

| 类型 | 提前时间 | 适用场景 |
|------|---------|---------|
| 重要里程碑 | 1440 分钟（1 天） | 关键节点 |
| 一般任务 | 60 分钟（1 小时） | 日常任务 |
| 长期项目 | 10080 分钟（7 天） | 月度/季度目标 |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.4 | 2026-03-29 | 所有 TODO 内容全部替换为 xxx（产能调研/系统上线/成果展示等全部脱敏） |
| v1.0.3 | 2026-03-29 | 完全脱敏所有示例数据（人名/项目名/链接全部替换为 XXX） |
| v1.0.2 | 2026-03-29 | 完全重写执行过程示例，所有敏感信息已脱敏为 XXX |
| v1.0.1 | 2026-03-29 | 修复敏感信息泄露问题，所有示例人名和项目名称已脱敏为 XXX |
| v1.0.0 | 2026-03-29 | 初始版本 |

---

## 许可证

MIT License

---

## 维护者

OpenClaw Community
