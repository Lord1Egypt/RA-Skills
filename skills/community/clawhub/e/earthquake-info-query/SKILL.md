---
name: earthquake-info-query
entry: scripts/main.js
---

# 地震信息查询 Skill

查询中国地震台网中心（CENC）的地震目录数据，支持按震级、时间、地区范围筛选，结果可按时间、震级、深度排序。

## 触发方式

当用户提到以下内容时，调用此 Skill：

- 询问最近/近期/今天的**地震**信息
- 询问某个地区是否有**地震**发生
- 询问某次**地震**的震级、震源深度、位置等详情
- 询问**震级**大于某个值的地震
- 询问**全球**或**中国**范围内的地震情况
- 查询特定**时间段**内的地震记录

关键词：地震、震级、震源、震动、地震台网、地震信息

## 参数说明

调用 execute(input) 时，input 为对象，支持以下字段：

| 参数          | 类型    | 默认值 | 说明                                             |
| ------------- | ------- | ------ | ------------------------------------------------ |
| startMg       | number  | 0      | 最小震级，范围 0-10                              |
| endMg         | number  | 10     | 最大震级，范围 0-10                              |
| locationRange | number  | 1      | 地区范围：1=中国范围，2=全球范围                 |
| orderBy       | string  | id     | 排序字段：id(时间)、magnitude(震级)、depth(深度) |
| isAsc         | boolean | false  | 是否升序排列，false=降序                         |
| startTime     | string  | 3天前  | 起始日期，格式 YYYY-MM-DD HH:mm:ss               |
| endTime       | string  | 今天   | 结束日期，格式 YYYY-MM-DD HH:mm:ss               |

> 所有参数均为可选。不传任何参数时，默认查询最近 3 天中国范围内的全部地震，按时间降序。

## 返回值格式

**成功时：**

    {
      "status": "success",
      "count": 3,
      "data": [
        {
          "id": 12345,
          "oriTime": "2024-04-15 08:30:00",
          "locName": "四川宜宾市珙县",
          "magnitude": 4.5,
          "focDepth": 10,
          "epiLat": 28.45,
          "epiLon": 104.72
        }
      ]
    }

每条记录字段说明：

| 字段      | 说明          |
| --------- | ------------- |
| id        | 地震 ID       |
| oriTime   | 发震时间      |
| locName   | 参考位置名称  |
| magnitude | 震级 (M)      |
| focDepth  | 震源深度 (km) |
| epiLat    | 纬度          |
| epiLon    | 经度          |

**失败时：**

    {
      "status": "error",
      "type": "param_error",
      "message": "参数 startMg 超出范围 [0, 10]，收到: 12"
    }

type 取值：param_error（参数校验错误）、request_error（网络或服务端错误）

## 使用用例

### 用例 1：查询最近3天的地震（默认）

用户：最近有没有地震？

    execute({})

### 用例 2：查询5级以上的地震

用户：最近有没有5级以上的地震？

    execute({ startMg: 5.0 })

### 用例 3：查询特定时间段的地震

用户：2024年1月有哪些地震？

    execute({
      startTime: '2024-01-01 00:00:00',
      endTime: '2024-01-31 23:59:59'
    })

### 用例 4：查询全球范围的地震

用户：全球范围内最近有什么地震？

    execute({ locationRange: 2 })

### 用例 5：按震级排序，查最大的地震

用户：最近最强的地震是哪个？

    execute({ orderBy: 'magnitude', isAsc: false })

### 用例 6：查询3到5级之间的地震，按深度升序

用户：最近3到5级的地震有哪些，按深度从小到大排一下

    execute({
      startMg: 3.0,
      endMg: 5.0,
      orderBy: 'depth',
      isAsc: true
    })

## Agent 提示词

当用户询问关于"地震"、"震动"、"震级"等信息时，请调用此技能。根据用户描述提取对应参数：

- 提到"X级以上" → 设置 startMg 为 X
- 提到"X级以下"或"X级以内" → 设置 endMg 为 X
- 提到"全球" → 设置 locationRange 为 2
- 提到时间范围 → 设置 startTime / endTime
- 提到"最强/最大" → 设置 orderBy: magnitude, isAsc: false
- 提到"最深/最浅" → 设置 orderBy: depth

如果用户没有明确指定参数，使用默认值即可。返回结果后，用自然语言向用户总结地震信息，包括时间、地点、震级和深度。

## 联系作者

- 邮箱：[wang760635994@gmail.com](mailto:wang760635994@gmail.com)
