# v1.5.0 升级详细说明

## 1. _smart_correct() 简化

### 改动前
```python
def _smart_correct(text: str) -> str:
    # 保护"主力+动作动词"类（保护大机构语境）
    protected = []
    patterns = [
        "主力吸", "主力买", "主力出", "主力拉",
        "主力砸", "主力抢", "大主力", "主力资",
        ...共18个模式...
    ]
    for i, p in enumerate(patterns):
        if p in text:
            ph = f"__P{i}__"
            text = text.replace(p, ph)
            protected.append((ph, p))
    
    # 应用全局纠错（含"主力→阻力"无脑替换）
    from transcription_enhancer import apply_all_corrections
    corrected = apply_all_corrections(text)
    
    # 恢复保护的语境
    for ph, orig in protected:
        corrected = corrected.replace(ph, orig)
    
    # 额外常见误认
    corrected = corrected.replace("一贴", "一单")
    return corrected
```

问题: 18个被保护模式也无法穷举，"主力准备吸筹、主力正在吸筹、主力刚吸完"都会漏掉。

### 改动后
```python
def _smart_correct(text: str) -> str:
    """确定性纠错：100%不会错的替换，无需语境判断"""
    text = text.replace("一贴", "一单")
    return text
```

原则: 只有0歧义的替换留在代码里。任何需要"结合上下文判断"的纠错，移入提示词，由LLM根据语境做决策。

## 2. COMBINED_SYSTEM_PROMPT 扩充

### 改动前
有一组简单列表，以纯文字叙述形式写在"常识检查"下。

### 改动后
结构化归类，每条附带"触发条件":
```
### 🔧 交易领域常见纠错（按类别）
同音字群:
  拼罢/拼盼→Pinbar, 运线/晕线→孕线/均线
  脏色→止损, 阴力→盈利, 扛单→扛单
  
语境敏感纠错（结合上下文判断）:
  主力结构/位/区→阻力结构/位/区（技术术语语境）
  主力吸筹/买入/出货→保留"主力"（大资金方语境）
  尺寸→止损（交易语境）
  排单→卖单（阻力区语境）
  
说话人专属纠错:
  图行之死扛→图形止损法（张聚贤视频中常见）
  十之间之神→时间止损法
  深证→恒生（张聚贤说恒生指数）
```

## 3. JSON输出新增 confidence_score

### 改动前
```json
{
  "corrected": "...",
  "summary": "...",
  "keywords": [],
  "chapters": [],
  "topics": []
}
```

### 改动后
```json
{
  "corrected": "...",
  "summary": "...",
  "keywords": [],
  "chapters": [],
  "topics": [],
  "confidence_score": 0.92
}
```

confidence_score 取值范围 0~1:
- 0.8~1.0: LLM确信修复正确 → 直接保存
- 0.5~0.8: LLM有部分不确定 → 保存但标记"待人工复查"
- <0.5: LLM整体不确定 → 触发降级流程

## 4. 降级决策逻辑

### 改动前
降级触发条件单一：两次合并调用都返回JSON解析失败。

### 改动后
```python
confidence = parsed.get("confidence_score", 0.5)
if confidence < 0.5:
    # LLM都不确定，走降级
    走两阶段调用降级
elif confidence < 0.8:
    # LLM部分不确定，保存结果但加标记
    保存结果，加"待复查"标记
else:
    # 正常保存
    直接保存
```

## 影响范围
- pipeline.py 是唯一修改的文件
- 不涉及 schemas.py（confidence_score 是LLM输出字段，不是数据模型字段）
- 不涉及 speaker_knowledge.py（知识库逻辑不变）
- 不涉及 BG吴江技能（任何BG技能文件不改动）
