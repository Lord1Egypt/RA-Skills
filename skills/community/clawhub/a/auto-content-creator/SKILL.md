---
name: auto-content-creator
description: |
  自动化内容创作助手 - 一键生成抖音/小红书/公众号内容。
  支持：文生文案、图生文案、爆款改写、多平台适配。
  触发词："写文案"、"生成内容"、"小红书"、"抖音"、"公众号"、"content"、"create post"。
  自动输出：标题 + 正文 + 标签 + 发布建议。
author: anyafu
license: MIT
copyright: Copyright © 2026 anyafu. All rights reserved.
---

# Auto Content Creator - 自动化内容创作助手

一键生成多平台爆款内容，让内容创作效率提升 10 倍。

## 支持平台

| 平台 | 内容类型 | 格式特点 |
|------|----------|----------|
| 小红书 | 图文笔记 | emoji 丰富、分段清晰、标签多 |
| 抖音 | 视频文案 | 简短有力、开头抓人、引导互动 |
| 公众号 | 长文 | 结构完整、深度分析、专业感 |
| 朋友圈 | 短文案 | 生活化、真实感、适度营销 |
| 微博 | 短内容 | 热点结合、话题标签、互动性强 |

## 使用方法

### 基础用法

```bash
# 生成小红书文案
auto-content create --platform xiaohongshu --topic "AI 工具推荐"

# 生成抖音文案
auto-content create --platform douyin --topic "职场效率技巧"

# 生成公众号文章
auto-content create --platform wechat --topic "2026AI 趋势分析" --length long
```

### 高级用法

```bash
# 基于素材生成
auto-content create --platform xiaohongshu --input素材.md

# 爆款改写
auto-content rewrite --input 原文.md --platform xiaohongshu

# 批量生成
auto-content batch --topics 话题列表.txt --platform all
```

## 文案模板

### 小红书模板

```
标题：[数字] + [痛点/收益] + [情绪词]

正文：
开头：戳痛点/展示效果
中间：3-5 个核心点（emoji + 短句）
结尾：引导互动 + 标签

标签：#话题 1 #话题 2 #话题 3
```

### 抖音模板

```
开头（3 秒）：[悬念/反差/痛点]
中间（15 秒）：[核心内容/展示]
结尾（5 秒）：[引导关注/评论]

BGM 建议：[音乐类型]
画面建议：[拍摄建议]
```

### 公众号模板

```
标题：[吸引力] + [价值] + [紧迫感]

导语：[背景] + [问题] + [预告]

正文：
一、[小标题 1]
   - 论点 + 论据 + 案例

二、[小标题 2]
   - 论点 + 论据 + 案例

三、[小标题 3]
   - 论点 + 论据 + 案例

结尾：总结 + 行动号召 + 关注引导
```

## 脚本示例

### content-generator.py - 内容生成脚本

