# 概述
更新指定的任务，当前任务更新只用于**删除**任务的人工确认 环节
# 方法定义
Go SDK 通过 `vikingdb.New(sess)` 创建的客户端实例调用 `UpdateVikingdbTask(input)` 方法发起任务创建请求， input 参数类型为 `vikingdb.UpdateVikingdbTaskInput` ，包含任务创建所需的完整配置信息
# 请求参数
| 字段名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| TaskId | string | 是 | 任务ID，在创建任务时返回 |
| TaskStatus <br>  | string <br>  | 只有 confirm 状态可以更新，只能更新为 confirmed，必填 |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
# 返回参数
| 参数 | 类型 | 示例值 | 描述 |
| --- | --- | --- | --- |
| Message | string | success | 操作结果信息 |
# 示例

```Go
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

    input := &vikingdb.UpdateVikingdbTaskInput{
       TaskId:     volcengine.String("your-task-id"),
       TaskStatus: volcengine.String(vikingdb.EnumOfTaskStatusForUpdateVikingdbTaskInputConfirmed),
    }

    resp, err := svc.UpdateVikingdbTask(input)
    if err != nil {
       panic(err)
    }

    fmt.Println(*resp.Message)
}
```

## 
