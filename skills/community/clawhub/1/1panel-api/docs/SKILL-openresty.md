# OpenResty - 1Panel API

## 模块说明
OpenResty 模块接口

## 接口列表 (10 个)

---

### GET /openresty
**功能**: Load OpenResty conf
**说明**: 获取 OpenResty 完整配置文件

**参数**: 无

**返回**: NginxFile 对象

---

### GET /openresty/https
**功能**: Get default HTTPs status
**说明**: 获取默认 HTTPS 配置状态

**参数**: 无

**返回**: NginxConfigRes 对象

---

### GET /openresty/modules
**功能**: Get OpenResty modules
**说明**: 获取已安装的 OpenResty 模块列表

**参数**: 无

**返回**: NginxBuildConfig 对象

---

### GET /openresty/status
**功能**: Load OpenResty status info
**说明**: 获取 OpenResty 运行状态信息

**参数**: 无

**返回**: NginxStatus 对象

---

### POST /openresty/build
**功能**: Build OpenResty
**说明**: 编译构建 OpenResty

**参数 (NginxBuildReq)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| taskID | string | 是 | 任务ID，用于跟踪构建进度 | - |
| mirror | string | 是 | 镜像源地址 | - |

---

### POST /openresty/file
**功能**: Update OpenResty conf by upload file
**说明**: 通过上传文件方式更新 OpenResty 配置

**参数 (NginxConfigFileUpdate)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| content | string | 是 | 配置文件完整内容 | - |
| backup | bool | 否 | 是否在更新前备份原配置 | true/false |

---

### POST /openresty/https
**功能**: Operate default HTTPs
**说明**: 启用或禁用默认 HTTPS 配置

**参数 (NginxDefaultHTTPSUpdate)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| operate | string | 是 | 操作类型 | `enable`, `disable` |
| sslRejectHandshake | bool | 否 | 是否拒绝 SSL 握手 | true/false |

---

### POST /openresty/modules/update
**功能**: Update OpenResty module
**说明**: 创建、更新或删除 OpenResty 模块

**参数 (NginxModuleUpdate)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| operate | string | 是 | 操作类型 | `create`, `delete`, `update` |
| name | string | 是 | 模块名称 | - |
| script | string | 否 | 模块初始化脚本 | - |
| packages | string | 否 | 依赖包列表，多个包用空格分隔 | - |
| enable | bool | 否 | 是否启用该模块 | true/false |
| params | string | 否 | 模块额外参数 | - |

---

### POST /openresty/scope
**功能**: Load partial OpenResty conf
**说明**: 根据指定范围获取部分 OpenResty 配置

**参数 (NginxScopeReq)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| scope | NginxKey | 是 | 配置范围类型 | 见下方 NginxKey 取值 |
| websiteId | uint | 否 | 网站ID，范围为 website 时需要 | - |

**NginxKey 取值范围**:

| 值 | 说明 |
|----|------|
| `index` | 首页配置 |
| `limit-conn` | 连接限流配置 |
| `ssl` | SSL 证书配置 |
| `cache` | 缓存配置 |
| `http-per` | HTTP 性能配置 |
| `proxy-cache` | 代理缓存配置 |

---

### POST /openresty/update
**功能**: Update OpenResty conf
**说明**: 根据范围更新 OpenResty 配置

**参数 (NginxConfigUpdate)**:

| 字段 | 类型 | 必填 | 说明 | 取值范围 |
|------|------|------|------|----------|
| scope | NginxKey | 否 | 配置范围类型 | 同上 NginxKey 取值 |
| operate | string | 是 | 操作类型 | `add`, `update`, `delete` |
| websiteId | uint | 否 | 网站ID | - |
| params | interface{} | 否 | 具体参数值，类型根据 scope 而定 | - |

**scope 对应 params 结构**:

- `index`: 数组，如 `["index.php", "index.html"]`
- `limit-conn`: 对象，如 `{"limit_conn": 10, "limit_rate": 100}`
- `ssl`: 对象，如 `{"ssl_certificate": "/path/to/cert"}`
- `http-per`: 对象，如 `{"client_max_body_size": "100m", "keepalive_timeout": 60}`

---

## 枚举值参考

### NginxKey 范围键
```go
const (
    Index      NginxKey = "index"
    LimitConn  NginxKey = "limit-conn"
    SSL        NginxKey = "ssl"
    CACHE      NginxKey = "cache"
    HttpPer    NginxKey = "http-per"
    ProxyCache NginxKey = "proxy-cache"
)
```

### 操作类型 operate
- **模块操作**: `create`, `delete`, `update`
- **HTTPS操作**: `enable`, `disable`
- **配置操作**: `add`, `update`, `delete`

### 负载均衡算法
```go
var LBAlgorithms = map[string]struct{}{
    "ip_hash": {},    // IP 哈希
    "least_conn": {}, // 最少连接
}
```
