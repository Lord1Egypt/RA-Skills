
---
name: controller-call-chain-analysis
description: 本技能用于分析 Java 微服务项目中 Controller 层的完整调用链路，能够自动追溯到 Service、Mapper、Repository 层，并提取完整的 SQL 语句。最终生成结构化的 JSON 文件，便于 API 文档生成、代码审计或架构理解。
---

# Java Controller 调用链路分析 Skill

## 简介
本技能用于分析 Java 微服务项目中 Controller 层的完整调用链路，能够自动追溯到 Service、Mapper、Repository 层，并提取完整的 SQL 语句。最终生成结构化的 JSON 文件，便于 API 文档生成、代码审计或架构理解。

## 适用场景
- 需要快速了解某个 Controller 接口背后的业务逻辑和数据流向
- 自动化生成 API 调用链路文档
- 审计 SQL 语句或分析数据库访问模式
- 批量分析整个模块的接口实现细节

## 输入参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `controllerPath` | string | 是 | Controller 源文件的相对路径，例如 `src/main/java/org/ssh/boot/itemSupply/controller/pham/TDrugdictController.java` |
| `outputPath` | string | 否 | 输出 JSON 文件的目录，默认为 `docs/api_analysis/`。如果目录不存在，会自动创建。 |

## 输出
在指定的输出目录下生成一个以 Controller 类名命名的 JSON 文件（例如 `TDrugdictController.json`），文件内容遵循固定的 JSON 结构（详见下文）。该文件包含了从 Controller 方法到 Service 实现、再到 Mapper/Repository 以及最终 SQL 语句的完整调用链路信息。

## 工作流程

### 1. 读取 Controller 文件
- 解析 Java 源文件，提取：
    - 类名、包名
    - 类级别的 `@RequestMapping` 路径
    - 类级别的 `@Api` 或 `@ApiOperation` 注解（接口描述）
    - 每个方法的 HTTP 方法注解（`@GetMapping`、`@PostMapping` 等）及路径
    - 方法参数列表（包括参数名、类型、是否必填、`@ApiParam` 描述等）

### 2. 追溯 Service 实现类
- 根据 Controller 中注入的 Service 字段类型，定位对应的 Service 接口
- 查找接口的实现类 Search(pattern: "implements 接口名称", path: "项目地址") 
- 读取实现类，识别每个方法内部调用的 Mapper 或 Repository 方法
- 读取实现类，识别每个方法内部方法（该方法可能存在Mapper 或 Repository 方法调用）
- 根据代码，输出方法介绍

### 3. 追溯 Mapper 层（MyBatis）
- 查找与 Service 中调用的 Mapper 接口（通常在 `mapper/` 目录下）
- 定位对应的 MyBatis XML 文件（通常在 `src/main/resources/mapper/` 目录下，命名与接口相同）
- 提取 XML 中对应方法的 SQL 语句，并解析出表名、查询条件、SQL 类型（select/insert/update/delete）

### 4. 追溯 Repository 层（Spring Data JPA）
- 查找 Service 中调用的 Repository 接口（通常在 `repository/` 目录下）
- 提取方法上的 `@Query` 注解中的 JPQL 或原生 SQL；如果方法名符合命名规范，则根据方法名解析 SQL（可选）

### 5. 生成 JSON 输出
按照预定义的 JSON 结构，将上述信息组合并写入文件。

## 输出 JSON 结构
```json
{
  "module": "模块名",                        // 根据包名自动推断，例如 "itemSupply"
  "controller": {
    "className": "Controller类名",
    "filePath": "Controller源文件路径",
    "requestMapping": "/请求路径",           // 类级别的 @RequestMapping
    "description": "Controller描述",         // @Api 注解的 value 或 description
    "methods": [
      {
        "name": "方法名",
        "httpMethod": "GET/POST/PUT/DELETE",
        "url": "/完整URL",                    // 类路径 + 方法路径
        "description": "接口描述",             // @ApiOperation 的值
        "controllerFilePath": "Controller.java:行号", // 源文件位置
        "params": [
          {
            "name": "参数名",
            "type": "类型",
            "required": true/false,
            "description": "描述"             // @ApiParam 的值
          }
        ],
        "service": [{                         // 可能多个
          "className": "ServiceImpl类名",
          "filePath": "ServiceImpl源文件路径",
          "method": "方法名",                  // Service 中调用的方法
          "steps": ["业务步骤描述"],            // 可选，可提取方法中的业务逻辑注释
          "mapper": [{                          // 如果调用的是 MyBatis Mapper,可能的多个
            "className": "Mapper接口类名",
            "filePath": "Mapper接口源文件路径",
            "method": "方法名",
            "xmlFilePath": "Mapper XML文件路径",
            "sql": {
              "id": "SQL ID",
              "table": "表名",
              "statement": "完整SQL语句",
              "conditions": ["查询条件"]
            }
          }],
          "repository": [{                       // 如果调用的是 JPA Repository,可能的多个
            "className": "Repository接口类名",
            "filePath": "Repository源文件路径",
            "method": "方法名",
            "framework": "Spring Data JPA",
            "sql": "JPQL或native SQL"
          }]
        }]
      }
    ]
  }
}
```

## 注意事项
- **项目根目录**：本技能默认项目根路径为当前目录，所有文件路径均相对于此目录。如需修改，请在调用前调整。
- **输出目录**：如未指定 `outputPath`，默认输出到 `docs/api_analysis/`。
- **批量分析**：本技能一次只分析一个 Controller；若需批量分析，请通过循环调用本技能，每次传入不同的 `controllerPath`。
- **依赖假设**：代码结构需遵循常见的 Spring Boot + MyBatis / JPA 的包命名规范（如 `service.impl`、`mapper`、`repository`、`resources/mapper`）。若项目结构特殊，分析可能不完整。

---