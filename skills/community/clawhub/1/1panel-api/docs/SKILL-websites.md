# Website, Website Domain, Website Nginx, Website PHP - 1Panel API

## 模块说明
Website, Website Domain, Website Nginx, Website PHP 模块接口，提供网站创建、配置、反向代理、SSL 证书等功能。

## 文件路径说明

### 网站目录结构

| 路径类型 | 说明 | 默认位置 |
|----------|------|----------|
| **网站根目录** | 网站静态文件存放目录 | `/opt/1panel/www/sites/{网站名称}/index` |
| **网站配置目录** | Nginx 配置文件目录 | `/opt/1panel/sites/{网站名称}/conf` |
| **网站日志目录** | 访问日志、错误日志 | `/opt/1panel/sites/{网站名称}/log` |
| **SSL 证书目录** | SSL 证书存放目录 | `/opt/1panel/sites/{网站名称}/ssl` |

### 网站目录变量

| 变量 | 说明 | 示例 |
|------|------|------|
| 网站名称 | 创建网站时指定的名称 | `myblog`、`shop` |
| 网站类型 | static/php/go/node/python/java | `static` 表示静态网站 |

### 常见路径示例

| 网站 | 类型 | 根目录 | Nginx 配置 | 日志 |
|------|------|--------|------------|------|
| myblog | static | `/opt/1panel/www/sites/myblog/index` | `/opt/1panel/sites/myblog/conf/nginx.conf` | `/opt/1panel/sites/myblog/log` |
| shop | php | `/opt/1panel/www/sites/shop/index` | `/opt/1panel/sites/shop/conf/nginx.conf` | `/opt/1panel/sites/shop/log` |

### 关键 API 参数

| API | 参数 | 说明 |
|-----|------|------|
| POST /websites | siteDir | 网站根目录 |
| POST /websites/dir/update | siteDir | 更新网站目录 |
| POST /websites/config/update | - | 更新 Nginx 配置 |

## 接口列表 (63 个)

### POST /websites/search
**功能**: Page websites - 分页查询网站列表
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| page | int | 是 | 页码 | - |
| pageSize | int | 是 | 每页数量 | - |
| name | string | 否 | 网站名称搜索 | - |
| orderBy | string | 是 | 排序字段 | primary_domain/type/status/createdAt/expire_date/created_at/favorite |
| order | string | 是 | 排序方式 | null/ascending/descending |
| websiteGroupId | uint | 否 | 网站分组ID | - |
| type | string | 否 | 网站类型 | static/php/go/node/python/java |

---

### GET /websites/list
**功能**: List websites - 获取所有网站列表
**参数**: 无

---

### POST /websites/options
**功能**: List website names - 获取网站名称列表（用于下拉选择）
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| types | []string | 否 | 网站类型过滤 | static/php/go/node/python/java |

---

### POST /websites
**功能**: Create website - 创建网站
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | 是 | 网站类型 | static/php/go/node/python/java |
| alias | string | 是 | 网站别名 | - |
| remark | string | 否 | 备注 | - |
| proxy | string | 否 | 代理配置 | - |
| websiteGroupId | uint | 是 | 网站分组ID | - |
| ipv6 | bool | 否 | 是否启用IPv6 | true/false |
| domains | []WebsiteDomain | 否 | 域名列表 | - |
| appType | string | 否 | 应用类型 | new/installed |
| appInstall | NewAppInstall | 否 | 新应用安装配置 | - |
| appId | uint | 否 | 已安装应用ID | - |
| appInstallId | uint | 否 | 已安装应用实例ID | - |
| runtimeId | uint | 否 | 运行时ID | - |
| taskId | string | 否 | 任务ID | - |
| parentWebsiteId | uint | 否 | 父网站ID（用于子站） | - |
| siteDir | string | 否 | 网站目录 | - |
| proxyType | string | 否 | 代理类型 | - |
| port | int | 否 | 端口号 | - |
| ftpUser | string | 否 | FTP用户名 | - |
| ftpPassword | string | 否 | FTP密码 | - |
| createDb | bool | 否 | 是否创建数据库 | true/false |
| dbName | string | 否 | 数据库名称 | - |
| dbUser | string | 否 | 数据库用户名 | - |
| dbPassword | string | 否 | 数据库密码 | - |
| dbHost | string | 否 | 数据库主机 | - |
| dbFormat | string | 否 | 数据库格式 | - |
| enableSSL | bool | 否 | 是否启用SSL | true/false |
| websiteSSLId | uint | 否 | SSL证书ID | - |
| streamPorts | string | 否 | 流端口 | - |
| name | string | 否 | 名称 | - |
| algorithm | string | 否 | 算法 | - |
| udp | bool | 否 | 是否UDP | true/false |
| servers | []NginxUpstreamServer | 否 | 上游服务器列表 | - |

