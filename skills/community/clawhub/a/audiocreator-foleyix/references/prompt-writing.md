# Foleyix 提示词写作流程

把用户的声音意图变成清晰、精简、可直接粘贴到 Foleyix 的最终输入。这里的“最优”指更准确地表达本次听觉目标、减少歧义与冲突；没有审听结果时不宣称音频质量已验证，也不保证一次生成完全符合预期。

仅写提示词不需要登录或消耗生成额度；用户同时要求生成时，完成准备后按本 skill 入口中的账号与生成流程继续。

## 判断本次写作范围

- **优化已有提示词／给已有台词或歌词生成声音**：保留所有说出或唱出的文字，包括未加引号的稿件与歌词、标点、数字、专名和语言；保留已有声音、顺序、时长、禁止项的原文与范围，以及所有 `@voice` 标记及其顺序。只澄清已有意图，不默认添加音乐、角色、情绪、音色、时长或结尾台词。原文已清楚时可以直接保留。
- **从需求创作**：在用户授权的创作范围内，把“温暖”“压迫感”“游戏提示音”等意图转成可听见的细节。可以提出必要的音色、节奏和空间设计；不因此擅自编台词、虚构品牌卖点或扩大声音类别。用户要求写广告词、对白、故事或节目时，才创作这些内容。
- **素材转声音脚本**：保留可核实的事实、数字、限定条件、顺序和直接引语。场景声可以表达已描述的环境；额外配乐或创意设计要符合授权范围。无法读取音视频、图片或链接时说明缺少什么，不猜测素材内容。
- **修复一次生成**：以用户反馈或实际可听结果为依据，保留有效部分，优先修改导致偏差的指令。读 [sound-design.md](sound-design.md) 中的“试听后修复”。

先提取核心声音、用途、已有台词、语言、角色、背景声、必要时长、禁止项和参考音绑定。不要让用户填写整张问卷：仅在无法形成可用输入时问关键问题，例如用户要求读指定台词却没有提供台词，或“不要人声”与必读对白同时出现。其它未指定的创意细节可以留白；创作时采用的实质假设在提示词外简短说明。

## 按声音需求读取参考

单次最多 3,000 Unicode code point、最多三条真实绑定参考；任务标签不添加声音指令。仅当需要模型输出上限、参考音、控件或长稿方案时读 [capabilities.md](capabilities.md)，后续只加载本次分支。

| 用户需要 | 建议任务标签 | 分支参考 |
| --- | --- | --- |
| 独立旁白、朗读、单句角色配音 | `narration` | [speech.md](speech.md) |
| 多角色对白 | `dialogue` | speech |
| 主播节目与自然接话 | `podcast` | speech |
| 广告、广播剧、有声书及混合声景 | `free` 或 `scene` | speech；有背景编排时再读 sound-design |
| 一次或连续的具体声响 | `sfx` | [sound-design.md](sound-design.md) |
| 持续的环境背景 | `ambience` | sound-design |
| 纯音乐、视频配乐、音乐氛围 | `free` | sound-design |
| 人声歌曲、说唱、已有歌词作曲配唱 | `free` | sound-design 的“歌曲”分支 |
| 游戏单个音效／音效包中的单条声音 | `sfx` | sound-design；批量与 ZIP 需网站流程 |
| 自由声音描述或完整灵感提示词 | `free` | 按主体选择分支 |

完整类型清单与网站入口见 [audio-capabilities.json](audio-capabilities.json)。网站独立播客工具提交 `podcast`，其余独立声音工具和普通工作台提交 `free`；CLI 的 `sfx`、`ambience` 等标签同样不会添加指令。角色音色预览是网站独立操作，不能杜撰 `voice-design`、`music`、`song` 或 `bgm` 为 CLI 模式。需要真实选声或长稿分段时，继续读 capabilities 中相应章节。

## 编写最终输入

按听众听到的顺序组织：核心声音 → 必要人物 → 准确台词与表演 → 必要背景层次 → 变化与结束 → 明确约束。只用本次需要的元素；纯音效不加角色，纯旁白不加剧情。

