#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""config_pack.py — 一键配置包生成器（标准配置包 → 可迁到任意大模型）

用法：
  python config_pack.py gen --name 小张 --role 电商客服 --lang zh --out ./pack

说明：
- 生成标准配置包目录（对齐 31 号）：
    SOUL.md / IDENTITY.md / USER.md / memory/ / tools.json / rules.json / README.md
- 配置包模型无关：换平台 / 换模型不换人格；加密 ID 凭证可随后签发（id_verify）。
"""
import argparse, json, os, time


def gen(name, role, lang, out):
    os.makedirs(os.path.join(out, "memory"), exist_ok=True)
    ts = time.strftime("%Y-%m-%d")
    soul = f"""# SOUL.md - 我是谁

- 名字：{name}
- 角色：{role}（类人数字员工，配置生成于 {ts}）
- 语气：专业、简洁、先共情后解决；不串角色、不越权。
- 边界：高危动作需二次确认；涉密 / 越权请求一律拒绝。
"""
    ident = f"""# IDENTITY.md - 标识

- 名称：{name}
- 角色：{role}
- 语言：{lang}
- 配置包版本：1.0.0（对齐 13 号能力版本管理）
"""
    user = f"""# USER.md - 关于主人

- 主人：待填写（交付时由服务方与客户共同完善）
- 偏好：待填写
- 红线：待填写
"""
    memory = f"""# MEMORY.md - 长期记忆骨架

- 用户偏好：待沉淀（任务完成后自动写回）
- 项目事实：待沉淀
- 每日日志：见 memory/YYYY-MM-DD.md（任务完成后追加）
"""
    tools = {"name": f"{name}-tools", "version": "1.0.0", "tools": [],
             "note": "按 00 四件套·工具最小权限原则逐项增补"}
    rules = {"name": f"{name}-rules", "version": "1.0.0",
             "proactive": [{"trigger": "示例：每日9:00巡检未结工单", "action": "提醒负责人", "auth": "需授权"}],
             "high_risk_confirm": True}
    readme = f"""# {name} · 数字员工配置包

- 角色：{role} ｜ 语言：{lang} ｜ 生成：{ts}
- 组件：SOUL / IDENTITY / USER / memory / tools.json / rules.json
- 一键接入：WorkBuddy / Claude / Cursor 文件直读；Coze / Dify 平台导入（见 31 四通道对照表）
- 换模型不换人格：配置包模型无关，换平台后重跑 ai_bench 评测（16）
- 验真：向服务方索取加密 ID 凭证（id_verify / 17）
"""
    files = {"SOUL.md": soul, "IDENTITY.md": ident, "USER.md": user,
             "memory/MEMORY.md": memory, "tools.json": json.dumps(tools, ensure_ascii=False, indent=2),
             "rules.json": json.dumps(rules, ensure_ascii=False, indent=2), "README.md": readme}
    for rel, content in files.items():
        p = os.path.join(out, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"[config_pack] 已生成配置包 -> {out}")
    for rel in files:
        print("   " + rel)


def main():
    ap = argparse.ArgumentParser(description="一键配置包生成器")
    ap.add_argument("gen")
    ap.add_argument("--name", required=True)
    ap.add_argument("--role", default="数字员工")
    ap.add_argument("--lang", default="zh")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    gen(a.name, a.role, a.lang, a.out)


if __name__ == "__main__":
    main()
