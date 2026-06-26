# DataWorks 常见错误代码与解决方案

本参考文档收录了 DataWorks 任务执行中常见的错误类型及其解决方案。

---

## 错误分类索引

| 分类 | 错误类型 | 严重程度 |
|------|----------|----------|
| 🔴 资源类 | 资源配额不足、内存溢出、磁盘空间不足 | 高 |
| 🔴 网络类 | 连接超时、网络不可达、白名单问题 | 高 |
| 🔴 权限类 | 权限不足、认证失败、AK 无效 | 高 |
| 🟡 代码类 | SQL 语法错误、表不存在、字段错误 | 中 |
| 🟡 数据类 | 数据质量检查失败、空值约束违反 | 中 |
| 🟡 依赖类 | 上游任务失败、依赖缺失 | 中 |
| 🟢 限流类 | API 调用超限、QPS 限制 | 中 |

---

## 🔴 资源类错误

### 1. 资源配额不足

**错误特征：**
```
ERROR: quota exceeded
ERROR: resource insufficient
ERROR: no available resource in queue
```

**常见原因：**
- 资源组使用率已达上限
- 并发任务数超过配额
- 资源组配置过小

**解决方案：**
1. 查看资源组使用情况
   ```bash
   # 在 DataWorks 控制台查看资源组监控
   ```
2. 释放闲置资源
   - 停止不必要的测试任务
   - 优化长期运行的任务
3. 提升配额
   - 联系管理员调整资源组配置
   - 升级资源组规格
4. 错峰调度
   - 调整任务调度时间，避开高峰

**参考文档：**
https://help.aliyun.com/document_detail/dataworks/resource-group.html

---

### 2. 内存溢出 (OOM)

**错误特征：**
```
ERROR: OutOfMemoryError
ERROR: Java heap space
ERROR: GC overhead limit exceeded
ERROR: Container killed by YARN for exceeding memory limits
```

**常见原因：**
- 数据处理量过大
- SQL 查询未优化，扫描全表
- 数据倾斜导致单点内存不足

**解决方案：**
1. 增加内存配置
   ```
   任务配置 → 资源设置 → 增加内存 (如 4GB → 8GB)
   ```
2. 优化 SQL
   ```sql
   -- 添加分区裁剪
   SELECT * FROM table WHERE ds = '20240115'
   
   -- 避免 SELECT *
   SELECT col1, col2 FROM table
   
   -- 使用近似计算
   SELECT APPROX_COUNT_DISTINCT(user_id) FROM table
   ```
3. 处理数据倾斜
   ```sql
   -- 添加随机前缀打散数据
   SELECT /*+ MAPJOIN(small_table) */ * FROM large_table JOIN small_table
   ```
4. 分批处理
   - 将大任务拆分为多个小任务
   - 使用增量处理替代全量

**参考文档：**
https://help.aliyun.com/document_detail/dataworks/performance-tuning.html

---

### 3. 磁盘空间不足

**错误特征：**
```
ERROR: No space left on device
ERROR: Disk quota exceeded
ERROR: Storage exhausted
```

**解决方案：**
1. 清理临时文件
2. 检查输出表数据量是否异常
3. 增加磁盘配额
4. 优化任务减少中间数据

---

## 🔴 网络类错误

### 1. 连接超时

**错误特征：**
```
ERROR: Connection timeout
ERROR: Connect timed out
ERROR: Network unreachable
ERROR: Host unreachable
```

**常见原因：**
- 数据源服务器不可达
- 防火墙阻挡
- 白名单未配置
- VPC 网络不通

**解决方案：**
1. 检查网络连通性
   ```bash
   ping your-database-host.com
   telnet your-database-host.com 3306
   ```
2. 配置白名单
   - 添加 DataWorks 服务器 IP 到数据源白名单
   - 参考：https://help.aliyun.com/document_detail/dataworks/ip-ranges.html
3. 检查 VPC 配置
   - 确保 DataWorks 和数据源在同一 VPC
   - 或配置 VPC 对等连接
4. 增加超时时间
   ```
   任务配置 → 高级设置 → 连接超时 (如 30s → 60s)
   ```

---

### 2. 白名单问题

**错误特征：**
```
ERROR: Access denied for IP
ERROR: Host not in whitelist
ERROR: Connection rejected by whitelist
```

**解决方案：**
1. 获取 DataWorks IP 段
   - 查看官方文档 IP 列表
   - 或在控制台查看当前工作区 IP
