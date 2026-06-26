#!/bin/bash
# 初始化游戏目录结构

GAMES_DIR="$HOME/games"

echo "🎮 初始化游戏目录结构..."
echo "位置: $GAMES_DIR"

# 创建主目录
mkdir -p "$GAMES_DIR"

# 创建子目录
mkdir -p "$GAMES_DIR/video"
mkdir -p "$GAMES_DIR/board" 
mkdir -p "$GAMES_DIR/party"
mkdir -p "$GAMES_DIR/kids"

# 创建模板文件
echo "# 视频游戏 - 正在玩
## 游戏名称
平台: PS5/PC/Switch
时长: ~小时
进度: 
评分: ★★★★☆
" > "$GAMES_DIR/video/playing.md"

echo "# 视频游戏 - 待玩列表
## 高优先级
- 游戏名称 — 需要时间

## 打折关注  
- 游戏名称 — 等待折扣
" > "$GAMES_DIR/video/backlog.md"

echo "# 桌游收藏
## 已拥有
- Catan — 经典，适合新手
- Wingspan — 精美，中等复杂度

## 按玩家数量
### 2人游戏
- 7 Wonders Duel
- Patchwork

### 5+人游戏  
- Codenames
- Wavelength
" > "$GAMES_DIR/board/collection.md"

echo "# 桌游愿望清单
- 游戏名称 — 理由
" > "$GAMES_DIR/board/wishlist.md"

echo "# 派对游戏点子
## 无需设备
- 你画我猜 (Charades)
- 20个问题 (20 Questions)

## 需要卡片/桌游
- Codenames
- Wavelength

## 饮酒游戏 (成人)
- Kings Cup
- Beer Pong
" > "$GAMES_DIR/party/ideas.md"

echo "# 儿童活动建议
## 按年龄
### 幼儿 (2-4岁)
- 躲猫猫 (Hide and seek)
- 西蒙说 (Simon says)

### 儿童 (5-10岁)
- Uno
- Candy Land

### 青少年
- Exploding Kittens
- Ticket to Ride
" > "$GAMES_DIR/kids/activities.md"

echo "# 最爱游戏
## 视频游戏
1. 游戏名称

## 桌游
- 游戏名称

## 派对游戏
- 游戏名称

## 儿童游戏  
- 游戏名称
" > "$GAMES_DIR/favorites.md"

echo "# 游戏夜日志
## 日期
参与人: 
游戏: 
赢家: 
备注: 

## 什么效果好

## 下次改进
" > "$GAMES_DIR/game-nights.md"

echo "✅ 游戏目录结构初始化完成！"
echo ""
echo "📁 目录结构:"
tree "$GAMES_DIR" 2>/dev/null || find "$GAMES_DIR" -type f | sed 's|'"$GAMES_DIR"'/|    |g'

echo ""
echo "🎯 接下来可以:"
echo "1. 编辑 $GAMES_DIR/video/playing.md 添加正在玩的游戏"
echo "2. 编辑 $GAMES_DIR/board/collection.md 添加桌游收藏"
echo "3. 使用 'fun-skills' 技能获取游戏建议"