---
name: config-health-check
description: Convbox-DiagClaw Prof.Skill 的配置与 API 健康自检工具（聚焦凭证与接口连通，区别于店铺「经营健康」分析）。两阶段：校验 CONVBOX_API_KEY 与 access.yaml 是否就绪；对 access.yaml 中全部端点全量探测并按字段定义校验响应 schema。在「报错查不到数据」「上线/换环境前自检」「数据质量与追踪治理」场景由 Prof.Skill 调用。
metadata:
  openclaw:
    emoji: "🩺"
    type: utility
    primaryEnv: CONVBOX_API_KEY
    requires:
      env:
        - CONVBOX_API_KEY
license: MIT-0
---

# config-health-check — 配置与 API 健康自检（utility）

> 命名说明：本工具检查的是**凭证配置与接口连通**（technical health），与店铺**经营健康**（增长/留存等业务分析）相区分。

## 一、定位

属 `utilities/` 工具集。**叶子节点**：只读环境变量 `CONVBOX_API_KEY` 并直连 access.yaml 所定义的 Convbox API——不调用 Tools / Agent.Skills、不读写 Key 本体。

回答的是两个问题：

1. **配置是否完整** —— `CONVBOX_API_KEY` 是否就绪；`access.yaml` 是否存在、合法、结构齐全。
2. **API 响应是否正常** —— 对 access.yaml 中全部端点逐个真实探测，按其 `response_fields` / 样例定义逐字段校验响应 schema。

## 二、何时调用

由 Prof.Skill 在以下情形触发：

- 取数反复报错、`code != 1`、或怀疑 Key/连接异常时，先自检定位是配置问题还是数据问题。
- 「数据质量与追踪治理（Data Quality & Tracking Governance）」套餐里的连通性 / 配置体检环节。
- 上线、切换环境或轮换 Key 后的回归自检。

## 三、如何运行

脚本零业务依赖，仅需 PyYAML：

```bash
pip install pyyaml --break-system-packages   # 首次
python utilities/config-health-check/config_health_check.py
```

默认从 `../../access.yaml`（即 Prof.Skill 根目录的 access.yaml）读取端点定义。常用参数：

| 参数 | 作用 |
|------|------|
| `--config-only` | 只做阶段一，不发任何网络请求（无凭证 / 离线自检） |
| `--recent-window N` | 把日期型端点的窗口收敛为最近 N 天（默认用 access 样例日期） |
| `--json` | 以 JSON 输出，便于程序消费 |
| `--strict` | 把 WARN 也视为失败（CI 用） |
| `--access PATH` | 指定 access.yaml 路径 |
| `--timeout S` | 单请求超时秒数（默认 15） |

## 四、输出与判定

每条检查标 `OK / WARN / FAIL / SKIP`：

- **OK** —— 通过。空数据（区间内无记录）记 OK 并提示「不据空编造结论」。
- **WARN** —— schema 偏差（缺/多字段）、封套缺字段。access 响应侧为「代表性 schema」，线上字段可能演进，故记警告而非失败。
- **FAIL** —— 配置缺失、连通失败、HTTP 异常、非 JSON、或 `code != 1`。
- **SKIP** —— 前置不满足（如透传端点无已连接账户）。

透传端点（meta_query / google_query）会先经 connection_source 解析真实 account_id，无连接账户则 SKIP。

退出码：`0` 全通过 · `2` 有 FAIL · `1` 有 WARN（仅 `--strict`）。

## 五、安全约束

绝不打印、索要或回显 `CONVBOX_API_KEY` 本体（阶段一仅报告其是否存在与脱敏长度）。凭证只经 access.yaml 声明的请求头携带。
