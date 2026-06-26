# Pandajourneys 工作流完整文档

## 流水线架构

```
M1策略 → M1.5文案(TTS+搜索) → M2审核
→ M3素材匹配 → M3-BGM → Whisper字幕
→ M4 HyperFrames渲染 → M5质检 → M6发布(Metricool)
```

## 各阶段职责

### M1 — 策略分析
- 读取账号配置（accounts.json）确定方向轮换
- 按 DIRECTIONS 循环分配：成都→重庆→川西→北川→川南

### M1.5 — 文案生成
- DeepSeek API 生成 TikTok 口播（40-60词）
- 搜索注入真实信息（景点事实）
- 输出：钩子→内容→CTA 一条链

### M2 — 文案审核
- 检查 CTA 完整性、句子长度（≤40词）
- 生成 storyboard（分场景 + speech_snippet）
- 同场景去重合并

### M3 — 素材匹配
- 场景名 → 中文关键词 → 素材库匹配
- 精确匹配优先，模糊兜底
- 7天去重（exclude_files）
- 短素材黑名单（<7s 拒绝）

### M4 — HyperFrames 渲染
- 5种视觉风格：velvet / soft_signal / shadow_cut / swiss_pulse / comparison
- Chrome headless 渲染 HTML + GSAP 动画
- 输出 1080×1920 竖屏 MP4

### M5 — 质检
- 黑帧检测（阈值 1.0s）
- 音频电平检查
- 字幕重叠检查
- 场景数量验证

### M6 — 发布
- Metricool API 自动排期
- TK + IG 双平台
- 排期随机偏移（防算法检测）

## 配置文件

`config.yaml` — 主配置
`accounts/` — 每个账号一个 JSON
`config/metricool.json` — Metricool 品牌绑定

## 快速开始

```bash
# 测试单条
python3 scripts/run_and_notify.py 00 2026-06-01 AM

# 批量跑
python3 scripts/batch_runner.py 00 2026-06-01 2026-06-07
```
