# 历史数据命令参考

## 数据层级

```
设备(BOX_ID) → 历史记录条目(ItemName) → 通道(ChannelId) → 时间序列(Timestamp + Value)
```

查询历史数据需先通过 `history list` 获取条目配置和通道 ID。

---

## history list

列出 FBox 的历史记录条目配置。

```bash
fboxcli history list <BOX_ID> [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | long | 条目 ID |
| name | string | 条目名称 |
| sampleType | enum | 采样类型：Cycle（周期）/ Trigger（触发） |
| channels | array | 通道列表，每个通道包含 id 和 name |

**示例：**

```bash
fboxcli history list 12345 --json
```

---

## history query

查询历史记录数据。支持不同粒度和时间范围。

```bash
fboxcli history query --ids <IDS> --begin <BEGIN> --end <END> [OPTIONS] [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --ids | string | **是** | 逗号分隔的通道 ID |
| --begin | long | **是** | 开始时间（毫秒时间戳） |
| --end | long | **是** | 结束时间（毫秒时间戳） |
| --granularity | int | 否 | 粒度：0=原始, 1=分钟, 2=小时, 3=天 [默认: 0] |
| --limit | int | 否 | 最大条数，最大 1000 [默认: 100] |
| --tz | string | 否 | 时区字符串 |

**返回字段（每条记录）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| timestamp | long | 时间戳（毫秒） |
| value | object | 数据值 |

**粒度说明：**

| 值 | 含义 | 适用场景 |
|----|------|---------|
| 0 | 原始数据 | 短时间范围精确查看 |
| 1 | 分钟聚合 | 数小时范围趋势 |
| 2 | 小时聚合 | 数天范围趋势 |
| 3 | 天聚合 | 数月范围趋势 |

**示例：**

```bash
# 查询原始数据
fboxcli history query --ids 2001,2002 --begin 1700000000000 --end 1700003600000 --json

# 按小时粒度，限制50条
fboxcli history query --ids 2001 --begin 1700000000000 --end 1700086400000 \
  --granularity 2 --limit 50 --json
```

---

## history delete

删除历史记录条目。⚠️ 需用户确认。

```bash
fboxcli history delete <BOX_ID> --ids <IDS>
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |
| --ids | string | 是 | 逗号分隔的条目 ID |

**示例：**

```bash
fboxcli history delete 12345 --ids 2001,2002
```
