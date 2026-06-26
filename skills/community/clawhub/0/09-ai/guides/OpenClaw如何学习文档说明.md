# 💡 关于OpenClaw学习文档的说明

## ✅ 可以做什么

### 1. OpenClaw会自动读取SKILL.md

如果你把MD文档放在正确的位置：

```
~/.openclaw/skills/fpsp-advisor/SKILL.md
```

OpenClaw会：
- ✅ 自动读取这个文件
- ✅ 了解skill的功能和用法
- ✅ 在对话中参考这些内容
- ✅ 根据文档描述来响应你的请求

**但是**：
- ❌ 不会自动安装Python依赖
- ❌ 不会自动执行代码
- ❌ 不会自动配置环境

---

## 🤔 正确的理解

### OpenClaw的"学习"是指

1. **读取文档**：读取SKILL.md和references/下的文档
2. **理解功能**：了解这个skill能做什么
3. **响应请求**：根据文档内容回复你的问题
4. **调用工具**：如果你提供了工具脚本，它会在对话中调用

**不是**：
- ❌ 自动安装pip包
- ❌ 自动配置环境
- ❌ 自动执行独立脚本

---

## ✅ 正确的做法

### 第1步：准备Skill文件

确保文件在正确位置：

```bash
~/.openclaw/skills/fpsp-advisor/
├── SKILL.md                    # 主文档（OpenClaw会读）
├── references/                 # 参考文档（OpenClaw会读）
│   ├── news_analysis.md
│   ├── market_analysis.md
│   └── ...
└── tools/                     # 工具脚本（需要手动调用）
    └── stock_api_final.py
```

### 第2步：安装Python依赖（手动）

```bash
pip install requests pandas numpy
```

### 第3步：在对话中"教"OpenClaw使用

**通过对话来教OpenClaw**：

```
用户: 我有一个股票数据API，位置在~/.openclaw/skills/fpsp-advisor/tools/stock_api_final.py

OpenClaw: 明白了，我知道这个API的位置。

用户: 当我问"查询股票"时，请调用这个API

OpenClaw: 好的，我记住了。

用户: 查询600519

OpenClaw: [调用API并返回结果]
```

---

## 🎯 推荐的完整流程

### 流程1：基于现有Skill（已安装）

**你的情况**：
- ✅ FPSP-A Skill已经在 `~/.openclaw/skills/fpsp-advisor/`
- ✅ SKILL.md已经被OpenClaw读取
- ✅ references/文档可被引用

**下一步**：
1. 安装Python依赖（一次性）
2. 在OpenClaw对话中告诉它如何使用API

**示例对话**：

```
用户: 我可以在FPSP-A中使用股票数据API了，位置是~/.openclaw/skills/fpsp-advisor/tools/stock_api_final.py

OpenClaw: 明白了！你现在可以使用股票数据API了。

用户: 以后当我说"查询股票XX"时，请调用这个API获取实时行情

OpenClaw: 好的，我记住了。

用户: 查询600519

OpenClaw: 让我为你调用股票API...
      [执行查询并返回结果]
      贵州茅台 (600519): 1491.66 (+1.69%)
```

### 流程2：创建新的Skill

如果你想创建一个全新的skill给别人：

**第1步**：创建skill目录

```bash
mkdir -p ~/.openclaw/skills/my-stock-api
```

**第2步**：创建SKILL.md（关键格式）

```markdown
---
name: my-stock-api
description: 我的股票数据API，支持实时行情查询
version: 1.0.0
---

# 我的股票API

## 功能

- 查询实时行情
- 获取指数数据
- 批量监控

## 使用方法

查询股票：
```
查询600519
```

查看市场：
```
市场概况
```
```

**第3步**：确保OpenClaw识别

```bash
openclaw skills list | grep my-stock-api
```

---

## 📝 对话式"教学"示例

### 教OpenClaw使用API

**第1次对话**：

```
用户: 我有一个股票API在~/.openclaw/skills/fpsp-advisor/tools/stock_api_final.py，
它有几个主要功能：
1. get_realtime(symbol) - 获取实时行情
2. get_index(code) - 获取指数
3. get_batch_quotes(symbols) - 批量获取

OpenClaw: 明白了，我已经记录了这个API的位置和功能。

用户: 当我说"查股票XX"时，请调用get_realtime方法

OpenClaw: 好的，我会记住这个规则。
```

**第2次对话**：

```
用户: 查询600519

OpenClaw: 我来为你调用股票API...
      [调用API]
      贵州茅台: 1491.66 (+1.69%)
```

**第3次对话**（以后不需要再教）：

```
用户: 查询000001

OpenClaw: [自动调用API]
      平安银行: 12.35 (-0.56%)
```

---

## 🔄 工作流程对比

### ❌ 错误理解

```
用户: 把文档丢给OpenClaw，它会自动学习、安装、执行

OpenClaw: ...
      [期望：自动安装、自动调用]

实际情况:
- ✅ OpenClaw会读取文档
- ❌ OpenClaw不会自动安装依赖
- ❌ OpenClaw不会自动执行脚本
```

