---
name: alert-inspection
description: 当用户要求进行设备健康巡检、告警审查、巡检报告生成或导出监控告警到 Excel 时使用。通过 Python 获取监控数据，生成 Markdown 巡检报告，并导出包含 4 个 Sheet 的 Excel 工作簿。
---

# 设备健康巡检 Skill

## Overview

用纯 Python 流程完成一次设备健康巡检：

1. 分开取正常主机、异常主机和告警数据
2. 生成文本巡检报告
3. 落盘标准化 `hosts.json` / `problems.json`
4. 基于模板生成一次性临时导出脚本
5. 导出 4 个 Sheet 的 `.xlsx`

## Files

- 主入口: `skills/alert-inspection/generate_report.py`
- 共享取数与归一化逻辑: `skills/alert-inspection/alert_data.py`
- Excel 模板脚本: `skills/alert-inspection/references/export_excel_template.py`
- 配置文件: `skills/alert-inspection/.env`

## Default Workflow

用户说“做巡检”“监控设备巡检”“告警巡检”时，默认按以下顺序执行：

1. 运行：

```bash
python3 skills/alert-inspection/generate_report.py --output reports
```

该脚本内部必须按以下方式查询主机，不要改成一次性全量 host-list：

- 正常主机：`host-list` 传 `active_status=0`
- 异常主机：`host-list` 传
  - `active_status[0]=1`
  - `active_status[1]=5`
  - `active_status[2]=4`
  - `active_status[3]=3`
  - `active_status[4]=2`
  - `active_status[5]=-1`

然后合并两次主机查询结果，再继续生成报告和 Excel。

2. 读取输出 JSON，获得：
   - `report_file`
   - `hosts_file`
   - `problems_file`
   - `environment_name`
   - `export_template`

3. 直接在回复中给出文本巡检结论。不要再猜测不存在的“生成报告命令”；文本报告由模型基于 `report_markdown` 或落盘的 Markdown 文件直接返回。

4. 基于模板生成本次专用临时导出脚本，再执行导出：

```bash
cp skills/alert-inspection/references/export_excel_template.py /tmp/alert_inspection_export.py
```

把下列占位符替换为本次真实值：

- `{{HOSTS_JSON}}`
- `{{PROBLEMS_JSON}}`
- `{{OUTPUT_XLSX}}`
- `{{ENVIRONMENT_NAME}}`
- `{{CURRENT_TIME}}`

然后执行：

```bash
python3 /tmp/alert_inspection_export.py
```

5. 回复中必须同时返回：
   - 文本巡检报告或巡检结论
   - 实际生成的 `.xlsx` 文件路径

## Hard Rules

- 这是纯 Python skill。不要调用 `node`、`tsx`、`index.ts`，也不要猜测 `report`、`generate-report`、`export` 之类不存在的 CLI 子命令。
- 文本巡检报告和 Excel 导出是同一次巡检的必交付物，不要拆成“先给报告，再问是否导出 Excel”。
- 不要再询问用户“是否需要导出 Excel”；默认必须一起导出。
- 模板脚本只是结构模板。真正执行时，必须生成一次性的临时导出脚本，并替换成这次巡检的真实数据路径和时间。
- 主机查询必须分两次执行：正常主机单独查 `active_status=0`，异常主机单独查 `active_status[0..5]=1,5,4,3,2,-1`；不要改成单次 host-list 全量查询后本地再猜测分组。
- `巡检概览` 是一个完整的 Sheet，里面包含标题、告警概览表、主机概览表、巡检结论等所有内容。严禁把这些子段拆成独立的 Sheet。Excel 有且只有 4 个 Sheet，不能多也不能少。

## Report Template

**重要：下面所有内容（标题、告警概览表、主机概览表、巡检结论）全部属于同一个 Sheet「巡检概览」，必须写入同一个 worksheet。严禁把这些内容拆分成多个 Sheet。Excel 总共只有 4 个 Sheet，「巡检概览」是第一个，它包含了下面模板的全部内容。**

