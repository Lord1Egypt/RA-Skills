# 飞书文档API使用指南

## 概述

本文档提供飞书文档API的详细使用指南，特别关注创建长文档时的最佳实践和问题解决。

## API工具

OpenClaw中使用的飞书文档工具：`feishu_doc`

### 可用操作
- `create` - 创建新文档
- `read` - 读取文档内容
- `write` - 写入文档内容（覆盖）
- `append` - 追加文档内容
- `list_blocks` - 列出文档块
- `get_block` - 获取文档块详情
- `update_block` - 更新文档块
- `delete_block` - 删除文档块

## 创建文档工作流程

### 标准工作流程
1. **创建文档** → `create`操作
2. **等待初始化** → 等待2秒
3. **分批写入** → `append`操作（多次）
4. **验证结果** → `read`操作

### 详细步骤

#### 步骤1：创建文档
```python
# 示例：创建文档
response = feishu_doc.create(
    title="文档标题",
    content="# 文档标题"  # 通常只写标题
)

# 返回结果
{
    "document_id": "XXX...",
    "title": "文档标题",
    "url": "https://feishu.cn/docx/XXX..."
}
```

**重要提示**：
- `create`操作通常只能创建标题，不能写入大量内容
- 初始内容应尽量简单，避免复杂格式

#### 步骤2：等待初始化
```python
# 必须等待文档在服务端完全初始化
import time
time.sleep(2)  # 等待2秒
```

**为什么需要等待**：
- 飞书服务端需要时间处理文档创建
- 立即写入可能导致API错误
- 2秒通常是安全的等待时间

#### 步骤3：分批写入
```python
# 将内容分割成多个段落
segments = split_content(full_content, max_length=500)

for i, segment in enumerate(segments):
    # 写入段落
    success = feishu_doc.append(
        doc_token=document_id,
        content=segment
    )
    
    # 段落间等待
    if i < len(segments) - 1:
        time.sleep(1)  # 等待1秒
```

**内容分割策略**：
1. **按章节分割**：以`## 标题`为界
2. **按长度分割**：每段300-500字符
3. **按逻辑分割**：保持段落完整性

#### 步骤4：错误处理和重试
```python
def append_with_retry(doc_token, content, max_retries=3):
    for retry in range(max_retries):
        try:
            result = feishu_doc.append(
                doc_token=doc_token,
                content=content
            )
            return True, result
        except Exception as e:
            if "400" in str(e):
                # 内容格式问题，简化后重试
                simplified = simplify_content(content)
                content = simplified
                time.sleep(2)  # 等待后重试
            else:
                return False, str(e)
    return False, "达到最大重试次数"
```

## 常见错误代码

### 400错误：请求参数错误
**可能原因**：
1. 内容过长（单次超过1000字符）
2. 格式不支持（复杂Markdown）
3. 文档未初始化完成
4. 权限问题

**解决方案**：
1. 减少单次写入内容长度
2. 简化内容格式
3. 增加等待时间后重试
4. 检查API权限

### 403错误：权限不足
**可能原因**：
1. API token过期
2. 应用权限不足
3. 文档访问权限限制

**解决方案**：
1. 检查API token有效性
2. 验证应用权限范围
3. 确认文档可访问性

### 429错误：请求频率限制
**可能原因**：
1. API调用频率过高
2. 短时间内大量请求

**解决方案**：
1. 增加请求间隔时间
2. 实现指数退避重试
3. 批量处理请求

### 500错误：服务器错误
**可能原因**：
1. 飞书服务端问题
2. 网络连接问题
3. 超时错误

**解决方案**：
1. 等待后重试
2. 检查网络连接
3. 联系飞书技术支持

## 内容格式指南

### 支持的格式
1. **标题**：`# 一级标题`，`## 二级标题`
2. **列表**：`- 项目`，`1. 项目`
3. **文本**：普通段落文本
4. **分割线**：`---`
5. **引用**：`> 引用文本`

