# domain-navigator（Hermes skill 形态）

《领域领航员》的 Hermes 形态：把 WorkBuddy 专家提示词（`workbuddy/domain-navigator/agents/domain-navigator.md`）与 `domain-learning` 技能合并为**一个自包含的 Hermes Skill**，去掉了 WorkBuddy 专属清单、路径与表述。

与 WorkBuddy 专家形态共用同一份产品定义；领域地图模板、覆盖度进度、待核验项与 AI 接口段全部保留。

## 布局

```text
SKILL.md                 合并后的完整技能（开始 / 制图 / 陪学 / 证据核验 / 完成态 / 交付续接 / AI 接口段）
references/地图模板.md    《⟨领域⟩地图》10 项模板（与 WorkBuddy 包内模板逐字节一致，验证器防漂移）
```

评测用例不在本目录复制——权威来源是 `workbuddy/domain-navigator/evaluations/cases.json`，由验证器直接引用。

## 发布前验证

```bash
python3 scripts/verify_hermes_skill.py   # 结构 + 泄漏 + 模板 + 18 条评测用例措辞守护
python3 -m unittest discover -s tests    # 全部测试（含本验证器的破坏检测）
```

验证器把每条评测用例映射为一组「让该用例期望行为成立的必备措辞」（`scripts/verify_hermes_skill.py` 的 `CASE_GUARDS`）；合并或改写 SKILL.md 时丢掉这些措辞即构建失败。新增评测用例必须同步映射，否则同样失败。

## 安装到本机 Hermes

把 `hermes/domain-navigator/` 整个目录复制（或软链）到 `~/.hermes/skills/` 下即可，例如：

```bash
ln -s ~/coding/map-domain-experts/hermes/domain-navigator ~/.hermes/skills/domain-navigator
```

## 双形态纪律

本产品是双形态产品（WorkBuddy 专家 + Hermes skill）。核心能力（模板、节奏、完成态标准、证据规则）变化时两个形态要一起改、一起发，模板以 WorkBuddy 包内 `skills/domain-learning/references/地图模板.md` 为权威副本，验证器会拒绝单边漂移。
