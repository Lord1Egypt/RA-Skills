# 锦衣卫使用指南

## 概述

锦衣卫是大明核心系统的**独立监察系统**，负责巡查系统运行状态、记录关键事件、发出安全预警。锦衣卫独立于三省六部，直接向皇上汇报。

## 核心功能

### 1. 系统巡查
- 定期巡查三省六部运行状态
- 检查系统资源使用情况
- 监控任务执行进度

### 2. 安全监控
- 检测异常操作
- 监控安全事件
- 预警潜在威胁

### 3. 日志记录
- 记录所有关键操作
- 保存巡查报告
- 维护安全日志

### 4. 预警通知
- 实时预警异常情况
- 分级告警机制
- 多渠道通知

## 使用方式

### 命令行使用

```bash
# 启动锦衣卫巡查
python3 -m skill1.jinyiwei.main patrol

# 查看系统状态
python3 -m skill1.jinyiwei.main status

# 查看安全日志
python3 -m skill1.jinyiwei.main logs --limit 10

# 手动触发巡查
python3 -m skill1.jinyiwei.main manual-patrol
```

### Python API使用

```python
from skill1.jinyiwei.main import create_jinyiwei, patrol_system, get_system_status

# 创建锦衣卫实例
jinyiwei = create_jinyiwei()

# 执行系统巡查
report = patrol_system()
print(f"巡查ID: {report['patrol_id']}")
print(f"巡查结果: {report['overall_status']}")

# 获取系统状态
status = get_system_status()
print(f"系统状态: {status['system_status']}")
print(f"活跃告警: {len(status['active_alerts'])}个")
```

### 集成到其他模块

```python
from skill1.jinyiwei.main import create_jinyiwei

class YourService:
    def __init__(self):
        self.jinyiwei = create_jinyiwei()
    
    def critical_operation(self):
        # 在执行关键操作前记录
        self.jinyiwei.record_event(
            event_type="operation_start",
            severity="info",
            message="开始执行关键操作",
            context={"operation": "critical_operation"}
        )
        
        try:
            # 执行操作
            result = self._do_operation()
            
            # 记录成功
            self.jinyiwei.record_event(
                event_type="operation_success",
                severity="info",
                message="关键操作执行成功",
                context={"result": result}
            )
            
            return result
        except Exception as e:
            # 记录失败
            self.jinyiwei.record_event(
                event_type="operation_failed",
                severity="error",
                message="关键操作执行失败",
                context={"error": str(e)}
            )
            raise
```

## 配置说明

### 告警阈值配置

锦衣卫的告警阈值可以在初始化时配置：

```python
jinyiwei = JinYiWei(
    alert_thresholds={
        "task_count": 50,           # 最大活跃任务数
        "token_usage_rate": 0.8,    # Token使用率阈值
        "failed_audits": 3,         # 连续失败审核数
        "execution_timeout": 3600   # 执行超时时间（秒）
    }
)
```

### 巡查间隔配置

默认巡查间隔为300秒（5分钟），可以通过环境变量修改：

```bash
export JINYIWEI_PATROL_INTERVAL=60  # 改为60秒
```

## 巡查报告格式

### 巡查报告结构

```json
{
  "patrol_id": "PATROL-20260325-0001",
  "patrol_started": "2026-03-25T10:00:00",
  "patrol_areas": ["三省状态", "六部运行"],
  "findings": [
    {
      "area": "三省状态",
      "status": "normal",
      "details": "中书省、门下省、尚书省运行正常"
    }
  ],
  "alerts": [],
  "recommendations": [],
  "overall_status": "normal"
}
```

### 告警级别

1. **info**：信息级别，仅记录不告警
2. **warning**：警告级别，需要关注但无需立即处理
3. **error**：错误级别，需要立即处理
4. **critical**：严重级别，系统可能崩溃

## 安全事件记录

### 事件类型

锦衣卫记录以下类型的安全事件：

1. **system_startup**：系统启动
2. **system_shutdown**：系统关闭
3. **task_created**：任务创建
4. **task_completed**：任务完成
5. **task_failed**：任务失败
6. **audit_passed**：审核通过
7. **audit_failed**：审核失败
8. **security_alert**：安全告警
9. **resource_warning**：资源警告
10. **performance_issue**：性能问题

### 事件格式

