---
name: category-link-collector
description: 采集电商网站分类链接信息，提取分类层级数据并保存为CSV文件。当需要从电商网站分类链接中提取结构化数据时使用此技能。
---

# Category Link Collector Skill

## 功能
- 从给定的分类链接URL中提取分类信息
- 解析分类路径，提取一级和二级分类
- 生成结构化的CSV文件
- 支持自定义输出目录和文件名

## 使用方法

### 基本用法
```
采集以下分类链接：
https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops
https://lulumonclick-eu.shop/collections/women-women-clothes-bras-underwear
```

### 参数说明
- **域名变量**: 自动从链接中提取域名部分
- **输出目录**: 默认为 `/Users/zhangqirong/工作/caiji`，可自定义
- **文件名**: 自动使用域名作为文件名（如 `lulumonclick-eu.shop.csv`）

## 数据结构
生成的CSV文件包含以下列：
1. **完整链接**: 原始分类链接
2. **分类路径**: 从URL中提取的分类路径（如 `women-women-clothes-tank-tops`）
3. **域名**: 网站域名
4. **1级分类**: 提取的一级分类名称（如 `Women`）
5. **2级分类**: 提取的二级分类名称（如 `Tank Tops`）
6. **3级分类**: 提取的三级分类名称（如存在）
7. **4级分类**: 提取的四级分类名称（如存在）
8. **...**: 更多级别分类（根据实际深度动态生成）

## 多级分类支持
技能现在支持无限级分类提取：
- 自动识别分类层级深度
- 动态生成CSV列（1级分类、2级分类、3级分类...）
- 智能合并特殊词组（T-shirts, Co-ord等）
- 正确处理数字范围（0-18 months等）

## 处理逻辑
1. 从URL中提取域名部分
2. 从 `/collections/` 后提取分类路径
3. 解析分类路径：
   - 使用智能算法分割分类路径
   - 识别一级分类（Women, Men, Kids, Beauty等）
   - 提取所有级别的下级分类
   - 智能合并特殊词组和数字范围
4. 根据最大分类深度动态生成CSV列
5. 生成CSV文件，保存到指定目录

## 示例
输入链接：
```
https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops
```

输出CSV行：
| 完整链接 | 分类路径 | 一级分类 | 二级分类 | 域名 |
|---------|---------|---------|---------|------|
| https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops | women-women-clothes-tank-tops | Women | Tank Tops | lulumonclick-eu.shop |

## 文件位置
- Skill主文件: `SKILL.md`
- 脚本文件: `scripts/collect_categories.py`
- 配置文件: `config/settings.json` (可选)

## 依赖
- Python 3.x
- pandas 库 (用于CSV处理)

## 扩展能力
后续可以扩展的功能：
1. 批量处理多个链接
2. 支持更多分类层级（三级、四级等）
3. 自动去重和验证
4. 支持不同的URL格式
5. 添加时间戳和采集状态
6. 集成到自动化工作流中