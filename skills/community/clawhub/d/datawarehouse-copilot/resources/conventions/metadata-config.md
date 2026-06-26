# 元数据获取方式配置

> 本文件是五种元数据获取方式的唯一定义来源，Phase 1 元数据收集阶段查阅此文件选择采集方式。

根据实际环境选择合适的 `source_type`，各方式可组合使用。

---

## 目录

- [方式 A：manual — 手动提供](#方式-a-manual--手动提供)
- [方式 B：jdbc — 数据库直连](#方式-b-jdbc--数据库直连)
- [方式 C：openapi — OpenAPI 接口](#方式-c-openapi--openapi-接口)
- [方式 D：web — 前端元数据页面](#方式-d-web--前端元数据页面)
- [方式 E：hdfs — HDFS 路径文件](#方式-e-hdfs--hdfs-路径文件)

---

## 方式 A：manual — 手动提供

用户直接粘贴表结构、字段信息、业务说明等文本内容，无需额外配置。适合快速验证或少量表场景。

```yaml
metadata:
  source_type: manual
```

**注意事项**
- 粘贴内容建议包含：表名、字段名、数据类型、字段注释、分区信息
- 内容格式不限（DDL / JSON / 自然语言均可），Agent 会自动解析

---

## 方式 B：jdbc — 数据库直连

通过 JDBC 连接数据库，自动查询 `information_schema` 采集元数据。

```yaml
metadata:
  source_type: jdbc
  jdbc:
    host: 10.0.0.1            # 必填：数据库主机地址
    port: 10000               # 必填：端口号
    database: ods             # 必填：目标数据库名
    username: ${DW_JDBC_USER} # 必填：用户名（建议使用环境变量）
    password: ${DW_JDBC_PASS} # 必填：密码（建议使用环境变量）
    driver: hive2             # 可选：驱动类型，默认 hive2
    tables:                   # 可选：指定采集的表，留空则采集整库
      - user_order
      - user_profile
    collect:                  # 可选：采集内容，默认全部
      - columns
      - partitions
      - table_comment
      - column_comment
      - storage_format
      - row_count
```

**字段说明**

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| host | ✅ | — | 数据库主机地址或 IP |
| port | ✅ | — | 数据库端口号 |
| database | ✅ | — | 目标数据库（Schema）名 |
| username | ✅ | — | 连接用户名 |
| password | ✅ | — | 连接密码 |
| driver | ❌ | `hive2` | JDBC 驱动类型 |
| tables | ❌ | 空（采集整库） | 指定采集的表名列表 |
| collect | ❌ | 全部 | 采集内容项列表 |

**采集 SQL**

```sql
-- Step 1: 列举相关数据库
SHOW DATABASES;

-- Step 2: 获取目标库下所有表
SELECT table_name, table_comment, create_time, table_rows
FROM information_schema.tables
WHERE table_schema = '{target_database}';

-- Step 3: 获取字段详情
SELECT
  table_name, column_name, ordinal_position,
  data_type, character_maximum_length,
  is_nullable, column_default, column_comment
FROM information_schema.columns
WHERE table_schema = '{target_database}'
  AND table_name IN ({relevant_tables})
ORDER BY table_name, ordinal_position;
```

Hive 环境补充查询：
```sql
SHOW PARTITIONS {table_name};
DESCRIBE FORMATTED {table_name};
```

**注意事项**
- 确保运行环境已安装对应 JDBC 驱动包
- 网络需与数据库主机连通，防火墙放行对应端口
- 账号需具备 `information_schema` 的 SELECT 权限
- 敏感字段（username / password）建议通过环境变量传入，避免明文写入配置文件

---

## 方式 C：openapi — OpenAPI 接口

调用平台提供的标准 OpenAPI 接口，通过 AK/SK 鉴权获取元数据。

```yaml
metadata:
  source_type: openapi
  openapi:
    host: https://meta.example.com   # 必填：API 服务地址（含协议）
    api_path: /api/v1/metadata/tables # 必填：接口路径
    ak: ${META_API_AK}               # 必填：Access Key
    sk: ${META_API_SK}               # 必填：Secret Key
    method: GET                      # 可选：请求方法，默认 GET
    headers:                         # 可选：附加请求头
      X-Tenant-Id: default
    tables:                          # 可选：过滤指定表，留空则获取全部
      - user_order
      - product_info
```

**字段说明**

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| host | ✅ | — | API 服务地址，含协议（http/https） |
| api_path | ✅ | — | 接口路径 |
| ak | ✅ | — | Access Key（建议使用环境变量） |
| sk | ✅ | — | Secret Key（建议使用环境变量） |
| method | ❌ | `GET` | HTTP 请求方法 |
| headers | ❌ | 空 | 附加 HTTP 请求头（键值对） |
| tables | ❌ | 空（获取全部） | 过滤指定表名列表 |

**注意事项**
- AK/SK 属于敏感凭证，**必须**通过环境变量传入，禁止明文写入配置文件或代码仓库
- 接口需返回可解析的结构化数据（JSON 格式），响应中须包含表名、字段名、字段类型等基础信息
- 若接口使用签名鉴权（如 HMAC-SHA256），需确认签名算法与平台文档一致

---

## 方式 D：web — 前端元数据页面

请求前端元数据页面或数据接口地址，解析返回的结构化元数据。适用于仅有页面入口、无法直连数据库的场景。

```yaml
metadata:
  source_type: web
  web:
    url: https://data-portal.example.com/meta/tables # 必填：页面或 API 地址
    auth_type: token   # 必填：鉴权方式，支持 token / cookie / none
    token: ${WEB_META_TOKEN}  # 条件必填：auth_type=token 时必填
    cookie: "session=xxx; csrf=yyy"  # 条件必填：auth_type=cookie 时必填
    tables:            # 可选：过滤指定表，留空则获取全部
      - user_order
```

**字段说明**

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| url | ✅ | — | 目标页面或 API 地址（含协议） |
| auth_type | ✅ | — | 鉴权方式：`token` / `cookie` / `none` |
| token | 条件必填（auth_type=token） | — | Bearer Token 或 API Token |
| cookie | 条件必填（auth_type=cookie） | — | 完整 Cookie 字符串 |
| tables | ❌ | 空（获取全部） | 过滤指定表名列表 |

**注意事项**
- 目标地址必须返回**结构化元数据**（JSON），纯 HTML 渲染页面无法解析
- token / cookie 属于敏感凭证，建议通过环境变量传入
- 注意认证信息的有效期，Cookie/Token 过期后需重新获取
- 若存在跨域限制，需确保请求端与目标服务在同一网络或已配置 CORS

---

## 方式 E：hdfs — HDFS 路径文件

读取存储在 HDFS 路径下的元数据文件，支持多种文件格式。

```yaml
metadata:
  source_type: hdfs
  hdfs:
    hdfs_path: /data/metadata/source-tables.json  # 必填：HDFS 文件或目录路径
    file_format: json     # 必填：文件格式，支持 json / csv / parquet / orc
    namenode: hdfs://namenode.example.com:8020    # 必填：NameNode 地址
    kerberos:             # 可选：Kerberos 认证配置（非 Kerberos 环境忽略）
      principal: dw_user@EXAMPLE.COM
      keytab: /etc/security/keytabs/dw_user.keytab
```

**字段说明**

| 字段 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| hdfs_path | ✅ | — | HDFS 上的文件路径或目录路径 |
| file_format | ✅ | — | 文件格式：`json` / `csv` / `parquet` / `orc` |
| namenode | ✅ | — | NameNode 服务地址（含协议和端口） |
| kerberos | ❌ | 空（不启用） | Kerberos 认证配置，整体可选 |
| kerberos.principal | 条件必填（启用 kerberos） | — | Kerberos 主体名称 |
| kerberos.keytab | 条件必填（启用 kerberos） | — | keytab 文件的本地路径 |

**注意事项**
- Kerberos 环境下需确保运行环境已安装 `krb5` 并正确配置 `krb5.conf`
- 确认运行账号对 `hdfs_path` 具有读取权限
- 若 `hdfs_path` 为目录，将递归读取目录下所有符合 `file_format` 的文件
- parquet / orc 格式需要对应的解析依赖库
