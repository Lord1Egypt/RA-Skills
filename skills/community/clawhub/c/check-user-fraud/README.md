# 用户刷单系统性分析工具文档

## 概述

本工具提供一站式用户刷单分析，整合多个数据源，系统性识别刷单行为。

## 功能模块

### 1. 基础信息查询 (`query_user_detail.py`)
查询用户注册信息、实名认证、会员等级、邀请关系等。

```bash
python3 query_user_detail.py <userId>
```

**输出字段：**
- 用户ID、手机号、支付宝账号
- 真实姓名、身份证号（脱敏）
- 注册时间、邀请码
- 上级ID、徒弟状态、系统备注
- 会员等级、会员类型、过期时间

### 2. 登录记录分析 (`query_user_login_logs.py`)
分析用户登录IP、设备、地理位置分布。

```bash
python3 query_user_login_logs.py <userId>
```

**输出字段：**
- 登录时间、IP地址
- 地理位置（省份+城市）
- 设备ID、应用版本
- 登录方式、渠道

### 3. APP访问记录分析 (`query_user_visit_logs.py`)
查询用户APP访问历史，用于发现设备共用、IP关联等。

```bash
python3 query_user_visit_logs.py <userId>
```

**输出字段：**
- 访问时间、IP地址
- 设备ID、手机品牌
- 应用版本、渠道

### 4. 刷单行为分析 (`check_fraud.py` / `check_fraud_enhanced.py`)
核心刷单检测脚本，分析用户做单记录。

```bash
python3 check_fraud.py <userId>
python3 check_fraud_enhanced.py <userId>  # 增强版，包含发单人账单分析
```

**分析维度：**
- 完成时间分析（是否过快）
- 发单人集中度
- 任务重复度
- 置顶刷新状态
- 发单人账单分析（增强版）

### 5. 任务做单人分析 (`analyze_task_completers.py`)
分析特定任务的所有做单人，识别批量注册模式。

```bash
python3 analyze_task_completers.py <taskNo>
```

**分析维度：**
- 注册时间分布
- 推荐人集中度
- 新用户占比

### 6. 用户任务分析 (`analyze_user_tasks_completers.py`)
分析用户所做任务的做单人分布。

```bash
python3 analyze_user_tasks_completers.py <userId>
```

**输出：**
- 每个任务的做单人统计
- 新用户占比
- 风险等级评估

### 7. 发单记录分析 (`analyze_user_publisher_tasks.py`)
分析用户作为发单人的任务及接单人分布。

```bash
python3 analyze_user_publisher_tasks.py <userId>
```

**输出：**
- 发单任务列表
- 每个任务的接单人分析
- 新用户占比

### 8. 任务操作记录分析 (`query_user_task_ops.py`)
查询用户任务操作历史（上架、下架、置顶等）。

```bash
python3 query_user_task_ops.py <userId>
```

**输出：**
- 操作类型统计
- 操作时间线
- IP和设备信息

### 9. IP关联用户查询 (`query_users_by_ip.py`)
根据IP查询关联用户，发现共享IP的刷量团伙。

```bash
python3 query_users_by_ip.py <ip>
```

**输出：**
- 该IP下的所有用户
- 注册时间分布
- 设备分布

### 10. 系统性综合分析 (`fraud_analyzer.py`)
整合所有分析维度，生成综合报告。

```bash
python3 fraud_analyzer.py <userId>
```

**输出：**
- 风险等级（low/medium/high）
- 风险指标列表
- 综合分析结论

## 数据库配置

```python
DB_CONFIG = {
    'host': 'rr-wz97dxha81orq30j0eo.mysql.rds.aliyuncs.com',
    'port': 3389,
    'user': 'oc_gw',
    'password': 'm83KkZVLQp2Wg7HgDVb5cRjQ',
    'database': 'yc_db',
    'charset': 'utf8mb4'
}
```

## 核心SQL语句

### 1. 查询用户基本信息
```sql
SELECT u.id, u.mobile, u.truename, u.regTime, u.inviteCode,
       IFNULL(p.userId, '') as parentId,
       IFNULL(i.idNo, ip.idNo) as idNo,
       IFNULL(ip.status, 0) as proStatus,
       u.level, u.memberType,
       IFNULL(c.dataStatus, -1) as dataStatus,
       c.remarker
FROM t_user u
LEFT JOIN t_user p ON u.refereeId = p.id
LEFT JOIN t_user_identity i ON i.userId = u.id
LEFT JOIN t_user_identitypro ip ON ip.id = u.id
LEFT JOIN t_invite_usercmpdata c ON c.id = u.id
WHERE u.userId = #{userId}
```

