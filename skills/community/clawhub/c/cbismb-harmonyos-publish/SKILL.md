---
name: cbismb-harmonyos-publish
version: 1.0.0
description: 自动发布文章到中小企业IT网 HarmonyOS 板块。当用户要求发布文章到中小企业IT网、cbismb.com、HarmonyOS开发者社区时触发此技能。
license: MIT
input:
  properties:
    category:
      type: string
      description: 文章分类
      default: HarmonyOS
    tags:
      type: string
      description: 文章标签
      default: HarmonyOS
    is_original:
      type: boolean
      description: 是否原创
      default: true
    privacy_agreement:
      type: boolean
      description: 是否勾选隐私声明
      default: true
    enable_comments:
      type: boolean
      description: 是否开启评论
      default: true
---

# 中小企业 IT 网 HarmonyOS 板块文章发布

## 概述

本技能用于自动发布文章到中小企业 IT 网 HarmonyOS 开发者社区板块。

**发布页面地址**: `https://www.cbismb.com/harmonyos/release`

**板块首页**: `https://www.cbismb.com/harmonyos/home`

## 前置条件

- 用户已登录中小企业 IT 网账号
- Chrome 浏览器已附加 OpenClaw Browser Relay 扩展

## 发布流程

### 1. 打开发布页面

```
browser action=open url=https://www.cbismb.com/harmonyos/release
```

### 2. 填写文章内容

| 字段     | 操作                             | 备注               |
| -------- | -------------------------------- | ------------------ |
| **标题** | 点击 `textbox "请输入标题"` 输入 | 限制长度，简洁明了 |
| **正文** | 点击编辑区域 `paragraph` 输入    | 支持 Markdown 格式 |

### 3. 设置文章属性

| 属性             | 选择路径/操作                                                                    |
| ---------------- | -------------------------------------------------------------------------------- |
| **分类**         | 优先使用用户输入的 `category` (默认: HarmonyOS)。路径参考: 操作系统 > [category] |
| **标签**         | 优先使用用户输入的 `tags` (默认: HarmonyOS)。点击 `+` 按钮，输入标签名后按 Enter |
| **是否原创**     | 根据用户输入的 `is_original` (默认: true) 设置开关状态                           |
| **是否开启评论** | 根据用户输入的 `enable_comments` (默认: true) 设置开关状态                       |

### 4. 确认发布

1. 根据 `privacy_agreement` (默认: true) 勾选「隐私声明」复选框（勾选后才能发布）
2. 点击「发布」按钮

## 页面元素参考

### 分类选择

```
点击分类下拉框 → 展开"操作系统" → 选择"HarmonyOS" (或用户指定的分类)
```

分类下拉菜单结构：

- 操作系统
  - HarmonyOS
  - OpenHarmony
  - 其它
- 应用开发
- 设备开发
- 框架语言
- 其它

### 常用标签

根据文章内容选择合适的标签：

- HarmonyOS
- HarmonyOS 6
- 鸿蒙生态
- ArkTS
- ArkUI
- 鸿蒙开发

## 注意事项

1. **隐私声明**：原创文章需要勾选隐私声明才能发布
2. **审核机制**：文章发布后可能需要审核，通常 1-3 个工作日
3. **正文统计**：页面底部显示"正文数字"，确保内容完整
4. **保存草稿**：如需暂存，点击「保存草稿」而非「发布」

## 示例用法

**用户请求**：

> 帮我在中小企业 IT 网的 HarmonyOS 板块发布一篇关于 HarmonyOS API 22 的介绍文章

**执行步骤**：

1. 提示用户输入参数（分类、标签、原创、隐私、评论），使用默认值或用户输入
2. 打开发布页面
3. 输入标题：`HarmonyOS API 22 新特性详解`
4. 输入正文（Markdown 格式）
5. 选择分类：操作系统 > [用户输入的分类]
6. 添加标签：[用户输入的标签]
7. 根据输入设置原创和评论开关
8. 根据输入勾选隐私声明
9. 点击发布

## 错误处理

| 问题           | 解决方案                |
| -------------- | ----------------------- |
| 页面无法加载   | 检查网络连接和登录状态  |
| 找不到分类选项 | 确认分类下拉框已展开    |
| 发布按钮无响应 | 检查是否勾选隐私声明    |
| 标签添加失败   | 确保输入后按 Enter 确认 |
