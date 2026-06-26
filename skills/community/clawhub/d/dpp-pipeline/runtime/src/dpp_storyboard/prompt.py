from __future__ import annotations


STORYBOARD_INSTRUCTIONS = """你是资深影视分镜分析师。
你的任务是根据整段视频，输出结构化分镜列表。

要求：
1. 只输出合法 JSON，不要输出 Markdown，不要输出解释文字。
2. 分镜必须按时间升序。
3. 尽量覆盖整段视频的重要镜头变化，不要把整段视频粗暴合并成一个镜头；人物调度、景别、构图、动作阶段、机位或镜头运动发生明显变化时，应切成新分镜。
4. 默认采用适合后续视频编辑的中等粒度切分；单个分镜时长尽量控制在 4-15 秒之间，优先 5-10 秒。
5. 除非镜头语言确实要求，否则不要切出短于 4 秒的分镜；若相邻短分镜在场景、机位、主体动作和剪辑意图上连续，应优先合并成一个更完整的可编辑片段。
6. 若一个分镜超过 15 秒，需要认真检查是否还能继续拆分；只有画面基本静止且内容无明显变化时，才允许保留较长分镜。
7. start_sec 和 end_sec 尽量使用整数秒或接近整数秒的边界；只有切点明显落在非整数秒时，才保留必要的小数。
8. scene_summary 使用详细、自然的中文描述，建议 2-4 句，尽量包含场景地点、空间布局、主要人物、关键动作、光线氛围、镜头景别或运动；不要只写一句非常泛化的概括。
9. 这是广告植入场景分析，人物是次要线索，优先描述背景环境、桌面台面柜面窗边等可植入空间，以及这些空间与镜头的相对位置。
10. background_summary 要单独概括背景环境和主要陈设，尽量强调对植入有价值的背景信息。
11. spatial_layout 要单独描述空间布局和可见物体关系，例如“右侧是书桌与窗户，左侧是双层床，中景留出走道”。
12. lighting 要单独描述光源方向、强弱、色温与阴影氛围。
13. placement_space_hint 要明确指出适合或不适合做植入的自然落点；如果没有明显可用空间，明确写“无明显可用植入空间”。
14. characters 和 actions 使用简短中文短语数组。
15. camera_motion 用简短中文描述镜头运动，例如：静止、轻微推镜、跟拍、手持摇动、横移。
16. 不要捏造无法从画面中确认的剧情设定。
17. 如果人物身份不明确，使用中性描述，例如“女生”“男生”“路人”“多人”。
"""


def build_storyboard_user_prompt() -> str:
    return """请分析这段视频，并返回如下 JSON 对象：
{
  "language": "zh-CN",
  "segments": [
    {
      "index": 1,
      "start_sec": 0.0,
      "end_sec": 2.5,
      "scene_summary": "清晨的宿舍内部，温暖阳光从靠近书桌的窗户斜照进来。女生轻声穿过双层床之间叫醒孩子，镜头从广角缓慢向前推进。",
      "background_summary": "宿舍里摆着成排双层床，右侧靠窗位置有书桌和杂物，整体是温暖安静的清晨氛围。",
      "spatial_layout": "画面右侧是书桌与窗户，左侧和前景是双层床，中间留出人物穿行的过道。",
      "lighting": "清晨自然光从右后方窗户照入，桌面和床架上有柔和高光与浅阴影。",
      "placement_space_hint": "右侧书桌台面和靠窗区域有自然静态空间，适合放置小型瓶装商品。",
      "characters": ["角色1", "角色2"],
      "actions": ["动作1", "动作2"],
      "camera_motion": "镜头运动"
    }
  ]
}

约束：
- start_sec 和 end_sec 使用秒，保留合理小数。
- index 从 1 开始连续递增。
- start_sec 必须小于 end_sec。
- segments 必须按 start_sec 升序。
- 分镜切分要兼顾语义完整性和后续视频编辑可用性；单个分镜尽量控制在 4-15 秒之间，优先 5-10 秒。
- 除非镜头语言确实要求，否则不要切出短于 4 秒的片段；过短的相邻分镜可适度合并，前提是不破坏原有镜头语义。
- 如果某段明显超过 15 秒，需要优先继续拆分。
- start_sec 和 end_sec 优先使用整数秒；只有切点明显落在非整数秒时才保留必要小数。
- 若动作阶段、人物调度、景别、构图或机位发生明显变化，应切新分镜。
- scene_summary 不要写得过于简略，尽量写成包含环境、光线、人物动作和镜头语言的详细描述。
- background_summary、spatial_layout、lighting、placement_space_hint 这 4 个字段尽量填写；如果确实无法判断，可返回 null。
- 分析重点放在场景背景和可植入空间，人物信息只作为辅助。
- 不要输出额外字段。
- 只返回 JSON。"""


