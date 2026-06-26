# DataWorks 每日任务监控技能

## 功能
每日统计 DataWorks 任务运行情况，成功/失败汇总，失败任务告警

## 触发词
- "检查 DataWorks 任务状态"
- "昨天 DataWorks 任务运行情况"
- "DataWorks 失败任务有哪些"
- "dataworks 监控"
- "任务运行日报"

## 执行流程

### 1. 读取配置
从环境变量读取：
- `ALIYUN_ACCESS_KEY_ID`
- `ALIYUN_ACCESS_KEY_SECRET`
- `DATAWORKS_PROJECT_ID`
- `DATAWORKS_REGION_ID` (默认：cn-shanghai)

### 2. 计算时间范围
获取昨天的时间范围：
- Start: 昨天 00:00:00
- End: 昨天 23:59:59

### 3. 调用 DataWorks API
```python
ListDagInstances(
  ProjectId=PROJECT_ID,
  StartTime=start_time,
  EndTime=end_time
)
```

### 4. 统计任务状态

**状态分类：**
- ✅ 成功 (SUCCESS, SUCCEEDED)
- ❌ 失败 (FAILED, FAILURE)
- ⏳ 运行中 (RUNNING, PENDING)
- ❄️ 冻结/暂停 (FROZEN, FREEZED) - **不计入失败**
- ⏭️ 未运行 (NOT_RUN, SKIP, SKIPPED) - **不计入失败**
- 📊 其他

**统计逻辑：**
- 实际运行数 = 成功 + 失败 + 运行中
- 冻结/暂停/未运行的任务单独统计，不算失败

### 5. 生成报告
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

详情：https://dataworks.console.aliyun.com/...
```

### 6. 发送报告
通过飞书发送给用户

### 7. 失败告警
如果有失败任务，@用户告警

## API 配置

**环境变量：**
```bash
export ALIYUN_ACCESS_KEY_ID="your_access_key_id"
export ALIYUN_ACCESS_KEY_SECRET="your_access_key_secret"
export DATAWORKS_PROJECT_ID="your_project_id"
export DATAWORKS_REGION_ID="cn-shanghai"
```

## 核心 API

| API | 功能 |
|-----|------|
| `ListDagInstances` | 获取指定日期的任务实例列表 |
| `GetInstanceStatus` | 查询任务实例状态 |

## 报告格式

```
📊 DataWorks 任务日报 (YYYY-MM-DD)

✅ 成功：X 个
❌ 失败：X 个
⏳ 运行中：X 个
📋 总计：X 个

❌ 失败任务：
1. 任务名 - 错误信息
2. ...

详情链接：[DataWorks 控制台]
```

## 定时任务

**时间：** 每天上午 9:00 自动执行

**触发词：** `dataworks-daily-check`

## 注意事项

1. **权限要求** - 需要有 DataWorks API 访问权限
2. **配置安全** - AccessKey 不要泄露
3. **失败告警** - 有失败任务时立即告警
4. **报告保存** - 可选保存到文件
