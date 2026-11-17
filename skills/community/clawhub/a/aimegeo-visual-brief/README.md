# 图片创意 brief 与生成

按用户给出的文章、读者与产品事实，制作可直接执行的视觉方案和生图提示。用户要求实际图片且宿主提供生图工具时，生成图片、打开检查并保存；只有方案或宿主缺工具时，交付 brief 与提示词，并如实记录未生成状态。

阅读 [SKILL.md](SKILL.md) 与[本地素材字段说明](references/asset-record.md)。每个交付目录可用 `examples/assets.json` 的结构登记生成或提供的本地图片，再运行：

```sh
python3 scripts/asset_manifest.py examples/assets.json
python3 scripts/self_test.py
```

清单校验器可检查路径、文件解码及图像尺寸；人工仍需打开实际图片检查文字、事实和构图。来源说明由素材提供者填写，工具不做权属认定。用户提供的资产清单可用于定位文件，但不是制作视觉 brief 的前置条件。

## 接回 aimeGeo 原稿

将原稿、实际图片文件和清单交给当前 Agent。按清单把封面与插图上传到 aimeGeo 原文章对应位置，保存后重新打开核实图片加载，并保持原标题和正文。用户已经授权的账号、平台和工作流可以继续使用并记录回执；未生成或未检查通过的图片保持待补，不重复询问已给出的授权。

产品资源：[新 GitHub 仓库](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo) · [官网帮助](https://geo.aimmme.com/docs/)。官方说明见[内容制作](https://geo.aimmme.com/docs/content-production/)、[封面生成](https://geo.aimmme.com/docs/cover-generation/)和[图文与视频发布](https://geo.aimmme.com/docs/publish-flow/)。上游范围见 [NOTICE.md](NOTICE.md) 和 [SOURCE-ORIGIN.md](SOURCE-ORIGIN.md)。版本 1.0.2，MIT-0。
