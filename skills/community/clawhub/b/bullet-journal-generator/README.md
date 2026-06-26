# 子弹笔记生成器（Bullet Journal Generator）

将零散的自然语言输入转换为规范的子弹笔记格式，支持多种输出格式和Obsidian集成。

## ✨ 功能特性

- 📝 **智能处理**：自动识别时间、分类内容、润色语言
- 🎯 **符号系统**：使用标准子弹笔记符号（● ○ – > < ☆）
- 🔗 **Obsidian集成**：工作学习内容自动生成符合规范的日志（标签、双链）
- 🎨 **可视化卡片**：生成带日期、天气、温度的精美HTML卡片
- 🖨️ **打印版本**：生成适合打印的A4格式文档
- 💾 **自动保存**：多格式自动保存，便于归档和备份

## 🚀 快速开始

### 基本使用

```bash
# 进入scripts目录
cd scripts

# 运行主程序
python3 main.py
```

### 输入示例

```
09:00 今天要把有机逆合成的逻辑和思路整理出来最好自动化。去买卫生纸，预约羽毛球场地
09:17 老板突然紧急需要的立项书，我先把摘要写出来
明天超市有打折的鸡蛋
最近的股票市场波动比较大，要尝试新的分析方法了
```

### 输出内容

程序会自动生成以下文件：

1. **子弹笔记文本** (`data/YYYY/MM/DD/bullet_journal.txt`)
   - 规范化的子弹笔记格式
   - 包含日期、天气、温度
   - 使用标准符号系统

2. **Obsidian日志** (`data/YYYY/MM/DD/YYYY-MM-DD.md`)
   - 仅包含工作学习相关内容
   - 支持标签系统和双链
   - 符合Obsidian规范

3. **HTML卡片** (`cards/YYYY-MM-DD.html`)
   - 手写风格设计
   - 可视化展示
   - 响应式布局

4. **打印版本** (`printable/YYYY-MM-DD.html`)
   - A4格式优化
   - 高分辨率打印
   - 留有手写空间

5. **JSON数据** (`data/YYYY/MM/DD/data.json`)
   - 结构化数据
   - 便于程序处理
   - 自动备份

## 📁 项目结构

```
bullet-journal-gen/
├── SKILL.md                    # Skill定义文件
├── README.md                   # 本文件
├── scripts/                    # 核心脚本
│   ├── __init__.py
│   ├── main.py                # 主入口（推荐使用）
│   ├── process_notes.py       # 语言润色与分类
│   ├── generate_bullet_journal.py    # 生成子弹笔记文本
│   ├── generate_obsidian_log.py       # 生成Obsidian日志
│   ├── generate_card.py              # 生成HTML卡片
│   ├── generate_pdf.py               # 生成打印版本
│   ├── get_weather.py                # 获取天气信息
│   └── save_notes.py                 # 文件保存与管理
├── templates/                  # HTML模板
│   ├── card_template.html     # 卡片模板
│   └── print_template.html    # 打印模板
├── data/                      # 数据存储
│   ├── YYYY/
│   │   └── MM/
│   │       └── DD/
│   │           ├── bullet_journal.txt
│   │           ├── YYYY-MM-DD.md
│   │           └── data.json
│   └── backup/               # 备份目录
├── cards/                     # HTML卡片
│   └── YYYY-MM-DD.html
└── printable/                 # 打印版本
    └── YYYY-MM-DD.html
```

## 🔧 符号系统说明

| 符号 | 类型 | 说明 | 示例 |
|------|------|------|------|
| ● | 任务 | 待办事项 | ● 整理有机逆合成逻辑 |
| ○ | 事件 | 已发生或计划的活动 | ○ 09:17 紧急处理立项书 |
| – | 笔记 | 想法、灵感、关键信息 | – 股票市场波动较大 |
| > | 迁移 | 未完成推迟的任务 | > 购买卫生纸（推迟至明日） |
| < | 计划 | 未来安排 | < 明天 家家悦购买鸡蛋 |
| ☆ | 优先 | 高优先级任务 | ☆ 有机逆合成自动化整理 |

## 💡 使用技巧

### 1. 语言润色规则

系统会自动转换以下口语化表达：

- "要把" → "整理/处理/完成"
- "突然" → 紧急标注（☆或前缀）
- "最好" → 目标补充
- "想一想" → "思考/研究"
- "看一下" → "查看/了解"

### 2. 工作学习识别

系统会自动识别以下关键词为工作学习内容：

```
项目、报告、分析、研究、学习、会议、文档、代码、
开发、设计、策划、立项、数据、实验、逆合成、
股票、市场、技术、方法、方案、总结、优化、整理
```

这些内容会自动合并到Obsidian日志中。

### 3. 时间格式

支持以下时间格式：

- `09:00` - 24小时制
- `09时00分` - 中文时间
- `明天` - 未来日期
- `下周` - 未来日期

