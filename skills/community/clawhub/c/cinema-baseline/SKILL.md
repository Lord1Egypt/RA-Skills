---
name: cinema-baseline
description: 全国基线影院数据 Skill（专资编码锚定 + 哈哈预对齐）—— 影院归一化（基线 ↔ 出票渠道映射）身份基准。
---

# 基线影院 Skill（2026-13-15）

全国基线影院数据资产包：13276 家影院（专资编码全表唯一锚定），
其中 11454 家携带哈哈渠道预对齐结果（离线混合归一：规则引擎 ≥0.88 为主、
MGeo 地址互证兜底、不硬匹配；未匹配保留基线原样交由人工裁决）。

## 数据维护

1. cinemaData 离线管线产出新的 `*_含哈哈对齐_混合.json`；
2. 重新构建：`node scripts/build-cinema-baseline-package.mjs --input <新JSON> --version <x.y.z>`；
3. 发布：包目录内 `npm publish --access public`；
4. 宿主更新：`openclaw plugins install clawhub:@rascalagnt001/cinema-baseline`（不带版本号）。

## 数据形状

`cinema-agent/baseline-cinemas.json`：`{schemaVersion, dataVersion, generatedAt,
totalCount, cinemas:[{baselineId, stdCode, name, city, address, chain,
haha?:{cinemaId, name, city, address, source, confidence, score, tier}}]}`。

哈哈对齐双刻度：规则引擎行 `confidence`（0~1）；MGeo 行 `score`（90~132 原始评分）。
