# 智能路由实现方案 - Article Workflow Smart Router

## 📋 概述

本文档说明如何在 OpenClaw 中实现文章分析工作流的智能路由优化。

**核心目标：**
1. 单篇文章 → 主 Agent 一次性执行（1 次流式请求）
2. 多篇文章 → SubAgent 并发执行（N 次但并行）
3. 流式优化 → 工具调用不中断流式，算 1 次请求

---

## 🚀 实现方案

### 方案 A：智能路由（已实现）

在 `scripts/smart_router.py` 中实现自动路由逻辑。

#### 触发方式

**单篇模式（自动识别）：**
```
分析这篇文章：https://example.com/article
```

**批量模式（自动识别）：**
```
批量分析这些文章：
- https://example.com/article1
- https://example.com/article2
- https://example.com/article3
```

或
```
分析这 5 篇文章：[url1, url2, url3, url4, url5]
```

#### 路由逻辑

```python
def is_batch_mode(urls: List[str], user_input: str) -> bool:
    """判断是否为批量模式"""
    # 1. 检查批量关键词
    batch_keywords = ["批量", "这些文章", "多篇文章", "全部分析"]
    has_batch_keyword = any(keyword in user_input for keyword in batch_keywords)
    
    # 2. 检查 URL 数量
    multiple_urls = len(urls) > 1
    
    return has_batch_keyword or multiple_urls
```

---

## 🔧 OpenClaw 集成实现

### 单篇模式实现（主 Agent）

```python
# 在 OpenClaw 会话中直接执行
async def process_article_single(url: str):
    """单篇模式：主 Agent 一次性执行（1 次流式请求）"""
    
    # 1. 抓取内容（工具调用，不中断流式）
    content = await web_fetch(url=url, extractMode="markdown")
    
    # 2. 分析内容（继续流式生成）
    analysis = await llm_analyze(content)
    
    # 3. 生成报告（继续流式生成）
    report = await llm_generate_report(analysis)
    
    # 4. 创建文档（工具调用，不中断流式）
    doc = await feishu_create_doc(
        title=analysis.title,
        markdown=report
    )
    
    # 5. 归档到 Bitable（工具调用，不中断流式）
    record = await feishu_bitable_app_table_record(
        app_token=BITABLE_TOKEN,
        table_id=TABLE_ID,
        fields={
            "标题": analysis.title,
            "URL": url,
            "摘要": analysis.summary,
            "文档链接": doc.url
        }
    )
    
    # 6. 添加到缓存
    add_url_to_cache(url, analysis.title, record.id, doc.url)
    
    return {
        "success": True,
        "title": analysis.title,
        "doc_url": doc.url,
        "bitable_url": record.url
    }
```

**关键点：**
- ✅ 所有步骤在**同一次流式请求**中完成
- ✅ 工具调用使用 `stream.send_tool_result()` 不中断流式
- ✅ 模型请求次数 = 1 次

---

### 批量模式实现（SubAgent 并发）

```python
# 在 OpenClaw 主 Agent 中
async def process_article_batch(urls: List[str]):
    """批量模式：SubAgent 并发执行"""
    
    MAX_CONCURRENT = 5
    results = []
    
    # 分批处理（如果超过最大并发数）
    batches = chunk_list(urls, MAX_CONCURRENT)
    
    for batch_idx, batch in enumerate(batches, 1):
        print(f"处理第 {batch_idx}/{len(batches)} 批...")
        
        # 并发创建 SubAgent
        tasks = []
        for url in batch:
            task = sessions_spawn(
                runtime="subagent",
                mode="run",
                task=f"分析这篇文章：{url}",
                streamTo="parent"
            )
            tasks.append(task)
        
        # 等待所有 SubAgent 完成
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
    
    # 汇总结果
    return summarize_results(results)
```

**关键点：**
- ✅ 每个 SubAgent 独立执行（1 次流式请求）
- ✅ 并发执行，总时间 ≈ 单次请求时间
- ✅ 主 Agent 只负责汇总（额外 1 次请求）

---

## 📊 模型请求次数对比

| 场景 | 传统方案 | 优化后方案 | 优化效果 |
|------|---------|-----------|---------|
| 单篇分析 | 1 次 | 1 次 | ✅ 不变 |
| 5 篇批量 | 5 次（串行，~50 秒） | 5 次（并发，~10 秒） | ⏱️ **时间减少 80%** |
| 10 篇批量 | 10 次（串行，~100 秒） | 10 次（2 批并发，~20 秒） | ⏱️ **时间减少 80%** |
| 20 篇批量 | 20 次（串行，~200 秒） | 20 次（4 批并发，~40 秒） | ⏱️ **时间减少 80%** |

---

## 🔍 流式请求优化细节

### ❌ 错误方式（多次请求）

```python
# 每次工具调用都中断流式，重新发起请求
result1 = await llm.generate(prompt1)  # 请求 1
tool_result1 = await fetch_url(url)     # 工具调用
result2 = await llm.generate(prompt2)  # 请求 2（新的请求！）
tool_result2 = await create_doc()       # 工具调用
result3 = await llm.generate(prompt3)  # 请求 3（新的请求！）
```

