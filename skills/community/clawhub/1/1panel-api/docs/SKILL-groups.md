# System Group - 1Panel API

## 模块说明
System Group 模块接口，用于管理系统中的分组（如网站分组、主机分组、命令分组等）

## Group Type 取值范围
- `website` - 网站分组
- `host` - 主机分组
- `command` - 命令分组
- `script` - 脚本分组
- `cronjob` - 定时任务分组

## 接口列表 (8 个)

---

### POST /core/groups
**功能**: Create group (Core 创建分组)
**说明**: 创建一个新的分组

**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 否 | 分组ID（创建时通常不传，由系统自动生成） | - |
| name | string | **是** | 分组名称 | 最大长度根据实际业务 |
| type | string | **是** | 分组类型 | `website`, `host`, `command`, `script`, `cronjob` |

---

### POST /core/groups/del
**功能**: Delete group (Core 删除分组)
**说明**: 根据ID删除指定分组

**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | **是** | 分组ID | 有效的分组记录ID |

---

### POST /core/groups/search
**功能**: List groups (Core 查询分组列表)
**说明**: 根据类型查询分组列表

**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| type | string | **是** | 分组类型 | `website`, `host`, `command`, `script`, `cronjob` |

**返回**: `GroupInfo[]`
| 字段 | 类型 | 说明 |
|------|------|------|
| id | uint | 分组ID |
| name | string | 分组名称 |
| type | string | 分组类型 |
| isDefault | bool | 是否为默认分组 |

---

### POST /core/groups/update
**功能**: Update group (Core 更新分组)
**说明**: 更新指定分组的信息

**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | **是** | 分组ID | 有效的分组记录ID |
| name | string | 否 | 分组名称（更新时可选） | 最大长度根据实际业务 |
| type | string | **是** | 分组类型 | `website`, `host`, `command`, `script`, `cronjob` |
| isDefault | bool | 否 | 是否设为默认分组 | `true`, `false` |

---

### POST /groups
**功能**: Create group (Agent 创建分组)
**说明**: 创建一个新的分组（Agent端接口）

**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | 否 | 分组ID（创建时通常不传，由系统自动生成） | - |
| name | string | **是** | 分组名称 | 最大长度根据实际业务 |
| type | string | **是** | 分组类型 | `website`, `host`, `command`, `script`, `cronjob` |

---

### POST /groups/del
**功能**: Delete group (Agent 删除分组)
**说明**: 根据ID删除指定分组（Agent端接口）

**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | **是** | 分组ID | 有效的分组记录ID |

---

### POST /groups/search
**功能**: List groups (Agent 查询分组列表)
**说明**: 根据类型查询分组列表（Agent端接口）

**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| type | string | **是** | 分组类型 | `website`, `host`, `command`, `script`, `cronjob` |

**返回**: `GroupInfo[]`
| 字段 | 类型 | 说明 |
|------|------|------|
| id | uint | 分组ID |
| name | string | 分组名称 |
| type | string | 分组类型 |
| isDefault | bool | 是否为默认分组 |

---

### POST /groups/update
**功能**: Update group (Agent 更新分组)
**说明**: 更新指定分组的信息（Agent端接口）

**参数 (Body)**:
| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| id | uint | **是** | 分组ID | 有效的分组记录ID |
| name | string | 否 | 分组名称（更新时可选） | 最大长度根据实际业务 |
| type | string | **是** | 分组类型 | `website`, `host`, `command`, `script`, `cronjob` |
| isDefault | bool | 否 | 是否设为默认分组 | `true`, `false` |

---

## DTO 结构参考

### GroupCreate (创建分组)
```go
type GroupCreate struct {
    ID   uint   `json:"id"`
    Name string `json:"name" validate:"required"`
    Type string `json:"type" validate:"required"`
}
```

### OperateByID (删除分组)
```go
type OperateByID struct {
    ID uint `json:"id" validate:"required"`
}
```

### GroupSearch / OperateByType (查询分组)
```go
type GroupSearch struct {
    Type string `json:"type" validate:"required"`
}

type OperateByType struct {
    Type string `json:"type"`
}
```

### GroupUpdate (更新分组)
```go
type GroupUpdate struct {
    ID        uint   `json:"id"`
    Name      string `json:"name"`
    Type      string `json:"type" validate:"required"`
    IsDefault bool   `json:"isDefault"`
}
```

### GroupInfo (分组信息)
```go
type GroupInfo struct {
    ID        uint   `json:"id"`
    Name      string `json:"name"`
    Type      string `json:"type"`
    IsDefault bool   `json:"isDefault"`
}
```
