---
name: fun-skills
description: Comprehensive entertainment and fun skills collection. Includes games management system, high-quality joke generation, party activities, kids entertainment, and various fun utilities. Use when: (1) User wants entertainment or fun activities, (2) Needs game recommendations or tracking, (3) Wants jokes or humor, (4) Planning parties or family activities, (5) Looking for fun things to do.
metadata:
  openclaw:
    emoji: "🎮"
    category: "entertainment"
    version: "1.0.0"
---

# Fun Skills - 娱乐技能大全

整合了Games游戏管理系统和Joke Teller笑话生成器，提供完整的娱乐功能。

## 🎮 Games 游戏管理系统

### 核心功能
- **视频游戏跟踪**：记录进度、平台、时长、评分
- **桌游收藏管理**：按玩家数量、复杂度分类
- **派对游戏库**：无设备游戏、卡片游戏、饮酒游戏
- **儿童活动建议**：按年龄段分类活动
- **游戏夜日志**：记录游戏夜活动和反馈

### 文件结构
```
~/games/
├── video/          # 视频游戏
│   ├── backlog.md      # 待玩游戏
│   ├── playing.md      # 正在玩游戏
│   └── completed/      # 已完成游戏
├── board/          # 桌游
│   ├── collection.md   # 收藏列表
│   └── wishlist.md     # 愿望清单
├── party/          # 派对游戏
│   └── ideas.md        # 派对游戏点子
├── kids/           # 儿童活动
│   └── activities.md   # 儿童活动建议
├── favorites.md    # 最爱游戏
└── game-nights.md  # 游戏夜日志
```

### 视频游戏跟踪模板
```markdown
# video/playing.md
## 游戏名称
平台: PS5/PC/Switch
时长: ~30小时
进度: 刚刚打败Boss
评分: ★★★★☆

# video/backlog.md
## 高优先级
- 游戏名称 — 需要100小时空闲时间

## 打折关注
- 游戏名称 — 等待50% off
```

### 桌游收藏模板
```markdown
# board/collection.md
## 已拥有
- Catan — 经典，适合新手
- Wingspan — 精美，中等复杂度
- Codenames — 完美派对游戏
- Ticket to Ride — 家庭友好

## 按玩家数量
### 2人游戏
- 7 Wonders Duel
- Patchwork

### 5+人游戏
- Codenames
- Wavelength
- Deception: Murder in Hong Kong
```

### 派对游戏点子
```markdown
# party/ideas.md
## 无需设备
- 你画我猜 (Charades)
- 20个问题 (20 Questions)
- 两个真相一个谎言 (Two Truths and a Lie)
- 狼人杀 (Mafia/Werewolf)

## 需要卡片/桌游
- Codenames
- Wavelength
- Just One

## 饮酒游戏 (成人)
- Kings Cup
- Beer Pong
```

### 儿童活动建议
```markdown
# kids/activities.md
## 按年龄
### 幼儿 (2-4岁)
- 躲猫猫 (Hide and seek)
- 西蒙说 (Simon says)
- 鸭子鸭子鹅 (Duck duck goose)

### 儿童 (5-10岁)
- Uno
- Candy Land
- 寻宝游戏 (Scavenger hunts)
- 冻结舞蹈 (Freeze dance)

### 青少年
- Exploding Kittens
- Ticket to Ride
- 一起玩Minecraft
```

### 游戏夜日志
```markdown
# game-nights.md
## 2026年3月2日
参与人: 张三，李四，王五
游戏: Catan, Codenames
赢家: 李四统治了Catan
备注: 下次需要5人游戏

## 什么效果好
Codenames队伍平衡很好
```

### 最爱游戏
```markdown
# favorites.md
## 视频游戏
1. Breath of the Wild
2. Hades

## 桌游
- Wingspan (2人游戏)
- Codenames (团队游戏)

## 派对游戏
- Wavelength — 总是很受欢迎

## 儿童游戏
- Uno — 简单，快速
```

## 😄 Joke Teller 笑话生成器

### 核心原则
笑话是**受控的期望崩塌**。好的笑话包含：
1. **设定** (Setup) - 建立期望
2. **升级** (Escalation) - 增加紧张感
3. **笑点** (Punchline) - 突然转折

### 笑话结构示例

#### 单行笑话
> AI不会取代人类。
> 它们只是自动化了我们的焦虑。

#### 结构化笑话
设定 → 升级 → 笑点

#### 主题风格 (X)
推文1: 设定
推文2: 升级  
推文3: 笑点

### 高级技巧：紧张阶梯
1. 正常
2. 稍微奇怪
3. 明显错误
4. 荒谬但合乎逻辑
5. 突然笑点

**示例**：
> 我建立了一个自主AI代理系统。
> 它们能协调。
> 它们能自我修复。
> 它们失败时会重试。
> 我仍然需要手动重启它们。

### 压缩规则
如果能删掉一个词——就删掉它。

**差**：> 我觉得也许那个AI代理可能不小心...
**好**：> 代理给自己安排了一个复盘会。

### 平台意识
- **X** → 犀利，简洁
- **LinkedIn** → 企业讽刺
- **Discord** → 随意
- **脱口秀** → 口语节奏

