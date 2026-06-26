---
name: mtl-api-create
version: 0.1.0
description: 摩天轮开放接口二次封装技能。当用户需要对接摩天轮(MTL)开放平台接口、创建MTL HTTP接口、封装摩天轮API时触发。支持自动检测并添加mtl-open-sdk-consumer依赖、初始化ApiClient Bean、创建MtlRestController、根据原生接口定义生成HTTP接口代码。
---

# 摩天轮接口封装

将摩天轮开放原生接口封装为 HTTP 接口,基于 Spring Boot + mtl-open-sdk-consumer。

## 执行流程

### 步骤1:检测并添加 Maven 依赖

检测 `pom.xml` 是否已引入 `mtl-open-sdk-consumer`,若无则添加:

```xml
<dependency>
    <groupId>com.alibaba.mtl</groupId>
    <artifactId>mtl-open-sdk-consumer</artifactId>
    <version>2.0</version>
</dependency>
```

### 步骤2:初始化 ApiClient Bean

检测项目中是否已存在 `ApiClient` Bean 配置,若无则在配置类中添加:

```java
@Bean(name = "mtlClient")
public ApiClient mtlClient() throws URISyntaxException {
    return new ApiClient(
            "{clientIdentifier}",  // 需在摩天轮申请
            new URI("https://open.mtl4.alibaba-inc.com"),
            EntryToken.builder()
                    .identifier("{clientIdentifier}")
                    .token("{token}")  // 需在摩天轮申请
                    .build(),
            new ClientConfiguration());
}
```

**注意**:`clientIdentifier` 和 `token` 需在摩天轮平台申请,URI 固定为 `https://open.mtl4.alibaba-inc.com`。

### 步骤3:创建 rest 包

检测项目中是否存在 `rest` package,若无则创建。

### 步骤4:创建 MtlRestController

检测 `rest` 包下是否存在 `MtlRestController` 类,若无则创建:

```java
@RestController
@RequestMapping("/mtl")
public class MtlRestController {

    @Autowired
    private ApiClient mtlClient;

    // 若项目存在 MtlLogProducer 日志类,还需注入:
    // @Autowired
    // private GetEnv getEnv;
}
```

### 步骤5:确认原生接口定义

**必须向用户确认原生接口信息**,完整定义示例:

```
接口路径(path):/dev/api/v1/alterSheet/detail
方法类型:GET/POST
描述:查询变更单明细
Parameters(query参数):{
  "id": "integer类型,必传"
}
RequestBody(body参数):{
  "targetReleaseId": "integer类型",
  "testers": "string类型"
}
```

### 步骤6:生成 HTTP 接口

根据原生接口定义在 `MtlRestController` 中创建接口方法。

**GET 请求示例**(原生接口:`/dev/api/v1/alterSheet/detail`):

```java
@GetMapping("/api/v1/alterSheet/detail")
public Map<String, Object> getAlterSheet(@RequestParam("id") String id) {
    Map<String, Object> result = MapBuilder.of("success", true).build();
    RequestMessage request = RequestMessage.builder()
            .method(HttpMethod.GET)
            .path("/dev/api/v1/alterSheet/detail")
            .json(null)
            .parameters(MapBuilder.ofAssignType("id", id).build())
            .build();
    try {
        ResponseMessage responseMessage = mtlClient.sendRequest(request);
        if (null == responseMessage) {
            throw new RuntimeException("response is null");
        }
        result.put("data", LubanTypeUtil.toJSON(responseMessage.getJson()));
    } catch (Exception e) {
        result.put("success", false);
        result.put("msg", e.getMessage());
    }
    return result;
}
```

**POST 请求示例**(带 RequestBody):

```java
@PostMapping("/api/v1/xxx")
public Map<String, Object> postXxx(@RequestBody Map<String, Object> body) {
    Map<String, Object> result = MapBuilder.of("success", true).build();
    RequestMessage request = RequestMessage.builder()
            .method(HttpMethod.POST)
            .path("/dev/api/v1/xxx")
            .json(LubanTypeUtil.toJSONString(body))
            .parameters(null)
            .build();
    try {
        ResponseMessage responseMessage = mtlClient.sendRequest(request);
        if (null == responseMessage) {
            throw new RuntimeException("response is null");
        }
        result.put("data", LubanTypeUtil.toJSON(responseMessage.getJson()));
    } catch (Exception e) {
        result.put("success", false);
        result.put("msg", e.getMessage());
    }
    return result;
}
```

## 关键规则

| 规则 | 说明 |
|------|------|
| HTTP 路径 | 去除原生路径中的 `/dev` 前缀 |
| GET 参数 | 使用 `parameters` 传递 query 参数 |
| POST Body | 使用 `LubanTypeUtil.toJSONString()` 转换后放入 `json` 字段 |
| 日志记录 | 仅当项目存在 `MtlLogProducer` 类时添加日志代码 |

## 日志代码(可选)

若项目存在 `MtlLogProducer` 类,在 try-catch 中添加:

```java
// 成功日志
MtlLogProducer.info(
        "/dev/api/v1/xxx",
        getEnv.curEnv().getEnv(),
        "接口描述",
        LubanTypeUtil.toJSONString(request),
        LubanTypeUtil.toJSONString(responseMessage));

// 异常日志
MtlLogProducer.error(
        "/dev/api/v1/xxx",
        getEnv.curEnv().getEnv(),
        "接口描述",
        LubanTypeUtil.toJSONString(request),
        e);
```