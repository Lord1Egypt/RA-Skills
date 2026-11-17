# API 规范分析指引 | API Spec Analyzer

> 指导 AI 分析项目 API 设计规范，提取 `api-spec.md` 规范。

## 分析流程

1. **先读 `references/api-spec.md`** 了解条目编号
2. **读 `project_context.json`** 获取语言和框架信息；用 `exec` 搜索 API 文件位置（如 `Get-ChildItem -Path src/api -Recurse` 或 `find src/api -type f`），用 `read` 读关键 API 封装文件
3. **读关键 API 封装文件**（axios instance 创建 / request factory）
4. **写入 `.code-spec/api-spec.md`**

## 各条目分析要点

### RESTful 约定 [API-01 ~ API-03]

#### [API-01] URL 命名
- 用 `exec` 列出 `src/api/` 目录文件，用 `read` 抽样几个 API 调用文件，提取 URL 模式
- 是否有统一的 API 前缀（/api/v1）
- 资源命名：复数还是单数、下划线还是连字符

#### [API-02] HTTP 方法使用
- 统计 get/post/put/patch/delete 的使用模式
- 每个方法对应的操作类型
- 是否有自定义 method（如软删除用 post 还是 delete）

#### [API-03] 资源命名
- URL 路径段的命名风格
- 嵌套资源约定深度

### 请求格式 [API-04 ~ API-08]

#### [API-04] 请求头规范
- 读 axios 实例 / fetch 封装的默认 headers
- Content-Type 是否统一指定
- 语言头 / 版本头

#### [API-05] 请求体格式
- JSON / FormData / URLSearchParams 使用场景
- 请求体字段命名：camelCase vs snake_case
- 日期时间字段格式

#### [API-06] 分页参数
- 搜索 page/limit/offset/size/pageSize/pageNum
- 参数命名约定

#### [API-07] 筛选排序参数
- sort/sortBy/orderBy/order 参数格式
- 筛选参数的传递方式（query string / body）

#### [API-08] 文件上传规范
- multipart/form-data 使用方式
- 文件参数名约定（file/image/upload）
- 是否支持分片上传

### 响应格式 [API-09 ~ API-11]

#### [API-09] 成功响应结构
- 读响应拦截器/类型定义
- `{ code: 0, data, message }` vs `{ data, status }` vs 直接返回 data
- 列表接口的分页响应结构

#### [API-10] 错误响应结构
- 错误对象格式
- 业务错误码字段名（code/errorCode/errCode）

#### [API-11] HTTP 状态码
- 200/201/204/400/401/403/404/500 的使用场景
- 是否所有错误都返回 200 + 业务错误码

### 错误码体系 [API-12 ~ API-13]

#### [API-12] 业务错误码
- 搜索 code/errorCode/errCode 常量定义
- 错误码分类（用户/权限/数据/系统）

#### [API-13] 错误消息规范
- 后端返回还是前端映射
- 是否有多语言错误消息

### 工程化 [API-14 ~ API-18]

#### [API-14] API 文件组织
- 用 `exec` 列出 `src/api/` 目录结构（如 `Get-ChildItem -Path src/api -Recurse` 或 `find src/api -type f`）
- 按模块分文件 vs 集中一个文件 vs 按页面就近

#### [API-15] API 版本策略
- URL 版本号 / Header 版本 / 无版本
- 是否检测到旧版本 API

#### [API-16] 接口文档
- 搜索 Swagger/OpenAPI JSON 或 YAML 文件
- 是否有接口文档链接

#### [API-17] Base URL 配置
- 环境变量中的 API_BASE_URL / VITE_API_BASE
- 多环境代理配置

#### [API-18] 超时与重试
- axios 的 timeout 设置
- 请求重试逻辑（axios-retry / 自定义）

### 认证/鉴权 [API-19 ~ API-22]

#### [API-19] 认证方式
- JWT / OAuth / Cookie Session / API Key
- token 存储位置（localStorage / sessionStorage / cookie）
- 搜索 token/Token/Authorization/Bearer

#### [API-20] Token 传递与刷新
- 请求拦截器中如何注入 token
- refreshToken 刷新机制

#### [API-21] 请求拦截
- 读请求拦截器内容
- 附加的公共参数（时间戳/签名/设备信息）

#### [API-22] 响应拦截
- 读响应拦截器内容
- 统一错误处理逻辑
- 401 处理（跳转登录页）
- 重新登录后重新发请求（队列机制）
