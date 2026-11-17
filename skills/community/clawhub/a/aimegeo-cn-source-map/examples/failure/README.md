# 失败样例与修复

这两份 JSON 故意包含错误使用决定，用于确定性回归；不作为真实研究结论。

在技能根目录运行：

```bash
python3 scripts/evidence_table.py --input examples/failure/company-as-industry.json --out-dir /tmp/cn-source-map-rejected-company
python3 scripts/evidence_table.py --input examples/failure/unverified-statistic.json --out-dir /tmp/cn-source-map-rejected-statistic
```

两条命令都应退出 `2`，不导出证据成果。首个错误是把企业功能自述标成行业需求证据；第二个错误是把未运行查证的“1.2万亿元”数字线索标成已核实事实。实际错误输出见 [expected-errors.json](expected-errors.json)。

修复时保留原论点与材料，改 `use` 为 `pending` 或 `reject`、清空 `citation_text`，填写具体 `next_step`。不要只改状态来绕过校验：能否改成 `cite` 取决于是否实际补到对应证据。修复后的待核实记录能正常导出，但数字仍不能进入可用出处段落。

对于仅有媒体转载的情况，自测另外验证：未做原文定位不得引用；只有实际尝试后才能记 `not_found`，且只允许明确归属的背景转述。无法定位原文不等于原文不存在。
