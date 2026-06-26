#!/usr/bin/env python3
"""
Auto Content Creator v2.0 - 智能内容生成器
用法：python3 content-generator.py <platform> <topic> [选项]

Copyright © 2026 anyafu. All rights reserved.
Licensed under MIT License.
"""

import json
import os
import sys
import random
import hashlib
from datetime import datetime
from pathlib import Path

# 配置
CONFIG = {
    'output_dir': '/tmp/auto-content',
    'version': '2.0',
}

# 增强版 Emoji 库
EMOJIS = {
    'fire': ['🔥', '💥', '⚡', '✨', '💫'],
    'star': ['⭐', '🌟', '💫', '✦', '🌠'],
    'check': ['✅', '✔️', '✓', '☑️', '🆗'],
    'heart': ['❤️', '💕', '💗', '💖', '💓'],
    'think': ['🤔', '💭', '🧠', '💡', '🤓'],
    'work': ['💼', '💻', '📊', '📈', '🖥️'],
    'money': ['💰', '💵', '💎', '🏆', '💹'],
    'time': ['⏰', '📅', '⌚', '🕐', '📆'],
    'alert': ['⚠️', '❗', '❌', '🚫', '⛔'],
    'gift': ['🎁', '🎉', '🎊', '🌈', '🎀'],
    'love': ['😍', '🥰', '😘', '💕', '💝'],
    'cool': ['😎', '🤩', '🚀', '🔥', '💯'],
    'cry': ['😭', '😢', '💔', '😞', '😔'],
    'laugh': ['😂', '🤣', '😆', '😄', '😊'],
}

# 爆款标题模板库（按平台分类）
TITLE_TEMPLATES = {
    'xiaohongshu': [
        "打工人必备！{topic} 让我效率翻倍",
        "后悔没早知！{topic} 真的太香了",
        "{topic} 全攻略，看这一篇就够了",
        "亲测有效！{topic} 的{num}个使用技巧",
        "被问爆了！{topic} 到底怎么用",
        "{topic} 避坑指南，新手必看",
        "月入{num} 万，全靠{topic}",
        "{topic} 天花板！用完回不去了",
        "偷偷用{topic}，同事都以为我开挂了",
        "答应我！一定要试试{topic}",
        "救命！{topic} 也太好用了吧",
        "我真的会谢！{topic} 绝绝子",
        "咱就是说！{topic} 必须拥有",
        "一整个爱住！{topic} 真香警告",
        "狠狠安利！{topic} 都给我去买",
    ],
    'douyin': [
        "30 秒教会你{topic}",
        "{topic} 的正确打开方式",
        "用了{topic}，我后悔了...",
        "关于{topic}，90% 的人都不知道",
        "{topic} 居然还能这样用？",
        "千万别买{topic}！除非你看完了",
        "曝光{topic} 的真相！",
        "{topic} 翻车现场...",
        "因为{topic}，我被骂了",
        "挑战用{topic} 做到...",
    ],
    'wechat': [
        "{topic} 完全指南：从入门到精通",
        "深度解析：{topic} 的底层逻辑",
        "{topic} 实战手册",
        "为什么你应该关注{topic}？",
        "{topic} 的{num}个关键认知",
        "揭秘{topic} 背后的真相",
        "{topic}：一场正在发生的革命",
        "万字长文：{topic} 全解析",
    ],
    'weibo': [
        "# {topic}# 这个话题火了！",
        "刚刚发现{topic}，太实用了",
        "求推荐好用的{topic}",
        "{topic} 到底值不值得入手？",
        "关于{topic}，我有话要说",
        "被{topic} 圈粉了！",
    ],
    'friends': [
        "最近在用{topic}，感觉不错",
        "被{topic} 惊艳到了",
        "花{money} 买了{topic}，真香",
        "安利一个神器：{topic}",
        "{topic}，用过回不去",
    ],
}

# 开头钩子模板
OPENING_TEMPLATES = [
    "姐妹们！发现一个超级好用的{topic}！",
    "说实话，之前我对{topic} 真没啥期待...",
    "作为一个{role}，我真的太需要这个了！",
    "用了{topic} 一个月，来交作业了！",
    "被{topic} 震惊到了，必须分享给你们！",
    "今天必须安利这个{topic}！",
    "花{money} 买的{topic}，到底值不值？",
    "朋友推荐的{topic}，结果...",
    "刷到{topic} 的时候我心动了",
    "纠结了很久，终于入手了{topic}",
]

