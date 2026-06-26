# 🦞 ClipMatrix — 1人管理100个自媒体账号

<p align="center">
  <b>把你的实拍素材丢进去 → AI写好口播 → 自动匹配画面 → 加上字幕特效 → 批量发布</b><br>
  <b>100条视频成本不到10块钱。真正的一人矩阵工厂。</b>
</p>

<p align="center">
  <img src="demo/before_after.gif" width="480" alt="Before/After — raw footage vs ClipMatrix output">
</p>

---

## 这玩意儿能干嘛

你拍了一堆素材，不想每天花3小时剪视频。ClipMatrix接管全部：

```
你拍的素材 + 你定义的风格卡
        ↓
   AI写口播（钩子→内容→CTA，搜真实信息不瞎编）
        ↓
   ChatTTS原生英文配音（男女声可选）
        ↓
   自动从素材库匹配画面（7天不重复）
        ↓
   5种视觉风格 + 逐词字幕特效（金色/暖陶土/琥珀/蓝调/酒红）
        ↓
   黑帧检测→音画同步→字幕重叠 → 不合格自动重做
        ↓
   一键发布TikTok + Instagram（可根据自身需求调整发布平台）
```

**全程不用你动手。你要做的只有三件事：拍素材、定义风格、收钱。**

## 为什么牛逼

| | 传统做法 | ClipMatrix |
|------|---------|------------|
| 剪辑 | 一条视频30-60分钟 | **40秒** |
| 文案 | 自己想/找ChatGPT | **AI自动生成+真实信息注入** |
| 配音 | 录音/找配音员 | **ChatTTS原生发音** |
| 素材管理 | 手动挑、怕重复 | **自动匹配+7天去重** |
| 字幕特效 | 手动加、一条条调 | **口播词级对齐+自动特效** |
| 发布 | 一个号一条发 | **1人管理100个账号** |
| 成本 | 外包$5-20/条 | **100条不到¥10** |

## 成本拆解（100条视频）

| 费用项 | 花费 |
|--------|------|
| DeepSeek API（文案生成） | ¥2-3 |
| 素材 | 你自己的，免费 |
| TTS配音 | ChatTTS本地跑，免费 |
| 渲染 | 你的电脑跑，免费 |
| 发布 | 看各自需求的自媒体平台API |
| **总成本 100条** | **¥10以内** |

> 一条视频不到1毛钱。外包一条至少$5。100条差$499。

## 6个阶段自动化

```
M1 策略分析      → 自动分配内容方向，避免相邻视频撞车
M1.5 文案生成    → DeepSeek写TikTok风格英文口播，自动搜索注入真实信息
M2 文案审核      → 检查CTA完整性、句子长度、生成分镜表
M3 素材匹配      → 场景名→中文关键词→素材库文件名匹配，7天去重
M4 视觉渲染      → 5种HyperFrames风格模板 + 逐词字幕特效 + GSAP动画
M5 质检          → 黑帧/音画不同步/字幕重叠检测，不合格自动打回重做
M6 自动发布      → 按需选择发布平台API → 自动推送到你的账号
```

## 5种视觉风格

每套风格独立的字体、色系、动画、字幕特效——不同账号不同风格，刷到同一个人的两个账号也看不出来是同一套工具做的。

| Velvet | Soft Signal | Shadow Cut |
|:--:|:--:|:--:|
| ![Velvet](demo/velvet.gif) | ![Soft Signal](demo/soft_signal.gif) | ![Shadow Cut](demo/shadow_cut.gif) |
| 🏙️ 金色杂志风 | 👨‍👩‍👧 暖陶土编辑风 | 🗺️ 琥珀路线时间轴 |
| 城市/奢华 | 亲子/慢旅行 | 线路/攻略 |

## 实际跑分

已经在跑 **25个TikTok+Instagram账号**，日均产出40+条视频。

| Metricool 批量排期 | 多账号发布队列 |
|:--:|:--:|
| ![排期](demo/schedule1.jpg) | ![发布](demo/schedule2.jpg) |

## 安装

```bash
# OpenClaw 一键安装
openclaw skills install git:373246784-design/clipmatrix

# 或手动
git clone https://github.com/373246784-design/clipmatrix.git
cd clipmatrix
pip install -r requirements.txt
```

需要装：Python 3 + ffmpeg + Chrome（M4渲染用）

## 配置

```bash
cp config.yaml.example config.yaml
```

填3个东西就能跑：

| 配置 | 哪来的 |
|------|--------|
| `DEEPSEEK_API_KEY` | [platform.deepseek.com](https://platform.deepseek.com) |
| `METRICOOL_TOKEN` | Metricool后台 → API |
| `paths.library_dir` | 你的素材目录 |

## 使用

```bash
# 单条跑
python3 scripts/run_and_notify.py 00 2026-06-01 AM

# 批量跑（7天=14条）
python3 scripts/batch_runner.py 00 2026-06-01 2026-06-07
```

## 定价

| 方案 | 价格 | 内容 |
|------|------|------|
| 🎉 免费试用 | $0 · 7天 | M1-M5全功能 |
| 💎 Pro 订阅 | **$15/月** | 无限制使用 + 批量生产 + 自动更新 |

[👉 Get Pro · $15/月](https://zplaze.gumroad.com/l/uunfl)

## 更多

- [完整工作流文档](references/WORKFLOW.md)
- [故障排查指南](references/TROUBLESHOOTING.md)
