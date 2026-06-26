---
name: ai-content-detection
description: Use this skill whenever a user wants to verify whether content (text, images, audio, video, or documents) was created by AI; detect deepfakes or AI-synthesized voices; use tools like GPTZero, Turnitin, ELA error analysis, or spectral analysis for authenticity checking; understand what percentage of online content is AI-generated; create a structured detection report with confidence scores; or defend against a false AI-writing accusation. Also applies when users suspect received materials (articles, promotional copy, contracts) may be AI-generated and want guidance on how to tell. Relevant regardless of language — including Chinese (检测AI生成内容、AI合成语音、深度伪造、ELA图片篡改分析、置信度报告、AI内容占比统计).
---

# AI内容检测完整指南

## 概述

本技能提供对AI生成内容（文本、图片、视频、音频、文档、链接）的系统性检测方法，包含技术证据指标、置信度框架、工具对比及当前AI内容占比统计数据（截至2025年3月）。

## 快速导航

| 检测目标 | 直接跳转 |
|---------|---------|
| 文章/文本是否AI生成 | → 第2.1节（文本检测）|
| 图片是否AI生成/伪造 | → 第2.2节（图片检测）|
| 视频是否Deepfake | → 第2.3节（视频检测）|
| 语音/音频是否合成 | → 第2.4节（音频检测）|
| 文档/合同是否篡改 | → 第2.5节（文档检测）|
| 链接/流量是否Bot | → 第2.6节（链接检测）|
| AI内容占比统计数据 | → 第一部分 |
| 生成检测报告 | → 第四部分（报告模板）|

---

## 第一部分：AI内容现状统计

| 统计项 | 数值 | 来源 |
|--------|------|------|
| 新发布网页含AI内容比例 | **74.2%** | Ahrefs 2025年4月研究（90万页样本）|
| 所有在线文章中AI撰写比例 | **52%** | Graphite SEO 2025数据 |
| 全部在线文本中AI辅助/生成比例 | **~57%** | 综合分析 |
| 2026年预测AI内容比例 | **~90%** | Europol/欧盟预测 |
| ChatGPT发布前AI内容比例（2022年末）| **~10%** | 历史基线 |
| 金融科技行业2023年Deepfake事件增长 | **700%** | 行业报告 |
| AI生成文档欺诈占比（欧洲2025）| **12%**（2022年<2%）| Deloitte 2025 |

---

## 第二部分：按内容类型的检测方法

---

### 2.1 文本检测（Text Detection）

#### 核心检测指标

| 指标 | 说明 | AI特征 | 置信权重 |
|------|------|--------|---------|
| **困惑度（Perplexity）** | 衡量文本的语言不可预测性 | AI文本困惑度低（5-10），人类文本高（20-50）| 高（但受语言水平影响）|
| **突发性（Burstiness）** | 句子长度/风格的变异程度 | AI文本突发性低，节奏均匀 | 中（现代AI可模仿）|
| **词汇多样性** | 词汇重复率和词汇密度 | AI倾向使用固定词汇组合 | 中 |
| **语义一致性** | 段落间逻辑连贯程度 | AI过度连贯，缺乏人类的思维跳跃 | 中 |
| **水印信号** | 隐藏统计模式/Unicode字符 | 生成时嵌入（可被释义绕过）| 高（若未被篡改）|
| **N-gram分布** | 短语使用频率模式 | 与已知AI模型输出分布匹配 | 高 |
| **风格一致性** | 整篇文章风格变化 | AI风格高度一致，人类有自然波动 | 中 |

#### 重要证据（高置信度）

```
强证据（单项即可怀疑）：
✓ 检测到合法水印信号（如C2PA标准）
✓ N-gram分析匹配已知LLM输出分布
✓ 困惑度持续低于10分（标准英文基准）

中等证据（需多项组合）：
✓ 全文突发性标准差<0.3（异常均匀）
✓ 句子长度标准差<5词（机械规律）
✓ 无拼写错误、无口语化错误
✓ 标点使用完全符合规范（人类有自然偏差）

辅助证据（仅作参考）：
✓ 逻辑结构过于完整（引言-正文-结论）
✓ 缺乏个人经历、情感波动、偏见
✓ 回避争议性立场
```

---

### 2.2 图片检测（Image Detection）

#### 核心检测指标

