# AI 开发常见坑与解决方案

## 1. LLM 调用

### 坑: 输出格式不稳定
**现象**: 要求JSON输出但模型有时返回纯文本, 有时多一个```json包裹

**解决方案**:
```python
import json, re

def safe_parse_json(llm_output: str) -> dict:
    """安全解析LLM输出的JSON"""
    # 去掉可能的 markdown 代码块标记
    output = re.sub(r'```(?:json)?\s*', '', llm_output).strip()
    output = re.sub(r'```\s*$', '', output).strip()
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        # 兜底: 用正则提取
        match = re.search(r'\{.*\}', output, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"无法解析JSON: {output[:200]}")
```

### 坑: Token耗尽导致截断
**现象**: 长对话或大文档导致回复被截断

**解决方案**:
- 设置 `max_tokens` 参数并检查 `finish_reason`
- 对长文档做摘要预处理
- 使用滑动窗口管理对话历史
- 关键信息放最后 (lost-in-the-middle 效应)

### 坑: 幻觉 (Hallucination)
**现象**: 模型编造不存在的事实

**缓解策略**:
- RAG: 只基于检索到的文档回答
- Prompt约束: "如果不知道,请说'我不确定'"
- 不确定性标注: 让模型对不确定内容加上 `[置信度: 低]`
- 后处理校验: 关键信息(日期、数值)做规则校验

## 2. RAG 开发

### 坑: 切片破坏了上下文
**现象**: 检索到的片段缺少上下文, 无法理解

**解决方案**:
- 使用 Small-to-Big: 检索小片段, 返回大段落
- 保留文档标题层级作为元数据
- Chunk 之间加 overlap (10-20%)
- 对表格/列表使用语义保持切片

### 坑: 检索召回率低
**现象**: 明明有答案但检索不到

**排查步骤**:
1. 检查 Embedding 模型是否与文档语言匹配 (中英文分开)
2. 添加 Query Rewriting (指代消解、同义词扩展)
3. 启用混合检索 (向量 + BM25)
4. 增加检索数量 (top_k 从 3 提到 10)
5. 检查切片大小是否合适

### 坑: 向量数据库性能问题
**现象**: 检索延迟高、内存爆炸

**优化**:
- 使用索引 (IVF_FLAT / HNSW)
- 对超大集合做分区
- 合理设置 `ef_search` / `nprobe` 参数
- embedding维度不是越高越好, 512/768维通常够用

## 3. Agent 开发

### 坑: Agent 陷入死循环
**现象**: Agent 重复调用同一工具不停止

**解决方案**:
- 硬限制 `max_steps` (通常 10-15)
- 检测重复调用: 最近3步工具+参数相同 → 强制终止
- 每步检查是否离目标更近 (进度追踪)

### 坑: 工具描述不当导致误调用
**现象**: Agent 调用了不该调的工具, 或没调用该调的

**解决方案**:
- 工具描述要精确: 包含输入输出格式、使用条件、示例
- 分组管理: 按场景分工具组, 减少选择空间
- 添加工具使用校验层: 调用前检查参数合法性
- 用 Function Calling 而非 Prompt 描述工具 (结构化更强)

### 坑: Multi-Agent 协调混乱
**现象**: 多个Agent互相等待或重复工作

**解决方案**:
- 用状态机管理 Agent 生命周期
- 明确输入输出契约 (每个Agent的输入Schema和输出Schema)
- 超时机制: 每个Agent有最大等待时间
- 加入协调Agent/Orchestrator统一调度

## 4. 性能

### 坑: 首Token延迟过高
**现象**: 用户等待3秒+才开始看到回复

**优化**:
- 使用流式输出 (SSE) — 感知延迟可降 70%
- 并行预加载: 在用户输入时同时检索RAG
- 模型预热: 保持长连接, 避免冷启动
- 选择更小/更快的模型处理简单任务

### 坑: 并发量不足
**现象**: 并发用户多时请求排队、超时

**优化**:
- API 层做 Request Queue + 限流
- LLM 层加连接池
- 语义缓存 — 减少 50-80% 的 LLM 调用
- 异步非阻塞架构 (FastAPI + asyncio)

## 5. 安全

### 坑: Prompt Injection
**现象**: 用户输入绕过 System Prompt

**防护**:
- 用特殊分隔符隔离用户输入和系统指令
- 输入过滤: 检测 "忽略之前的指令" 等注入模式
- 输出审核: 检查是否泄露了 System Prompt 或内部信息
- 人工回环: 高风险操作必须人工确认

### 坑: PII 泄露
**现象**: 个人信息出现在日志或训练数据中

**防护**:
- 日志脱敏: 自动检测并替换手机号/身份证/邮箱
- 用户数据隔离: 不同用户的对话历史完全隔离
- API Key 管理: 用环境变量, 不进代码仓库

## 6. 运维

### 坑: 生产环境和测试环境Prompt不一致
**现象**: 测试通过但上线效果差

**解决方案**:
- Prompt 版本化管理 (Git + 注册中心)
- 上线前在 Staging 环境用生产数据验证
- Canary 部署: 新Prompt只在 5% 用户上生效

### 坑: LLM API 突然不可用
**现象**: OpenAI/第三方API宕机导致服务不可用

**熔断策略**:
```python
class LLMFallback:
    def __init__(self, primary, fallback, circuit_breaker=5):
        self.primary = primary     # 主模型
        self.fallback = fallback   # 备用模型
        self.failures = 0
        self.circuit_breaker = circuit_breaker
    
    async def chat(self, **kwargs):
        if self.failures >= self.circuit_breaker:
            return await self.fallback.chat(**kwargs)
        try:
            return await self.primary.chat(**kwargs)
        except Exception:
            self.failures += 1
            return await self.fallback.chat(**kwargs)
```

### 坑: Token 成本失控
**现象**: 月账单远超预期

**排查**:
- 检查是否有异常长Prompt (如把整个文档塞进Prompt)
- 查看是否有死循环导致重复调用
- 确认 `max_tokens` 设置合理 (不要默认最大)
- 检查缓存是否正常生效
