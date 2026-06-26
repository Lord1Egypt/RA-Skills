---
name: feishu-send-file-directly
description: 飞书消息直接发送文件附件技能。当用户需要直接通过飞书消息发送文件附件（而不是文档链接）时使用此技能。
metadata:
  openclaw:
    emoji: 📎
    always: false
    requires:
      tools: ["message", "write", "exec"]
    categories: ["feishu", "file-transfer"]
    version: "1.0.0"
    created: "2026-04-13"
    author: "OpenClaw Assistant"
    tags: ["feishu", "file", "attachment", "send", "direct"]
---

# 飞书消息直接发送文件技能

## 技能概述
本技能提供了通过飞书消息直接发送文件附件的工作流程，解决了发送文档链接而非直接文件的问题。

## 适用场景
- 用户需要直接发送文件附件，而不是文档链接
- 需要批量发送多个文件
- 发送各种类型的文件（.docx, .pdf, .ppt, .jpg等）
- 需要控制文件在客户端的显示名称

## 核心原理
使用 `message` 工具的 `path` 参数直接发送本地文件，避免使用 `media` 参数发送文档链接。

## 前置条件
1. 飞书 channel 已正确配置并启用
2. 有权限读取要发送的本地文件
3. 文件大小在飞书允许的范围内

## 基础用法

### 发送单个文件
```javascript
// 步骤1：创建或确认文件存在
write({
  path: "/path/to/your/file.docx",
  content: "文件内容..."
});

// 步骤2：发送文件附件
message({
  action: "send",
  message: "文件说明",
  path: "/path/to/your/file.docx",  // 关键：使用path参数
  filename: "自定义文件名.docx"     // 可选：设置显示名称
});
```

### 查找并发送特定类型文件
```javascript
// 查找所有.docx和.pdf文件
exec({
  command: "find /root/.openclaw/workspace/ -name '*.docx' -o -name '*.pdf'"
});

// 逐个发送找到的文件
const files = ["file1.docx", "file2.pdf"];
files.forEach(file => {
  message({
    action: "send",
    message: `发送文件: ${file}`,
    path: `/root/.openclaw/workspace/${file}`,
    filename: file
  });
});
```

## 参数详解

### message 工具参数
| 参数 | 类型 | 必需 | 说明 | 示例 |
|------|------|------|------|------|
| `action` | string | 是 | 操作类型，固定为"send" | `"send"` |
| `message` | string | 是 | 消息正文内容 | `"这是要发送的文件"` |
| `path` | string | 是 | **本地文件绝对路径** | `"/root/.openclaw/workspace/file.pdf"` |
| `filename` | string | 否 | 客户端显示的文件名 | `"报告.pdf"` |
| `channel` | string | 否 | 指定channel，默认当前channel | `"feishu"` |

### 其他相关工具
- `write`: 创建或修改文件内容
- `exec`: 查找、列出或验证文件
- `read`: 读取文件内容（发送前预览）

## 完整工作流程

### 流程1：发送已知文件
```
1. 确认文件路径 → 2. 设置发送参数 → 3. 调用message发送 → 4. 验证结果
```

### 流程2：批量发送文件
```
1. 查找目标文件 → 2. 过滤文件类型 → 3. 逐个发送文件 → 4. 统计发送结果
```

### 流程3：创建并发送文件
```
1. 创建文件内容 → 2. 保存到本地 → 3. 发送文件 → 4. 清理临时文件（可选）
```

## 示例代码

### 示例1：发送PPT文件
```javascript
// 创建PPT内容
const pptContent = `幻灯片1: 封面
- 标题: AI MaaS述职报告
- 汇报人: [姓名]
- 日期: ${new Date().toLocaleDateString()}

幻灯片2: 目录
1. 概述
2. 市场分析
3. 技术架构
4. 未来展望`;

// 保存文件
write({
  path: "/tmp/ai_maas_report.ppt",
  content: pptContent
});

// 发送文件
message({
  action: "send",
  message: "AI MaaS述职报告PPT",
  path: "/tmp/ai_maas_report.ppt",
  filename: "AI_MaaS_述职报告_2026.ppt"
});
```

### 示例2：批量发送工作区文档
```javascript
// 查找工作区所有文档
exec({
  command: "ls -la /root/.openclaw/workspace/*.docx /root/.openclaw/workspace/*.pdf 2>/dev/null || true"
});

// 假设找到以下文件
const documents = [
  "项目报告.docx",
  "技术方案.pdf", 
  "会议纪要.docx",
  "数据分析.pdf"
];

// 发送进度提示
message({
  action: "send",
  message: `开始发送 ${documents.length} 个文档文件...`
});

// 逐个发送
documents.forEach((doc, index) => {
  message({
    action: "send",
    message: `文档 ${index + 1}/${documents.length}: ${doc}`,
    path: `/root/.openclaw/workspace/${doc}`,
    filename: doc
  });
});

// 发送完成提示
message({
  action: "send",
  message: `✅ 已完成发送 ${documents.length} 个文档文件`
});
```

