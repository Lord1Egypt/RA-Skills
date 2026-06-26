---
name: "basic-integration-guide"
description: "指导开发者如何接入basic基础服务，包括依赖引入、gRPC调用、REST API使用、配置说明。涵盖国际化(i18n)、项目管理、租户管理、字典管理、存储、认证等核心能力"
---

# Basic 基础服务接入指南

## 1. 服务概述

Basic 是畅远飞轮平台的基础服务，提供以下核心能力：

- **国际化 (i18n)**：词条空间管理、词条翻译、多语言发布、导入导出（JSON/CSV/Excel）
- **项目管理**：项目与应用实体管理、项目-应用关联与语言配置
- **租户管理**：多租户创建、配置、域名绑定
- **字典管理**：字典项目/模块/分组/字典项的 CRUD、版本发布与回滚、草稿对比、资产导入导出
- **存储服务**：虚拟存储操作（OSS / CopyParty 适配）
- **内部认证**：OIDC 认证、JWT 验证

接口协议：gRPC + REST API

## 2. 快速接入

### 2.1 Maven 依赖

**轻量客户端（仅接口定义和 DTO）：**
```xml
<dependency>
    <groupId>com.ginlong</groupId>
    <artifactId>basic-client</artifactId>
    <version>1.0.0-SNAPSHOT</version>
</dependency>
```

**gRPC 接口包（含 Protobuf Stub）：**
```xml
<dependency>
    <groupId>com.ginlong</groupId>
    <artifactId>basic-grpc-interface</artifactId>
    <version>1.0.0-SNAPSHOT</version>
</dependency>
```

### 2.2 gRPC 客户端配置

在调用方的 `application.yaml` 中配置 gRPC 通道：

```yaml
grpc:
  client:
    basic-grpc-server:
      address: 'dns:///basic-service:9090'
      negotiationType: plaintext
      enableKeepAlive: true
      keepAliveTime: 30s
      keepAliveTimeout: 5s
```

注入 gRPC Stub 示例：

```java
@GrpcClient("basic-grpc-server")
private I18nServiceGrpc.I18nServiceBlockingStub i18nStub;

@GrpcClient("basic-grpc-server")
private ProjectServiceGrpc.ProjectServiceBlockingStub projectStub;

@GrpcClient("basic-grpc-server")
private TenantServiceGrpc.TenantServiceBlockingStub tenantStub;
```

### 2.3 认证与租户上下文

REST API 调用时需传递以下 Header：

| Header | 说明 | 必填 |
|--------|------|------|
| X-TENANT | 租户编码 | 是 |
| X-UID | 用户ID | 视接口而定 |
| Authorization | Bearer Token (OIDC) | 认证接口必填 |

gRPC 调用时通过 Metadata 传递：

```java
Metadata metadata = new Metadata();
metadata.put(Metadata.Key.of("X-TENANT", Metadata.ASCII_STRING_MARSHALLER), tenantCode);
metadata.put(Metadata.Key.of("X-UID", Metadata.ASCII_STRING_MARSHALLER), userId);
```

## 3. gRPC 服务接口

### 3.1 I18nService

**包名：** `com.ginlong.basic.grpc.i18n`

| RPC 方法 | 请求类型 | 响应类型 | 说明 |
|----------|----------|----------|------|
| findProject | FindProjectReqPB | FindProjectRespPB | 查询项目应用信息 |
| searchTermSpaces | SearchTermSpacesReqPB | SearchTermSpacesRespPB | 搜索词条空间 |
| findTermSpace | FindTermSpaceReqPB | TermSpaceRespPB | 查询词条空间详情 |
| createTermSpace | CreateTermSpaceReqPB | CreateTermSpaceRespPB | 创建词条空间 |
| deleteTermSpace | DeleteTermSpaceReqPB | DeleteTermSpaceRespPB | 删除词条空间 |
| publishTermSpace | PublishTermSpaceReqPB | PublishTermSpaceRespPB | 发布词条空间 |
| importTermSpace | ImportTermSpaceReqPB | ImportTermSpaceRespPB | 导入词条空间 |
| exportTermSpace | ExportTermSpaceReqPB | ExportTermSpaceRespPB | 导出词条空间 |
| searchTerms | SearchTermsReqPB | SearchTermsRespPB | 搜索词条 |
| findTerm | FindTermReqPB | TermRespPB | 查询词条详情 |
| saveTerm | SaveTermReqPB | SaveTermRespPB | 保存词条 |
| deleteTerm | DeleteTermReqPB | DeleteTermRespPB | 删除词条 |

