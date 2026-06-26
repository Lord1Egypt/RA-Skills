---
name: create-feishu-doc
description: "Use this skill whenever the user wants to create, generate, write to, or organize content into a Feishu document. Triggers include: any mention of 'Feishu doc', 'Feishu document', '飞书文档', '创建飞书文档', '生成飞书文档', or requests to produce structured or complete documents within Feishu. This applies to scenarios requiring fully formatted documents, including but not limited to: technical documentation, PRDs, project plans, reports, notes, articles, or novels. Use this skill whenever content needs to be compiled, structured, and delivered as a Feishu document."
---

# 通用飞书文档创建技能

## 概述

本技能提供通用的飞书文档创建功能，根据用户提供的任意内容创建文档。支持各种文档类型：小说、技术文档、项目计划、报告、笔记、文章等。由于飞书文档API对单次写入内容长度有限制，本技能通过智能分段、分批写入和重试机制确保各种长文档的完整创建。

## 核心工作流程

### 第一步：创建空白文档
1. 调用飞书API的`feishu_doc`工具的`create`操作
2. 传入文档标题和初始内容（通常只包含标题）
3. 记录返回的`document_id`和文档URL

### 第二步：等待文档初始化
1. 等待2秒钟，确保文档在飞书服务端完全初始化
2. 这是关键步骤，避免在文档未就绪时进行写入操作

### 第三步：分批次追加内容
1. 将完整内容按逻辑分段（每段约300-500字）
2. 对每个内容段：
   - 调用`feishu_doc`工具的`append`操作
   - 使用上一步获取的`document_id`
   - 等待1秒后再处理下一段
3. 内容分段建议：
   - 按自然段落或章节分段（如：小说章节、文档章节、主题段落等）
   - 避免单段内容过长导致API失败（建议300-500字/段）
   - 保持逻辑完整性，不在句子中间切断
   - 根据内容类型智能分段：小说按章节、技术文档按主题、报告按部分

### 第四步：错误处理和重试
1. 如果`append`操作失败（返回400错误）：
   - 等待2秒后重试
   - 最多重试3次
   - 如果仍然失败，记录错误并继续下一段
2. 重试时可以考虑：
   - 减少内容长度
   - 简化格式（移除复杂Markdown）
   - 检查网络连接

## 最佳实践

### 内容分段策略
- **小段落优先**：每段300-500字，避免API限制
- **逻辑完整**：按章节或主题分段，不在句子中间切断
- **格式简化**：使用飞书支持的简单格式（纯文本、简单列表）
- **进度跟踪**：记录已写入的段落数和总段落数

### 错误处理策略
- **立即重试**：首次失败后等待2秒重试
- **降级处理**：重试失败时简化内容格式
- **跳过继续**：单个段落失败不影响整体进度
- **最终验证**：所有段落写入后读取文档验证完整性

### 性能优化
- **并行写入**：可以同时处理多个文档
- **批量操作**：相似内容可以合并写入
- **缓存利用**：重复内容可以缓存避免重复生成
- **进度保存**：支持断点续传，记录已完成的段落

## 使用示例

### 示例1：创建小说章节文档
```python
# 伪代码示例
1. create_doc("剑来小说第一章")
2. wait(2)
3. append_content("第一节：小镇少年...")
4. wait(1)
5. append_content("第二节：集市奇遇...")
6. wait(1)
7. append_content("第三节：神秘预言...")
8. 验证文档完整性
```

### 示例2：创建技术文档
```python
# 伪代码示例
1. create_doc("Python编程指南")
2. wait(2)
3. append_content("第一章：Python基础...")
4. wait(1)
5. append_content("第二章：函数和模块...")
6. wait(1)
7. append_content("第三章：面向对象编程...")
8. 验证文档完整性
```

### 示例3：通用文档创建流程
```python
# 伪代码示例
1. 获取用户输入的文档标题和内容
2. 创建空白文档
3. 等待文档初始化
4. 将内容智能分段
5. 分批次写入所有段落
6. 处理错误和重试
7. 验证文档完整性
8. 返回文档链接和创建结果
```

## 常见问题解决

### 问题1：API返回400错误
**原因**：内容过长或格式不支持
**解决**：
1. 减少单次写入内容长度
2. 移除复杂Markdown格式
3. 使用纯文本格式重试

### 问题2：文档内容丢失
**原因**：写入操作未成功但未检测到
**解决**：
1. 每次写入后验证返回状态
2. 记录每个段落的写入状态
3. 最终读取文档验证完整性

### 问题3：写入速度慢
**原因**：等待时间过长或网络延迟
**解决**：
1. 优化等待时间（1-2秒通常足够）
2. 考虑并行写入多个段落
3. 使用本地缓存减少重复生成

## 资源文件

### scripts/create_feishu_doc.py
提供Python脚本实现完整的文档创建流程，包括错误处理和重试机制。

### references/feishu_api_guide.md
飞书API使用指南，包含常见错误代码和解决方案。

---

**技能特点**：
- **通用性强**：支持各种类型的文档内容创建
- **智能分段**：根据内容类型自动智能分段
- **错误处理**：智能重试和格式简化机制
- **进度跟踪**：实时显示写入进度和成功率
- **完整性验证**：创建后验证文档完整性
- **用户友好**：简单的接口和详细的状态报告
