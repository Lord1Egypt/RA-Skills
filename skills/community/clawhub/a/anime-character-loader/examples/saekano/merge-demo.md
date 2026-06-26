# MERGE 模式演示

## 执行过程

### Step 1: 生成第一个角色
```bash
$ python load_character.py "加藤惠" --anime "Saekano"

🔍 Searching for: 加藤惠 (Anime: Saekano)
✅ Selected: Katou Megumi (ID: 118763)
✅ Validation: PASSED (85/100)

⚠️  Output file SOUL.generated.md already exists.
    [1] REPLACE - Overwrite existing
    [2] MERGE   - Merge with existing  ← 选择此项
    [3] KEEP    - Keep existing, create backup

选择: 2

📝 Generated: SOUL.generated.md
📊 Mode: MERGE (single character, baseline created)
```

### Step 2: 追加第二个角色
```bash
$ python load_character.py "霞之丘诗羽" --anime "Saekano"

🔍 Searching for: 霞之丘诗羽 (Anime: Saekano)
✅ Selected: Kasumigaoka Utaha (ID: 118761)
✅ Validation: PASSED (92/100)

⚠️  Output file SOUL.generated.md already exists.
    [1] REPLACE - Overwrite existing
    [2] MERGE   - Merge with existing  ← 选择此项
    [3] KEEP    - Keep existing, create backup

选择: 2

📝 Updated: SOUL.generated.md
📊 Mode: MERGE (merged with existing character)
✅ Added Character Selection Guide
```

## 输出结构对比

### 单角色 (Step 1 后)
```markdown
# Character SOUL: Katou Megumi

**Source:** Saenai Heroine no Sodatekata

## Identity
[角色A设定...]

## Personality
[角色A性格...]

## Speaking Style
[角色A说话方式...]

## Boundaries
[角色A限制...]
```

### 多角色 (Step 2 后)
```markdown
# Multi-Character SOUL: Saekano Edition

## Katou Megumi
[角色A完整设定...]

## Kasumigaoka Utaha
[角色B完整设定...]

## Character Selection Guide

### When to choose Megumi:
- 需要被动观察型角色
- 场景需要平淡但真实的反应
- 适合日常/校园剧情

### When to choose Utaha:
- 需要主动攻击型角色
- 场景需要毒舌/吐槽
- 适合冲突/喜剧剧情

### Combination Strategies:
- 双角色互动：Megumi 吐槽 Utaha 的傲娇
- 对照使用：同一事件的不同反应
```

## 关键优势

1. **避免覆盖**: MERGE 不会丢失已有角色数据
2. **智能指南**: 自动生成角色选择建议
3. **对比维度**: 明确标注角色差异（被动 vs 主动等）
4. **扩展性**: 可继续 MERGE 第三个、第四个角色...

## 查看完整输出

见同目录: `SOUL.generated.md`
