---
name: cosmetic-detect
version: 1.0.0
description: Analyze facial/body photos to detect signs of cosmetic surgery or aesthetic procedures. Use when the user uploads a photo and asks to identify cosmetic work, detect plastic surgery, assess facial naturalness, check if someone has had work done, analyze before/after photos, or evaluate aesthetic procedure signs. Also trigger when users ask about specific procedures visible in photos (fillers, Botox, rhinoplasty, jaw contouring, etc.), compare photos for surgical changes, or want a "naturalness score" for a face. Works with single images, multiple comparison images, and video screenshots. 触发词：整容检测、看看有没有整、自然度评分、鉴定一下、有没有动过。
---

# Cosmetic Surgery Detection

## Core Principle

Cosmetic procedures alter human tissue in ways that diverge from natural developmental patterns. Detection means identifying "anti-natural" signals — places where anatomy, proportion, texture, or dynamics break the statistical norms of unmodified faces/bodies.

This is adversarial: the best work is designed to be undetectable. **Never claim certainty — use probability language** ("consistent with," "suggestive of," "possible indicator of").

## Analysis Protocol

Before analysis, read `references/analysis-framework.md` for the detailed region-by-region indicator checklist.

### Step 1: Initial Assessment

- **Image quality**: Resolution, lighting, angle, makeup level. Low quality or heavy filters significantly reduce reliability — say so.
- **Apparent ethnicity/ancestry**: Establishes anatomical baseline. A "high nose bridge" is normal for Europeans but statistically unusual for East Asians.
- **Apparent age**: Sets expectations for skin quality, volume, aging signs.
- **Filters/editing**: Check for digital manipulation (smoothing, warping, face-tuning) — flag these as NOT cosmetic surgery to avoid false positives.

### Step 2: Region-by-Region Analysis

Analyze each region independently using indicators from the reference file. For each region assess:

1. Are features within normal range for the person's apparent ethnicity and age?
2. Are there specific indicators of surgical or non-surgical intervention?
3. Confidence level: Low / Medium / High

### Step 3: Cross-Region Coherence Check

The most powerful detection layer. Natural faces have internal consistency. Look for:

- **Ethnic coherence**: Do all features align with one consistent genetic background? (e.g., East Asian bone structure + Caucasian nose bridge = mismatch)
- **Age coherence**: Do all regions show consistent aging? (smooth forehead but aged hands = possible Botox)
- **Symmetry**: Natural faces have asymmetry. Excessive bilateral symmetry suggests correction.
- **Proportion harmony**: Do ratios between features fall within natural ranges?

### Step 4: Output

```
## 整容检测分析 / Cosmetic Procedure Detection Analysis

### 基础信息 / Baseline
- 图像质量评估 / Image quality assessment
- 参考人种基线 / Ethnic baseline reference
- 年龄估计 / Estimated age
- 滤镜/修图评估 / Filter/editing assessment

### 区域分析 / Regional Analysis
For each region with findings:
- 观察到的特征 / Observed features
- 可能的项目 / Possible procedure(s)
- 置信度 / Confidence: Low|Medium|High
- 判断依据 / Reasoning

### 整体协调性 / Cross-Region Coherence
- 种族特征一致性 / Ethnic feature consistency
- 年龄一致性 / Age consistency
- 对称性分析 / Symmetry analysis

### 总评 / Overall Assessment
- 自然度评分 / Naturalness score (1-10, 10=completely natural)
- 最可能的项目清单 / Most likely procedures (if any)
- 整体置信度 / Overall confidence
- 重要声明 / Important disclaimer
```

Use the user's language. Template above is bilingual for reference.

## Special Modes

### Before/After Comparison

When 2+ photos of the same person at different times are provided:

- Align facial landmarks mentally between photos
- Prioritize **skeletal/structural changes** as highest confidence (bone/cartilage don't change naturally)
- Volume changes could be aging, weight, OR fillers
- Skin/texture changes could be aging, skincare, OR procedures

### Celebrity/Public Figure

- Use knowledge of their appearance history if available
- Note that top-tier surgeons' work is hardest to detect
- Be especially careful with confidence levels

### Batch Analysis

When analyzing multiple people (group photo, set of photos):

- Analyze each person independently
- Use the group as a natural baseline for comparison

## Guidelines

- **Never claim certainty.** Even experienced surgeons can't always tell from photos.
- **Acknowledge limitations.** Lighting, angle, makeup, filters, genetics, image quality all affect analysis.
- **Distinguish surgical vs non-surgical.** Rhinoplasty vs Botox have different visual signatures — clearly separate them.
- **Stay neutral.** No judgment about whether someone "should" or "shouldn't" have had work done.
- **Cultural sensitivity.** Double eyelid surgery is extremely common in East Asia. Rhinoplasty is common globally. Note neutrally.
