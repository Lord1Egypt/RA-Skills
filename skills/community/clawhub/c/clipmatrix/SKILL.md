---
name: clipmatrix
description: "Real-footage batch video production for TikTok/Instagram content matrix — AI script, 5 visual styles, auto match from your library, batch run 25 accounts, auto-publish."
metadata:
  openclaw:
    requires:
      bins: ["python3", "ffmpeg", "node"]
      env: ["DEEPSEEK_API_KEY"]
---

# ClipMatrix — TikTok/IG 真实素材批量混剪+口播+发布矩阵

**定位**：一套用真实素材自动剪辑TikTok/IG短视频的生产线，适合做矩阵运营的创作者。不是模板生成——是真的从你的素材库里匹配实拍画面、AI写文案、TTS配音、自动渲染并发布。

## 核心能力（6个阶段）

| 阶段 | 做什么 | 怎么做的 |
|------|--------|---------|
| **M1 策略** | 自动分配内容方向 | 按方向轮换（成都→重庆→川西→北川→川南），避免相邻视频重复 |
| **M1.5 文案** | AI生成TikTok口播 | DeepSeek写40-60词英文钩子→正文→CTA，注入真实地点信息（非编造） |
| **TTS 配音** | 文字转语音 | ChatTTS原生发音，自动清洗特殊字符，支持男女声切换 |
| **M2 审核** | 文案质量把关 | CTA完整性检查、句子长度校验、storyboard生成 |
| **M3 素材匹配** | 从素材库自动挑素材 | 场景名→中文关键词→素材文件名匹配，7天去重，短素材自动过滤 |
| **M4 渲染** | HyperFrames视觉引擎 | **5种视觉风格**可选：|
| | | ▸ `velvet` — 金色杂志封面风（城市介绍） |
| | | ▸ `soft_signal` — 暖陶土编辑式双字体（亲子/慢旅行） |
| | | ▸ `shadow_cut` — 琥珀SVG路线时间轴（路线定制） |
| | | ▸ `swiss_pulse` — 蓝色动态排版+数字滚动（种草建议） |
| | | ▸ `comparison` — 酒红VS分屏对比（旅游对比） |
| **M5 质检** | 自动质量检测 | 黑帧（>1s自动打回）、音频电平、字幕重叠、场景数量 |
| **M6 发布** | 自动排期发布 | Metricool API → TikTok + Instagram，随机偏移防算法检测 |

## 适用场景

- ✅ 旅游/美食/探店等有**真实素材库**的垂直领域
- ✅ 运营**多账号矩阵**（最多25个账号同时跑）
- ✅ 需要**每天稳定产出**竖屏短视频（当前产出量：日均40+条）
- ✅ 想要**视觉风格差异化**（不同账号不同风格，避免千篇一律）
- ⚠️ 不适合纯AI生成画面、不适合无素材库的纯文字类视频

## 快速开始

```bash
# 1. 安装
openclaw skills install git:373246784-design/clipmatrix

# 2. 配置
cd clipmatrix
cp config.yaml.example config.yaml
# 编辑 config.yaml 填入: DeepSeek API Key, Metricool Token, 素材库路径

# 3. 跑一条
python3 scripts/run_and_notify.py 00 2026-06-01 AM

# 4. 批量生产（7天×2条=14条）
python3 scripts/batch_runner.py 00 2026-06-01 2026-06-07
```

## 配置

| 配置项 | 说明 | 必需 |
|--------|------|:--:|
| `DEEPSEEK_API_KEY` | DeepSeek API Key（环境变量） | ✅ |
| `METRICOOL_TOKEN` | Metricool API Token | ✅ |
| `api.deepseek.model` | 文案模型（默认 deepseek-v4-pro） | - |
| `paths.library_dir` | 素材库存放路径 | ✅ |
| `workflow.tta_max_duration_sec` | TTS最长秒数（默认50） | - |
| `video.min_words/max_words` | 口播词数范围（60-120） | - |
| `directions` | 内容方向列表 | - |
| `accounts.id_range` | 账号ID范围 | ✅ |

## 故障排查

- **M4黑屏** → 素材太短，降 `workflow.storyboard_padding` 或换长素材
- **DeepSeek超时** → API不稳定，切 `fallback_model: deepseek-v4-flash`
- **M3素材缺口** → 素材文件名需包含场景中文名，补到 `library_dir/竖屏/`
- **M6发布失败** → Metricool Token过期，重新获取

完整排查见 `references/TROUBLESHOOTING.md`，架构说明见 `references/WORKFLOW.md`。
