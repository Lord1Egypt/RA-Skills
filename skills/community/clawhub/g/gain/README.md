# 🌾 GAIN — Genomic-Assisted Intelligence for Agronomic Niches

> 基于 MMoE 深度学习模型的水稻农艺性状预测 AI Skill

---

## 简介

**GAIN** 是一个运行在 AI 助手（WorkBuddy / CodeBuddy）中的 Skill，通过基因型 + 环境数据，预测水稻的 10 种农艺性状，支持多种气候胁迫模拟。

---

## 安装

在 WorkBuddy / CodeBuddy 中，执行：

```bash
clawdhub install gain
```

安装完成后，AI 助手即可自动识别水稻预测请求，无需额外配置。

---

## 支持的性状

| 代码 | 中文 | 英文 | 单位 |
|------|------|------|------|
| HD | 抽穗期 | Heading Date | 天 |
| PH | 株高 | Plant Height | cm |
| PL | 穗长 | Panicle Length | cm |
| TN | 分蘖数 | Tiller Number | 个 |
| GP | 每穗粒数 | Grains Per Panicle | 粒 |
| SSR | 结实率 | Seed Setting Rate | % |
| TGW | 千粒重 | Thousand Grain Weight | g |
| GL | 粒长 | Grain Length | mm |
| GW | 粒宽 | Grain Width | mm |
| Y | 产量 | Yield | kg/ha |

---

## 支持的地点（7个内置站点）

| 代码 | 城市 | 纬度 | 经度 |
|------|------|------|------|
| km | 昆明 | 25.02 | 102.68 |
| gzl | 六盘水 | 26.59 | 104.83 |
| nn | 南宁 | 22.82 | 108.37 |
| wh | 武汉 | 30.58 | 114.27 |
| hf | 合肥 | 31.82 | 117.25 |
| hz | 杭州 | 30.25 | 120.17 |
| th | 通化 | 41.73 | 125.94 |

> 也支持任意经纬度输入，系统会自动匹配最近站点；联网时可调用 NASA POWER API 获取精确气象数据。

---

## 支持的胁迫类型

| 类型 | 说明 | 默认强度 |
|------|------|---------|
| high_temp | 高温胁迫 | 最高气温+3°C，最低气温+2°C |
| low_temp | 低温胁迫 | 最高气温-3°C，最低气温-2°C |
| drought | 干旱胁迫 | 降水减少 90% |
| flood | 涝害胁迫 | 降水增加 3 倍 |
| low_light | 寡照胁迫 | 光合有效辐射减少 60% |

---

## 使用示例

安装 skill 后，直接用中文或英文向 AI 助手提问即可：

### 基础预测
```
预测武汉地区 sample1 的水稻产量和株高
```

```
Predict heading date and grain length for sample1 at lat 30.5, lon 114.3
```

### 胁迫模拟
```
模拟高温胁迫对南宁地区 sample1 产量的影响
```

```
如果发生严重干旱（胁迫强度加倍），合肥地区 sample1 的结实率会怎样变化？
```

### 上传自己的基因型数据
```
我有自己的基因型文件（VAE编码，1024维），帮我预测杭州地区的千粒重
```
> 文件格式：CSV，1024列（VAE编码特征），第一列为样本索引

### 批量预测
```
批量预测 sample1、sample2、sample3 在武汉的所有性状
```

---

## 环境要求（首次使用）

如需手动运行脚本，需安装以下依赖：

```bash
pip install torch>=2.0 numpy pandas scikit-learn scipy requests
```

验证环境：
```bash
python <SKILL_DIR>/scripts/check_env.py
```

---

## 数据说明

- **内置样本**：3925 个水稻样本（sample1 ~ sample3925），已完成 VAE 基因组编码
- **环境数据**：自动从 NASA POWER API 获取并缓存，离线时使用历史均值数据
- **模型**：10 个性状各一个 env+gene 融合模型，7 个站点各一个纯基因型模型

---

## 输出说明

预测结果包含三类值：

| 字段 | 说明 |
|------|------|
| `genotype_prediction` | 仅基因型预测（基线值） |
| `environment_prediction` | 基因型 + 环境融合预测（**主要参考值**） |
| `stress_prediction` | 胁迫情景预测（与正常情景对比） |

---

## 发布信息

- **作者**：[@Qianlvdouhua](https://clawdhub.com/@Qianlvdouhua)
- **版本**：v1.0.0
- **平台**：[ClawdHub](https://clawdhub.com/skills/gain)
- **安装**：`clawdhub install gain`
