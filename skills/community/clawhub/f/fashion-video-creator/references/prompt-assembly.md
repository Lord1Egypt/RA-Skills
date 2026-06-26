# Seedance Prompt Assembly Rules

> **Role:** Defines the composition ORDER and FORMAT for assembling Seedance 2.0 prompts from dialogue/action/scene components.
> Dialogue content (scripts, openings, closings, actions): see [dialogue-library.md](dialogue-library.md).
> Load at: Step 4-6 (assembling prompt and SOP).

## Prompt Assembly Order

```
一位{model_ref}年轻{gender_word}穿着 @图片1 中的服装，{scene_desc}。
{style_transfer (if stylized ref)}
{pronoun}{action}，
对着镜头说：「{opening}{dialogue_core}{selling_closing}」
{dialogue_style_instruction}
Do not alter clothing pattern, color, texture or style.
{camera}。
音频要求：全程只有模特一个人的清晰人声，不出现第二个人的声音或对白。
背景有符合场景的自然环境音（如户外有车声鸟鸣、室内有空调低鸣），音量不超过人声的10%。
视觉要求：全程保持中景到中近景，不要切到手部或脚部的特写镜头，避免手指变形问题。
模特展示服装细节时始终使用右手操作，避免左右手切换导致的镜像翻转。
全程画面中只有模特一人，不出现其他人物。
```

## Variable Resolution

| Variable | Source | Example |
|----------|--------|---------|
| `{model_ref}` | If has_model_ref: "面容和身材参考@图片2的"; if stylized: "身材比例和姿态参考@图片2（忽略动画风格）的" | 面容和身材参考@图片2的 |
| `{gender_word}` | "女性" or "男性" | 女性 |
| `{scene_desc}` | SCENE_PRESETS[key] or custom text | 在简约现代的白色公寓客厅中，自然光从落地窗照入 |
| `{pronoun}` | "她" or "他" | 她 |
| `{action}` | From dialogue-library.md: ACTION_DEMEANOR + GARMENT_ACTIONS | 面朝镜头表情生动自然地展示服装，右手拉起裙摆展示面料... |
| `{opening}` | From dialogue-library.md: OPENINGS[(gender, audience)][lang] | 姐妹们你们快看... |
| `{dialogue_core}` | From dialogue-library.md: DIALOGUE_CORE[garment][gender][lang] | 哇，不是，我真的没想到... |
| `{selling_closing}` | From dialogue-library.md: SELLING_CLOSINGS[(audience, garment)][lang] | 超显腿长，闭眼入。 |
| `{dialogue_style_instruction}` | From dialogue-library.md: STYLE_INSTRUCTIONS[style][gender] | 语气自然亲切... |
| `{camera}` | CAMERA_PROMPTS[style] | 手持vlog镜头感，竖屏9:16构图 |

## Custom Dialogue Handling

When user provides custom dialogue (overrides DIALOGUE_CORE):
1. Still wrap with OPENING + custom text + SELLING_CLOSING
2. Append fusion instruction: "（以上为核心台词要点，请以自然口语化的方式说出，加入适当停顿、语气词和过渡，不要原封不动念稿。）"
3. Actions switch to adaptive mode (sync with content, not pre-choreographed)

## Multi-Segment Chaining (duration > 15s)

### Constants
- CHARS_PER_SECOND = 4 (Chinese speaking rate)
- TARGET_SEGMENT_CHARS = 55 (~13.5s)
- MIN_SEGMENT_CHARS = 30 (~7.5s)
- MAX_SEGMENT_CHARS = 65 (~16s)

### Split Algorithm
1. If total spoken chars <= 65: single segment
2. Split at sentence boundaries (。！？…)
3. Accumulate until > 65 chars, then flush
4. If last segment < 30 chars: merge with previous

### Segment Structure
- **Segment 0** (is_base=true): full prompt with scene + @image refs + dialogue part 1
- **Segments 1+** (is_base=false): extend prompt only:

```
继续上一段的内容，保持相同的人物、服装、场景和说话风格。
模特接着说：「{segment_dialogue}」
{dialogue_style_instruction}
动作与台词内容同步配合，始终使用右手操作。
保持中景到中近景，不切手部特写。
全程只有模特一个人的声音，环境音延续上一段。
```

### Duration Calculation
```
scale = total_duration / sum(segment.estimated_seconds)
per_segment = max(5, min(15, round(estimated_seconds * scale)))
```

## SOP Template (Single Segment)

```markdown
# Seedance 视频生成操作指南
## 素材文件
- 衣服商品图（图片1）：{garment_path}
- 模特参考图（图片2）：{model_path}
## 操作步骤
1. 打开即梦 https://jimeng.jianying.com
2. 点击「视频生成 Seedance 2.0」
3. 点击 + 按钮，依次上传 2 张图片（顺序重要：图片1=衣服, 图片2=模特）
4. 粘贴 prompt
5. 确认「输出声音」已开启
6. 设置：模式=参考生成, 分辨率={resolution}, 时长={duration}秒, 数量=4条
7. 生成 -> 从4条中挑选最佳 -> 下载
## 质量检查
- [ ] 衣服颜色/面料/版型与商品图一致
- [ ] 对白清晰可听、语调自然
- [ ] 嘴型与语音基本同步
- [ ] 动作自然有真人感
- [ ] 面部稳定表情生动
```

## SOP Template (Multi-Segment Chain)

```markdown
# Seedance 分段接龙操作指南
## 总览：共 {n} 段，总时长约 {total}秒
## 第 1 段：初始生成
1-5. 同单段 SOP
6. 不要下载！留在平台准备延长
## 第 2+ 段：延长生成
1. 点击上一段结果的「延长」按钮
2. 粘贴延长 prompt
3. 设置时长 -> 生成 -> 挑选
4. 最后一段下载完整视频
## 质量检查
- [ ] 衣服全程一致
- [ ] 面部全程一致（无漂移）
- [ ] 段间对白自然衔接
- [ ] 总时长接近预期
```
