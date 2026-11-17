---
name: brand-knowledge
description: 品牌知识库,管理品牌名/Slogan/视觉规范/话术模板/品牌调性,支持多品牌切换和品牌一致性检查。触发:品牌创建/品牌查询/内容品牌合规检查
tools: [read, exec]
dependencies: []
metadata:
  openclaw:
    emoji: "🏷️"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: ["python"]
      env: []
      config: []
---

# 品牌知识库

## 使用场景

1. **品牌创建**: 新品牌上线时，定义品牌名/Slogan/品牌故事/调性/视觉规范/话术模板，生成品牌档案并持久化存储
2. **品牌查询**: 内容创作或客服回复时，快速检索品牌调性、视觉规范和话术模板，确保输出与品牌一致
3. **品牌合规检查**: 发布内容前，自动对比品牌调性和话术模板，输出合规度评分和不合规项，防止品牌形象偏移
4. **多品牌切换**: 运营多个品牌时，一键切换活跃品牌，后续所有内容生成自动使用该品牌规范
5. **品牌知识检索**: 通过语义搜索在向量库中检索品牌相关知识，支持模糊查询和跨品牌对比

## 工作流

### 1. 品牌定义

- 输入: 品牌名/Slogan/品牌故事/品牌调性(专业/活泼/温暖/高端)/目标人群/视觉规范(主色/辅色/字体/logo描述)/话术模板(售前/售后/推广)
- 验证: 品牌名非空且唯一，调性必须为[专业/活泼/温暖/高端]之一，主色为合法HEX色值
- 处理: 生成品牌档案JSON，包含brand_id(品牌名kebab-case)、创建时间、完整品牌信息
- 输出: 品牌档案JSON结构

### 2. 知识入库

- 输入: Step1生成的品牌档案JSON
- 处理: 保存到`data/brands/{brand_id}.json`，同步到memory-qdrant向量库(品牌知识可语义检索)
- 降级: memory-qdrant不可用时，仅保存JSON文件，记录降级日志，后续查询走JSON文件检索
- 输出: 入库结果(成功/降级/失败)

### 3. 品牌查询

- 输入: 品牌名或关键词
- 处理: 优先从memory-qdrant语义检索，降级到JSON文件精确匹配+模糊搜索
- 输出: 品牌调性+视觉规范+话术模板，若未找到返回error

### 4. 一致性检查

- 输入: 待发布内容(文本)+目标品牌名
- 处理: 读取品牌档案→对比品牌调性(语气/用词风格)+视觉规范(色彩提及)+话术模板(关键话术匹配)→计算合规度评分(0-100)
- 评分规则: 调性匹配40分+视觉规范匹配30分+话术模板匹配30分
- 输出: 合规度评分+不合规项列表(含具体建议)，评分<60时标记为不合规并建议修改

### 5. 品牌切换

- 输入: 目标品牌名
- 验证: 品牌档案必须存在
- 处理: 更新`data/brands/active_brand.json`为当前活跃品牌
- 输出: 切换结果+当前活跃品牌信息，后续所有内容生成自动使用该品牌规范

## 输入格式

### 品牌定义输入
```json
{
  "action": "create",
  "name": "Light Anchor",
  "slogan": "点亮创意，锚定价值",
  "story": "Light Anchor致力于用AI技术赋能创作者...",
  "tone": "专业",
  "target_audience": "自由职业者/小团队创业者",
  "visual": {
    "primary_color": "#1A5276",
    "secondary_color": "#AED6F1",
    "font": "思源黑体",
    "logo_description": "锚+灯泡融合图标，深蓝色调"
  },
  "templates": {
    "presale": "您好，{brand_name}为您提供{service}，专业可靠有保障。",
    "aftersale": "感谢选择{brand_name}，如有问题随时联系，我们7x24小时为您服务。",
    "promo": "{brand_name}限时优惠，{offer_detail}，立即体验！"
  }
}
```

### 品牌查询输入
```json
{
  "action": "query",
  "keyword": "Light Anchor"
}
```

### 一致性检查输入
```json
{
  "action": "check",
  "brand_name": "Light Anchor",
  "content": "哈喽亲！我们的东西超便宜快来买！"
}
```

### 品牌切换输入
```json
{
  "action": "switch",
  "brand_name": "Amboras"
}
```

## 输出格式

### 品牌定义输出
```json
{
  "success": true,
  "data": {
    "brand_id": "light-anchor",
    "name": "Light Anchor",
    "slogan": "点亮创意，锚定价值",
    "tone": "专业",
    "created_at": "2026-05-20T10:00:00"
  },
  "error": null,
  "code": null
}
```

### 一致性检查输出
```json
{
  "success": true,
  "data": {
    "score": 35,
    "compliant": false,
    "violations": [
      {"category": "调性不匹配", "detail": "内容语气过于随意，品牌调性为'专业'", "suggestion": "改用正式商务用语"},
      {"category": "话术模板不匹配", "detail": "未使用品牌标准售前话术", "suggestion": "参考模板: '您好，Light Anchor为您提供...'"}
    ]
  },
  "error": null,
  "code": null
}
```

## 异常处理

| 异常场景 | 处理方式 | 错误码 |
|:---------|:---------|:-------|
| 品牌档案不存在 | 返回error+建议先创建品牌 | BRAND_NOT_FOUND |
| 品牌名已存在 | 返回error+提示使用update或换名 | BRAND_EXISTS |
| 调性值非法 | 返回error+列出合法调性值[专业/活泼/温暖/高端] | INVALID_TONE |
| memory-qdrant不可用 | 降级到JSON文件检索，记录降级日志 | QDRANT_FALLBACK |
| 一致性检查评分<60 | 标记不合规，列出具体不合规项和修改建议 | COMPLIANCE_LOW |
| 活跃品牌未设置 | 返回error+提示先switch设置活跃品牌 | NO_ACTIVE_BRAND |
| JSON文件读写失败 | 返回error+检查文件权限和路径 | IO_ERROR |

## 示例

### 示例1: 创建品牌

```
用户: 创建品牌Light Anchor，Slogan"点亮创意，锚定价值"，调性专业，目标人群自由职业者
执行: python skills/brand-knowledge/scripts/brand_manager.py create --name "Light Anchor" --slogan "点亮创意，锚定价值" --tone 专业 --target-audience "自由职业者"
结果: 品牌档案已保存到data/brands/light-anchor.json，向量库同步成功
```

### 示例2: 一致性检查

```
用户: 检查这段内容是否符合Light Anchor品牌: "哈喽亲！超值优惠快来抢！"
执行: python skills/brand-knowledge/scripts/brand_manager.py check --brand "Light Anchor" --content "哈喽亲！超值优惠快来抢！"
结果: 合规度35分(不合规)，调性不匹配(随意vs专业)，话术不匹配(未使用标准模板)
```

### 示例3: 品牌切换

```
用户: 切换到Amboras品牌
执行: python skills/brand-knowledge/scripts/brand_manager.py switch --brand "Amboras"
结果: 活跃品牌已切换为Amboras，后续内容生成将使用Amboras品牌规范
```