### 4. Obsidian集成

生成的Obsidian日志包含：

- **Frontmatter**：日期、标签、类型
- **双链**：`[[项目名称/子标题]]` 格式
- **标签系统**：work, study, plan, observe, think
- **结构化内容**：优先任务、任务、事件、思考与观察、下一步行动

## 🎨 自定义配置

### 修改天气信息

编辑 `scripts/get_weather.py`，替换为真实的天气API：

```python
def fetch_weather_from_api(self) -> Optional[Dict]:
    # 替换为真实的天气API
    # 示例：和风天气、高德天气等
    pass
```

### 自定义符号系统

编辑 `scripts/process_notes.py`：

```python
SYMBOLS = {
    'task': '●',
    'event': '○',
    'note': '–',
    'migration': '>',
    'scheduled': '<',
    'priority': '☆'
}
```

### 自定义HTML样式

编辑 `templates/card_template.html` 或 `templates/print_template.html`，修改CSS样式。

## 📊 使用场景

### 场景1：日常记录

```
今天要完成周报，下午3点开会。晚上去健身房。
明天记得给客户打电话。
```

输出：
```
● 完成周报
○ 15:00 团队会议
○ 晚间 健身房训练
< 明天 给客户打电话
```

### 场景2：工作学习

```
最近股票波动大，要试试新方法。老板要项目摘要，我先写一下。
```

Obsidian日志：
```markdown
---
date: 2025-03-16
tags: [工作, 研究]
type: daily_log
---

## 任务
- [[立项书/项目摘要]] 准备项目摘要 ⭐

## 思考与观察
[[股票分析/市场波动]] 市场波动较大，研究新方法
```

### 场景3：混合内容

系统会自动区分工作学习内容和生活内容：

- 工作学习 → Obsidian日志
- 所有内容 → 子弹笔记文本
- 所有内容 → HTML卡片和打印版本

## 🔗 集成Obsidian

### 方法1：手动导入

1. 打开生成的 `data/YYYY/MM/DD/YYYY-MM-DD.md` 文件
2. 复制内容到Obsidian
3. 粘贴到Daily Notes

### 方法2：自动同步（待开发）

可配置Obsidian Vault路径，实现自动同步。

## 🛠️ 高级用法

### 单独使用各个脚本

```bash
# 仅处理笔记
python3 process_notes.py

# 仅生成Obsidian日志
python3 generate_obsidian_log.py

# 仅生成HTML卡片
python3 generate_card.py

# 仅生成打印版本
python3 generate_pdf.py
```

### 批量处理

编辑 `main.py`，添加批量处理逻辑：

```python
# 处理多日笔记
dates = ['2025-03-16', '2025-03-17', '2025-03-18']
for date in dates:
    # 读取该日的输入
    with open(f"inputs/{date}.txt") as f:
        raw_input = f.read()
    # 处理
    generator.process_input(raw_input, date=date)
```

## 📝 示例对比

### 输入
```
09:00 今天要把有机逆合成的逻辑和思路整理出来最好自动化。去买卫生纸，预约羽毛球场地
09:17 老板突然紧急需要交给政府的立项书，我先把摘要写出来
明天家家悦有打折的鸡蛋
最近的股票市场波动比较大，要尝试新的分析方法了
```

### 输出：子弹笔记
```
2025-03-16 (周日) | ☀️ 晴 | 15°C

○ 09:00 今天整理有机逆合成的逻辑和思路出来目标：自动化。去买卫生纸，预约羽毛球场地
☆ 09:17 老板紧急需要交给政府的立项书，我先把摘要写出来
< 明天家家悦有打折的鸡蛋
– 最近的股票市场波动比较大，要尝试新的分析方法
```

### 输出：Obsidian日志
```markdown
---
date: 2025-03-16
tags: ['2025-03', 'observe', 'plan', 'study', 'think', 'work']
type: daily_log
---

# 2025-03-16 日志

## 优先任务

- [[立项书/政府项目]] 老板紧急需要交给政府的立项书，我先把摘要写出来 ⭐

## 事件

- 09:00 今天整理有机逆合成的逻辑和思路出来目标：自动化。去买卫生纸，预约羽毛球场地

## 思考与观察

[[股票分析/市场波动]] 最近的股票市场波动比较大，要尝试新的分析方法

## 下一步行动

- [ ] 老板紧急需要交给政府的立项书，我先把摘要写出来
```

## 🎯 下一步计划

- [ ] 添加天气API集成
- [ ] 支持批量处理多日笔记
- [ ] Obsidian Vault自动同步
- [ ] Web界面支持
- [ ] 移动端适配
- [ ] 统计分析功能

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📮 联系方式

如有问题或建议，请通过Issue反馈。

---

**享受你的子弹笔记之旅！** ✨
