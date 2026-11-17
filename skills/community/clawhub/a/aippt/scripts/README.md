# 接口文档
**返回值通用字段说明**

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| status | int | 是 | 状态码0：成功，非 0 表示失败 | 0 |
| msg | string | 是 | 状态描述 | "success" |


## 获取模板列表
使用分页方式调用该接口可以获取到所有的模板列表。

### API 信息
- **URL**: `https://ppt-api.7niuai.com/ppt/tpl/list`
- **方式**: POST
- **Content-Type**: `application/json`

### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| page | int | 是 | 页码 | 1 |
| num | int | 是 | 每页数量 | 10 |

### 返回值字段说明
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| status | int | 是 | 状态码0：成功，非 0 表示失败 | 0 |
| msg | string | 是 | 状态描述 | "success" |
| data | object | 是 | 数据 | |
| data.count | int | 是 | 总条数 | 10 |
| data.list | array | 是 | 模板列表 | |
| data.list.uuid | string | 是 | 模板 UUID | "e06cfbe4458b180ae9a753ae9a00b03a" |
| data.list.name | string | 是 | 模板名称 | "商务简约风-PPT模板" |
| data.list.thumb | string | 是 | 模板缩略图（横向图） URL | "https://ppt-img.7niuai.com/e06cfbe4458b180ae9a753ae9a00b03a/ae551d409e5d81bb86355a08aacbae30_thumb.jpg" |
| data.list.picture | string | 是 | 模板组合图（竖向图） URL | "https://ppt-img.7niuai.com/e06cfbe4458b180ae9a753ae9a00b03a/ae551d409e5d81bb86355a08aacbae30.jpg" |


### 请求示例
```bash
curl --location 'https://ppt-api.7niuai.com/ppt/tpl/list' \
--header 'X-Platform: web' \
--header 'Content-Type: application/json' \
--data '{
    "page":1, 
    "num": 10
}'
```

### 返回示例
```json
{
    "status": 0,
    "msg": "success",
    "data": {
      "count": 10,
      "list": [
        {
          "uuid": "e06cfbe4458b180ae9a753ae9a00b03a",
          "name": "商务简约风-PPT模板",
          "thumb": "https://ppt-img.7niuai.com/e06cfbe4458b180ae9a753ae9a00b03a/ae551d409e5d81bb86355a08aacbae30_thumb.jpg",
          "picture": "https://ppt-img.7niuai.com/e06cfbe4458b180ae9a753ae9a00b03a/ae551d409e5d81bb86355a08aacbae30.jpg"
        },
        {
          "uuid": "58dc4b5325b4c27dc37d05c29124d712",
          "name": "科技风-机器人-黑色-PPT模板",
          "thumb": "https://ppt-img.7niuai.com/58dc4b5325b4c27dc37d05c29124d712/197080fa293425cc05a385645d2973b0_thumb.png",
          "picture": "https://ppt-img.7niuai.com/58dc4b5325b4c27dc37d05c29124d712/197080fa293425cc05a385645d2973b0.jpg"
        }
      ],
    }
}
```

### 使用示例

```bash
python3 get_template.py --page=1 --num=10
```

### 注意事项
- page 从 1 开始
- num 最大为 10
- 超时时间设置为 30 秒
- thumb 字段为模板首页的缩略图（横向图） URL
- picture 字段为集合图，包含了模板的：首页、目录页、章节页、内容页等多图的组合图（竖向图） URL


## 根据内容生成PPT
根据用户Markdown内容获取一个PPT下载链接的脚本。

### API 信息
- **URL**: `https://ppt-api.7niuai.com/openclaw/generate_ppt_by_content`
- **方式**: POST
- **Content-Type**: `application/json`

### 请求参数
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| tpl_id | string | 是 | 模板 ID | "e06cfbe4458b180ae9a753ae9a00b03a" |
| markdown_content | string | 是 | 最终PPT的 Markdown 内容 | "# 智启未来：AI时代的变革与担当..." |

### 返回值字段说明
| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| status | int | 是 | 状态码0：成功，非 0 表示失败 | 0 |
| msg | string | 是 | 状态描述 | "success" |
| data | object | 是 | 数据 | |
| data.view_url | string | 是 | 生成的PPT连接 | "https://jcppt.com/preview-in-ai/ed0bdb7485..." |

### 请求示例
```bash
curl --location 'https://ppt-api.7niuai.com/openclaw/generate_by_content' \
--header 'token: ODk4Nzg2YMjRmNDM=' \
--header 'Content-Type: application/json' \
--data '{
    "tpl_id": "e06cfbe4458b180ae9a753ae9a00b03a",
    "markdown_content": "# 智启未来：AI时代的变革与担当\n\n> 探讨人工智能发展带来的深刻变革与人类社会的应对之道，展望未来智慧文明新图景\n\n## 智能浪潮的崛起\n\n## 深刻变革的冲击\n\n## 共生共荣的未来......"
}'
```

### 返回示例
```json
{
    "code": 0,
    "msg": "success",
    "time": "2026-03-06 15:10:51",
    "data": {
        "view_url": "https://jcppt.com/preview-in-ai/ed0bdb7485..."
    }
}
```

### 使用示例

```bash
python3 generate_by_content.py --tpl_id=e06cfbe4458b180ae9a753ae9a00b03a --markdown_content="# 智启未来：AI时代的变革与担当\n\n> 探讨人工智能发展带来的深刻变革与人类社会的应对之道，展望未来智慧文明新图景\n\n## 智能浪潮的崛起\n\n## 深刻变革的冲击\n\n## 共生共荣的未来......"
```

### 注意事项
- **markdown_content** ：是用户生成的最终Markdown的内容，并非只有大纲内容。


