# 抖音发布技能

## 🚀 一键自动发布抖音文章内容

这是一个专门用于自动发布抖音文章的智能技能，用户只需提供主题，技能会自动生成Markdown格式的文章内容和封面图片，然后调用已安装的抖音自动发布命令行工具进行发布。

## ✨ 主要特点

- 🤖 **智能内容生成**：根据主题自动生成吸引人的文章内容
- 🖼️ **智能封面生成**：自动生成与文章主题相关的封面图片  
- 🚀 **一键发布**：调用`sau`命令自动发布到抖音
- ⚡ **高效自动化**：无需手动制作内容和图片
- 🎯 **高质量输出**：AI生成的标题和内容具有吸引力
- 🔧 **高度可定制**：支持自定义主题分类、图片风格等

## 🎯 使用方式

### 基本使用

```bash
# 发布文章到抖音
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

## 📁 文件结构

```
~/.openclaw/extensions/douyin/skills/douyin-upload/
├── SKILL.md                    # 技能描述文档
├── scripts/
│   ├── main.py                # 主模块
│   ├── generate_content.py    # 内容生成脚本
│   ├── generate_image.py      # 图片生成脚本  
│   ├── publish.py             # 发布脚本
│   ├── config.py              # 配置文件
│   ├── requirements.txt       # 依赖要求
│   └── install.sh             # 安装脚本
├── references/
│   ├── examples.md            # 使用示例
│   └── README.md              # 本文件
└── .env                       # 环境变量配置文件
```

## ⚙️ 配置说明

### 环境变量

创建 `~/.openclaw/extensions/douyin/skills/douyin-upload/.env` 文件：

```bash
# 抖音发布技能环境变量配置
OPENAI_API_KEY=your_openai_api_key_here
```

### 配置文件

编辑 `scripts/config.py`：

```python
# 内容生成配置
CONTENT_GENERATION = {
    "model": "gpt-4",  # 可选：gpt-4, gpt-3.5-turbo
    "max_tokens": 1000,
    "temperature": 0.7
}

# 发布配置
PUBLISH_CONFIG = {
    "sau_command": "sau",
    "platform": "douyin",
    "account_name": "xiaoA"
}
```

## 📦 安装步骤

### 1. 环境准备

```bash
# 安装Python依赖
pip install -r scripts/requirements.txt

# 安装PIL
pip install Pillow

# 安装可选依赖
pip install requests pytest
```

### 2. 配置sau命令

确保抖音自动发布命令行工具已正确安装并配置：

```bash
# 检查sau命令
which sau

# 如果未安装，参考官方文档安装
# https://github.com/your-sau-repo
```

### 3. 配置API密钥（可选）

如果需要高质量的内容生成，配置OpenAI API密钥：

```bash
export OPENAI_API_KEY="your-api-key"
```

## 🔧 高级功能

### 自定义主题分类

```python
from scripts.config import THEME_CATEGORIES, COVER_STYLES

# 添加新的分类
THEME_CATEGORIES["编程"] = ["Python", "JavaScript", "开发"]
COVER_STYLES.append("科技感")

# 重新初始化技能
from scripts.main import DouyinUploadSkill
skill = DouyinUploadSkill()
```

### 批量处理

```python
from scripts.main import DouyinUploadSkill

skill = DouyinUploadSkill()
themes = ["人工智能", "旅游攻略", "美食制作"]

for theme in themes:
    result = skill.process_theme(theme)
    print(f"主题 '{theme}' 处理完成")
```

## 📊 性能优化

### 缓存机制

```python
import os

# 设置缓存目录
cache_dir = os.path.expanduser("~/.openclaw/workspace/cache")
os.makedirs(cache_dir, exist_ok=True)

# 避免重复生成相同主题的内容
if os.path.exists(f"{cache_dir}/{theme}.md"):
    print("主题已缓存，跳过生成")
```

## 🐛 故障排除

### 常见错误

| 错误信息 | 解决方案 |
|---------|---------|
| `sau命令不可用` | 安装并配置抖音自动发布工具 |
| `模型加载失败` | 检查网络连接或API密钥 |
| `文件验证失败` | 检查sau命令和抖音账号 |
| `封面生成失败` | 检查PIL和网络连接 |

## 📈 使用示例

### 示例1：发布科技内容

```bash
python3 scripts/main.py "人工智能的技术趋势"
```

**输出**：
- 自动生成关于人工智能的文章内容
- 生成科技风格的封面图片
- 调用sau命令发布到抖音

### 示例2：发布生活内容

```bash
python3 scripts/main.py "健康生活的5个技巧"
```

**输出**：
- 自动生成生活类文章
- 生成温馨风格的封面
- 一键发布到抖音

### 示例3：批量处理

```python
from scripts.main import DouyinUploadSkill

skill = DouyinUploadSkill()
themes = [
    "旅游攻略",
    "美食制作", 
    "学习方法"
]

for theme in themes:
    result = skill.process_theme(theme)
    if result.get("success"):
        print(f"✓ '{theme}' 发布成功")
    else:
        print(f"✗ '{theme}' 发布失败: {result.get('error')}")
```

## 🎯 最佳实践

1. **定期更新配置** - 根据实际需求调整模型和参数
2. **监控发布日志** - 查看日志文件了解发布状态
3. **质量检查** - 发布前检查内容和图片质量
4. **错误处理** - 实现完善的错误处理机制
5. **性能优化** - 使用缓存和批量处理提升效率

## 📞 支持与反馈

如遇到问题或有改进建议，欢迎：

1. 查看详细的[使用示例](references/examples.md)
2. 参考[故障排除](#-故障排除)部分
3. 提交问题反馈

---

*版本: 1.0.0*  
*创建日期: 2026年3月10日*  
*作者: 抖音发布技能团队*