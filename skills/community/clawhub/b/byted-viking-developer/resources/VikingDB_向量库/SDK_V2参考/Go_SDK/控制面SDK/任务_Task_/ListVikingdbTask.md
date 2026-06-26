# 概述
获取多个task的信息，最多一次性展示20条
# 方法定义
Go SDK 通过 `vikingdb.New(sess)` 创建的客户端实例调用 `ListVikingdbTask(input)` 方法发起任务创建请求， input 参数类型为 `vikingdb.ListVikingdbTaskInput` ，包含任务创建所需的完整配置信息
# 请求参数
| 参数 | 类型 | 是否必填 | 描述 |
| --- | --- | --- | --- |
| ProjectName | string | 否 | 项目名称 |
| CollectionName | string | 2选1 | 数据集名称 |
| ResourceId | string |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
| TaskStatus | string | 是 | 任务状态，见下 |
| TaskType | string | 是 | 任务类型，见下 |
| PageNumber | int | 否 | 翻页页码。起始为1。 |
| PageSize | int | 否 | 翻页每页的大小。 |
# 返回参数
| 字段 | 类型 | 子字段说明 |
| --- | --- | --- |
| Tasks <br>  | []TaskForListVikingdbTaskOutput | 任务ID |
| PageSize | int |  |
| PageNumber | int |  |
| TotalCount | int |  |

* List<TaskForListVikingdbTaskOutput>

| **属性** |  | **类型** | **说明** |
| --- | --- | --- | --- |
| TaskId |  | string | 任务ID |
| TaskConfig |  | TaskConfigForListVikingdbTaskOutput |  |
|  | CollectionName  | string |  |
|  | ExportAll  | bool |  |
| TaskType |  | string | 任务类型 |
| TaskStatus |  | string | 任务状态 |
| UpdatePerson |  | string | 任务更新人 |
| UpdateTime |  | string | 任务信息更新时间 |
| CreateTime |  | string | 任务信息创建时间 |
| TaskProcessInfo |  | TaskProcessInfoForListVikingdbTaskOutput  | 任务处理信息，见下 |

* taskType 类型包括

| data_import | 数据导入任务 |
| --- | --- |
| data_export | 数据导出任务 |
| filter_update | 数据过滤更新任务 |
| filter_delete | 数据过滤删除任务 |

* taskStatus 任务状态包括

| init | queued | running | done | fail |
| --- | --- | --- | --- | --- |
| 初始化中 | 排队中 | 执行中 | 完成 | 失败 |

* TaskProcessInfoForListVikingdbTaskOutput 包括

| **字段** | **类型** | **说明** |
| --- | --- | --- |
| TaskProgress | string | 任务进度 例如50% |
| ErrorMessage | string | 任务错误信息 |
| SampleData | []SampleDataForGetVikingdbTaskOutput | 采样5条数据用于展示 |
| SampleTimestamp | int | 采样的时间戳，后写入的数据不会被处理 |
| ScanDataCount | int | 当前扫描数据量 |
| TotalDataCount | int | collection 数据总条数(预估） |
| TotalFilterCount | int | 已经过滤出的数据 |
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

    input := &vikingdb.ListVikingdbTaskInput{
       ProjectName:    volcengine.String("default"),
       CollectionName: volcengine.String("Your Collection Name"),
    }

    resp, err := svc.ListVikingdbTask(input)
    if err != nil {
       panic(err)
    }

    fmt.Println(*resp.TotalCount)
    for _, task := range resp.Tasks {
       fmt.Println(*task.TaskId, *task.TaskStatus)
    }
}
```

## 
