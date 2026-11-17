# v1.5.0 回退检查清单

## 回退条件
出现以下任一情况应当回退：
- [ ] 修复后文本质量明显下降（更多错字/不通顺）
- [ ] confidence_score 虚高（LLM给高分但实际质量差）
- [ ] LLM频繁触发降级（提示词太复杂导致LLM困惑）
- [ ] 特定UP主的专业性急剧下降

## 回退步骤

### 开发版回退
```bash
cd ~/openclaw/workspace
git checkout -- biliyoutik2brain/core/pipeline.py  # 恢复到上次checkpoint
```

### 发布版回退
```bash
cp ~/.openclaw/skills/biliyoutik2brain/scripts/biliyoutik2brain/core/pipeline.py.v1.4.0_backup \
   ~/.openclaw/skills/biliyoutik2brain/scripts/biliyoutik2brain/core/pipeline.py
```

### 回退后验证
- [ ] 跑一个之前跑过的视频，结果与v1.4.0一致
- [ ] 确认没有遗留代码（例如在prompt里还引用旧函数）