### 不支持的格式（可能导致400错误）
1. **复杂表格**：多行列合并
2. **嵌套列表**：多层缩进列表
3. **代码块**：```代码```
4. **数学公式**：LaTeX公式
5. **复杂HTML**：内嵌HTML标签

### 格式简化函数
```python
def simplify_content(content):
    """简化内容格式，提高API兼容性"""
    
    # 移除代码块
    content = content.replace('```', '')
    
    # 简化标题格式
    content = content.replace('### ', '**')
    
    # 分割长行
    lines = content.split('\n')
    simplified_lines = []
    
    for line in lines:
        if len(line) > 100:
            # 分割长行
            words = line.split()
            current_line = []
            current_length = 0
            
            for word in words:
                if current_length + len(word) + 1 > 80:
                    simplified_lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = len(word)
                else:
                    current_line.append(word)
                    current_length += len(word) + 1
            
            if current_line:
                simplified_lines.append(' '.join(current_line))
        else:
            simplified_lines.append(line)
    
    return '\n'.join(simplified_lines)
```

## 性能优化建议

### 1. 批量处理
```python
# 不好的做法：频繁小请求
for item in items:
    append_small_content(item)

# 好的做法：批量处理
batches = create_batches(items, batch_size=5)
for batch in batches:
    append_batch_content(batch)
    time.sleep(1)
```

### 2. 并行处理
```python
# 同时处理多个文档
import threading

def create_document_parallel(doc_info):
    creator = FeishuDocCreator(doc_info['title'])
    creator.create_complete_document(doc_info['content'])

threads = []
for doc_info in documents:
    thread = threading.Thread(target=create_document_parallel, args=(doc_info,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
```

### 3. 缓存利用
```python
# 缓存重复内容
content_cache = {}

def get_cached_content(content_key):
    if content_key in content_cache:
        return content_cache[content_key]
    else:
        content = generate_content(content_key)
        content_cache[content_key] = content
        return content
```

## 监控和日志

### 日志记录
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def log_operation(operation, document_id, status, details=None):
    logger.info(f"{operation} - {document_id} - {status}")
    if details:
        logger.debug(f"Details: {details}")
```

### 性能监控
```python
import time
from collections import defaultdict

performance_stats = defaultdict(list)

def track_performance(operation, start_time):
    duration = time.time() - start_time
    performance_stats[operation].append(duration)
    
    # 定期报告
    if len(performance_stats[operation]) % 10 == 0:
        avg_time = sum(performance_stats[operation]) / len(performance_stats[operation])
        logger.info(f"{operation}平均耗时: {avg_time:.2f}秒")
```

## 故障排除检查表

### 创建失败
- [ ] API token有效
- [ ] 应用有文档创建权限
- [ ] 网络连接正常
- [ ] 标题不超过100字符

### 写入失败
- [ ] 文档ID正确
- [ ] 等待文档初始化完成
- [ ] 单次内容不超过500字符
- [ ] 格式简化处理
- [ ] 重试机制生效

### 性能问题
- [ ] 请求间隔合理（≥1秒）
- [ ] 批量处理优化
- [ ] 缓存有效利用
- [ ] 并行处理适当

### 最终验证
- [ ] 文档可访问
- [ ] 内容完整
- [ ] 格式正确
- [ ] 链接有效

## 最佳实践总结

1. **分而治之**：长文档分批次写入
2. **耐心等待**：操作间适当等待
3. **简化格式**：避免复杂Markdown
4. **错误处理**：实现重试机制
5. **监控验证**：记录日志并验证结果
6. **性能优化**：批量、并行、缓存
7. **用户反馈**：提供进度和结果报告

## 相关资源

- 飞书开放平台：https://open.feishu.cn/
- API文档：https://open.feishu.cn/document/server-docs/docs/docs
- 错误代码：https://open.feishu.cn/document/ukTMukTMukTM/ugjM14COyUjL4ITN
- 社区支持：https://open.feishu.cn/document/ukTMukTMukTM/uYDN14SN0QjL4QDN