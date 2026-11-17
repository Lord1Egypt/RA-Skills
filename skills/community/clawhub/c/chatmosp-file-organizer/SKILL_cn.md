---
name: chatmosp-file-organizer
description: |
  chatMOSP 系统的文件系统管理器。负责 MSR / KMC 任务的目录结构创建、智能命名（按
  金属_气体分压_温度K_压强Pa_R尺寸 格式）、安全文件操作（路径遍历防护、白名单限制）。
  触发场景：parameter-builder 完成参数构建并经用户确认后，创建任务目录；
  或 KMC 任务需要在 MSR 目录下创建子目录时。
---

> **🌐 Language routing / 语言路由**
> Detect the user's language from their latest message.
> - **If the user writes in English** → read `SKILL_cn.md` in this same skill
>   directory and follow it as the authoritative instructions; respond in English;
>   you do NOT need to read the rest of this Chinese document.
> - **若用户使用中文** → 继续使用本文件（`SKILL.md`）作为权威指令，并用中文回复。
> Always match the response language to the user's input language.

# chatmosp-file-organizer

## 1. 核心职责

1. **智能任务命名**：按 MSR / KMC 不同格式生成任务名
2. **标准目录创建**：MSR 和 KMC 的标准目录结构
3. **路径逻辑管理**：直接 KMC vs 接续 KMC 两种模式
4. **安全文件操作**：路径遍历防护 + 白名单限制

## 2. 安全第一原则

- ✅ 路径遍历防护：自动清理 `../`、`//`、`~` 等危险字符
- ✅ 白名单路径：所有操作限制在 `mosp-for-chatMOSP/OUTPUT/`
- ✅ TaskNameValidator：验证任务名合法性，支持新命名格式
- ✅ 权限检查：确保有适当读写权限

禁止模式：`..`、`//`、`~`、`/root`、`/etc`、`*.exe`、`*.sh`

允许字符：`a-zA-Z0-9_-.Å`

最大路径长度：512

## 3. 任务命名规则

### 3.1 MSR 任务

**格式**：`{金属}_{气体分压}_{温度}K_{压强}Pa_R{尺寸}`

**示例**：`Pd_CO9_O18_473K_101325Pa_R50`

| 字段 | 规则 | 默认值 |
|------|------|--------|
| 金属 | Pd、Pt、Au 等元素符号 | 必填 |
| 气体分压 | 多气体用 `_` 连接，分压跟在气体后（CO9 表示 CO 9%） | 必填 |
| 温度 | 数值 + K | 500 |
| 压强 | 数值 + Pa | 101325 |
| 尺寸 | R + 数值（Å） | 20 |

### 3.2 KMC 任务

**⚠️ 重要**：KMC 任务目录必须在对应 MSR 任务目录下创建子目录。

**推荐格式**：`KMC_{步数}steps`（简洁，温度/压强等信息已在 MSR 目录名中）

**备选格式**：`KMC_{温度}K_{压强}Pa_{步数}steps`

**示例**：
- 简化：`KMC_5000000steps`
- 详细：`KMC_473K_101325Pa_5000000steps`

## 4. 目录结构

### 4.1 MSR 任务目录

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
├── faceinfo.txt            # 晶面信息
├── ini.xyz                 # 真实团簇（KMC 输入）
├── {task_name}_cluster.xyz # 绘图用结构文件
├── rotation.gif            # 旋转动画
├── structure.png           # 结构图
├── parameter_analysis.md   # 参数分析文档
├── paint.py                # 绘图脚本
├── input.json              # MSR 参数文件
└── metadata.json           # 任务元数据
```

### 4.2 KMC 任务目录（必须在 MSR 目录下）

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
└── KMC_{步数}steps/
    ├── input.json          # KMC 参数（必填）
    ├── ini.xyz             # 从 MSR 复制
    ├── coverage.csv        # 覆盖度数据
    ├── coverage.png        # 覆盖度 vs 时间
    ├── coverage_steps.png  # 覆盖度 vs 步数
    ├── run.log             # 运行日志
    ├── site_tof.csv        # 位点 TOF
    ├── tof.csv             # TOF 数据
    ├── tof.png             # TOF vs 时间
    ├── tof_time.png        # TOF vs 步数
    ├── INPUT/              # KMC 自动填充
    │   ├── events.txt
    │   ├── input.txt
    │   ├── LI.txt
    │   ├── products.txt
    │   └── species.txt
    └── OUTPUT/             # KMC 自动输出
        ├── rec_cov.data
        ├── rec_event.data
        └── rec_site_spc.data
```