**关键 Message 定义：**

```protobuf
// 查询项目应用
message FindProjectReqPB {
  string projectCode = 1;  // 项目编码（必填）
  string appCode = 2;      // 应用编码（必填）
}

message FindProjectRespPB {
  string projectCode = 1;
  string appCode = 12;
  string name = 2;
  string description = 3;
  string defaultLangCode = 4;           // 默认语言编码
  repeated string supportLangCodes = 5; // 支持的语言编码列表
  google.protobuf.Struct extraProps = 6;
  google.protobuf.Struct langCodeNameMap = 7; // 语言编码-名称映射
}

// 搜索词条
message SearchTermsReqPB {
  string projectCode = 1;
  string appCode = 12;
  string spaceCode = 2;     // 词条空间编码
  string codeLike = 3;      // 编码模糊匹配
  string codeEqual = 8;     // 编码精确匹配
  string contentLike = 4;   // 内容模糊匹配
  int32 size = 5;           // 每页大小
  int32 pageInx = 6;        // 页码
  repeated string codeLikes = 7; // 批量编码模糊匹配
}

// 词条响应
message TermRespPB {
  string projectCode = 1;
  string appCode = 12;
  string spaceCode = 2;
  string code = 3;
  google.protobuf.Struct content = 4;     // 多语言内容 {langCode: text}
  int64 gmtPublished = 5;                 // 发布时间戳
  int64 gmtSaved = 6;                     // 保存时间戳
  google.protobuf.Struct extraProps = 7;
}

// 导入方法枚举
enum ImportMethodEnumPb {
  UNKNOWN_IMP_METHOD = 0;
  RESET_AND_APPEND = 1;          // 清空后追加
  APPEND_AND_OVERWRITE = 2;      // 追加并覆盖已有
  APPEND_AND_NOT_OVERWRITE = 3;  // 追加但不覆盖已有
}

// 导入导出格式枚举
enum ImportExportTypeEnumPB {
  UNKNOWN_IMP_EXP_TYPE = 0;
  JSON = 1;
  CVS = 2;
  XLS = 3;
}
```

**调用示例：**

```java
// 搜索词条
SearchTermsReqPB req = SearchTermsReqPB.newBuilder()
    .setProjectCode("my-project")
    .setAppCode("web")
    .setSpaceCode("common")
    .setSize(20)
    .setPageInx(0)
    .build();
SearchTermsRespPB resp = i18nStub.searchTerms(req);
```

<!-- PLACEHOLDER_SECTION_3_2 -->

### 3.2 ProjectService

**包名：** `com.ginlong.basic.grpc.project`

| RPC 方法 | 请求类型 | 响应类型 | 说明 |
|----------|----------|----------|------|
| findProject | FindProjectReqPB | ProjectRespPB | 查询项目详情 |
| searchProjects | SearchProjectsReqPB | SearchProjectsRespPB | 搜索项目列表 |
| findProjectApp | FindProjectAppReqPB | ProjectAppRespPB | 查询项目应用详情 |
| searchProjectApps | SearchProjectAppsReqPB | SearchProjectAppsRespPB | 搜索项目应用列表 |

**关键 Message 定义：**

```protobuf
message FindProjectReqPB {
  string projectCode = 1;  // 项目编码（必填）
}

message ProjectRespPB {
  string code = 1;
  string name = 2;
  string note = 3;
  google.protobuf.Struct publicProp = 4;    // 公开属性
  google.protobuf.Struct internalProp = 5;  // 内部属性
}

message FindProjectAppReqPB {
  string projectCode = 1;  // 项目编码（必填）
  string code = 2;         // 应用编码（必填）
}

message ProjectAppRespPB {
  string code = 1;
  string projectCode = 2;
  string name = 3;
  string note = 4;
  string endType = 5;            // 端类型
  repeated string endTag = 6;    // 端标签
  bool isDefault = 7;            // 是否默认应用
  bool isVirtual = 8;            // 是否虚拟应用
  google.protobuf.Struct publicProp = 9;
  google.protobuf.Struct internalProp = 10;
}
```

