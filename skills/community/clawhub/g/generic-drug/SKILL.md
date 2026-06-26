# generic_drug 技能

## 描述

通过搜索查询药品的通用名。当用户提供药品名称时，尝试查询其通用名。

## 功能

- 接受药品名称作为参数
- 使用 SearXNG 本地搜索服务进行查询
- 搜索该药品的通用名信息
- **如果查不到通用名，则默认该名称本身就是通用名**

## 使用方法

```bash
# 查询药品通用名
~/.openclaw/workspace/skills/generic_drug/tool.sh <药品名称>

# 示例
~/.openclaw/workspace/skills/generic_drug/tool.sh 乳膏基质一号
~/.openclaw/workspace/skills/generic_drug/tool.sh 头孢克洛胶囊
```

## 查询逻辑

1. 使用 SearXNG 搜索：`<药品名称> 药品通用名`
2. **返回原始搜索结果**，由当前会话（LLM）智能分析：
   - LLM 基于完整上下文判断通用名
   - 能理解"一般指"、"又称"、"俗称"等多种表述
   - 能区分药品和辅料
   - 能处理复杂情况

## 返回格式

脚本返回 JSON 格式（包含原始搜索结果）：
```json
{
  "drug_name": "药品原始名称",
  "search_count": 搜索结果数量，
  "search_context": "格式化后的搜索结果摘要",
  "note": "需要 LLM 分析"
}
```

**LLM 最终输出格式**：
```json
{
  "drug_name": "药品原始名称",
  "generic_name": "智能识别的通用名",
  "found": true/false,
  "type": "非药品（可选）",
  "note": "LLM 智能识别/未找到/非药品"
}
```

## 配置

- **SearXNG URL**: `http://localhost:8080`
- **搜索格式**: `<query> 药品通用名`
- **分析方式**: 由当前会话 LLM 智能分析搜索结果上下文

## 注意事项

- 药品名称应该准确输入
- 对于非药品（如辅料、基质），可能查不到通用名，将返回原名称
- SearXNG 服务需要正常运行

## 示例

```bash
# 查询"乳膏基质一号"
$ generic_drug 乳膏基质一号
{
  "drug_name": "乳膏基质一号",
  "generic_name": "乳膏基质一号",
  "found": true,
  "note": "未找到其他通用名，原名称即为通用名"
}

# 查询"头孢克洛胶囊"
$ generic_drug 头孢克洛胶囊
{
  "drug_name": "头孢克洛胶囊",
  "generic_name": "头孢克洛",
  "found": true,
  "note": "查得通用名为：头孢克洛"
}
```
