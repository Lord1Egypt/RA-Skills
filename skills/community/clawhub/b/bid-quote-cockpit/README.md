# 投标报价对比分析驾驶舱（bid-quote-cockpit）

一个**配置驱动、无项目信息**的投标报价分析看板技能。把「一堆供应商报价表」变成
「一份可决策、可发布、可复用的交互式 HTML 看板」，支持多轮回标、分部分项横向对比、
单方造价、异常报价核查、勾稽校验、评委打分固化、综合评分、定标建议、行动清单。

**不含任何真实门店 / 公司 / 供应商 / 评委名称** —— 换项目、换供应商、换货币、换分项结构、
换评委，都只改配置 JSON，不改代码。

---

## 一、安装

把 `bid-quote-cockpit` 整个文件夹放到技能目录下：

| 平台 | 技能目录 |
|---|---|
| Windows | `C:\Users\<你的用户名>\.workbuddy\skills\` |
| macOS / Linux | `~/.workbuddy/skills/` |

放好后目录结构应为：

```
~/.workbuddy/skills/bid-quote-cockpit/
├── SKILL.md              ← 技能主文档（先读这个）
├── CHANGELOG.md          ← 版本记录与已知边界
├── scripts/              ← 可执行脚本
├── references/           ← 契约与踩坑手册
├── examples/             ← 全套脱敏示例（可直接跑）
└── assets/echarts.min.js ← 内联用，保证产物离线自包含
```

依赖：**Python 3.9+**（纯标准库出 HTML）；`verify_dashboard.js` 需 **Node.js**；
真机校验需 **Chrome**。Excel 相关操作另需 `openpyxl`。

---

## 二、快速上手（3 步）

```bash
SK=~/.workbuddy/skills/bid-quote-cockpit

# 1. 拿到配置模板，填项目信息（门店/供应商/轮次/分项都在这里改）
cp $SK/scripts/config.example.json        ./config.json
cp $SK/examples/score_config.example.json ./score_config.json   # 有评委打分才需要

# 2. 生成看板与打分区块（有评委打分才需要第二步）
python $SK/scripts/gen_score_panel.py    --config ./score_config.json --out ./score_panel.html --report
python $SK/scripts/build_dashboard.py    --config ./config.json --score-panel ./score_panel.html --out ./报价分析看板.html

