---
name: emr-analyer
description: Linux 系统上开源大数据应用分析诊断工具。支持服务状态检查、参数配置获取和调优、任务报错分析并提供优化建议。支持 YARN、Hive、HDFS、Spark、Impala、Trino、Tez、StarRocks、HBase、Kafka、ZooKeeper、Ranger、OpenLDAP、Hue、Flink。
---

# 大数据应用分析诊断工具

本技能提供 Linux 系统上开源大数据应用的分析诊断能力，包括服务状态确认、参数配置获取和调优、任务报错分析并提供优化建议。

---

## 支持的服务

| 服务 | 进程名 | 默认端口 | 配置文件路径 | 日志路径 |
|------|--------|----------|--------------|----------|
| YARN | ResourceManager, NodeManager | 8088, 8042 | /etc/taihao-apps/hadoop-conf/yarn-site.xml | /var/log/hadoop-yarn/ |
| HDFS | NameNode, DataNode | 9870, 9864 | /etc/taihao-apps/hadoop-conf/hdfs-site.xml | /var/log/hadoop-hdfs/ |
| Hive | HiveServer2, Metastore | 10000, 9083 | /etc/taihao-apps/hive-conf/hive-site.xml | /var/log/hive/ |
| Spark | Spark Master, Worker | 8080, 8081 | /etc/taihao-apps/spark-conf/spark-env.sh | /var/log/spark/ |
| Impala | impalad, catalogd, statestored | 21050, 25010, 25020 | /etc/taihao-apps/impala-conf/impala-site.xml | /var/log/impala/ |
| Trino | trino-server | 8080 | config.properties | /var/log/trino/ |
| Tez | (运行在 YARN 上) | - | tez-site.xml | /var/log/hadoop-yarn/ |
| StarRocks | fe, be | 8030, 9030 | /opt/starrocks/fe/conf/fe.conf | /opt/starrocks/log/ |
| HBase | HMaster, RegionServer | 16010, 16030 | /etc/taihao-apps/hbase-conf/hbase-site.xml | /var/log/hbase/ |
| Kafka | kafka.Kafka | 9092 | /etc/taihao-apps/kafka-conf/server.properties | /var/log/kafka/ |
| ZooKeeper | QuorumPeerMain | 2181 | /etc/taihao-apps/zookeeper-conf/zoo.cfg | /var/log/zookeeper/ |
| Ranger | ranger-admin, ranger-usersync | 6080, 6180 | ranger-admin-site.xml | /var/log/ranger/ |
| OpenLDAP | slapd | 389, 636 | slapd.conf | /var/log/slapd.log |
| Hue | runserver | 8888 | hue.ini | /var/log/hue/ |
| Flink | StandaloneClusterEntrypoint, TaskManager | 8081 | /etc/taihao-apps/flink-conf/flink-conf.yaml | /var/log/flink/ |

**配置文件路径说明**: 优先查找 `/etc/taihao-apps/<service>-conf/`，如果不存在则回退到 `/etc/ecm/<service>-conf/`

---

## 使用方法

### 1. 检查集群整体状态

**用户输入**: "帮我分析下这个集群的服务整体情况"

**执行流程**:
1. 调用 `check_service_status.py all` 获取所有服务状态
2. 汇总 RUNNING/NOT_RUNNING 状态
3. 输出服务健康报告

```bash
python3 {baseDir}/scripts/check_service_status.py all
```

### 2. 检查单个服务状态

**用户输入**: "YARN 服务正常吗？" / "检查 HDFS 状态"

```bash
python3 {baseDir}/scripts/check_service_status.py <service_name>
```

### 3. 分析报错日志

**用户输入**: 
- "帮我分析下这个报错：[错误日志内容]"
- "Hive 查询失败了，看看日志"

**执行流程**:
1. 识别报错所属服务
2. 调用 `analyze_logs.py <service>` 分析日志
3. 匹配错误模式并提供修复建议

```bash
python3 {baseDir}/scripts/analyze_logs.py <service_name> [lines]
```

### 4. 获取配置参数

**用户输入**: 
- "查看 Spark 的配置参数"
- "YARN 的内存配置是多少"

```bash
python3 {baseDir}/scripts/check_config.py <service_name>
```

### 5. 获取调优建议

**用户输入**: 
- "如何优化 Hive 查询性能"
- "Kafka 配置怎么调优"

**执行流程**:
1. 调用 `check_config.py` 获取当前配置
2. 根据 KEY_PARAMS 和调优规则生成建议
3. 输出优化建议

---

## 脚本说明

### check_service_status.py

检查服务进程、端口监听、systemd 服务状态。

**输出示例**:
```json
{
  "name": "yarn",
  "status": "RUNNING",
  "processes": [
    {"name": "ResourceManager", "running": true, "details": "..."},
    {"name": "NodeManager", "running": true, "details": "..."}
  ],
  "ports": [
    {"port": 8088, "listening": true, "details": "..."}
  ],
  "systemd": "active",
  "version": "Hadoop 3.3.6"
}
```

### analyze_logs.py

分析服务日志，识别错误模式并提供修复建议。

