# 第三方来源与权利声明（THIRD-PARTY NOTICES）

> 本文件列出 `bazi-engine` 仓库中**非作者原创**内容的来源、许可与使用边界。
> 目的：① 履行上游 MIT 许可的"保留版权声明"义务；② 明确**哪些内容不得转授商业许可**。
> 维护约定：新增/移除任何第三方来源内容时，必须同步更新本文件。

最后更新：2026-10-11

---

## 1. 开源社区项目

### 1.1 jinchenma94/bazi-skill

| 项 | 内容 |
|---|---|
| 仓库 | https://github.com/jinchenma94/bazi-skill |
| 许可 | **MIT License**（GitHub API `license.spdx_id = MIT`） |
| 版权 | `Copyright (c) 2025 jinchenma94` |
| 本项目使用方式 | 排盘静态查表数据与部分规则整理的**参考来源**（见 `kb/README.md` 数据来源说明） |
| 义务 | 保留上述版权声明与 MIT 许可全文；MIT 允许商用与再许可 |
| 影响范围 | `kb/01-basics/`（干支/纳音/时辰/神煞等查表类数据）及部分规则条目 |

> MIT 许可全文见 <https://opensource.org/licenses/MIT>。

### 1.2 dshxliuyu-lang/bazimbtifenxi.skill ⚠️ 权利链不完整

| 项 | 内容 |
|---|---|
| 仓库 | https://github.com/dshxliuyu-lang/bazimbtifenxi.skill |
| 许可 | **无许可证声明**（GitHub API `license = null`）→ 依默认规则"保留一切权利" |
| 本项目使用方式 | `kb/README.md` 曾将其列为数据来源之一（`kb/02-rules/bazi-mbti.md` 与本项目的早期整理存在主题重叠） |
| 结论 | **作者无权就该项目的表达性内容对外转授许可**，也不得将其纳入商业授权交付包 |
| 处置 | ① `kb/02-rules/bazi-mbti.md` **已整体重写为本项目原创版本**，并从发布包与商业交付包中排除（见 `tools/build_release_zip.py` 的 `EXCLUDE_SUB`）；② `kb/01-basics/najin.md` 早期版本曾在第三方整理件基础上形成，已于 2026-10 **整体重写**（现版本的结构编排、文字表述与解读均为本项目原创）；③ 两者均与 `kb/04-rules-db/rules.json` 无关（断语库 1000 条中无该来源条目）；④ `kb/README.md` 已移除对本项目的来源引用；⑤ 历史版本处置见 §6 |
| 影响范围 | 不进入交付包、不构成可授权标的 |

---

## 2. 古籍原文（公有领域）

《三命通会》《渊海子平》《滴天髓》《子平真诠》《穷通宝鉴》《黄帝内经》等经典原文**属公有领域**，
任何人可自由引用。本项目的贡献在于**汇编、摘录、结构化与条件化编译**，而非原文本身。

- 目录：`kb/03-classics/`（含由 docx 提取整理的全文梳理件）
- 说明：`rules.json` 每条规则的 `source` 字段标注古籍出处，属引用与溯源，不主张对原文的权利。
- **引用溯源说明**：`kb/03-classics/shigan-lun.md` 中标注【原文】的段落均为上述**公有领域原文**的引用；
  内部取材阶段曾参考第三方整理的 docx 全文（`qiongtong-baojian.md` 等 6 件），但该整理件**不随发布/商业交付包分发**（见 §4），
  交付内容为原文引用 + 本项目原创的编排、取舍与解读，不包含第三方整理者的表达性内容。

---

## 3. 地理坐标数据（`engine/engine.dist.js` 内 `CITY_LON`）

| 数据 | 来源 | 说明 |
|---|---|---|
| 行政区划名单 | modood 行政区划项目 | 仅用于确定城市名称集合 |
| 经纬度坐标 | GeoNames | CC BY 4.0（署名要求）；本项目以数值形式内联使用 |
| 县改市旧址经度 | 公开资料整理 | 少数县级市 |
| 少量常识补录 | 公开地理常识 | 已逐项人工复核 |

