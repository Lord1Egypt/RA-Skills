# 阿里云日志查询技能 (aliyun-sls-get-log)

## 技能描述

调用阿里云日志服务（SLS）CLI命令查询指定Project和Logstore下的日志数据，支持基础日志查询和SQL分析查询，适用于获取指定时间范围内、指定数量的日志数据场景。

## 前置依赖与环境准备

### 系统与软件要求

| 依赖项      | 要求                                                                                          |
| -------- | ------------------------------------------------------------------------------------------- |
| 操作系统     | Windows、Linux、macOS                                                                         |
| Python版本 | Python 2.7+ 或 Python 3.7+（推荐Python 3.7及以上）                                                  |
| 依赖组件     | docopt、aliyun-log-python-sdk、jmespath、aliyun-python-sdk-core、aliyun-python-sdk-sts、requests |

### Python环境配置

#### Linux/macOS

1. 创建并编辑环境变量配置文件
   
   ```bash
   touch ~/.bash_profile
   vim ~/.bash_profile
   ```
2. 添加Python安装路径（替换为实际路径）
   
   ```bash
   export PATH=$PATH:/usr/local/python3/bin
   ```
3. 使配置生效
   
   ```bash
   source ~/.bash_profile
   ```
   
   #### Windows
4. 右键单击「此电脑」→「属性」→「高级系统设置」→「环境变量」
5. 在「用户变量」的「Path」中添加Python安装路径下的bin目录，例如：`D:\dev\python\python37\bin`
6. 重启命令行或IDE使配置生效
   
   ### CLI安装
   
   #### 通用安装命令（推荐）
   
   ```bash
   pip3 install aliyun-log-python-sdk aliyun-log-cli -U --no-cache
   ```
   
   #### 各系统验证安装
   
   ```bash
   aliyunlog --version
   # 输出示例：aliyun-log-cli 0.2.9
   ```
   
   ### CLI升级与卸载
- 升级到最新版本
  
  ```bash
  pip3 install aliyun-log-python-sdk aliyun-log-cli -U --no-cache
  ```
- 卸载CLI
  
  ```bash
  pip3 uninstall aliyun-log-cli
  ```
  
  ## CLI配置指南
  
  ### 凭证优先级（从高到低）
1. 命令行直接传入的全局参数（--access-id、--access-key等）
2. --profile参数指定的阿里云CLI配置文件凭证
3. ALIYUN_LOG_CLI系统环境变量
4. 日志服务CLI配置文件（~/.aliyunlogcli）
5. 阿里云CLI系统环境变量（ALIBABACLOUD、ALICLOUD）
6. 阿里云CLI配置文件（~/.aliyun/config.json）
   
   ### 配置默认账号
7. 执行配置命令
   
   ```bash
   aliyunlog configure "你的AccessKey ID" "你的AccessKey Secret" "cn-hangzhou.log.aliyuncs.com"
   ```
8. 验证配置
   配置文件会自动生成在以下路径：
- Linux/macOS：`~/.aliyunlogcli`
- Windows：`C:\Users\你的用户名\.aliyunlogcli`
  文件内容示例：
  
  ```ini
  [main]
  access-id = LTAI******pLMZ
  access-key = XjAsP******eRqax
  region-endpoint = cn-hangzhou.log.aliyuncs.com
  sts-token =
  ```
  
  ### 配置多账号
1. 执行配置命令（指定配置名称）
   
   ```bash
   aliyunlog configure "你的AccessKey ID" "你的AccessKey Secret" "cn-shanghai.log.aliyuncs.com" "test"
   ```
2. 使用指定账号执行命令
   
   ```bash
   aliyunlog log get_log ... --client-name=test
   ```
   
   ### 全局输出格式配置
- 全局配置JSON格式化输出
  
  ```bash
  aliyunlog configure --format-output=json
  ```
- 全局配置不转义非英文字符（解决中文乱码）
  
  ```bash
  aliyunlog configure --format-output=no_escape
  ```
