# 统一写组命令参考

统一写组允许将多个设备的监控点绑定为一组，实现跨设备批量写入同一值。

---

## control list

列出所有统一写组。

```bash
fboxcli control list [--json]
```

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | long | 写组 ID |
| uid | long | 写组 UID |
| name | string | 写组名称 |
| type | enum | 数据类型 |
| options | array | 关联的监控点列表 |

---

## control get

获取单个统一写组的详细信息。

```bash
fboxcli control get <GROUP_ID> [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| GROUP_ID | long | 是 | 写组 ID |

---

## control add

通过 JSON 数据添加统一写组。

```bash
fboxcli control add '<JSON_DATA>'
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| JSON_DATA | string | 是 | JSON 格式的分组定义 |

**JSON 结构：**

```json
{
  "name": "温度控制组",
  "type": 7,
  "controlOptions": [
    {
      "bn": "FB001234",
      "dgn": "默认分组",
      "dn": "目标温度",
      "alias": "车间1号"
    }
  ]
}
```

| 字段 | 说明 |
|------|------|
| name | 写组名称 |
| type | 数据类型编号 |
| controlOptions[].bn | FBox 序列号 |
| controlOptions[].dgn | 监控点分组名 |
| controlOptions[].dn | 监控点名称 |
| controlOptions[].alias | 设备别名 |

---

## control delete

删除统一写组。⚠️ 需用户确认。

```bash
fboxcli control delete --ids <IDS>
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --ids | string | 是 | 逗号分隔的写组 ID |

---

## control write

向统一写组写入值。⚠️ 写操作，需用户确认。

```bash
fboxcli control write --value <VALUE> [OPTIONS]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --uid | long | 二选一 | 写组 UID |
| --name | string | 二选一 | 写组名称 |
| --value | string | **是** | 要写入的值 |

**示例：**

```bash
# 按 UID 写值
fboxcli control write --uid 6001 --value 100

# 按名称写值
fboxcli control write --name "温度控制组" --value 75.5

# 写入布尔值
fboxcli control write --uid 6001 --value true
```
