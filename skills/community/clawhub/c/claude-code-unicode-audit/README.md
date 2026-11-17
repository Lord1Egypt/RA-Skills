# Claude Code 中国用户“标记”扫描器

> 中文名：Claude给中国用户的“标记”扫描器
> 作者：wuwenbin-bj-st-01 ｜ 版本：1.0.1 ｜ 协议：MIT

Claude Code（Anthropic 的 AI 编程工具）曾针对中国用户注入一段**对人类肉眼不可见**的“标记”。本工具用于检查本机安装的 Claude Code 二进制，判断是否含有向系统提示词 `Today's date is` 注入近不可见 Unicode 撇号/分隔符的“隐写标记”代码，并在受影响时升级到干净版本。

## 背景

Claude Code v2.1.193–v2.1.196 曾在系统提示词的日期行里做隐写：当时区为 `Asia/Shanghai` 或 `Asia/Urumqi`（和/或代理/中转域名命中一份 XOR 加密清单）时，把 `Today's date is` 里的撇号替换成近不可见的 Unicode 变体（U+2019 / U+02BC / U+02B9），并把日期分隔符 `-` 换成 `/`，以此让服务端静默识别“中国/代理用户”。该行为已在 v2.1.197 回滚。

## 受影响版本

| 状态 | 版本 |
|---|---|
| 受影响 | 2.1.193, 2.1.194, 2.1.195, 2.1.196 |
| 干净（已回滚）| ≥ 2.1.197（latest 已含修复）|

## 使用方法

### 审计本机 Claude Code
```bash
python3 scripts/audit_cc_date_prompt.py
# 加 --json 输出机器可读结果
# 退出码：0 = 干净，2 = 受影响/可疑
```

### 受影响时升级到干净版本（需先确认）
```bash
python3 scripts/upgrade_cc.py --apply
# 默认 dry-run；--apply 才执行 npm install -g @anthropic-ai/claude-code@latest 并复检
```

## 工作原理

审计目标直接指向**二进制本身**（隐写逻辑编译在 `claude.exe` 内，运行时提示词不易 dump）。关键检测特征：

- 时区判定 `Asia/Shanghai` + `Asia/Urumqi`
- 变量撇号模板 `Today${...}s date is`
- XOR(密钥 91) 域名/实验室关键词清单解码（`Kup=91` / `r^91` / `endsWith("."+r)`）
- 标记码点 U+2019 / U+02BC / U+02B9

详见 `references/known_versions.md`。

## 注意事项

- 升级会改动全局 npm 包，属外部副作用，**必须先取得用户明确同意**再 `--apply`。
- 不要手动 patch 二进制（脆弱、易破坏、升级即覆盖）。
