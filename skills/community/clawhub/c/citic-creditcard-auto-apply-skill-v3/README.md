# citic-creditcard-auto-apply

这是把原先“声明式 YAML steps”改写成 **OpenClaw 更适合落地的结构** 的版本：

- `SKILL.md`：告诉 agent 何时使用 browser 和本地脚本
- `config/workflow.template.yaml`：流程模板，只用于配置和说明
- `scripts/profile_extractor.py`：从工作区资料中提取候选字段
- `scripts/build_application_plan.py`：生成可执行计划 JSON
- `scripts/citic_cc_advisor.py`：输出卡种推荐（markdown / json）

## 为什么要这样改

OpenClaw 的 skill 负责“教 agent 怎么做”，不是原生 step-runner。
所以：

- 你的 YAML 仍然保留，但转成模板文件
- 真正执行网页操作的，是 OpenClaw 的 `browser` 工具
- 真正组织数据的，是本地脚本输出的 JSON

## 推荐用法

### 1. 准备客户资料

复制并填写：

```bash
cp profiles/applicant_profile.template.json profiles/applicant_profile.json
```

### 2. 生成推荐结果

```bash
python3 scripts/citic_cc_advisor.py recommend --profile profiles/applicant_profile.json
```

或：

```bash
python3 scripts/citic_cc_advisor.py recommend --profile profiles/applicant_profile.json --format json
```

### 3. 提取候选申请字段

```bash
python3 scripts/profile_extractor.py --workspace . --json --out output/candidates.json
```

### 4. 生成完整预填计划

```bash
python3 scripts/build_application_plan.py   --workspace .   --workflow config/workflow.template.yaml   --out output/application_plan.json
```

### 5. 让 OpenClaw 按 SKILL.md + browser 工具执行

推荐流程：

1. 先推荐卡种
2. 用户选定卡片
3. 用户授权读取资料
4. 生成并确认候选字段
5. 用 browser 打开官网申请页
6. 预填资料
7. 停在最终提交前

## 文件结构

- `SKILL.md`
- `config/workflow.template.yaml`
- `data/card_catalog.json`
- `scripts/citic_cc_advisor.py`
- `scripts/profile_extractor.py`
- `scripts/build_application_plan.py`
- `profiles/applicant_profile.template.json`
- `docs/browser_workflow.md`
- `docs/security_notes.md`

## 依赖

```bash
pip install -r requirements.txt
```

## 部署

将整个文件夹放到：

- `<workspace>/skills/citic-creditcard-auto-apply/`
- 或 `~/.openclaw/skills/citic-creditcard-auto-apply/`

然后重新开启 OpenClaw session。
