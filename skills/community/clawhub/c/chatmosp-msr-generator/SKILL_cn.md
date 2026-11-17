---
name: chatmosp-msr-generator
description: |
  chatMOSP 系统的 MSR（多尺度结构重构）计算引擎。调用 mosp-for-chatMOSP/utils/msr.py
  执行金属团簇结构生成计算（基于 Wulff 构造），产出 ini.xyz 和 {task_name}_cluster.xyz，
  并自动生成 PNG 结构图和 GIF 旋转动画，最后通过飞书发送给用户。
  触发场景：parameter-builder 完成参数构建并经用户确认后，由本技能执行 MSR 计算。
---

> **🌐 Language routing / 语言路由**
> Detect the user's language from their latest message.
> - **If the user writes in English** → read `SKILL_cn.md` in this same skill
>   directory and follow it as the authoritative instructions; respond in English;
>   you do NOT need to read the rest of this Chinese document.
> - **若用户使用中文** → 继续使用本文件（`SKILL.md`）作为权威指令，并用中文回复。
> Always match the response language to the user's input language.

# chatmosp-msr-generator

## 1. 核心职责

1. 执行金属团簇结构生成计算（基于 Wulff 构造）
2. 验证输入参数完整性
3. 大尺寸团簇计算时间预警（R ≥ 50Å）
4. 生成结构文件 + 可视化图像
5. 飞书发送结果给用户

## 2. 前置条件

- ✅ parameter-builder 已完成参数构建
- ✅ 用户已通过 5 选项确认（详见 parameter-builder §参数展示格式）
- ✅ `input.json` 位于 `OUTPUT/{task_name}/input.json`
- ✅ 目标目录已由 file-organizer 创建
- ✅ 已安装外部 `mosp-for-chatMOSP`，且存在 `utils/msr.py` 和 `utils/paint.py`
- ❌ 禁止绕过 parameter-builder 手动构建参数
- ❌ 禁止跳过用户确认直接执行计算

## 3. 输入契约（input.json 必含字段）

| 字段 | 说明 |
|------|------|
| Element | 金属元素（Pd、Pt、Au 等） |
| Temperature / Pressure | 温度 / 压力 |
| Gas1_name / Gas1_pp / Gas1_S | 气体 1 名称 / 分压 / 气体熵 |
| Gas2_name / Gas2_pp / Gas2_S | 气体 2 名称 / 分压 / 气体熵 |
| Radius | 团簇半径（Å） |
| nFaces / Face1 / Face2 / Face3 | 晶面参数 |

气体熵（`Gas1_S` / `Gas2_S`）由 parameter-builder 按 §7.1 公式计算，**不要手动填写或直接复用 example 的值**。

## 4. 大尺寸团簇警告

执行前必须判断团簇半径。R ≥ 50Å 时提醒用户：

```
⚠️ 计算时间提醒：
当前团簇半径为 {R}Å，预计计算时间约 {estimated_minutes} 分钟。
（R=50Å 约 20 分钟，R=65Å 约 40 分钟）
是否继续执行 MSR 计算？
```

| 半径 | 原子数（约） | 时间（约） |
|------|--------------|------------|
| 50 Å | 11,000 | 20 分钟 |
| 65 Å | 35,000 | 40 分钟 |
| 更大 | 立方增长 | 显著延长 |

## 5. 执行步骤

### 步骤 1：执行 MSR 计算

```bash
cd mosp-for-chatMOSP
python3 utils/msr.py --json OUTPUT/{task_name}/input.json --output OUTPUT/{task_name}/
cd -
```

### 步骤 2：验证输出

```bash
ls -lh OUTPUT/{task_name}/ini.xyz
ls -lh OUTPUT/{task_name}/{task_name}_cluster.xyz
```

- ✅ `ini.xyz` 必须存在且 > 0KB，否则 MSR 失败
- ✅ `{task_name}_cluster.xyz` 必须存在（用于可视化）

### 步骤 3：生成可视化（两步分别执行）

