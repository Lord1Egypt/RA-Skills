# Bethune 任务模式参考

## 目录

- 任务族概览
- 任务34固定骨架
- 列表展开变体
- 配置键模式
- 实施检查清单

## 任务族概览

33 到 36 可以分成两类：

- 单行模式：33、34。每条 Kafka 消息通常产出一行 `Po`。
- 列表展开模式：35、36。消息中存在列表字段，`flatMap()` 逐项展开输出多行。

四个任务共享的不变量：

- `FlinkUtil.getFlinkEnv(60 * 1000L, false)`
- `KafkaSource<SkyNetVo>` + `SkyNetVoDeserialization`
- 仅在流上按 `module` 过滤，除非需求明确要求附加条件
- `parseAndFormatLogTime()` 统一把毫秒截断后按 `yyyy-MM-dd HH:mm:ss` 解析
- Hive sink 使用 `HiveSink.createHdfsSinkForString(path, Duration.ofMinutes(30), MemorySize.ofMebiBytes(512), DELIMITER)`
- Hive 行末尾追加 `year, month, day`
- `TableSchema` 顺序必须等于 `rowBuilder` 顺序，也必须等于 `toHiveRow()` 的业务字段顺序

## 任务34固定骨架

任务 34 是最适合复用的单行模板，核心特征如下：

- topic key: `kafka.bus.serch.c.replaceprice.topic`
- group key: `travel.car.serch.c.replaceprice.group`
- module 常量: `BUS_Public_SFC_Replace_Price_Monitor`
- StarRocks key: `starrocks.fe.travel.common.car_search_c_count_replaceprice`
- Hive key: `hive.hive_train_ops.car_search_c_count_replaceprice`

输出字段顺序：

1. `st`
2. `traceid`
3. `id`
4. `cnt`
5. `replacesuppliername`
6. `replacesuppliercode`
7. `priceratio`
8. `addamount`
9. `pricetype`
10. `calreferprice`
11. `replaceflag`

34 的关键业务规则：

- `referPrice.supplierName/supplierCode` 优先
- 若 `referPrice` 为空或内部字段为空，再回退到顶层 `referSupplierName/referSupplierCode`
- `replaceFlag` 输出到 `Po` 时转成 `Integer`：`true -> 1`, 其他情况 -> `0`

因此，若新任务存在“嵌套字段优先、顶层字段兜底”的语义，直接复用 34 的写法，不要省略分支。

## 列表展开变体

35 模式：

- 列表字段位于 `response.fullPriceList`
- 若 `response == null` 或列表为空，整条消息丢弃
- 同一条消息生成多个 `Po`，共享 `st/id/cnt/traceid` 等公共字段

36 模式：

- 列表字段位于顶层 `datas`
- 若 `datas == null` 或为空，整条消息丢弃
- 列表元素中的数值字段通常直接保留为 `Integer` / `Double`

当用户没有明确说“参考 35/36”，但消息结构中出现数组字段时，应主动切换到列表展开模式。

## 固定模板

`parseAndFormatLogTime()`：

```java
private static String parseAndFormatLogTime(SkyNetVo skyNetVo) {
    String logTime = skyNetVo.getLogTime();
    if (StringUtils.isBlank(logTime)) {
        LOG.error("任务{N}缺少logTime，按A方案丢弃。id={}, module={}, category={}, subCategory={}",
                skyNetVo.getId(), skyNetVo.getModule(), skyNetVo.getCategory(), skyNetVo.getSubCategory());
        return null;
    }
    String baseTime = logTime.contains(".") ? logTime.split("\\.")[0] : logTime;
    try {
        LocalDateTime dt = LocalDateTime.parse(baseTime, LOG_TIME_FORMATTER);
        return dt.format(LOG_TIME_FORMATTER);
    } catch (Exception ex) {
        LOG.error("任务{N}解析logTime失败，按A方案丢弃。id={}, logTime={}, message={}",
                skyNetVo.getId(), logTime, skyNetVo.getMessage(), ex);
        return null;
    }
}
```

`safe()`：

```java
private static String safe(String value) {
    return value == null ? "" : value;
}
```

`toHiveRow()` 尾部分区字段：

```java
String[] dateParts = row.getSt().split(" ")[0].split("-");
String year = dateParts.length > 0 ? dateParts[0] : "";
String month = dateParts.length > 1 ? dateParts[1] : "";
String day = dateParts.length > 2 ? dateParts[2] : "";
```

## 配置键模式

四个文件都要同步更新：

- `src/main/resources/config.properties`
- `src/main/resources/dev/config.properties`
- `src/main/resources/product/config.properties`
- `src/main/resources/stage/config.properties`

插入时保持 4 个区块分别有序：

- topic 区块
- group 区块
- `#starrocks table` 区块
- `#hive` 区块

34 在主配置中的相邻位置示例：

- topic 位于 `kafka.bus.serch.c.abtest.topic` 与 `kafka.bus.carpool.calenter.topic` 之间
- group 位于 `travel.car.serch.c.abtest.group` 与 `travel.car.carpool.calenter.group` 之间
- StarRocks 位于 `starrocks.fe.travel.common.car_search_c_count_abtest` 与 `starrocks.fe.travel.common.bus_carpool_calenter_monitor` 之间
- Hive 位于 `hive.hive_train_ops.car_search_c_count_abtest` 与 `hive.hive_train_ops.bus_carpool_calenter_monitor` 之间

通常遵循这些值模式：

- group value: `train_bethune_group_{topic}` 或在末尾追加业务后缀
- Hive value: `viewfs://dcfs/ns-traffic/dev/train_java_edison/hive_train_ops/{tableName}`
- StarRocks value: 通常等于实际表名

## 实施检查清单

- `MessageModel` 是否准确覆盖顶层字段、嵌套对象和列表元素
- `Po` 字段顺序是否与最终输出顺序一致
- `flatMap()` 是否正确处理空消息、空列表、嵌套回退逻辑
- `TableSchema`、`rowBuilder`、`toHiveRow()` 是否完全同序
- 4 份配置文件是否都已同步更新
- 若仓库可编译，是否执行 `mvn -DskipTests compile`