**WebsiteDomain 子结构**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| domain | string | 是 | 域名 | - |
| port | int | 否 | 端口 | 默认80 |
| ssl | bool | 否 | 是否启用SSL | true/false |

---

### POST /websites/operate
**功能**: Operate website - 网站操作（启动/停止/重启）
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 网站ID | - |
| operate | string | 是 | 操作类型 | start/stop/reload |

---

### POST /websites/del
**功能**: Delete website - 删除网站
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 网站ID | - |
| deleteApp | bool | 否 | 是否删除关联应用 | true/false |
| deleteBackup | bool | 否 | 是否删除备份 | true/false |
| forceDelete | bool | 否 | 是否强制删除 | true/false |
| deleteDB | bool | 否 | 是否删除数据库 | true/false |

---

### POST /websites/update
**功能**: Update website - 更新网站基本信息
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 网站ID | - |
| primaryDomain | string | 是 | 主域名 | - |
| remark | string | 否 | 备注 | - |
| websiteGroupId | uint | 否 | 网站分组ID | - |
| expireDate | string | 否 | 过期日期 | - |
| ipv6 | bool | 否 | 是否启用IPv6 | true/false |
| favorite | bool | 否 | 是否收藏 | true/false |

---

### GET /websites/:id
**功能**: Search website by id - 根据ID获取网站详情
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | path | 是 | 网站ID | - |

---

### GET /websites/:id/config/:type
**功能**: Search website nginx by id - 获取网站Nginx配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | path | 是 | 网站ID | - |
| type | path | 是 | 配置类型 | nginx |

---

### POST /websites/config
**功能**: Load nginx conf - 加载Nginx配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| scope | string | 是 | 配置范围 | index/ssl/cache/limit-conn/proxy-cache/http-per |
| websiteId | uint | 否 | 网站ID | - |

---

### POST /websites/config/update
**功能**: Update nginx conf - 更新Nginx配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| scope | string | 否 | 配置范围 | index/ssl/cache/limit-conn/proxy-cache/http-per |
| operate | string | 是 | 操作类型 | add/update/delete |
| websiteId | uint | 否 | 网站ID | - |
| params | interface{} | 否 | 配置参数 | - |

---

### GET /websites/:id/https
**功能**: Load https conf - 获取网站HTTPS配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | path | 是 | 网站ID | - |

---

### POST /websites/:id/https
**功能**: Update https conf - 更新网站HTTPS配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| enable | bool | 是 | 是否启用 | true/false |
| websiteSSLId | uint | 否 | SSL证书ID | - |
| type | string | 否 | SSL类型 | existed/auto/manual |
| privateKey | string | 否 | 私钥（手动） | - |
| certificate | string | 否 | 证书（手动） | - |
| privateKeyPath | string | 否 | 私钥路径（导入） | - |
| certificatePath | string | 否 | 证书路径（导入） | - |
| importType | string | 否 | 导入类型 | - |
| httpConfig | string | 否 | HTTP配置 | HTTPSOnly/HTTPAlso/HTTPToHTTPS |
| SSLProtocol | []string | 否 | SSL协议版本 | - |
| algorithm | string | 否 | 算法 | - |
| hsts | bool | 否 | 是否启用HSTS | true/false |
| hstsIncludeSubDomains | bool | 否 | HSTS包含子域名 | true/false |
| httpsPorts | []int | 否 | HTTPS端口列表 | - |
| http3 | bool | 否 | 是否启用HTTP3 | true/false |

---

### POST /websites/check
**功能**: Check before create website - 创建前检查
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| installIds | []uint | 否 | 安装ID列表 | - |

---

### POST /websites/nginx/update
**功能**: Update website nginx conf - 更新网站Nginx配置文件
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 网站ID | - |
| content | string | 是 | Nginx配置内容 | - |

---

### POST /websites/log
**功能**: Operate website log - 操作网站日志
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 网站ID | - |
| operate | string | 是 | 操作类型 | - |
| logType | string | 是 | 日志类型 | - |
| page | int | 否 | 页码 | - |
| pageSize | int | 否 | 每页数量 | - |

---

### POST /websites/default/server
**功能**: Change default server - 修改默认站点
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 网站ID | - |

---

### POST /websites/php/version
**功能**: Update php version - 更换PHP版本
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| runtimeId | uint | 否 | 运行时ID | - |

---

