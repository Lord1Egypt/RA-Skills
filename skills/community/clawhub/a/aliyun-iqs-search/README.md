# 阿里云IQS搜索技能

这是一个基于阿里云信息查询服务（Intelligent Query Service, IQS）UnifiedSearch API的搜索技能。

## 环境配置

需要在 `.env` 文件中配置以下环境变量：

```env
ALI_IQS_API_KEY=你的阿里云IQS API密钥
```

API密钥可以在阿里云控制台的IQS服务中获取。

## 使用方法

```bash
# 基本搜索
node skills/aliyun-iqs-search/scripts/search.mjs "搜索关键词"

# 示例
node skills/aliyun-iqs-search/scripts/search.mjs "浩卡联盟"
```

## 输出格式

返回JSON格式的结果，包含：
- `success`: 是否成功
- `data.web`: 搜索结果数组，每个结果包含：
  - `title`: 标题
  - `url`: 链接  
  - `description`: 描述内容
  - `score`: 相关性分数
  - `position`: 排名位置

## 特点

- 使用阿里云官方IQS UnifiedSearch API
- 返回高质量、相关性强的搜索结果
- 支持中文搜索优化
- 结果包含相关性评分，便于筛选

## 注意事项

- 需要有效的阿里云IQS API密钥
- API调用可能有配额限制，请参考阿里云官方文档
- 搜索结果会自动过滤低质量内容（分数>0.5）