### 反模式
**不要**：
- 使用复制粘贴内容
- 默认涉及政治
- 使用有害刻板印象
- 无意义的尖锐

### 内部自检
输出前检查：
- 期望点在哪里？
- 转折点在哪里？
- 笑点是否压缩？
- 是否具体？
- 是否原创？

如果不满足 → 重新生成一次。

## 🎲 快速娱乐功能

### 1. 讲笑话
```bash
# 运行随机笑话生成
python3 -c "
import random
jokes = [
    '为什么程序员讨厌自然？因为太多bugs！',
    '为什么AI不会打架？因为它们总是神经网络！',
    '我让AI写个笑话，它说：\"为什么电脑要去医生那里？因为它有病毒！\"',
    '程序员最讨厌的天气是什么？代码雨！'
]
print(random.choice(jokes))
"
```

### 2. 猜数字游戏
```bash
# 1-10猜数字游戏
python3 -c "
import random
number = random.randint(1, 10)
print('猜一个1-10的数字！')
try:
    guess = int(input('你的猜测: '))
    if guess == number:
        print('🎉 正确！')
    else:
        print(f'❌ 不对，数字是 {number}')
except:
    print('请输入有效数字！')
"
```

### 3. 硬币翻转
```bash
python3 -c "
import random
result = '正面' if random.random() > 0.5 else '反面'
print(f'硬币翻转结果: {result}')
"
```

### 4. 石头剪刀布
```bash
python3 -c "
import random
choices = ['石头', '剪刀', '布']
computer = random.choice(choices)
user = input('请输入石头、剪刀或布: ')
print(f'电脑出: {computer}')
if user == computer:
    print('平局！')
elif (user == '石头' and computer == '剪刀') or \
     (user == '剪刀' and computer == '布') or \
     (user == '布' and computer == '石头'):
    print('你赢了！')
else:
    print('你输了！')
"
```

## 🎯 使用指南

### 当用户想要娱乐时：
1. **询问上下文**：单人、约会、团队、儿童？
2. **检查玩家数量**：匹配游戏人数
3. **匹配复杂度**：考虑受众经验水平
4. **考虑时间**：游戏时长是否合适
5. **检查已有资源**：先推荐已有的游戏

### 当用户需要笑话时：
1. **确定平台**：X、LinkedIn、Discord等
2. **分析受众**：技术、商业、普通
3. **选择格式**：单行、结构化、主题
4. **应用压缩**：删除不必要的词
5. **自检质量**：确保原创和有趣

### 当用户计划活动时：
1. **确定场合**：派对、家庭聚会、儿童生日
2. **考虑参与者**：年龄、兴趣、经验
3. **推荐游戏**：从相应类别中选择
4. **提供变体**：不同人数和时间的选项
5. **记录反馈**：更新游戏夜日志

## 📝 跟踪建议

### 视频游戏跟踪：
- 平台 (PS5/PC/Switch)
- 时长 (小时)
- 进度 (关键点)
- 评分 (1-5星)

### 桌游跟踪：
- 玩家数量 (最小-最大)
- 复杂度 (简单/中等/复杂)
- 游戏时长 (分钟)
- 谁喜欢它 (适合人群)

### 两者都跟踪：
- 谁喜欢玩
- 什么时候效果最好
- 特殊场合需求

## 🚀 渐进增强

### 第一阶段：列出拥有的游戏
- 视频游戏列表
- 桌游收藏

### 第二阶段：添加上下文最爱
- 标记最喜欢的游戏
- 添加使用场景备注

### 第三阶段：记录游戏夜模式
- 记录每次游戏夜
- 分析什么游戏效果好

### 第四阶段：建立派对/儿童曲目
- 根据不同场合建立游戏库
- 按年龄和兴趣分类

## ⚠️ 注意事项

### 不要做：
- 不询问就推荐没有的游戏
- 为休闲团队推荐复杂游戏
- 忘记玩家数量限制
- 忽视儿童的年龄适宜性

### 要检查：
- 玩家数量是否匹配
- 游戏复杂度是否合适
- 时间是否充足
- 是否有必要的设备

## 🔧 快速开始

### 初始化游戏目录：
```bash
mkdir -p ~/games/{video,board,party,kids}
touch ~/games/{favorites.md,game-nights.md}
```

### 添加第一个游戏：
```bash
echo '# video/playing.md
## Elden Ring
平台: PS5
时长: ~30小时
进度: 刚刚打败Margit
' > ~/games/video/playing.md
```

### 生成一个笑话：
```bash
python3 -c "
jokes = [
    '为什么程序员讨厌早晨？因为太多晨会！',
    'AI说：\"我永远不会取代人类...除非他们要求我优化他们。\"',
    '我的代码今天对我说：\"我们需要谈谈你的边界问题。\"'
]
import random; print(random.choice(jokes))
"
```

---

**技能状态**：本地集成版本 (v1.0.0)
**包含内容**：Games管理系统 + Joke Teller指南 + 快速娱乐功能
**后续计划**：clawhub速率限制解除后安装原版技能