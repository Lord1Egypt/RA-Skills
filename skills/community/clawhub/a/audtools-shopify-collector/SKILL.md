---
name: audtools-shopify-collector
description: AudTools Shopify 批量采集器 - 读取 CSV 中的分类链接，批量自动提交到 https://www.audtools.com，自动填充链接、设置商品数量为 9999，间隔 2 秒提交，完成批量采集商品。
allowed-tools: exec, read, write, edit
---

# AudTools Shopify 批量采集器

自动批量采集 Shopify 分类商品到 AudTools 网站，支持从 CSV 读取链接，自动填充、设置数量，间隔提交。

## 功能特点

- ✅ 读取 CSV 文件中的"完整链接"列
- ✅ 自动打开 AudTools 网站
- ✅ 检测是否需要登录，需要登录会提醒你手动登录
- ✅ 依次在输入框填入每个链接
- ✅ 自动设置商品数量为 9999
- ✅ 点击提交，每条操作间隔 2 秒
- ✅ 完全自动化，不需要手动操作

## 使用方法

```bash
# 默认 CSV 读取默认路径 C:\workspace\caiji\shop-futvortexstore-com-categories.csv
node batch-collect.js

# 指定 CSV 文件路径
node batch-collect.js C:\path\to\your\categories.csv
```

## 工作流程

1. **自动流程：
1. 打开 `https://www.audtools.com/users/shopns#/users/shopns/collecs`
2. 检测是否有登录表单，如果有会暂停，请你手动登录
3. 登录完成后继续执行
4. 读取 CSV 中"完整链接"列的每个链接
5. 在输入框填入链接，设置商品数量为 9999
6. 点击提交
7. 等待 2 秒
8. 处理下一个链接
9. 全部完成后暂停，你可以在浏览器导出结果

## CSV 格式要求

CSV 需要有一列叫 **完整链接**，每个单元格是分类页面的完整 URL。就是 category-collector 输出的 CSV 格式正好匹配，可以直接使用。

## 示例

配合 category-collector 使用：

1. 先用 `category-collector` 采集 Shopify 分类得到 CSV
2. 然后用 `audtools-shopify-collector` 批量提交到 AudTools 采集商品

```bash
# 第一步：采集分类
node category-collector/collect.js https://shop-futvortexstore.com/ C:\workspace\caiji

# 第二步：批量提交到 AudTools
node audtools-shopify-collector/batch-collect.js C:\workspace\caiji\shop-futvortexstore-com-categories.csv
```

## 安装依赖

```bash
npm install
```

依赖：
- playwright (已经安装)
- csv-parser (新增，需要安装)

## 作者

Created by OpenClaw 自动生成，根据需求定制

