# 产物形态样例：`brief` 一次给全的那张简报（合成主体）

**这枚文件是什么**：下面分隔线之后那 17 行，是本包 `cue.py brief` 那一条命令的 stdout 原样——材料目录（来源编号｜类型｜日期｜页数｜解析通道｜标题）＋线索件（对象·为何现在·建议动作）＋每条可直接粘贴的逐字证据（JSON 行），一行没改、一字没补。
**里面的主体、公告、页码与数字全是合成的**：出自本包已提交的合成夹具 `scripts/fixtures/omni_real_shape.json`（@cueai/omni-reader-mcp 的实测回执形制、文本为合成、编号为假），本页不含任何真实机构、个人或真披露。
**怎么复跑**（纯标准库；临时根用 `mktemp -d` 现取一枚唯一名，同机多会话也不互撞，**取不到就当场停手、不带空路径往下跑**，跑完自己删）：

```bash
RUN="$(mktemp -d "${TMPDIR:-/tmp}/cue-lead-pieces-sample-XXXXXX")" || { echo "取不到临时根，停手"; exit 1; }
test -n "$RUN" && test -d "$RUN" || { echo "临时根空或不在，停手"; exit 1; }
export RUN
python3 -B - <<'PY'
import json, os, pathlib
fx = json.loads(pathlib.Path('scripts/fixtures/omni_real_shape.json').read_text(encoding='utf-8'))
run = pathlib.Path(os.environ['RUN']); run.mkdir(parents=True, exist_ok=True)
pathlib.Path(run / 'in_full.json').write_text(json.dumps(fx['inline_tools_call']), encoding='utf-8')
PY
python3 -B scripts/cue.py ingest "$RUN/DEMO" --omni "$RUN/in_full.json" --sid ANN-1 --kind announcement \
  --date 2026-10-01 --title '关于逾期债务的公告（合成样件）' --company '合成测试主体（synthetic）' --market CN
CUE_LLM_BASE_URL='https://llm.invalid/v1' CUE_LLM_API_KEY='synthetic-token' CUE_LLM_MODEL='synthetic-model' \
  python3 -B scripts/cue.py leads "$RUN/DEMO" --no-llm
CUE_LLM_BASE_URL='https://llm.invalid/v1' CUE_LLM_API_KEY='synthetic-token' CUE_LLM_MODEL='synthetic-model' \
  python3 -B scripts/cue.py brief "$RUN/DEMO"
```

**这一趟零网络，靠的是两个条件，不是环境的运气**：`brief` 在数据目录还没有线索件缓存时，会先调一次大模型对齐——那一步只在 `CUE_LLM_BASE_URL`、`CUE_LLM_API_KEY`、`CUE_LLM_MODEL` 三枚同时在场时才发起（缺任一枚就走确定性分组、不发请求）。上面最后两条把这三枚显式设成合成值（`llm.invalid` 域，不是真端点），再带 `--no-llm` 先把缓存落盘，因此最后那条 `brief` 只读缓存：按假传输桩核过，这一趟发请求次数 0。**去掉 `--no-llm` 那条、又在你机器上留齐这三枚环境值，`brief` 首跑就会走网络那一支**——那已不是本样例的复跑形制。
**这五条各打什么**（现读逐条）：第一条取临时根（那三行：`mktemp -d` 取一枚唯一名，取不到就打印「取不到临时根，停手」并退 1，再断言它非空且在场，最后才 `export`——三步分开写，是为了让赋值不吃掉失败码），第二条铺输入件，这两条都不打字；第三条 `ingest` 打一行登记回执 `ANN-1: 3 pages (parser=omni-grounded, page_basis=pdf_page)`；第四条 `leads --no-llm` 打线索件本身 9 行；第五条 `brief` 的 stdout 就是下面那 17 行（`wc -l` 17 行、全文 698 字符含末换行、去首尾空白 697 字符，逐字对拍差异 0 行）。第三、四条打的是它们自己的进度与线索件，不属于 `brief` 的产物，所以不在下面这段里。第四条与第五条前缀那三枚合成环境值（`llm.invalid`）为的是把「带着它们也照样不发请求」这条路一起证下来。

（同一枚夹具也由包内回归测试 `scripts/test_skill_regression.py` 使用；那条测试跑完即删临时目录。真实用法里，登记走 `fetch`、解析走 Cue Omni Reader 或本地兜底——**花费之前一定先问**，本样例走的是不发请求的那条路。）

**边界**：线索件只是提示，排序与判断归人；本件不构成投资建议或信贷建议，**评级与目标价一律 `[待人工]`**——下面那条「建议动作」是核对动作（去找原文、向公司索要说明），不是买卖动作。

---

# Cue 简报：合成测试主体（synthetic）（合成测试主体（synthetic），CN）
一次给全：材料目录、线索件、可直接粘贴的逐字证据。不需要再 ls / cat sources.json / Read 原文件。

## 材料（来源编号｜类型｜日期｜页数｜解析通道｜标题）
ANN-1｜announcement｜2026-10-01｜3｜omni-grounded/PDF页｜关于逾期债务的公告（合成样件）

## 线索件（每行 JSON 证据都由程序从原文截取并已逐字核对，可原样粘贴进 answer.json 的 evidence）

### L1 诉讼
为何现在：2 条相关变化，最近一条 2026-10-01
建议动作：核对原文并向公司索要说明
{"source": "ANN-1", "page": 2, "quote": "一、新增诉讼情况公司作为被告的诉讼事项有 12 件，金额 3.40 亿元。"}  # 2026-10-01 事项
{"source": "ANN-1", "page": 2, "quote": "| 序号 | 诉讼类别 | 涉诉案件数量（件） 涉诉案件金额（亿元） |"}  # 2026-10-01 事项

## 下一步
1. 线索件证据不够时，在同一条命令里一次补查：find DIR 关键词1 关键词2 --max 30，或 page DIR 来源 页码,页码-页码 来源2 页码。
2. 一次写好 answer.json，然后运行一次 verify DIR --json answer.json --fix，修正后直接复述，不要逐句复核。