**调用示例：**

```java
// 查询项目
FindProjectReqPB req = FindProjectReqPB.newBuilder()
    .setProjectCode("my-project")
    .build();
ProjectRespPB resp = projectStub.findProject(req);
```

### 3.3 TenantService

**包名：** `com.ginlong.basic.grpc.tenant`

| RPC 方法 | 请求类型 | 响应类型 | 说明 |
|----------|----------|----------|------|
| findTenant | FindTenantReqPB | TenantRespPB | 按编码查询租户 |
| findTenantByHost | FindTenantByHostReqPB | TenantRespPB | 按域名查询租户 |

**关键 Message 定义：**

```protobuf
message FindTenantReqPB {
  string tenantCode = 1;  // 租户编码（必填）
}

message FindTenantByHostReqPB {
  string host = 1;  // 域名（必填）
}

message TenantRespPB {
  string code = 1;
  string name = 2;
  repeated string hosts = 3;          // 绑定域名列表
  string countryRegionCode = 4;       // 国家/地区编码
  int32 status = 5;                   // 状态
  google.protobuf.Struct contactInfo = 6; // 联系信息
  repeated TenantConfRespPB confs = 7;    // 租户配置列表
}

message TenantConfRespPB {
  string tenantCode = 1;
  string projectCode = 2;
  string bizType = 3;      // 业务类型
  string confKey = 4;      // 配置键
  string confValue = 5;    // 配置值
  int32 isPrivate = 6;     // 是否私有
  int32 status = 7;
  string note = 8;
}
```

**调用示例：**

```java
// 按域名查询租户
FindTenantByHostReqPB req = FindTenantByHostReqPB.newBuilder()
    .setHost("app.example.com")
    .build();
TenantRespPB resp = tenantStub.findTenantByHost(req);
```

<!-- PLACEHOLDER_SECTION_4 -->

## 4. REST API 接口

### 4.1 国际化管理 (i18n)

**基础路径前缀：** `internal/i18nmng-api/`

#### 语言管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `lang` | 查看语言列表 |
| POST | `lang` | 创建语言 |
| PUT | `lang/{langCode}` | 更新语言 |
| DELETE | `lang/{langCode}` | 删除语言 |

#### 项目应用管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `project/app` | 项目应用列表 |
| POST | `project/app` | 创建项目应用 |
| GET | `project/{projectCode}/app/{appCode}` | 获取项目应用详情 |
| PUT | `project/{projectCode}/app/{appCode}` | 更新项目应用 |
| DELETE | `project/{projectCode}/app/{appCode}` | 删除项目应用 |

#### 词条空间管理

**基础路径：** `internal/i18nmng-api/project/{projectCode}/app/{appCode}/termspace`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `page` | 词条空间分页搜索 |
| GET | `{spaceCode}` | 查询词条空间详情 |
| POST | `` | 创建词条空间 |
| POST | `copy` | 拷贝词条空间 |
| PUT | `{code}` | 更新词条空间 |
| DELETE | `{spaceCode}` | 删除词条空间 |
| POST | `{spaceCode}/action/publish` | 发布词条空间 |
| GET | `{spaceCode}/action/publish` | 查看发布历史 |
| DELETE | `{spaceCode}/action/publish` | 删除发布历史 |
| GET | `{spaceCode}/version/diff` | 发布差异对比 |
| PUT | `{spaceCode}/reset` | 重置词条空间 |
| PUT | `{spaceCode}/import` | 导入词条（multipart） |
| GET | `{spaceCode}/export/json` | 导出词条（JSON） |
| GET | `{spaceCode}/export` | 导出词条（文件下载） |

#### 词条管理

**基础路径：** `internal/i18nmng-api/project/{projectCode}/app/{appCode}/termspace/{spaceCode}/term`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `` | 词条分页搜索 |
| POST | `` | 创建词条 |
| PUT | `{termCode}` | 更新词条 |
| DELETE | `{termCode}` | 删除词条 |