> 该表仅提供"真太阳时经度校正"的近似值（精度目标 <0.3°，约 1.2 分钟），不用于任何测绘用途。
> 若未来将 `CITY_LON` 单独作为数据产品对外授权，需单独核实并标注 GeoNames 的 CC BY 署名。

---

## 4. 明确排除在商业授权交付包之外的内容

以下内容**不随商业授权交付**，理由见上：

1. `kb/02-rules/bazi-mbti.md`（来源为微信公众号/百家号文章，无作者、无 URL、无授权）
2. `kb/03-classics/` 中的 docx 提取件（古籍原文属公有领域，转售无标的价值，且来源为第三方整理）。
   **具体为 6 个文件**：`bazi-wuxing-table.md`、`ditian-sui.md`、`qiongtong-baojian.md`、
   `sanming-tonghui.md`、`workflow-full.md`、`yuanhai-ziping.md`。
3. `HANDOFF.md`、`工作区说明.md`、`docs/`（内部文档，非交付物）
4. `assets/screenshots/`（含作者个人联系方式素材）
5. 因第 4 条，**发布包内 `README.md` 的图片链接（`assets/screenshots/contact-card.png`）会失效**；
   包内 README 的联系方式文本（微信 / 公众号）不受影响——这是已知且预期的现象，不是打包缺陷。

> **本条已由构建脚本强制执行（不是纸面声明）**：`tools/build_release_zip.py` 会读取每个 `.md` 文件头部的
> `来源：…docx` 标注，**自动排除**这类第三方整理件，并在打包后做硬校验——一旦交付包内仍存在此类文件则
> **构建失败（exit 1）**。因此 `bazi-engine-*.zip`（GitHub Release 附件与 SkillHub 上传包）与本节声明一致；
> 2026-10 风险面扫描曾发现此声明**未被执行**（旧包内含上述 6 个文件），现已修复并加门禁。


---

## 5. 作者原创部分（可对外授权）

以下为作者原创编译成果，是本项目**唯一可对外授权**的标的：

- `kb/04-rules-db/rules.json`：1000 条结构化断语（触发条件 / 结论 / 古籍出处 / 置信度 / 行动建议）
- 质检流水线（`tools/audit_hit_distribution.js`、`check_conflicts.js`、`check_dup_hits.js` 等）
- 规则条件化编译方法、`suggestion` 行动建议文案、置信度标注

> `kb/04-rules-db/rules.json` 顶层已**内嵌许可标识**（`license` / `license_url` / `copyright` / `license_note` /
> `commercial_license` / `third_party_notices`），因此该数据文件单独流转时也自带许可声明，
> 不依赖随附的 `LICENSE-DATA` 文件或平台页面上的 License 字段。

---

## 6. 历史版本作废声明（Historical versions void）

`kb/01-basics/najin.md` 与 `kb/02-rules/bazi-mbti.md` 在 2026-10 之前存在"在第三方整理件基础上形成"的版本。
两个文件已于 2026-10 **整体重写为原创表达**，重写后的版本自 commit `b2a444e`（v1.3.9）起生效。

| 文件 | 重写前的旧版本（git 历史中仍可检索到） | 重写后 |
|---|---|---|
| `kb/01-basics/najin.md` | `838538b:kb/01-basics/najin.md`（与现版差异 75 insertions / 61 deletions） | 结构编排、文字表述与解读均为本项目原创 |
| `kb/02-rules/bazi-mbti.md` | `838538b:kb/02-rules/bazi-mbti.md`（较现版多 199 行） | 223→80 行整体重写，含 MBTI 商标与使用边界声明 |

**声明**：git 历史中仍可检索到的上述旧版本内容**已作废**，未被任何当前版本、发布包或商业交付包使用；
旧版本的表达性内容不构成本项目可对外授权标的，也不应被继续引用或再分发。

> 若需从历史中彻底移除，可对该两个路径执行 `git filter-repo --path <path> --invert-paths` 重写历史
> （需强推 + 删除并重打全部 tag + 重传 Release 资产）。**截至本版本尚未执行**，属已知残留，在此明示。

---

*本文件不替代 [LICENSE](LICENSE) 与 [LICENSE-DATA](LICENSE-DATA)；如有冲突，以两者为准。*