### POST /websites/rewrite
**功能**: Get rewrite conf - 获取伪静态配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| name | string | 是 | 伪静态规则名称 | - |

---

### POST /websites/rewrite/update
**功能**: Update rewrite conf - 更新伪静态配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| name | string | 是 | 伪静态规则名称 | - |
| content | string | 否 | 伪静态规则内容 | - |

---

### POST /websites/rewrite/custom
**功能**: Operate custom rewrite - 操作自定义伪静态
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| operate | string | 是 | 操作类型 | create/delete |
| content | string | 否 | 伪静态内容 | - |
| name | string | 否 | 规则名称 | - |

---

### GET /websites/rewrite/custom
**功能**: List custom rewrite - 获取自定义伪静态列表
**参数**: 无

---

### POST /websites/dir/update
**功能**: Update Site Dir - 更新网站目录
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 网站ID | - |
| siteDir | string | 是 | 网站目录路径 | - |

---

### POST /websites/dir/permission
**功能**: Update Site Dir permission - 更新网站目录权限
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 网站ID | - |
| user | string | 是 | 用户 | - |
| group | string | 是 | 用户组 | - |

---

### POST /websites/dir
**功能**: Get website dir - 获取网站目录配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 网站ID | - |

---

### POST /websites/proxies
**功能**: Get proxy conf - 获取反向代理配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 网站ID | - |

---

### POST /websites/proxies/update
**功能**: Update proxy conf - 更新反向代理配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 反向代理ID | - |
| operate | string | 是 | 操作类型 | create/update/delete |
| enable | bool | 否 | 是否启用 | true/false |
| cache | bool | 否 | 是否缓存 | true/false |
| cacheTime | int | 否 | 缓存时间 | - |
| cacheUnit | string | 否 | 缓存时间单位 | - |
| serverCacheTime | int | 否 | 服务器缓存时间 | - |
| serverCacheUnit | string | 否 | 服务器缓存时间单位 | - |
| name | string | 是 | 代理名称 | - |
| modifier | string | 否 | 修饰符 | - |
| match | string | 是 | 匹配规则 | - |
| proxyPass | string | 是 | 代理目标地址 | - |
| proxyHost | string | 是 | 代理主机头 | - |
| content | string | 否 | 代理配置内容 | - |
| filePath | string | 否 | 配置文件路径 | - |
| replaces | map[string]string | 否 | 替换规则 | - |
| sni | bool | 否 | 是否启用SNI | true/false |
| proxySSLName | string | 否 | 代理SSL名称 | - |
| cors | bool | 否 | 是否启用CORS | true/false |
| allowOrigins | string | 否 | 允许的来源 | - |
| allowMethods | string | 否 | 允许的方法 | - |
| allowHeaders | string | 否 | 允许的头部 | - |
| allowCredentials | bool | 否 | 允许凭证 | true/false |
| preflight | bool | 否 | 预检请求 | true/false |

---

### POST /websites/proxies/file
**功能**: Update proxy file - 更新反向代理配置文件
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| content | string | 是 | 代理配置内容 | - |
| name | string | 是 | 代理名称 | - |

---

### POST /websites/proxy/config
**功能**: update website proxy cache config - 更新代理缓存配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| open | bool | 否 | 是否启用缓存 | true/false |
| cacheLimit | int | 是 | 缓存限制 | - |
| cacheLimitUnit | string | 是 | 缓存限制单位 | - |
| shareCache | int | 是 | 共享缓存大小 | - |
| shareCacheUnit | string | 是 | 共享缓存单位 | - |
| cacheExpire | int | 是 | 缓存过期时间 | - |
| cacheExpireUnit | string | 是 | 缓存过期单位 | - |

---

### GET /websites/proxy/config/:id
**功能**: Get website proxy cache config - 获取代理缓存配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | path | 是 | 网站ID | - |

---

### POST /websites/proxy/clear
**功能**: Clear Website proxy cache - 清理代理缓存
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |

---

### POST /websites/auths
**功能**: Get AuthBasic conf - 获取网站Basic认证配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |

---

### POST /websites/auths/update
**功能**: Update AuthBasic conf - 更新网站Basic认证配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| operate | string | 是 | 操作类型 | - |
| username | string | 否 | 用户名 | - |
| password | string | 否 | 密码 | - |
| remark | string | 否 | 备注 | - |

---

### POST /websites/auths/path
**功能**: Get AuthBasic path conf - 获取网站目录Basic认证配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |

---

