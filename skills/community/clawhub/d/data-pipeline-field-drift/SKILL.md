---
name: data-pipeline-field-drift
slug: data-pipeline-field-drift
displayName: 数据流水线字段名漂移排查
version: 1.0.0
visibility: public
category: dev-programming
subCategories: [dev-debug, dev-data]
description: 当数据流水线里某个字段「一直读不到」、某类条目静默消失、或下游把「有数据」当成「没数据」时，用契约名比对法定位字段名漂移（同一逻辑字段在采集/暂存/落盘/读取四处各有一个名字），并写「契约名回归测试」钉死。含 grep 排查模板、死变量识别、回填对账顺序。当用户说「这个字段怎么一直是空的」「数据明明有却读不到」「回填没效果」「某类记录莫名不见了」时使用。
agent_created: true
---

# 数据流水线字段名漂移排查

## 什么时候用

出现下面任一症状，先怀疑字段名漂移，**不要**先去怀疑数据源或解析器：

- 某字段在库里「一直是空的 / 一直是待补」，但数据源明明返回了
- 下游按某个字段做量级/等级判断，结果把「有大数字」的条目当成「没有数据」
- 回填脚本跑完显示「N 条已更新」，但目标字段还是空的
- 某类记录静默消失（不报错、不进异常日志）

**漂移 bug 的共同特征：不报错。** 因此它比解析失败更难发现 —— 表现是「今天没采到东西」而不是「今天崩了」。

## 第一步：把所有引用点摊开比对（核心动作）

按**逻辑字段名**（人话，比如「近 30 天收入」）在整仓搜，不要按你猜的键名搜：

```bash
# 1) 契约声明在哪（数据 schema / 字段清单文档）
grep -rn "字段中文名\|last_30d_revenue" docs/ data/sources.json README.md

# 2) 谁在写、谁在读、谁只是路过
grep -rn "last_30d_revenue\|revenue_last30d\|last30Days\|last30\b" \
  --include="*.py" --include="*.js" --include="*.json" --include="*.md" . \
  | grep -v "__pycache__\|node_modules\|/.git/\|dist/\|public/"

# 3) 落盘数据里实际存在哪些键（最硬的证据）
python -c "
import json,collections
d=json.load(open('data/xxx.json',encoding='utf-8'))
c=collections.Counter()
for r in (d if isinstance(d,list) else d.values()):
    for k in (r.get('metrics') or {}): c[k]+=1
print(dict(c))
"
```

第 3 条最关键：**如果某个键在落盘数据里出现次数为 0，那它在读取侧就是死代码**，无论代码写得多对。

典型的三套命名（实测踩过）：

| 位置 | 键名 |
|---|---|
| 契约文档（`sources.json` / schema） | `last_30d_revenue` |
| 采集内部暂存（`_api` / 原始响应转发） | `revenue_last30d` |
| 落盘（`metrics`） | **一个都没写** |
| 读取（下游评分/初筛） | `last_30d_revenue` ← 永远读不到 |

## 第二步：找「读出来但没写入」的死变量

这是最隐蔽的一种。表现是变量**声明并赋值了**，但从没进入输出：

```python
last30 = rev.get("last30Days") or 0     # 读出来了
total  = rev.get("total") or 0

if mrr and not m.get("mrr"):
    m["mrr"] = mrr                      # 写入了
if total and not m.get("all_time"):
    m["all_time"] = total               # 写入了
# ... last30 再也没出现过 —— 死变量，静默丢数
```

排查手法：把赋值过的局部变量名丢进 grep，看它是否只出现一次（定义那一次）。只出现一次 = 死变量。

```bash
grep -n "last30" script.py     # 期望看到「定义 + 至少一次使用」
```

## 第三步：修法（三条铁律）

1. **以契约文件为唯一真名。** 向内落盘（写进 `metrics` / 数据库列）一律用契约名；采集层的内部暂存（原样转发的响应）可以保留原名，但要**加注释说明两者关系**，否则下一个人还会踩。
2. **口径照实写。** 如果新字段的量级与既有字段差很多（实测有 36 倍差），文案里必须区分，别把「月流水」写成「MRR」。同时把口径写进该记录的 `metric_note` / 字段说明。
3. **只补空，不覆盖。** 回填脚本要幂等：`if val and not m.get(key)`。跑第二遍必须是「0 条更新」。

## 第四步：用「契约名回归测试」钉死

普通单测测「有没有写」，**不够** —— 键名再漂移一次，同样的故障会重演。要测三件事：

```python
CONTRACT_KEY = "last_30d_revenue"      # 改这个字符串等于改契约，要一起动

class WritesField(unittest.TestCase):
    def test_键名是契约名(self):
        B.merge_record(r, rich)
        self.assertIn(CONTRACT_KEY, r["metrics"])
        self.assertNotIn("revenue_last30d", r["metrics"],
                         "又用回采集内部暂存名了 —— 下游会读不到")

    def test_下游能读到(self):
        # 端到端：写入方写进去的键，读取方必须真的取得出值
        B.merge_record(r, rich)
        self.assertEqual(Downstream.revenue_of(r), 79596.73)

    def test_幂等(self):
        B.merge_record(r, rich); first, _ = B.merge_record(r, rich)
        self.assertFalse(first)

class RealData(unittest.TestCase):
    def test_存量数据里没有漂移键名(self):
        # 扫全库落盘数据，出现非契约键名即失败
        ...
```

**最后一条最值得写**：它是唯一能在数据层面拦住漂移的断言。

## 第五步：验证顺序（别跳步）

1. 先跑纯函数单测（离线、秒级）
2. 再跑回填/修复脚本的 `--dry-run` 看会改什么
3. 确认后正式跑（要备份：`cp data/x.json _backup/x.json.bak-$(date +%Y%m%d-%H%M%S)`）
4. **对账**：改了多少条、目标字段覆盖从几变成几、下游分布是否真的收敛了
5. 最后跑全量测试 + 重建派生产物（静态站 / 打包产物）

## 坑

- **回填脚本走逐条详情页兜底时很慢**（每条 `sleep` + 网络），全量可能 6 分钟以上，会撞前台超时 → 放后台跑，输出重定向到日志文件（注意 Python 重定向时 stdout 有缓冲，日志会长时间为空，属正常）。
- **别在自测运行时做构建**。自测脚本常会「备份→临时改数据→还原」，期间构建会把中间态写进产物；读数据做统计也会得到错数（实测出现过候选池 31/33/34 三个数）。
- 顺带确认派生产物是否**该包含**这份数据（比如未核实的原始队列通常不该进对外发布的那一份）。默认输出目录常是「本地预览版」，对外版另有开关。
