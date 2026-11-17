# 抖音科技内容策划

把技术、AI 工具或软件主题及其来源材料，整理成受众明确、收益单一、证据顺序清楚的短视频或图文策划。技能指引 AI 阅读用户提供的实际材料；附带校验器仅检查结构和事实 ID 引用，不替代来源核验或内容判断。

## 输入结构

事实文件：

```json
{
  "facts": [
    {"id": "F1", "claim": "用户材料中可复核的事实", "source": "来源 URL 或文档名", "status": "verified"}
  ]
}
```

策划输出：

```json
{
  "audience": "主要受众",
  "keyword": "一个核心关键词",
  "promise": "一个具体观看收益",
  "hook": "开场钩子",
  "opening_evidence": {"seconds": 0, "fact_ids": ["F1"], "beat": "开场呈现什么结果或证据"},
  "beats": [{"order": 1, "text": "口播、画面或分页要点", "fact_ids": ["F1"]}],
  "title_direction": "标题方向",
  "share_motivation": "受众为什么可能分享；不适用则说明",
  "cta": null,
  "unknowns": []
}
```

`fact_ids` 必须对应输入事实中的已核验 ID。未核验、冲突或缺少来源的材料写进 `unknowns`，不得用在事实性钩子或结论中。

## 校验和自测

```bash
python3 scripts/validate_plan.py examples/facts.json examples/plan.json
python3 scripts/self_test.py
```

示例中的产品、数据与来源全部是虚构占位，仅演示结构。校验器不能判断引用来源是否可信、事实是否被准确概括，也不能证明选题会获得播放或分享。

## 内容

- [Skill 指令](SKILL.md)
- [MIT No Attribution 许可](LICENSE)
- [来源记录](SOURCE-ORIGIN.md)