| 指标 | 说明 | 检测方法 | 置信权重 |
|------|------|---------|---------|
| **视觉伪影（Visual Artifacts）** | 像素排列异常、边缘失真 | 像素级检查、局部放大 | 高 |
| **GAN棋盘格纹** | GAN生成特有的棋盘状噪声 | 频域分析（FFT/DCT）| 高（对GAN图像）|
| **频域异常** | DCT/DWT变换后的低频异常 | HiFE网络分析 | 高 |
| **ELA误差分析** | 不同区域JPEG压缩级别差异 | Error Level Analysis工具 | 高（篡改检测）|
| **元数据检查** | EXIF中相机型号、GPS、时间戳 | ExifTool等 | 中（可被清除）|
| **光照/阴影一致性** | 光源方向与阴影方向矛盾 | 人工/AI综合判断 | 中 |
| **皮肤纹理** | 面部边缘异常融合、不自然过渡 | 局部放大检查 | 高 |
| **手指/文字** | AI图像常见手指数量异常、文字变形 | 人工检查 | 中高 |

#### 重要证据

```
强证据：
✓ FFT/DCT分析发现低频域周期性异常
✓ ELA显示局部区域再压缩痕迹
✓ 皮肤/毛发边缘高度局部放大后出现混合伪影
✓ 检测到C2PA/Content Credentials内容凭据

中等证据：
✓ EXIF元数据完全缺失（现代相机必有）
✓ 手指数量≠5或手指形状异常
✓ 背景中文字无法辨认或逻辑混乱
✓ 眼睛/牙齿区域不自然的对称性

辅助证据：
✓ 整体风格过于"完美"（无噪点、无自然缺陷）
✓ 珠宝、眼镜等配件细节异常
```

---

### 2.3 视频检测（Video Detection）

#### 核心检测指标

| 指标 | 说明 | 检测方法 | 置信权重 |
|------|------|---------|---------|
| **面部特征漂移（FFD）** | 连续帧之间面部特征微妙漂移抖动 | 帧间比较 | 高 |
| **时域频率伪影** | 频域时间轴上的不可见伪影 | 像素级时序频率分析（ICCV 2025）| 高 |
| **光流异常** | 运动轨迹违反物理规律 | 双分支RGB+光流残差模型 | 高 |
| **闪烁/抖动** | 面部局部闪烁（眼、鼻、嘴区域）| 逐帧分析（0.25x速度）| 中高 |
| **时间不一致** | 帧间物体形变、细节消失重现 | 逐帧检查 | 高 |
| **嘴唇同步** | 唇形与音频不匹配 | AV同步分析 | 高（换脸类）|
| **眨眼频率** | 不自然的眨眼节律（过多/过少）| 视频时序分析 | 中 |
| **元数据** | 缺失摄像头信息、时间戳异常 | 元数据工具 | 中 |

#### 重要证据

```
强证据：
✓ 0.25x慢速播放可见形变/翘曲效应
✓ 面部特征漂移（眼/鼻/嘴在静态场景中微抖）
✓ 唇形与音频明显不同步
✓ 帧间光流分析发现非物理运动轨迹

中等证据：
✓ 牙齿细节在不同帧间变化
✓ 头发/耳朵边缘区域出现融合伪影
✓ 视频元数据缺失相机型号信息
✓ 长视频（64帧+）时间轴上累积不一致性

辅助证据：
✓ 背景元素在镜头切换间不自然变化
✓ 环境光源方向与面部高光矛盾
```

#### 2025年前沿检测框架
- **D3**（ICCV 2025）— 免训练，基于二阶牛顿力学特征
- **UNITE**（CVPR 2025）— 通用合成视频检测器
- **FFD + 视频混合**（CVPR 2025）— 面部特征漂移检测
- **AiVidect** — 面向Sora、Veo 3等主流AI视频的实用检测工具

---

### 2.4 音频检测（Audio Detection）

#### 核心检测指标

| 指标 | 说明 | 检测方法 | 置信权重 |
|------|------|---------|---------|
| **梅尔频谱（Mel Spectrogram）** | 时频模式保留分析 | CNN分类器 + Grad-CAM | 高 |
| **MFCC系数** | 梅尔频率倒谱系数 | 传统+深度学习模型 | 高 |
| **常量Q变换（CQT）** | 非线性频率细节分析 | 宽频谱精细分析 | 高 |
| **SSL特征融合** | 自监督学习表征 | Wave2Vec2BERT | 最高（跨域泛化最佳）|
| **语速均匀性** | 人类语速有自然变化 | 时序分析 | 中 |
| **音高/音调自然度** | AI合成音调不自然波动 | 基频分析 | 中 |
| **谐波异常** | 不寻常谐波成分 | 频谱分析 | 高 |
| **背景噪声连续性** | AI音频背景噪声异常均匀或突变 | 声谱对比 | 中 |

