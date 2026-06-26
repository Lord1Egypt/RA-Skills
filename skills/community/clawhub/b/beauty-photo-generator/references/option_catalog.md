# Option Catalog

Use these menus when the user's request is short, fuzzy, or missing structure. Reuse the user's own wording whenever it is already specific enough.

## Preset templates

- `A` 东方现代写实（默认）
- `B` 车模写真
- `C` 时尚杂志封面
- `D` 清冷电影感
- `E` 甜美日系
- `F` 高级御姐

## First-round core options

### Face shape

- `1` 鹅蛋脸
- `2` 圆脸
- `3` 心形脸
- `4` 菱形脸
- `5` 方圆脸
- `6` 长脸

### Eye shape

- `1` 杏眼
- `2` 丹凤眼
- `3` 桃花眼
- `4` 狐狸眼
- `5` 瑞凤眼
- `6` 柔和下垂眼

### Hairstyle

- `1` 中长直发（默认）
- `2` 锁骨发
- `3` 利落短发
- `4` 长卷发
- `5` 高马尾
- `6` 低束发

### Vibe

- `1` 温柔清透
- `2` 清冷克制
- `3` 甜美自然
- `4` 都市时尚
- `5` 高级御姐
- `6` 古典柔和

### Background

- `1` 干净高级纯色背景（默认）
- `2` 落地窗城市室内
- `3` 复古质感室内
- `4` 夜景霓虹
- `5` 极简户外
- `6` 汽车或展厅场景

## Second-round detail options

### Age feel

- `1` 23-27岁感（默认）
- `2` 28-32岁感
- `3` 32-38岁成熟感
- `4` 清爽轻熟感

### Body tendency

- `1` 自然匀称身材（默认）
- `2` 健康紧致身材
- `3` 略丰满曲线
- `4` 纤细修长

### Makeup

- `1` 淡妆（默认）
- `2` 裸感光泽妆
- `3` 银闪冷调眼妆
- `4` 玫瑰豆沙妆
- `5` 红唇杂志感妆容

### Hair color

- `1` 自然黑发（默认）
- `2` 深棕色
- `3` 栗色
- `4` 冷棕色
- `5` 玫瑰金
- `6` 亚麻雾棕

### Expression

- `1` 平静凝视（默认）
- `2` 轻微微笑
- `3` 冷淡高级
- `4` 温柔回望
- `5` 若有所思

### Lighting mood

- `1` 自然日光
- `2` 清冷电影感
- `3` 暖调古典氛围
- `4` 高级杂志棚拍
- `5` 夜色霓虹氛围
- `6` 柔雾梦幻感

## Defaults when the user skips the detail round

- Template: `A` 东方现代写实
- Age feel: `1` 23-27岁感
- Body tendency: `1` 自然匀称身材
- Hairstyle: `1` 中长直发 or `3` 利落短发
- Makeup: `1` 淡妆
- Crop: 半身特写
- Style baseline: 写实摄影
- Background: `1` 干净高级纯色背景

## Prompt assembly notes

- Keep the final portrait prompt in natural Chinese.
- If the user says `性感` but is vague, reinterpret it as tasteful fashion portrait language instead of explicit content.
- Preserve any clear user requirements such as hair length, scene, or color choices even when they differ from defaults.
- The two portrait outputs should share one coherent identity and differ mainly by angle:
  - 正面微偏左
  - 侧脸回望