文本报告与 `Sheet1: 巡检概览` 都必须复用下面这套结构：

```text
🚨 设备健康巡检报告 · {环境名称}
巡检时间：{当前时间}
报告生成: lerwee运维智能体

📊 告警概览
告警等级    数量   占比
紧急(P5)    {n}    {n}%
严重(P4)    {n}    {n}%
次要(P3)    {n}    {n}%
警告(P2)    {n}    {n}%
信息(P1)    {n}    {n}%
合计        {total}    100%

📋 主机概览
主机状态    数量 占比
正常主机   {n}  {n}%
异常主机   {n}  {n}%
合计      {total}    100%

📌 巡检结论
● 🔴 {紧急+严重数}条高危告警需立即处理
● ⚠️ {次要+警告数}条告警需关注
● ✅ {正常主机数}台主机无告警
```

## Excel Contract

Excel 必须且只能包含以下 4 个 Sheet，名称和顺序必须完全一致：

1. `巡检概览`
2. `正常主机`
3. `异常主机`
4. `异常详细清单`

字段要求：

- `巡检概览`：必须复用 `## Report Template` 中的标题、巡检时间、`📊 告警概览`、`📌 巡检结论`
- `正常主机`：`主机名`、`IP`、`监控类型`、`监控状态`、`采集状态`
- `异常主机`：`主机名`、`IP`、`监控类型`、`监控状态`、`采集状态`
- `异常详细清单`：`主机名`、`IP`、`告警描述`、`告警等级`、`告警时间`、`持续时长`

不得缺少 Sheet，不得新增额外 Sheet，不得修改名称或顺序。

主机字段语义：

- `监控类型`：优先使用 `classification_label`，否则使用 `classification` 映射后的中文类型
- `监控状态`：优先使用 `active_status_label`；数值含义为 `active_status`，其中 `-1=未监控`、`0=正常`、`1=信息`、`2=警告`、`3=次要`、`4=严重`、`5=紧急`
- `采集状态`：优先使用 `power_label`；数值含义为 `power_status`，其中 `1=正常`、`2=异常`

主机分组规则：

- `正常主机` 数据来源必须是 `host-list active_status=0`
- `异常主机` 数据来源必须是 `host-list active_status[0]=1 active_status[1]=5 active_status[2]=4 active_status[3]=3 active_status[4]=2 active_status[5]=-1`
- 合并两次查询后的主机全集，再用于整体巡检统计
- 不要根据“是否存在告警明细”来划分 `正常主机` 和 `异常主机`

## Configuration

需要以下环境变量：

- `LWJK_API_URL`
- `LWJK_API_SECRET`

默认从 `skills/alert-inspection/.env` 读取。

## Common Commands

全量巡检：

```bash
python3 skills/alert-inspection/generate_report.py --output reports
```

按监控类型巡检：

```bash
python3 skills/alert-inspection/generate_report.py --classification 101 --output reports
```

从本地 JSON 复用已有数据：

```bash
python3 skills/alert-inspection/generate_report.py \
  --hosts-file reports/xxx.hosts.json \
  --problems-file reports/xxx.problems.json \
  --output reports
```

## Completion Checklist

完成前必须自检：

- 已生成 Markdown 巡检报告
- 已生成标准化 `hosts.json` 和 `problems.json`
- 已实际生成可打开的 `.xlsx` 文件
- Sheet 数量等于 4
- Sheet 名称和顺序完全正确
- `正常主机` 和 `异常主机` 已严格按 `active_status` 划分
- 实际主机查询已按“两次 host-list”执行，而不是一次全量查询
- 文本报告与 `巡检概览` 基于同一批完整分页数据

如果因为依赖、权限、配置或运行环境问题导致 `.xlsx` 无法生成，必须明确说明阻塞原因，并指出任务未完成。
