# Shopify 分类采集器 (Category Collector)

自动采集 Shopify 网店的所有分类链接，提取多级分类名称，保存为带表头的 CSV 文件。

## 功能

- ✅ 自动提取页面中所有分类链接
- ✅ 自动从 URL slug 解析多级分类
- ✅ 支持 1-4 级分类层级提取
- ✅ 输出标准 CSV 格式，包含清晰的中文表头
- ✅ 自动创建输出目录
- ✅ 自动保存页面截图
- ✅ 支持任意 Shopify 网店
- ✅ 自动去重

## 支持的 URL 格式

这个技能支持：
- `/collections/category-slug` (Shopify 默认)
- `/collections/category/sub-category`
- `/categories/category-slug` 
- `/product-category/category-slug` (WooCommerce)

## 安装

```bash
npm install
# playwright 已经安装过了，如果没有则运行：
# npx playwright install chromium
```

## 使用方法

```bash
# 基本用法（默认输出到 C:\workspace\caiji）
node collect.js https://shop.futvortexstore.com/

# 指定输出目录
node collect.js https://shop.futvortexstore.com/ C:\my-output-folder
```

## CSV 输出格式

| 列名 | 说明 |
|------|------|
| **完整链接** | 分类页面的完整 URL |
| **URL 路径 slug** | URL 中的路径部分 |
| **链接文本** | 页面上显示的链接文字 |
| **一级分类** | 提取的第一级分类名称 |
| **二级分类** | 提取的第二级分类名称 |
| **三级分类** | 提取的第三级分类名称 |
| **四级分类** | 提取的第四级分类名称（完整名称）|
| **层级深度** | 分类深度（单词数量） |

## 示例

输入 URL:  
`https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops`

提取结果：

| 字段 | 值 |
|------|-----|
| 完整链接 | `https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops` |
| URL 路径 slug | `women-women-clothes-tank-tops` |
| 一级分类 | `Women` |
| 二级分类 | `Women Women` |
| 三级分类 | `Women Women Clothes` |
| 四级分类 | `Women Women Clothes Tank Tops` |
| 层级深度 | 4 |

## 示例输出

看看实际采集结果：[示例 CSV](./example-output.csv)

## 作者

由 OpenClaw 自动生成 - 需求提出 & 代码生成 🤖