### 2. 查询用户做单记录
```sql
SELECT sb.id, sb.taskAmout, sb.examineText, t.taskNo, t.title,
       s.deviceId, sb.status,
       FROM_UNIXTIME(sb.claimTime/1000) as claimTime,
       FROM_UNIXTIME(sb.subTime/1000) as subTime,
       u.userId, c.provice, c.city, s.ip
FROM t_task_subctx s
INNER JOIN t_task_submit sb ON sb.id = s.subId
INNER JOIN t_task t ON sb.taskId = t.id
INNER JOIN t_user u ON u.id = sb.subId
INNER JOIN t_ip_config c ON c.id = INET_ATON(s.ip)
WHERE u.userId = #{userId} AND sb.status = 2
ORDER BY sb.claimTime DESC
LIMIT 100
```

### 3. 查询发单人账单
```sql
SELECT a.id, a.transDetail, a.amount, a.payTime
FROM t_accout_trans a
WHERE a.userId = (SELECT id FROM t_user WHERE userId = #{userId})
AND a.status = 4
ORDER BY a.subTime DESC
LIMIT 50
```

### 4. 查询任务做单人
```sql
SELECT sb.id, u.regTime, u.userId as userNo, sb.claimTime,
       sb.subTime, sb.examineTime, u.refereeId
FROM t_task_submit sb
INNER JOIN t_user u ON u.id = sb.subId
INNER JOIN t_task t ON sb.taskId = t.id
WHERE t.taskNo = #{taskNo} AND sb.status = 2
ORDER BY sb.examineTime DESC
LIMIT 100
```

### 5. 查询用户登录记录
```sql
SELECT l.ip, c.provice, c.city, l.loginTime, l.deviceId
FROM t_user_loginlogs_2022 l
INNER JOIN t_user u ON l.userId = u.id
INNER JOIN t_ip_config c ON c.id = INET_ATON(l.ip)
WHERE u.userId = #{userId}
ORDER BY l.loginTime DESC
LIMIT 10
```

### 6. 查询IP关联用户
```sql
SELECT DISTINCT u.userId, u.mobile, u.truename, u.regTime
FROM t_user_loginlogs_2022 l
INNER JOIN t_user u ON l.userId = u.id
WHERE l.ip = #{ip}
AND l.loginTime > DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY l.loginTime DESC
LIMIT 20
```

### 7. 查询APP访问记录
```sql
SELECT v.id, v.appId, v.channel, v.version, v.deviceId,
       FROM_UNIXTIME(v.visitTime/1000) as visitTime,
       v.ip, v.mobileBrand
FROM t_app_visitlog_202204 v
WHERE v.userId = (SELECT id FROM t_user WHERE userId = #{userId})
ORDER BY v.visitTime DESC
LIMIT 10
```

### 8. 查询任务操作记录
```sql
SELECT l.taskId, l.ops, l.optime, l.ip, l.deviceId
FROM t_task_opdetaillogs l
INNER JOIN t_user u ON l.userId = u.id
WHERE u.userId = #{userId}
ORDER BY l.optime DESC
LIMIT 20
```

### 9. 查询账户账单（置顶/刷新消费）
```sql
-- inFlag: 0=消费, 1=充值
-- status: 4和6才是成功状态
-- payTime: 日期格式，无需FROM_UNIXTIME转换
-- subTime: 毫秒时间戳，需要FROM_UNIXTIME转换
SELECT 
    a.id,
    a.transDetail,
    a.amount,
    a.payTime,
    FROM_UNIXTIME(a.subTime/1000) as subTime
FROM t_accout_trans a 
WHERE a.userId = (SELECT id FROM t_user WHERE userId = #{userId})
AND a.inFlag = 0
AND a.status IN (4, 6)
AND (a.transDetail LIKE '%置顶%' OR a.transDetail LIKE '%刷新%' OR a.transDetail LIKE '%推荐%')
ORDER BY a.subTime DESC
LIMIT 100
```

### 10. 通过手机号查询用户
```sql
SELECT 
    id,
    userId,
    truename,
    mobile,
    FROM_UNIXTIME(regTime/1000) as regTime
FROM t_user 
WHERE mobile = #{mobile}
LIMIT 1
```

### 11. 查询用户状态（禁言/限制/冻结）
**注意：以下查询的userId是数字ID（t_user.id），不是字符串userId**

```sql
-- 是否禁言 (status >= 1 表示被禁言)
SELECT status FROM t_msg_black WHERE userId = #{id} AND status >= 1 LIMIT 1;

-- 是否禁止发单 (typeId=1)
SELECT reason FROM t_task_black WHERE id = #{id} AND typeId = 1 AND status = 1 LIMIT 1;

-- 是否禁止接单 (typeId=2)
SELECT reason FROM t_task_black WHERE id = #{id} AND typeId = 2 AND status = 1 LIMIT 1;

-- 是否禁止充值
SELECT typeId, remarker FROM t_hb_black WHERE userId = #{id} AND status = 1 LIMIT 1;

-- 是否冻结 (方式1: status=100)
SELECT attr5 FROM t_accout WHERE userId = #{id} AND status = 100 LIMIT 1;

-- 是否冻结 (方式2: status=0)
SELECT reason FROM t_user_frozen WHERE userId = #{id} AND status = 0 LIMIT 1;

-- 查询账户余额
SELECT d.typeCode as accoutType, d.balance as amount 
FROM t_accout_detail d 
INNER JOIN t_accout a ON d.accoutId = a.id
WHERE a.userId = #{id}
LIMIT 10;
```

