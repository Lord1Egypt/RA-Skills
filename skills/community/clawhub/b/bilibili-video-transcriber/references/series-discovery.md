# 系列视频发现与处理（2026-07-19）

## 发现方法

视频详情页会展示同UP主的相关/系列视频。

### 方法1：web_extract 提取视频页
```python
from hermes_tools import web_extract
result = web_extract(urls=[f"https://www.bilibili.com/video/{bvid}"])
# 返回内容中包含系列视频标题+封面图，可解析出系列视频标题
```

### 方法2：UP主空间搜索
```python
# 获取UP主mid后，搜索其视频列表
r = requests.get(f"https://api.bilibili.com/x/space/wbi/arc.search?mid={up_mid}&ps=30&pn=1",
    headers={"User-Agent": "Mozilla/5.0", "Referer": f"https://space.bilibili.com/{up_mid}/"}, timeout=15)
# 注意：WBI签名版API可能需要特殊处理
```

### 方法3：直接搜索BV号
已知标题关键词时，通过搜索API查BV号：
```python
r = requests.get("https://api.bilibili.com/x/web-interface/search/all/v2",
    params={"keyword": "标题关键词", "page": 1},
    headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
for item in r.json().get("data", {}).get("result", []):
    if item.get("result_type") == "video":
        for v in item.get("data", [])[:10]:
            print(f"{v.get('bvid')} | {v.get('title')} | {v.get('duration')}")
```

## 系列视频判断

- **同一UP主 + 同一讲师**：从字幕/标题识别（如"老赵"、"沿路"）
- **超长视频（>3小时）**：通常是系列课程，多章节有独立字幕
- **标题规律**：如"顶尖掼蛋高手 全局透视思维"和"老赵和颜路的掼蛋高手三板斧"是同系列

## 处理策略

| 情况 | 处理方式 |
|------|---------|
| 超长有字幕 | 只获取已有字幕，写入飞书，标注"本集字幕/章节字幕" |
| 无字幕超长 | 不做Whisper全片转写（不现实），告知用户 |
| 有字幕的系列视频 | 批量获取字幕，本地保存JSON+TXT，再逐个写飞书文档 |
| 无字幕短视频（<30分钟） | Whisper转写（后台，tiny模型） |

## 已知系列案例

### 掼蛋系列（UP主：万事如番茄）

| 视频 | BV号 | 时长 | 字幕 |
|------|------|------|------|
| 顶尖掼蛋高手 全局透视思维视频课程 | BV1cm5C6cEvg | 11h37m | ✅209条（本集字幕） |
| 老赵和颜路的掼蛋高手三板斧训练视频课程 | BV1yaB5B3Epq | 19h05m | ⚠️仅6条（片尾） |
| 掼蛋口诀技巧——浓缩版 | BV1uMKSzXEwY | 4m | ✅134条 |
| 掼蛋如何快速记牌 | BV1Wh4y1x7Yx | 5m | ❌无 |
