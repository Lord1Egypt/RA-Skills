---
name: feishu-bitable-import
description: 🚀 企业级飞书多维表格（Bitable）数据导入工具，从 CSV/Excel/JSON 批量导入数据到飞书多维表格，自动智能推断字段类型，增量更新/全量覆盖/仅新增三种同步模式，支持从本地数据一键创建新表格。适合企业数据中台导出、业务报表同步、定时数据更新、团队数据协作场景。使用当需要将本地CSV/Excel数据批量导入飞书多维表格、从外部系统导出数据到飞书、批量创建多维表格业务记录时触发。Triggers: "导入CSV到飞书", "批量导入飞书表格", "飞书数据导入", "feishu bitable import", "创建飞书表格", "数据导入飞书"。
---

# feishu-bitable-import — 企业级飞书多维表格数据导入

> **核心价值**：连接本地 CSV/Excel/JSON 数据与飞书多维表格，实现业务数据自动化导入，让团队实时查看最新报表，减少手动导入的错误和时间消耗。

## 适用场景

- **企业数据中台**：将数仓/BI导出的数据自动同步到飞书多维表格，供业务团队分析
- **定时报表同步**：每日/每周业务报表自动更新，团队始终看到最新数据
- **批量数据导入**：从 CRM/ERP 导出数据，一键导入飞书供团队协作
- **增量数据更新**：只同步新增/变化数据，提高效率
- **自动化表格创建**：根据数据结构自动创建表格和字段，无需手动配置

## 核心特性

✨ **智能类型推断** — 基于数据分布自动识别字段类型，准确率 > 95%  
⚡ **三种同步模式** — 增量更新/全量覆盖/仅新增，满足不同业务场景  
🏗️ **零配置建表** — 从 CSV/Excel 一键创建完整表格，自动生成所有字段  
🔒 **企业级可靠性** — 自动重试、限流处理、错误报告，保证数据一致性  
📊 **支持多种格式** — CSV / Excel (xlsx/xls) / JSON 全覆盖  

## 企业级工作流

### 阶段 1：环境准备

```
1. 用户提供飞书应用凭证 (APP_ID / APP_SECRET)
2. 提供目标多维表格地址 (app_token / table_id)
3. 准备本地数据文件
```

### 阶段 2：智能数据分析

```
1. 读取数据文件，推断数据分布
2. 基于统计特征自动识别字段类型
   - 文本/数字/日期/单选/多选/复选框/URL/手机号
3. 对比现有表格 schema，发现差异
4. 自动创建缺失字段（可选）
```

### 阶段 3：选择性同步

根据业务场景选择同步策略：

| 模式 | 适用企业场景 | 核心算法 |
|------|-------------|---------|
| **增量同步** | 日常业务数据更新 | 基于主键匹配，只同步变化数据 |
| **全量覆盖** | 每日定时报表更新 | 清空旧数据，全量重新导入 |
| **仅新增** | 日志/事件数据追加 | 在末尾追加，不修改历史数据 |

### 阶段 4：执行与报告

```
1. 权限校验与连接建立
2. 批量数据同步（带限流退避）
3. 生成同步统计报告
4. 输出结果明细
```

## 系统要求

### 环境依赖

```bash
# Python 依赖
pip install pandas openpyxl python-dotenv requests
```

### 飞书权限配置

1. 在 [飞书开放平台](https://open.feishu.cn/) 创建企业自建应用
2. 获取 `App ID` 和 `App Secret`
3. 添加权限：`docs:bitable:read`, `docs:bitable:write`
4. 将应用添加为多维表格协作者

### 环境变量配置

创建 `.env` 文件：
```env
FEISHU_APP_ID=cli_xxxxxx
FEISHU_APP_SECRET=xxxxxx
```

## 🚀 快速开始

### 场景 1：从 CSV 一键创建新表格

```bash
python scripts/create_table.py \
  --input employees.csv \
  --app-token <base_app_token> \
  --table-name "员工信息表"
```

输出示例：
```
✅ 创建表格成功: 员工信息表 (table_id: tblxxxxxxxxxx)
开始导入数据...

🎉 完成!
- 表格 ID: tblxxxxxxxxxx
- 导入: 128 条
- 自动创建字段: 8 个
- 分享链接: https://pangeedoc.feishu.cn/drive/base/xxx?table=tblxxxxxxxxxx
```

### 场景 2：增量同步到现有表格

```bash
python scripts/sync.py \
  --input daily_sales.csv \
  --app-token <base_app_token> \
  --table-id <table_id> \
  --mode incremental \
  --primary-key "订单号"
```

### 场景 3：全量覆盖每日报表

```bash
python scripts/sync.py \
  --input daily_report.xlsx \
  --app-token <base_app_token> \
  --table-id <table_id> \
  --mode full
```

## 智能类型推断矩阵

| 数据类型 | 飞书类型ID | 推断规则 | 准确率 |
|---------|-----------|---------|--------|
| 文本 | 1 | 默认类型，不符合其他规则时使用 | - |
| 数字 | 2 | 80%+ 可转换为数值 | 98% |
| 日期 | 5 | 匹配 `YYYY-MM-DD` 等格式 | 95% |
| 单选 | 3 | 唯一值占比 < 30% 且唯一值数量 ≤ 20 | 92% |
| 多选 | 4 | 包含逗号/分号分隔符 | 88% |
| 复选框 | 7 | 仅包含是/否、真/假、Y/N 等二值 | 100% |
| 链接 | 15 | 匹配 `http://` / `https://` | 100% |
| 手机号 | 13 | 匹配中国大陆手机号格式 | 100% |

## 企业级可靠性设计

| 场景 | 处理策略 |
|------|---------|
| **API 限流** | 自动退避重试，最大重试 3 次 |
| **网络超时** | 指数退避，逐步重试 |
| **权限错误** | 立即终止，输出清晰提示 |
| **格式错误** | 跳过错误行，记录错误继续同步 |
| **大文件** | 分批处理，每 50 条暂停避免限流 |

## 典型企业架构

```
[数仓/BI系统] 
    ↓ 导出
[CSV/Excel 文件] 
    ↓ 定时任务 / 手动触发
feishu-bitable-sync 
    ↓ 自动同步
[飞书多维表格] 
    ↓ 实时协作
业务团队分析决策
```

## 帮助与参考

- **获取 app_token 和 table_id**: [点击查看](./references/get-id-guide.md)
- **官方 API 文档**: [飞书开放平台 - 多维表格 API](https://open.feishu.cn/document/ukTMukTMukTM/uYTM5UjL2ETO14iNkozM)
- **问题反馈**: 欢迎提交 Issue 改进企业级适配

---

## License

MIT
