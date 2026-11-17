# Foleyix 能力与提交边界

按 2026-10-04 的本地代码与官方文档整理。声音类型、网站路径、CLI／网站模式和输入限制以同目录 [audio-capabilities.json](audio-capabilities.json) 为准，它与网站共用源清单。此快照不证明所有本地页面已经上线；当用户要求实时可用性、具体目录项或线上操作时，读取当时的公开页面／数据，而不是沿用数量或发布状态。公开能力描述地址为 `https://foleyix.com/audio-capabilities.json`；未上线或读取失败时回退到包内快照。

## 单次生成

- 模型：`qwen-audio-3.1-tts-next`，统一生成人声、对白、音效、环境声与综合声景。项目也提供纯音乐 BGM 和有歌词演唱／说唱的歌曲生成，均沿用同一链路与 `free` 输入。不要将歌曲与纯器乐混为一种。
- 任务标签：`free`、`narration`、`dialogue`、`podcast`、`scene`、`sfx`、`ambience`。标签不追加隐藏风格、时长或内容指令；想要的声音必须写在最终文本里。独立播客工具提交 `podcast`，普通工作台及其它独立声音工具提交 `free`。CLI 可用 `free` 生成人声歌曲，无专用 `song` 参数。
- 文本上限：3,000 Unicode code point，包含换行、空格、共享指令、必要的角色参考前缀。官方输出上限：播客 240 秒，其它场景 120 秒。不能靠选 `podcast` 保证生成四分钟，也不能用该标签绕过其它场景的上限。
- 模型官方明确列出的语种为中文、英文。本地界面与角色／声音样例另含日、俄、法、葡、西、阿拉伯和韩语；UI 语言、提示词语言和实际说话语言是三个独立概念。用户选其它语言时保留原语言，说明该语言需要试听验证即可。
- 音频长度、精确停顿、节拍和音色一致性需要实际结果验证。项目常规生成请求 WAV、48 kHz、双声道；不能把文字要求当作已实现的多轨、音频 stems 或任意编码参数。

## 参考音与音色设计

| 路径 | 提示词写作所需区别 |
| --- | --- |
| 不选参考音 | 用文字描述合成人物的声音；不需要 `@voice` 标记 |
| 网站角色库 | 可以筛选试听、查看原始提示词，导入为自己账号的 ready 参考音后再选择；目录卡片 ID 不能直接当作 `@voice` 或 provider voice ID |
| 网站设计角色 | 分别提供声音描述与短样例台词；项目用同一个生成模型制作单人干声预览，目标不超过 25 秒，实际参考须不超过 30 秒 |
| 网站上传参考音 | 当前代码有权限／说话者许可确认和文件校验；每条最长 30 秒、最大 10,000,000 字节。浏览器转为 24 kHz 单声道 WAV，再进入已有参考音流程；是否线上开放需当时确认 |
| `$audiocreator-foleyix` CLI（1.5.0） | `voices --json` 查询账号已保存参考音；生成时重复 `--voice-id ID`，最多三条，按参数顺序映射 `@voice1`–`@voice3`。用 `voice-create` + `voice-preview` 创建合成参考，或用 `voice-upload --rights-confirmed` 上传有权使用的 WAV；这些写入需新增 `voices:write` 授权，旧连接需重新登录。目录导入仍用网站；仅写标记不会附上文件 |
| 公开生成 API（API key） | 仍只提交 `mode` 和 `prompt`，不支持参考音绑定；不要混同官方 CLI 的设备授权接口 |

最多三条参考，按选择顺序对应 `@voice1`、`@voice2`、`@voice3`，把编号与角色清晰关联。用户已有映射时保留，不自动重排。用户要求四位角色不等于必须选四条参考：可用合成描述区分，或在确实需要四个参考时分成多段；不保证同一参考分饰角色的差异。

当前本地目录是 104 条原创合成角色预览，含九种语言的基本档案和 32 个中文角色风格；年龄标签表示听觉印象。动漫／影视／游戏名称是发现与风格线索，不能称为官方演员声音。不要复制整个目录到提示词；有需要时只选本次相关条目。

目录读取：仓库 `app/lib/voice-catalog.json`，公开快照 `https://foleyix.com/voice-library/manifest.json`。关注 `language`、`promptLanguage`、`prompt`、`spokenText`、`referenceId`（若有）、真实时长和参考文件。条目用了另一个参考音时，原始提示词不能脱离该参考假装可独立复现。试听页是 `https://foleyix.com/voice-library`（中文 `/zh/voice-library`）。

## 控件与长稿

网站普通生成另有全局音量 0—100（默认 50）和速度 0.5、0.75、1、1.25、1.5、2 倍（默认 1）。数值参数不是角色演技：一句“紧张地快速接话”仍需写在文本中。仅在用户要设置时推荐控件，避免与已写的速度要求冲突；CLI 无这些参数。

专业项目支持分段、最多三个 ready 参考、共享声音指令、版本选择，以及音量、间隔、裁剪、淡入淡出和导出。当前分段流程以每段估计最多 120 秒为边界，自动切分目标约 2,000 原始字符，最多 100 段；最终编译文本仍须不超过 3,000。这只是项目的分段路径，不能承诺把十分钟全文一次生成。遇到逐字长稿，不静默摘要或删掉关键内容；优先使用专业分段方案。

## 灵感与来源

选公开样例时区分原始提示词和声音结果，取组织方式，不搬入无关台词、品牌或场景。已有脚本优化器的原则是保留全部说出的文字、原语言、参考标记和完整约束，不填补未给出的创意；显式创作请求则可以按授权范围写新内容。

本地依据（有仓库时再查看）：`app/lib/audio-input.ts`、`app/lib/contracts.ts`、`app/server/generations.ts`、`workers/generation-workflow.ts`、`app/server/prompt-optimization.ts`、`app/lib/professional-split.ts`、`skills/audiocreator-foleyix/SKILL.md`、`docs/voice-library.md`、`docs/bgm-generator.md`。

## 保持同步

维护源是 `app/lib/audio-capabilities.json`，网站认证入口、生成控件的提交模式和输入限制读取它。`node scripts/sync-audio-skill.mjs` 更新包内 `references/audio-capabilities.json`、入口类型表与公开静态描述 `public/audio-capabilities.json`；`--check` 只校验、不改文件。打包拒绝不同步的源与快照，不能只改一份技能文档就宣布网站具备新能力。

新类型必须有真实网站流程、受支持的 CLI 映射或明确标为网站专属；相关写作分支也要同步更新。生成单条声音、网站批量控制、长期参考音资源和整节目编辑／导出是不同操作，即使声音种类一致也不能虚构 CLI 参数。需要实时能力时读公开描述；新增线上模式若本地 CLI 未实现，更新技能或进入网站，不能直接将远程任意字符串当作模式提交。

外部依据（2026-10-03 读取；模型上限取模型详情，项目输入边界取当前代码）：[官方模型详情](https://help.aliyun.com/zh/model-studio/qwen-audio-3-1-tts-next)、[官方音频提示词指南](https://help.aliyun.com/zh/model-studio/audio-generation)、[Foleyix 写作说明](https://foleyix.com/zh/instruction)。不把官方 API 能力自动视为当前 Foleyix CLI 已支持的参数。
