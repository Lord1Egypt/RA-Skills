slug: cn-json-tools
name: JSON工具箱
version: "1.0.0"
author: 千策

# JSON工具箱

JSON格式化、比对、提取、压缩。

## 核心功能
- **format**：格式化JSON（缩进美化）
- **diff**：比对两个JSON文件的差异
- **extract**：从JSON中提取指定路径字段
- **minify**：压缩JSON（去除空白）
- **validate**：验证JSON格式是否合法

## 使用场景
- 调试API返回数据
- 对比两个配置文件差异
- 从复杂JSON中提取关键字段
- 压缩JSON用于配置文件

## 使用方式
```bash
# 格式化
python ~/.qclaw/skills/cn-json-tools/json_tool.py format "{\"a\":1,\"b\":2}"

# 比对
python ~/.qclaw/skills/cn-json-tools/json_tool.py diff file1.json file2.json

# 提取
python ~/.qclaw/skills/cn-json-tools/json_tool.py extract "{\"user\":{\"name\":\"张三\"}}" "user.name"

# 压缩
python ~/.qclaw/skills/cn-json-tools/json_tool.py minify "{\"a\":1,\"b\":2}"

# 验证
python ~/.qclaw/skills/cn-json-tools/json_tool.py validate "{\"a\":1}"
```

## 依赖
- Python3（标准库，无需安装任何包）

## 标签
cn, json, tools, format, diff, formatter

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