# 结尾模板
ENDING_TEMPLATES = {
    'xiaohongshu': [
        "总之，{topic} 真的值得试试！",
        "有疑问评论区见～",
        "喜欢的姐妹记得点赞收藏哦！",
        "下期想看什么内容？评论区告诉我！",
        "关注我，获取更多好物分享！",
    ],
    'douyin': [
        "关注我，获取更多干货！",
        "评论区告诉我你的想法！",
        "点赞收藏，不然找不到了！",
        "转发给需要的人！",
        "下期更精彩！",
    ],
    'wechat': [
        "如果你觉得这篇文章有帮助，欢迎分享到朋友圈！",
        "关注公众号，获取更多深度内容！",
        "有任何问题，欢迎在评论区留言！",
        "下期再见！",
    ],
    'weibo': [
        "转评赞走一波～",
        "你怎么看？评论区聊聊",
        "关注我，不迷路",
    ],
    'friends': [
        "有需要的朋友可以试试",
        "亲测有效，推荐给大家",
        "有问题私我",
    ],
}

# 标签库
TAGS_LIBRARY = {
    'xiaohongshu': [
        "#好物推荐", "#效率工具", "#干货分享", "#宝藏 APP",
        "#打工人必备", "#学习工具", "#职场干货", "#自我提升",
        "#科技数码", "#软件推荐", "#APP 推荐", "#神器推荐",
        "#生活小技巧", "#实用工具", "#种草", "#安利",
    ],
    'douyin': [
        "#干货分享", "#知识科普", "#实用技巧", "#生活小妙招",
        "#职场", "#学习", "#成长", "#效率",
        "#抖音小助手", "#热门推荐", "#爆款", "#流量",
    ],
    'wechat': [
        "#深度好文", "#原创", "#干货", "#行业观察",
        "#技术分享", "#职场", "#成长", "#思维",
        "#公众号", "#好文推荐", "#阅读", "#思考",
    ],
    'weibo': [
        "#好物推荐#", "#实用工具#", "#科技#", "#数码#",
        "#职场#", "#学习#", "#成长#", "#干货#",
        "#微博#", "#热门#", "#推荐#", "#分享#",
    ],
    'friends': [
        "#好物分享", "#日常", "#生活", "#推荐",
    ],
}

# 内容要点模板
CONTENT_POINTS = {
    'feature': [
        "{emoji} {topic} 的核心功能真的绝了",
        "{emoji} 功能超级强大，满足所有需求",
        "{emoji} 这个功能我必须单独拿出来说",
        "{emoji} 最惊喜的是这个功能",
    ],
    'easy': [
        "{emoji} 操作简单，新手也能快速上手",
        "{emoji} 零基础也能轻松学会",
        "{emoji} 界面友好，老人小孩都会用",
        "{emoji} 上手难度几乎为零",
    ],
    'efficiency': [
        "{emoji} 效率提升不止一倍",
        "{emoji} 每天节省{num}小时",
        "{emoji} 工作效率翻倍",
        "{emoji} 时间管理神器",
    ],
    'value': [
        "{emoji} 性价比超高，强烈推荐",
        "{emoji} 这个价格还要什么自行车",
        "{emoji} 物超所值，买就对了",
        "{emoji} 省钱又省心",
    ],
    'audience': [
        "{emoji} 适合人群：{role}",
        "{emoji} 强烈推荐给{role}",
        "{emoji} {role} 必备神器",
        "{emoji} 专为{role} 设计",
    ],
}

def random_emoji(category='star'):
    """随机返回一个 emoji"""
    return random.choice(EMOJIS.get(category, EMOJIS['star']))

def random_choice(items, count=None):
    """随机选择"""
    if count and count < len(items):
        return random.sample(items, count)
    return random.choice(items)

def generate_points(topic, count=5):
    """生成内容要点"""
    roles = ['打工人', '学生', '创业者', '自由职业者', '自媒体人', '设计师', '程序员']
    points = []
    
    templates = [
        random.choice(CONTENT_POINTS['feature']).format(emoji=random_emoji('check'), topic=topic),
        random.choice(CONTENT_POINTS['easy']).format(emoji=random_emoji('star'), topic=topic),
        random.choice(CONTENT_POINTS['efficiency']).format(emoji=random_emoji('fire'), topic=topic, num=random.randint(1, 3)),
        random.choice(CONTENT_POINTS['value']).format(emoji=random_emoji('heart'), topic=topic),
        random.choice(CONTENT_POINTS['audience']).format(emoji=random_emoji('think'), topic=topic, role=random.choice(roles)),
        f"{random_emoji('work')} 工作学习都能用",
        f"{random_emoji('money')} 省钱省时间",
        f"{random_emoji('time')} 每天节省{random.randint(1,3)}小时",
    ]
    
    return random.sample(templates, min(count, len(templates)))

