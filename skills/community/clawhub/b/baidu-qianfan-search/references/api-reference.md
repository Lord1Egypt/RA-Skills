# 百度千帆搜索API参考文档

**重要提示：这是百度千帆搜索API，不是普通的百度网页搜索。** 百度千帆搜索是百度智能云千帆平台的企业级搜索API，需要单独申请API Key。

## 基础信息
| 项 | 值 |
|----|----|
| 请求端点 | `https://qianfan.baidubce.com/v2/ai_search/web_search` |
| 请求方法 | POST |
| 认证方式 | Bearer Token（AppBuilder API Key） |
| 内容类型 | application/json |

## 请求参数说明

### 1. messages (必选)
搜索输入，仅支持单轮对话，取最后一条user的content作为搜索query。

| 字段 | 类型 | 必选 | 说明 |
|------|------|------|------|
| role | string | 是 | 角色，固定为 `user` |
| content | string | 是 | 搜索关键词，长度限制72个字符以内（1汉字=2字符），过长自动截断 |

### 2. edition (可选)
搜索版本，默认 `standard`
- `standard`: 完整版本，效果最好
- `lite`: 轻量版本，时延更低，效果略弱

### 3. search_source (可选)
搜索引擎版本，固定值：`baidu_search_v2`

### 4. resource_type_filter (可选)
资源类型过滤，默认值：
```json
[
  {"type": "web","top_k": 20},
  {"type": "video","top_k": 0},
  {"type": "image","top_k": 0},
  {"type": "aladdin","top_k": 0}
]
```

| 字段 | 类型 | 必选 | 说明 |
|------|------|------|------|
| type | string | 是 | 资源类型：`web`(网页)/`video`(视频)/`image`(图片)/`aladdin`(阿拉丁) |
| top_k | integer | 是 | 返回个数上限：<br>web最大50<br>video最大10<br>image最大30<br>aladdin最大5 |

> 注意：阿拉丁不支持站点和时效过滤，返回参数为beta版本

### 5. search_filter (可选)
搜索过滤条件

#### 5.1 match (可选)
条件查询
```json
"match": {
  "site": ["www.weather.com.cn", "baidu.com"]
}
```
- `site`: 只返回指定站点的搜索结果，包含子站点

#### 5.2 range (可选)
范围查询，支持日期和数值类型
```json
"range": {
  "page_time": {
    "gte": "2025-01-01",
    "lte": "2025-12-31"
  }
}
```

**时间表达式说明：**
- 固定日期格式：`YYYY-MM-DD`
- 相对时间表达式：
  - `now/d`: 当天
  - `now-1w/d`: 最近一周
  - `now-2d/d`: 最近两天
  - `now-1M/d`: 最近一个月
  - `now-3M/d`: 最近三个月
  - `now-6M/d`: 最近六个月
  - `now-1y/d`: 最近一年
- 比较符：
  - `gte`: 大于等于
  - `gt`: 大于
  - `lte`: 小于等于
  - `lt`: 小于

> 注意：gte/gt只需传一个，都传仅gt生效；lte/lt同理

#### 5.3 block_websites (可选)
屏蔽站点列表，数组格式
```json
"block_websites": ["tieba.baidu.com", "blog.csdn.net"]
```

### 6. search_recency_filter (可选)
快速时效性过滤，枚举值：
- `week`: 最近7天
- `month`: 最近30天
- `semiyear`: 最近180天
- `year`: 最近365天

### 7. safe_search (可选)
安全搜索开关，默认`false`
- `true`: 开启严格风控，过滤涉黄涉恐内容
- `false`: 关闭安全搜索

### 8. config_id (可选)
query干预配置ID，用于自定义干预策略，默认空

## 常见用例示例

### 示例1：基础网页搜索
```bash
node {baseDir}/scripts/search.mjs "北京有哪些旅游景区"
```

### 示例2：限定站点搜索
```bash
node {baseDir}/scripts/search.mjs "北京天气" --site "www.weather.com.cn"
```

### 示例3：时间范围搜索
```bash
# 最近7天
node {baseDir}/scripts/search.mjs "人工智能最新进展" --time week

# 过去48小时
node {baseDir}/scripts/search.mjs "AC米兰新闻" --from "now-2d/d" --to "now/d"
```

### 示例4：多资源类型搜索
```bash
node {baseDir}/scripts/search.mjs "北京故宫" --types web,image,video
node {baseDir}/scripts/search.mjs "北京故宫" --types web:10,image:5,video:3
```

### 示例5：屏蔽特定站点
```bash
node {baseDir}/scripts/search.mjs "Python教程" --block "csdn.net" --block "jianshu.com"
```

## 返回参数说明
```json
{
  "request_id": "ca749cb1-26db-4ff6-9735-f7b472d59003",
  "code": "错误码（异常时返回）",
  "message": "错误消息（异常时返回）",
  "references": [
    {
      "id": 1,
      "title": "网页标题",
      "url": "https://example.com/page.html",
      "web_anchor": "网站锚文本",
      "website": "站点名称",
      "snippet": "搜索摘要",
      "content": "网页内容片段",
      "date": "2025-05-23 11:58:00",
      "type": "web",
      "icon": "网站图标地址",
      "image": "图片详情（图片类型返回）",
      "video": "视频详情（视频类型返回）",
      "is_aladdin": false,
      "aladdin": "阿拉丁内容（阿拉丁类型返回）"
    }
  ]
}
```

## 错误码说明
| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 401 | 认证失败 | 检查API Key是否正确 |
| 400 | 参数错误 | 检查请求参数格式是否正确 |
| 403 | 权限不足 | 确认账号已开通该API服务 |
| 429 | 请求超限 | 降低请求频率 |
| 500 | 服务器错误 | 重试或联系客服 |

## 注意事项
1. 关键词长度限制72字符，过长会自动截断，建议控制在36个汉字以内
2. 时间范围查询时，gte和lte需同时存在才会生效
3. 阿拉丁资源不支持站点和时间过滤，建议搭配网页资源使用
4. 站点过滤支持同时指定多个站点，会返回任意匹配站点的结果
5. 屏蔽站点和指定站点可以同时使用，会先过滤屏蔽站点再匹配指定站点
