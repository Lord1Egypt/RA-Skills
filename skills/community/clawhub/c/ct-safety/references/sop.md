# ct-safety 操作 SOP / Operating SOP

> 适用范围：基于 FDA FAERS（openFDA）公开不良事件数据做 **disproportionality 信号检测**（PRR / ROR / IC），
> 辅助药物安全性监测；可选接入中国官方药物警戒通报（cdr-adr.org.cn）作**定性**佐证。
> 档位：B（普通输入 + 对外公开检索，零保密数据）。
> 红线：默认仅 PREVIEW；真实联网检索必须显式加 `--run`。

---

## 1. 适用场景

- 想回答「某药-事件组合是否被**过度报告**？」——用 PRR / ROR / IC 定量信号。
- 想看「该药整体**高频不良事件** top-N」——不做信号检测。
- 想用中国官方药物警戒快讯**定性佐证**一个 FAERS 信号（注意：cdr-adr 无计数，不能喂入 disproportionality）。

## 2. 前置条件

- Python 3 + `requests`（FAERS/openFDA 直连用 `requests`；**本沙箱托管 Python 若缺 `requests` 需 `pip install requests`**——这是环境缺口，非技能缺陷）。
- 联网（api.fda.gov 公开、低频、无密钥；可选 `--api-key` 提升配额）。
- **openFDA key 可选**：默认无 key 可运行（匿名配额 240 次/分、1,000 次/天）。仅在**高吞吐**（大批量个案下载、高并发 `--parallel`，>1000 请求/天）才需申请：到 https://open.fda.gov/api/register/ 免费注册（邮箱即注册、无需信用卡），再用 `--api-key`、环境变量 `OPENFDA_API_KEY` 或技能根 `.env` 提供。**切勿把 key 写进会随技能发布的文件**；打包红线见 `references/openfda_api_key.md`。
- 可选 CN-PV：联网访问 cdr-adr.org.cn 公开栏目（无 WAF、无密钥）。

## 3. 命令示例（从使用到产出）

### 3.1 看某药高频不良事件（仅 `--drug`，不做信号检测）
```bash
python scripts/ct_safety.py --drug "osimertinib" --top 10 --run --out-dir ./out
# 产出 faers_report.md：仅列 top 不良事件，无 2×2 表（自动降级，不报错）。
```

### 3.2 某药物-事件组合信号检测（加 `--event`）
```bash
python scripts/ct_safety.py --drug "osimertinib" --event "PNEUMONITIS" --run --out-dir ./out
# 产出 faers_report.md：含 ROR / PRR / IC 表 + 信号判定。
```

### 3.3 加中国官方药物警戒定性佐证
```bash
python scripts/ct_safety.py --drug "osimertinib" --event "PNEUMONITIS" \
    --with-cn-pv --drug-cn "奥希替尼" --event-cn "肺炎" --run --out-dir ./out
```

### 3.4 自定义 FAERS 药物字段
```bash
python scripts/ct_safety.py --drug "osimertinib" --event "PNEUMONITIS" \
    --field patient.drug.openfda.substance_name --run --out-dir ./out
```

## 4. 参数表

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--drug` | **必填** | 药物名（FAERS `patient.drug.medicinalproduct`） |
| `--event` | — | 不良事件 MedDRA PT；**省略则仅出高频不良事件 top-N** |
| `--field` | `patient.drug.medicinalproduct` | FAERS 药物名字段 |
| `--top` | `10` | 高频不良事件返回条数 |
| `--api-key` | — | openFDA key（提升配额） |
| `--with-cn-pv` | off | 附加中国官方药物警戒通报检索（定性） |
| `--drug-cn` | — | CN-PV 中文药名（提升召回） |
| `--event-cn` | — | CN-PV 中文事件词 |
| `--cn-terms` | — | CN-PV 额外 AND 关键词（可多个） |
| `--cn-max` | `10` | CN-PV 每栏目抽样最新文章上限 |
| `--out-dir` | `./out` | 产出目录 |
| `--run` | off | **必加**才真正联网；否则仅 PREVIEW |

## 5. 产出文件（位于 `--out-dir`）

| 文件 | 说明 |
|---|---|
| `faers_fetch.json` | FAERS 原始抓取（含 drug_total / top_events / counts） |
| `disproportionality.json` | 2×2 信号结果（仅 `--event` 时生成） |
| `faers_report.md` | **主产出**：Markdown 报告 |
| `cn_pv.json` | 中国官方药物警戒命中（仅 `--with-cn-pv`） |

## 6. 典型工作流

1. 先 `--drug X`（无 `--event`）看高频不良事件 → 锁定关注事件。
2. 再加 `--event <PT>` 做信号检测 → 看 ROR/PRR/IC 是否阳性。
3. 阳性信号 → 加 `--with-cn-pv --drug-cn --event-cn` 做中国官方定性佐证。
4. 信号仅作筛查，非因果；监管提交（DSUR/PBRER/标签）须按 GCP / ICH E2 另行评估。

## 7. 排错

| 现象 | 原因 | 处理 |
|---|---|---|
| `urllib.error.URLError` / timeout | 无网/代理 | 确认 api.fda.gov 可达；配置代理 |
| HTTP 429 | 无 key 高频调用 | 加 `--api-key`，或降低频率 |
| 仅给 `--drug` 未给 `--event` | 意图看高频事件 | **不再报错**：自动降级 top-N 报告（见 §8） |
| CN-PV HTTP 412 / WAF | nmpa.gov.cn 被拦 | 预期——仅抓 cdr-adr.org.cn，NMPA 已排除 |
| CN-PV 0 命中 | 词过窄/仅抽样最新页 | 传 `--drug-cn`+`--event-cn`；加大 `--cn-max` |
| `ModuleNotFoundError: requests` | 运行环境缺依赖 | `pip install requests`（环境缺口，非代码缺陷） |

## 8. 本次修复记录

- **无 `--event` 崩溃修复**：旧版 `run()` 在未给 `--event` 时仍调用 `disproportionality.compute(cnt["a"], …)`，
  但 `fetch_counts` 返回 `counts=None` → `TypeError` 崩溃。现 `cnt is None` 或 `event` 缺失时跳过 2×2 计算，
  改调 `_render_top_events()` 输出「高频不良事件 top-N 报告」，与 SKILL.md 承诺行为一致。已单测两种路径均正常。