def generate_xiaohongshu(topic, length='medium', style='casual'):
    """生成小红书文案"""
    
    # 生成标题
    title_template = random.choice(TITLE_TEMPLATES['xiaohongshu'])
    title = title_template.format(
        topic=topic,
        num=random.choice([3, 5, 7, 10])
    )
    
    # 生成开头
    opening_template = random.choice(OPENING_TEMPLATES)
    opening = opening_template.format(
        topic=topic,
        role=random.choice(['打工人', '创业者', '自由职业者', '学生党', '自媒体人']),
        money=random.choice([99, 199, 299, 999])
    )
    
    # 生成正文
    points = generate_points(topic, 5)
    content = "\n\n".join(points)
    
    # 生成结尾
    ending_template = random.choice(ENDING_TEMPLATES['xiaohongshu'])
    ending = f"\n{ending_template.format(topic=topic)} {random_emoji('heart')}"
    
    # 生成标签
    base_tags = [f"#{topic.replace(' ', '').replace('/', '')}"]
    extra_tags = random.sample(TAGS_LIBRARY['xiaohongshu'], 6)
    tags = ' '.join(base_tags + extra_tags)
    
    return {
        'platform': 'xiaohongshu',
        'title': title,
        'opening': opening,
        'content': content,
        'ending': ending,
        'tags': tags,
        'images_suggestion': f"建议配图：3-5 张{topic}使用场景图 + 效果对比图",
        'style': style,
    }

def generate_douyin(topic, length='short', style='dramatic'):
    """生成抖音文案"""
    
    hook = random.choice(TITLE_TEMPLATES['douyin']).format(topic=topic)
    
    content_templates = [
        f"今天给大家分享一下{topic}的使用技巧，看完你也会用！",
        f"{topic}到底有多好用？我用了一个月，来告诉你真实感受！",
        f"很多人都不知道{topic}的正确用法，今天一条视频教会你！",
        f"关于{topic}，今天必须说点大实话！",
        f"挑战用{topic}做到...结果惊呆了！",
    ]
    
    cta = random.choice(ENDING_TEMPLATES['douyin'])
    
    return {
        'platform': 'douyin',
        'hook': f"🎬 {hook}",
        'content': f"📹 {random.choice(content_templates)}",
        'cta': f"💬 {cta}",
        'bgm': f"🎵 BGM 建议：轻快节奏音乐",
        'shooting': f"📸 拍摄建议：开场特写 + 使用过程 + 效果展示",
        'duration': "建议时长：30-60 秒",
    }

def generate_wechat(topic, length='long', style='professional'):
    """生成公众号文章大纲"""
    
    title_template = random.choice(TITLE_TEMPLATES['wechat'])
    title = title_template.format(
        topic=topic,
        num=random.choice([3, 5, 7])
    )
    
    outline = [
        f"一、什么是{topic}？为什么值得关注",
        f"二、{topic} 的核心功能和优势",
        f"三、{topic} 的实际应用场景",
        f"四、{topic} 使用教程（图文）",
        f"五、常见问题解答",
        f"六、总结与建议",
    ]
    
    ending = random.choice(ENDING_TEMPLATES['wechat'])
    
    return {
        'platform': 'wechat',
        'title': f"📰 {title}",
        'outline': outline,
        'ending': ending,
        'word_count': "建议字数：2000-3000 字",
        'images': "建议配图：5-8 张（封面 + 各章节配图）",
    }

def generate_weibo(topic, length='short', style='casual'):
    """生成微博文案"""
    
    title = random.choice(TITLE_TEMPLATES['weibo']).format(topic=topic)
    
    content = f"最近在用{topic}，感觉还不错！有没有也在用的朋友？来聊聊使用感受～"
    
    tags = random.sample(TAGS_LIBRARY['weibo'], 4)
    
    return {
        'platform': 'weibo',
        'title': title,
        'content': content,
        'tags': ' '.join(tags),
        'image': "配图建议：1-3 张使用截图"
    }

def generate_friends(topic, length='short', style='casual'):
    """生成朋友圈文案"""
    
    templates = [
        f"最近发现个好东西：{topic}，亲测好用！有需要的朋友可以试试～",
        f"用{topic} 解决了一个大麻烦，太爽了！",
        f"被{topic} 圈粉了，必须安利给你们！",
        f"花{money} 买了{topic}，真香！",
    ]
    
    return {
        'platform': 'friends',
        'content': random.choice(templates).format(
            topic=topic,
            money=random.choice([9.9, 19.9, 99, 199])
        ),
        'image': "配图建议：1 张使用截图或效果对比图"
    }

