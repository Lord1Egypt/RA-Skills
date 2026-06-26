---
name: bilibili-hot
description: "自动抓取Bilibili全站排行榜视频数据，包含详细的视频统计信息"
metadata: { "openclaw": { "emoji": "📺", "requires": { "bins": ["node"] } } }
---

# Skill: Bilibili热搜抓取

自动抓取Bilibili全站排行榜视频数据，包含详细的视频统计信息。

## 触发方式

```
B站热搜
bilibili hot
获取B站热榜
B站热门
b站排行榜
```

## 能力

- 使用Bilibili官方API获取全站排行榜
- 抓取Top 50热门视频的完整信息
- 提取视频标题、UP主、播放量、弹幕数等详细数据
- 返回结构化视频数据（JSON格式）
- 生成易读的文本格式输出

## 输出格式

```json
[
  {
    "rank": 1,
    "title": "⚡对 对 子 战 神⚡",
    "up": "洛温阿特金森",
    "play": "863.0万播放",
    "danmu": "4.0万弹幕",
    "like": "86.1万点赞",
    "coin": "22.2万投币",
    "favorite": "26.9万收藏",
    "score": 0,
    "link": "https://www.bilibili.com/video/BV1bXAJz8EYC",
    "type": "全站榜"
  }
]
```

控制台输出示例：

```
📊 Bilibili全站排行榜 (Top 50):
================================================================================
 1. ⚡对 对 子 战 神⚡
   👤 UP主: 洛温阿特金森
   📺 863.0万播放
   💬 4.0万弹幕
   👍 86.1万点赞
   🪙 22.2万投币
   ⭐ 26.9万收藏
```

## 配置

无需额外配置！使用B站官方API，无需安装Puppeteer。

依赖：Node.js内置的`https`模块。

## API说明

使用Bilibili官方排行榜API：
- `https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all`
- rid=0 表示全站
- type=all 表示综合排名

## 数据存储

抓取结果保存到：
1. `workspace/scripts/bilibili-hot.json` - JSON格式
2. `workspace/scripts/bilibili-hot.txt` - 文本格式

## 示例对话

```
用户: B站热搜
助手: 🎯 开始抓取Bilibili热搜...
      📊 Bilibili全站排行榜 (Top 50):
      1. ⚡对 对 子 战 神⚡
         👤 UP主: 洛温阿特金森
         📺 863.0万播放
         💬 4.0万弹幕
         👍 86.1万点赞
      ✅ 已保存到 bilibili-hot.json
```

## 优势

1. **速度快**：直接调用API，无需浏览器启动
2. **数据全**：获取完整的视频统计信息
3. **稳定**：使用官方API，不易被屏蔽
4. **轻量**：无需Puppeteer，节省资源

## 扩展功能

可添加以下功能：
1. 分区排行榜（游戏、动画、知识等）
2. 热搜词抓取
3. 历史数据对比
4. 数据可视化图表

### 分区API示例
- 动画区: `rid=1`
- 游戏区: `rid=4`
- 知识区: `rid=36`

## 维护

更新脚本位置：`skills/bilibili-hot/bilibili-hot.js`

如果API变更，需要更新：
1. API端点URL
2. 数据解析逻辑