# 🔮 comprehensive-divination-skill

> 算卦综合 Skill · A Comprehensive Fortune-Telling Skill for AI Agents
> [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
> [![agentskills.io](https://img.shields.io/badge/standard-agentskills.io-blue)](https://agentskills.io)
> [![Python](https://img.shields.io/badge/python-3.11%20%7C%203.13-blue)](requirements.txt)

四术合一 · 智能路由 · 真太阳时校准 · 农历节气精确计算

Four methods in one · Smart routing · True solar time · Precise lunar calendar

---

## ✨ 特性 / Features

| | 中文 | English |
|---|---|---|
| 🎯 **四术合一** | 小六壬 / 六爻纳甲 / 梅花易数 / 大六壬 四大主流算卦法 | Four classical methods in one package |
| 🧠 **智能路由** | 根据问题复杂度、决策重要性、时效、领域四维评分，自动推荐最优方法 | 4-dim weighted scoring auto-recommends the optimal method |
| ⏰ **真太阳时** | 50+ 城市内置经纬度，支持手动输入经度，自动校正时辰边界 | Built-in coordinates for 50+ cities, manual longitude input |
| 🌍 **海外友好** | 时间基准强制为北京时间（UTC+8）；内置 60+ 中国城市 + 40+ 英文城市字典；支持经纬度（西经为负）；查不到时自动网络降级 | Time anchor is Beijing time; 60+ CN cities + 40+ EN cities; auto network fallback |
| 📅 **zhdate 精度** | 基于 zhdate 的农历 / 节气 / 干支精确计算（节气级精度） | Zhdate-backed lunar / solar-term / ganzhi precision |
| 🔧 **可调用脚本** | 5 个独立 Python 脚本，支持 `--json` 输出，可被任何 LLM 消费 | 5 standalone Python scripts with `--json` output |
| 🔌 **函数化 pipeline** | 4 个独立函数可串可拆：get_beijing_time → longitude_to_true_solar → datetime_to_shichen → 起卦 | 4 composable functions for custom pipelines |
| 📚 **知识库** | 15 篇 markdown references，覆盖核心理论与各方法细则 | 15 markdown references covering theory + methods |

## 🌍 海外用户 / International Users

时间基准强制为北京时间（UTC+8），与用户机器所在时区无关。

```bash
# 海外用户用法 3 种方式（按推荐度排序）

# 方式 1：直接传经度（最快、最精确）
python common.py --snapshot --lon -74.006    # 纽约
python common.py --snapshot --lon -0.1278    # 伦敦
python common.py --snapshot --lon 151.21     # 悉尼

# 方式 2：传城市名（自动查表，国内+海外 100+ 城市）
python common.py --snapshot --city 纽约
python common.py --snapshot --city "New York"
python common.py --snapshot --city 香港       # 国内/港澳

# 方式 3：未知名城市 → 自动调用 Open-Meteo Geocoding API 网络查询
python common.py --snapshot --city Reykjavik  # 雷克雅未克（冰岛）
# 查询结果自动缓存到 scripts/_geo_cache.json，下次秒开
```

**网络行为说明**：
- 本地查表命中 → **0 ms**（无网络）
- 本地缓存命中 → **0 ms**（无网络）
- 都未命中 → **0.3-0.8 秒**网络查询（Open-Meteo 免费 API，无需 key）
- 完全离线时网络降级会失败 → 改用 `--lon` 传经度即可

**Python API**（推荐，函数化 pipeline）：

```python
import sys; sys.path.insert(0, 'scripts')
import common

# 1. 强制取北京时间（不依赖机器本地时间）
bj = common.get_beijing_time()

# 2. 北京时间 + 经度 → 当地真太阳时
tst = common.longitude_to_true_solar(bj, longitude=-74.006)  # 纽约
print(tst['tst_datetime'], tst['tst_offset_min'], '分钟')

# 3. 一站式：取北京时间 + TST 校准 + 时辰 + 农历 + 干支
info = common.get_full_pipeline(longitude=-74.006)
print(info['day_gz'], info['shichen'], info['lunar_month'], info['lunar_day'])

# 4. 海外城市名查坐标（自动 local → cache → network 三级回退）
coord = common.get_city_coordinates('纽约')
# {'name': '紐約市，纽约州，美国', 'longitude': -74.006, 'latitude': 40.714, 'source': 'cache'}
```

**The time anchor is always Beijing time (UTC+8)**, independent of the user's local timezone. This ensures divination timing is consistent worldwide.

## 🚀 快速开始 / Quick Start

### 安装 / Install

```bash
# 1. 把 skill 放到 Hermes / 任何 agentskills.io 兼容 agent 的 skills 目录
cp -r comprehensive-divination-skill ~/.hermes/skills/

# 2. 安装唯一外部依赖
pip install -r requirements.txt   # 安装 zhdate==0.1
```

> **注意**：如果你的 `python` 解析到 venv 但 venv 没有 pip，先 `python -m ensurepip`。

### 三步起卦 / 3-Step Divination

```bash
# Step 1: 冻结时间 + 真太阳时校准（成都）
cd comprehensive-divination-skill/scripts
python common.py --snapshot --city 成都

# Step 2: 选择方法并起卦（小六壬）
python xiao_liuren.py -m 4 -d 25 -t 15

# 或六爻
python liuyao_yaogua.py --json --day-tg 乙 --day-dz 卯

# 或梅花
python meihua_qigua.py -d 2026-06-15 -t 8

# 或大六壬
python da_liuren.py -d 2026-06-15 -t 8
```

## 📖 触发方式 / Triggers

**中文关键词** / Chinese: 算、占卜、卜卦、算算、测算、求测、预测、小六壬、六爻、梅花易数、大六壬、马前课、掐指、摇卦、铜钱卦、起卦、断卦

**English keywords**: divination, fortune telling, oracle, I Ching, hexagram, Meihua, Liu Yao, Da Liu Ren, predict, cast lots

## 🏗️ 架构 / Architecture

```
用户输入 "帮我算个事"
  ↓
[Step 0] 时间锚定 + 真太阳时校准  →  frozen snapshot
  ↓
[Step 1] 智能路由（4 维加权评分）  →  选方法
  ↓
[Step 2] 按需加载 references       →  加载方法详情
  ↓
[Step 3] 确定性计算（Python 脚本）  →  卦象 / 起卦
  ↓
[Step 4] LLM 解读（五行生克等）    →  最终解读
```

## 📚 Examples

End-to-end usage examples:

- **[examples/quickstart.md](examples/quickstart.md)** — 3-step cold-start for all 4 methods
- **[examples/re-consultation-comparison.md](examples/re-consultation-comparison.md)** — same question, 4 castings over 6 days (脱敏真实案例)
- **[examples/international-user.md](examples/international-user.md)** — time anchor + longitude calibration for users outside UTC+8

## 📂 目录结构 / Directory Structure

```
comprehensive-divination-skill/
├── SKILL.md                    # Skill 主文档（含 frontmatter）
├── README.md                   # 本文件
├── LICENSE                     # MIT License
├── CHANGELOG.md                # 版本变更
├── requirements.txt            # 依赖（zhdate==0.1）
├── scripts/                    # Python 计算脚本
│   ├── common.py               # 干支/农历/月将/真太阳时/城市查询
│   ├── xiao_liuren.py          # 小六壬
│   ├── liuyao_yaogua.py        # 六爻纳甲
│   ├── meihua_qigua.py         # 梅花易数
│   └── da_liuren.py            # 大六壬
├── references/                 # 知识库（按需加载）
    ├── core/                   # 核心理论（八卦/干支/五行/六亲）
    ├── router/                 # 路由决策矩阵
    ├── xiao-liuren/            # 小六壬方法
    ├── liuyao/                 # 六爻方法
    ├── meihua-yishu/           # 梅花易数方法
    ├── da-liuren/              # 大六壬方法
    └── comprehensive-divination-skill-pitfalls.md  # 故障排查
└── examples/                   # 端到端使用示例
    ├── README.md
    ├── quickstart.md           # 3 步快速开始
    ├── re-consultation-comparison.md  # 4 次复占脱敏对比
    └── international-user.md   # 海外用户示例
```

## 🧪 验证 / Verify

```bash
# 端到端验证四术都能跑
cd scripts
python -c "
import xiao_liuren, liuyao_yaogua, meihua_qigua, da_liuren, common
from datetime import datetime
n = datetime.now()
lunar = common.solar_to_lunar_date(n.year, n.month, n.day)
sn, hi = common.hour_to_shichen(n.hour)
print('小六壬:', xiao_liuren.by_month_day_hour(lunar['lunar_month'], lunar['lunar_day'], hi))
print('日干支:', common.get_day_ganzhi())
print('OK')
"
```

## 🤝 贡献 / Contributing

欢迎 PR！请阅读 [SKILL.md](SKILL.md) 了解工作流和路由规则。

PRs welcome. Read [SKILL.md](SKILL.md) for the workflow and routing rules.

## ⚠️ 免责声明 / Disclaimer

本工具仅供文化、教育、娱乐用途。占卜结果**不应**作为重大人生、财务、医疗、法律决策的唯一依据。所有结果均为传统中国宇宙观符号系统的概率性解读，**不保证**准确性、预测效力或超自然有效性。**使用风险自担。**

This tool is for cultural, educational, and entertainment purposes only. Divination results should **NOT** be used as the sole basis for important life, financial, medical, or legal decisions. All outputs are probabilistic interpretations of traditional Chinese cosmological symbolic systems with **no guarantee** of accuracy or predictive validity. **Use at your own risk.**

## 📜 License

[MIT](LICENSE) © 2026 comprehensive-divination-skill contributors

## 🔗 Links

- **标准 / Standard**: [agentskills.io](https://agentskills.io)
- **Hermes Agent**: [hermes-agent.ai](https://hermes-agent.ai)
- **Issue Tracker**: (待补 / TBD)

---

> 占卜结果仅供参考，请结合实际情况理性判断。
> Divination results are for reference only; please use rational judgment based on actual circumstances.