```bash
# 静态结构图
cd mosp-for-chatMOSP && python3 utils/paint.py \
  OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --output OUTPUT/{task_name}/structure.png

# 旋转动画
cd mosp-for-chatMOSP && python3 utils/paint.py \
  OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --gif OUTPUT/{task_name}/rotation.gif
```

> `paint.py` 每次调用只能生成一种类型（PNG 或 GIF），必须分两步执行。原子数 > 20,000 时建议只生成静态图，跳过 GIF。

### 步骤 4：飞书发送给用户

```json
{
  "action": "send",
  "channel": "feishu",
  "filePath": "{workspace}/mosp-for-chatMOSP/OUTPUT/{task_name}/structure.png",
  "caption": "{金属}-{温度}K-{压强}Pa-CO{pp1}%-O2{pp2}%-R{半径}Å"
}
```

操作要求：

1. 发送 `structure.png` 给用户
2. 发送 `rotation.gif` 给用户
3. 简要描述结构特征（如"Pd 纳米颗粒呈截角八面体，主要暴露 (111) 晶面"）

## 6. 输出文件

| 文件 | 说明 |
|------|------|
| ini.xyz | 真实团簇结构（包含所有原子），KMC 计算的输入 |
| {task_name}_cluster.xyz | 表面原子已分类的绘图用结构文件 |
| faceinfo.txt | 晶面信息统计 |
| input.json | MSR 参数文件 |
| structure.png | 静态结构图 |
| rotation.gif | 旋转动画 |

## 7. 关键原则

- MSR `input.json` 不含 KMC 参数——KMC 参数由 kmc-simulator 独立准备
- `ini.xyz` 是 MSR 的**输出**，不是输入——不要为 MSR 任务准备 `ini.xyz`
- 不要直接复制 `MOSP_database` 的 example 文件——必须用 parameter-builder 重新计算气体熵

## 8. 错误处理

| 错误 | 处理 |
|------|------|
| ini.xyz 缺失或 0KB | MSR 失败，建议调整参数重试 |
| {task_name}_cluster.xyz 缺失 | 检查 MSR 日志，可能为收敛失败 |
| MSR 运行超时 | 减小团簇半径或检查参数合理性 |
| 用户中途取消 | 终止执行，保留已生成文件 |

## 9. 跨技能衔接

- **MSR → KMC**：MSR 完成后产出 `ini.xyz`。KMC 任务由 kmc-simulator 独立从 MOSP_database 取 KMC 完整参数，不复用本技能的 `input.json`。详见 kmc-simulator。
- **MSR 失败 → parameter-builder**：参数问题回到 parameter-builder 调整。
- **重复执行 MSR**：如目录已存在，询问用户是否覆盖。

## 10. 依赖

- **mosp-for-chatMOSP** — MSR 计算引擎（已克隆）
- **chatmosp-parameter-builder** — 参数构建与气体熵计算
- **chatmosp-file-organizer** — 目录结构
- **chatmosp-input-coordinator** — 任务入口

## 11. 文件结构

```
chatmosp-msr-generator/
├── SKILL.md       # 本文件（中文）
└── SKILL_cn.md    # 英文版
```

## 12. 示例

```
用户: 计算 Pt 纳米颗粒在 500K 下的团簇结构

系统: [识别为 MSR 任务 → parameter-builder 查参数 → 展示 5 选项确认 →
      用户选确认 → 检查 R=20Å 不需警告 → 调 msr.py → 验证输出 →
      生成 PNG+GIF → 飞书发送]
```
## ChatMOSP 配套技能

本技能属于 ChatMOSP 技能组。完整功能需要在 ClawHub 中安装以下配套技能：

- chatmosp-input-coordinator
- chatmosp-parameter-builder
- chatmosp-msr-generator
- chatmosp-kmc-simulator
- chatmosp-literature-search
- chatmosp-file-organizer

如果缺少必要的配套技能，请先提示用户从 ClawHub 安装缺失的 ChatMOSP 技能后再继续。GitHub 仓库只作为备用安装方式。