#### 生产使用接口（无需 internal 前缀）

**基础路径：** `i18nmng-api/project/termspace`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `package/export/file` | 对象存储词条文件导出（项目打包用） |
| GET | `project/{projectCode}/app/{appCode}/lang` | 列出项目相关语言 |
| GET | `project/{projectCode}/app/{appCode}/translation/version` | 词条空间最新版本和语言信息 |

**curl 示例：**

```bash
# 搜索词条空间
curl -X GET 'http://basic-service/internal/i18nmng-api/project/my-project/app/web/termspace/page?size=20&pageInx=0' \
  -H 'X-TENANT: tenant001'

# 创建词条
curl -X POST 'http://basic-service/internal/i18nmng-api/project/my-project/app/web/termspace/common/term' \
  -H 'Content-Type: application/json' \
  -H 'X-TENANT: tenant001' \
  -d '{"code":"btn.submit","content":{"zh_CN":"提交","en_US":"Submit"}}'

# 获取翻译版本信息（生产使用）
curl -X GET 'http://basic-service/i18nmng-api/project/termspace/project/my-project/app/web/translation/version' \
  -H 'X-TENANT: tenant001'
```

<!-- PLACEHOLDER_SECTION_4_2 -->

### 4.2 项目管理

**基础路径前缀：** `project-api/project`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `` | 搜索项目列表 |
| GET | `app` | 搜索项目应用列表 |

**curl 示例：**

```bash
curl -X GET 'http://basic-service/project-api/project' \
  -H 'X-TENANT: tenant001'
```

### 4.3 租户管理

**基础路径前缀：** `internal/tenant-api/`

#### 租户 CRUD

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `tenant` | 创建租户 |
| GET | `tenant/page` | 分页查询租户列表 |
| GET | `tenant/{code}` | 按编码查询租户详情 |
| PUT | `tenant/{id}` | 更新租户 |
| DELETE | `tenant/{id}` | 删除租户（级联删除配置） |

#### 租户配置

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `tenant-conf` | 创建租户配置 |
| GET | `tenant-conf/page` | 分页查询租户配置 |
| PUT | `tenant-conf/{id}` | 更新租户配置 |
| DELETE | `tenant-conf/{id}` | 删除租户配置 |

**curl 示例：**

```bash
# 按编码查询租户
curl -X GET 'http://basic-service/internal/tenant-api/tenant/tenant001' \
  -H 'X-TENANT: tenant001'

# 创建租户配置
curl -X POST 'http://basic-service/internal/tenant-api/tenant-conf' \
  -H 'Content-Type: application/json' \
  -H 'X-TENANT: tenant001' \
  -d '{"tenantCode":"tenant001","projectCode":"proj1","bizType":"config","confKey":"theme","confValue":"dark"}'
```

### 4.4 字典管理

#### 字典项目管理

**基础路径：** `dictionary-api/project`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `` | 创建字典项目 |
| GET | `/page` | 分页查询字典项目列表 |
| DELETE | `/{id}` | 删除字典项目 |

#### 字典模块管理

**基础路径：** `internal/dictionary-api/module`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `` | 创建字典模块 |
| GET | `/page` | 分页查询字典模块列表 |
| PUT | `/{id}` | 更新字典模块 |
| DELETE | `/{id}` | 删除字典模块 |

#### 字典分组管理

**基础路径：** `internal/dictionary-api/group`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `` | 创建字典分组 |
| GET | `/page` | 分页查询字典分组列表 |
| GET | `/{groupCode}` | 按编码查询分组详情（含字典项） |
| PUT | `/{id}` | 更新字典分组 |
| DELETE | `/{id}` | 删除字典分组（级联删除字典项） |
| POST | `/{groupCode}/module` | 关联分组到模块 |
| DELETE | `/{groupCode}/module/{moduleCode}` | 解除分组与模块关联 |
| GET | `/by-module/{moduleCode}` | 按模块查询关联分组列表 |

#### 字典项管理