#### 重要证据

```
强证据：
✓ 梅尔频谱图显示非自然时频模式
✓ SSL模型（Wave2Vec2BERT）置信评分>0.85
✓ LFCC+MFCC+CQCC三特征融合均异常

中等证据：
✓ 语速方差极低（<0.05ms变异）
✓ 呼吸声、停顿位置不符合人类习惯
✓ 高频谐波分布异常（TTS特有模式）
✓ 音频首尾无自然环境背景噪声

辅助证据：
✓ 整段音频音色完全一致（无情绪波动）
✓ 发音过于标准（方言/口音完全消失）
```

---

### 2.5 文档检测（Document/PDF Detection）

#### 核心检测指标

| 指标 | 说明 | 检测方法 | 置信权重 |
|------|------|---------|---------|
| **ELA误差分析** | 被篡改区域重压缩等级不同 | ErrorLevelAnalysis工具 | 高 |
| **PDF结构法证** | 元数据、字体分析、透明层检测 | PDF元数据工具 | 高 |
| **修订链重建** | 追踪每次修改时间和内容 | 文档历史分析 | 高 |
| **字体一致性** | 不同区域字体渲染差异 | 专业OCR/字体分析 | 中高 |
| **像素级篡改** | 数字/文字替换留下的像素痕迹 | 图像法证分析 | 高 |
| **元数据完整性** | 创建工具、时间戳、作者信息 | ExifTool/pdfinfo | 中 |
| **签名后修改** | 签名后内容被更改（签名仍有效）| 增量更新重建 | 高 |
| **模板特征** | 批量生成文档共享相同模板痕迹 | 跨文档比对 | 中高 |

#### 重要证据

```
强证据：
✓ ELA显示文档中存在不一致的压缩层
✓ PDF增量更新记录显示签名后内容修改
✓ 字体渲染在不同区域明显不一致
✓ 元数据显示生成工具为AI/Python脚本

中等证据：
✓ 创建时间戳与声称日期矛盾
✓ 文档未包含正常相机/扫描仪元数据
✓ PDF结构包含不可见透明层（隐藏内容）
✓ 跨文档分析发现相同模板特征

辅助证据：
✓ 文档来源链接/印章与官方格式不符
✓ 字体大小/间距在关键数字处细微异常
```

---

### 2.6 链接/URL检测（Link/URL/Bot Traffic Detection）

#### 核心检测指标

| 指标 | 说明 | 检测方法 | 置信权重 |
|------|------|---------|---------|
| **流量模式异常** | 突发性访问量/低质量页面高流量 | 流量分析工具 | 高 |
| **用户代理异常** | 过时浏览器/不可能的设备组合 | 请求头分析 | 高 |
| **行为模式** | 完美时间戳规律、机械点击模式 | 行为分析引擎 | 高 |
| **会话数据** | 零秒会话多页浏览、零转化 | Analytics分析 | 高 |
| **地理异常** | 来自异常地区的突发流量 | GeoIP分析 | 中 |
| **Referrer垃圾** | 伪造的来源域名 | 来源分析 | 中 |
| **SSL证书** | 短期证书、不信任CA | HTTPS检查 | 中 |
| **域名历史** | 新注册域名、AI生成的欺骗性域名 | WHOIS + NLP分析 | 高 |

#### 重要证据（AI生成恶意链接）

```
强证据：
✓ 域名注册时间<7天且仿冒知名品牌
✓ 请求中user-agent为已知爬虫/AI工具特征
✓ 点击时间间隔完全规律（毫秒级精确）
✓ 登录失败率异常高（凭据填充攻击）

中等证据：
✓ 访问路径完全相同（无自然浏览习惯）
✓ 流量突增但转化率为0
✓ Referrer域名从未在浏览器中打开
✓ SSL证书域名与显示文本不匹配

辅助证据：
✓ 链接包含AI生成的诱导性上下文文本
✓ 域名使用Unicode字符模仿ASCII（如rnicrosoft.com）
```

---

## 第三部分：置信度评估框架

### 综合置信度评分方法

```
置信度 = (强证据数 × 3 + 中等证据数 × 1.5 + 辅助证据数 × 0.5) / 内容类型最高分

解读：
≥0.75  →  高置信度AI生成
0.50-0.74 →  中置信度（存在AI成分，需综合判断）
0.25-0.49 →  低置信度（疑似AI辅助，不能确定）
<0.25   →  可能为人类创作（不能排除AI辅助）
```

### 实际计算示例（文本检测）

