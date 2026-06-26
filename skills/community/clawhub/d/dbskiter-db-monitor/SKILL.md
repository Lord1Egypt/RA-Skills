---
name: db-monitor
description: |
  数据库健康监控，支持健康检查、异常检测、容量预测、高级容量预测、趋势分析、基线对比。

  智能数据源选择：
  - Oracle 数据库自动使用 Zabbix 监控
  - MySQL 数据库优先使用直连，其次使用 Prometheus
  - 支持 Z 系列资产组（如 Z18, Z5）自动识别

  使用场景：
  - 用户说"检查健康" -> 执行 health
  - 用户说"有异常吗" -> 执行 anomalies
  - 用户说"容量够吗" -> 执行 capacity
  - 用户说"采集指标" -> 执行 collect
  - 用户说"看历史" -> 执行 history
  - 用户说"高级容量预测" -> 执行 capacity-advanced
  - 用户说"趋势分析" -> 执行 trend
  - 用户说"基线对比" -> 执行 compare

  用法：
  - dbskiter --output-mode=ai --database=<name> monitor health
  - dbskiter --output-mode=ai --database=<name> monitor anomalies
  - dbskiter --output-mode=ai --database=<name> monitor capacity --resource=disk
  - dbskiter --output-mode=ai --database=<name> monitor collect
  - dbskiter --output-mode=ai --database=<name> monitor history <metric>
  - dbskiter --output-mode=ai --database=<name> monitor capacity-advanced --resource=disk
  - dbskiter --output-mode=ai --database=<name> monitor trend --metric=cpu_usage
  - dbskiter --output-mode=ai --database=<name> monitor compare --metric=qps --value=1250 --baseline=2026-04-01
---

# 数据库监控 Skill

## 智能数据源选择

系统会根据 `--database` 参数自动选择最优数据源：

| 数据库类型 | 识别规则 | 数据源优先级 |
|-----------|---------|-------------|
| Oracle | Z 系列资产组（Z18, Z5等）或 KF 系列 | Zabbix |
| MySQL | 其他名称 | 直连数据库 > Prometheus |

**示例**：**示例**:
```bash
# Oracle 数据库（自动使用 Zabbix）
dbskiter --output-mode=ai --database=Z18 monitor health
dbskiter --output-mode=ai --database=Z5 monitor capacity --resource=disk

# MySQL 数据库（优先直连，其次 Prometheus）
dbskiter --output-mode=ai --database=jump monitor health
dbskiter --output-mode=ai --database=prod monitor anomalies
```

## 何时使用

当用户提到以下关键词时，使用此skill：

| 用户说法 | 执行命令 | 说明 |
|---------|---------|------|
| "检查健康" | `dbskiter --output-mode=ai --database=<name> monitor health` | 整体健康评分 |
| "有异常吗" | `dbskiter --output-mode=ai --database=<name> monitor anomalies` | 检测异常指标 |
| "容量够吗" | `dbskiter --output-mode=ai --database=<name> monitor capacity` | 容量预测 |
| "采集数据" | `dbskiter --output-mode=ai --database=<name> monitor collect` | 采集当前指标 |
| "看历史" | `dbskiter --output-mode=ai --database=<name> monitor history <指标>` | 查看指标历史 |
| "高级容量预测" | `dbskiter --output-mode=ai --database=<name> monitor capacity-advanced` | 多算法容量预测 |
| "趋势分析" | `dbskiter --output-mode=ai --database=<name> monitor trend` | 指标趋势分析 |
| "基线对比" | `dbskiter --output-mode=ai --database=<name> monitor compare` | 与历史基线对比 |

## 核心命令（8个）

### 高级功能（新增）

#### 6. 高级容量预测
```bash
dbskiter --output-mode=ai --database=<数据库名> monitor capacity-advanced --resource=disk
```
**特点**：
- 自动选择最佳预测算法（线性回归、移动平均、指数平滑、多项式拟合）
- 提供置信度评估
- 更精确的预测结果

**输出**：
```json
{
  "algorithm": "linear_regression",
  "confidence": 0.85,
  "predictions": {
    "7d": 68.5,
    "30d": 75.2,
    "90d": 88.5
  },
  "days_to_threshold": 45,
  "recommendation": "建议在45天内扩容"
}
```

#### 7. 趋势分析
```bash
dbskiter --output-mode=ai --database=<数据库名> monitor trend --metric=cpu_usage --days=7
```
**适用场景**：
- 分析指标变化趋势
- 对比当前值与历史平均值
- 判断性能是改善还是恶化

**输出**：
```json
{
  "trend_direction": "degrading",
  "current_value": 75.5,
  "historical_avg": 65.2,
  "change_percent": 15.8,
  "recommendation": "CPU使用率呈恶化趋势，建议关注"
}
```

#### 8. 基线对比
```bash
dbskiter --output-mode=ai --database=<数据库名> monitor compare --metric=qps --value=1250 --baseline=2026-04-01
```
**适用场景**：
- 对比当前性能与历史基线
- 评估优化效果
- 检测性能退化

**输出**：
```json
{
  "current_value": 1250,
  "baseline_value": 1000,
  "change_percent": 25.0,
  "severity": "normal",
  "message": "QPS较基线上升25.0%，在正常范围内"
}
```

#### 9. 性能退化检测
```bash
dbskiter --output-mode=ai --database=<数据库名> monitor degradation
```
**适用场景**：
- 自动检测所有性能退化指标
- 与db-diagnose性能快照集成

**输出**：
```json
{
  "degradation_count": 2,
  "degradations": [
    {
      "metric_type": "cpu_usage",
      "change_percent": 30.5,
      "severity": "warning"
    }
  ]
}
```

### 1. 健康检查
```bash
dbskiter --database=<数据库名> monitor health
```
**输出**：总体评分、各组件状态、关键指标

**评分标准**：
- 90-100：优秀 [OK]
- 70-89：良好 [WARN]
- <70：需要关注 [CRITICAL]

### 2. 异常检测
```bash
dbskiter --database=<数据库名> monitor anomalies
```
**默认行为**：检测所有指标的异常

**输出**：异常列表、严重程度、建议

### 3. 容量预测
```bash
dbskiter --database=<数据库名> monitor capacity --resource=disk
```
**可选资源**：
- `disk`：磁盘空间
- `memory`：内存使用
- `connections`：连接数

**输出**：当前使用率、预测值、剩余天数、风险等级

### 4. 采集指标
```bash
dbskiter --database=<数据库名> monitor collect
```
**默认行为**：采集所有核心指标

**可选参数**：
- `--metrics=qps,connections`：只采集指定指标

### 5. 查看历史
```bash
dbskiter --database=<数据库名> monitor history connections_active --hours=24
```
**输出**：历史指标数据、趋势图表

## AI决策流程

### 场景1：用户说"检查数据库健康"

```
步骤1：执行 dbskiter --database=<name> monitor health
步骤2：解读健康评分和状态
步骤3：如果有问题，执行 dbskiter --database=<name> monitor anomalies
步骤4：总结给用户
```

### 场景2：用户说"磁盘还够用吗"

```
步骤1：执行 dbskiter --database=<name> monitor capacity --resource=disk
步骤2：解读当前使用率和预测
步骤3：如果接近阈值，给出扩容建议
```

### 场景3：用户说"看看有没有异常"

```
步骤1：执行 dbskiter --database=<name> monitor anomalies
步骤2：列出发现的异常
步骤3：对严重异常，建议进一步诊断
```