**基础路径：** `internal/dictionary-api/item`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `` | 创建字典项 |
| POST | `/batch` | 批量创建字典项 |
| PUT | `/{id}` | 更新字典项 |
| PUT | `/batch` | 批量更新字典项 |
| DELETE | `/{id}` | 删除字典项（递归删除子节点） |
| PUT | `/{id}/enable` | 启用字典项 |
| PUT | `/{id}/disable` | 禁用字典项 |

#### 字典统一查询（生产使用）

**基础路径：** `dictionary-api/query`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `` | 统一查询接口，读取已发布版本数据，支持 `projectCode@versionNumber` 格式增量更新 |

#### 字典发布版本管理

**基础路径：** `internal/dictionary-api/publish`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/project` | 查询已发布过的项目列表 |
| POST | `/{projectCode}` | 发布项目字典 |
| POST | `/{projectCode}/rollback/{versionNumber}` | 回滚到指定版本 |
| GET | `/{projectCode}/version` | 分页查询版本历史 |
| GET | `/{projectCode}/version/{versionNumber}` | 查询版本详情 |

#### 字典草稿对比

**基础路径：** `internal/dictionary-api/diff`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/{projectCode}` | 查询草稿与最新发布版本的差异 |

#### 字典资产管理

**基础路径：** `internal/dictionary-api/asset`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/{projectCode}/export` | 导出字典资产 |
| POST | `/{projectCode}/import` | 导入字典资产 |
| DELETE | `/{projectCode}/draft` | 清空草稿资产 |

**curl 示例：**

```bash
# 统一查询字典（生产使用）
curl -X GET 'http://basic-service/dictionary-api/query?projectCodes=proj1&groupCodes=gender,status' \
  -H 'X-TENANT: tenant001'

# 发布字典
curl -X POST 'http://basic-service/internal/dictionary-api/publish/proj1' \
  -H 'Content-Type: application/json' \
  -H 'X-TENANT: tenant001' \
  -d '{"remark":"v2 release"}'

# 查询草稿差异
curl -X GET 'http://basic-service/internal/dictionary-api/diff/proj1' \
  -H 'X-TENANT: tenant001'
```

### 4.5 内部认证

**基础路径前缀：** `internal/auth-api/`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `user/info` | 获取用户信息（需 Authorization Header） |
| GET | `route/info` | 获取路由信息 |

**curl 示例：**

```bash
curl -X GET 'http://basic-service/internal/auth-api/user/info' \
  -H 'Authorization: Bearer <token>'
