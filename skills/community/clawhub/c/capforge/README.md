# CapForge（铸能）— ClawHub Skill

**作者/品牌：Austin Liu（ausitnliu）**

本目录是用于发布到 ClawHub 的技能包（`SKILL.md` + 支持文件）。

## 快速使用

```bash
# 统一工作空间（可选）
export CAPFORGE_WORKSPACE=~/.capforge

# 导入并扫描
npx capforge import https://github.com/nousresearch/hermes-agent
npx capforge scan hermes-agent
npx capforge describe hermes-agent
```

产物默认在：

- `~/.capforge/output/capabilities/hermes-agent.md`

## 发布到 ClawHub（示例）

```bash
clawhub skill publish . \
  --slug capforge \
  --name "CapForge" \
  --version 1.0.0 \
  --tags latest \
  --changelog "Branding update (Autsin)"
```