### 示例3：发送图片文件
```javascript
// 注意：图片文件通常是二进制，需要用其他方式创建
// 这里假设图片已存在

message({
  action: "send",
  message: "产品设计图",
  path: "/path/to/product_design.jpg",
  filename: "产品设计图.jpg"
});
```

## 错误处理

### 常见错误及解决方案
1. **文件不存在错误**
   ```javascript
   // 发送前检查文件
   exec({
     command: `test -f "/path/to/file" && echo "EXISTS" || echo "NOT_FOUND"`
   });
   ```

2. **权限错误**
   ```javascript
   // 检查文件权限
   exec({
     command: "ls -la /path/to/file"
   });
   ```

3. **文件大小超限**
   ```javascript
   // 检查文件大小（字节）
   exec({
     command: "stat -c%s /path/to/file"
   });
   ```

### 错误恢复策略
```javascript
try {
  const result = message({
    action: "send",
    message: "文件",
    path: "/path/to/file"
  });
  
  if (!result.ok) {
    // 记录错误，尝试其他文件
    console.error(`发送失败: ${result.error}`);
  }
} catch (error) {
  // 异常处理
  console.error(`发送异常: ${error.message}`);
}
```

## 最佳实践

### 1. 文件管理
- 使用有意义的文件名
- 组织文件到特定目录
- 定期清理临时文件

### 2. 发送策略
- 一次发送一个文件，避免并发问题
- 大文件考虑压缩或分卷
- 添加有意义的消息说明

### 3. 用户体验
- 发送前告知用户文件信息
- 发送后确认结果
- 提供文件下载指引

### 4. 性能优化
- 批量发送时添加延迟
- 避免同时发送过多大文件
- 监控发送成功率

## 注意事项

### 技术限制
1. 飞书对附件大小有限制（通常为2GB）
2. 某些文件类型可能被安全策略限制
3. 网络状况可能影响大文件发送

### 安全考虑
1. 不要发送敏感或机密文件
2. 验证文件来源和内容
3. 遵循公司安全政策

### 兼容性
1. 确保文件格式客户端支持
2. 考虑不同设备的显示效果
3. 测试不同文件类型的发送

## 扩展功能

### 1. 文件预览
```javascript
// 发送前预览文本文件内容
const content = read({
  path: "/path/to/file.txt",
  limit: 1000  // 预览前1000字符
});

message({
  action: "send",
  message: `文件预览:\n\`\`\`\n${content}\n\`\`\`\n\n完整文件见附件`,
  path: "/path/to/file.txt",
  filename: "file.txt"
});
```

### 2. 文件信息统计
```javascript
// 获取文件信息
exec({
  command: "stat --format='大小: %s 字节 | 修改时间: %y' /path/to/file"
});

// 发送带统计信息的文件
message({
  action: "send",
  message: `文件信息: ${fileInfo}\n\n文件见附件`,
  path: "/path/to/file",
  filename: "file.pdf"
});
```

### 3. 自动压缩大文件
```javascript
// 检查文件大小并决定是否压缩
exec({
  command: "find /path/to/file -size +10M -exec echo 'LARGE_FILE' \\;"
});

// 如果文件太大，先压缩
exec({
  command: "zip -q /path/to/file.zip /path/to/file"
});

// 发送压缩文件
message({
  action: "send",
  message: "大文件已压缩",
  path: "/path/to/file.zip",
  filename: "file.zip"
});
```

## 故障排除

### Q1: 文件发送失败，返回权限错误
**A**: 检查文件读取权限，确保OpenClaw进程有权限访问该文件。

### Q2: 用户收到的是链接而不是文件
**A**: 确认使用了`path`参数而不是`media`参数。

### Q3: 文件名显示乱码
**A**: 使用英文文件名或确保编码正确。

### Q4: 大文件发送超时
**A**: 考虑压缩文件或分卷发送。

### Q5: 批量发送时部分文件失败
**A**: 添加错误重试机制，记录失败文件。

## 版本更新

### v1.0.0 (2026-04-13)
- 初始版本发布
- 基于实际发送15个文件的实践经验
- 包含基础发送流程和示例代码

## 相关资源
- [飞书消息工具文档](https://docs.openclaw.ai/tools/message)
- [文件操作工具文档](https://docs.openclaw.ai/tools/write)
- [OpenClaw工作区管理](https://docs.openclaw.ai/guides/workspace)

## 贡献指南
欢迎提交改进建议、错误报告或示例代码。请通过OpenClaw社区渠道提交。

---
**技能创建者**: OpenClaw Assistant  
**创建日期**: 2026年4月13日  
**最后更新**: 2026年4月13日  
**适用场景**: 飞书消息直接发送文件附件