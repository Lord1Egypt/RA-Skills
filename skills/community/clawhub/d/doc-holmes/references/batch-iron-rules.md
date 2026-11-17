# 批量工程铁律（doc-holmes runner）

> 每条铁律都有对应用例（tests/test_runner.py），改 runner 必须全绿。

## 八条铁律

1. **realpath 归一**：所有输入/输出路径 `os.path.realpath()` 后比较与存储；黑名单匹配不受符号链接与相对路径干扰。
2. **排除目录**：`os.walk` 显式剔除 `_duplicates/ _non_pdf_assets/ __pycache__/ .git/ output/ _translated/ .venv/ node_modules/`——历史事故：把 `_duplicates` 里的旧副本一起翻了，白烧 3 小时端点配额。
3. **set 化**：黑名单、完成表一律 `set`（sha256 为 key）；列表 `in` 在千级文件上是 O(n²)。
4. **默认单进程**：`--workers N` 显式开启且 N≤4（engine 是子进程，并发过高 OOM/限流双风险；Docling 每进程 ~3GB 的教训）。
5. **每文件超时**：默认 `min(max(180, 15s×页数), 600)`；`subprocess.run(timeout=)` 到点 kill，绝不挂死批次。卡死文件进审计 `status=timeout`，批次继续。
6. **watchdog 停滞监测**：30s 一拍跟踪最近完成时刻，停滞 >300s 记入审计与报告（per-file 超时负责杀进程，watchdog 负责让停滞可见）。
7. **断点续传**：`audit.jsonl` 重放，`status=success` 且产物文件仍在 → skip。中断/Ctrl-C/崩溃后直接重跑同一条命令即可。
8. **编译门**：`python -m compileall src` 进测试链（`test_rule_8_compileall_source`），语法错误挡在发布前。

> **回滚语义**（不属于八条编号，属审计行为）：每个文件使用独立输出子目录 `outdir/<sha256[:12]>/`，失败/超时当场删除该目录内本次产生的残缺产物——并发互不波及、绝不跨文件误删（评审 P0-2 回归锁：`test_discovery_exact_stem_boundary`）。
> **C 级语义**：批量通路不自动 OCR，tier C 显式 skip（reason=tier_C_needs_ocr）；OCR 是单文件 `translate --ocr auto` 的显式决策。

## 审计格式

- 单文件：`<stem>.audit.json`（triage 全量 + 引擎结果（密钥脱敏）+ OCR 统计）。
- 批量：`audit.jsonl` 逐行一条：

```json
{"path": "papers/a.pdf", "sha256": "…", "tier": "B", "status": "success",
 "duration_s": 41.2, "dual_path": "…dual.pdf", "mono_path": "…mono.pdf",
 "chars_per_page": 2318.4, "triage_reasons": ["…"],
 "repair": {"pages": 8, "spans_duplicated": 3, "chars_duplicated": 210,
            "examples": ["…"]}, "error": null}
```

- `status ∈ success / failed / timeout / skipped`；failed/timeout 的残缺产物**当场回滚**（不留半成品）。
- 同内容 PDF（sha256 相同）按同一文件处理：续传时自动跳过副本，属刻意去重。

## 报告

`report.md` 逐文件状态表 + 末行「汇总: 总计/成功/失败/超时/跳过」——验收链 grep 依赖这一行（无「汇总」即视为批次无效）。
