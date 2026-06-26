# Fun Skills 娱乐技能

由于clawhub速率限制，这是一个本地集成的娱乐技能包，包含了Games游戏管理系统和Joke Teller笑话生成器的完整功能。

## 🎯 功能概述

### 🎮 Games 游戏管理系统
- 视频游戏跟踪（进度、平台、评分）
- 桌游收藏管理（按玩家数量、复杂度分类）
- 派对游戏库（无设备游戏、卡片游戏、饮酒游戏）
- 儿童活动建议（按年龄段分类）
- 游戏夜日志记录

### 😄 Joke Teller 笑话生成器
- 高质量笑话生成（技术、通用、企业类别）
- 多种笑话格式（单行、结构化、主题风格）
- 笑话生成指南和原理
- 平台适配建议

### 🎲 快速娱乐功能
- 猜数字游戏
- 硬币翻转
- 石头剪刀布
- 骰子滚动
- 幸运数字生成
- 命运预测

## 📁 文件结构

```
fun-skills/
├── SKILL.md                    # 主技能文件
├── README.md                   # 说明文件
└── scripts/                    # 辅助脚本
    ├── init_games_directory.sh  # 初始化游戏目录
    ├── joke_generator.py       # 笑话生成器
    └── quick_fun.py           # 快速娱乐脚本
```

## 🚀 快速开始

### 1. 初始化游戏目录
```bash
# 运行初始化脚本
bash scripts/init_games_directory.sh

# 或手动创建
mkdir -p ~/games/{video,board,party,kids}
```

### 2. 使用笑话生成器
```bash
# 生成随机笑话
python3 scripts/joke_generator.py

# 生成技术类笑话
python3 scripts/joke_generator.py tech

# 生成单行笑话
python3 scripts/joke_generator.py oneliner

# 查看笑话指南
python3 scripts/joke_generator.py guide
```

### 3. 使用快速娱乐
```bash
# 启动娱乐中心
python3 scripts/quick_fun.py

# 直接玩特定游戏
python3 scripts/quick_fun.py 猜数字
python3 scripts/quick_fun.py 硬币翻转
python3 scripts/quick_fun.py 石头剪刀布
```

## 📝 使用示例

### 添加正在玩的游戏
```bash
echo '# video/playing.md
## Elden Ring
平台: PS5
时长: ~30小时
进度: 刚刚打败Margit
评分: ★★★★☆
' > ~/games/video/playing.md
```

### 生成企业笑话
```bash
python3 scripts/joke_generator.py corporate
```

### 玩猜数字游戏
```bash
python3 scripts/quick_fun.py 猜数字
```

## 🎮 Games 系统详细使用

### 视频游戏跟踪
- **位置**: `~/games/video/playing.md` - 正在玩的游戏
- **位置**: `~/games/video/backlog.md` - 待玩游戏列表
- **跟踪项**: 平台、时长、进度、评分

### 桌游收藏管理
- **位置**: `~/games/board/collection.md` - 已有桌游
- **位置**: `~/games/board/wishlist.md` - 愿望清单
- **分类**: 按玩家数量、复杂度、游戏时长

### 派对游戏库
- **位置**: `~/games/party/ideas.md`
- **分类**: 无需设备、需要卡片/桌游、饮酒游戏

### 儿童活动建议
- **位置**: `~/games/kids/activities.md`
- **分类**: 幼儿(2-4)、儿童(5-10)、青少年

### 最爱游戏
- **位置**: `~/games/favorites.md`
- **分类**: 视频游戏、桌游、派对游戏、儿童游戏

### 游戏夜日志
- **位置**: `~/games/game-nights.md`
- **记录**: 日期、参与人、游戏、赢家、备注

## 😄 Joke Teller 高级功能

### 笑话结构
1. **设定** (Setup) - 建立期望
2. **升级** (Escalation) - 增加紧张感
3. **笑点** (Punchline) - 突然转折

### 紧张阶梯技巧
```python
1. 正常
2. 稍微奇怪
3. 明显错误
4. 荒谬但合乎逻辑
5. 突然笑点
```

### 压缩规则
- 如果能删掉一个词，就删掉它
- 保持简洁、直接

### 平台适配
- **X**: 犀利，简洁
- **LinkedIn**: 企业讽刺
- **Discord**: 随意
- **脱口秀**: 口语节奏

## 🔧 技能集成

### 通过旺财使用
告诉旺财：
- "我想玩个游戏"
- "讲个笑话"
- "推荐派对游戏"
- "记录我刚玩的游戏"

### 手动使用
直接运行上述脚本命令，或编辑游戏目录中的文件。

## ⏰ 原版技能安装状态

由于clawhub速率限制，原版技能安装暂未成功。已设置定时重试：

- 重试时间: 09:30, 10:30, 11:30
- 目标技能: games, joke-teller
- 当前状态: 等待速率限制解除

## 📞 支持

如有问题或需要新功能：
1. 通过飞书联系旺财
2. 编辑技能文件自定义功能
3. 等待原版技能安装成功

---

**版本**: 1.0.0 (本地集成版)
**更新日期**: 2026-03-02
**状态**: 功能完整，可立即使用