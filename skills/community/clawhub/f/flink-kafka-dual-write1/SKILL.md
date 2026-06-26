---
name: flink-kafka-dual-write
description: 为 bethune 项目生成新的 Flink Kafka 到 Hive 和 StarRocks 双写监控任务，参考 Bus_Search_ReplacePrice_KafkaToStarRock_34 及相邻的 33/35/36 模式，自动产出 Job 类、MessageModel、PO、4 个 config.properties 更新，并在可行时执行编译校验。用于“参考任务34写一个新任务”“按任务33/34/35/36模式新增 Kafka 任务”“生成类似 ReplacePrice 的埋点监控任务”等请求。
---

# Flink Kafka 双写任务生成

按下面流程执行，默认服务对象是 bethune 仓库中的 Kafka 日志监控任务。

## 先做什么

先确认用户给了哪些输入。若信息不全，只问最小必需项：

- 任务编号
- 参考任务，若用户说“参考任务34”则优先复用 34 的骨架
- Kafka topic
- module 过滤值
- 目标表名或业务名
- 消息字段结构，尤其是是否存在嵌套对象或列表展开字段

若用户已经给出“按任务34类似模式”，默认理解为：

- 单条消息通常产出一行，不按列表展开
- 保留 Kafka -> filter -> flatMap -> Hive -> StarRocks 的完整链路
- 沿用 `parseAndFormatLogTime()`、`safe()`、Hive 分区补齐、4 份 config 同步更新的处理方式

若任务更接近 35 或 36 这类列表展开模式，按列表展开规则处理。详细模式见 `references/bethune-patterns.md`。

## 实现步骤

1. 先阅读参考任务及相关 `MessageModel`、`Po`、`config.properties` 键位，确认命名和字段顺序。
2. 生成或更新 3 个 Java 文件：`MessageModel`、`Po`、`Job`。
3. 同步更新 4 个配置文件：
   - `src/main/resources/config.properties`
   - `src/main/resources/dev/config.properties`
   - `src/main/resources/product/config.properties`
   - `src/main/resources/stage/config.properties`
4. 在仓库可编译时运行 `mvn -DskipTests compile` 验证新增任务。
5. 向用户回传新增文件、配置键、是否编译通过；若用户需要，再补 Hive 和 StarRocks DDL。

## 必须遵守的约束

- 保持 `TableSchema`、`StarRocksSinkRowBuilder`、`toHiveRow()` 三处字段顺序完全一致。
- `st` 永远放在输出首列；Hive 行末尾永远追加 `year`、`month`、`day`。
- `module` 过滤值写死在 Job 类常量里，不写入配置。
- `logTime` 统一走 A 方案：为空或解析失败都记录错误日志并丢弃。
- `message` 为空直接丢弃。
- `id` 优先取 `skyNetVo.getId()`，为空时生成 `UUID`。
- `cnt` 通常固定为 `1`。
- 字符串字段优先通过 `safe()` 兜底，数值字段保留原始数值类型。
- 列表字段为 `null` 或空集合时，整条消息直接丢弃。

## 命名规则

- `MessageModel`：`src/main/java/com/ly/tms/po/carSupply/SkynetLog{BizName}MessageModel.java`
- `Po`：`src/main/java/com/ly/tms/po/carSupply/SkynetLog{BizName}Po.java`
- `Job`：`src/main/java/com/ly/tms/job/Bus_{BizName}_KafkaToStarRock_{任务编号}.java`

配置键遵循 bethune 现有分组：

- topic key: `kafka.bus.{biz}.topic`
- group key: `travel.car.{biz}.group`
- StarRocks key: `starrocks.fe.travel.common.{tableKey}`
- Hive key: `hive.hive_train_ops.{tableKey}`

## 生成代码时的判断规则

- 用户给的是顶层字段 + 少量嵌套对象：按 34 模式写单行输出。
- 用户给的是 `datas`、`fullPriceList` 这类列表：按 35/36 模式在 `flatMap()` 中逐项展开。
- JSON 字段名与 Java 字段名不一致时，在 `MessageModel` 上补 `@JSONField(name = "...")`。
- 若参考任务里存在“嵌套字段优先，顶层字段兜底”的业务规则，保留该优先级，不要简化成单字段直取。

## 输出要求

完成后至少说明：

- 新增或修改了哪些文件
- 新增了哪些配置键
- 本次任务属于“单行模式”还是“列表展开模式”
- 是否完成编译验证

## 参考资料

读取 `references/bethune-patterns.md` 获取以下内容：

- 任务 33/34/35/36 的差异
- 任务 34 的完整骨架摘要
- `parseAndFormatLogTime()` 与 `toHiveRow()` 的固定模板
- 4 份配置文件中的插入分组位置
    cnt           INT,
    traceid       STRING,
    {其余字段按 PO 顺序}
)
PARTITIONED BY (year STRING, month STRING, day STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\001'
STORED AS TEXTFILE;
```

### StarRocks
```sql
CREATE TABLE TCTravelStreamData_db.{表名} (
    st            DATETIME,
    apmtraceid    VARCHAR(256),
    id            VARCHAR(256),
    cnt           INT,
    traceid       VARCHAR(256),
    {其余字段：STRING→VARCHAR(512), INT→INT, DOUBLE→DOUBLE}
)
DUPLICATE KEY(st, apmtraceid)
DISTRIBUTED BY HASH(id) BUCKETS 8
PROPERTIES ("replication_num" = "3");
```

---

## 参考示例（已实现任务）

| 任务 | 类名 | Topic | Module | List展开字段 | SR表名 |
|------|------|-------|--------|------------|--------|
| 33 | Bus_Search_Abtest_KafkaToStarRock_33 | skynet_log_Public_SFC_ABTest_Monitor | BUS_Public_SFC_ABTest_Monitor | 无 | bus_sfc_abtest_monitor |
| 34 | Bus_Search_ReplacePrice_KafkaToStarRock_34 | skynet_log_Public_SFC_Replace_Price_Monitor | BUS_Public_SFC_Replace_Price_Monitor | 无(ReferPriceBean嵌套) | bus_sfc_replace_price_monitor |
| 35 | Bus_Carpool_CalEnter_KafkaToStarRock_35 | skynet_log_3304590_CallEnter | BUS_PUBLIC_CARPOOL_PRICING_CallEnter | fullPriceList | bus_carpool_calenter_monitor |
| 36 | Bus_Metric_Collection_KafkaToStarRock_36 | skynet_log_3309435_bus_travelmetrics | BUS_METRIC_COLLECTION | datas | bus_metric_collection_monitor |
