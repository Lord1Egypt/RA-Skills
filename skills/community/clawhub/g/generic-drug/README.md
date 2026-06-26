# generic_drug 技能

## 概述

查询药品通用名的工具，当查不到通用名时，默认原名称即为通用名。

## 快速开始

```bash
# 查询药品通用名
~/.openclaw/workspace/skills/generic_drug/tool.sh 乳膏基质一号
~/.openclaw/workspace/skills/generic_drug/tool.sh 头孢克洛胶囊
```

## 使用方法

### 基本用法

```bash
./tool.sh <药品名称>
```

### 参数

- `药品名称`: 必填参数，需要查询通用名的药品名称

## 查询逻辑

1. **构建搜索词**: `<药品名称> 药品通用名`
2. **调用 SearXNG**: 使用本地 SearXNG 服务进行搜索
3. **分析结果**:
   - 搜索返回结果 > 0 → 分析内容是否包含通用名信息
   - 搜索返回结果 = 0 → 返回原名称作为通用名
4. **返回结果**: JSON 格式

## 返回格式

```json
{
  "drug_name": "原始药品名称",
  "generic_name": "查询到的通用名",
  "found": true,
  "note": "说明信息"
}
```

## 配置要求

- **SearXNG 服务**: 运行在 `http://localhost:8080`
- **Python3**: 需要 `python3` 用于 JSON 处理

## 测试

```bash
# 测试 1: 非药品名称（如辅料）
$ ./tool.sh 乳膏基质一号
{"drug_name": "乳膏基质一号", "generic_name": "乳膏基质一号", "found": true, "note": "未找到其他通用名，原名称即为通用名"}

# 测试 2: 具体药品名称
$ ./tool.sh 头孢克洛胶囊
# 可能返回包含通用名信息的复杂结果
```

## 注意事项

1. 需要 SearXNG 服务正常运行
2. 搜索结果分析基于简单的文本匹配
3. 对于复杂的药品名，可能需要手动调整查询逻辑
4. 非药品（如辅料、基质）会返回原名称

## 维护

- 定期更新 SearXNG 搜索逻辑
- 优化通用名提取算法
- 测试各种药品名称的查询效果

## 依赖

- bash
- curl
- python3
