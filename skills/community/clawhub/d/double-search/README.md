# Double Search Skill

双重搜索功能，支持Tavily和Kimi两个搜索引擎的并行搜索和结果合并。

## 📋 特性

- ✅ **双引擎并行搜索**：同时使用Tavily和Kimi
- ✅ **智能结果合并**：自动合并、去重和排序
- ✅ **异步高效**：基于asyncio的高性能实现
- ✅ **错误容错**：单个搜索失败不影响整体
- ✅ **一键安装**：包含安装脚本和配置向导
- ✅ **无需复杂配置**：支持环境变量和.env文件

## 🚀 快速开始

### 方式1：一键安装（推荐）

```bash
cd ~/.openclaw/skills/double-search
chmod +x install.sh
./install.sh
```

### 方式2：手动安装

```bash
# 1. 安装Python依赖
pip install aiohttp python-dotenv

# 2. 设置环境变量
export TAVILY_API_KEY="tvly-xxxxxxxxxxxx"
export KIMI_API_KEY="your_kimi_api_key_here"

# 3. 测试搜索功能
python3 __init__.py
```

## 📖 使用方法

### 基本用法

```python
from double_search import DoubleSearcher

async def search(query: str):
    searcher = DoubleSearcher()
    results = await searcher.search(query)
    return results
```

### 高级用法

```python
from double_search import DoubleSearcher

async def advanced_search(query: str):
    searcher = DoubleSearcher()

    # 自定义参数
    results = await searcher.search(
        query=query,
        merge_results=True,
        limit_per_source=3
    )

    return results
```

## 📚 API文档

### DoubleSearcher类

| 方法 | 说明 |
|------|------|
| `search(query, merge_results=True, limit_per_source=5)` | 执行搜索 |

### 返回格式

```json
{
  "query": "搜索内容",
  "merged_results": [
    {
      "title": "结果标题",
      "url": "https://example.com",
      "snippet": "结果摘要",
      "source": "tavily"
    }
  ],
  "source_breakdown": {
    "tavily": [...],
    "kimi": [...]
  }
}
```

## 🔧 配置

### 环境变量

```bash
# 必需
TAVILY_API_KEY=tvly-xxxxxxxxxxxx

# 可选（不设置则只使用Tavily）
KIMI_API_KEY=your_kimi_api_key_here
```

### .env文件

```bash
# .env文件示例
TAVILY_API_KEY=tvly-xxxxxxxxxxxx
KIMI_API_KEY=your_kimi_api_key_here
```

## 📝 示例代码

运行示例代码：

```bash
python3 example.py
```

示例包括：
- 基本搜索
- 自定义搜索查询
- 不合并结果
- 过滤特定领域结果
- 市场分析任务
- 比较不同搜索引擎

## 🔍 测试

执行内置测试：

```bash
python3 __init__.py
```

## 🛠️ 故障排除

### 问题：搜索无结果

```bash
# 检查API Keys
echo $TAVILY_API_KEY
echo $KIMI_API_KEY

# 验证API Keys有效性
```

### 问题：Python模块未找到

```bash
# 确保在正确的工作目录
cd ~/.openclaw/skills/double-search

# 检查Python路径
which python3
```

### 问题：依赖缺失

```bash
# 重新安装依赖
pip install -r requirements.txt
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 支持

如有问题，请查看SKILL.md文档或运行示例代码。

---

**版本**: 1.0.0
**更新日期**: 2026-03-27
**作者**: 028 Team
