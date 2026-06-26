---
name: ai-question
description: 通过对话框模型从上传资料生成或规范考试题库 Excel，并启动或停止 QuizAI 刷题服务。Use when the user asks to 生成题库、规范题库、格式化题库、考试题目、ai-question、generate-question-bank、normalize-question-bank、start-question-service、stop-question-service、上传资料出题、模型出题，或需要启动/停止本项目 Python 服务。
---

# AI Question — 资料出题 Skill

在含 `run.py` 的 **QuizAI 仓库根目录** 使用本 skill（FastAPI 刷题应用 + 本技能包）。

## 安装与路径

| 环境 | Skill 目录 |
|------|------------|
| **ClawHub / OpenClaw**（推荐发布源） | `skills/ai-question` |
| Cursor | `.cursor/skills/ai-question`（联接至 `skills/ai-question`） |
| Claude Code | `.claude/skills/ai-question` 或 `~/.claude/skills/ai-question` |

- 下文命令均在**仓库根目录**执行，脚本路径统一为 `skills/ai-question/scripts/`。
- 发布到 ClawHub：`clawhub skill publish skills/ai-question --slug ai-question --name "AI Question" --version <semver> --changelog "..."`（需先 `clawhub login`）。
- 本地安装：`clawhub install ai-question`（安装到 workdir 的 `./skills/`）。

## 四大功能

| 功能 | 命令标识 | 方式 |
|------|----------|------|
| 生成题库 | `generate-question-bank` | **对话框模型出题** + 脚本导出 |
| 规范题库 | `normalize-question-bank` | `scripts/normalize_question_bank.py` |
| 启动服务 | `start-question-service` | `scripts/start_question_service.ps1` |
| 暂停服务 | `stop-question-service` | `scripts/stop_question_service.ps1` |

用户 @ 本 skill 或说明上述功能时，按对应章节执行。

---

## 1. 生成题库（generate-question-bank）

### 目标

根据用户上传的**学习资料**，由**当前对话框中的模型**阅读资料并出题，再导出为标准 Excel（格式见 [reference.md](reference.md)）。

### 核心原则

> **禁止**调用 `app/services/ai_generator.py` 本地模板出题。  
> **必须**由 Agent 在对话中阅读资料、生成题目 JSON，再用脚本导出 Excel。

详细规范见 **[generation-guide.md](generation-guide.md)**（执行本功能前必须先读）。

### 强规则

1. 题目**严格基于资料**，不得编造
2. 题干**不含**「第 1 题」「第 2 题」等序号
3. 题型顺序：**单选题 → 判断题 → 多选题**
4. 解析紧扣资料，点明对错原因与核心知识点，不冗余
5. 判断题 **A=正确、B=错误**（固定顺序不打乱），解析与答案字母一致
6. 单选/多选导出时脚本会**随机打乱选项**（模型生成时可先把正确答案放 A）

### 工作流

```
Task Progress:
- [ ] 读取 generation-guide.md
- [ ] 运行 extract_material.py 提取资料文本
- [ ] 在对话中阅读资料，按规范生成题库 JSON
- [ ] 将 JSON 写入 data/generated-bank.json（或用户指定路径）
- [ ] 运行 export_question_bank.py 导出 xlsx
- [ ] 确认输出文件存在、题量正确、题干无序号前缀
- [ ] 询问用户是否导入刷题系统；若确认，运行 import_bank_to_db.py
```

### Step 1：提取资料

```bash
python skills/ai-question/scripts/extract_material.py "资料.docx" -o data/material-extract.txt
```

### Step 2：对话框模型出题

Agent 阅读 `data/material-extract.txt`（或用户 @ 的文件），按 [generation-guide.md](generation-guide.md) 生成 JSON，写入：

```
data/generated-bank.json
```

### Step 3：导出 Excel

```bash
python skills/ai-question/scripts/export_question_bank.py data/generated-bank.json -o "输出题库.xlsx"
```

### Step 4：询问是否导入刷题系统

Excel 导出成功后，**必须**询问用户：

> 题库已生成。是否导入到刷题系统（写入本地数据库）？

- **用户同意**：运行 `import_bank_to_db.py`（优先用 JSON，与 Excel 选项打乱一致）
- **用户拒绝**：结束，告知 xlsx 路径即可

```bash
python skills/ai-question/scripts/import_bank_to_db.py data/generated-bank.json
```

导入成功后告知：题库 ID、我的题库 `http://127.0.0.1:8000/banks`、刷题 `http://127.0.0.1:8000/practice/{id}`。若服务未启动，提示先执行 `start-question-service`。

### 辅助脚本

| 脚本 | 作用 |
|------|------|
| `extract_material.py` | 从 pdf/doc/docx/txt/md 提取文本 |
| `export_question_bank.py` | JSON → 规范 xlsx（含选项打乱、题型排序） |
| `import_bank_to_db.py` | JSON / Excel → 写入 `data/quizai.db` |
| `generate_question_bank.py` | 仅提取资料并提示后续步骤；或 `--json` 直接导出 |

若 JSON 已生成，可一步导出：

```bash
python skills/ai-question/scripts/generate_question_bank.py "资料.pdf" -o "输出.xlsx" --json data/generated-bank.json
```

---

## 2. 规范题库（normalize-question-bank）

用户上传的文件**本身就是题库**但格式不规范时，运行：

```bash
python skills/ai-question/scripts/normalize_question_bank.py "原始题库.docx" -o "规范题库.xlsx"
```

实现：`app/services/bank_normalizer.py`（规则解析，非对话框出题）。

---

## 3. 启动服务（start-question-service）

```powershell
.\start.ps1
```

或：

```powershell
.\skills\ai-question\scripts\start_question_service.ps1
```

验证：`Invoke-WebRequest http://127.0.0.1:8000/health -UseBasicParsing`

> ClawScan：本 skill 会启动本地 FastAPI（`127.0.0.1:8000`），仅用于刷题 Web，非外网回调。

---

## 4. 暂停服务（stop-question-service）

```powershell
.\skills\ai-question\scripts\stop_question_service.ps1
```

---

## 目录结构

```
skills/ai-question/
├── SKILL.md
├── skill.manifest.json
├── generation-guide.md   # 对话框模型出题规范（必读）
├── reference.md
└── scripts/
    ├── _quizai_root.py
    ├── extract_material.py
    ├── export_question_bank.py
    ├── import_bank_to_db.py
    ├── generate_question_bank.py
    ├── normalize_question_bank.py
    ├── start_question_service.ps1
    └── stop_question_service.ps1
```

## 故障排查

| 现象 | 处理 |
|------|------|
| 题目质量差 | 确认 Agent 已读 generation-guide.md 与完整资料，非本地模板 |
| 导出失败 | 检查 JSON 格式与 questions 非空 |
| 资料解析失败 | 确认 pdf/doc/docx/txt/md 格式 |
| 导入 DB 失败 | 确认 `data/quizai.db` 可写；JSON 中 questions 非空 |
| 规范题库失败 | 使用 normalize-question-bank |
| 找不到项目根 | 在含 `run.py` 的仓库根目录打开 Agent；脚本会自动向上查找 |
