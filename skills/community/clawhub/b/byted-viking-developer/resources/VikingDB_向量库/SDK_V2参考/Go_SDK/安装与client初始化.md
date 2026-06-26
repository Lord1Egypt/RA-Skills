向量数据库 Viking DB 支持通过 Go SDK 操作数据库。在使用 Go SDK 之前，需要先完成安装 SDK 和 初始化 SDK 步骤。
# 前提条件

1. 已通过 [注册账号及开通服务](https://www.volcengine.com/docs/84313/1254444) 操作完成注册账号及开通服务。
2. 获取安全凭证。Access Key（访问密钥）是访问火山引擎服务的安全凭证，包含Access Key ID（简称为AK）和Secret Access Key（简称为SK）两部分。可登录火山引擎控制台并前往【密钥管理】查看当前账号的 AK / SK，更多详情请参考 [Access Key（密钥）管理](https://www.volcengine.com/docs/6291/65568)。

![Image](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_5ef0f716976d0e2060797391b516a839.png)
# 安装 SDK
为优化权限系统，向量库 SDK分为**控制面**和**数据面**，其中控制面为管理数据集、索引、离线任务；数据面为数据、检索和向量化。控制面同时支持从页面操作，请您根据需要配置依赖。
## 1.  控制面和数据面依赖配置
```XML
# 数据面SDK
go get -u github.com/volcengine/vikingdb-go-sdk

# 控制面SDK
go get -u github.com/volcengine/volcengine-go-sdk
```



# 初始化 SDK
如需私网连接，参考[私网连接方式](/c8p1dfoq/wfkp3iey)进行配置并获取域名。目前私网连接请求域名仅支持http。
代码中 Your ak 及 Your sk 需要分别替换为您的 AK 及 SK，Your host、Your region、Your scheme 替换为您使用的域名、地区、请求协议（http / https）。



1. **数据面(Data / Search / Embedding)**

| **Region 中文名称** | **Region ID** | 互联网域名（外网） | 私网连接终端节点服务（**非域名**，请参考[私网连接](https://www.volcengine.com/docs/84313/1254445)文档） |
| --- | --- | --- | --- |
| 华北2（北京） | cn-beijing | [api-vikingdb.vikingdb.cn-beijing.volces.com](http://api-vikingdb.vikingdb.cn-beijing.volces.com/) | [com.volces.privatelink.cn-beijing.vikingdb-ann](com.volces.privatelink.cn-beijing.vikingdb-ann) |
| 华南1（广州） | cn-guangzhou | [api-vikingdb.vikingdb.cn-guangzhou.volces.com](http://api-vikingdb.vikingdb.cn-guangzhou.volces.com/) | [com.volces.privatelink.cn-guangzhou.vikingdb-ann](com.volces.privatelink.cn-guangzhou.vikingdb-ann) |
| 华东2（上海） | cn-shanghai | [api-vikingdb.vikingdb.cn-shanghai.volces.com](http://api-vikingdb.vikingdb.cn-shanghai.volces.com/) | [com.volces.privatelink.cn-shanghai.vikingdb-ann](com.volces.privatelink.cn-shanghai.vikingdb-ann) |
| 亚太东南（柔佛） | ap-southeast-1 | [api-vikingdb.vikingdb.ap-southeast-1.volces.com](http://api-vikingdb.vikingdb.ap-southeast-1.volces.com/) | 火山柔佛region不支持私网访问 |
```Java
package main

import (
    "fmt"
    "github.com/volcengine/vikingdb-go-sdk/vector"
    "os"
    "time"
)

func main() {
    var (
       accessKey = os.Getenv("VIKINGDB_AK")
       secretKey = os.Getenv("VIKINGDB_SK")
       //apiKey    = os.Getenv("VIKINGDB_APIKEY")
       endpoint  = "https://api-vikingdb.vikingdb.cn-beijing.volces.com"
       region    = "cn-beijing"
    )

    client, err := vector.New(
       vector.AuthIAM(accessKey, secretKey), // IAM auth
       // vector.AuthAPIKey(apiKey),            // APIKey auth
       vector.WithEndpoint(endpoint),
       vector.WithRegion(region),
       vector.WithTimeout(time.Second*30),
       vector.WithMaxRetries(3),
    )
    if err != nil {
       fmt.Println("New client failed, err: ", err)
       panic(err)
    }
}
```



2. **控制面(Collection / Index / Task)**

| **Region 中文名称** | **Region ID** | 互联网域名（外网） | 私网连接终端节点服务（**非域名**，请参考[私网连接](https://www.volcengine.com/docs/84313/1254445)文档） |
| --- | --- | --- | --- |
| 华北2（北京） | cn-beijing | [vikingdb.cn-beijing.volcengineapi.com](http://vikingdb.cn-beijing.volcengineapi.com/) | com.volces.privatelink.cn-beijing.api.vikingdb |
| 华南1（广州） | cn-guangzhou | [vikingdb.cn-guangzhou.volcengineapi.com](http://vikingdb.cn-guangzhou.volcengineapi.com/) | com.volces.privatelink.cn-guangzhou.api.vikingdb |
| 华东2（上海） | cn-shanghai | [vikingdb.cn-shanghai.volcengineapi.com](http://vikingdb.cn-shanghai.volcengineapi.com/) | com.volces.privatelink.cn-shanghai.api.vikingdb |
| 亚太东南（柔佛） | ap-southeast-1 | [vikingdb.ap-southeast-1.volcengineapi.com](http://vikingdb.ap-southeast-1.volcengineapi.com/) | com.volces.privatelink.ap-southeast-1.api.vikingdb |
```Java
package main

import (
    "fmt"
    "os"

    "github.com/volcengine/volcengine-go-sdk/service/vikingdb"
    "github.com/volcengine/volcengine-go-sdk/volcengine"
    "github.com/volcengine/volcengine-go-sdk/volcengine/credentials"
    "github.com/volcengine/volcengine-go-sdk/volcengine/session"
)

func main() {
    var (
       accessKey = os.Getenv("VIKINGDB_AK")
       secretKey = os.Getenv("VIKINGDB_SK")
       region    = "cn-beijing"
    )
    config := volcengine.NewConfig().
       WithRegion(region).
       WithCredentials(credentials.NewStaticCredentials(accessKey, secretKey, ""))

    sess, err := session.NewSession(config)
    if err != nil {
       panic(err)
    }
    svc := vikingdb.New(sess)

    fmt.Printf("APIVersion: %s\n", svc.APIVersion)
}
```


