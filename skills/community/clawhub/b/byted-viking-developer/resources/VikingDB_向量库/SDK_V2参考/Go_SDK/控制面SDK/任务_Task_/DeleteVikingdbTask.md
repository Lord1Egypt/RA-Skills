# 概述
删除指定的任务，删除后任务将终止
# 方法定义
Go SDK 通过 `vikingdb.New(sess)` 创建的客户端实例调用 `DeleteVikingdbTask(input)` 方法发起任务创建请求， input 参数类型为 `vikingdb.DeleteVikingdbTaskInput` ，包含任务创建所需的完整配置信息
# 请求参数
| 字段名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| TaskId | string | 是 | 任务ID，在创建任务时返回 |
# 返回参数
| 参数 | 类型 | 示例值 | 描述 |
| --- | --- | --- | --- |
| Message | String | success | 操作结果信息 |
# 示例
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

    input := &vikingdb.DeleteVikingdbTaskInput{
       TaskId: volcengine.String("your-task-id"),
    }

    resp, err := svc.DeleteVikingdbTask(input)
    if err != nil {
       panic(err)
    }

    fmt.Println(*resp.Message)
}
```

## 