```python
#!/usr/bin/env python3
"""
多平台内容生成器
"""
import json
import random
import sys
from datetime import datetime

# 小红书 emoji 库
XHS_EMOJIS = {
    'fire': ['🔥', '💥', '⚡'],
    'star': ['⭐', '✨', '💫'],
    'check': ['✅', '✔️', '✓'],
    'heart': ['❤️', '💕', '💗'],
    'think': ['🤔', '💭', '🧠'],
    'work': ['💼', '💻', '📊'],
    'money': ['💰', '💵', '💎'],
    'time': ['⏰', '📅', '⌚'],
}

# 标题模板
TITLE_TEMPLATES = [
    "打工人必备！{topic} 让我效率翻倍",
    "后悔没早知！{topic} 真的太香了",
    "{topic} 全攻略，看这一篇就够了",
    "亲测有效！{topic} 的{num}个使用技巧",
    "被问爆了！{topic} 到底怎么用",
    "{topic} 避坑指南，新手必看",
    "月入{num} 万，全靠{topic}",
    "{topic} 天花板！用完回不去了",
]

# 开头模板
OPENING_TEMPLATES = [
    "姐妹们！发现一个超级好用的{topic}！",
    "说实话，之前我对{topic} 真没啥期待...",
    "作为一个{role}，我真的太需要这个了！",
    "用了{topic} 一个月，来交作业了！",
    "被{topic} 震惊到了，必须分享给你们！",
]

def generate_xiaohongshu(topic, length='medium'):
    """生成小红书文案"""
    
    # 生成标题
    title_template = random.choice(TITLE_TEMPLATES)
    title = title_template.format(
        topic=topic,
        num=random.choice([3, 5, 7, 10])
    )
    
    # 生成开头
    opening_template = random.choice(OPENING_TEMPLATES)
    opening = opening_template.format(
        topic=topic,
        role=random.choice(['打工人', '创业者', '自由职业者', '学生党'])
    )
    
    # 生成正文
    points = [
        f"{random.choice(XHS_EMOJIS['check'])} {topic} 的核心功能真的绝了",
        f"{random.choice(XHS_EMOJIS['star'])} 操作简单，新手也能快速上手",
        f"{random.choice(XHS_EMOJIS['fire'])} 效率提升不止一倍",
        f"{random.choice(XHS_EMOJIS['heart'])} 性价比超高，强烈推荐",
        f"{random.choice(XHS_EMOJIS['think'])} 适合人群：{random.choice(['打工人', '学生', '创业者'])}",
    ]
    
    content = "\n\n".join(points[:random.randint(3, 5)])
    
    # 生成结尾
    ending = f"""
总之，{topic} 真的值得试试！
有疑问评论区见～ {random.choice(XHS_EMOJIS['heart'])}
"""
    
    # 生成标签
    tags = [
        f"#{topic.replace(' ', '')}",
        "#好物推荐",
        "#效率工具",
        "#干货分享",
        "#宝藏 APP",
        "#打工人必备",
    ]
    
    return {
        'title': title,
        'opening': opening,
        'content': content,
        'ending': ending,
        'tags': ' '.join(tags),
        'platform': 'xiaohongshu'
    }

def generate_douyin(topic, length='short'):
    """生成抖音文案"""
    
    hooks = [
        f"你知道吗？{topic} 能让你效率翻倍！",
        f"还在为{topic.split()[0] if ' ' in topic else '这个'}烦恼？看这里！",
        f"30 秒教会你{topic} 的正确用法！",
        f"用了{topic}，我真的回不去了...",
    ]
    
    cta = [
        "关注我，获取更多干货！",
        "评论区告诉我你的想法！",
        "点赞收藏，不然找不到了！",
        "转发给需要的人！",
    ]
    
    return {
        'hook': random.choice(hooks),
        'content': f"今天给大家分享一下{topic}的使用技巧...",
        'cta': random.choice(cta),
        'bgm': "轻快 BGM",
        'platform': 'douyin'
    }

def generate_wechat(topic, length='long'):
    """生成公众号文章大纲"""
    
    return {
        'title': f"{topic} 完全指南：从入门到精通",
        'outline': [
            "一、什么是{topic}？",
            "二、为什么需要{topic}？",
            "三、{topic} 的核心功能",
            "四、{topic} 使用教程",
            "五、{topic} 常见问题",
            "六、总结与建议",
        ],
        'platform': 'wechat'
    }

def main():
    if len(sys.argv) < 3:
        print("用法：python3 content-generator.py <platform> <topic>")
        print("平台：xiaohongshu | douyin | wechat")
        sys.exit(1)
    
    platform = sys.argv[1]
    topic = sys.argv[2]
    length = sys.argv[3] if len(sys.argv) > 3 else 'medium'
    
    if platform == 'xiaohongshu':
        result = generate_xiaohongshu(topic, length)
    elif platform == 'douyin':
        result = generate_douyin(topic, length)
    elif platform == 'wechat':
        result = generate_wechat(topic, length)
    else:
        print(f"不支持的平台：{platform}")
        sys.exit(1)
    
    # 输出结果
    print(f"\n{'='*50}")
    print(f"📝 {platform} 文案生成完成")
    print(f"{'='*50}\n")
    
    if platform == 'xiaohongshu':
        print(f"📌 标题：{result['title']}\n")
        print(f"{result['opening']}\n")
        print(f"{result['content']}\n")
        print(f"{result['ending']}")
        print(f"\n🏷️  标签：{result['tags']}")
    elif platform == 'douyin':
        print(f"🎬 开头：{result['hook']}\n")
        print(f"📹 内容：{result['content']}\n")
        print(f"💬 结尾：{result['cta']}\n")
        print(f"🎵 BGM 建议：{result['bgm']}")
    elif platform == 'wechat':
        print(f"📰 标题：{result['title']}\n")
        print("📋 大纲：")
        for section in result['outline']:
            print(f"  {section}")
    
    print(f"\n{'='*50}")

if __name__ == '__main__':
    main()
```

## 使用场景

### 1. 产品推广

```bash
# 为新产品生成全平台内容
auto-content create --topic "AI 写作工具" --platform all
```

### 2. 知识分享

```bash
# 生成教程类内容
auto-content create --topic "Python 入门教程" --platform xiaohongshu
```

### 3. 热点追踪

```bash
# 结合热点生成内容
auto-content create --topic "Sora AI" --platform douyin --hot
```

### 4. 批量生产

```bash
# 批量生成一周内容
auto-content batch --topics 本周话题.txt --platform xiaohongshu
```

## 变现模式

### 免费层
- 每日 5 次基础生成
- 标准模板
- 支持 3 个平台

### 付费层（¥49/月）
- 无限次生成
- 高级模板库
- 支持所有平台
- 批量生成
- 历史记录

### 企业层（¥299/月）
- 定制模板
- 品牌语调适配
- API 访问
- 团队协作

## 下一步

1. [ ] 完成脚本开发
2. [ ] 添加更多模板
3. [ ] 集成 AI 优化
4. [ ] 发布到 ClawHub
5. [ ] 制作演示视频

---

## 📜 License

**Copyright © 2026 anyafu. All rights reserved.**

Licensed under the MIT License.

### MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### 商业使用

- ✅ 允许个人和商业使用
- ✅ 允许修改和分发
- ✅ 允许私有化部署
- ⚠️ 如需闭源商业授权，请联系作者 anyafu