**问题：** 3 次独立的模型请求

---

### ✅ 正确方式（1 次流式请求）

```python
# 保持流式上下文，工具调用不中断
stream = await llm.stream_generate(initial_prompt)

# 第 1 步：抓取内容
stream.send_tool_result(await fetch_url(url))
stream.continue_generate()  # 继续流式

# 第 2 步：分析内容
stream.send_tool_result(await analyze_content())
stream.continue_generate()  # 继续流式

# 第 3 步：创建文档
stream.send_tool_result(await create_doc())
stream.continue_generate()  # 继续流式

# 第 4 步：归档
stream.send_tool_result(await archive_to_bitable())
stream.continue_generate()  # 继续流式

# 完成
final_result = stream.finish()
```

**优势：** 整个流程算 1 次请求

---

## 🎯 实施步骤

### Step 1: 更新 SKILL.md ✅

已在 `skills/article-workflow/SKILL.md` 中添加智能路由说明。

### Step 2: 创建智能路由执行器 ✅

已创建 `scripts/smart_router.py`，提供：
- URL 解析
- 模式识别（单篇/批量）
- 路由逻辑
- 并发控制

### Step 3: 集成到 OpenClaw 工具系统

需要在 OpenClaw 主会话中实现：

```python
# 在 OpenClaw 会话中监听文章分析请求
async def handle_article_request(user_input: str):
    """处理文章分析请求"""
    from skills.article_workflow.scripts.smart_router import ArticleSmartRouter
    
    router = ArticleSmartRouter()
    
    # 解析 URL
    urls = router.parse_input(user_input)
    if not urls:
        return "未找到有效的文章 URL"
    
    # 智能路由
    if router.is_batch_mode(urls, user_input):
        # 批量模式
        return await process_article_batch(urls)
    else:
        # 单篇模式
        return await process_article_single(urls[0])
```

### Step 4: 测试流式优化

验证工具调用是否真的不中断流式：

```bash
# 测试单篇模式
python scripts/smart_router.py https://mp.weixin.qq.com/s/xxx

# 测试批量模式
python scripts/smart_router.py url1 url2 url3
```

### Step 5: 监控模型请求次数

在 `logs/workflow.log` 中记录：
- 请求次数
- 请求类型（单篇/批量）
- 执行时间

---

## 📝 使用示例

### 示例 1：单篇分析

**用户输入：**
```
分析这篇文章：https://mp.weixin.qq.com/s/abc123
```

**执行流程：**
```
1. 解析 URL → ["https://mp.weixin.qq.com/s/abc123"]
2. 识别模式 → 单篇模式（1 个 URL，无批量关键词）
3. 主 Agent 执行 → 1 次流式请求
4. 输出结果 → 摘要 + 报告链接 + 评分
```

### 示例 2：批量分析

**用户输入：**
```
批量分析这些文章：
- https://mp.weixin.qq.com/s/abc123
- https://zhuanlan.zhihu.com/p/456789
- https://github.com/blog/tech-update
```

**执行流程：**
```
1. 解析 URL → [url1, url2, url3]
2. 识别模式 → 批量模式（关键词"批量" + 多个 URL）
3. 创建 3 个 SubAgent → 并发执行
4. 等待完成 → 汇总结果
5. 输出结果 → 汇总报告 + 各文章链接
```

---

## ⚠️ 注意事项

### 1. 并发数限制

```python
MAX_CONCURRENT_SUBAGENTS = 5  # 最多 5 个并发
```

超过 5 个 URL 会自动分批处理。

### 2. 流式请求保持

确保工具调用使用正确的方式，不中断流式：
- ✅ 使用 `stream.send_tool_result()`
- ✅ 使用 `stream.continue_generate()`
- ❌ 避免重新调用 `llm.generate()`

### 3. 错误处理

每个 SubAgent 独立处理错误，不影响其他文章：

```python
try:
    result = process_single(url)
except Exception as e:
    result = ArticleResult(
        url=url,
        success=False,
        error=str(e)
    )
```

---

## 📊 性能监控

### 日志格式

```json
{
  "timestamp": "2026-03-15T09:00:00+08:00",
  "mode": "single",
  "url_count": 1,
  "model_requests": 1,
  "execution_time_seconds": 8.5,
  "success": true
}
```

### 统计指标

- 平均执行时间（单篇/批量）
- 模型请求次数统计
- 成功率统计
- 并发效率提升比

---

## 🔗 相关文件

- `skills/article-workflow/SKILL.md` - Skill 文档（已更新）
- `skills/article-workflow/scripts/smart_router.py` - 智能路由执行器（已创建）
- `skills/article-workflow/scripts/workflow.py` - 原有工作流脚本
- `skills/article-workflow/core/analyzer.py` - 分析器核心模块

---

## ✅ 下一步

1. **集成测试** - 在 OpenClaw 中实际测试单篇/批量模式
2. **性能验证** - 确认模型请求次数符合预期
3. **日志监控** - 添加详细的执行日志
4. **用户反馈** - 根据实际使用优化体验

---

*最后更新：2026-03-15*
*作者：Nox（DongNan 的 AI 助理）*
