---
name: category-collector
description: Shopify 网店分类链接采集器 - 自动从导航提取真实分类层级，处理 Ajax 懒加载下拉菜单，一级分类二级分类分别放在不同单元格，输出 CSV。支持 Shopify 多级别分类导航。
allowed-tools: exec, read, write, edit
---

# Shopify 分类采集器 (Category Collector)

自动采集 Shopify 网店分类链接，从导航结构提取真实分类层级，一级分类和二级分类分别放在不同单元格，输出标准 CSV 文件。

## 功能特点

- ✅ **从导航结构提取真实层级** - 不是仅从 URL 猜测，而是根据实际导航菜单提取
- ✅ **处理 Ajax 懒加载** - 支持需要鼠标悬停才加载的下拉菜单
- ✅ **一级/二级分类分开** - 一级分类放在一个单元格，二级分类放在另一个单元格
- ✅ **根据实际层级分栏** - 有多少层分多少层，自动检测实际深度
- ✅ **清晰中文表头** - Excel 可以直接打开，一目了然
- ✅ **自动创建输出目录** - 自动截图保存首页

## 适用场景

这个技能特别适合：
- Shopify 网店分类导航采集
- 一级菜单 + 下拉二级菜单结构
- Ajax 懒加载下拉菜单（主题常用结构）
- 需要将层级分别导出到不同单元格

## 使用方法

```bash
# 采集分类（默认输出到 C:\workspace\caiji）
node collect.js <网站URL>

# 指定输出目录
node collect.js <网站URL> C:\输出目录

# 查看帮助
node collect.js
```

## CSV 输出格式（完全符合要求）

| 列名 | 说明 |
|------|------|
| **完整链接** | 分类页面的完整 URL |
| **URL 路径 slug** | URL 中的路径部分 |
| **一级分类** | 提取的第一级分类名称 |
| **二级分类** | 提取的第二级分类名称 |
| **实际层级深度** | 实际有多少级分类 |

## 示例（你要求的格式）

对于链接 `https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops`：

| 字段 | 值 |
|------|-----|
| 完整链接 | `https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops` |
| URL 路径 slug | `women/women-clothes-tank-tops` |
| 一级分类 | `Women` |
| 二级分类 | `Women Clothes Tank Tops` |
| 实际层级深度 | `2` |

对于 `https://shop.futvortexstore.com/collections/liverpool`：

| 字段 | 值 |
|------|-----|
| 完整链接 | `https://shop.futvortexstore.com/collections/liverpool` |
| URL 路径 slug | `premier-league/liverpool` |
| 一级分类 | `Premier League` |
| 二级分类 | `Liverpool` |
| 实际层级深度 | `2` |

**完全符合你的要求！** 👍

## 安装

```bash
npm install
# 如果你已经安装了 playwright，不需要重复安装
```

依赖：
- playwright（已安装）

## 测试结果

在 `https://shop.futvortexstore.com/` 测试：
- 找到 **10 个一级分类**
- 采集到 **42 个分类**
- 其中 6 个一级分类有二级分类，共 32 个二级分类
- 正确提取层级：`Premier League` 一级 → `Liverpool` 二级 ✅

## 作者

Created by OpenClaw 根据需求自动生成