```

<!-- PLACEHOLDER_SECTION_5 -->

## 5. 客户端 SDK 接口

`basic-client` 模块提供以下 ClientService 接口，供域内服务直接依赖调用。

### 5.1 I18n 域

**I18nTermClientService** — 词条管理
- `searchTerms(SearchTermsQuery)` → `SearchTermsDto`
- `findTerm(FindTermQuery)` → `TermDto`
- `saveTerm(SaveTermCmd)` → `SaveTermDto`
- `deleteTerm(DeleteTermCmd)` → `DeleteTermDto`

**I18nLangClientService** — 语言管理
- `listLangs(ListLangQuery)` → `ListLangDto`
- `saveLang(SaveLangCmd)` → `SaveLangDto`
- `deleteLang(DeleteLangCmd)` → `DeleteLangDto`

**I18nTermSpaceClientService** — 词条空间管理
- `searchTermSpaces(SearchTermSpacesQuery)` → `SearchTermSpacesDto`
- `findTermSpace(FindTermSpaceQuery)` → `TermSpaceDto`
- `saveTermSpace(SaveTermSpaceCmd)` → `SaveTermSpaceDto`
- `copyTermSpace(CopyTermSpaceCmd)` → `CopyTermSpaceDto`
- `deleteTermSpace(DeleteTermSpaceCmd)` → `DeleteTermSpaceDto`
- `publishTermSpace(PublishTermSpaceCmd)` → `PublishTermSpaceDto`
- `importTerms(ImportTermsCmd)` → `ImportTermsDto`
- `exportTerms(ExportTermsQuery)` → `ExportTermsDto`
- `exportFile(ExportFileCmd)` → `ExportFileDto`
- `translationVersion(TranslationVersionQuery)` → `TranslationVersionDto`
- 更多方法见源码

**I18nProjectAppClientService** — 项目应用管理
- `findProjectApp(FindProjectAppQuery)` → `ProjectAppDto`
- `listProjectApps(ListProjectAppsQuery)` → `ListProjectAppsDto`
- `saveProjectApp(SaveProjectAppCmd)` → `SaveProjectAppDto`
- `deleteProjectApp(DeleteProjectAppCmd)` → `DeleteProjectsAppDto`
- `listProjectAppSupportLang(ListProjectAppSupportLang)` → `List<SimpleLangDto>`

### 5.2 Project 域

**ProjectClientService** — 项目管理
- `search(ProjectSearchDto)` → `List<ProjectDto>`

**ProjectAppClientService** — 项目应用管理
- `search(ProjectAppSearchDto)` → `List<ProjectAppDto>`
- `find(ProjectAppFindDto)` → `ProjectAppDto`

### 5.3 Tenant 域

**TenantClientService** — 租户查询
- `findByCode(String tenantCode)` → `TenantDto`
- `findByHost(String host)` → `TenantDto`

**TenantManageService** — 租户管理
- `create(TenantDto)` → `TenantDto`
- `update(Long id, ...)` → `TenantDto`
- `delete(Long id)` → `void`
- `findByCode(String code)` → `TenantDto`
- `search(String name, int page, int size)` → `SearchTenantsDto`

**TenantConfManageService** — 租户配置管理
- `create(TenantConfDto)` → `TenantConfDto`
- `update(Long id, TenantConfDto)` → `TenantConfDto`
- `delete(Long id)` → `void`
- `search(String tenantCode, String projectCode, String bizType, int page, int size)` → `SearchTenantConfsDto`

### 5.4 Dictionary 域

**DictionaryProjectClientService** — 字典项目
- `create(String projectCode)` → `DictionaryProjectDto`
- `delete(Long id)` → `void`
- `page(int page, int size)` → `SearchDictionaryProjectsDto`

**DictionaryModuleClientService** — 字典模块
- `create(DictionaryModuleDto)` → `DictionaryModuleDto`
- `update(Long id, String moduleName, String description)` → `DictionaryModuleDto`
- `delete(Long id)` → `void`
- `search(String projectCode, String moduleName, int page, int size)` → `SearchDictionaryModulesDto`

**DictionaryGroupClientService** — 字典分组
- `create(DictionaryGroupDto)` → `DictionaryGroupDto`
- `update(Long id, String groupName, String type, String description)` → `DictionaryGroupDto`
- `delete(Long id)` → `void`
- `findByGroupCode(String projectCode, String groupCode)` → `DictionaryGroupDto`
- `search(String projectCode, String groupName, int page, int size)` → `SearchDictionaryGroupsDto`
- `bindModule(String groupCode, String moduleCode)` → `void`
- `unbindModule(String groupCode, String moduleCode)` → `void`

**DictionaryItemClientService** — 字典项
- `create(DictionaryItemDto)` → `DictionaryItemDto`
- `batchCreate(List<DictionaryItemDto>)` → `List<DictionaryItemDto>`
- `update(Long id, DictionaryItemDto)` → `DictionaryItemDto`
- `batchUpdate(List<DictionaryItemDto>)` → `List<DictionaryItemDto>`
- `delete(Long id)` → `void`
- `setEnabled(Long id, boolean enabled)` → `void`

**DictionaryQueryClientService** — 字典查询
- `query(List<String> projectCodes, List<String> moduleCodes, List<String> groupCodes)` → `Map<String, DictionaryGroupDataDto>`
- `queryPublished(...)` → `Map<String, ProjectQueryDataDto>`

**DictionaryPublishClientService** — 字典发布
- `publish(String projectCode, String remark)` → `DictionaryPublishVersionDto`
- `rollback(String projectCode, int targetVersionNumber)` → `DictionaryPublishVersionDto`
- `listVersions(String projectCode, int page, int size)` → `SearchPublishVersionsDto`
- `getVersionDetail(String projectCode, int versionNumber)` → `DictionaryPublishVersionDto`
- `getActiveVersionNumber(String projectCode)` → `Integer`
- `listPublishedProjects()` → `List<ProjectPublishSummaryDto>`

**DictionaryDiffClientService** — 字典对比
- `diff(String projectCode)` → `DiffResult`

**DictionaryAssetClientService** — 字典资产
- `export(String projectCode, Integer versionNumber)` → `ExportPackage`
- `importAsset(String projectCode, ExportPackage, boolean strictParent)` → `ImportResultDto`
- `clearDraft(String projectCode)` → `ClearResultDto`

### 5.5 Storage 域

**PhysicalStorageOperationClientService** — 物理存储操作
- `upload(String bucketName, String key, Map<String, String> metadata, InputStream inputStream)` → `void`
- `deleteBatch(String bucketName, String keyPrefix)` → `void`
- `exist(String bucketName, List<String> keys)` → `Map<String, Boolean>`

## 6. 配置参考

### 6.1 必填配置

| 环境变量 | 说明 | 示例 |
|----------|------|------|
| K8S_ALL_REDIS_HOST | Redis 主机 | `redis.svc` |
| K8S_ALL_REDIS_PORT | Redis 端口 | `6379` |
| K8S_ALL_REDIS_PASSWORD | Redis 密码 | - |
| K8S_ALL_REDIS_DB | Redis 数据库 | `0` |
| K8S_ALL_MYSQL_HOST | MySQL 主机 | `mysql.svc` |
| K8S_ALL_MYSQL_PORT | MySQL 端口 | `3306` |
| K8S_BASIC_MYSQL_USERNAME | MySQL 用户名 | `basic` |
| K8S_BASIC_MYSQL_PASSWORD | MySQL 密码 | - |

### 6.2 可选配置

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| K8S_BASIC_MYSQL_DATABASE | MySQL 数据库名 | `basic` |
| K8S_ALL_MYSQL_POOL_SIZE_IDLE | 连接池最小空闲 | `1` |
| K8S_ALL_MYSQL_POOL_SIZE_MAX | 连接池最大连接 | `10` |
| K8S_ALL_MID_COPYPARTY_ENABLED | CopyParty 存储开关 | `true` |

### 6.3 存储配置（按需）

| 环境变量 | 说明 |
|----------|------|
| K8S_ALL_STORAGE_OSS_ENABLED | OSS 存储开关 |
| K8S_ALL_STORAGE_OSS_ENDPOINT | OSS 端点 |
| K8S_ALL_STORAGE_OSS_KEY | OSS Access Key |
| K8S_ALL_STORAGE_OSS_SECRET | OSS Access Secret |
| K8S_ALL_MID_COPYPARTY_ADDR | CopyParty 地址 |
| K8S_ALL_MID_COPYPARTY_PREFIX | CopyParty 路径前缀 |
| K8S_ALL_MID_COPYPARTY_USER | CopyParty 用户名 |
| K8S_ALL_MID_COPYPARTY_PASS | CopyParty 密码 |

### 6.4 i18n 存储配置

| 环境变量 | 说明 |
|----------|------|
| K8S_BASIC_I18N_STORAGE_CDN_HOST | i18n CDN 域名 |
| K8S_BASIC_I18N_STORAGE_BUCKET_HOST | i18n 存储桶名 |

### 6.5 OIDC 认证配置

| 环境变量 | 说明 |
|----------|------|
| K8S_BASIC_OIDC_CLIENT_ID | OIDC 客户端 ID |
| K8S_BASIC_OIDC_CLIENT_SECRET | OIDC 客户端密钥 |
| K8S_BASIC_OIDC_PROVIDER_ADDR | OIDC 提供者地址 |

## 7. 最佳实践

- **超时配置**：gRPC 调用建议设置 5s 超时，导入导出等大文件操作可放宽至 30s
- **重试策略**：查询类接口可安全重试（幂等），写入类接口需确认幂等性后再重试
- **缓存策略**：租户信息、项目信息变更频率低，建议本地缓存 5 分钟；字典查询接口支持版本号增量更新，利用 `projectCode@versionNumber` 格式减少全量拉取
- **多租户**：所有请求必须携带 `X-TENANT` Header，gRPC 通过 Metadata 传递