### ✅ 正确理解

```
用户: 把文档放好位置 + 安装依赖 + 对话式教学

OpenClaw:
第1步: 读取SKILL.md（自动）
第2步: 在对话中学习用法（交互式）
第3步: 根据对话调用API（需要你的指导）
```

---

## 💡 最佳实践

### 实践1：在SKILL.md中写清楚使用方法

```markdown
## 使用方法

### 命令行调用

```bash
cd ~/.openclaw/skills/fpsp-advisor/tools
python3 stock_query.py "600519"
```

### Python代码调用

```python
from stock_api_final import StockAPI
api = StockAPI()
quote = api.get_realtime('600519')
```

### OpenClaw对话调用

当你说"查询600519"时，我会：
1. 读取stock_api_final.py
2. 创建StockAPI实例
3. 调用get_realtime('600519')
4. 返回结果
```

### 实践2：创建wrapper函数

在SKILL.md中添加：

```markdown
## Wrapper函数

OpenClaw可以直接调用以下函数：

```python
# 在tools/stock_query.py中
def query_stock(symbol):
    api = StockAPI()
    return api.get_realtime(symbol)
```

对话示例：
- "查询600519" → 调用query_stock('600519')
- "市场概况" → 调用get_index('000001')等
```

---

## ✅ 总结

### OpenClaw能自动做的

- ✅ 读取SKILL.md
- ✅ 读取references/文档
- ✅ 理解skill功能
- ✅ 根据文档响应请求

### 需要手动做的

- ⚠️ 安装Python依赖（pip install）
- ⚠️ 初始化配置
- ⚠️ 在对话中教OpenClaw如何使用
- ⚠️ 提供工具脚本让OpenClaw调用

### 推荐：混合方式

1. **文档部分**：通过MD文档让OpenClaw了解功能
2. **依赖部分**：手动安装（一次性）
3. **使用部分**：通过对话教OpenClaw如何调用
4. **工具部分**：提供wrapper函数供OpenClaw调用

---

## 🎯 你的情况

### 已经完成的

- ✅ FPSP-A Skill已创建在正确位置
- ✅ SKILL.md已有正确格式（YAML front matter）
- ✅ references/文档已创建
- ✅ 工具脚本已创建

### 下一步

**第1步**：安装Python依赖

```bash
pip install requests pandas numpy
```

**第2步**：在OpenClaw对话中教它使用

```
用户: 我在FPSP-A skill中添加了股票数据API，位置在
~/.openclaw/skills/fpsp-advisor/tools/stock_api_final.py

主要功能：
- get_realtime(symbol) - 实时行情
- get_index(code) - 指数数据

请记住这个功能，以后我说"查询XX"时请调用它。

OpenClaw: 明白了！
```

**第3步**：直接使用

```
用户: 查询600519

OpenClaw: [根据你的指示调用API]
```

---

## 📚 相关概念

### RAG（检索增强生成）

OpenClaw使用RAG：
1. **检索**：从你的文档中搜索相关内容
2. **增强**：将搜索结果与你的问题结合
3. **生成**：生成回复

所以：
- ✅ 文档会被索引和检索
- ✅ OpenClaw会根据文档回答
- ❌ 但不会自动执行代码

### Agent行为

OpenClaw作为Agent：
- ✅ 可以读取文件
- ✅ 可以理解文档
- ✅ 可以调用工具（如果提供）
- ❌ 不会自动安装依赖

---

## 🎉 结论

### 简单来说

**可以部分自动**：
- ✅ MD文档可以让OpenClaw"学习"功能
- ✅ SKILL.md会被自动读取
- ❌ 但需要手动安装依赖
- ❌ 需要在对话中教它如何调用

### 最佳做法

1. **文档自动**：通过MD文档让OpenClaw了解功能
2. **依赖手动**：手动安装Python包
3. **交互式学习**：通过对话教OpenClaw使用
4. **持续优化**：根据使用情况调整

### 实际流程

```
你的MD文档
  ↓
OpenClaw读取并索引
  ↓
在对话中你教OpenClaw如何使用
  ↓
OpenClaw学会了（记住规则）
  ↓
以后可以直接对话使用
```

---

## 💡 立即尝试

### 第1步：确认skill已识别

```bash
openclaw skills info fpsp-advisor
```

### 第2步：在对话中"教"OpenClaw

```
用户: 我在FPSP-A中添加了股票API，位置在~/.openclaw/skills/fpsp-advisor/tools/stock_api_final.py，
有get_realtime、get_index等功能。请记住这个位置和功能。

OpenClaw: 明白了。
```

### 第3步：测试使用

```
用户: 请用这个API查询600519

OpenClaw: 我来调用API查询600519...
      [执行并返回结果]
```

---

**总结**：OpenClaw会自动读取文档，但需要你：
1. 手动安装依赖（pip install）
2. 在对话中教它如何使用
3. 提供清晰的工具脚本

**关键**：文档 + 依赖安装 + 对话式教学 = 完整的OpenClaw Skill！