```json
{
  "event_id": "EVENT-20260325-0001",
  "event_type": "security_alert",
  "severity": "warning",
  "timestamp": "2026-03-25T10:00:00",
  "message": "Token使用率超过80%",
  "context": {
    "token_usage_rate": 0.85,
    "threshold": 0.8
  },
  "source": "锦衣卫巡查",
  "recommended_action": "检查Token分配或增加预算"
}
```

## 预警机制

### 预警触发条件

1. **Token使用率 > 80%**：资源即将耗尽
2. **活跃任务数 > 50**：系统负载过高
3. **连续审核失败 > 3次**：审核流程异常
4. **任务执行超时 > 1小时**：执行卡住
5. **系统错误率 > 10%**：系统不稳定

### 预警通知方式

1. **控制台输出**：实时显示在控制台
2. **日志文件**：记录到安全日志
3. **API回调**：调用预设的回调URL
4. **消息推送**：推送到消息队列

## 日志管理

### 日志文件位置

- **巡查日志**：`{{PROJECT_ROOT}}/logs/patrol_logs.json`
- **安全日志**：`{{PROJECT_ROOT}}/logs/security_logs.json`
- **事件日志**：`{{PROJECT_ROOT}}/logs/event_logs.json`

### 日志轮转策略

- 每个日志文件最大10MB
- 保留最近5个备份文件
- 每天自动清理30天前的日志

## 故障排除

### 常见问题

#### 问题1：锦衣卫无法启动
**可能原因**：依赖模块缺失
**解决方案**：
```bash
pip install -r requirements.txt
```

#### 问题2：巡查报告为空
**可能原因**：系统未正常运行
**解决方案**：
```bash
# 检查三省六部服务状态
python3 -m skill1.zhongshu.main status
python3 -m skill1.menxia.main status
python3 -m skill1.shangshu.main status
```

#### 问题3：告警未触发
**可能原因**：阈值配置过高
**解决方案**：
```python
# 调整告警阈值
jinyiwei = JinYiWei(
    alert_thresholds={
        "task_count": 30,           # 降低阈值
        "token_usage_rate": 0.7,    # 降低阈值
        "failed_audits": 2,         # 降低阈值
        "execution_timeout": 1800   # 降低阈值
    }
)
```

### 调试模式

启用调试模式获取详细日志：

```bash
export JINYIWEI_DEBUG=true
python3 -m skill1.jinyiwei.main patrol
```

## 最佳实践

### 1. 定期巡查
- 建议巡查间隔：60-300秒
- 高峰期缩短间隔
- 低峰期延长间隔

### 2. 分级告警
- 不同级别不同处理方式
- 严重告警立即处理
- 轻微告警定期汇总

### 3. 日志分析
- 定期分析安全日志
- 发现异常模式
- 优化告警规则

### 4. 性能优化
- 避免频繁的磁盘IO
- 使用缓存减少重复计算
- 异步处理非关键操作

## 扩展开发

### 添加新的巡查项

```python
from skill1.jinyiwei.main import JinYiWei

class CustomJinYiWei(JinYiWei):
    def _patrol_custom_area(self, patrol_report: Dict):
        """巡查自定义区域"""
        # 实现自定义巡查逻辑
        custom_finding = {
            "area": "自定义区域",
            "status": "normal",
            "details": "自定义巡查结果",
            "metrics": {"custom_metric": 42}
        }
        
        patrol_report["findings"].append(custom_finding)
        
        # 添加自定义告警
        if custom_metric > 50:
            patrol_report["alerts"].append({
                "area": "自定义区域",
                "level": "warning",
                "message": "自定义指标超过阈值",
                "details": {"custom_metric": custom_metric}
            })
```

### 集成外部监控系统

```python
from skill1.jinyiwei.main import create_jinyiwei
import requests

jinyiwei = create_jinyiwei()

# 添加外部监控回调
def external_monitor_callback(report):
    """发送巡查报告到外部监控系统"""
    response = requests.post(
        "https://external-monitor.com/api/reports",
        json=report,
        timeout=10
    )
    return response.status_code == 200

# 注册回调
jinyiwei.add_callback(external_monitor_callback)
```

## 安全注意事项

### 1. 权限控制
- 锦衣卫需要适当的系统权限
- 避免过度权限
- 定期审计权限使用

### 2. 数据保护
- 敏感信息脱敏
- 日志文件加密
- 访问控制

### 3. 防滥用
- 限制巡查频率
- 验证巡查请求
- 监控锦衣卫自身

---

**文档版本**：1.0.0  
**最后更新**：2026-03-25  
**维护者**：大明核心系统锦衣卫组