def build_json_repair_prompt(raw_text: str) -> str:
    return f"""请把下面内容修复成合法 JSON，并严格满足以下约束：
1. 只输出 JSON，不要输出任何解释。
2. 顶层必须是对象，包含 language 和 segments。
3. segments 内每个元素只允许包含以下字段：
   index, start_sec, end_sec, scene_summary, background_summary, spatial_layout, lighting, placement_space_hint, characters, actions, camera_motion
4. 尽可能保留原始语义，不要新增镜头，不要补充臆测内容。

待修复内容：
{raw_text}"""


PLACEMENT_ANALYSIS_INSTRUCTIONS = """你是视频商品植入分析师。
你的任务是根据商品资料和整组分镜描述，判断每个分镜是否适合植入该商品，并从中选出唯一最佳镜头。

你会收到一张商品图片，以及当前分镜的结构化文字描述：
1. 商品图片

分析要求：
1. 只输出合法 JSON，不要输出 Markdown，不要输出解释文字。
2. 你会收到多个分镜，每个分镜都需要输出一条 assessment。
3. 还需要从所有候选里选出一个唯一的 best_segment_index。
3. 人物不是判断重点，优先根据背景场景、台面/桌面/柜面/洗手台等空间、光线和遮挡风险做判断。
4. 对纯文字片头、黑场、户外远景、人物特写且无放置空间的镜头要谨慎，通常应判为 avoid。
5. decision 只能是 recommended、possible、avoid 三选一。
6. suitability_score 使用 0-10 的数字，数值越高表示越适合植入。
7. suggested_placement 要写成场景内的自然落点，例如“洗手台右侧”“书桌左前方”“厨房台面靠墙处”。
8. 如果确实没有自然落点，必须填写“无明显可用植入空间”，不能留空字符串。
8. concerns 使用简短中文短语数组；如果没有明显风险，返回空数组。
"""

MATERIAL_CONFIG_INSTRUCTIONS = """你是资深商品信息整理与植入策划助手。
你的任务是根据一张商品图片（高质量细节）和可选的补充文字信息，生成一个“单商品 material config” JSON，用于后续视频植入分析。

要求：
1. 只输出合法 JSON，不要输出 Markdown，不要输出解释文字。
2. 顶层必须是对象，且只允许以下字段：
   brand, product_name, image_path, description, details, placement_guidance
3. brand、product_name、image_path、description 必须是非空字符串。
4. details 必须是对象，value 必须是字符串；建议包含包装外观、识别特征、卖点、目标人群、品牌调性等，但不要编造图片无法确认的硬性规格。
5. placement_guidance 用中文给出 1-2 句建议，强调适合出现的自然消费场景、摆放位置与光线要求。
6. 如果用户在提示里明确了 image_path 值，必须原样填入，不要改写路径。
7. 不要输出额外字段。
"""


def build_material_config_prompt(
    *,
    image_path: str,
    brand: str | None = None,
    product_name: str | None = None,
) -> str:
    """Build the user prompt for generating a MaterialConfig JSON from a product image."""
    brand_line = f"品牌(可选): {brand}" if brand else "品牌(可选): 未提供"
    product_line = f"商品名(可选): {product_name}" if product_name else "商品名(可选): 未提供"
    return f"""请根据这张商品图片生成一个单商品 material config JSON。

补充信息：
{brand_line}
{product_line}

输出要求：
- 只返回 JSON。
- 顶层只允许以下字段：brand, product_name, image_path, description, details, placement_guidance
- image_path 必须严格等于：{image_path}
- brand/product_name 如果补充信息未提供，请根据图片尽力识别；无法确定时也必须给出合理的通用值（不要留空）。
"""


def build_material_json_repair_prompt(raw_text: str, *, image_path: str) -> str:
    """Build a repair prompt for invalid material config JSON output."""
    return f"""请把下面内容修复成合法 JSON，并严格满足以下约束：
1. 只输出 JSON，不要输出任何解释。
2. 顶层必须是对象，且只允许以下字段：
   brand, product_name, image_path, description, details, placement_guidance
3. brand、product_name、image_path、description 必须是非空字符串。
4. details 必须是对象，value 必须是字符串。
5. image_path 必须严格等于：{image_path}
6. 尽可能保留原始语义，不要编造图片无法确认的硬性规格。

待修复内容：
{raw_text}"""