**识别的错误类型**:
- 内存问题 (OOM, GC overhead)
- 连接问题 (Connection refused/timeout)
- 权限问题 (Permission denied)
- 磁盘问题 (No space left)
- 超时问题 (TimeoutException)
- 服务特定错误 (DataNode unavailable, Container killed 等)

**输出示例**:
```json
{
  "service": "hive",
  "status": "ANALYZED",
  "error_summary": {
    "OOM - 内存不足": 5,
    "连接超时": 2
  },
  "suggestions": {
    "OOM - 内存不足": ["增加 JVM 堆内存", "检查内存泄漏", ...]
  },
  "recommendations": ["优先处理内存问题 - 检查并调整 JVM 堆内存配置"]
}
```

### check_config.py

获取服务配置参数并提供调优建议。

**输出示例**:
```json
{
  "service": "spark",
  "config_file": "/etc/ecm/spark-conf/spark-env.sh",
  "config_exists": true,
  "params": {
    "spark.executor.memory": "4g",
    "spark.sql.shuffle.partitions": "200"
  },
  "suggestions": [
    {
      "param": "spark.executor.memory",
      "current": "4g",
      "suggestion": "根据数据量调整，一般 4g-8g 起步",
      "reason": "Executor 内存影响任务处理能力"
    }
  ]
}
```

---

## 工作流程

### 场景 1: 集群健康检查

```
用户：帮我分析下这个集群的服务整体情况
  ↓
1. 执行 check_service_status.py all
  ↓
2. 汇总各服务状态 (RUNNING/NOT_RUNNING)
  ↓
3. 识别异常服务
  ↓
4. 对异常服务执行 analyze_logs.py
  ↓
5. 输出健康报告 + 问题诊断 + 修复建议
```

### 场景 2: 报错分析

```
用户：[粘贴报错日志]
  ↓
1. 识别报错所属服务 (关键词匹配)
  ↓
2. 执行 analyze_logs.py <service>
  ↓
3. 匹配错误模式
  ↓
4. 从 FIX_SUGGESTIONS 获取修复建议
  ↓
5. 输出错误分析 + 解决方案
```

### 场景 3: 性能调优

```
用户：如何优化 Spark 查询性能
  ↓
1. 执行 check_config.py spark
  ↓
2. 获取当前关键配置参数
  ↓
3. 根据调优规则生成建议
  ↓
4. 输出配置现状 + 优化建议 + 预期效果
```

---

## 日志路径参考

### 配置文件路径

- **优先**: `/etc/taihao-apps/<service>-conf/`
- **回退**: `/etc/ecm/<service>-conf/` (如果 taihao-apps 不存在)

### 日志路径

- **Hadoop 生态**: `/var/log/hadoop-<service>/`
- **Hive**: `/var/log/hive/`
- **Spark**: `/var/log/spark/`
- **其他服务**: 详见 `references/services.md`

---

## 常见错误及解决方案

### YARN
| 错误 | 原因 | 解决方案 |
|------|------|----------|
| Container killed by AM | 超时/OOM | 增加 executor 内存，检查任务耗时 |
| NodeManager unavailable | 进程挂掉/网络 | 检查 NM 进程，查看 NM 日志 |
| Queue full capacity | 队列资源满 | 等待任务完成或增加队列容量 |

### HDFS
| 错误 | 原因 | 解决方案 |
|------|------|----------|
| SafeMode | 磁盘满/块损坏 | 清理空间，运行 fsck |
| DataNode unavailable | DN 失联 | 检查 DN 进程和网络 |
| Missing blocks | 数据块丢失 | 从备份恢复，检查副本数 |

### Spark
| 错误 | 原因 | 解决方案 |
|------|------|----------|
| ExecutorLostFailure | Executor 挂掉 | 检查 OOM，增加内存 |
| OutOfMemoryError | 内存不足 | 调大 -Xmx，减少数据量 |
| Task not serializable | 序列化问题 | 检查闭包变量 |

### Hive
| 错误 | 原因 | 解决方案 |
|------|------|----------|
| Metastore connection failed | DB 连接问题 | 检查 MySQL 服务，连接串 |
| OutOfMemoryError | 内存不足 | 增加 Container 大小 |
| Permission denied | 权限问题 | 检查 HDFS/Ranger 权限 |

### Kafka
| 错误 | 原因 | 解决方案 |
|------|------|----------|
| NotLeaderForPartition | Leader 选举 | 等待选举完成 |
| TimeoutException | 超时 | 增加 timeout 配置 |
| OutOfMemoryError | 内存不足 | 增加 heap 大小 |

---

## 外部文档

- [阿里云 EMR 文档](https://help.aliyun.com/zh/emr/)
- [阿里云 EMR 日志路径](https://help.aliyun.com/zh/emr/emr-on-ecs/user-guide/paths-of-frequently-used-files)
- [Apache Hadoop 官方文档](https://hadoop.apache.org/docs/)
- [Apache Spark 官方文档](https://spark.apache.org/docs/)

---

## 注意事项

1. **权限要求**: 需要 SSH 访问目标服务器，建议有 sudo 权限
2. **日志轮转**: 旧日志可能被压缩，需要 zcat/gunzip 查看
3. **配置变更**: 修改配置后需要重启服务才能生效
4. **生产环境**: 调优前建议在测试环境验证

---

*大数据应用分析诊断工具 - 让集群运维更高效 🔍*
