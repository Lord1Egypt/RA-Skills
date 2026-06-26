---
name: feishu-bitable-weekly-report-merge
description: 飞书多维表格周报权限检查与合并一体化工具。用户输入一个飞书多维表格 URL，自动完成：提取「链接地址」列 → 批量检查飞书文档阅读权限 → 将有权限的文档按章节合并为新文档。输出有权限列表、无权限列表，以及合并后的新飞书文档链接。触发词：多维表格周报合并、批量合并周报、多维表格文档合并。
---

# Feishu Bitable Weekly Report Merge

输入多维表格 URL，一键完成权限检查 + 文档合并全流程。

## 工作流程

### Step 1：解析多维表格 URL

支持格式：
- 完整 URL：`https://asiainfo.feishu.cn/base/FDo4bVmnVaYRJlslJttcPwgwnfh?table=tblRjin7OM9XvEDL&view=vew3qPDrS3`
- 仅 app_token：需同时提供 table_id

从 URL 提取：
- `app_token`：第一个路径段
- `table_id`：`table=` 参数值

### Step 2：查找「链接地址」列字段 ID

调用 `feishu_bitable_app_table_field` 获取表结构，找到字段名「链接地址」的 `field_id`。

### Step 3：提取所有记录

调用 `feishu_bitable_app_table_record`，返回 `员工姓名` + `链接地址` 两列。

### Step 4：批量检查文档权限

对每个链接调用 `feishu_fetch_doc`：
- 成功 → 有权限
- `forBidden` → 无权限
- `frequency limit` → 等 3 秒重试，再失败视为无权限

### Step 5：输出结果

向用户汇报：
- ✅ 有权限文档（数量 + 列表）
- ❌ 无权限文档（数量 + 列表）

### Step 6：合并有权限文档

**注意：需先向用户确认是否继续合并操作**，避免自动合并大量文档产生不预期结果。

合并规则（详见 `references/merge_rules.md`）：
- 按文档提供顺序拼接
- 每位员工前加 `## 【姓名】` 子标题
- Part1~Part5 依次排列
- 原文不修改不总结，`lark-table` 等格式保留

调用 `feishu_create_doc` 创建合并文档，标题：
`[AIO]-[姓名1/姓名2/...]-周报合并-YYYY-MM`

## 关键约束

1. **确认后再合并**：权限检查完成后，输出有/无权限列表后，先问用户"是否将以上有权限的文档合并？"，用户确认后再执行合并
2. **权限隔离**：只向 owner 报告结果
3. **限流处理**：每个文档最多重试 2 次，每次间隔 3 秒
4. **空表处理**：如果所有文档均无权限，告知用户并结束

## 工具依赖链

```
feishu_bitable_app_table_field  → 查字段
feishu_bitable_app_table_record → 读记录
feishu_fetch_doc                → 验权限
feishu_create_doc               → 建合并文档
```

详细权限判断逻辑见 `references/permission_rules.md`。
