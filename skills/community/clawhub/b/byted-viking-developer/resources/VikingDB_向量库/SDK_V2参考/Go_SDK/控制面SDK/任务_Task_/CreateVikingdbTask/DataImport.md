# 概述
将 数据导入到 Collection 中，要求文件的列名必须和 Collection Fields 重合，否则会解析失败
使用前请先授权 VikingDB 跨服务访问 TOS [去授权](https://console.volcengine.com/iam/service/attach_role/?ServiceName=vikingdb)
# 方法定义
Go SDK 通过 `vikingdb.New(sess)` 创建的客户端实例调用 `CreateVikingdbTask(input)` 方法发起任务创建请求， input 参数类型为 `vikingdb.CreateVikingdbTaskInput` ，包含任务创建所需的完整配置信息
# 请求参数
| 参数 | 子参数 | 类型 | 是否必填 | 描述 |
| --- | --- | --- | --- | --- |
| ProjectName |  | string | 否 | 项目名称 |
| CollectionName |  | string | 2选1 | 数据集名称 |
| ResourceId |  | string |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
| TaskType |  | string | 是 | data_import |
| TaskConfig |  | TaskConfigForCreateVikingdbTaskInput | 是 | 任务具体配置 |
|  | FileType | string | 是 | 文件类型, json 或者 parquet，必填 |
|  | TosPath | string | 是 | TOS 路径，格式 ：{桶名}/{路径}，注意不是域名。必填 |
|  | IgnoreError | bool | 否 | 设置为 true 时遇到数据会继续解析文件，默认为 false |
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

    input := &vikingdb.CreateVikingdbTaskInput{
       TaskType: volcengine.String(vikingdb.EnumOfTaskTypeForCreateVikingdbTaskInputDataImport),
       TaskConfig: &vikingdb.TaskConfigForCreateVikingdbTaskInput{
          FileType: volcengine.String(vikingdb.EnumOfFileTypeForCreateVikingdbTaskInputJson),
          TosPath:  volcengine.String("your-tos-bucket-name/path/data.json"),
       },
       ProjectName:    volcengine.String("default"),
       CollectionName: volcengine.String("Your Collection Name"),
    }

    resp, err := svc.CreateVikingdbTask(input)
    if err != nil {
       panic(err)
    }

    fmt.Println(*resp.TaskId)
}
```


## 
