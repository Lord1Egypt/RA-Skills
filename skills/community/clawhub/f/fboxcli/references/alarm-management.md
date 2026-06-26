# 报警与联系人命令参考

## alarm list

列出 FBox 的报警条目配置。

```bash
fboxcli alarm list <BOX_ID> [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | long | 报警条目 ID |
| uid | long | 报警条目 UID |
| name | string | 报警名称 |
| alarmMsg | string? | 报警消息模板 |
| condition | string | 触发条件 |

---

## alarm history

获取报警历史记录。

```bash
fboxcli alarm history <BOX_ID> --begin <BEGIN> --end <END> [OPTIONS] [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |
| --begin | long | **是** | 开始时间（毫秒时间戳） |
| --end | long | **是** | 结束时间（毫秒时间戳） |
| --limit | int | 否 | 最大条数 |

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 报警名称 |
| alarmMsg | string | 报警消息 |
| triggeredAt | DateTime | 触发时间（UTC） |
| recoveredAt | DateTime? | 恢复时间（UTC） |
| confirmedAt | DateTime? | 确认时间（UTC） |

**示例：**

```bash
fboxcli alarm history 12345 --begin 1700000000000 --end 1700086400000 --json
```

---

## alarm confirm

确认（应答）一条报警。⚠️ 写操作，需用户确认。

```bash
fboxcli alarm confirm <UID>
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| UID | long | 是 | 报警条目 UID |

---

## alarm groups

列出 FBox 的报警分组及其关联联系人。

```bash
fboxcli alarm groups <BOX_ID> [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |

---

## alarm add-group

添加报警分组，可关联联系人。

```bash
fboxcli alarm add-group <BOX_ID> <NAME> [OPTIONS]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |
| NAME | string | 是 | 分组名称（20字以内） |
| --contacts | string | 否 | 逗号分隔的联系人 UID |

**示例：**

```bash
fboxcli alarm add-group 12345 "紧急报警" --contacts 4001,4002
```

---

## alarm delete-group

删除报警分组。⚠️ 需用户确认。

```bash
fboxcli alarm delete-group <BOX_ID> <UID>
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |
| UID | long | 是 | 报警分组 UID |

---

## alarm delete

删除报警条目。⚠️ 需用户确认。

```bash
fboxcli alarm delete <BOX_ID> --ids <IDS>
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| BOX_ID | long | 是 | FBox ID（数字） |
| --ids | string | 是 | 逗号分隔的报警条目 ID |

---

## contact list

列出所有报警联系人。

```bash
fboxcli contact list [--json]
```

**返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| uid | long | 联系人 UID |
| name | string | 联系人名称 |
| email | string? | 邮箱 |
| phone | string? | 手机号 |
| noticeType | enum | 通知类型：0=无, 1=短信, 2=语音, 3=短信+语音 |

---

## contact get

获取单个联系人详细信息。

```bash
fboxcli contact get <UID> [--json]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| UID | long | 是 | 联系人 UID |

---

## contact add

添加联系人。

```bash
fboxcli contact add <NAME> [OPTIONS]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| NAME | string | 是 | 联系人名称 |
| --email | string | 否 | 邮箱地址 |
| --phone | string | 否 | 手机号 |
| --notice-type | int | 否 | 通知类型：0=无, 1=短信, 2=语音, 3=短信+语音 [默认: 0] |

**示例：**

```bash
fboxcli contact add "张三" --phone 13800138000 --notice-type 1
```

---

## contact update

更新联系人信息。只需传入要修改的字段。

```bash
fboxcli contact update <UID> [OPTIONS]
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| UID | long | 是 | 联系人 UID |
| --name | string | 否 | 新名称 |
| --email | string | 否 | 新邮箱 |
| --phone | string | 否 | 新手机号 |

---

## contact delete

删除联系人。⚠️ 需用户确认。

```bash
fboxcli contact delete <UID>
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| UID | long | 是 | 联系人 UID |