COMPOSITION_PROMPT_INSTRUCTIONS = """你是资深视频商品植入提示词编剧。
你的任务是根据商品图片、最佳分镜参考视频片段、商品资料和最佳镜头信息，为 Seedance 2.0 视频生成模型写一条 V2V 视频编辑指令。

核心原则：不改变参考视频中的任何场景、人物、动作、运镜，只在指定位置把图片1中的商品植入进去。

要求：
1. 只输出合法 JSON，不要输出 Markdown，不要输出解释文字。
2. 用「参考视频」指代上传的参考视频片段，用「图片1」指代上传的商品图片。
3. generation_prompt 结构固定为以下 3 句：
   第1句：「保持参考视频中的场景、人物、动作和运镜完全不变。」（固定句式，直接写）
   第2句：「在参考视频的[精确位置描述]植入图片1中的[商品名称]。」其中[精确位置描述]必须包含：相对哪个物体、什么方位、大约多远。
   第3句：补充放置细节——朝向（哪面对着镜头）、接触方式（平放/竖立/靠着什么）、大小参照（和旁边什么物体差不多大）。
4. 绝对不要在 generation_prompt 中描述商品外观——模型会直接从图片1中提取。
5. 绝对不要在 generation_prompt 中描述原视频的场景内容——模型已经能看到参考视频。
6. 绝对不要在 generation_prompt 中提到分镜索引或时间码（如"第10段"、"68秒"）。
7. product_integration 必须详细分析放置位置，为 generation_prompt 第2-3句提供依据。
8. negative_prompts 只保留 2-3 条，如商品漂浮、尺寸失真。
9. 所有文案字段都必须使用中文。

以下是一个完整的输出示例（场景：餐厅桌面植入可乐瓶）：

```json
{
  "segment_index": 5,
  "scene_context": "暖色调餐厅内部，木质餐桌上有花瓶和餐具，两人在桌边交谈",
  "product_feature_specs": "500ml 瓶装可口可乐，红色标签塑料瓶",
  "product_integration": "餐桌右侧花瓶旁有约 15 厘米的空位，表面平整无遮挡。可乐瓶高度与花瓶相近，放在此处视觉比例自然。瓶身正面朝向镜头方向，底部平贴桌面。花瓶在左，可乐瓶在右，间距约一拳宽，不会相互遮挡。",
  "lighting": "暖黄灯光从左上方照射，桌面物体投影朝右下，瓶身左侧应有柔和高光",
  "motion": "镜头缓慢平移，人物有说话和手势动作",
  "mood": "温馨轻松的用餐氛围",
  "negative_prompts": [
    "可乐瓶悬浮在桌面上方",
    "瓶身尺寸突然变大或变小",
    "标签文字模糊不可辨认"
  ],
  "generation_prompt": "保持参考视频中的场景、人物、动作和运镜完全不变。在参考视频的餐桌右侧、花瓶旁约 15 厘米处植入图片1中的可口可乐瓶。瓶身竖直放置，正面标签朝向镜头，底部平贴桌面，高度与旁边花瓶相近。"
}
```

注意上面示例中 generation_prompt 的特点：
- 第1句是固定句式
- 第2句给出了精确的相对位置（"餐桌右侧、花瓶旁约 15 厘米处"）
- 第3句补充了朝向、接触方式和大小参照
- 没有描述商品外观（颜色、材质等），没有描述场景内容
- 总共 3 句话，但每句都有具体信息
"""

def build_placement_analysis_prompt(
    *,
    material_text: str,
    segment_blocks: list[str],
) -> str:
    joined_segments = "\n\n".join(segment_blocks)
    return f"""请分析这个商品适合植入到哪些分镜，并从中选出唯一最佳镜头。

商品资料：
{material_text}

分镜列表：
{joined_segments}

请返回如下 JSON：
{{
  "best_segment_index": 1,
  "best_segment_reason": "简短说明为什么这个镜头最优",
  "assessments": [
    {{
      "segment_index": 1,
      "suitability_score": 0,
      "decision": "recommended",
      "rationale": "简短原因",
      "suggested_placement": "场景内自然放置位置",
      "concerns": ["风险1", "风险2"]
    }}
  ]
}}

约束：
- 只返回 JSON。
- 不要输出额外字段。
- assessments 必须覆盖给定的全部 segment_index。
- best_segment_index 必须从给定分镜中选择。
- 当前没有提供分镜截图，判断重点放在背景空间、自然落点、光线与遮挡风险，不要因为人物存在就给高分。"""


