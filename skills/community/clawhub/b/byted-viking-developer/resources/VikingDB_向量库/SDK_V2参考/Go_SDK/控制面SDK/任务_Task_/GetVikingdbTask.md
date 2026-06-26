# 概述
查询指定 task 的详情信息和执行进度
# 方法定义
Go SDK 通过 `vikingdb.New(sess)` 创建的客户端实例调用 `GetVikingdbTask(input)` 方法发起任务创建请求， input 参数类型为 `vikingdb.GetVikingdbTaskInput` ，包含任务创建所需的完整配置信息
# 请求参数
| 字段名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| TaskId | string | 是 | 任务ID，在创建任务时返回 |
# 返回参数
| **属性** | **类型** | **说明** |
| --- | --- | --- |
| TaskId | string | 任务ID |
| TaskType | string | 任务类型 |
| TaskStatus | string | 任务状态 |
| UpdatePerson | string | 任务更新人 |
| UpdateTime | string | 任务信息更新时间 |
| CreateTime | string | 任务信息创建时间 |
| TaskProcessInfo | TaskProcessInfoForGetVikingdbTaskOutput | 任务处理信息，例如进度等 |

* task_type 类型包括

| data_import | 数据导入任务 |
| --- | --- |
| data_export | 数据导出任务 |
| filter_update | 数据过滤更新任务 |
| filter_delete | 数据过滤删除任务 |

* task_status 任务状态包括

| init | queued | confirm | confirmed | running | done | fail |
| --- | --- | --- | --- | --- | --- | --- |
| 初始化中 | 排队中 | 需要人工确认 | 已确认 | 执行中 | 完成 | 失败 |

* TaskProcessInfoForGetVikingdbTaskOutput 

| **字段** | **类型** | **说明** |
| --- | --- | --- |
| TaskProgress | string | 任务进度 例如50% |
| ErrorMessage | string | 任务错误信息 |
| SampleData | []SampleDataForGetVikingdbTaskOutput> | 采样5条数据用于展示 |
| SampleTimestamp | int | 采样的时间戳，后写入的数据不会被处理 |
| ScanDataCount | int | 当前扫描数据量 |
| TotalDataCount | int | collection 数据总条数(预估） |
| TotalFilterCount | int | 已经过滤出的数据 |
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

    input := &vikingdb.GetVikingdbTaskInput{
       TaskId: volcengine.String("your-task-id"),
    }

    resp, err := svc.GetVikingdbTask(input)
    if err != nil {
       panic(err)
    }

    fmt.Println(*resp.TaskStatus)
    fmt.Println(*resp.TaskType)
}
```

## 
