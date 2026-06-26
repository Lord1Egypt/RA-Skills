# DataWorks 每日任务监控技能

## 🎯 功能说明

每日自动统计 DataWorks 任务运行情况，包括：
- 成功/失败/运行中任务数量
- 失败任务详细列表
- 失败原因分析
- 飞书报告发送
- 失败告警

---

## 📝 使用方法

### 方式 1：手动触发

**你说：**
```
检查 DataWorks 任务状态
```
或
```
昨天 DataWorks 任务运行情况
```

**我会：**
1. 调用 DataWorks API
2. 统计分析
3. 生成报告
4. 发送飞书

---

### 方式 2：自动执行

**定时：** 每天早上 9:00 自动执行

**内容：** 统计前一天的任务运行情况

---

## 🔧 配置说明

### 环境变量

需要配置以下环境变量：

```bash
# 阿里云 AccessKey
export ALIYUN_ACCESS_KEY_ID="LTAI5tXXXXXXXXXXXX"
export ALIYUN_ACCESS_KEY_SECRET="XXXXXXXXXXXXXXXXXXXX"

# DataWorks 项目配置
export DATAWORKS_PROJECT_ID="XXXXXX"
export DATAWORKS_REGION_ID="cn-shanghai"  # 可选，默认 cn-shanghai
```

---

### 配置位置

**推荐方式：** 在 Gateway 配置文件中设置

```bash
# 编辑 ~/.openclaw/openclaw.json
# 或添加到 ~/.bashrc
```

---

## 📊 报告格式

### 示例输出

```
📊 DataWorks 任务日报 (2026-02-26)

✅ 成功：158 个
❌ 失败：3 个
⏳ 运行中：0 个
📋 总计：161 个

❌ 失败任务：
1. ods_user_info_df - 数据源连接超时
2. dwd_order_detail_di - 字段类型不匹配
3. ads_daily_report_di - 内存不足

🔗 详情：https://dataworks.console.aliyun.com/...
```

---

### 字段说明

| 字段 | 说明 |
|------|------|
| **成功** | 状态为 SUCCESS/SUCCEEDED 的任务 |
| **失败** | 状态为 FAILED/FAILURE 的任务 |
| **运行中** | 状态为 RUNNING/PENDING 的任务 |
| **总计** | 所有任务实例总数 |

---

## 🔍 任务状态映射

| DataWorks 状态 | 统计分类 |
|---------------|---------|
| SUCCESS | ✅ 成功 |
| SUCCEEDED | ✅ 成功 |
| FAILED | ❌ 失败 |
| FAILURE | ❌ 失败 |
| RUNNING | ⏳ 运行中 |
| PENDING | ⏳ 运行中 |
| 其他 | 其他 |

---

## 📋 执行流程

```
1. 读取配置
   - AccessKey
   - ProjectId
   - RegionId
       ↓
2. 计算时间范围
   - 昨天 00:00:00
   - 昨天 23:59:59
       ↓
3. 调用 API
   - ListDagInstances
       ↓
4. 统计分析
   - 成功/失败/运行中
   - 失败任务详情
       ↓
5. 生成报告
   - 格式化文本
   - 添加详情链接
       ↓
6. 发送报告
   - 飞书发送
       ↓
7. 失败告警
   - 如有失败任务，@用户
```

---

## 🛠️ API 说明

### ListDagInstances

**功能：** 查询 DAG 实例列表

**参数：**
```json
{
  "ProjectId": "项目 ID",
  "StartTime": "2026-02-26T00:00:00Z",
  "EndTime": "2026-02-26T23:59:59Z",
  "PageNumber": 1,
  "PageSize": 100
}
```

**返回：**
```json
{
  "Data": {
    "Instances": [
      {
        "InstanceId": "xxx",
        "TaskName": "ods_user_info_df",
        "Status": "SUCCESS",
        "ErrorMessage": "",
        "Owner": "user@company.com"
      }
    ]
  }
}
```

---

### GetInstanceStatus

**功能：** 查询单个实例状态

**参数：**
```json
{
  "ProjectId": "项目 ID",
  "InstanceId": "实例 ID"
}
```

---

## ⚠️ 注意事项

### 权限要求

1. ✅ **DataWorks API 访问权限**
2. ✅ **项目读取权限**
3. ✅ **实例查询权限**

---

### 配置安全

1. 🔒 **AccessKey 保密** - 不要提交到代码库
2. 🔒 **使用 RAM 子账号** - 不要使用主账号
3. 🔒 **最小权限原则** - 只授予必要权限

---

### 错误处理

**常见问题：**

| 错误 | 原因 | 解决 |
|------|------|------|
| `Access Denied` | 权限不足 | 检查 RAM 权限 |
| `Invalid Parameter` | 参数错误 | 检查 ProjectId |
| `Service Unavailable` | API 限流 | 稍后重试 |

---

## 📅 定时任务

### 默认配置

**时间：** 每天早上 9:00  
**内容：** 前一天的任务统计  
**发送：** 飞书私信

### 自定义时间

如需修改执行时间，告诉我即可。

---

## 🎯 使用示例

### 示例 1：手动检查

**你说：**
```
检查昨天 DataWorks 任务
```

**我执行：**
1. 查询昨天所有任务实例
2. 统计成功/失败数量
3. 列出失败任务
4. 发送报告

**返回：**
```
📊 DataWorks 任务日报 (2026-02-27)

✅ 成功：156 个
❌ 失败：2 个
⏳ 运行中：0 个
📋 总计：158 个

❌ 失败任务：
1. ods_order_info_df - 数据源连接失败
2. dwd_user_detail_di - SQL 语法错误

🔗 详情：https://dataworks.console.aliyun.com/...
```

---

### 示例 2：查看失败任务

**你说：**
```
DataWorks 失败任务有哪些
```

**我执行：**
- 筛选失败任务
- 显示错误信息
- 提供解决建议

---

## 📚 相关技能

| 技能 | 功能 |
|------|------|
| `th-dataworks-auth` | 查询用户权限 |
| `th-dataworks-add-analyst-role` | 添加分析师角色 |
| `etl-generator` | ETL 流程生成 |

---

## 💡 最佳实践

### 日常监控

1. ✅ 每天查看日报
2. ✅ 及时处理失败任务
3. ✅ 关注趋势变化

### 故障排查

1. 🔍 查看错误日志
2. 🔍 检查数据源
3. 🔍 验证 SQL 语法
4. 🔍 确认资源充足

### 性能优化

1. ⚡ 优化慢 SQL
2. ⚡ 合理设置并发
3. ⚡ 使用增量处理

---

## 🔗 参考文档

- [DataWorks API 文档](https://help.aliyun.com/document_detail/138726.html)
- [ListDagInstances API](https://help.aliyun.com/document_detail/138730.html)
- [DataWorks 监控最佳实践](https://help.aliyun.com/document_detail/144230.html)

---

**技能已就绪，随时可以监控任务！** 📊🔧
