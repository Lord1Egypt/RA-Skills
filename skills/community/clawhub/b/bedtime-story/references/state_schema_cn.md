# 数据结构参考

## StoryWorld

```json
{
  "world_name": "星光恐龙谷",
  "world_description": "在银河系的尽头，有一片被星光照耀的山谷...",
  "characters": [
    {
      "role": "narrator",
      "name": "旁白",
      "personality": "温柔沉稳的讲述者",
      "catchphrase": "在那遥远的地方..."
    },
    {
      "role": "protagonist",
      "name": "小明",
      "personality": "勇敢好奇的小探险家",
      "catchphrase": "我们去看看吧！"
    },
    {
      "role": "sidekick",
      "name": "小星星",
      "personality": "活泼开朗的小伙伴",
      "catchphrase": "太有趣了！"
    },
    {
      "role": "elder",
      "name": "月光爷爷",
      "personality": "智慧慈祥的长者",
      "catchphrase": "孩子，让我告诉你一个秘密..."
    }
  ]
}
```

## StorySegment

```json
{
  "speaker": "narrator",
  "text": "夜幕降临，星光恐龙谷里的萤火虫开始跳起了舞。"
}
```

## StoryEpisode

```json
{
  "title": "星光恐龙谷的秘密",
  "segments": [],
  "summary": "小明和小星星在星光恐龙谷发现了一颗会发光的恐龙蛋...",
  "cliffhanger": "恐龙蛋裂开了一条缝，里面传来了奇怪的声音..."
}
```

## StoryState（story_state.json）

```json
{
  "child_name": "小明",
  "age": 5,
  "interests": "恐龙,太空",
  "world": {},
  "episodes": [
    {
      "episode": 1,
      "title": "星光恐龙谷的秘密",
      "summary": "...",
      "cliffhanger": "..."
    }
  ],
  "current_episode": 1
}
```

## 音色配置

```json
{
  "narrator": {
    "voice_id": "male_0004_a",
    "speed": 0.9,
    "pitch": 0
  },
  "protagonist": {
    "voice_id": "child_0001_a",
    "speed": 1.0,
    "pitch": 0
  },
  "sidekick": {
    "voice_id": "child_0001_b",
    "speed": 1.0,
    "pitch": 0
  },
  "elder": {
    "voice_id": "male_0018_a",
    "speed": 0.85,
    "pitch": -2
  }
}
```