### POST /websites/auths/path/update
**功能**: Update AuthBasic path conf - 更新网站目录Basic认证配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| operate | string | 是 | 操作类型 | - |
| name | string | 否 | 目录名称 | - |
| username | string | 否 | 用户名 | - |
| password | string | 否 | 密码 | - |
| path | string | 否 | 目录路径 | - |
| remark | string | 否 | 备注 | - |

---

### GET /websites/cors/:id
**功能**: Get CORS Config - 获取CORS配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | path | 是 | 网站ID | - |

---

### POST /websites/cors/update
**功能**: Update CORS Config - 更新CORS配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| cors | bool | 否 | 是否启用CORS | true/false |
| allowOrigins | string | 否 | 允许的来源 | - |
| allowMethods | string | 否 | 允许的方法 | - |
| allowHeaders | string | 否 | 允许的头部 | - |
| allowCredentials | bool | 否 | 允许凭证 | true/false |
| preflight | bool | 否 | 预检请求 | true/false |

---

### POST /websites/leech
**功能**: Get AntiLeech conf - 获取防盗链配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |

---

### POST /websites/leech/update
**功能**: Update AntiLeech - 更新防盗链配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| extends | string | 否 | 扩展名 | - |
| returnCode | string | 否 | 返回状态码 | - |
| enable | bool | 否 | 是否启用 | true/false |
| serverNames | []string | 否 | 允许的域名 | - |
| cache | bool | 否 | 是否缓存 | true/false |
| cacheTime | int | 否 | 缓存时间 | - |
| cacheUnit | string | 否 | 缓存时间单位 | - |
| noneRef | bool | 否 | 无Referer | true/false |
| logEnable | bool | 否 | 启用日志 | true/false |
| blocked | bool | 否 | 是否阻止 | true/false |

---

### POST /websites/redirect/update
**功能**: Update redirect conf - 更新重定向配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| name | string | 是 | 重定向名称 | - |
| websiteId | uint | 是 | 网站ID | - |
| domains | []string | 否 | 域名列表 | - |
| keepPath | bool | 否 | 是否保留路径 | true/false |
| enable | bool | 否 | 是否启用 | true/false |
| type | string | 是 | 重定向类型 | - |
| redirect | string | 是 | 重定向目标 | - |
| path | string | 否 | 路径 | - |
| target | string | 是 | 目标URL | - |
| operate | string | 是 | 操作类型 | - |
| redirectRoot | bool | 否 | 是否重定向根目录 | true/false |

---

### POST /websites/redirect
**功能**: Get redirect conf - 获取重定向配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |

---

### POST /websites/redirect/file
**功能**: Update redirect file - 更新重定向配置文件
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| content | string | 是 | 重定向配置内容 | - |
| name | string | 是 | 重定向名称 | - |

---

### GET /websites/default/html/:type
**功能**: Get default html - 获取默认页面
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | path | 是 | 页面类型 | - |

---

### POST /websites/default/html/update
**功能**: Update default html - 更新默认页面
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| type | string | 是 | 页面类型 | - |
| content | string | 是 | 页面内容 | - |
| sync | bool | 否 | 是否同步 | true/false |

---

### GET /websites/:id/lbs
**功能**: Get website upstreams - 获取网站负载均衡配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | path | 是 | 网站ID | - |

---

### POST /websites/lbs/create
**功能**: Create website upstream - 创建负载均衡
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| name | string | 是 | 负载均衡名称 | - |
| algorithm | string | 否 | 算法 | - |
| servers | []NginxUpstreamServer | 否 | 上游服务器列表 | - |

**NginxUpstreamServer 子结构**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| server | string | 是 | 服务器地址 | - |
| weight | int | 否 | 权重 | 默认1 |
| failTimeout | int | 否 | 失败超时时间 | - |
| failTimeoutUnit | string | 否 | 失败超时单位 | - |
| maxFails | int | 否 | 最大失败次数 | - |
| maxConns | int | 否 | 最大连接数 | - |
| flag | string | 否 | 标记 | - |

---

### POST /websites/lbs/del
**功能**: Delete website upstream - 删除负载均衡
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| name | string | 是 | 负载均衡名称 | - |

---

### POST /websites/lbs/update
**功能**: Update website upstream - 更新负载均衡
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| name | string | 是 | 负载均衡名称 | - |
| algorithm | string | 否 | 算法 | - |
| servers | []NginxUpstreamServer | 否 | 上游服务器列表 | - |

---

### POST /websites/lbs/file
**功能**: Update website upstream file - 更新负载均衡配置文件
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| name | string | 是 | 负载均衡名称 | - |
| content | string | 是 | 配置文件内容 | - |

---

