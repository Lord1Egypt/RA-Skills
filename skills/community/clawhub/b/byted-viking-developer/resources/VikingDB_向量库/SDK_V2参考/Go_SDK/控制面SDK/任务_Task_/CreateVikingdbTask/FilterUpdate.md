# 概述
按特定条件批量更新数据，不支持vector、sparse_vector、text 类型字段的更新
# 方法定义
Go SDK 通过 `vikingdb.New(sess)` 创建的客户端实例调用 `CreateVikingdbTask(input)` 方法发起任务创建请求， input 参数类型为 `vikingdb.CreateVikingdbTaskInput` ，包含任务创建所需的完整配置信息
# 请求参数
| 参数 | 子参数 | 类型 | 是否必填 | 描述 |
| --- | --- | --- | --- | --- |
| ProjectName |  | string | 否 | 项目名称 |
| CollectionName |  | string | 2选1 | 数据集名称 |
| ResourceId |  | string |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
| **TaskType** |  | string | 是 | filter_update |
| TaskConfig |  | TaskConfigForCreateVikingdbTaskInput | 是 | 任务具体配置 |
|  | FilterConds | []interface{} | 是 | 过滤条件。使用参考https://www.volcengine.com/docs/84313/1791133 <br>  |
|  | UpdateFields | interface{} | 是 | 需要更新的字段值，必须是标量字段，不支持vector、sparse_vector、text 类型字段的更新 |
# 返回参数
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| TaskId | string | 任务ID |
| Message | string | 操作结果信息 |
# 示例
## 请求参数
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

    // 创建更新任务
    input := &vikingdb.CreateVikingdbTaskInput{
       TaskType: volcengine.String(vikingdb.EnumOfTaskTypeForCreateVikingdbTaskInputFilterUpdate),
       TaskConfig: &vikingdb.TaskConfigForCreateVikingdbTaskInput{
          FilterConds: []interface{}{
             map[string]interface{}{
                "op":    "must",
                "field": "name",
                "conds": []string{"old value1", "old value2"},
             },
          },
          UpdateFields: map[string]interface{}{
             "name": "new value",
          },
       },
       CollectionName: volcengine.String("Your Collection Name"),
       ProjectName:    volcengine.String("default"),
    }

    resp, err := svc.CreateVikingdbTask(input)
    if err != nil {
       panic(err)
    }

    fmt.Println(*resp.TaskId)
}
```

## 
