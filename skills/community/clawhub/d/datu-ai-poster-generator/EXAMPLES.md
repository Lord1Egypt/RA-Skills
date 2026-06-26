# 使用示例

## 示例 1：设计化大图生成

```json
{
  "text": "请将以下内容整理成一张适合发布会传播的高质量海报：2026 春季产品发布会，主题为“智能协作新范式”，包含时间、地点、亮点和报名方式。",
  "aspect_ratio": "16:9",
  "resolution": "4k",
  "magic_wand": true
}
```

适合：

- 发布会
- 活动宣传
- 长内容整理成结构化海报

## 示例 2：竖版 9:16 大图生成

```json
{
  "text": "把以下政策解读生成一张适合手机端传播的竖版海报，顶部标题要强，内容分成四个纵向模块，底部保留总结区。",
  "aspect_ratio": "9:16",
  "resolution": "4k",
  "magic_wand": true
}
```

适合：

- 朋友圈传播
- 公众号配图
- 小红书 / 短视频封面式信息图

## 示例 3：关闭魔法棒，直接用原始 Prompt

```json
{
  "text": "A premium fintech infographic poster about AI wealth management in China, deep navy and gold palette, elegant typography, bold title, readable Chinese labels",
  "aspect_ratio": "16:9",
  "resolution": "4k",
  "magic_wand": false
}
```

适合：

- 已经写好 Prompt
- 只想让系统直接生成
- 快速实验多个视觉方向

## 示例 4：文件上传生成

请求：`multipart/form-data`

字段：

```text
file=marketing-plan.pdf
aspect_ratio=21:9
resolution=4k
magic_wand=true
```

说明：

- 系统会先解析文件
- 开启 `magic_wand` 时会做设计化 Prompt 生成
- 关闭 `magic_wand` 时会把解析文本直接作为 Prompt

## 示例 5：基础修图

用户说“改这张图”“修改这张海报”“基于原图修改”“换字”“替换 logo”“保留版式继续优化”时，必须走 /api/edit/create，不要重新生成一张新图。

```json
{
  "image": "https://cdn.example.com/poster.png",
  "prompt": "把整体配色改成深蓝金，强化标题区层次，并让模块分隔更清晰",
  "magic_think": true,
  "aspect_ratio": "16:9",
  "resolution": "4k"
}
```

适合：

- 已有海报换字、改色、调布局
- 保留原图主体和版式，只做局部优化
- 基于上一轮生成结果继续修改

## 示例 6：继续修图 + 标注图 + 参考图

```json
{
  "image": "https://cdn.example.com/poster-v1.png",
  "annotated_image": "https://cdn.example.com/poster-annotated.png",
  "ref_images": [
    "https://cdn.example.com/ref-a.png",
    "https://cdn.example.com/ref-b.png"
  ],
  "prompt": "按标注区域强化顶部标题区，参考图的高级金属质感可以借鉴到主视觉卡片上",
  "magic_think": true,
  "aspect_ratio": "9:16",
  "resolution": "4k",
  "parent_task_id": "DT1234567890"
}
```

## 示例 7：查询大图状态

```bash
curl https://datu.digilifeform.com/api/datu/status/DT1234567890 \
  -H "X-API-Key: YOUR_API_KEY"
```

## 示例 8：查询修图状态

```bash
curl https://datu.digilifeform.com/api/edit/status/ED1234567890 \
  -H "X-API-Key: YOUR_API_KEY"
```