# 3. 交付前必跑校验（全部 exit 0 才可交付）
node   $SK/scripts/verify_dashboard.js   ./报价分析看板.html
python $SK/scripts/check_overflow.py     ./报价分析看板.html 1500,1280,1100
python $SK/scripts/verify_score_frozen.py ./报价分析看板.html --config ./score_config.json
```

⚠️ 评分区块**只能用 `--score-panel` 交给生成器装配**。不要事后再往 HTML 里塞 ——
产物内联的压缩版 ECharts 源码里含有 `</body>`、`<style>` 等**字符串字面量**，
按字符串找锚点会命中假锚点，把面板塞进 JS 里：文件变大、不报错、却渲染不出来。

先跑示例感受效果（无需准备数据）：

```bash
cd $SK/examples
python ../scripts/build_dashboard.py --config config.json          # 9 节 / 15 图
python ../scripts/build_dashboard.py --config config_without_history.json
python ../scripts/gen_score_panel.py --config score_config.example.json --out ./score_panel.html --report
python ../scripts/build_dashboard.py --config config.json --score-panel ./score_panel.html --out ./with_score.html
```

---

## 三、文件说明

| 文件 | 作用 |
|---|---|
| `scripts/build_dashboard.py` | 主生成器：出 9 节看板 HTML（ECharts 内联，离线自包含）；`--score-panel` 装配评分区块 |
| `scripts/gen_score_panel.py` | 评分区块生成器：评委打分**固化**成只读表 + 内联种子 |
| `scripts/verify_score_frozen.py` | 固化一致性真机校验（两个全新浏览器配置 = 两台电脑） |
| `scripts/verify_dashboard.js` | 语法门禁 + 运行时冒烟 + NaN 扫描 |
| `scripts/check_overflow.py` | 版式溢出体检（页面横滚 / 超出容器 / 被裁切） |
| `scripts/dump_rendered.py` | 渲染级「单位 ↔ 金额」配对断言 |
| `scripts/lint_py_const_leak.py` | 查 Python 常量泄漏进 JS（会静默中断渲染） |
| `scripts/normalize_quote.py` | 报价数据归一化 / 统计自检 |
| `references/data-contract.md` | `config.json` / `quotes.json` / `history.json` 字段级契约 |
| `references/score-panel-contract.md` | `score_config.json` 契约 + 有效平均算法 + 改分流程 |
| `references/publish-and-verify.md` | 上线发布与线上核验手册（含缓存 / 壳页 / 版本陷阱） |
| `references/module-spec.md` | 各节出现条件、数据源、呈现形式、易错点 |
| `references/pitfalls.md` | 全部实盘踩坑记录（判据 / 根因 / 修复） |
| `references/design-conventions.md` | 配色 / 版式 / 图表规范 |

---

## 四、核心红线（所有环节适用）

1. **只用报价文件原文数字**。禁止推算、补全、「同口径估算」。确需推算（如总价÷面积=单方）
   属**透明算术**，允许但必须在页面上标注公式。
2. **口径全程统一**：含税/不含税二选一并贯彻始终；跨项目对比一律不含税。
   原文未标税率 → 显示「待确认」，不自作主张。
3. **三态规则**：有报价+有税率=数字 ／ 有报价+无税率=待确认 ／ 无报价=暂无报价。严禁混用。
4. **名义最低价必须显式标注**：数字最低但报价不完整时加「名义·不完整」，
   并同时给出有效可比排名。反向亦然：给了整包总价 + 书面范围说明的，属有效报价，不得剥夺排名资格。
5. **中间产物 JSON 的统计字段不可直接采信**，凡零单价/条目数一类统计一律回到明细重算。
6. **多轮对比保留首轮列**，二轮在旁边新增；无二轮报价者沿用首轮价参与排名并标注。

---

## 五、评委打分为什么要「固化」

打分的原始做法是存浏览器 `localStorage`，只在**同一台电脑**有效。一旦看板要发给别人看
（云端链接 / 附件 / 嵌入），就会出事，而且**不报错**：

| 现象 | 根因 |
|---|---|
| 本地打开有分数，云端打开全空 | `file://` 与 `https://` 是不同 origin，存储互不相通 |
| 嵌入式打开存储不可用 | 第三方存储策略 → `setItem` 抛异常，被 try/catch 吞掉 |
| 别人电脑显示**另一套分数** | 探不到分 → **静默回退到静态基线**，看起来合理却是错的（最危险） |

**解法**：分数在构建期烘焙进 HTML 字节（`window.__SCORE_SEED__`），页面只读 ——
分数随字节走，任何设备打开一致。

改分流程（交付后唯一路径）：

```
改 score_config.json → 重跑 gen_score_panel.py → 带 --score-panel 重新生成看板 → 重新发布 → verify_score_frozen --online 复核
```

**脏数据处理**：缺失 / 越界 / 非整数一律**置空 + 告警**，绝不自动补齐或四舍五入 ——
宁可缺一格并留痕，不可补一个数。

---

## 六、校验脚本判读

| 输出 | 含义 |
|---|---|
| `PAGE_SCROLL` | 页面级横向滚动（**致命**） |
| `BEYOND_WRAP` | 内容超出主容器右边界（**致命**） |
| `CLIPPED` | 内容被人为高度上限裁掉，只有滚动才看得见（**致命**，典型受害行是「合计」） |
| `SCROLLABLE` | 容器内部横滚（信息项，仍可看到） |
| `ctl == 0` | 评分区块内无任何可编辑控件（固化正确） |
| `lsKeys: []` | 未写入评分类 localStorage（固化正确） |

`verify_score_frozen.py` 会用**两个全新浏览器配置**各渲染一次 —— 这等价于两台互不相通的电脑。
两次结果完全一致，才等于「换台电脑分数不变」。

⚠️ 若看板是纯价格比价版（无评分节），脚本会打印 `--` 级说明并跳过综合分断言。
**跳过 ≠ 通过**：若本应含评分节，说明选择器没指对，需检查 `render_rules.json` 的 `_selectors`。

---

## 七、发布与交付

发布前三条硬门：① 无第三方 `<img>` 外链；② 无 CDN 外链（ECharts / 前端 SDK 一律内联，
国内网络与微信内置浏览器取不到）；③ 磁盘字节数 == 生成时打印的字节数。

⚠️ **分享链接通常只是几 KB 的引导壳**（含 `__PUBLISH_BOOTSTRAP__`），真实 HTML 在
另一个静态域名下、版本号递增。线上核验必须**下载真字节**再断言，否则校的是壳页。
完整手册见 `references/publish-and-verify.md`。

交付时**只给一个最终链接**，并附核验结论。
