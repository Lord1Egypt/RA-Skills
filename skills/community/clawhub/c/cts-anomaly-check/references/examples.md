# CTS 异常检查使用示例

## 基本用法

### 1. 检查最近24小时的异常

```bash
python3 scripts/check_cts_anomaly.py \
  --region=cn-north-4 \
  --project-id=05a890974a00269c2fd0c01d4ca90eea
```

### 2. 检查最近1小时的异常

```bash
python3 scripts/check_cts_anomaly.py \
  --region=cn-north-4 \
  --project-id=05a890974a00269c2fd0c01d4ca90eea \
  --hours=1
```

### 3. 输出JSON格式

```bash
python3 scripts/check_cts_anomaly.py \
  --region=cn-north-4 \
  --project-id=05a890974a00269c2fd0c01d4ca90eea \
  --output=json
```

### 4. 增加查询记录数

```bash
python3 scripts/check_cts_anomaly.py \
  --region=cn-north-4 \
  --project-id=05a890974a00269c2fd0c01d4ca90eea \
  --limit=500
```

## 在技能中使用

### 快速检查

直接调用脚本：

```bash
python3 /path/to/check_cts_anomaly.py \
  --region=cn-north-4 \
  --project-id=05a890974a00269c2fd0c01d4ca90eea
```

### 定期检查（通过cron）

```bash
# 每小时检查一次
0 * * * * python3 /path/to/check_cts_anomaly.py --region=cn-north-4 --project-id=xxx >> /var/log/cts-check.log 2>&1
```

### 与告警集成

```bash
# 检查并发送告警
RESULT=$(python3 scripts/check_cts_anomaly.py --region=cn-north-4 --project-id=xxx --output=json)
INCIDENT_COUNT=$(echo $RESULT | jq '.analysis.by_rating.incident')

if [ "$INCIDENT_COUNT" -gt 0 ]; then
  # 发送告警
  echo "发现 $INCIDENT_COUNT 条事故记录，请立即检查！" | mail -s "CTS异常告警" admin@example.com
fi
```

## 输出解读

### 正常输出示例

```
============================================================
CTS 异常检查报告
============================================================
检查时间: 2026-06-09 13:30:00
时间范围: 最近 24 小时

追踪器 [system]: ✅ 已启用

异常统计:
- 正常记录: 150 条
- 警告记录: 3 条
- 事故记录: 0 条
- 失败操作: 2 条

服务分布:
  - ECS: 80 条
  - IAM: 45 条
  - VPC: 25 条

用户分布:
  - user1: 100 条
  - user2: 50 条

建议措施:
- 检查警告级别记录，确认是否有配置问题
- 分析失败操作原因，检查权限配置

============================================================
```

### 发现异常的输出示例

```
============================================================
CTS 异常检查报告
============================================================
检查时间: 2026-06-09 13:30:00
时间范围: 最近 24 小时

追踪器 [system]: ✅ 已启用

异常统计:
- 正常记录: 145 条
- 警告记录: 5 条
- 事故记录: 2 条
- 失败操作: 3 条

⚠️  敏感操作 (8 条):
  - [2026-06-09 10:15:23] user1 - deleteUser (normal)
  - [2026-06-09 11:20:45] admin - attachRoleToUser (normal)
  - [2026-06-09 12:05:12] user2 - createAccessKey (warning)
  ...

🗑️  删除操作 (3 条):
  - [2026-06-09 10:15:23] user1 - deleteInstance - ecs-server-001
  - [2026-06-09 11:30:00] admin - deleteSecurityGroupRule - rule-xxx
  ...

❌ 失败操作 (3 条):
  - [2026-06-09 09:45:12] user3 - createInstance (code: 403)
  - [2026-06-09 10:20:33] user2 - attachRole (code: 401)
  ...

建议措施:
- 检查警告级别记录，确认是否有配置问题
- ⚠️  立即检查事故级别记录，可能存在安全风险
- 分析失败操作原因，检查权限配置
- 审查敏感操作，确认是否有未授权操作
- 确认删除操作是否为预期操作

============================================================
```

## 常见场景

### 场景1：日常安全巡检

每天检查一次，关注：
- 事故级别记录
- 失败操作
- 敏感操作

### 场景2：权限变更审计

检查IAM相关操作：
- 用户创建/删除
- 角色授权
- 权限策略变更

### 场景3：故障排查

检查失败操作：
- 403错误：权限不足
- 401错误：认证失败
- 404错误：资源不存在

### 场景4：合规检查

定期审计：
- 删除操作记录
- 敏感服务访问
- 异常登录行为

## 集成建议

### 1. 与监控系统集成

将脚本输出接入：
- Prometheus
- Grafana
- ELK Stack

### 2. 与告警系统集成

异常时发送告警：
- 邮件通知
- 短信通知
- 企业微信/钉钉

### 3. 与SIEM系统集成

将CTS记录导入：
- Splunk
- QRadar
- ArcSight

### 4. 与自动化运维集成

异常时自动处理：
- 自动回滚
- 自动通知
- 自动阻断

## 性能优化

### 大量记录时的优化

1. **缩小时间范围**
   ```bash
   --hours=1  # 只查询最近1小时
   ```

2. **限制记录数**
   ```bash
   --limit=100  # 只查询100条
   ```

3. **添加过滤条件**
   - 按服务过滤
   - 按用户过滤
   - 按资源过滤

### 定期检查优化

1. **增量检查**
   - 记录上次检查时间
   - 只查询新增记录

2. **分区检查**
   - 按服务分区
   - 并行查询

3. **缓存优化**
   - 缓存追踪器状态
   - 缓存用户信息
