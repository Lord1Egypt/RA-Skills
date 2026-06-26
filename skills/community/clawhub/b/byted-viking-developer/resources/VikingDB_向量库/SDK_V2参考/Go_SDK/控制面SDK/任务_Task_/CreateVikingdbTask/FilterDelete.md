# 概述
按特定条件批量删除Collection中的数据
# 方法定义
```Java
public CreateVikingdbTaskResponse createVikingdbTask(CreateVikingdbTaskRequest body) throws ApiException
```

# 请求参数
若要将数据备份至TOS，请先授权 VikingDB 跨服务访问 TOS [去授权](https://console.volcengine.com/iam/service/attach_role/?ServiceName=vikingdb)


| 参数 | 子参数 | 类型 | 是否必填 | 描述 |
| --- | --- | --- | --- | --- |
| ProjectName |  | String | 否 | 项目名称 |
| CollectionName |  | String | 2选1 | 数据集名称 |
| ResourceId |  | String |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
| **TaskType** |  | String | 是 | filter_delete |
| TaskConfig |  | TaskConfigForCreateVikingdbTaskInput | 是 | 任务具体配置 |
|  | FileType | String | 是 | 文件类型, json 或者 parquet，必填 |
|  | NeedConfirm | Boolean | 否 | 是否可跳过人工确认环节，默认为true |
|  | FilterConds | List<Object> | 是 | 过滤条件。使用参考https://www.volcengine.com/docs/84313/1791133 |
|  | TosPath | String | 是 | TOS 路径，格式 ：{桶名}/{路径}，注意不是域名。必填 |
# 返回参数
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| taskId | String | 任务ID |
| message | String | 操作结果信息 |
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

## 返回参数
| 参数 | 类型 | 示例值 | 描述 |
| --- | --- | --- | --- |
| TaskId | String |  | 任务ID |
| Message | String | success | 操作结果信息 |

## 后续处理
如果需要人工确认，可执行**任务更新**操作
