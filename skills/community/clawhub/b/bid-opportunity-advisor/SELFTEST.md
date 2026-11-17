# 技能自测说明（SELFTEST）

本技能自带回归夹具与一键自测，用于上线前 / 改动后验证「解析 → 合并 → 去重 → 引擎」整条链路未退化。

## 运行

从技能**根目录**执行（脚本内部按相对路径定位 demo 夹具）：

```bash
python scripts/selftest.py
```

全部通过会打印 `✅ ALL SELF-TESTS PASSED`；任一断言失败则打印 `❌ FAIL` 并非零退出。

## 覆盖点

| # | 验证项 | 依据 |
|---|--------|------|
| 1 | listing 解析 + 详情合并 | `fetch_ccgp.parse_listing` 得 3 条；`parse_detail`+`apply_detail` 正确补全 `win_company=云南新秦云科技有限公司`、`win_amount=4800000`、`budget_amount=5000000` |
| 2 | 跨源去重（合成） | `opportunity_engine.dedup_records` 对「同名+同采购人+同日期、不同来源」的重复项只计一次（移除 1 条） |
| 3 | 引擎全链路 | 全分析函数 + `html_report` 不崩溃；**含 `discount_stats` 为空时的格式化崩溃回归**（无中标样本不抛 `ValueError`） |
| 4 | 多源真实样本去重 | `demo/multisource_real.json`（20 条 ccgp 真实 + 3 条 cebpubservice 真实 + 1 条受控跨源重复）→ 移除 1 条；合并记录保留 ccgp 中标侧 `win_company`；3 条真实 ceb 项目互不误合并 |
| 5 | ceb 详情页解析（两种形态 + schema 一致） | `fetch_ceb.parse_ceb_detail` 表格形态得 `type=招标`/`buyer=中国建设银行四川省分行`/`budget_amount=11015000`/`region=四川`/`publish_date=2026-06-03`；文本形态得 `type=中标`/`win_company=武汉智联信息技术有限公司`/`win_amount=24800000`；且 `set(ceb_record.keys())==set(ccgp_record.keys())`（schema 一致，可混合喂引擎） |

## 夹具（demo/）

- `test_listing.html` — 3 条 ccgp 风格 listing（`<li>` 含标题/日期/采购人/代理/公告类型/省份）。
- `test_detail_t2.html` — 1 条中标详情（label→value 邻接表格：供应商/金额/评分）。
- `test_ceb_detail_table.html` — 1 条 ceb 表格 `<td>` 形态详情（四川大学智慧校园建设项目招标公告：招标控制价 1101.5 万元、招标人、行政区域四川、公告时间 2026-06-03）。
- `test_ceb_detail_text.html` — 1 条 ceb「标签：值」文本段落形态详情（湖北大学知行学院总承包中标结果公示：中标人、中标金额 2480 万元、公示时间 2026-07-10）。
- `test_ceb_records.json` — 上述两条 ceb 夹具的解析落盘结果（参考用）。
- `test_records.json` — 上一步解析落盘的 records（参考用）。
- `test_profile.json` — 测试用公司画像（`~/.bidprofile.json` 同 schema）。
- `multisource_real.json` — **多源真实样本**：20 条 ccgp 真实记录 + 3 条 cebpubservice 真实项目（取自公开检索）+ 1 条受控跨源重复（同一 ccgp 项目在 ceb 重发）。用于验证跨源去重在真实字段值上的表现。
- `sample_records.json` / `sample_report.html` — 早期 20 条真实样本的运行产物。

## 改了脚本后

任何对 `fetch_ccgp.py` / `fetch_ceb.py`（解析正则）或 `opportunity_engine.py`（评分/报告）的改动，都应先跑 `selftest.py` 确认绿色；若解析规则或期望值变化，同步更新本文件与对应夹具。

## 预期输出示例

```
[1] 解析 + 合并 ...
  ✅ 解析 3 条 / 合并 win_company+金额 正确
[2] 跨源去重 ...
  ✅ 跨源同名同采购人同日期 → 移除 1 条
[4] 多源真实样本去重 ...
  ✅ 20 ccgp + 3 ceb + 1跨源重复 → 移除1，字段合并保留中标人，无假合并
[5] ceb 详情页解析（两种形态 + schema 一致）...
  ✅ 表格/文本两形态解析正确，schema 与 ccgp 一致（可混合喂引擎）
[3] 引擎全链路（含折扣为空回归）...
  · 有中标样本: 报告 OK（xxxx 字节）
  · 无中标样本(折扣为空): 报告 OK（xxxx 字节）
  ✅ 引擎无崩溃，报告无破损格式化

✅ ALL SELF-TESTS PASSED
```
