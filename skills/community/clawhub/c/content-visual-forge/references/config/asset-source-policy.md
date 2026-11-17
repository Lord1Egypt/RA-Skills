# Asset Source Policy

本文件定义 `content-visual-forge` 在工程化渲染、封面背景、社交卡和公众号文内图中使用外部素材的规则。HTML / CSS 渲染可以引入背景照片、纹理和截图，但必须记录来源、授权状态和替代方案。

## Source Priority

按优先级选择素材：

1. `generated_graphics`：CSS 纹理、渐变、几何图形、图标系统、AI 生成的无文字背景图。
2. `user_provided_owned`：用户明确提供并声明可用的图片、截图、logo、产品图或照片。
3. `official_press_kit`：官网、官方 press kit、公开产品图或品牌素材；只在授权允许的场景使用。
4. `public_domain_or_cc0`：公共领域、CC0 或明确免署名素材。
5. `permissive_stock_license`：Unsplash、Pexels、Pixabay 等免费图库素材；必须记录页面 URL、许可证和访问日期。
6. `cc_by_or_cc_by_sa`：需要署名或相同方式共享的素材；只有当交付形态允许署名和遵守附加条件时使用。
7. `unknown_or_restricted`：来源不明、授权不明、带品牌 / IP / 肖像风险或禁止商用的素材；默认不用。

## Background Asset Rules

HTML / CSS 渲染需要更好的视觉质量时，允许使用：

- 低对比纸张纹理、胶片颗粒、玻璃反光、桌面、自然光、空间背景。
- 与内容相关但不承载事实的抽象背景图。
- 用户授权的截图、产品图、照片或 logo。
- 可验证来源的公共素材。

背景素材不得：

- 干扰中文标题、正文、截图、代码或表格可读性。
- 包含未经授权的人脸、品牌、IP 角色、影视剧照、艺术作品或新闻照片。
- 用作事实证据，除非它来自当前 Source Lock 或可验证授权来源。
- 作为“纯装饰”填补内容结构不足；内容不足时先回到页面角色或内容压缩阶梯。

## Asset Source Record

凡是使用外部图片、纹理、logo、产品图或照片，必须记录：

```yaml
asset_source_record:
  asset_id: ""
  role: background / evidence / logo / product_image / texture / screenshot
  source_type: generated_graphics / user_provided_owned / official_press_kit / public_domain_or_cc0 / permissive_stock_license / cc_by_or_cc_by_sa / unknown_or_restricted
  source_url: ""
  provider: ""
  creator_or_owner: ""
  license: ""
  attribution_required: true/false
  attribution_text: ""
  commercial_use_allowed: true/false/unknown
  transformation: crop / color_overlay / blur / duotone / masked / none
  checked_at: "YYYY-MM-DD"
  decision: use / replace / request_confirmation / reject
  notes: ""
```

如果无法填出 `source_url`、`license` 或 `commercial_use_allowed`，不得把该素材用于正式交付。

## Safe Public Sources

这些来源可以作为素材搜索方向，但仍需逐张确认授权：

- Openverse：适合检索 Creative Commons 和 public domain 图片。
- Wikimedia Commons：适合历史、地点、教育和公共领域素材；必须逐文件检查 license。
- Unsplash / Pexels / Pixabay：适合通用摄影背景；不是“无版权”，必须遵守各自许可证和限制。
- 官方 press kit / 官网素材：适合产品和品牌证据层；只用于授权允许的上下文。

## Engineering Rendering Requirements

进入 `engineering_rendering` 时：

- 背景图应进入数据层或 CSS 变量，不硬编码来源不明的远程 URL。
- 渲染包必须包含 `asset_source_record[]`。
- `object-fit`、`object-position`、遮罩、渐变叠层和模糊参数必须写清楚。
- 背景图不稳定、授权不明或遮挡文字时，改用 CSS 纹理、抽象图形、低噪渐变或重新请求素材。

## Delivery Rules

- 纯 CSS / 自绘 / AI 生成无文字背景：记录为 `generated_graphics`，版权风险低，但仍要检查仿写和平台规则。
- 用户素材：记录为 `user_provided_owned`，不替用户断言商业授权；必要时输出 `needs_user_confirmation`。
- 免费图库素材：记录来源和许可证，不把“免费”写成“无版权”。
- CC BY / CC BY-SA：交付必须包含署名方案；无法署名时不用。
- 来源不明、授权不明或涉及敏感品牌 / 肖像 / IP：拒绝使用，改为抽象背景、信息图或请求用户补充授权素材。
