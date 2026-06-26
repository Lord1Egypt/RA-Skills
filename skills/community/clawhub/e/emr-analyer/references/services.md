# 大数据服务参考手册

本文档记录各大数据服务的进程名、端口、配置文件路径、日志路径等关键信息。

---

## 服务列表

| 服务 | 进程名 | 默认端口 | 配置文件 | 日志路径 |
|------|--------|----------|----------|----------|
| YARN | ResourceManager, NodeManager | 8088, 8042 | yarn-site.xml | /var/log/hadoop-yarn/ |
| HDFS | NameNode, DataNode | 9870, 9864 | hdfs-site.xml | /var/log/hadoop-hdfs/ |
| Hive | HiveServer2, Metastore | 10000, 9083 | hive-site.xml | /var/log/hive/ |
| Spark | Spark Master, Worker | 8080, 8081 | spark-env.sh | /var/log/spark/ |
| Impala | impalad, catalogd, statestored | 21050, 25010, 25020 | impala-site.xml | /var/log/impala/ |
| Trino | trino-server | 8080 | config.properties | /var/log/trino/ |
| Tez | (运行在 YARN 上) | - | tez-site.xml | /var/log/hadoop-yarn/ |
| StarRocks | fe, be | 8030, 9030 | fe.conf, be.conf | /opt/starrocks/log/ |
| HBase | HMaster, RegionServer | 16010, 16030 | hbase-site.xml | /var/log/hbase/ |
| Kafka | kafka.Kafka | 9092 | server.properties | /var/log/kafka/ |
| ZooKeeper | QuorumPeerMain | 2181 | zoo.cfg | /var/log/zookeeper/ |
| Ranger | ranger-admin, ranger-usersync | 6080, 6180 | ranger-admin-site.xml | /var/log/ranger/ |
| OpenLDAP | slapd | 389, 636 | slapd.conf | /var/log/slapd.log |
| Hue | runserver | 8888 | hue.ini | /var/log/hue/ |
| Flink | StandaloneClusterEntrypoint, TaskManager | 8081 | flink-conf.yaml | /var/log/flink/ |

---

## 阿里云 EMR 日志路径参考

来源：https://help.aliyun.com/zh/emr/emr-on-ecs/user-guide/paths-of-frequently-used-files

### 通用日志目录

```
/var/log/
├── hadoop-hdfs/          # HDFS 日志
├── hadoop-yarn/          # YARN 日志
├── hive/                 # Hive 日志
├── spark/                # Spark 日志
├── impala/               # Impala 日志
├── hbase/                # HBase 日志
├── kafka/                # Kafka 日志
├── zookeeper/            # ZooKeeper 日志
├── flink/                # Flink 日志
└── hue/                  # Hue 日志
```

### 配置文件目录

**优先查找**: `/etc/taihao-apps/`
```
/etc/taihao-apps/
├── hadoop-conf/          # Hadoop 配置 (hdfs-site.xml, yarn-site.xml, core-site.xml)
├── hive-conf/            # Hive 配置 (hive-site.xml)
├── spark-conf/           # Spark 配置
├── impala-conf/          # Impala 配置
├── hbase-conf/           # HBase 配置
├── kafka-conf/           # Kafka 配置
├── zookeeper-conf/       # ZooKeeper 配置
└── flink-conf/           # Flink 配置
```

**回退路径**: `/etc/ecm/` (如果 taihao-apps 不存在)
```
/etc/ecm/
├── hadoop-conf/          # Hadoop 配置
├── hive-conf/            # Hive 配置
├── spark-conf/           # Spark 配置
├── impala-conf/          # Impala 配置
├── hbase-conf/           # HBase 配置
├── kafka-conf/           # Kafka 配置
├── zookeeper-conf/       # ZooKeeper 配置
└── flink-conf/           # Flink 配置
```

### 数据目录

```
/mnt/disk1/
├── hadoop/               # HDFS 数据
├── yarn/                 # YARN 本地数据
└── ...
```

---

## 常用诊断命令

### 检查进程状态

```bash
# 检查服务进程
ps aux | grep -E '<进程名>'

# 检查端口监听
netstat -tlnp | grep <端口>
# 或
ss -tlnp | grep <端口>

# 检查系统服务状态
systemctl status <服务名>
```

### 获取服务版本

```bash
# Hadoop 生态
hadoop version
hdfs version
yarn version
hive --version
spark-submit --version
impala-shell --version
hbase version
kafka-topics.sh --version
zookeeper-server-status.sh
flink --version

# StarRocks
mysql -h 127.0.0.1 -P 8030 -u root -e "SHOW FRONTENDS;"

# Trino
trino --version
```

### 获取配置参数

```bash
# Hadoop
hdfs getconf -confKey <key>
yarn getconf -confKey <key>

# Hive
hive --config /etc/hive/conf/conf.server/ -e "SET <key>;"

# 直接读取配置文件
cat /etc/ecm/hadoop-conf/hdfs-site.xml | grep <property>
```

### 查看日志

```bash
# 查看最近日志
tail -100 /var/log/<service>/<logfile>

# 搜索错误
grep -i "error\|exception\|fatal" /var/log/<service>/<logfile>

# 实时跟踪日志
tail -f /var/log/<service>/<logfile>

# 按时间过滤
awk '/2026-04-09 10:00/,/2026-04-09 11:00/' /var/log/<service>/<logfile>
```

---

## 常见错误模式

### YARN
- `Container killed by the ApplicationMaster` - 容器被杀死，检查资源不足
- `NodeManager unavailable` - NM 失联，检查网络和进程状态
- `Queue is at full capacity` - 队列容量已满

### HDFS
- `SafeMode` - 安全模式，检查磁盘空间和数据块完整性
- `DataNode unavailable` - DN 失联
- `Block report timeout` - 块报告超时

### Hive
- `Metastore connection failed` - 元数据库连接问题
- `OutOfMemoryError` - 内存不足
- `Permission denied` - 权限问题

### Spark
- `ExecutorLostFailure` - Executor 丢失
- `OutOfMemoryError: Java heap space` - JVM 内存不足
- `Task not serializable` - 序列化问题

### Kafka
- `NotLeaderForPartitionException` - Leader 选举中
- `TimeoutException` - 超时，检查网络和负载
- `OutOfMemoryError` - 内存不足

---

## 性能调优参数参考

### YARN
```
yarn.nodemanager.resource.memory-mb     # 节点总内存
yarn.nodemanager.resource.cpu-vcores    # 节点总 CPU
yarn.scheduler.maximum-allocation-mb    # 单容器最大内存
```

### Spark
```
spark.executor.memory                   # Executor 内存
spark.executor.cores                    # Executor CPU 核心数
spark.driver.memory                     # Driver 内存
spark.sql.shuffle.partitions            # Shuffle 分区数
```

### Hive
```
hive.exec.parallel                      # 并行执行
hive.auto.convert.join                  # 自动 MapJoin
hive.tez.container.size                 # Tez 容器大小
```

### HBase
```
hbase.regionserver.global.memstore.size # 全局 MemStore 大小
hfile.block.cache.size                  # BlockCache 大小
```

---

## 外部文档链接

- [Apache Hadoop 官方文档](https://hadoop.apache.org/docs/)
- [Apache Spark 官方文档](https://spark.apache.org/docs/)
- [Apache Hive 官方文档](https://hive.apache.org/docs/)
- [StarRocks 官方文档](https://docs.starrocks.io/)
- [Apache Kafka 官方文档](https://kafka.apache.org/documentation/)
- [阿里云 EMR 文档](https://help.aliyun.com/zh/emr/)
