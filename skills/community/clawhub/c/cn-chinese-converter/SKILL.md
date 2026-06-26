slug: cn-chinese-converter
name: 中文繁简转换
version: "1.0.0"
author: 千策

# 中文繁简转换

中文简繁转换工具。两岸三地内容适配必备。

## 功能

- **简体→繁体**：中国大陆简体转台湾/香港繁体
- **繁体→简体**：繁体转大陆简体
- **词汇适配**：不同地区的用词差异（软件→軟體、网络→網路）
- **批量处理**：支持多行文本同时转换

## 安装要求

- Python 3.6+
- 外部依赖：opencc-python-reimplemented

## 使用方法

```bash
# 简体转繁体
python3 scripts/chinese_converter.py "s2t 人工智能正在改变世界"

# 繁体转简体
python3 scripts/chinese_converter.py "t2s 人工智慧正在改變世界"
```

## 示例

输入：`s2t 人工智能正在改变世界`
输出：`人工智慧正在改變世界`

## 分类

生产力工具

## 关键词

中文, 简体, 繁体, 转换, opencc, chinese

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
