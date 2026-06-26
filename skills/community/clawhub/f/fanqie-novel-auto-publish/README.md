# novel-auto-publish

AI小说创作 + 番茄小说自动发布 一条龙技能

整合了三个开源技能：
- **open-novel-writing** - AI小说创作，从想法到完整正文
- **novel-generator** - 中文爽文快速生成
- **fanqie-publisher** - 番茄小说自动发布

## 特点

- 一站式服务，从想法到发布一键完成
- 自动格式转换，适配番茄要求
- 支持继续创作发布，自动化推进
- 内置质量检查，不达标自动修订

## 安装

```bash
# 依赖三个技能已经装好：
clawhub install open-novel-writing
clawhub install novel-generator
clawhub install fanqie-publisher

# 然后安装本整合技能：
# 已经手动安装到 ~/.openclaw/skills/novel-auto-publish
```

## 使用方法

### 1. 检查登录状态
```bash
cd ~/.openclaw/skills/novel-auto-publish/scripts
python main.py check
python main.py login  # 如果没登录
```

### 2. 从头开始一条龙
```bash
python main.py full "你的小说想法" "番茄上的作品名" [章节数]

# 示例：
python main.py full "都市重生回到2010年做移动互联网" "重生之我是互联网大佬" 5
```

完整流程：
1. **open-novel-writing** 根据想法生成设定、大纲
2. 自动批量生成N章正文，经过评审和修订
3. 转换格式为番茄要求
4. **fanqie-publisher** 自动逐章发布到你指定的作品

### 3. 继续发布已创作章节
```bash
python main.py continue "作品名" /path/to/open-novel-project 起始章 结束章

# 示例：
python main.py continue "重生之我是互联网大佬" ./projects/rebirth-internet 6 10
```

## 目录结构

```
novel-auto-publish/
├── SKILL.md              # OpenClaw 技能描述
├── README.md             # 本文件
└── scripts/
    ├── __init__.py
    ├── config.py         # 配置
    ├── main.py           # 命令行入口
    ├── auto_publish.py   # 主流程协调
    └── format_converter.py # 格式转换
```

## 配置

编辑 `scripts/config.py`：

```python
DEFAULT_CHAPTER_COUNT = 5      # 默认生成章节数
PASSING_SCORE = 85             # 评审通过分数
PUBLISH_INTERVAL_SECONDS = 5   # 发布间隔（防封禁）
```

## 工作流程

```
用户想法
    ↓
┌─────────────────────────┐
│  open-novel-writing      │
│  - 世界观设定            │
│  - 人物设定              │
│  - 故事大纲              │
│  - 逐章生成 + 评审修订  │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│  格式转换                │
│  提取标题和正文          │
│  保存为可发布格式        │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│  fanqie-publisher       │
│  按顺序发布到番茄        │
└─────────────────────────┘
    ↓
✅ 发布完成，等待读者
```

## 依赖

- Python 3.8+
- open-novel-writing 技能
- fanqie-publisher 技能
- 已登录番茄小说作家账号

## 许可证

遵循上游技能的许可证。

---

企业开发·定制技能请联系Wx：CChenJ_
