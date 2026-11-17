# 免费生图 / 生视频模型审计 {{DATE}}

> 由 `free-media-gen` 技能 `media_auditor.py` 自动生成。
> 本报告为**滚动更新**：文件名与标题日期始终反映最近一次审计，旧日期同名文件会在审计时移除，
> 因此始终只保留一份权威清单。

## 一、审计范围

已检测到平台密钥：{{PROVIDERS}}

## 二、当前纳入的媒体模型

| 模型 | 平台 | 模态 | 免费 | 需 VPN | 状态 | 特点 |
|---|---|---|---|---|---|---|
{{INCLUDED_ROWS}}

## 三、新发现的候选模型{{LIVE_NOTE}}

{{CANDIDATES_BLOCK}}

## 四、本次变更

{{CHANGES}}
{{UNREACHABLE_BLOCK}}

## 五、维护提醒

- 密钥以明文存于 `models.json`，建议定期在平台控制台轮换。
- 免费策略可能变动（如 Agnes Video 2.5 Flash 为限时免费），建议按需复检。
- 本次审计仅覆盖"媒体生成"模态；聊天/文本模型由 `free-model-auditor` 负责，两者互不重叠。
