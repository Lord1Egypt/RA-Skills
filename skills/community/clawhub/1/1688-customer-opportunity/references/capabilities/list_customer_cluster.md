# list_customer_cluster

查询商家 AI 客群列表。客群是 brave-troops CRM 系统按算法将买家分组的结果，每个客群包含特征描述、分析原因及 planId；后续可凭 planId 调 `list_cluster_buyer_detail` / `get_cluster_marketing_plan` / `activate_cluster_plan`。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）
- 主账号 userId 由后端通过 AK 自动解析，无需传参

## 参数

无参数，固定返回老客客群。

## 返回字段

`data` 包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| cluster_count | int | 客群总数 |
| list | array | 客群列表 |
| list[].plan_id | string | 客群计划 ID（唯一键） |
| list[].cluster_name | string | 客群名称 |
| list[].cluster_main_tag | string | 客群主标签 code |
| list[].cluster_main_tag_desc | string | 客群主标签描述 |
| list[].buyer_type_desc | string | 客群买家类型 |
| list[].feature | string | 客群特征描述 |
| list[].plan_reason | string | 客群分析原因 |
| list[].buyer_num | int | 买家总数 |
| list[].daily_date | string | 当日更新日期（yyyyMMdd） |
| list[].rank | int | 客群排名（优先级） |
| list[].plan_ds | string | 数据分区日期（yyyyMMdd） |
| list[].status | int | 运营计划开启状态：0=未开启 / 1=启用 / 2=暂停 |

## 典型用法

**场景：查看老客 AI 客群，选一个客群后用 planId 串联后续操作**

```bash
python cli.py list_customer_cluster
# planId 用于后续 list_cluster_buyer_detail / get_cluster_marketing_plan / activate_cluster_plan
```

## 展示规则

- 全部结果以 Markdown 表格直接展示，不设数量阈值
- 表格列：# | 客群名称 | 买家数 | 特征描述
- 表格上方展示客群说明：根据店铺老客在平台上的行为表现，按不同维度智能划分客群…
- `plan_id` / `cluster_main_tag` 通过 HTML 注释嵌入，供后续步骤（`get_cluster_marketing_plan` / `list_cluster_buyer_detail`）使用

## 输出格式

### 成功

```json
{
  "success": true,
  "markdown": "...",
  "data": { "cluster_count": 3, "list": [...] }
}
```

### 失败

```json
{
  "success": false,
  "markdown": "错误描述信息"
}
```

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| AK 未配置 | 引导用户执行 `cli.py configure YOUR_AK` 配置 AK |
| cluster_count = 0 | 数据尚未更新（AI 客群通常每周一更新），告知用户稍后重试 |
| 接口返回格式异常 | 提示"格式异常，请稍后重试" |
| 其他运行时异常 | 原样输出错误信息 |

通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。
