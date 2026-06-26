# Step 4: 去AI味

## 操作流程

```bash
# 1. 检测AI味
python3 ${SKILL_DIR}/scripts/detect_cn.py article.md

# 2. 科技博客风格优化
python3 ${SKILL_DIR}/scripts/humanize_cn.py article.md --scene tech -o article_clean.md

# 3. 公众号风格深度优化
python3 ${SKILL_DIR}/scripts/style_cn.py article_clean.md --style wechat -o article_final.md

# 4. 再次检测，确认 LOW
python3 ${SKILL_DIR}/scripts/detect_cn.py article_final.md -s
```

## AI概率标准

- LOW ✅ 合格
- MEDIUM ⚠️ 需要优化
- HIGH/VERY\_HIGH ❌ 必须重写

## 去AI味重点

### 结构清理
- 去掉"首先...其次...最后"、"一方面...另一方面"等三段式机械结构
- 去掉"其一...其二...其三"等列举式结构

### 词汇优化
- 去掉"赋能"、"闭环"、"数字化转型"、"协同增效"等空洞大词
- 去掉"助力"、"彰显"、"底层逻辑"、"抓手"、"触达"等AI高频词
- 去掉"值得注意的是"、"综上所述"、"不难发现"、"归根结底"等机械连接词
- 去掉"值得一提的是"、"众所周知"、"毫无疑问"等套话

### 句式调整
- 合并过短的连续句子，使表达更流畅
- 拆分过长的句子，在自然断点处分割（如"但是"、"不过"、"同时"等）
- 减少过度使用的标点符号（如分号、破折号）
- 多样化词汇，减少重复词（如"进行"、"实现"、"提供"等）

### 节奏优化
- 调整段落长度，避免过于均匀的段落结构
- 增加句子长度变化，避免单调的表达节奏
- 增加情感表达和个人观点，避免情感平淡
- 减少重复的句首开头，增加表达多样性

### 风格转换
- 应用公众号风格，增加故事性和吸引力
- 可使用激进模式（-a）获得更自然的效果
- 保持适度的口语化表达，增强可读性

### 验证标准
- AI评分低于25分（LOW级别）才合格
- 评分25-49分（MEDIUM级别）需要进一步优化
- 评分50分以上（HIGH/VERY HIGH级别）必须重写

