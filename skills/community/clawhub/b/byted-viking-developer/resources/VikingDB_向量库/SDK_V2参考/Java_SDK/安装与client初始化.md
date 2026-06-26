向量数据库 Viking DB 支持通过 Java SDK 操作数据库。在使用 Java SDK 之前，需要先完成安装 SDK 和 初始化 SDK 步骤。
# 前提条件

1. 已通过 [注册账号及开通服务](https://www.volcengine.com/docs/84313/1254444) 操作完成注册账号及开通服务。
2. 获取安全凭证。Access Key（访问密钥）是访问火山引擎服务的安全凭证，包含Access Key ID（简称为AK）和Secret Access Key（简称为SK）两部分。可登录火山引擎控制台并前往【密钥管理】查看当前账号的 AK / SK，更多详情请参考 [Access Key（密钥）管理](https://www.volcengine.com/docs/6291/65568)。
   ![Image](https://portal.volccdn.com/obj/volcfe/cloud-universal-doc/upload_5ef0f716976d0e2060797391b516a839.png)

# 安装 SDK
为优化权限系统，向量库 SDK分为**控制面**和**数据面**，其中控制面为管理数据集、索引、离线任务；数据面为数据、检索和向量化。控制面同时支持从页面操作，请您根据需要配置依赖。
## 1.  控制面依赖配置
```XML
<dependency>
    <groupId>com.volcengine</groupId>
    <artifactId>volcengine-java-sdk-vikingdb</artifactId>
    <version>{version}</version>
    <!-- 推荐使用最新版本 -->
    <!-- 版本号可以参考https://central.sonatype.com/artifact/com.volcengine/volcengine-java-sdk-vikingdb/versions -->
</dependency>
```

maven仓库：
[https://central.sonatype.com/artifact/com.volcengine/volcengine-java-sdk-vikingdb/versions](https://central.sonatype.com/artifact/com.volcengine/volcengine-java-sdk-vikingdb/versions)
源代码地址：
[https://github.com/volcengine/volcengine-java-sdk/tree/master/volcengine-java-sdk-vikingdb](https://github.com/volcengine/volcengine-java-sdk/tree/master/volcengine-java-sdk-vikingdb)
## 2.  数据面依赖配置
```XML
<dependency>
    <groupId>com.volcengine</groupId>
    <artifactId>vikingdb-java-sdk</artifactId>
    <version>{version}</version>
    <!-- 推荐使用最新版本 -->
    <!-- 版本号可以参考https://central.sonatype.com/artifact/com.volcengine/vikingdb-java-sdk/versions -->
</dependency>
```

maven仓库：
[https://central.sonatype.com/artifact/com.volcengine/vikingdb-java-sdk/versions](https://central.sonatype.com/artifact/com.volcengine/vikingdb-java-sdk/versions)
源代码地址：
[https://github.com/volcengine/vikingdb-java-sdk](https://github.com/volcengine/vikingdb-java-sdk)

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
import com.volcengine.vikingdb.runtime.core.auth.AuthWithAkSk;
import com.volcengine.vikingdb.runtime.core.ClientConfig;
import com.volcengine.vikingdb.runtime.enums.Scheme;
import com.volcengine.vikingdb.runtime.vector.service.VectorService;

import java.util.Properties;

public class VikingDBQuickStart {

    public static void main(String[] args) throws Exception {
        String host = "api-vikingdb.vikingdb.cn-beijing.volces.com";
        String region = "cn-beijing";
        String accessKey = "your-access-key";
        String secretKey = "your-secret-key";

        // 初始化客户端
        VectorService vectorService = new VectorService(
                Scheme.HTTPS,
                host,
                region,
                new AuthWithAkSk(accessKey, secretKey),
                ClientConfig.builder().build()
        );

        System.out.println("VikingDB client initialized successfully.");

        // 后续操作...
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
import com.volcengine.ApiClient;
import com.volcengine.sign.Credentials;
import com.volcengine.vikingdb.VikingdbApi;

public class QuickStart {
    public static void main(String[] args) {
        String ak = "your-access-key"; // 替换为您的 AK
        String sk = "your-secret-key"; // 替换为您的 SK
        String endpoint = "vikingdb.cn-beijing.volcengineapi.com"; // 填写您的控制面服务域名
        String region = "cn-beijing"; // 填写您的服务区域

        ApiClient apiClient = new ApiClient()
                .setEndpoint(endpoint)
                .setCredentials(Credentials.getCredentials(ak, sk))
                .setRegion(region);

        VikingdbApi api = new VikingdbApi(apiClient);

        // 您现在可以使用 'api' 对象调用 VikingDB API
        // ......
    }
}
```


