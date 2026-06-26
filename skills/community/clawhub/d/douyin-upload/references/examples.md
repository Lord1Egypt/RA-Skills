# 抖音发布技能使用示例

## 1. 基本使用

### 发布文章到抖音

```bash
# 基本命令
python3 scripts/main.py "人工智能的发展"

# 跳过发布，仅生成内容和图片
python3 scripts/main.py "人工智能的发展" --skip-publish

# 显示技能状态
python3 scripts/main.py --status

# 显示可用主题分类
python3 scripts/main.py --categories
```

### 交互式使用

```python
from scripts.main import DouyinUploadSkill

# 初始化技能
skill = DouyinUploadSkill()

# 处理主题
theme = "人工智能"
result = skill.process_theme(theme)

# 检查结果
if result.get("success"):
    print("发布成功！")
else:
    print("发布失败:", result.get("error"))
```

## 2. 高级使用

### 自定义配置

```python
from scripts.main import DouyinUploadSkill
from scripts.config import CONTENT_GENERATION, IMAGE_GENERATION

# 修改配置
CONTENT_GENERATION["temperature"] = 0.9
IMAGE_GENERATION["size"] = "1792x1024"

# 初始化并使用
skill = DouyinUploadSkill()
result = skill.process_theme("我的新主题")
```

### 批量处理

```python
from scripts.main import DouyinUploadSkill

skill = DouyinUploadSkill()
themes = [
    "人工智能",
    "旅游攻略", 
    "美食制作",
    "学习方法"
]

for theme in themes:
    result = skill.process_theme(theme)
    print(f"主题 '{theme}' 处理完成")
```

## 3. 与OpenAI集成

### 创建OpenAI API配置

```python
import os
from scripts.config import CONTENT_GENERATION, IMAGE_GENERATION

# 设置API密钥
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# 修改配置为使用OpenAI
CONTENT_GENERATION["model"] = "gpt-4"
IMAGE_GENERATION["model"] = "dall-e-3"

# 初始化技能
skill = DouyinUploadSkill()
```

### 生成高质量内容

```python
# 使用高质量模型
from scripts.config import CONTENT_GENERATION, IMAGE_GENERATION

CONTENT_GENERATION["model"] = "gpt-4"
CONTENT_GENERATION["temperature"] = 0.8

skill = DouyinUploadSkill()
result = skill.process_theme("高质量文章主题")
```

## 4. 错误处理

### 常见错误及解决方案

```python
from scripts.main import DouyinUploadSkill

skill = DouyinUploadSkill()

try:
    result = skill.process_theme("测试主题")
    
    if not result.get("success"):
        error = result.get("error")
        print(f"错误类型:")
        print(f"- {error}")
        
        # 根据错误类型处理
        if "sau命令不可用" in error:
            print("请安装抖音自动发布工具")
        elif "模型加载失败" in error:
            print("请检查网络连接或API密钥")
            
except ValueError as e:
    print(f"输入错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

## 5. 日志分析

### 查看发布日志

```bash
# 查看最新的发布日志
ls -la ~/.openclaw/workspace/logs/ | grep process_log_ | tail -5

# 查看详细的发布结果
cat ~/.openclaw/workspace/logs/process_log_*.json | python -m json.tool
```

### 日志格式

```json
{
  "timestamp": "2026-03-10T22:00:00",
  "theme": "人工智能",
  "version": "1.0.0",
  "success": true,
  "steps": {
    "content": {
      "success": true,
      "path": "/path/to/article.md"
    },
    "image": {
      "success": true,
      "path": "/path/to/cover.jpg"
    },
    "publish": {
      "success": true,
      "output": "抖音API响应内容",
      "response": {...}
    }
  }
}
```

## 6. 自定义主题处理

### 创建自定义主题分类

```python
from scripts.config import THEME_CATEGORIES

# 添加新的分类
THEME_CATEGORIES["编程"] = ["Python", "JavaScript", "Java", "开发", "代码"]

# 重新初始化技能
from scripts.main import DouyinUploadSkill
skill = DouyinUploadSkill()
```

### 自定义封面风格

```python
from scripts.config import COVER_STYLES

# 添加新的封面风格
COVER_STYLES.append("游戏风格")
COVER_STYLES.append("学术风格")

# 重新初始化技能
from scripts.main import DouyinUploadSkill
skill = DouyinUploadSkill()
```

## 7. 性能优化

### 缓存机制

```python
import os
from scripts.main import DouyinUploadSkill

# 设置缓存目录
cache_dir = os.path.expanduser("~/.openclaw/workspace/cache")
os.makedirs(cache_dir, exist_ok=True)

# 避免重复生成相同主题的内容
if os.path.exists(f"{cache_dir}/{theme}.md"):
    print("主题已缓存，跳过生成")
else:
    skill = DouyinUploadSkill()
    result = skill.process_theme(theme)
```

## 8. 调试模式

### 启用详细日志

```python
import logging
from scripts.main import DouyinUploadSkill

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

# 初始化并使用技能
skill = DouyinUploadSkill()
result = skill.process_theme("调试主题")
```

### 查看详细输出

```python
from scripts.main import DouyinUploadSkill

skill = DouyinUploadSkill()

# 获取技能状态
status = skill.get_skill_status()
print("技能状态:")
print(status["requirements"])

# 获取可用分类
categories = skill.get_available_categories()
print("可用分类:", categories)
```

## 9. 常见问题

### Q: 为什么生成的内容质量不高？
A: 尝试：
1. 更换模型（gpt-3.5-turbo vs gpt-4）
2. 调整temperature参数
3. 使用更强的API密钥

### Q: 封面图片生成失败？
A: 检查：
1. OpenAI API密钥是否正确
2. 网络连接是否正常
3. 是否有其他图片生成器可用

### Q: 发布到抖音失败？
A: 检查：
1. sau命令是否已正确安装
2. 抖音账号是否已授权
3. 文章内容是否符合规范

## 10. 最佳实践

1. **定期更新主题分类** - 根据内容趋势调整分类
2. **监控发布日志** - 及时发现和解决问题
3. **使用缓存机制** - 避免重复生成相同内容
4. **定期备份** - 重要内容需要备份
5. **性能监控** - 监控生成过程的性能

---

*最后更新: 2026年3月10日*