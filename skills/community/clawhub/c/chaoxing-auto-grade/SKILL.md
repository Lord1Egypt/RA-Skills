---
name: chaoxing-auto-grade
description: 超星学习通(MOOC)作业下载、自动批改与成绩处理。支持(1)通过Chrome CDP从超星教师端批量下载学生批阅HTML，(2)自动勾选显示客观题，(3)AI批改主观题，(4)清理HTML只保留题目-答案-分数。触发词：超星、学习通、自动批改、作业下载、成绩处理、主观题评分、填空题提取。
---

# 超星学习通 作业自动批改

## 工作流总览

```
① 配置 config.json → ② 下载作业HTML → ③ 提取主观题 → ④ AI批改 → ⑤ 写回评分 → ⑥ 清理输出
```

---

## 0. 前置准备

### Chrome 远程调试

```bash
# 以CDP模式启动Chrome（关闭所有Chrome窗口后运行）
chrome.exe --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir="C:\ChromeDebug"
```

### 安装依赖

```bash
pip install websockets
```

---

## 1. 下载作业 HTML

```bash
python scripts/download_homework.py --config config.json --login
```

`--login` 会在浏览器打开超星登录页，等待手动登录（或自动登录若密码已配置）。

**无 `--login`** 则假设已有登录态，直接开始下载。

### 参数

| 参数 | 说明 |
|------|------|
| `--login` | 首次运行需登录 |
| `--course "数据标注"` | 只下载指定课程 |
| `--students "张三,李四"` | 只下载指定学生 |

### config.json 下载相关配置

```json
{
  "login": {
    "chrome_port": 9222,
    "script_base": "https://mooc2-ans.chaoxing.com",
    "account": "手机号",
    "password": "密码",
    "cpi": "cpi参数（从超星URL获取）"
  },
  "download": {
    "target_students": ["学生A", "学生B"],
    "courses": [
      {"name": "课程名", "courseid": 123, "classes": [
        {"name": "班级名", "clazzid": 456}
      ]}
    ],
    "output_dir": "下载目录"
  }
}
```

**获取 courseid / clazzid / cpi**：登录后打开任意作业列表页，URL中 `courseid=xxx&clazzid=xxx&cpi=xxx`。

### 下载说明

- 每个学生按姓名创建子目录，文件命名 `学生名_课程_作业名.html`
- 自动勾选"显示客观题"checkbox + JS强制移除 `display:none`
- 支持作业列表分页 + 学生列表分页
- 已存在的文件自动跳过（断点续传）

---

## 2. 提取主观题 → JSON

```bash
python scripts/extract_subj.py --config config.json
```

读取 `paths.input_dir` 下所有HTML → 提取主观题（简答题）题干、学生答案、满分 → 输出 `{work_dir}/subj_questions.json`

---

## 3. AI 批改主观题

```bash
python scripts/grade_subj.py --config config.json
```

读取 `subj_questions.json` → 逐题调用LLM API评分 → 输出 `{work_dir}/subj_graded.json`

**特性**：
- 断点续评（已有记录跳过）
- 每 `save_every` 题自动保存
- API限流控制 `rate_limit_seconds`

---

## 4. 写回评分到原始HTML

```bash
python scripts/apply_scores.py --config config.json
```

读取 `subj_graded.json` → 在原始HTML的 `<input class="inputBranch questionScore">` 更新 `value` → 原地修改

---

## 5. 清理HTML（最终输出）

```bash
python scripts/clean_html.py --config config.json
```

读取 `paths.input_dir` → 输出到 `paths.output_dir`

**处理内容**：
- 剥离 `<script>`、`<style>`、编辑器垃圾
- 客观题（选择/判断）：学生答案、正确答案、得分、✓/✗标记
- **填空题**：多空答案 `|` 分隔（`<dd class="fillBox">` → `<p>`）
- **主观题**：读取AI评分后的分数
- 文件头显示 **总分汇总**

**缩减效果**：~75MB → ~2.5MB（~97%）

---

## HTML结构说明

### 清理后HTML

```html
<div class="header">
  <div class="title">学生名 — 作业名</div>
  <div class="meta">总分: XX.Y / ZZZ 分</div>
</div>
<div class="section-title">客观题 (N题)</div>
<div class="q-block">
  <div class="q-title">✓/✗ N. (题型, 分数)</div>
  <div class="q-stem">题目</div>
  <div class="answer-row">学生答案: xxx</div>
  <div class="answer-row">正确答案: xxx</div>
  <div class="score-row">得分: X / Y 分</div>
</div>
<div class="section-title">主观题 (N题)</div>
<div class="q-block">
  <div class="subj-answer">学生答案: ...</div>
  <div class="score-row">得分: X.X / Y 分</div>
</div>
```

### 关键DOM约束（原始HTML）

- 填空题学生答案：`<dd class="fillBox">` → `<p>`，非旧版 `学生答案：A` 格式
- 客观题对错标记基于得分对比（满分=✓）
- 主观题分数从 `<input class="inputBranch questionScore">` 的 `value` 读取

---

## 目录约定

```
output_dir/                  ← config.json → download.output_dir
├── 学生A/
│   ├── 学生A_课程_作业一.html
│   └── ...

work_dir/                    ← config.json → paths.work_dir
├── subj_questions.json      ← Step 2 输出
├── subj_graded.json         ← Step 3 输出
```