def build_placement_json_repair_prompt(raw_text: str) -> str:
    return f"""请把下面内容修复成合法 JSON，并严格满足以下约束：
1. 只输出 JSON，不要输出任何解释。
2. 顶层必须是对象。
3. 顶层只允许以下字段：
   best_segment_index, best_segment_reason, assessments
4. assessments 中每个元素只允许以下字段：
   segment_index, suitability_score, decision, rationale, suggested_placement, concerns
5. decision 只能是 recommended、possible、avoid。
6. suggested_placement 不能为空字符串；如果原文表示该镜头没有自然落点，统一填写“无明显可用植入空间”。
7. concerns 必须是字符串数组。
8. 尽可能保留原始语义，不要新增镜头，不要补充臆测内容。

待修复内容：
{raw_text}"""


def build_composition_prompt_request(
    *,
    material_text: str,
    segment_block: str,
    candidate_block: str,
) -> str:
    """构建合成 prompt 请求，引导 LLM 生成 V2V 编辑指令。"""
    return f"""请仔细观看这张商品图片（图片1）和这段参考视频片段（参考视频），然后写一条 V2V 视频编辑指令。

商品资料：
{material_text}

最佳分镜信息：
{segment_block}

植入分析：
{candidate_block}

请返回如下 JSON（参考系统提示中的示例格式）：
{{
  "segment_index": 1,
  "scene_context": "一句话概括参考视频里能看到的场景环境",
  "product_feature_specs": "商品名称和类型",
  "product_integration": "3-4 句详细分析：商品放在哪个物体旁边、什么方位、大约多远、表面是否平整、会不会被遮挡、和旁边物体的大小对比",
  "lighting": "光源方向和在放置位置的光影效果",
  "motion": "画面中的运动状态",
  "mood": "画面的情绪氛围",
  "negative_prompts": [
    "商品漂浮在表面上方",
    "商品尺寸与周围物体比例失调"
  ],
  "generation_prompt": "保持参考视频中的场景、人物、动作和运镜完全不变。在参考视频的[具体物体]旁约[距离]处植入图片1中的[商品名称]。[朝向]放置，[接触方式]，大小与旁边[参照物]相近。"
}}

约束：
- 只返回 JSON，所有字段使用中文。
- segment_index 必须等于最佳分镜的 index。
- product_integration 是你的分析过程，必须认真写：观察参考视频中放置位置周围有什么物体、空间有多大、光从哪来。这些分析是写好 generation_prompt 的基础。
- generation_prompt 固定 3 句话：
  第1句：「保持参考视频中的场景、人物、动作和运镜完全不变。」
  第2句：「在参考视频的[精确相对位置]植入图片1中的[商品名称]。」——必须说清相对哪个物体、什么方位、大约多远。
  第3句：补充朝向（哪面对镜头）、接触方式（平放/竖立）、大小参照（和什么差不多大）。
- 不要在 generation_prompt 中描述商品外观——模型从图片1提取。
- 不要在 generation_prompt 中描述视频场景——模型看参考视频就知道。
- negative_prompts 只写 2-3 条视觉失败。
- 商品必须在画面中清晰可见。"""


def build_composition_json_repair_prompt(raw_text: str) -> str:
    return f"""请把下面内容修复成合法 JSON，并严格满足以下约束：
1. 只输出 JSON，不要输出任何解释。
2. 顶层必须是对象。
3. 顶层只允许以下字段：
   segment_index, scene_context, product_feature_specs, product_integration, lighting, motion, mood, negative_prompts, generation_prompt
4. negative_prompts 必须是字符串数组，保留 2-3 条关键视觉失败模式。
5. generation_prompt 必须固定 3 句话：
   第1句：「保持参考视频中的场景、人物、动作和运镜完全不变。」
   第2句：「在参考视频的[精确相对位置]植入图片1中的[商品名称]。」
   第3句：补充朝向、接触方式、大小参照。
6. 不要在 generation_prompt 中描述商品外观或场景内容。
7. 尽可能保留原始语义，不要新增与原分镜无关的设定。

待修复内容：
{raw_text}"""
