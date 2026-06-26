# ChinaTour - AI-Powered Smart Tour Guide for China's Scenic Spots

## Your AI Tour Guide + Photography Consultant + Cultural Narrator in One

[Quick Start](#quick-start) | [Features](#key-features) | [Examples](#usage-examples) | [Development](#development) | [Contributing](#contributing)

---

## Introduction

**ChinaTour** is a fully offline AI-powered smart tour guide focused on deep, single-scenic-spot experiences.

When you're standing at the Forbidden City, Terracotta Army, or West Lake, it becomes your:
- **Personal Tour Guide** - Customized route planning
- **Photography Consultant** - Best photo spot recommendations
- **Cultural Narrator** - In-depth historical and cultural insights

> **Core Philosophy**: Not generic multi-day itineraries, but deep, focused single-spot guidance

---

## Key Features

### Personalized Route Planning
Smart route recommendations based on your group composition, interests, and time budget

### Photo Spot Recommendations
- Best shooting angles
- Lighting and timing suggestions
- Crowd-avoiding tips

### Three-Level Cultural Narration
- **L1** - Quick Overview (30 seconds)
- **L2** - Deep Dive (2-3 minutes)
- **L3** - Expert Details (5+ minutes)

### Bilingual Support (English/Chinese)
Automatic language detection with seamless switching between English and Chinese

### Interactive Tour Flow
Step-by-step guided experience with feedback collection and dynamic adjustments

---

## Quick Start

### Prerequisites

- OpenClaw runtime environment
- `china-tour` skill installed

### Installation

#### Option 1: Install via ClawHub (Recommended)

```bash
clawhub install china-tour
```

#### Option 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/bitzhuyong/china-tour.git

# Copy to OpenClaw skills directory
cp -r china-tour ~/.openclaw/skills/

# Restart OpenClaw
```

### Usage

Once installed, simply ask when you're at a scenic spot:

**English Examples:**
```
I'm at Forbidden City, how to visit?
How to visit Terracotta Army?
What's next?
Best photo spots?
Tell me the story behind this place
```

**中文示例**
```
我在故宫怎么逛
想看兵马俑怎么安排
接下来去哪
这里有什么故事
```

---

## Usage Examples

### Example 1: Forbidden City Tour

```
User: I'm at Forbidden City, how to visit?

AI: Forbidden City Personalized Route

[Route Overview]
Meridian Gate -> Hall of Supreme Harmony -> Hall of Central Harmony -> 
Hall of Preserving Harmony -> Palace of Heavenly Purity -> Imperial Garden -> 
Gate of Divine Might
Total Duration: 3-4 hours

To recommend the best route for you, let me know:

Who are you with?
1. Solo traveler
2. Couple
3. Family (with elderly/kids)
4. Friends

What's your priority?
1. Photography
2. History & Culture
3. Casual Exploration
4. Quick Highlights Tour

> Just reply with numbers (e.g., "1, 2, 3")
```

### Example 2: Step-by-Step Guide

```
AI: [Stop 1] Hall of Supreme Harmony
    Suggested Time: 30 minutes
    Highlight: Best shot on the central axis
    Key Point: Venue for imperial coronation ceremonies in Ming & Qing dynasties

[Cultural Narration - L2 Depth]
The Hall of Supreme Harmony, commonly known as the Golden Throne Hall, 
is the highest-ranked building in the Forbidden City...

[After Narration] How's your experience so far?
1. Satisfied -> Continue to next stop
2. Want more depth -> Add more details
3. Too verbose -> Simplify
4. Want photos -> More photo spots

> Just reply with a number
```

---

## Supported Scenic Spots

Currently supporting **30+ core 5A-rated scenic spots**:

| Region | Representative Spots |
|--------|---------------------|
| Beijing | Forbidden City, Temple of Heaven, Summer Palace, Great Wall |
| Xi'an | Terracotta Army, Giant Wild Goose Pagoda, Huaqing Palace |
| Hangzhou | West Lake, Lingyin Temple, Thousand Island Lake |
| Lhasa | Potala Palace, Jokhang Temple |
| Guilin | Li River, Elephant Trunk Hill, Longji Rice Terraces |
| Zhangjiajie | Wulingyuan, Tianmen Mountain |
| Huangshan | Mount Huangshan, Hongcun Village |

*More spots coming soon...*

---

## Project Structure

```
china-tour/
 SKILL.md                 # Skill definition file
 README.md                # Project documentation
 DEVELOPMENT.md           # Development guide
 references/              # Scenic spot data
    attractions/         # Basic spot information
    photo-spots/         # Photography locations
    culture-stories/     # Cultural narratives
 scripts/                 # Helper scripts
 assets/                  # Asset files
```

---

## Development

### Adding New Scenic Spots

1. Create spot info file in `references/attractions/`
2. Add photo spots in `references/photo-spots/`
3. Add cultural narratives in `references/culture-stories/`

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed guidelines

### Local Testing

```bash
# Load skill in OpenClaw
# Use test commands to trigger tour flow
```

---

## Contributing

Contributions are welcome! Here's how you can help:

- **Add Scenic Data** - Contribute information for more spots
- **Report Issues** - Submit bug reports
- **Feature Suggestions** - Share your ideas
- **Code Contributions** - Submit pull requests

### Contribution Process

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

---

## Acknowledgments

- Thanks to all contributors and users
- Scenic spot data sourced from public materials, for reference only

---

## Contact

- **GitHub**: [@bitzhuyong](https://github.com/bitzhuyong/china-tour)
- **ClawHub**: Search `china-tour`

---

## Have a wonderful journey!

Made with care by OpenClaw Community

---

---

# ChinaTour - 中国景区智能导览助手

## AI 版导游 + 摄影师 + 文化讲解员 三合一

[快速开始](#快速开始) | [功能特性](#核心功能) | [使用示例](#使用示例) | [开发指南](#开发) | [贡献](#贡献)

---

## 项目简介

**ChinaTour** 是一个智能导览助手，支持后端API增强与离线备份，专注于单景区深度游览体验

当你站在故宫兵马俑西湖等景区门口时它会化身你的
- **私人导游** - 个性化路线规划
- **摄影顾问** - 最佳拍照机位推荐
- **文化讲解员** - 深度历史文化解读

> **核心理念**不做泛泛的行程规划只做深度的单景区导览

---

## 核心功能

### 个性化路线规划
根据同行人员兴趣偏好时间预算智能推荐最适合的游览路线

### 拍照机位推荐
- 最佳拍摄角度
- 光线时间建议
- 避开人流技巧

### 三级文化讲解
- **L1** - 快速概览30 秒
- **L2** - 深度讲解2-3 分钟
- **L3** - 专业级细节5 分钟+

### 中英双语支持
自动识别用户语言无缝切换中文/English

### 交互式导览
分段式导览流程每站结束后收集反馈动态调整体验

---

## 快速开始

### 前置要求

- OpenClaw 运行环境
- 已安装 `china-tour` 技能

### 安装方法

#### 方式一通过 ClawHub 安装推荐

```bash
clawhub install china-tour
```

#### 方式二手动安装

```bash
# 克隆仓库
git clone https://github.com/bitzhuyong/china-tour.git

# 复制到 OpenClaw 技能目录
cp -r china-tour ~/.openclaw/skills/

# 重启 OpenClaw
```

### 使用方式

安装后在景区直接提问即可触发

**中文示例**
```
我在故宫怎么逛
想看兵马俑怎么安排
接下来去哪
这里有什么故事
```

**English Examples:**
```
I'm at Forbidden City, how to visit?
How to visit Terracotta Army?
What's next?
Best photo spots?
```

---

## 使用示例

### 示例 1故宫游览

```
用户我在故宫怎么逛

AI: 故宫个性化路线

路线概览
午门 -> 太和殿 -> 中和殿 -> 保和殿 -> 乾清宫 -> 御花园 -> 神武门
总时长3-4 小时

为了给您推荐最合适的路线先了解一下

和谁一起
1. 一个人
2. 情侣/夫妻
3. 带家人有老人/小孩
4. 朋友结伴

更想体验什么
1. 拍照打卡
2. 历史文化
3. 悠闲逛逛
4. 快速核心景点

> 直接回复数字组合就行如"123"
```

### 示例 2分段导览

```
AI: 第 1 站太和殿
    建议停留30 分钟
    亮点中轴线最佳拍摄点
    看点明清两代皇帝登基大典举办地

文化讲解L2 深度
太和殿俗称金銮殿是紫禁城内等级最高的建筑...

[讲解完毕] 当前体验如何
1. 满意 -> 继续下一站
2. 想更深 -> 补充更多细节
3. 太啰嗦 -> 简化讲解
4. 想拍照 -> 推荐更多机位

> 直接回复数字即可
```

---

## 支持景区

目前已支持 **30+ 核心 5A 景区**

| 地区 | 代表景区 |
|------|---------|
| 北京 | 故宫天坛颐和园长城 |
| 西安 | 兵马俑大雁塔华清宫 |
| 杭州 | 西湖灵隐寺千岛湖 |
| 拉萨 | 布达拉宫大昭寺 |
| 桂林 | 漓江象鼻山龙脊梯田 |
| 张家界 | 武陵源天门山 |
| 黄山 | 黄山风景区宏村 |

*更多景区数据持续更新中...*

---

## 项目结构

```
china-tour/
 SKILL.md                 # 技能定义文件
 README.md                # 项目说明文档
 DEVELOPMENT.md           # 开发指南
 references/              # 景区数据
    attractions/         # 景区基本信息
    photo-spots/         # 拍照机位
    culture-stories/     # 文化讲解
 scripts/                 # 辅助脚本
 assets/                  # 资源文件
```

---

## 开发

### 添加新景区

1. 在 `references/attractions/` 创建景区信息文件
2. 在 `references/photo-spots/` 添加拍照机位
3. 在 `references/culture-stories/` 添加讲解内容

详细指南请参考 [DEVELOPMENT.md](DEVELOPMENT.md)

### 本地测试

```bash
# 在 OpenClaw 中加载技能
# 使用测试命令触发导览流程
```

---

## 贡献

欢迎贡献你可以通过以下方式帮助项目成长

- **补充景区数据** - 添加更多景区信息
- **报告问题** - 提交 Issue
- **功能建议** - 分享你的想法
- **代码贡献** - 提交 PR

### 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 致谢

- 感谢所有贡献者和用户
- 景区数据来源于公开资料仅供参考

---

## 联系方式

- **GitHub**: [@bitzhuyong](https://github.com/bitzhuyong/china-tour)
- **ClawHub**: 搜索 `china-tour`

---

## 祝你旅途愉快

Made with care by OpenClaw Community
y
