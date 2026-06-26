# XI Stock Data Fetcher - Enhanced System
# 羲股票监控系统 - 增强版数据获取

## 📋 核心文件

### 主脚本
- `day.py` - 增强版日线数据获取（支持外部事件）
- `week.py` - 增强版周线数据获取（支持外部事件）
- `month.py` - 增强版月线数据获取（支持外部事件）
- `db_reset.py` - 数据库重置与数据获取工具

### 并行版本（批量处理）
- `day_parallel.py` - 并行日线数据获取
- `week_parallel.py` - 并行周线数据获取
- `month_parallel.py` - 并行月线数据获取

### 基础脚本
- `init_db.py` - 数据库初始化
- `fetch_stocks.py` - 获取股票列表

### 备份文件
- `day_original.py` - 原始日线获取脚本备份
- `week_original.py` - 原始周线获取脚本备份
- `month_original.py` - 原始月线获取脚本备份

## 🚀 快速使用

### 传统用法（获取所有活跃股票）
```bash
python day.py
python week.py
python month.py
```

### 增强用法（支持外部事件）

#### 获取单只股票
```bash
python day.py get 000001
python week.py get 000001
python month.py get 000001
```

#### 获取多只股票（逗号分隔）
```bash
python day.py get 000001,000002
python week.py get 000001,000002
python month.py get 000001,000002
```

#### 获取所有未更新股票
```bash
python day.py get all
python week.py get all
python month.py get all

# 限制数量
python day.py get all --limit 10
```

#### 随机获取股票
```bash
python day.py get rand
python week.py get rand
python month.py get rand

# 指定数量
python day.py get rand --limit 3
```

#### 默认行为（获取5只未更新股票）
```bash
python day.py get
python week.py get
python month.py get
```

### 数据库管理工具

#### 重置功能
```bash
python db_reset.py reset day      # 重置日线时间戳
python db_reset.py reset week     # 重置周线时间戳
python db_reset.py reset month    # 重置月线时间戳
python db_reset.py reset all      # 重置所有时间戳
python db_reset.py reset status   # 查看数据库状态
```

#### 直接获取功能
```bash
# 日线数据获取
python db_reset.py fetch day 000001
python db_reset.py fetch day all --limit 5
python db_reset.py fetch day rand --limit 3

# 周线数据获取
python db_reset.py fetch week 000001
python db_reset.py fetch week all --limit 5

# 月线数据获取
python db_reset.py fetch month 000001
python db_reset.py fetch month all --limit 5
```

## 📊 智能更新逻辑

1. **增量更新**：只获取 `timestamp_field < 当前时间` 的股票
2. **优先级**：从未更新的股票（NULL）优先
3. **随机选择**：`rand` 模式用于分散更新压力
4. **批量处理**：支持逗号分隔的多股票代码
5. **数量限制**：`--limit` 参数控制获取数量

## 🗄️ 数据库字段

### stocks 表结构
| 字段 | 类型 | 说明 |
|------|------|------|
| code | TEXT | 股票代码（主键） |
| name | TEXT | 股票名称 |
| market | TEXT | 市场类型 |
| day_get | TIMESTAMP | 最后日线获取时间 |
| week_get | TIMESTAMP | 最后周线获取时间 |
| month_get | TIMESTAMP | 最后月线获取时间 |
| status | TEXT | 状态（active/inactive） |
| created_at | TIMESTAMP | 创建时间 |

## 📁 数据文件位置

- **日线数据**: `D:\xistock\day\股票名称_股票代码.txt`
- **周线数据**: `D:\xistock\week\股票名称_股票代码.txt`
- **月线数据**: `D:\xistock\month\股票名称_股票代码.txt`

### 文件格式
```
date,open,close,high,low,change_pct
2024-01-01,10.50,10.80,11.00,10.40,2.857
2024-01-02,10.85,10.70,11.10,10.60,-0.926
...
```

## ⚙️ 初始化步骤

1. **初始化数据库**
```bash
python init_db.py
```

2. **获取股票列表**
```bash
python fetch_stocks.py
```

3. **开始数据收集**
```bash
# 传统方式（获取所有股票）
python day.py
python week.py
python month.py

# 或使用增强方式
python day.py get all --limit 10
```

## ⚠️ 注意事项

1. **API限制**：腾讯财经API有速率限制，脚本包含延迟机制
2. **网络连接**：需要稳定的网络连接
3. **磁盘空间**：确保 `D:\xistock` 有足够空间
4. **交易时段**：建议在非交易时段运行
5. **数据完整性**：重置操作会标记所有股票为需要更新

## 🔧 故障排除

### 数据库不存在
```bash
# 运行初始化脚本
python init_db.py
python fetch_stocks.py
```

### 股票代码不存在
```bash
# 检查股票是否在数据库中
python fetch_stocks.py  # 更新股票列表
```

### 网络连接失败
- 检查网络连接
- 脚本会自动重试失败股票
- 可以单独重试失败股票

## 📈 性能建议

1. **批量处理**：使用逗号分隔一次获取多只股票
2. **合理限制**：根据网络情况设置合适的 `--limit` 值
3. **定时任务**：配置Windows任务计划或Linux cron
4. **并行处理**：对于大量股票，使用 `*_parallel.py` 脚本

---

**版本**: 2.0.0 (增强版)  
**最后更新**: 2026-03-14  
**功能**: 支持外部事件控制、智能更新、批量处理