> 某篇文章检测结果：
> - 强证据2项：GPTZero评分0.92 + N-gram匹配GPT-4分布
> - 中等证据3项：全文突发性标准差0.15（极低）、无拼写错误、句长均匀
> - 辅助证据2项：结构过于完整、回避争议立场
>
> 计算：(2×3 + 3×1.5 + 2×0.5) / (3×3 + 3×1.5 + 2×0.5)
>      = (6 + 4.5 + 1) / (9 + 4.5 + 1)
>      = 11.5 / 14.5
>      = **0.79 → 高置信度AI生成**

---

## 第四部分：检测报告生成模板

```markdown
## AI内容检测报告

**内容类型：** [文本/图片/视频/音频/文档/链接]
**检测日期：** YYYY-MM-DD

### 检测结果摘要
- **AI生成概率：** XX%
- **置信度等级：** 高/中/低

### 发现的关键证据

**强证据（权重3）：**
1. [具体发现]

**中等证据（权重1.5）：**
1. [具体发现]

**辅助证据（权重0.5）：**
1. [具体发现]

### 置信度计算
总得分：(强×3 + 中×1.5 + 辅×0.5) = XX / 最高分 = XX%

### 结论
[基于证据的综合判断]

### 局限性说明
- 本报告基于当前可用检测技术，不构成法律证据
```

---

## 第五部分：局限性与注意事项

### 核心局限性

| 局限性 | 影响 | 缓解方法 |
|--------|------|---------|
| **非母语写作者假阳性** | 文本检测准确率显著下降 | 额外人工判断 |
| **对抗性规避** | AI可学会模拟人类特征 | 多特征综合 |
| **跨生成器泛化** | 新模型导致检测率下降50% | 持续更新检测器 |
| **水印可被绕过** | 释义/翻译即可去除 | 结合多种方法 |
| **法律证明力** | 检测结果不足以作为法律定罪证据 | 作为调查线索使用 |
| **压缩降质** | 多次压缩破坏频域证据 | 分析原始文件 |

### EU AI法规要求（2025年3月生效）
- 要求所有AI生成内容必须使用可检测信号标注（水印或元数据）
- C2PA（Coalition for Content Provenance and Authenticity）标准推广中
- 中国要求平台强制执行显性和隐性双重水印

---

## 参考来源

- [Ahrefs: 74%新网页含AI内容研究](https://ahrefs.com/blog/what-percentage-of-new-content-is-ai-generated/)
- [Futurism: 超50%互联网内容为AI生成](https://futurism.com/artificial-intelligence/over-50-percent-internet-ai-slop)
- [Pangram Labs: 困惑度与突发性局限分析](https://www.pangram.com/blog/why-perplexity-and-burstiness-fail-to-detect-ai)
- [PMC: Deepfake媒体法证研究](https://pmc.ncbi.nlm.nih.gov/articles/PMC11943306/)
- [ICCV 2025: 像素级时域频率Deepfake视频检测](https://openaccess.thecvf.com/content/ICCV2025/papers/Kim_Beyond_Spatial_Frequency_Pixel-wise_Temporal_Frequency-based_Deepfake_Video_Detection_ICCV_2025_paper.pdf)
- [CVPR 2025: UNITE通用合成视频检测器](https://arxiv.org/html/2412.12278)
- [Scientific Reports 2025: 深度伪造视频视觉注意力检测](https://www.nature.com/articles/s41598-025-23920-0)
- [PMC: 音频Deepfake检测综述](https://pmc.ncbi.nlm.nih.gov/articles/PMC11991371/)
- [Resemble AI: 音频Deepfake检测工具](https://www.resemble.ai/audio-deepfake-detection-tools/)
- [CheckFile.ai: AI文档欺诈检测技术](https://www.checkfile.ai/en-US/blog/ai-document-fraud-detection-techniques)
- [ACM Computing Surveys: AI生成内容法证系统综述](https://dl.acm.org/doi/full/10.1145/3760526)
- [Imperva 2025 Bot报告](https://www.imperva.com/resources/resource-library/reports/2025-bad-bot-report/)
- [SentinelOne: AkiraBot AI驱动垃圾邮件机器人](https://www.sentinelone.com/labs/akirabot-ai-powered-bot-bypasses-captchas-spams-websites-at-scale/)
- [GPTZero vs Turnitin vs Originality.AI对比](https://hastewire.com/blog/gptzero-vs-turnitin-vs-originalityai-test-results-accuracy-breakdown)
- [UCLA: AI检测工具的不完美性分析](https://humtech.ucla.edu/technology/the-imperfection-of-ai-detection-tools/)
