---
name: academic-email-finder
description: |
  学术人员邮箱批量搜索工具。从姓名+单位出发，通过搜索引擎自动查找学术人员的邮箱地址，结果写入Excel文件。

  触发词：邮箱搜索、学术邮箱、批量找人、email搜索、搜邮箱
---

# 学术人员邮箱批量搜索工具

> 版本：v1.0
> 用途：根据姓名+单位，自动从全网搜索学术人员邮箱
> 定位：单次任务型Skill，不驻留后台

---

## 能力概述

**输入：** Excel文件（含姓名列+单位列）
**输出：** 在原文件新增一列"邮箱"，逐行填入搜索到的地址

---

## 工作流程

```
1. 用户提供Excel文件路径 + 说明哪列是姓名、哪列是单位
2. 解析Excel，提取所有姓名+单位对
3. 对每条记录执行搜索：
   搜索词：「姓名 + 单位 + 教授/老师/讲师 + 邮箱」
4. 从搜索结果摘要中识别邮箱（正则匹配）
5. 优先保留官方域名邮箱（.edu.cn / .cn / .gov.cn）
6. 排除qq.com / 163.com 等个人邮箱（除非无更好选择）
7. 将邮箱写入指定列
8. 输出完成后的文件路径
```

---

## 搜索策略（三层级）

### 第1层：高校/机构官网教师主页
```
搜索词格式：
「{姓名} {单位} 教授 邮箱」
「{姓名} {单位} 副教授 邮箱」
「{姓名} {单位} 讲师 邮箱」
「{姓名} {单位} 导师 邮箱」
「{姓名} {单位} 研究生导师 email」

命中目标：xx大学人事处/研究生院/院系官网的教师主页
```

### 第2层：学术平台个人主页
```
搜索词格式：
「{姓名} {单位} email」
「{姓名} 研究方向 email」
「{姓名} {单位} 通讯作者」

命中目标：ResearchGate / Google Scholar / CNKI / 百度学术
```

### 第3层：论文PDF中的通讯作者邮箱
```
搜索词格式：
「{姓名} {单位} 论文 PDF」
「{姓名} {论文标题片段} 邮箱」

命中目标：论文PDF里通常标注通讯作者邮箱
```

---

## 邮箱识别规则

```python
import re

def extract_email(text):
    """从文本中提取邮箱地址"""
    # 匹配标准邮箱格式
    pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    matches = re.findall(pattern, text)

    # 优先级排序
    priority_domains = ['.edu.cn', '.gov.cn', '.ac.cn', '.cn', '.org']
    personal_domains = ['qq.com', '163.com', '126.com', 'gmail.com', 'hotmail.com', 'outlook.com']

    for email in matches:
        domain = email.split('@')[1].lower()
        # 跳过个人邮箱
        if any(pd in domain for pd in personal_domains):
            continue
        # 优先机构邮箱
        if any(pd in domain for pd in priority_domains):
            return email
        # 没有机构邮箱则退而求其次
        return email if matches else None

    return matches[0] if matches else None
```

---

## Excel操作规范

```python
import openpyxl

def write_email_to_excel(file_path, row_number, email, email_column=6):
    """将邮箱写入Excel

    Args:
        file_path: Excel文件路径
        row_number: 数据行号（1-based，含表头）
        email: 邮箱地址，没找到填"未找到"
        email_column: 邮箱列号（默认F列=6）
    """
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    ws.cell(row=row_number, column=email_column, value=email)
    wb.save(file_path)
```

---

## 局限性说明

| 渠道 | 可用性 | 备注 |
|------|--------|------|
| 高校官网教师主页 | ✅ 优先命中 | 信息公开，覆盖率较高 |
| 科研机构官网 | ✅ 可用 | 研究院/医院等 |
| 学术平台 | ✅ 辅助 | CNKI/Google Scholar/ResearchGate |
| 论文通讯作者 | ✅ 可用 | 仅限通讯作者，且需能找到论文 |
| 百度/Google直接搜 | ⚠️ 辅助 | 可能搜到多个同名学者，需核对 |
| 付费数据库 | ❌ 不可用 | 知网/万方需账号 |

**已知风险：**
- **同名不同人**：搜索"林也平 湖南大学"可能匹配到"林亚平"（重名）→ **需要人工复核**
- **冷门学者**：小众院校/地方机构可能官网不公开信息
- **个人信息保护**：部分学者主动隐藏邮箱
- **覆盖上限**：非高校机构（医院/国企/地方政府）官网往往没有教师主页

**建议：搜索完成后抽样验证（随机取5-10条用搜索引擎复核）**

---

## 使用示例

### 场景：用户提供Excel，需要填邮箱

**Step 1：用户提供文件**
```
文件路径：/tmp/people.xlsx
姓名列：B列（第2列）
单位列：C列（第3列）
邮箱写入列：F列（第6列）
```

**Step 2：解析文件**
```python
import openpyxl
wb = openpyxl.load_workbook('/tmp/people.xlsx')
ws = wb.active
people = []
for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
    name = row[1]  # B列
    unit = row[2]  # C列
    if name:
        people.append({'row': i+2, 'name': name, 'unit': unit})
```

**Step 3：逐条搜索（子Agent自动化）**
```
对每条记录：
  → web_search：「{name} {unit} 邮箱」
  → 提取邮箱
  → 写入 F列
  → 每20条汇报一次进度
```

**Step 4：输出结果**
```
/tmp/people_with_emails.xlsx
```

---

## 快速启动命令

如需立即对某个Excel运行搜索，复制以下提示词给子Agent：

```
你是一个邮件地址搜索机器人。任务：根据名单逐一搜索学术人员的邮箱地址。

## 输入文件
读取 /tmp/people_list.json，里面有N条记录，格式：
[{"row": 行号, "name": "姓名", "unit": "单位", "title": "论文标题"}, ...]

## 任务流程
对每一条记录：
1. web_search 搜索「姓名 + 单位 + 教授/老师 + 邮箱」
2. 从搜索结果中提取邮箱地址（格式：xxx@domain.com）
3. openpyxl 将邮箱写入 /tmp/target.xlsx 的第6列（F列）
4. 行号对应：第row行
5. 找到写入邮箱，没找到写入"未找到"
6. 每20人输出进度

## 邮箱识别
- 优先.edu.cn / .ac.cn等机构域名
- 排除qq.com / 163.com等个人邮箱
- 同名不同人时选择最匹配的

## 输出
覆盖保存 /tmp/target.xlsx
最后输出统计：找到X个，未找到Y个
```

---

## 版本历史

### v1.0
- ✅ 基本搜索流程
- ✅ 三层搜索策略
- ✅ 邮箱正则识别
- ✅ Excel读写
- ⚠️ 同名区分需人工复核

---

*Skill版本：v1.0*
*创建：小柱（ArkClaw）*
*最后更新：2026-04-21*
*用途：学术人员邮箱批量采集*