### POST /websites/realip/config
**功能**: Set Real IP - 设置真实IP配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| open | bool | 否 | 是否启用 | true/false |
| ipFrom | string | 否 | IP来源 | - |
| ipHeader | string | 否 | IP头部 | - |
| ipOther | string | 否 | 其他IP | - |

---

### GET /websites/realip/config/:id
**功能**: Get Real IP Config - 获取真实IP配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | path | 是 | 网站ID | - |

---

### GET /websites/resource/:id
**功能**: Get website resource - 获取网站资源使用情况
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | path | 是 | 网站ID | - |

---

### GET /websites/databases
**功能**: Get databases - 获取可用的数据库列表
**参数**: 无

---

### POST /websites/databases
**功能**: Change website database - 切换网站数据库
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| databaseId | uint | 否 | 数据库ID | - |
| databaseType | string | 否 | 数据库类型 | - |

---

### POST /websites/crosssite
**功能**: Operate Cross Site Access - 操作跨站访问
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| operation | string | 是 | 操作类型 | Enable/Disable |

---

### POST /websites/exec/composer
**功能**: Exec Composer - 执行Composer命令
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| command | string | 是 | Composer命令 | - |
| extCommand | string | 否 | 扩展命令 | - |
| mirror | string | 是 | 镜像源 | - |
| dir | string | 否 | 工作目录 | - |
| user | string | 否 | 用户 | - |
| websiteId | uint | 是 | 网站ID | - |
| taskId | string | 是 | 任务ID | - |

---

### POST /websites/batch/operate
**功能**: Batch operate websites - 批量操作网站
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| ids | []uint | 是 | 网站ID列表 | - |
| operate | string | 是 | 操作类型 | start/stop/reload |
| taskId | string | 是 | 任务ID | - |

---

### POST /websites/batch/group
**功能**: Batch set website group - 批量设置网站分组
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| ids | []uint | 是 | 网站ID列表 | - |
| groupId | uint | 是 | 分组ID | - |

---

### POST /websites/batch/ssl
**功能**: Batch set HTTPS for websites - 批量设置HTTPS
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| ids | []uint | 是 | 网站ID列表 | - |
| taskId | string | 是 | 任务ID | - |
| websiteSSLId | uint | 否 | SSL证书ID | - |
| type | string | 否 | SSL类型 | existed/auto/manual |
| privateKey | string | 否 | 私钥 | - |
| certificate | string | 否 | 证书 | - |
| privateKeyPath | string | 否 | 私钥路径 | - |
| certificatePath | string | 否 | 证书路径 | - |
| importType | string | 否 | 导入类型 | - |
| httpConfig | string | 否 | HTTP配置 | HTTPSOnly/HTTPAlso/HTTPToHTTPS |
| SSLProtocol | []string | 否 | SSL协议 | - |
| algorithm | string | 否 | 算法 | - |
| hsts | bool | 否 | 是否启用HSTS | true/false |
| hstsIncludeSubDomains | bool | 否 | HSTS包含子域名 | true/false |
| httpsPorts | []int | 否 | HTTPS端口 | - |
| http3 | bool | 否 | 是否启用HTTP3 | true/false |

---

### GET /websites/domains/:websiteId
**功能**: Search website domains by websiteId - 获取网站域名列表
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | path | 是 | 网站ID | - |

---

### POST /websites/domains
**功能**: Create website domain - 创建网站域名
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| domains | []WebsiteDomain | 是 | 域名列表 | - |

**WebsiteDomain 子结构**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| domain | string | 是 | 域名 | - |
| port | int | 否 | 端口 | - |
| ssl | bool | 否 | 是否启用SSL | true/false |

---

### POST /websites/domains/del
**功能**: Delete website domain - 删除网站域名
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 域名ID | - |

---

### POST /websites/domains/update
**功能**: Update website domain - 更新网站域名
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| id | uint | 是 | 域名ID | - |
| ssl | bool | 否 | 是否启用SSL | true/false |

---

### POST /websites/group/change
**功能**: Change website group - 更改网站分组
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| group | uint | 是 | 当前分组ID | - |
| newGroup | uint | 是 | 新分组ID | - |

---

### POST /websites/stream/update
**功能**: Update Stream Config - 更新Stream配置
**参数**:
| 参数名 | 类型 | 必填 | 说明 | 取值范围 |
|--------|------|------|------|----------|
| websiteId | uint | 是 | 网站ID | - |
| streamPorts | string | 否 | 流端口 | - |
| name | string | 否 | 名称 | - |
| algorithm | string | 否 | 算法 | - |
| udp | bool | 否 | 是否UDP | true/false |
| servers | []NginxUpstreamServer | 否 | 上游服务器列表 | - |
