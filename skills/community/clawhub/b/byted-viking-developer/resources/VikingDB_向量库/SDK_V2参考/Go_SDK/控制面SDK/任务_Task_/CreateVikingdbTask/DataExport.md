# 概述
按特定条件批量导出Collection中的数据
使用前请先授权 VikingDB 跨服务访问 TOS [去授权](https://console.volcengine.com/iam/service/attach_role/?ServiceName=ml_platform)

# 方法定义
Go SDK 通过 `vikingdb.New(sess)` 创建的客户端实例调用 `CreateVikingdbTask(input)` 方法发起任务创建请求， input 参数类型为 `vikingdb.CreateVikingdbTaskInput` ，包含任务创建所需的完整配置信息
# 请求参数
| 参数 | 子参数 | 类型 | 是否必填 | 描述 |
| --- | --- | --- | --- | --- |
| ProjectName |  | string | 否 | 项目名称 |
| CollectionName |  | string | 2选1 | 数据集名称 |
| ResourceId |  | string |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
| TaskType |  | string | 是 | data_export |
| TaskConfig |  | TaskConfigForCreateVikingdbTaskInput | 是 | 任务具体配置 |
|  | FileType | string | 是 | 文件类型, json 或者 parquet，必填 |
|  | FilterConds | []interface{} | 否 | 过滤条件。使用参考https://www.volcengine.com/docs/84313/1791133 <br>  <br> * 如果不填入FilterConds，则无关ExportAll，一定导出全部数据。 <br> * 如果填入FilterConds： <br>    * 不写Exportall，或Exportall=false，则默认导出满足条件的数据。 <br>    * 写exportall=true，则强制导出全部数据，此时FilterConds不生效。 |
|  | TosPath | string | 是 | TOS 路径，格式 ：{桶名}/{路径}，注意不是域名。必填 |
|  | ExportAll | bool | 否 | 是否导出全部数据，此时filter不生效。默认为false |
## 返回参数
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| TaskId | string | 任务ID |
| Message | string | 操作结果信息 |
# 示例
## 请求参数
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

    // 创建导出任务
    input := &vikingdb.CreateVikingdbTaskInput{
       TaskType: volcengine.String(vikingdb.EnumOfTaskTypeForCreateVikingdbTaskInputDataExport),
       TaskConfig: &vikingdb.TaskConfigForCreateVikingdbTaskInput{
          ExportAll: volcengine.Bool(true),
          FileType:  volcengine.String(vikingdb.EnumOfFileTypeForCreateVikingdbTaskInputJson),
          TosPath:   volcengine.String("your-tos-bucket-name/path/"),
       },
       CollectionName: volcengine.String("Your-Collection-Name"),
       ProjectName:    volcengine.String("default"),
    }

    resp, err := svc.CreateVikingdbTask(input)
    if err != nil {
       panic(err)
    }

    fmt.Println(*resp.TaskId)
}
```


## 后续处理
### 1、从 TOS 下载文件
```Go
package main

import (
    "context"
    "fmt"
    "os"

    "github.com/volcengine/ve-tos-golang-sdk/v2/tos"
)

func main() {
    var (
       endpoint  = "https://tos-cn-beijing.volces.com"
       region    = "cn-beijing"
       accessKey = os.Getenv("TOS_ACCESS_KEY")
       secretKey = os.Getenv("TOS_SECRET_KEY")
       bucket    = "liningrui-test"
       objectKey = "path/0.parquet"
       localPath = "data.parquet"
    )

    // Initialize TOS client
    client, err := tos.NewClientV2(endpoint, tos.WithRegion(region), tos.WithCredentials(tos.NewStaticCredentials(accessKey, secretKey)))
    if err != nil {
       fmt.Printf("Init client failed, err: %v\n", err)
       return
    }

    // Download object
    _, err = client.GetObjectToFile(context.Background(), &tos.GetObjectToFileInput{
       GetObjectV2Input: tos.GetObjectV2Input{
          Bucket: bucket,
          Key:    objectKey,
       },
       FilePath: localPath,
    })
    if err != nil {
       fmt.Printf("Get object failed, err: %v\n", err)
       return
    }

    fmt.Printf("Download success, object %s saved to %s\n", objectKey, localPath)
}
```

### 2、解析 parquet 类型数据
```Go
package main

import (
    "fmt"
    "log"

    "github.com/xitongsys/parquet-go-source/local"
    "github.com/xitongsys/parquet-go/reader"
)

// DemoStruct defines the schema of the parquet file
// You should modify this struct according to your parquet file schema
type DemoStruct struct {
    Name string `parquet:"name=name, type=BYTE_ARRAY, convertedtype=UTF8"`
    Id   int64  `parquet:"name=id, type=INT64"`
}

func main() {
    filePath := "data.parquet" // Replace with your parquet file path

    // 1. Open local file
    fr, err := local.NewLocalFileReader(filePath)
    if err != nil {
       log.Printf("Can't open file: %v", err)
       return
    }
    defer fr.Close()

    // 2. Create parquet reader
    // The second argument is an instance of the struct that matches the parquet schema
    pr, err := reader.NewParquetReader(fr, new(DemoStruct), 4)
    if err != nil {
       log.Printf("Can't create parquet reader: %v", err)
       return
    }
    defer pr.ReadStop()

    // 3. Get total number of rows
    num := int(pr.GetNumRows())
    fmt.Printf("Total rows: %d\n", num)

    // 4. Read and print rows
    // We read in batches for efficiency
    batchSize := 10
    for i := 0; i < num; i += batchSize {
       readNum := batchSize
       if i+batchSize > num {
          readNum = num - i
       }

       data := make([]DemoStruct, readNum)
       if err = pr.Read(&data); err != nil {
          log.Printf("Read error: %v", err)
          break
       }

       for _, item := range data {
          fmt.Printf("Row: %+v\n", item)
       }
    }
}
```


