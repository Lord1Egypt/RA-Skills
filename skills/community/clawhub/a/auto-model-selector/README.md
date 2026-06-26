# 智能路由技能使用指南

## 简介
智能路由技能可以根据用户问题的复杂度自动选择合适的AI模型进行处理。

## 快速开始

### 1. 测试技能
```bash
# 测试简单请求
./smart_router.sh "现在几点了"

# 测试复杂请求  
./smart_router.sh "帮我写一个Flutter登录页面"

# 使用Python直接测试
python3 main.py "现在几点了"
```

### 2. 输出示例
```json
{
  "complexity": "simple",
  "model": "ollama-local/deepseek-r1-7b",
  "reason": "简单请求，使用本地模型处理",
  "method": "pattern",
  "prompt_length": 5,
  "skill": "smart-router",
  "version": "1.0.0"
}
```

### 3. 集成到OpenClaw
将技能目录移动到OpenClaw技能目录：
```bash
# 复制到OpenClaw技能目录
cp -r smart-router ~/.openclaw/skills/

# 或者使用clawdhub安装（如果发布到clawdhub）
clawdhub install smart-router
```

## API接口

### Python API
```python
from smart_router import router

# 获取路由结果
result = router.route_request("现在几点了")
print(f"推荐模型: {result['model']}")

# 直接获取模型名称
model = router.get_recommended_model("现在几点了")
```

### Shell API
```bash
# 获取完整路由信息
./smart_router.sh "用户请求内容"

# 只获取模型名称（适合脚本使用）
./smart_router.sh "用户请求内容" | jq -r '.model'
```

## 配置

### 修改Ollama主机地址
编辑 `smart_router.py`：
```python
class SmartRouter:
    def __init__(self, ollama_host: str = "http://192.168.10.14:11434"):
        # 修改这里的地址
```

### 自定义路由规则
编辑 `smart_router.py` 中的模式列表：
- `simple_patterns`: 简单请求模式
- `complex_patterns`: 复杂请求模式

## 路由逻辑

### 判断流程
1. **快速模式匹配**：使用预定义关键词匹配
2. **模型判断**：如果快速匹配失败，使用deepseek-r1:1.5b模型判断
3. **缓存机制**：相同请求会缓存结果，提高性能

### 简单任务示例
- "现在几点了"
- "列出文件"
- "天气怎么样"
- "提醒我开会"

### 复杂任务示例
- "写一个登录页面"
- "解释量子力学"
- "分析代码性能"
- "设计系统架构"

## 性能优化

### 缓存机制
- 相同请求会缓存路由结果
- 减少模型调用次数
- 提高响应速度

### 快速匹配
- 使用正则表达式快速判断
- 避免不必要的模型调用
- 支持中英文关键词

## 故障排除

### 常见问题
1. **Ollama连接失败**
   - 检查Ollama服务是否运行
   - 检查网络连接
   - 修改`ollama_host`配置

2. **模型不可用**
   - 检查模型是否已下载：`ollama list`
   - 下载所需模型：`ollama pull deepseek-r1:7b`

3. **Python依赖问题**
   - 确保已安装requests库：`pip install requests`

### 日志输出
技能会输出详细日志，包括：
- 使用的判断方法（pattern/model）
- 判断结果
- 推荐模型和理由

## 扩展开发

### 添加新语言支持
在模式列表中添加新的语言关键词：
```python
simple_patterns = [
    # 中文
    r'^(你好|嗨)',
    # 英文
    r'^(hi|hello)',
    # 日文
    r'^(こんにちは|はい)',
]
```

### 添加自定义判断逻辑
继承`SmartRouter`类并重写方法：
```python
class CustomRouter(SmartRouter):
    def custom_check(self, prompt: str) -> Optional[str]:
        # 自定义判断逻辑
        pass
```

## 版本历史
- v1.0.0 (2026-03-05): 初始版本发布
  - 支持快速模式匹配
  - 支持模型判断
  - 缓存机制
  - 完整的API接口

## 许可证
MIT License