# cron_jobs/ — 生产 cron 任务的人类可读镜像

## ⚠️ 重要：本目录文件**不被任何代码读取**

`cron_jobs/cron_mirror.json` 是 `~/.hermes/cron/jobs.json` 里**独立脚本型 cron 任务的人类可读副本**。

- **不被 `skill_dispatcher.py` 读取**（dispatcher 只读 `templates/*.json`）
- **不被 OpenClaw cron 直接读取**（OpenClaw 只读 `~/.hermes/cron/jobs.json`）
- 作用是**给 AI / 用户审计**："A 股 3 个独立脚本任务在生产 cron 里到底是怎么配的"

## 文件清单

| 文件 | 作用 |
|------|------|
| `cron_mirror.json` | **唯一镜像文件**，内含 3 任务（close_summary/intraday/ipo_report）|
| `README.md` | 本文件 |

v3.1.4 起 3 镜像合为单文件，强制一致，避免之前"改一处忘改别处"的纪律性 bug。

## 4 端真相分布

| 维度 | 在哪里 | 角色 |
|------|--------|------|
| **LLM 调度模板** | `templates/{morning,evening,weekend}.json` | 被 `skill_dispatcher.py` 读取 |
| **生产 cron 真实配置** | `~/.hermes/cron/jobs.json` | 被 OpenClaw 读取并定时触发 |
| **本目录归档镜像** | `cron_jobs/cron_mirror.json` | **人类审计用**，内含 3 任务镜像，prompt 字段与 jobs.json 一字不差 |
| **SKILL.md 文档** | `SKILL.md` 任务清单段 | 文档层说明 |

## 单文件结构

```json
{
  "_meta": { "purpose": "...", "mirror_of": "...", "version": "...", "history": "...", "see_also": "..." },
  "tasks": {
    "close_summary": { "name": "A股收盘小结", "schedule": "...", "prompt": "...", ... },
    "intraday":      { "name": "A股盘中预警", "schedule": "...", "prompt": "...", ... },
    "ipo_report":    { "name": "A股IPO周报", "schedule": "...", "prompt": "...", ... }
  }
}
```

任务键名（close_summary/intraday/ipo_report）= 文件名时代的标识，跟历史档案一致。

## 维护纪律

**修改 `jobs.json` 里的 prompt 时，必须同步修改 `cron_jobs/cron_mirror.json` 中对应任务**，保证镜像与生产一致。

**🛡️ v3.1.5+ 推荐用护栏脚本一次性检查 4 端一致性**（templates ↔ cron_mirror ↔ jobs.json ↔ SKILL.md）：

```bash
python3 /root/.hermes/skills/A-stock-report/scripts/check_consistency.py
# exit 0=全过，1=有错误
# 加 --verbose 看每条 ✅，加 --fix-hint 看修复建议
```

**legacy 一行命令**（仅检查镜像与 jobs.json 的 prompt 一致性，v3.1.4 时代的命令，v3.1.5 起推荐上面那个）：

```bash
python3 -c "
import json
jobs = json.load(open('/root/.hermes/cron/jobs.json'))
mirror = json.load(open('/root/.hermes/skills/A-stock-report/cron_jobs/cron_mirror.json'))
m = {'A股收盘小结':'close_summary','A股盘中预警':'intraday','A股IPO周报':'ipo_report'}
for j in jobs['jobs']:
    if j['name'] in m:
        mirror_prompt = mirror['tasks'][m[j['name']]]['prompt']
        print(j['name'], j['prompt'] == mirror_prompt)
"
```

## 历史

- **v3.1.4 (2026-06-09)**: 合井 3 文件为 `cron_mirror.json`（67 行 / 2.6KB），README 同步更新
- **v3.1.3 (2026-06-09)**: 新建 `cron_jobs/intraday.json` 镜像（v3.0~v3.1.2 期间已存在 close_summary/ipo_report 镜像）
- **备份位置**: `/workspace/archive/cron_jobs_3split_20260609_1952.bak/`（v3.1.4 前 3 文件的完整备份）
