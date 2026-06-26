# Cclaw 命令速查

## 文本创作命令

### 脱口秀 / standup

**命令格式：**
```
写/创作/帮我写一段脱口秀
主题：<一句话描述>
可选：风格偏好、时长要求
```

**知识读取顺序（必须按顺序）：**
1. `modules/writing/standup-template.md` — 结构模板
2. `knowledge/cases/standup/growth-path.md` — 创作者心法（必读）
3. `knowledge/cases/standup/` — 其他案例文件
4. `knowledge/theory/eb7cb5ef.md` — 核心原理
5. `knowledge/theory/ac07d434.md` — 包袱结构

**适用场景：** 单人口述，5-20分钟，幽默演讲、社会观察、自我调侃

---

### 小品 / sketch

**命令格式：**
```
写/创作/帮我写一个小品
主题：<场景+冲突>
人物：<2-5人>
```

**知识读取顺序（必须按顺序）：**
1. `modules/writing/sketch-template.md` — 结构模板
2. `knowledge/cases/sketch/sketch创作模板_平台课程.md` — 小品创作模板
3. `knowledge/cases/sketch/` — 其他案例文件
4. `knowledge/theory/eb7cb5ef.md` — 核心原理
5. `knowledge/theory/9d01e4da.md` — 类型速查

---

### 漫才 / manzai

**命令格式：**
```
写/创作/帮我写一段漫才
题材：<话题描述>
```

**知识读取顺序（必须按顺序）：**
1. `modules/writing/manzai-template.md` — 漫才格式规范
2. `knowledge/theory/eb7cb5ef.md` — 核心原理

**注：** `knowledge/cases/manzai/` 当前为空，跳过案例步骤。

**核心手法：** 连续否认（三次以上）、极致化升级、收尾反差

---

### 讽刺 / satire

**命令格式：**
```
写/创作/帮我写一篇讽刺文章
对象：<社会现象/行业/政策>
角度：<批评/嘲笑/揭示>
```

**知识读取顺序：**
1. `modules/writing/satire-template.md` — 讽刺格式
2. `knowledge/theory/eb7cb5ef.md` — 核心原理
3. `knowledge/theory/126b44e8.md` — 笑的心理学

---

### 仿讽 / parody

**命令格式：**
```
写/创作/帮我写一段仿讽
原作：<作品名/类型>
主题：<新角度/反转>
```

**知识读取顺序：**
1. `modules/writing/parody-template.md` — 仿讽格式
2. `knowledge/theory/9d01e4da.md` — 类型速查

**注：** `knowledge/cases/parody/` 当前为空，跳过案例步骤。

---

### 剧本 / script

**命令格式：**
```
写/创作/帮我写一个喜剧剧本
类型：<情景剧/独角戏/电影/短剧>
主题：<核心冲突>
```

**知识读取顺序：**
1. `modules/writing/script-template.md` — 剧本格式
2. `knowledge/theory/eb7cb5ef.md` — 核心原理

**注：** `knowledge/cases/script/` 当前为空，跳过案例步骤。

---

### 荒诞剧 / absurdist

**命令格式：**
```
写/创作/帮我写一段荒诞剧
概念：<荒诞设定>
```

**知识读取顺序：**
1. `modules/writing/absurdist-template.md` — 荒诞剧格式
2. `knowledge/theory/eb7cb5ef.md` — 核心原理
3. `knowledge/theory/126b44e8.md` — 笑的心理学

---

## 视频工具命令

> 视频工具通过自然语言脚本驱动 FFmpeg。

**基础剪辑：**
```
帮我剪辑视频
文件：<路径>
脚本：<时间戳+操作描述>
```

**拼接：**
```
拼接以下片段（按顺序）：
- <文件1>：<起始时间>-<结束时间>
- <文件2>：<起始时间>-<结束时间>
```

**加字幕：**
```
给视频加字幕
文件：<路径>
字幕内容：<文字>
格式：硬字幕/软字幕
```

**转码：**
```
转换格式
文件：<路径>
目标格式：mp4/webm/mov
```

**更多配方：** 见 `modules/tools/video/README.md`

---

## 海报工具命令

> 海报生成通过 design brief 驱动 canvas-design skill 实现。

### 通用海报

**脱口秀海报：**
```
帮我生成一张脱口秀海报 / 做个B站封面
演员：<名字>
段子名：<名称>
可选：日期、场地、风格偏好
```

**演出宣传海报：**
```
帮我做一张演出海报 / 演出宣传图
演出名：<名称>
日期：<日期> 时间：<时间>
场地：<地点>
演员：<名单>
可选：票价、购票链接、宣传语
```

**金句分享卡：**
```
帮我把这段做成图 / 生成金句卡
内容：<金句文字>
可选：出处、作者、风格偏好
```

### 演出平台标准规格

**海报（竖版）：**
```
生成演出海报（大麦规格）
生成演出海报（猫眼规格）
```
- 大麦：1020×1360px
- 猫眼：1800×2400px（≤2M）

**详情页：**
```
生成演出详情页（大麦规格）
生成演出详情页（猫眼规格）
```
- 大麦：1020px宽，长度不限
- 猫眼：800px宽，长度不限（≤13M，支持动图）

**Banner：**
```
生成Banner（猫眼规格）
生成Banner（秀动规格）
生成Banner（大麦999×375）
生成Banner（大麦1404×320）
```

**从创作联动：**
写完脱口秀/漫才后可直接说「帮我生成一张海报」，自动从创作内容提取信息。

**更多详情：** 见 `modules/tools/poster/README.md`

---

## 通用说明

**创作时必须：**
- 按顺序读取知识（模板→案例→理论）
- 若对应类型的 cases 目录为空，直接跳过案例步骤
- 禁止在正文中出现人名/书名/理论术语标签
- 输出成品后附加创作笔记（手法+知识来源）

**遇到类型不确定时：** 先读取 `knowledge/theory/9d01e4da.md`（类型速查）再决定路由
