# 需求管理 - 使用示例 (v1.0.1)

## 示例1: 首次使用（自动创建）

### 用户输入
"帮我建立需求管理系统"

### AI执行
```json
// Step 1: 检查记忆文件
// 文件不存在，继续创建

// Step 2: 创建多维表格
feishu_bitable_app.create({ "name": "需求管理" })
// 返回: { app_token: "xxx", ... }

// Step 3: 创建项目列表
feishu_bitable_app_table.create({
  "app_token": "返回的app_token",
  "table": {
    "name": "项目列表",
    "fields": [...]
  }
})
// 返回: { table_id: "tblxxx1", ... }

// Step 4: 创建需求列表
feishu_bitable_app_table.create({
  "app_token": "返回的app_token",
  "table": { "name": "需求列表", ... }
})
// 返回: { table_id: "tblxxx2", ... }

// Step 5: 创建任务列表
feishu_bitable_app_table.create({
  "app_token": "返回的app_token",
  "table": { "name": "任务列表", ... }
})
// 返回: { table_id: "tblxxx3", ... }

// Step 6: 保存到记忆文件
memory/shared/requirement-manager.json
{
  "app_token": "xxx",
  "tables": {
    "project": {"table_id": "tblxxx1"},
    "requirement": {"table_id": "tblxxx2"},
    "task": {"table_id": "tblxxx3"}
  }
}
```

---

## 示例2: 非首次使用（读取记忆）

### 用户输入
"查看当前需求"

### AI执行
```json
// Step 1: 读取记忆文件
memory/shared/requirement-manager.json
// 获取: app_token, table_id

// Step 2: 查询需求列表
feishu_bitable_app_table_record.list({
  "app_token": "记忆中的app_token",
  "table_id": "记忆中的requirement table_id"
})

// Step 3: 展示结果
```

---

## 示例3: 创建需求

### 用户输入
"创建需求：开发一个投资分析工具，优先级P1，截止3月底"

### AI执行
```json
// Step 1: 读取记忆获取 app_token 和 table_id
memory/shared/requirement-manager.json

// Step 2: 创建需求
feishu_bitable_app_table_record.create({
  "app_token": "xxx",
  "table_id": "tblUGPrZCNd2BgYy",
  "fields": {
    "需求标题": "开发一个投资分析工具",
    "状态": "待处理",
    "优先级": "P1 - 重要",
    "截止日期": 1776124800000,  // 2026-03-31
    "需求类型": "产品",
    "提出日期": 1774243200000   // 2026-03-22
  }
})
```

---

## 示例4: 查看需求进度

### 用户输入
"查看当前需求进度"

### AI执行
```json
// Step 1: 读取记忆
memory/shared/requirement-manager.json

// Step 2: 查询进行中的需求
feishu_bitable_app_table_record.list({
  "app_token": "xxx",
  "table_id": "需求列表table_id",
  "filter": {
    "conjunction": "and",
    "conditions": [
      {"field_name": "状态", "operator": "isNot", "value": ["已完成"]}
    ]
  }
})

// Step 3: 查询关联任务
feishu_bitable_app_table_record.list({
  "app_token": "xxx",
  "table_id": "任务列表table_id"
})

// Step 4: 展示
```

### 输出示例
```
📊 当前进行中的需求：

| 需求 | 状态 | 进度 | 优先级 |
|------|------|------|--------|
| 开发修仙游戏 | 进行中 | 100% | P0 |
| AI趋势报告 | 已完成 | 100% | P1 |
| 定投分析 | 已完成 | 100% | P1 |
```

---

## 示例5: 更新任务状态

### 用户输入
"标记任务'撰写报告'为已完成"

### AI执行
```json
// Step 1: 读取记忆
memory/shared/requirement-manager.json

// Step 2: 先查询找到任务ID
feishu_bitable_app_table_record.list({
  "app_token": "xxx",
  "table_id": "任务列表table_id",
  "filter": {
    "conjunction": "and",
    "conditions": [
      {"field_name": "任务标题", "operator": "contains", "value": ["撰写报告"]}
    ]
  }
})

// Step 3: 更新状态
feishu_bitable_app_table_record.update({
  "app_token": "xxx",
  "table_id": "任务列表table_id",
  "record_id": "查询到的record_id",
  "fields": {
    "任务状态": "已完成"
  }
})
```