## 5. 路径逻辑

### 5.1 MSR 任务路径

- 位置：`mosp-for-chatMOSP/OUTPUT/{msr_task_name}/`
- MSR 生成 `ini.xyz` 和 `{task_name}_cluster.xyz`
- **不要**为 MSR 准备 `ini.xyz`（MSR 会生成）

### 5.2 KMC 任务路径（两种模式）

**模式 1：直接 KMC**（无对应 MSR，从 MOSP_database 复制结构）

- 位置：`mosp-for-chatMOSP/OUTPUT/{kmc_task_name}/`
- 适用：没有对应 MSR 结果时

**模式 2：接续 KMC**（使用 MSR 生成的 ini.xyz，**推荐**）

- 位置：`mosp-for-chatMOSP/OUTPUT/{msr_task_name}/{kmc_task_name}/`
- 适用：已有 MSR 结果时

**优先使用模式 2**，确保 MSR 与 KMC 团簇一致性。

## 6. 可视化命令（MSR 用）

```bash
# 静态结构图
python3 utils/paint.py OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --output OUTPUT/{task_name}/structure.png

# 旋转动画
python3 utils/paint.py OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --gif OUTPUT/{task_name}/rotation.gif
```

详见 msr-generator §5.3。

## 7. 接口示例

### 创建 MSR 目录

**输入**：

```json
{
  "action": "create_msr_directory",
  "parameters": {
    "metal": "Pd",
    "temperature": "473",
    "gases": ["CO", "O2"],
    "partial_pressures": {"CO": 9, "O2": 18},
    "pressure": "101325",
    "radius": "50"
  }
}
```

**输出**：

```json
{
  "success": true,
  "task_type": "MSR",
  "task_name": "Pd_CO9_O18_473K_101325Pa_R50",
  "directory_path": "mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_R50",
  "standard_files": [
    "faceinfo.txt", "ini.xyz", "{task_name}_cluster.xyz",
    "rotation.gif", "structure.png", "parameter_analysis.md",
    "paint.py", "input.json", "metadata.json"
  ]
}
```

### 创建 KMC 目录

**输入**：

```json
{
  "action": "create_kmc_directory",
  "parameters": {
    "metal": "Pd",
    "temperature": "473",
    "gases": ["CO", "O2"],
    "partial_pressures": {"CO": 9, "O2": 18},
    "pressure": "101325",
    "steps": "200000000",
    "parent_msr_task": null
  }
}
```

**输出**：

```json
{
  "success": true,
  "task_type": "KMC",
  "task_name": "Pd_CO9_O18_473K_101325Pa_200000000steps",
  "directory_path": "mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_200000000steps",
  "required_files": ["input.json", "ini.xyz"],
  "empty_directories": ["INPUT", "OUTPUT"],
  "output_files": ["coverage.csv", "coverage.png", "coverage_steps.png", "run.log", "site_tof.csv", "tof.csv", "tof.png", "tof_time.png"]
}
```

## 8. 错误处理

| 错误 | 处理 |
|------|------|
| 路径遍历攻击（../） | 拒绝操作，返回错误 |
| 任务名非法字符 | TaskNameValidator 拒绝 |
| 目录已存在 | 询问是否覆盖 |
| 权限不足 | 提示用户检查权限 |
| 路径超出白名单 | 拒绝操作 |

## 9. 跨技能衔接

- **parameter-builder → 本技能**：参数确认后调用创建目录
- **本技能 → msr-generator**：MSR 目录创建后调用计算
- **本技能 → kmc-simulator**：KMC 目录创建后调用模拟
- **msr-generator → 本技能**：MSR 完成后 KMC 任务调用本技能创建 KMC 子目录

## 10. 依赖

- **chatmosp-parameter-builder** — 获取任务参数
- **chatmosp-input-coordinator** — 获取任务类型
- **chatmosp-msr-generator** — MSR 计算接收方
- **chatmosp-kmc-simulator** — KMC 模拟接收方

## 11. 文件结构

```
chatmosp-file-organizer/
├── SKILL.md       # 本文件（中文）
└── SKILL_cn.md    # 英文版
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
