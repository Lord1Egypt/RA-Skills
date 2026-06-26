# ScriptLibrary, Command - 1Panel API

## 模块说明
ScriptLibrary, Command 模块接口

## 接口列表 (13 个)

---

### GET /core/commands/command
**功能**: List commands - 获取命令列表

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | 是 | 命令类型 | `redis`, `command` |

**请求体示例**:
```json
{
  "type": "command"
}
```

**响应参数**: 返回 `CommandInfo[]` 数组

---

### GET /core/commands/tree
**功能**: Tree commands - 获取命令树形结构

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | 是 | 命令类型 | `redis`, `command` |

**请求体示例**:
```json
{
  "type": "command"
}
```

**响应参数**: 返回 `CommandTree[]` 数组，包含树形结构

---

### POST /core/commands
**功能**: Create command - 创建快捷命令

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 否 | 命令ID（更新时必填） | - |
| type | string | 否 | 命令类型 | `redis`, `command` |
| groupID | uint | 否 | 分组ID | - |
| groupBelong | string | 否 | 所属分组名称 | - |
| name | string | 是 | 命令名称 | - |
| command | string | 是 | 命令内容 | - |

**请求体示例**:
```json
{
  "name": "查看进程",
  "command": "ps aux"
}
```

---

### POST /core/commands/del
**功能**: Delete command - 删除快捷命令

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ids | []uint | 是 | 要删除的命令ID数组 |

**请求体示例**:
```json
{
  "ids": [1, 2, 3]
}
```

---

### POST /core/commands/export
**功能**: Export command - 导出快捷命令

**请求参数**: 无

**响应参数**: 返回导出文件路径

---

### POST /core/commands/import
**功能**: Import command - 导入快捷命令

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| items | []CommandOperate | 是 | 命令列表 |

**CommandOperate 结构**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | uint | 否 | 命令ID |
| type | string | 否 | 命令类型 |
| groupID | uint | 否 | 分组ID |
| groupBelong | string | 否 | 所属分组 |
| name | string | 是 | 命令名称 |
| command | string | 是 | 命令内容 |

**请求体示例**:
```json
{
  "items": [
    {
      "name": "查看内存",
      "command": "free -h"
    }
  ]
}
```

---

### POST /core/commands/search
**功能**: Page commands - 分页查询命令

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| orderBy | string | 是 | 排序字段 | `name`, `command`, `createdAt` |
| order | string | 是 | 排序方式 | `null`, `ascending`, `descending` |
| groupID | uint | 否 | 分组ID | - |
| type | string | 是 | 命令类型 | `redis`, `command` |
| info | string | 否 | 搜索关键词 | - |

**请求体示例**:
```json
{
  "page": 1,
  "pageSize": 10,
  "orderBy": "createdAt",
  "order": "descending",
  "type": "command"
}
```

**响应参数**: 返回分页结果 `PageResult` { total: int64, items: []CommandInfo }

---

### POST /core/commands/update
**功能**: Update command - 更新快捷命令

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 命令ID | - |
| type | string | 否 | 命令类型 | `redis`, `command` |
| groupID | uint | 否 | 分组ID | - |
| groupBelong | string | 否 | 所属分组名称 | - |
| name | string | 是 | 命令名称 | - |
| command | string | 是 | 命令内容 | - |

**请求体示例**:
```json
{
  "id": 1,
  "name": "更新后的命令名称",
  "command": "updated command"
}
```

---

### POST /core/script
**功能**: Add script - 添加脚本

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | uint | 否 | 脚本ID（更新时必填） |
| isInteractive | bool | 否 | 是否交互式脚本 |
| name | string | 是 | 脚本名称 |
| script | string | 是 | 脚本内容 |
| groups | string | 否 | 所属分组（多个用逗号分隔） |
| description | string | 否 | 脚本描述 |

**请求体示例**:
```json
{
  "name": "备份脚本",
  "script": "#!/bin/bash\necho 'backup'",
  "description": "用于备份的脚本"
}
```

---

### POST /core/script/del
**功能**: Delete script - 删除脚本

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| ids | []uint | 是 | 要删除的脚本ID数组 |

**请求体示例**:
```json
{
  "ids": [1, 2, 3]
}
```

---

### POST /core/script/search
**功能**: Page script - 分页查询脚本

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | int | 是 | 页码 |
| pageSize | int | 是 | 每页数量 |
| groupID | uint | 否 | 分组ID |
| info | string | 否 | 搜索关键词 |

**请求体示例**:
```json
{
  "page": 1,
  "pageSize": 10,
  "info": "备份"
}
```

**响应参数**: 返回分页结果 `PageResult` { total: int64, items: []ScriptInfo }

---

### POST /core/script/sync
**功能**: Sync script - 同步远程脚本

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| taskID | string | 是 | 任务ID |

**请求体示例**:
```json
{
  "taskID": "sync-123"
}
```

---

### POST /core/script/update
**功能**: Update script - 更新脚本

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | uint | 是 | 脚本ID |
| isInteractive | bool | 否 | 是否交互式脚本 |
| name | string | 是 | 脚本名称 |
| script | string | 是 | 脚本内容 |
| groups | string | 否 | 所属分组 |
| description | string | 否 | 脚本描述 |

**请求体示例**:
```json
{
  "id": 1,
  "name": "更新后的脚本名称",
  "script": "#!/bin/bash\necho 'updated'",
  "description": "更新后的描述"
}
```

---

## 公共类型定义

### PageInfo
分页信息
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 是 | 页码，从1开始 |
| pageSize | int | 是 | 每页记录数 |

### PageResult
分页结果
| 字段 | 类型 | 说明 |
|------|------|------|
| total | int64 | 总记录数 |
| items | interface{} | 数据列表 |

### CommandInfo
命令信息
| 字段 | 类型 | 说明 |
|------|------|------|
| id | uint | 命令ID |
| groupID | uint | 分组ID |
| name | string | 命令名称 |
| type | string | 命令类型 |
| command | string | 命令内容 |
| groupBelong | string | 所属分组 |

### CommandTree
命令树结构
| 字段 | 类型 | 说明 |
|------|------|------|
| label | string | 显示名称 |
| value | string | 值 |
| children | []CommandTree | 子节点 |

### ScriptInfo
脚本信息
| 字段 | 类型 | 说明 |
|------|------|------|
| id | uint | 脚本ID |
| name | string | 脚本名称 |
| isInteractive | bool | 是否交互式 |
| lable | string | 标签 |
| script | string | 脚本内容 |
| groupList | []uint | 分组ID列表 |
| groupBelong | []string | 所属分组名称列表 |
| isSystem | bool | 是否系统脚本 |
| description | string | 脚本描述 |
| createdAt | time.Time | 创建时间 |