2. 添加 IP 到白名单
   - 登录数据源管理控制台
   - 添加 DataWorks IP 到访问白名单
3. 使用 VPC 网络（推荐）
   - 配置 VPC 绑定
   - 避免公网传输

---

## 🔴 权限类错误

### 1. 权限不足

**错误特征：**
```
ERROR: Permission denied
ERROR: Access denied
ERROR: Unauthorized
ERROR: Authentication failed
```

**常见原因：**
- 数据源账号权限不足
- RAM 角色未授权
- AccessKey 无效或过期

**解决方案：**
1. 检查账号权限
   ```sql
   -- MySQL 示例
   SHOW GRANTS FOR 'username'@'%';
   ```
2. 验证 AccessKey
   - 在 RAM 控制台检查 AK 状态
   - 确保 AK 有 DataWorks 相关权限
3. 配置 RAM 角色
   - 创建 RAM 角色
   - 授予必要权限
   - 在 DataWorks 中绑定角色

**权限清单：**
| 操作 | 所需权限 |
|------|----------|
| 读表 | SELECT |
| 写表 | INSERT, CREATE |
| 删表 | DROP |
| 执行存储过程 | EXECUTE |

**参考文档：**
https://help.aliyun.com/document_detail/dataworks/permission.html

---

## 🟡 代码类错误

### 1. SQL 语法错误

**错误特征：**
```
ERROR: Syntax error near 'xxx'
ERROR: Parse error at line X
ERROR: Invalid syntax
```

**解决方案：**
1. 使用语法检查工具
2. 检查关键字拼写
3. 验证表名、字段名
4. 检查特殊字符转义

**常见语法错误示例：**
```sql
-- 错误：缺少引号
SELECT * FROM table WHERE name = John

-- 正确
SELECT * FROM table WHERE name = 'John'

-- 错误：关键字未转义
SELECT order FROM table

-- 正确
SELECT `order` FROM table
```

---

### 2. 表/字段不存在

**错误特征：**
```
ERROR: Table 'xxx' doesn't exist
ERROR: Column 'xxx' not found
ERROR: Relation does not exist
```

**解决方案：**
1. 确认表名拼写
2. 检查数据库/Schema
3. 验证表是否被删除
4. 检查分区是否存在

---

## 🟡 数据类错误

### 1. 数据质量检查失败

**错误特征：**
```
ERROR: Data quality check failed
ERROR: Quality rule violation
ERROR: Null value not allowed
```

**常见原因：**
- 源数据存在空值
- 数据类型不匹配
- 违反唯一性约束

**解决方案：**
1. 检查数据质量规则配置
2. 分析源数据异常值
3. 添加数据清洗步骤
4. 配置容错处理

---

## 🟡 依赖类错误

### 1. 上游任务失败

**错误特征：**
```
ERROR: Dependency failed
ERROR: Upstream node failed
ERROR: Parent node not completed
```

**解决方案：**
1. 检查上游节点状态
2. 查看上游错误日志
3. 调整依赖配置
4. 添加重试机制

---

## 🟢 限流类错误

### 1. API 调用超限

**错误特征：**
```
ERROR: Rate limit exceeded
ERROR: Too many requests
ERROR: QPS limit reached
```

**解决方案：**
1. 降低调用频率
2. 添加重试退避
   ```python
   import time
   for i in range(3):
       try:
           call_api()
           break
       except RateLimitError:
           time.sleep(2 ** i)  # 指数退避
   ```
3. 申请提升配额
4. 使用批量接口

---

## 故障排查流程

```
1. 查看错误日志
   ↓
2. 识别错误类型（参考本手册）
   ↓
3. 根据解决方案逐一尝试
   ↓
4. 验证修复效果
   ↓
5. 如未解决，收集以下信息联系支持：
   - 完整错误日志
   - 任务配置截图
   - 相关资源监控数据
```

---

## 快速诊断命令

```bash
# 检查资源使用
dataworks-cli resource status

# 检查网络连接
dataworks-cli network check --target <datasource>

# 检查权限
dataworks-cli permission check --user <username>

# 获取任务日志
dataworks-cli task log --instance <instance_id>
```

---

## 有用的链接

- [DataWorks 官方文档](https://help.aliyun.com/product/27728.html)
- [常见问题 FAQ](https://help.aliyun.com/document_detail/dataworks/faq.html)
- [错误码大全](https://help.aliyun.com/document_detail/dataworks/error-codes.html)
- [社区论坛](https://developer.aliyun.com/group/dataworks)

---

## 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2024-01-15 | 初始版本 |
