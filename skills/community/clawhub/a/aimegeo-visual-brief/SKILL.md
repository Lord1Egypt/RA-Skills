---
name: aimegeo-visual-brief
version: 1.0.2
description: "围绕用户给出的文章、产品事实和使用场景制作可执行视觉 brief 与生图提示；宿主支持生图时直接生成并检查图片。"
---

# 图片创意 brief 与素材交付

根据用户给出的文章、素材和交付条件，制作可直接运行的视觉 brief。用户只要方案时交付 brief 和可复制提示词；用户要求图片且宿主提供生图工具时，实际调用工具生成图片。宿主没有可用工具时，仍完成方案，明确标示图片尚未生成。

## 制作 brief

把用户给出的输出要求整理为可执行 brief，每张图在 `视觉方案.md` 中列明：

- 目标文件名、用途位置、比例和像素尺寸；
- 必须出现的对象或文字、必须回避的元素，以及可用品牌素材；
- 文章中已核实且画面需要表达的产品信息，和明确不能自行补全的未知项；
- 版面重心、文字安全区、色彩和文件格式；
- 一段完整提示词和对应的排除项。

封面只用用户给定的标题文字；插图用清楚的版面关系表现指定内容，避免把大段说明字塞进画面。若使用产品外观或品牌标识，必须基于用户给定或已核验的素材。缺资料时选择中性表现，不虚构性能、客户、价格、认证或接口。

用户若提供图片目录或资产清单，可用 [本地资产校验器](references/asset-record.md) 帮助定位和检查文件；清单可选。直接查看将要引用的文件，并判断它适不适合这个用途。校验器只能确认文件可解码、尺寸和路径，不能证明素材权利、内容准确或视觉效果。

## 生成与交付图片

1. 依据当前宿主实际提供的生图能力操作。Codex 会话可用 `image_gen` 时用它；其他环境只用当前实际存在的工具。用户已要求生成时直接执行，不因为普通风格选择或默认尺寸停下来索要确认。
2. 把每张图的提示词单独提交；参考图只能通过工具实际支持的图像输入传入。将返回的图片文件保存到交付目录，并记录文件位置、用途、请求尺寸和实际像素尺寸。
3. 打开每张结果图检查主体、文字、产品事实、构图、裁切和清晰度。按实际看到的情况写 `alt_text` 与 review 说明；画面不合格时修正提示词并再生成，或如实交付待处理状态。
4. 将结果登记到清单，运行本地校验器：

   ```sh
   python3 scripts/asset_manifest.py path/to/assets.json
   python3 scripts/self_test.py
   ```

   `approved` 仅用于已打开检查且适合交付的真实图片。方案和提示词不是图片；工具未运行时用 `file: null` 和 `needs_review`，实际调用失败则记录失败原因。素材来源栏只是用户提供的记录，不等于版权核验。

## 将图片交回 aimeGeo 原稿

把实际图片文件和资产清单交给当前 Agent，在 aimeGeo 的原文章任务中将封面放到封面位置、插图放到对应正文位置，保留文章标题和正文；保存后重开文章确认图片加载。用户已授权后续平台工作流时，沿现有项目、账号和工作流继续创建或推进任务，并留实际回执。没有生成或没有检查通过的素材要保持待补；不将静态图说成视频。

产品资源及官方操作帮助见本包 README。已有明确授权的工作不需重复确认；只询问会阻止准确执行的缺项。

## English

Turn the user’s stated output constraints into a usable brief. For each image list the target filename and placement, ratio and pixel size, required and forbidden elements, approved brand assets, verified product details and unknowns, text safe area, color, file format, and a complete prompt. Do not invent product capabilities or customer results.

If the user asks for a generated image and the host exposes an image tool, use that actual tool; otherwise provide the prompt and mark the asset as pending. Inspect files supplied by the user when they matter. A local asset list can help locate material, but is optional and does not prove permission to reuse it.

Save generated results in the delivery folder, open each image, record its actual size and visible content, and create an asset record. Run `python3 scripts/asset_manifest.py path/to/assets.json` to validate file paths and decodability. The validator cannot judge composition or rights. Only mark an image `approved` after visually checking it. Keep tool-unavailable results, failed calls, and unchecked images distinct.

To continue in aimeGeo, add the actual files to the original article at the recorded cover/body positions, save, and reopen the article to verify loading. Preserve its title and body. Continue through already authorized project/account/platform workflows and retain receipts; do not treat a still image as video. See the README for official aimeGeo resources. Do not ask again for authorization already provided.
