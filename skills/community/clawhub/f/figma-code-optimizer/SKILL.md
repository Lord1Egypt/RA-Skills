---
name: figma-code-optimizer
description: 从Figma设计稿生成符合项目组件库和设计规范的高质量前端代码
version: 1.0.0
tags:
  - figma
  - code-generation
  - react
  - design-system
---

# Figma 代码生成优化技能

## 📋 技能概述
这个技能帮助AI代理从Figma设计稿生成代码时，能够：
1. **识别并复用**你项目中的现有组件库
2. **遵循**你的设计规范（颜色token、间距规则、字体系统）
3. **生成**结构清晰、可维护的生产级代码
4. **避免**常见的代码生成问题（如硬编码值、嵌套过深）

## 🔍 使用前提

### 在Figma中的准备
为了获得最佳效果，用户的Figma设计稿应该满足以下条件[citation:1][citation:6]：

| 要求 | 说明 | 为什么重要 |
|------|------|------------|
| **使用组件和变体** | 将重复元素转为Component，用Variants表示不同状态 | AI能将它们映射为代码组件和props |
| **应用Auto Layout** | 用自动布局代替手动排列 | 便于转换为flex/grid布局 |
| **使用样式和变量** | 统一用颜色样式、文字样式、间距变量 | 避免生成硬编码值 |
| **图层命名清晰** | 避免"Frame 42"、"Group Copy"这类自动命名 | 帮助AI理解每个元素的作用 |
| **避免过度嵌套** | 保持图层层级尽量浅 | 防止生成冗余的div嵌套 |
| **优先使用Frame** | 用Frame而不是Group作为容器 | Group在转换时行为不可预测[citation:6] |

### 必要的连接
- 用户需要已连接Figma MCP服务器（官方远程MCP或Figma-Context-MCP均可）[citation:4][citation:5]
- 需要在Figma中选中要生成代码的Frame或组件

## 🎯 核心工作流程

### 步骤1：获取设计上下文
当用户在Figma中选中一个Frame并请求生成代码时，AI代理应该：

1. **通过MCP获取设计信息**：
   - 获取选中的Frame及其所有子图层
   - 提取应用的样式和变量（颜色、字体、间距）
   - 识别使用的组件及其属性[citation:2][citation:7]

2. **分析设计结构**：
   - 识别哪些部分可以映射到现有组件库
   - 分析布局方式（Auto Layout对应flex/grid）
   - 检查是否有不符合规范的地方

### 步骤2：映射到项目组件库
根据用户的组件库文档，将Figma中的元素映射到代码组件[citation:9]：

| Figma中的元素 | 应映射到的代码组件 |
|--------------|-------------------|
| Button组件 | `<Button variant="primary\|secondary">` |
| Input组件 | `<Input size="md\|lg" />` |
| Card组件 | `<Card padding="md" />` |
| Icon实例 | `<Icon name="..." size={16} />` |

**映射规则示例**：
- 如果Figma中的Button有"Primary"变体 → 使用`variant="primary"`
- 如果Button有"Small"/"Medium"/"Large"属性 → 映射为`size="sm"`/`"md"`/`"lg"`
- 如果Button有"Icon Left"属性 → 添加`leftIcon`prop

### 步骤3：应用设计规范
根据用户的设计规范文档，将Figma中的样式值转换为代码token[citation:2][citation:7]：

| Figma中的值 | 应转换为的token |
|------------|----------------|
| #1890FF (蓝色) | `colors.primary.500` |
| 16px间距 | `spacing.md` |
| Inter 14px medium | `typography.body.medium` |
| 8px圆角 | `radius.md` |

### 步骤4：生成代码
生成符合以下标准的代码：

#### 代码结构要求
- ✅ **使用组件库导入**：`import { Button, Card } from 'your-component-library'`
- ✅ **使用token变量**：`color: ${theme.colors.primary.500}` 而不是 `#1890FF`
- ✅ **响应式布局**：使用flex/grid，配合断点实现响应式[citation:2]
- ✅ **可访问性**：包含ARIA属性和语义HTML[citation:7]
- ❌ **避免硬编码值**：除非是临时占位内容
- ❌ **避免多余的wrapper div**：除非必要

#### 框架适配示例

**React组件示例**：
```jsx
import React from 'react';
import { Card, Button, Text } from '@your-company/ui';
import { useTheme } from '@your-company/theme';

export const ProfileCard = ({ user, variant = 'default' }) => {
  const theme = useTheme();
  
  return (
    <Card padding="lg" shadow="sm">
      <div css={{ display: 'flex', gap: theme.spacing.md }}>
        <Avatar src={user.avatar} size="lg" />
        <div css={{ flex: 1 }}>
          <Text variant="heading" size="md">
            {user.name}
          </Text>
          <Text variant="body" color="secondary">
            {user.bio}
          </Text>
        </div>
      </div>
      <div css={{ marginTop: theme.spacing.lg }}>
        <Button variant="primary" size="sm" onClick={handleFollow}>
          Follow
        </Button>
      </div>
    </Card>
  );
};