def save_result(result, output_dir=None):
    """保存结果到文件"""
    if not output_dir:
        output_dir = f"/tmp/auto-content_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    os.makedirs(output_dir, exist_ok=True)
    
    platform = result.get('platform', 'unknown')
    filename = f"{platform}_content.md"
    filepath = os.path.join(output_dir, filename)
    
    # 格式化输出
    output = f"# {platform} 文案\n\n"
    output += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    output += f"**版本**: Auto Content Creator v{CONFIG['version']}\n\n"
    
    for key, value in result.items():
        if key != 'platform':
            if isinstance(value, list):
                output += f"## {key}\n\n"
                for item in value:
                    output += f"- {item}\n"
            else:
                output += f"## {key}\n\n{value}\n\n"
    
    output += f"\n---\n\n**Copyright © 2026 anyafu. All rights reserved.**\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(output)
    
    return filepath

def print_result(result):
    """打印结果"""
    platform = result.get('platform', 'unknown')
    
    print(f"\n{'='*60}")
    print(f"📝 {platform} 文案生成完成")
    print(f"{'='*60}\n")
    
    if platform == 'xiaohongshu':
        print(f"📌 标题：{result['title']}\n")
        print(f"{result['opening']}\n")
        print(f"{result['content']}\n")
        print(f"{result['ending']}\n")
        print(f"\n🏷️  标签：{result['tags']}")
        print(f"\n🖼️  {result['images_suggestion']}")
        
    elif platform == 'douyin':
        print(f"{result['hook']}\n")
        print(f"{result['content']}\n")
        print(f"{result['cta']}\n")
        print(f"{result['bgm']}")
        print(f"{result['shooting']}")
        print(f"{result['duration']}")
        
    elif platform == 'wechat':
        print(f"{result['title']}\n")
        print(f"📋 文章大纲：\n")
        for section in result['outline']:
            print(f"  {section}")
        print(f"\n📝 {result['ending']}")
        print(f"\n📊 {result['word_count']}")
        print(f"🖼️  {result['images']}")
        
    elif platform == 'weibo':
        print(f"{result['title']}\n")
        print(f"{result['content']}\n")
        print(f"\n🏷️  标签：{result['tags']}")
        print(f"🖼️  {result['image']}")
        
    elif platform == 'friends':
        print(f"{result['content']}\n")
        print(f"🖼️  {result['image']}")
    
    print(f"\n{'='*60}")

def main():
    if len(sys.argv) < 3:
        print(f"""
{__doc__}

平台选项:
  xiaohongshu  - 小红书
  douyin       - 抖音
  wechat       - 公众号
  weibo        - 微博
  friends      - 朋友圈
  all          - 全平台生成

示例:
  python3 content-generator.py xiaohongshu "AI 工具推荐"
  python3 content-generator.py douyin "职场效率技巧"
  python3 content-generator.py all "AI 写作工具"
  python3 content-generator.py xiaohongshu "AI 工具" --output ./my-content
""")
        sys.exit(1)
    
    platform = sys.argv[1]
    topic = sys.argv[2]
    output_dir = None
    
    # 解析参数
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    platforms = {
        'xiaohongshu': generate_xiaohongshu,
        'douyin': generate_douyin,
        'wechat': generate_wechat,
        'weibo': generate_weibo,
        'friends': generate_friends,
    }
    
    if platform == 'all':
        print(f"🚀 开始全平台内容生成：{topic}")
        print(f"📁 输出目录：{output_dir or '默认目录'}")
        
        results = []
        for p, func in platforms.items():
            print(f"\n正在生成 {p} 内容...")
            result = func(topic)
            results.append(result)
            print_result(result)
            if output_dir:
                filepath = save_result(result, output_dir)
                print(f"💾 已保存：{filepath}")
        
        print(f"\n✅ 全平台内容生成完成！共生成 {len(results)} 个平台的内容")
    else:
        if platform not in platforms:
            print(f"❌ 不支持的平台：{platform}")
            print(f"可用平台：{', '.join(platforms.keys())}")
            sys.exit(1)
        
        print(f"🚀 正在生成 {platform} 内容：{topic}")
        result = platforms[platform](topic)
        print_result(result)
        
        if output_dir:
            filepath = save_result(result, output_dir)
            print(f"\n💾 已保存到：{filepath}")

if __name__ == '__main__':
    main()
