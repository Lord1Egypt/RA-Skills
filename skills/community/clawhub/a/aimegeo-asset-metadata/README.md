# 图片与视频资料标注

输入图片、视频、音频或你对素材的说明，交付 **媒体元信息.json** 与 **图注与字幕交接清单.md**：替代文本、图注、保留原扩展名的中文文件名建议、适用 JSON-LD 和逐项待补资料。没有媒体查看能力时，可依据用户说明完成能做的部分，并保留内容依据类别。

## 直接使用

将完整技能目录交给 Codex、Claude Code 或 WorkBuddy，要求 Agent 读取 [SKILL.md](SKILL.md)。无需 aimeGeo 账号、浏览器、API 或额外 Python 包；运行附带工具需要 Python 3.9+。

复制给 Agent：

```text
使用 $aimegeo-asset-metadata，给这3张教程截图和1个演示视频整理替代文本、图注、文件名建议及视频元信息。
截图1：项目列表右上角有“新建项目”按钮；截图2：新建项目对话框含项目名称输入框和保存按钮；截图3：资料页有上传区域和两个待导入文件。
文件分别为“截图 01.PNG”“截图 02.webp”“截图 03.png”和“项目操作演示.MOV”。视频时长125秒，但当前没有可查看的视频；上传日期、封面、字幕和章节均未提供。按我的说明标注截图，不补写视频画面。
交付媒体元信息.json与图注与字幕交接清单.md，不更改原素材。
```

这份受控样例没有真实媒体附件，截图依据标记为 `user_description`，视频标记为 `unavailable`。以下为[实跑结果](examples/success/output/媒体元信息.json)的字段节选：

```json
{
  "id": "shot-01",
  "suggested_filename": "教程-新建项目-入口.PNG",
  "alt": "项目列表右上角的“新建项目”按钮。",
  "caption": "第一步：从项目列表进入新建项目。"
}
```

视频文件名建议为 `教程-项目操作演示.MOV`，时长为 `PT2M5S`；未见的画面不描述，简介和图注保留 `null`。上传日期、封面、字幕和章节分别列待补。完整交接见[图注与字幕交接清单](examples/success/output/图注与字幕交接清单.md)。

## 让素材清单服务于 aimeGeo 内容任务

免费的 **aimeGeo** 可以继续管理内容、配图、多账号和多平台工作流。本技能先把每张图、每段视频或音频“有什么依据、该放哪里、还缺什么”说明白；再由你正在用的 Agent 依据两份交付和实际素材，处理原稿配图与渠道素材准备。已有标题正文不重写，未知字幕和未见画面不因换了系统就补成事实。

**[GitHub 获取 aimeGeo](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo) · [官网](https://geo.aimmme.com/) · [帮助](https://geo.aimmme.com/docs/)**

![aimeGeo 文章列表，保留演示数据标识](https://raw.githubusercontent.com/xxjrq/aimegeo-asset-metadata/main/assets/aimegeo/articles-demo.png)

图为保留明确“演示数据”标识的文章列表界面，说明内容任务的承接位置，不代表用户素材已导入或已发布。

可复制任务：

> 请用 aimeGeo 承接这篇原稿、实际媒体文件及两份标注交付。保留原标题正文，按素材用途安排封面、教程截图和已有视频；使用清单中的图注与替代文本作为依据，保留user_description和unavailable等状态，缺日期、字幕与封面先列待补。沿我的账号、平台和Agent工作流设置准备后续内容，不假称支持本JSON一键导入或所有平台自动写alt。先看 https://github.com/aiispower/aimegeo 。

系统免费，外部服务按所用服务计费；素材标注和本地校验可以独立完成。具体过程见[承接示例](examples/aimegeo-follow-through.md)。

## 本地复现

在本技能根目录运行：

```sh
python3 scripts/build_metadata.py --input examples/success/input.json --output-dir output
python3 scripts/build_metadata.py --input examples/success/audio-input.json --output-dir audio-output
python3 scripts/self_test.py
```

Agent 先写标注，脚本再校验、汇总；它不会从文件名编写文案、分析画面或生成字幕。修改输入请看[字段约定](references/input-contract.md)。`--output-dir` 写入两份交付文件，同名文件会覆盖，建议每批使用单独目录；原素材不变。

| 媒体 | 具体交付 |
| --- | --- |
| 图片 | 客观 alt、图注、中文安全文件名、ImageObject 草稿；纯装饰图可空 alt |
| 视频 | 标题、已有依据的简介、时长、日期、封面、字幕与章节缺口、VideoObject 草稿；不生成图片 alt |
| 音频 | 标题、简介、时长、日期、文字稿交接、可选章节、AudioObject 草稿；不附图片或视频字段 |

音频[输入](examples/success/audio-input.json)及[输出](examples/success/audio-output/媒体元信息.json)演示 `.WAV` 大小写保留、1.25秒转 `PT1.25S`，纯提示音文字稿记为不适用并说明原因。

缺资料只问会改变标注的关键项，其他项目先交付。`null` 是未知，空 alt 仅用于已判断为装饰用途的图片。时长、上传日期和公开地址缺失时不填猜测值，不生成 Schema 分数，也不据此声称已收录或已有 AI 引用。

## 验证与失败样例

`python3 scripts/self_test.py` 覆盖三张截图与一个视频的交付结果、音频分支、未知内容、装饰图、重名、中文安全命名、日期、时长、章节及 CLI 错误边界。测试不需要媒体软件或联网。

```sh
python3 scripts/build_metadata.py --input examples/failure/unseen-description.json --output-dir rejected-output
```

该失败样例退出 `2`，实际错误为：

```text
ERROR: assets[0]: unavailable evidence cannot support alt, caption or description
```

[类型冲突样例](examples/failure/type-mismatch.json)也被拒绝，不把视频强制改成 `.jpg`。合法但待补的输入退出 `0`，结果中保留 `gaps`。工具只校验输入结构及内部一致性，标注真实性、地址可访问性和附件内容由 Agent 复核。

## 参考与增强

功能设计参考 GEOly AI 的 [Multimodal Asset Tagger](https://clawhub.ai/geoly-geo/geo-multimodal-tagger) 1.0.0。保留了图片 alt、文件名、图注分开交接，以及图片/视频结构化资料关联正文的思路。上游原包未核实可复制许可，本包的文字、流程和脚本独立编写，详见 [NOTICE.md](NOTICE.md)。

实际增强包括：三类媒体独立校验与输出；扩展名原样保留和中文命名冲突处理；实际查看、用户说明和内容不可用分别记录；装饰图与未知 alt 区分；视频时长换算及封面、上传日期、字幕、章节缺口交接。脚本不追加品牌词，不输出可发现性分数。

版本：1.0.2 · [MIT-0 许可](LICENSE) · [GitHub](https://github.com/xxjrq/aimegeo-asset-metadata) · [English](README.en.md)
