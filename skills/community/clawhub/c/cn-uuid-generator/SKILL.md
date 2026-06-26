name: UUID生成器
version: "1.0.0"
description: "生成多种格式的UUID，包括v1/v4/v5和短UUID，纯Python标准库，无需API Key。"
license: MIT-0
tags:
  - tools

# UUID生成器

UUID 生成器。生成多种格式的唯一标识符。

## 功能

- UUID v4 随机生成
- UUID v1 基于时间戳生成
- UUID v5 基于命名空间生成
- 短 UUID (Base62编码)
- 批量生成
- 纯本地处理，无需API

## 安装要求

- Python 3.6+
- 无外部依赖（使用内置 uuid 模块）

## 使用方法

```
千策，生成一个UUID
千策，生成10个UUID
千策，生成一个短UUID
```

## 参数

- `count`: 生成数量，默认1
- `version`: UUID版本 (1/4/5)，默认4
- `short`: 是否生成短UUID，默认false

## 示例

输入：
```
千策，生成5个UUID
```

输出：
```
a1b2c3d4-e5f6-7890-abcd-ef1234567890
b2c3d4e5-f6a7-8901-bcde-f12345678901
...
```

## 分类

开发

## 关键词

uuid, guid, 唯一标识, identifier, generator

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