- 组合配置（推荐）
  
  ```bash
  aliyunlog configure --format-output=json,no_escape
  ```
  
  ### 特殊字符转义
  
  当查询语句包含`$`、`` ` ``、`\`、`!`等特殊字符时，需使用以下两种方式之一转义：
1. 反斜线转义
   
   ```bash
   --query="event_name:\$_enter"
   ```
2. 单引号强制引用（推荐）
   
   ```bash
   --query='event_name:$_enter'
   ```
   
   ## 触发词
- 阿里云日志查询
- SLS日志查询
- aliyun log get
- 查询阿里云日志
- SLS日志分析
  
  ## 参数定义
  
  ### 业务参数
  
  | 参数名       | 类型      | 是否必选 | 默认值   | 描述                                                                                                    |
  | --------- | ------- | ---- | ----- | ----------------------------------------------------------------------------------------------------- |
  | project   | string  | 是    | -     | 阿里云SLS Project名称                                                                                      |
  | logstore  | string  | 是    | -     | 阿里云SLS Logstore名称                                                                                     |
  | from_time | string  | 是    | -     | 查询开始时间，支持两种格式：<br>1. Unix时间戳（秒级）<br>2. `%Y-%m-%d %H:%M:%S<time_zone>` 格式，如 `2026-05-14 18:00:00+8:00` |
  | to_time   | string  | 是    | -     | 查询结束时间，格式同`from_time`                                                                                 |
  | topic     | string  | 否    | ""    | 日志主题，默认空字符串                                                                                           |
  | query     | string  | 否    | "*"   | 查询语句或SQL分析语句，默认查询所有日志                                                                                 |
  | reverse   | boolean | 否    | false | 仅基础查询有效，是否按时间戳降序返回日志<br>true：降序<br>false：升序（默认）                                                       |
  | offset    | integer | 否    | 0     | 仅基础查询有效，查询开始行偏移量                                                                                      |
  | size      | integer | 否    | 100   | 仅基础查询有效，返回最大日志条数，范围0-100                                                                              |
  | power_sql | boolean | 否    | false | 是否使用SQL独享版<br>true：使用独享版<br>false：使用普通版（默认）                                                           |
  
  ### 全局参数（可选）
  
  | 参数名             | 类型     | 是否必选 | 示例值                          | 描述                          |
  | --------------- | ------ | ---- | ---------------------------- | --------------------------- |
  | access-id       | string | 否    | LTAI****************         | 阿里云AccessKey ID，优先级高于配置文件   |
  | access-key      | string | 否    | yourAccessKeySecret          | 阿里云AccessKey Secret         |
  | sts-token       | string | 否    | -                            | STS临时访问令牌                   |
  | region-endpoint | string | 否    | cn-hangzhou.log.aliyuncs.com | SLS服务入口域名                   |
  | client-name     | string | 否    | test                         | 使用指定的多账号配置名称                |
  | profile         | string | 否    | akProfile                    | 使用阿里云CLI配置文件中的凭证            |
  | format-output   | string | 否    | json,no_escape               | 输出格式，支持组合：json、no_escape    |
  | jmes-filter     | string | 否    | "data[*].status"             | JMES语法表达式，过滤返回结果            |
  | decode-output   | string | 否    | utf8                         | 二进制日志解码方式，支持utf8、latin1、gbk |
  
  ## 命令模板
  
  ```bash
  aliyunlog log get_log \
  --project="{{project}}" \
  --logstore="{{logstore}}" \
  --from_time="{{from_time}}" \
  --to_time="{{to_time}}" \
  {{#if topic}}--topic="{{topic}}"{{/if}} \
  {{#if query}}--query="{{query}}"{{/if}} \
  {{#if reverse}}--reverse={{reverse}}{{/if}} \
  {{#if offset}}--offset={{offset}}{{/if}} \
  {{#if size}}--size={{size}}{{/if}} \
  {{#if power_sql}}--power_sql={{power_sql}}{{/if}} \
  {{#if access-id}}--access-id="{{access-id}}"{{/if}} \
  {{#if access-key}}--access-key="{{access-key}}"{{/if}} \
  {{#if sts-token}}--sts-token="{{sts-token}}"{{/if}} \
  {{#if region-endpoint}}--region-endpoint="{{region-endpoint}}"{{/if}} \
  {{#if client-name}}--client-name="{{client-name}}"{{/if}} \
  {{#if profile}}--profile="{{profile}}"{{/if}} \
  {{#if jmes-filter}}--jmes-filter="{{jmes-filter}}"{{/if}} \
  {{#if decode-output}}--decode-output="{{decode-output}}"{{/if}} \
  --format-output={{format_output|default("json,no_escape")}}
  ```
  
  ## 使用示例
  
  ### 示例1：基础日志查询（获取最近100条INFO级别日志）
  
  ```
  用户输入：查询阿里云日志 project=aliyun-test-project logstore=logstore-a from_time="2026-05-14 18:00:00+8:00" to_time="2026-05-14 18:30:00+8:00" query="level:INFO" reverse=true
  ```
  
  生成命令：
  
  ```bash
  aliyunlog log get_log \
  --project="aliyun-test-project" \
  --logstore="logstore-a" \
  --from_time="2026-05-14 18:00:00+8:00" \
  --to_time="2026-05-14 18:30:00+8:00" \
  --query="level:INFO" \
  --reverse=true \
  --format-output=json,no_escape
  ```
  
  ### 示例2：SQL分析查询（统计不同状态码的请求数）
  
  ```
  用户输入：阿里云日志分析 project=aliyun-test-project logstore=logstore-a from_time="2026-05-14 00:00:00+8:00" to_time="2026-05-14 18:30:00+8:00" query="* | select status,COUNT(*) as pv group by status order by pv desc limit 20"
  ```
  
  生成命令：
  
  ```bash
  aliyunlog log get_log \
  --project="aliyun-test-project" \
  --logstore="logstore-a" \
  --from_time="2026-05-14 00:00:00+8:00" \
  --to_time="2026-05-14 18:30:00+8:00" \
  --query="* | select status,COUNT(*) as pv group by status order by pv desc limit 20" \
  --format-output=json,no_escape
  ```
  
  ### 示例3：使用全局参数指定临时凭证
  
  ```
  用户输入：SLS临时查询 project=aliyun-test-project logstore=logstore-a from_time="2026-05-14 12:00:00+8:00" to_time="2026-05-14 18:30:00+8:00" access-id="LTAI******" access-key="XjAsP******" region-endpoint="cn-beijing.log.aliyuncs.com"
  ```
  
  生成命令：
  
  ```bash
  aliyunlog log get_log \
  --project="aliyun-test-project" \
  --logstore="logstore-a" \
  --from_time="2026-05-14 12:00:00+8:00" \
  --to_time="2026-05-14 18:30:00+8:00" \
  --access-id="LTAI******" \
  --access-key="XjAsP******" \
  --region-endpoint="cn-beijing.log.aliyuncs.com" \
  --format-output=json,no_escape
  ```
  
  ### 示例4：使用JMES过滤结果（只返回状态码字段）
  
  ```
  用户输入：查询阿里云日志 project=aliyun-test-project logstore=logstore-a from_time="2026-05-14 18:00:00+8:00" to_time="2026-05-14 18:30:00+8:00" jmes-filter="data[*].status"
  ```
  
  生成命令：
  
  ```bash
  aliyunlog log get_log \
  --project="aliyun-test-project" \
  --logstore="logstore-a" \
  --from_time="2026-05-14 18:00:00+8:00" \
  --to_time="2026-05-14 18:30:00+8:00" \
  --jmes-filter="data[*].status" \
  --format-output=json,no_escape
  ```
  
  ## 重要注意事项
1. **SQL分析查询特殊规则**：当`query`参数包含SQL分析语句时，`reverse`、`offset`、`size`参数无效，必须通过SQL语句的`ORDER BY`指定排序，通过`LIMIT`语法实现分页
2. **时间格式要求**：必须指定时区，中国区建议使用`+8:00`时区，如`2026-05-14 18:30:00+8:00`
3. **返回条数限制**：基础查询单次最多返回100条日志，如需更多数据请使用分页查询
4. **SQL独享版**：除了通过`power_sql=true`参数开启外，也可以在`query`语句中添加`set session parallel_sql=true;`
5. **凭证安全**：避免在命令行明文输入AccessKey，优先使用配置文件或环境变量方式
6. **特殊字符处理**：查询语句包含特殊字符时，必须使用单引号引用或反斜线转义
7. **多账号使用**：跨账号操作时，使用`--client-name`指定配置名称，或通过`--profile`使用阿里云CLI凭证
   
   ## 返回结果说明
   
   返回结果为JSON格式，主要包含两部分：
- `data`：查询结果数据数组，包含日志字段和分析结果
- `meta`：查询元信息，包括执行状态、处理行数、CPU耗时、是否准确等
  示例返回结果：
  
  ```json
  {
  "data": [
  {
  "__source__": "192.168.1.100",
  "__time__": "1747297200",
  "pv": "1256",
  "status": "200"
  },
  {
  "__source__": "192.168.1.101",
  "__time__": "1747297200",
  "pv": "42",
  "status": "500"
  }
  ],
  "meta": {
  "count": 2,
  "isAccurate": true,
  "progress": "Complete",
  "processedRows": 1298,
  "cpuSec": 0.032,
  "elapsedMillisecond": 15
  }
  }
  ```
  
  ## 错误处理与常见问题
  
  | 错误现象                                                | 可能原因                      | 解决方法                                 |
  | --------------------------------------------------- | ------------------------- | ------------------------------------ |
  | 命令未找到：aliyunlog                                     | Python环境变量未配置或CLI未安装      | 检查Python环境变量，重新执行安装命令                |
  | 权限不足：Unauthorized                                   | AccessKey错误或无SLS操作权限      | 验证AccessKey有效性，为RAM用户授予SLS相关权限       |
  | 服务不可达：Connection refused                            | Endpoint错误或网络不通           | 检查region-endpoint是否正确，确认网络可访问SLS服务入口 |
  | 时间格式错误                                              | 未指定时区或格式不正确               | 使用`%Y-%m-%d %H:%M:%S+8:00`格式，确保时区正确  |
  | SQL语法错误                                             | 分析语句语法不正确                 | 检查SQL语句，参考SLS查询分析语法文档                |
  | 中文显示乱码                                              | 输出未配置no_escape            | 添加`--format-output=json,no_escape`参数 |
  | 参数无效：offset/size                                    | 使用了SQL分析语句但仍传入offset/size | 移除offset/size参数，使用SQL的LIMIT语法分页      |
  | 需要我帮你补充**自动分页查询**和**批量导出日志**的高级用法示例，让这个技能支持更多实际场景吗？ |                           |                                      |
