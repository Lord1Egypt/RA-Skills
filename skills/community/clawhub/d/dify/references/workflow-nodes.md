# Dify 工作流节点详解

## 输入输出节点

### User Input (用户输入)

定义用户输入变量，支持多种字段类型:

| 类型 | 用途 | 配置项 |
|-----|------|--------|
| Short Text | 短文本 | max_length, required |
| Paragraph | 长文本 | max_length, required |
| Select | 下拉选择 | options[], default |
| File | 单文件 | allowed_types, max_size |
| File List | 文件列表 | allowed_types, max_count |
| Number | 数字 | min, max, default |

**变量引用:** `{{User Input.variable_name}}`

### Output (输出)

工作流结束节点，输出最终结果。

---

## 逻辑控制节点

### IF/ELSE (条件分支)

根据条件分流执行路径:

**条件类型:**
- `contains` - 包含
- `not contains` - 不包含
- `is` - 等于
- `is not` - 不等于
- `empty` - 为空
- `not empty` - 不为空
- `in` - 在列表中
- `not in` - 不在列表中
- `>`, `>=`, `<`, `<=` - 数值比较

**多条件组合:** AND / OR 逻辑

### Iteration (迭代)

对数组元素逐个处理:

```
输入数组 → Iteration节点 → 对每个元素执行子流程
```

**变量:** `{{Iteration.item}}` 当前元素

### Parallel (并行)

同时执行多个分支，汇聚所有结果后继续。

---

## LLM节点

### LM (大语言模型)

调用LLM生成文本:

**配置项:**
- Model - 选择模型
- System Prompt - 系统提示词
- User Prompt - 用户提示词
- Context - 上下文变量
- Memory - 记忆设置
- Vision - 视觉能力开关

**变量:** `{{LLM.text}}` 输出文本

### Parameter Extractor (参数提取)

用LLM从自然语言提取结构化数据:

```json
{
  "name": "platform",
  "type": "Array[String]",
  "description": "提取目标平台名称",
  "required": true
}
```

支持类型: `String`, `Number`, `Boolean`, `Array[String]`, `Object`

### Question Classifier (问题分类)

自动分类用户问题，路由到不同处理分支。

---

## 数据处理节点

### List Operator (列表操作)

过滤和转换数组:

**过滤条件:**
```javascript
{{item.type}} in ["Image"]  // 保留图片类型
```

### Variable Aggregator (变量聚合)

将多个分支的变量聚合成一个对象。

### Template (模板)

使用Jinja2模板渲染文本:

```jinja2
{% for item in items %}
- {{item.name}}: {{item.value}}
{% endfor %}
```

### Code (代码执行)

运行Python或JavaScript代码:

```python
def main(args):
    result = process(args["input"])
    return {"output": result}
```

**限制:**
- 超时: 10秒
- 内存: 32MB
- 禁止文件系统和网络访问

---

## 工具节点

### HTTP Request (HTTP请求)

发送HTTP请求:

**配置:**
- Method: GET, POST, PUT, DELETE, PATCH
- URL
- Headers
- Body (JSON, Form, Raw)
- Timeout
- Retry

### Knowledge Retrieval (知识检索)

从知识库检索相关内容:

**配置:**
- Knowledge Base - 选择知识库
- Query - 检索查询
- Top K - 返回条数
- Score Threshold - 相似度阈值

### Tool (工具调用)

调用预定义工具或自定义工具。

---

## 高级节点

### Agent (智能体)

自主规划和执行任务:

- ReAct模式
- Function Calling
- 多轮工具调用

### Variable Assigner (变量赋值)

在工作流中修改变量值。

### Parameter Extractor (参数提取器)

见LLM节点部分。