## 数据库字段说明

### t_accout_trans 账单表
| 字段 | 说明 | 格式 |
|------|------|------|
| `inFlag` | 0=消费（支出），1=充值（收入） | 整数 |
| `status` | 4和6才是成功状态 | 整数 |
| `transDetail` | 交易描述（置顶、刷新、推荐等） | 字符串 |
| `amount` | 金额（单位：分） | 整数 |
| `payTime` | 支付时间 | **日期格式** `2026-03-08 11:14:17` |
| `subTime` | 提交时间 | **毫秒时间戳** |
| `transType` | 交易类型代码 | 整数 |
| `accoutType` | 账户类型 | 整数 |

### 账户类型 (accoutType)
| 代码 | 名称 | 用途 |
|------|------|------|
| `1000` | 任务余额 | **置顶/推荐/刷新只能使用此账户** |
| `1001` | 保证金 | 充值可用 |
| `1002` | 收入分红 | 接单收入 |
| `1003` | 推广收入 | 平台奖励 |

### t_task_submit 任务提交表
| 字段 | 说明 |
|------|------|
| `status` | 2=已完成 |
| `claimTime` | 报名时间（毫秒时间戳） |
| `subTime` | 提交时间（毫秒时间戳） |
| `examineTime` | 审核时间（毫秒时间戳） |

### t_user 用户表
| 字段 | 说明 |
|------|------|
| `userId` | 用户ID（字符串，如 3524F5） |
| `id` | 内部ID（数字） |
| `regTime` | 注册时间（毫秒时间戳） |
| `refereeId` | 上级ID（数字，0表示无上级） |

## 风险指标说明

### 高风险指标
1. **系统已标记**: 系统备注中包含"刷单"等关键词
2. **快速完成率高**: >50%的任务在5分钟内完成
3. **大量新用户接单**: 任务接单人>50%为最近7天注册
4. **无置顶消费**: 发单人但无置顶/刷新消费记录

### 中风险指标
1. **最近注册**: 7天内注册的新用户
2. **中等快速完成率**: 30-50%的任务在5分钟内完成
3. **发单人消费低**: 置顶/刷新消费比例偏低

### 低风险指标
1. **个别指标异常**: 单一指标轻微异常
2. **历史记录正常**: 无明显刷单模式

## 典型刷量团伙特征

### 1. 组织层级
```
顶级上级 (003183)
    └── 组织者 (4FFAF4)
        ├── 刷量账号1 (124BAA0)
        ├── 刷量账号2 (124B3B9)
        └── ... (25个徒弟)
```

### 2. 发单人网络
```
高风险发单人 (D444AD, 3BC684)
    └── 发布任务
        └── 刷量接单人完成
```

### 3. 地理分布
- 分布式：全国各地分散，避免集中
- 共享IP：少数IP共享（VPN/代理）
- 设备独立：每个账号独立设备

### 4. 时间模式
- 深夜操作：避开监控高峰
- 批量执行：短时间内完成大量任务
- 一次性账号：注册当天完成，之后不再使用

## 调查建议流程

### 第一步：初步筛查
```bash
python3 fraud_analyzer.py <userId>
```

### 第二步：深入调查（如风险等级高）
```bash
# 查询上级和徒弟
python3 query_user_detail.py <parentId>

# 查询任务做单人
python3 analyze_user_tasks_completers.py <userId>

# 查询发单人详情
python3 analyze_user_publisher_tasks.py <publisherId>
```

### 第三步：关联分析
```bash
# IP关联分析
python3 query_users_by_ip.py <ip>

# 设备关联分析（通过APP访问记录）
python3 query_user_visit_logs.py <userId>
```

### 第四步：生成报告
整合所有查询结果，形成完整的调查报告。

## 注意事项

1. **查询限制**: 所有查询都设置了LIMIT，避免大数据量查询
2. **时间范围**: 默认查询最近7天/30天的数据
3. **隐私保护**: 身份证号、手机号等敏感信息已脱敏
4. **性能优化**: 使用索引字段进行查询，提高查询效率

## 更新日志

- 2026-03-08: 创建系统性分析工具和文档
- 支持用户详情、登录记录、任务分析、发单分析等多维度查询
- 提供风险等级自动评估功能