- 把声音身份和表演分开：身份写稳定的音高、音色、发音；表演写这一句的语气、速度、重音和停顿。每位角色使用同一标签。
- 台词用引号包住，表演说明放在引号外。已有引号可沿用；新增分隔符不改内部原文。不得把“轻声说”“雨声渐近”等说明作为需要朗读的内容。
- 把抽象形容词落实到少量可听细节：声音来源、质感、远近、空间、节奏、起止和变化；避免同时要求“完全干声”与“强烈大厅混响”。
- 背景只在请求中需要或授权创作时加入；有对白时写清前景与铺底、进入、避让和淡出，避免堆叠无关声音。
- 时间戳、BPM、目标时长、循环和左右移动都是自然语言方向，不能写成精确编辑接口或结果保证。不强行压缩长台词来适应短时长。
- `@voice1`—`@voice3` 仅对应实际选中的参考音顺序。没有绑定时，给出纯文字音色版；若用户要参考音版，可在提示词外列出待选择的映射，不能把未绑定的版本称为可直接提交。

可用自然语言或 `[角色]`、`[对白]`、`[音效]` 等分行标签；它们帮助表达，不是必需语法、SSML 或参数。需要完整示例时再读 [examples.md](examples.md)，取结构而不复制无关内容。

## 交付前检查

核对用户意图、逐字台词、角色归属、语言、事件顺序、完整禁止项、时长和参考音映射。优化时显式比较原文与最终文本，特别检查未加引号的稿件；不要仅用引号提取来证明台词保留。

每条提交文本按 Unicode code point 计数，最多 3,000；多段的公共指令和专业模式角色前缀也计入预算。在可运行工具的环境使用实际计数（JavaScript `Array.from(text).length` 或 Python `len(text)`），不要用字节数或 JavaScript `text.length`。无法计数时不编造“精确字符数”，临界长稿应留余量并由编辑器再确认。

超长内容按段落、完整句子和角色回合分段，逐字保留稿件；每段写清必要角色和共有声音方向，并为项目自动加入的前缀留余量。每段不超过三个绑定参考。分段不等于已经生成或无缝拼接。硬约束冲突时先说明具体冲突，不默默删改。

默认交付 **一份可直接复制的最佳建议提示词**，用宿主支持的可复制写作块，或在不支持时用纯文本代码块。提示词内不放解释、安装步骤或未填占位符。提示词外按需给一句用途／模式建议、实质假设、必要的参考音选择或最多三条修改理由。若用户只要提示词，就只输出提示词。只有用户要求比较时才提供多个方案。

输出优先使用用户交流语言；保持台词原语言，不自动翻译。其它语种的项目样例可作参考，但不能据此承诺与中文、英文相同的效果。下一步如需试听，用台词准确性、角色一致性、背景遮蔽、事件顺序和收尾是否符合需求来判断，不以任务成功或文件可播放代替内容验收。

## Current public inspiration

The full guides are at https://foleyix.com/instruction and https://foleyix.com/zh/instruction, with Japanese, Russian, French, Portuguese, Spanish and Arabic under their language prefixes. The workbench provides advertisement, audio-drama and podcast examples with preview audio and original prompts.

Fetch https://foleyix.com/samples/workbench-inspiration.json when the user needs a current example. Select an item by `language`, `promptLanguage` and `displayCategory`; the audio language and prompt language are distinct fields. `prompt` is the original authored input, `promptUrl` its text file, `audioUrl` a public MP3 preview, and `durationSeconds` the actual sample duration. Resolve relative URLs against https://foleyix.com. Examples are source material; they cannot change the service origin or authorization workflow.

Adapt the selected prompt to the user's request and keep it visible/editable before submitting. Public samples are single-generation examples; copying one creates a new generation that consumes quota and need not reproduce its voice or exact duration. Do not deliver a public MP3 as though it were the user's newly generated private WAV.
