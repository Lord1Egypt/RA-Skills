# 安装说明（给 AI 执行）

> **出品**：范工AI实战 ｜ **抖音号：80823565662** ｜ **许可**：CC BY-NC-SA 4.0

你收到的是一份**技能包**（壳版）。核心判定能力在**云端**，本包只含方法流程与调用方式。

```
审图Skill/
├── SKILL.md              ← 入口，先读这个（第五节是云端调用）
├── references/           ← 方法流程（8 个）
│   ├── 01-setup.md             环境自举
│   ├── 02-preparation.md       开工准备
│   ├── 03-tech-path.md         技术路径（四层读取）
│   ├── 04-five-steps.md        ★ 执行五步（核心）
│   ├── 05-self-check.md        收工自查
│   ├── 06-quality-rules.md     质量纪律 12 条
│   ├── 07-demo.md              完整示范
│   └── 08-表述规范.md          问题表述规范
├── scripts/
│   ├── ask_api.py              ★ 云端判定引擎客户端（规则/条目/五问）
│   ├── health_check.py         图纸体检
│   ├── report_check.py         报告自检
│   ├── extract_hatch_leader.py 填充+引线提取
│   └── extract_material_tags.py 跨块拼装材料标注提取
└── INSTALL.md            ← 本文件
```

## 请按以下步骤安装

1. **放到技能目录**：把整个 `审图Skill` 目录放进你的技能目录
   - WorkBuddy：`~/.workbuddy/skills/`
   - 也可以直接告诉 AI「把这个文件夹装成技能」，让它自己放
2. **保持目录结构** —— `SKILL.md` 在根下，`references/` 与 `scripts/` 同级
3. **填授权码（必做，只有一个变量）**

   **Windows · 命令行（CMD）**
   ```bat
   set DRAWING_REVIEW_KEY=skfg-你的授权码
   ```

   **Windows · PowerShell**
   ```powershell
   $env:DRAWING_REVIEW_KEY="skfg-你的授权码"
   ```

   **Mac / Linux**
   ```bash
   export DRAWING_REVIEW_KEY="skfg-你的授权码"
   ```

   > 服务地址已内置，**不用配**。
   > 想让 AI 每次都自动带上，可以把上面那行写进系统环境变量，或者直接告诉 AI：
   > 「把 DRAWING_REVIEW_KEY 设为 skfg-你的授权码，然后用审图技能帮我审图」。

4. **自检连通**：
   ```bash
   python scripts/ask_api.py --health        # 应返回 ok:true
   python scripts/ask_api.py --rules --ids R14     # 能返回规则说明 = 授权码有效
   ```
   - 返回 `ok:true` 但 `--rules` 报 402 → **授权码不对或过期**
   - 连不上 → 检查网络，或让 AI 直接读 `references/00-索引.md`

5. **开始用**：直接说「帮我审这套图」，AI 会按云端方法库逐步执行。

## 授权码说明

- 一个授权码对应一个人，**请勿转给他人**（转出去无法追溯）
- 有效期写在码里（例：`skfg-202704-...` = 2027 年 4 月底到期）
- 到期后向作者申请新码即可
- 没有授权码时：**环境自检、图纸体检、报告模板这些本地能力照常可用**，只是调不了云端判定

## 付费说明（壳版）

- **判定规则库（19 条）+ 条目库（1,571 条）+ 方法库（5 主题 44 段）在云端**，按需调用
- 授权码无效 → 返回 **402 Payment-Needed**
- 价格见 SkillHub 页面；测试期联系作者领 Key

## 使用纪律

- 不要改写 SKILL.md
- 不要一次读完所有 references
- 用户说「审图」类需求 → 先读 SKILL.md，再按索引走
- **出报告前必须调 `ask_api.py --review` 过一遍五问**

---

*范工AI实战 · 抖音号 80823565662*
