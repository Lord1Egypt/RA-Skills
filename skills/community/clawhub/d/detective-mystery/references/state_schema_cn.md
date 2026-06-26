# 数据结构参考

## CaseData

```json
{
  "case_name": "消失的翡翠项链",
  "background": "在一个雨夜，著名收藏家王老先生家中的传家翡翠项链不翼而飞...",
  "crime": "翡翠项链于昨晚10点到今早6点之间被盗...",
  "suspects": [
    {
      "id": "suspect_a",
      "name": "张明",
      "occupation": "管家",
      "motive": "最近赌博欠下巨额债务",
      "alibi": "声称整晚都在自己房间休息",
      "personality": "沉着冷静，说话有条理",
      "is_culprit": false,
      "secret": "其实当晚偷偷出去还了一笔赌债"
    }
  ],
  "evidence": [
    {
      "id": "E1",
      "description": "书房窗户上的新鲜划痕",
      "location": "书房",
      "related_suspect": "suspect_b",
      "importance": "high"
    }
  ],
  "locations": [
    {
      "name": "书房",
      "description": "翡翠项链存放的房间，有一扇朝花园的窗户",
      "clues": ["E1", "E2"]
    }
  ],
  "solution": "根据证据分析，真凶是..."
}
```

## GameState

```json
{
  "case": {},
  "difficulty": "medium",
  "max_turns": 30,
  "current_turn": 5,
  "collected_evidence": ["E1", "E3"],
  "examined_locations": ["书房"],
  "interrogation_logs": {
    "suspect_a": {
      "rounds": 2,
      "history": [],
      "compressed_summary": null
    }
  },
  "actions_log": [
    {"turn": 1, "action": "examine", "target": "书房"},
    {"turn": 2, "action": "interrogate", "target": "suspect_a"}
  ]
}
```

## InterrogationEntry

```json
{
  "round": 1,
  "question": "你昨晚在哪里？",
  "response": "我整晚都在自己房间休息。",
  "emotion": "calm",
  "revealed_info": ""
}
```

## AccusationResult

```json
{
  "correct": true,
  "scores": {
    "logic": 25,
    "evidence": 28,
    "completeness": 18,
    "efficiency": 15,
    "total": 86
  },
  "feedback": "推理过程清晰，证据引用充分...",
  "truth_reveal": "事实的真相是..."
}
```

## 音色配置

```json
{
  "narrator": {
    "voice_id": "child_0001_a",
    "speed": 0.85,
    "pitch": -1
  },
  "suspect_a": {
    "voice_id": "male_0004_a",
    "speed": 1.0,
    "pitch": 0
  },
  "suspect_b": {
    "voice_id": "male_0018_a",
    "speed": 1.1,
    "pitch": 0
  },
  "suspect_c": {
    "voice_id": "child_0001_b",
    "speed": 1.0,
    "pitch": 2
  }
}
```
