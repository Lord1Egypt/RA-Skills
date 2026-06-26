# geo-monitor-toolkit 升级审计

## 审计结论

当前仓库本质上是一个 **文档优先的 GEO operating system 骨架**，而不是可以直接跑起来的 GEO monitoring toolkit。用户指出的问题与实际仓库结构高度一致，主要缺口如下。

| 优先级 | 问题 | 当前状态 | 本轮改造方向 |
|---|---|---|---|
| P0 | 可执行性不足 | 只有 playbooks、README、SKILL 和单个 Query Pool | 增加可运行 runner、打分脚本、示例产物目录 |
| P0 | 指标不可复现 | 有指标定义，但没有 rubric、annotation protocol、schema | 增加严格 rubric、标注协议、JSON Schema |
| P1 | 样例单一 | 仅有 MinerU 单案例 | 增加 SaaS、开源库、开发者工具共至少 3 个案例 |
| P1 | 结果闭环缺口 | 没有 action→metric change 的追踪结构 | 增加 repair validation 模板、experiment schema、回归结果目录 |
| P2 | 工程化缺失 | 无 CI、无 data/runs 规范、无产物 schema | 增加目录规范、CI、校验脚本、样例 run |

## 本轮最小可落地升级目标

本轮不追求做成真正连接各家闭源模型 API 的完整产品，而是交付一个 **可运行的离线/半自动评估骨架**，使团队可以：

1. 用统一 schema 准备 Query Pool 和回答样本；
2. 运行脚本生成标准化 run 目录；
3. 用统一 rubric 对回答进行打分；
4. 自动汇总四大指标并产出周报草稿；
5. 对修复动作做 T+7 / T+14 回归记录。

## 拟新增内容

| 类别 | 新增内容 |
|---|---|
| 脚本 | `scripts/run_monitor.py` `scripts/score_run.py` `scripts/generate_weekly_report.py` |
| Schema | `schemas/query-pool.schema.json` `schemas/run-results.schema.json` `schemas/repair-validation.schema.json` |
| 数据目录 | `data/query-pools/` `data/runs/` `data/repair-validations/` |
| Rubric | `rubrics/scoring-rubric.md` `rubrics/annotation-protocol.md` |
| 样例 | `data/query-pools/` 下增加 SaaS / open-source-library / developer-tool 示例 |
| 报告模板 | `templates/weekly-report.md` `templates/repair-validation.md` |
| 工程化 | `.github/workflows/ci.yml` `requirements.txt` `Makefile` |

## 执行原则

本轮将优先满足用户提出的五个落地项：runner、rubric、report schema、多行业样例、修复验证模板；同时顺手补齐最基础的工程化骨架，避免仓库继续停留在纯文档层。
