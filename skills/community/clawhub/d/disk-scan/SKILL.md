---
name: disk-scan
description: 磁盘占用扫描 — 只读扫描目录占用：Top N 大文件 + 各子目录大小排行，快速定位空间杀手（零依赖） 适用场景：当需要磁盘占用扫描能力时使用本技能；触发词：disk-scan。
slug: disk-scan
version: 1.0.5
display_name: 磁盘占用扫描
display_name_en: Disk Usage Scan
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write
category: 效率工具
platforms: [claude, codex, cursor, windsurf, workbuddy]
copyright: SynomosAI
read_when:
  - 磁盘快满、想快速定位是谁吃掉了空间
  - 要看 Top N 大文件 + 各子目录大小排行
  - 服务器运维评估磁盘健康、清理归档旧数据
  - 用户说「哪个文件最大」「磁盘占用怎么看」「哪个目录占空间」
description_zh: "磁盘占用扫描 — 只读扫描目录占用：Top N 大文件 + 各子目录大小排行，快速定位空间杀手（零依赖）"
description_en: "Read-only disk usage scan: Top-N largest files plus per-subdirectory size ranking to locate space hogs quickly (zero-dependency)."
classification:
  skillhub: ["productivity"]
  iso_25010: ["Maintainability", "Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [disk-scan, 效率工具]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/disk_scan.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "命令行参数透传给主脚本，具体取值见各包 --help"
    required: false
output_schema:
  stdout:
    type: string
    description: "标准输出为 JSON 结果，含逐项检查与总体结论"
  exit_code:
    type: integer
    description: "0=PASS/完成；1=FAIL/有警告或待补强；2=用法或参数错误"
capabilities:
  - cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.5: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
Use it whenever you need to analyze local or remote disk space usage — in particular to hunt for unknown large files or to rank subdirectories by size. Fits the moments when the system warns that storage is running low, when old data needs archiving, or when server operations need to assess disk health. Because it is zero-dependency and strictly read-only, it can run a safe probe quickly on any system with no special network constraints.

### Usage
Invoke the script directly: `python disk_scan.py`. Use `-p <dir>` to set the scan root (defaults to the current directory). Use `--top <number>` to cap the number of largest files returned — 100 is recommended to balance speed and precision. Add `--recursive` to force traversal of deep substructures. Run `-h` for the standard help text.

### Workflow
1. Confirm the target disk path and open the matching shell or SSH session.
2. Run `python disk_scan.py -p /mnt/data -n 50 --recursive` to start the scan.
3. Watch the console log, focusing on how file sizes compare against total capacity.
4. Read the generated ranking list; extract the paths and sizes of the top-ten largest files.
5. Based on the subdirectory ranking, decide whether the space hog is a single file or a pile-up in folders.
6. Turn the findings into a cleanup plan or export a report, closing the loop on the space investigation.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.5
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
适用于需要分析本地或远程磁盘空间占用情况，特别是排查未知大文件或统计子目录大小排名的场景。当系统提示存储空间不足、需清理归档旧数据、或服务器运维中评估磁盘健康状态时使用本技能。因其零依赖且为只读模式，适合在任何没有特定网络环境限制的系统上快速执行安全探查。

### 用法
直接调用脚本命令：`python disk_scan.py`。支持参数 `-p <目录路径>` 指定扫描目标根目录，默认为当前目录；使用 `--top <数字>` 设置大文件返回数量上限，推荐设为 100 以平衡性能与精度；添加 `--recursive` 参数可强制遍历深层子结构。若需查看具体命令帮助信息，请调用 `-h` 参数获取标准配置说明。

### 流程
1. 确认目标磁盘路径并进入对应的命令行环境或 SSH 会话。
2. 执行脚本 `python disk_scan.py -p /mnt/data -n 50 --recursive` 启动扫描进程。
3. 等待控制台输出终端日志，重点关注文件占用大小与总容量对比。
4. 查看生成的排名列表，提取前十大大文件的具体路径及大小数值。
5. 根据子目录排行数据判断占用源头是单点文件还是文件夹堆积。
6. 依据分析结果规划清理策略或导出报告，完成空间排查任务闭环。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.5
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
