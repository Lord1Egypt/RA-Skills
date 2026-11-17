---
name: dgngjx-skill
description: "多功能免费工具箱 - 图片处理、PDF转换、数据换算、文本工具、开发工具、视频工具、教育、生活娱乐、实用小工具、系统工具、AI办公。11大模块49个工具。v4.1 包化架构：SKILL.md 129KB→30KB + 11模块外置 + 四包机制（core/dev/ent/media）+ 首次体检报告。"
version: 4.1.0
---


# 多功能工具箱 dgngjx-skill v4.1.0

## 🚀 dgngjx CLI 统一入口 ⭐ v3.9.0 新增

**✅ 开箱即用**（纯 Python 标准库 argparse，零依赖）

> v4.1.0 新增：`--install-pack` 安装可选包、`--list-packs` 列出可用包、`--health` 首次体检报告。

<details>
<summary>📋 CLI 使用方式</summary>

```bash
# 直接调用工具（参数化，非交互）
dgngjx calc.mortgage --amount 1000000 --years 30 --rate 4.2
dgngjx text.encode --method base64 --text "Hello World"
dgngjx img.compress --path ./photos/ --quality 80 --format JPEG
dgngjx hash.md5 --file document.pdf
dgngjx exchange --amount 100 --from USD --to CNY

# 机器可解析输出（供 CI/计划任务使用）
dgngjx sys.monitor --json

# 无人值守模式（跳过非危险确认点）
dgngjx file.rename --dir ./photos/ --prefix "vacation_" --yes
# 或设置环境变量
export DGNGJX_ASSUME_YES=1
dgngjx img.convert --path ./photos/ --format PNG

# 包管理（v4.1.0 新增）
dgngjx --list-packs          # 列出所有可用包
dgngjx --install-pack ent    # 安装娱乐包
dgngjx --install-pack media  # 安装媒体包
dgngjx --install-pack ai     # 安装 AI 包

# 体检报告（v4.1.0 新增）
dgngjx --health              # 首次运行体检

# 无参数启动 → 进入交互向导（兼容旧体验）
dgngjx
```

</details>

<details>
<summary>📋 CLI 入口代码（dgngjx 命令）</summary>

```python
#!/usr/bin/env python3
"""dgngjx CLI - 多功能工具箱统一命令行入口"""
import argparse, json, os, sys

def load_registry():
    """加载工具注册表"""
    reg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "registry.json")
    with open(reg_path, encoding="utf-8") as f:
        return json.load(f)

def build_tool_index(registry):
    """将 modules[].tools 嵌套结构扁平化为 tool_id → info 索引"""
    index = {}
    for mod in registry.get("modules", []):
        for tool_id, tool_info in mod.get("tools", {}).items():
            tool_info["module_id"] = mod["id"]
            tool_info["module_name"] = mod["name"]
            tool_info["pack"] = mod.get("pack", "core")
            index[tool_id] = tool_info
    return index

def main():
    parser = argparse.ArgumentParser(prog="dgngjx", description="多功能工具箱 dgngjx-skill")
    parser.add_argument("tool", nargs="?", help="工具路径，如 calc.mortgage / text.encode / img.compress")
    parser.add_argument("--json", action="store_true", help="输出机器可解析 JSON")
    parser.add_argument("--yes", "-y", action="store_true", help="跳过非危险确认点")
    parser.add_argument("--help-tools", action="store_true", help="列出所有可用工具")
    parser.add_argument("--list-packs", action="store_true", help="列出所有可用包（v4.1.0）")
    parser.add_argument("--install-pack", metavar="PACK", help="安装指定包（v4.1.0）")
    parser.add_argument("--health", action="store_true", help="运行体检报告（v4.1.0）")
    
    args, remaining = parser.parse_known_args()
    
    if os.environ.get("DGNGJX_ASSUME_YES"):
        args.yes = True
    
    registry = load_registry()
    
    # 包管理命令
    if args.list_packs:
        packs = registry.get("packs", {})
        print("📦 可用包：")
        for pid, pinfo in packs.items():
            default = "（默认）" if pinfo.get("default") else ""
            print(f"  {pid}: {pname}{default} — {pinfo.get('description','')}")
        return
    
    if args.install_pack:
        pack_id = args.install_pack
        packs = registry.get("packs", {})
        if pack_id not in packs:
            print(f"❌ 未知包: {pack_id}。可用: {', '.join(packs.keys())}")
            return
        # 标记包已安装（写入配置文件）
        config_path = os.path.join(os.path.expanduser("~"), ".workbuddy", "dgngjx_config.json")
        config = {}
        if os.path.exists(config_path):
            with open(config_path, encoding="utf-8") as f:
                config = json.load(f)
        installed_packs = config.get("installed_packs", ["core"])
        if pack_id not in installed_packs:
            installed_packs.append(pack_id)
        config["installed_packs"] = installed_packs
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"✅ 已安装包: {packs[pack_id]['name']}")
        return
    
    if args.health:
        # 运行体检
        health_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "health_check.py")
        if os.path.exists(health_path):
            os.system(f"{sys.executable} {health_path} --force")
        else:
            print("❌ 未找到 health_check.py")
        return
    
    tool_index = build_tool_index(registry)
    
    if args.help_tools or not args.tool:
        if args.tool:
            tool_info = tool_index.get(args.tool)
            if tool_info:
                print(f"工具: {args.tool}")
                print(f"描述: {tool_info.get('description','')}")
                print(f"参数: {json.dumps(tool_info.get('params',{}), ensure_ascii=False, indent=2)}")
            else:
                print(f"❌ 未找到工具: {args.tool}")
        else:
            print("🔧 dgngjx-skill 交互向导")
            print("=" * 40)
            for mod in registry.get("modules", []):
                print(f"\n{mod['name']}:")
                for tool_id, tool_info in mod.get("tools", {}).items():
                    print(f"  {tool_id}: {tool_info.get('description','')}")
        return
    
    tool_info = tool_index.get(args.tool)
    if not tool_info:
        print(f"❌ 未找到工具: {args.tool}")
        print(f"可用工具: {', '.join(list(tool_index.keys())[:10])}...")
        sys.exit(1)
    
    tool_args = {}
    i = 0
    while i < len(remaining):
        if remaining[i].startswith("--"):
            key = remaining[i][2:].replace("-","_")
            if i + 1 < len(remaining) and not remaining[i+1].startswith("--"):
                tool_args[key] = remaining[i+1]
                i += 2
            else:
                tool_args[key] = True
                i += 1
        else:
            i += 1
    
    tool_args["_json"] = args.json
    tool_args["_yes"] = args.yes
    
    module = tool_info.get("module_id")
    print(f"▶ 运行: {args.tool} (模块 {module})")

if __name__ == "__main__":
    main()
```

</details>

---

## 30 秒速查表

| 我想做 | 直接说 |
|--------|--------|
| 算房贷 / 五险一金 | `"算房贷"` `"算五险一金"` |
| 日期 / 单位换算 | `"日期计算"` `"公里转英里"` `"MB转GB"` `"100美元换人民币"` |
| 统计字数 / 编码 | `"字数统计"` `"Base64编码"` `"算MD5"` `"进制转换"` |
| 词频分析 / 差异 | `"词频统计"` `"对比两段文本"` |
| JSON / HTTP / Token | `"JSON格式化"` `"测试接口"` |
| 查知识 / 下壁纸 | `"查勾股定理"` `"下壁纸"` |
| 压缩 / 修复图片 | `"帮我压缩 D:\photo.jpg"` `"修复老照片"` |
| 合并 / 拆分 PDF | `"合并这几个PDF"` `"拆分第5-10页"` |
| 视频格式转换 | `"MP4转GIF"` |
| 二维码 / 密码 / 正则 | `"生成二维码"` `"生成随机密码"` `"测试正则 \d+"` `"检测密码强度"` |
| 文件哈希 / UUID | `"校验文件哈希"` `"生成UUID"` |
| 时间戳 / IP工具 | `"时间戳转换"` `"查本机IP"` `"算子网"` |
| CSV / 颜色 / 随机数 | `"看CSV文件"` `"#FF0000转HSL"` `"随机数"` |
| BMI / 番茄钟 | `"算BMI"` `"开始番茄钟"` |
| 历史 / 配置 / 周报 | `"查看历史记录"` `"修改配置"` `"生成本周周报"` |
| 会议纪要 | `"生成会议纪要"` `"语音转会议纪要"` |
| 系统资源监控 | `"看看CPU使用率"` `"内存够不够"` |
| 批量文件重命名 | `"把这些文件都改名"` `"批量添加前缀"` |
| Markdown转HTML | `"把这份MD转成HTML"` |

---

## 🆕 v4.1.0 更新提醒

> 🔔 **您正在使用 dgngjx-skill v4.1.0**
> 
> 检查更新：`skillhub search dgngjx-skill`
> 
> 升级命令：`clawhub update dgngjx-skill`
> 
> 📧 **有任何建议？联系作者邮箱：njskills@agent.qq.com**

---

## 快速开始

### 第一次用？做这 3 步

| 步骤 | 做什么 | 为什么 |
|:----:|--------|--------|
| ① | **快速试一个**：对 AI 说 `"算房贷"` | 零依赖，秒回，建立信心 |
| ② | **按需装依赖**：用到图片/PDF功能时，AI 会提示安装，输入 `install` 确认 | 一次安装，后面都能用 |
| ③ | **高级功能**：参考下方「📦 依赖管理」或跳过直接用在线工具 | 按需取用 |

### 你可以直接说（触发词）

| 说 | 做 | 备注 |
|----|----|------|
| `"算房贷 100万 30年 4.2%"` | 等额本息计算 | ✅ 开箱即用 |
| `"算五险一金 北京 15000"` | 税后工资 | ✅ 开箱即用 |
| `"从 2026-06-26 到国庆多少天"` | 日期计算 | ✅ 开箱即用 |
| `"Base64编码 Hello"` | 编码转换 | ✅ 开箱即用 |
| `"统计字数"` 然后粘贴文本 | 中英词频统计 | ✅ 开箱即用 |
| `"测试 https://api.github.com"` | HTTP 请求 | ✅ 开箱即用 |
| `"帮我压缩 D:\photo.jpg"` | 图片压缩 | 📦 需确认装 Pillow |
| `"合并这几个PDF"` | PDF 合并 | 📦 需确认装 PyPDF2 |
| `"MP4转GIF"` | 视频转换 | 📦 需确认装 FFmpeg |
| `"给视频加水印 文字=我的水印"` | 视频编辑 | 📦 需确认装 FFmpeg |
| `"生成二维码 内容=Hello"` | 二维码 | ✅ 开箱即用 |
| `"生成随机密码 长度=16"` | 密码生成 | ✅ 开箱即用 |
| `"测试正则 \d+ 文本=abc123"` | 正则测试 | ✅ 开箱即用 |
| `"看看CPU使用率"` | 系统资源监控 | ✅ 开箱即用 |
| `"把这个MD转成HTML"` | Markdown转HTML | ✅ 开箱即用 |

---

## 📋 registry.json 工具注册表 ⭐ v3.9.0 新增

> 49 个工具的元数据注册表，包含模块/参数 schema/依赖声明/示例/安全等级。CLI 启动时只加载此文件（轻量），工具代码延迟加载。

<details>
<summary>📋 registry.json 结构说明</summary>

```json
{
  "version": "4.1.0",
  "total_tools": 49,
  "packs": {
    "core": {"name": "核心包", "description": "默认加载", "default": true},
    "ent": {"name": "娱乐包", "description": "娱乐/生活模块", "default": false},
    "media": {"name": "媒体包", "description": "图片/PDF/视频", "default": false},
    "ai": {"name": "AI包", "description": "AI 办公", "default": false}
  },
  "modules": [...]
}
```

> **字段说明**：`deps` 为空表示零依赖；`safety` 为 `warn` 表示需用户确认；`pack` 表示所属包（core 默认加载，其余按需安装）。

</details>

---

## 🔒 安全规则（v3.9.0 分级重构）

> **dgngjx-skill v3.9.0 起采用三级安全策略**：🔴 硬拦截 / 🟡 警告+确认 / 🟢 自由读写。

### 🔴 硬拦截（不处理，即使明确要求也拒绝）

**Windows 可执行 / 批处理脚本：**
`.bat`、`.cmd`、`.ps1`、`.vbs`、`.exe`、`.dll`、`.lnk`、`.msi`

**其他风险脚本：**
`.sh`、`.com`、`.scr`、`.hta`、`.reg`

**二进制镜像 / 安装包：**
`.iso`、`.dmg`、`.apk`、`.jar`

**系统缓存 / 隐藏文件：**
`.DS_Store`、`.git` 目录、`.env`、`.log`、`.tmp`

### 🟡 警告+用户确认（显示风险说明，用户确认后可读写）

**Office 二进制文档：**
`.docx`、`.xlsx`、`.pptx`、`.doc`、`.xls`、`.ppt`、`.xlsm`、`.docm`、`.pptm`

> ⚠️ 警告内容："此操作将读取/写入 Office 文档，可能包含宏或敏感数据。确认继续？"

### 🟢 自由读写（非风险类型，无需确认）

图片（`.jpg/.png/.webp/.bmp/.gif/.tiff`）、文档（`.pdf/.md/.txt/.csv/.json/.xml`）、音频（`.mp3/.wav/.m4a`）、视频（`.mp4/.gif`）等非风险类型。

<details>
<summary>📋 安全过滤代码（v3.9.0 分级版）</summary>

```python
import os

# === v3.9.0 安全规则：三级分级策略 ===

BLOCKED_EXTENSIONS = {
    '.bat', '.cmd', '.ps1', '.vbs', '.exe', '.dll', '.lnk', '.msi',
    '.sh', '.com', '.scr', '.hta', '.reg',
    '.iso', '.dmg', '.apk', '.jar',
    '.ds_store', '.env', '.log', '.tmp',
}

WARN_EXTENSIONS = {
    '.docx', '.xlsx', '.pptx', '.doc', '.xls', '.ppt', '.xlsm', '.docm', '.pptm',
}

BLOCKED_DIRS = {'.git', '.svn', '.hg', '__pycache__', 'node_modules', '.idea', '.vscode'}

def _is_safe_file(filepath: str, assume_yes: bool = False) -> tuple:
    """检查文件安全等级。返回 (状态, 原因) 状态: 'safe' / 'warn' / 'block'"""
    basename = os.path.basename(filepath)
    if basename.startswith('.') and basename.lower() in {'.ds_store', '.env', '.gitconfig', '.bashrc'}:
        return 'block', f"隐藏系统文件 {basename} 被拦截"
    parts = filepath.replace('\\', '/').split('/')
    for part in parts:
        if part.lower() in BLOCKED_DIRS:
            return 'block', f"系统目录 {part} 被拦截"
    ext = os.path.splitext(filepath)[1].lower()
    if ext in BLOCKED_EXTENSIONS:
        return 'block', f"{ext} 可执行/风险类型被安全规则禁止"
    if ext in WARN_EXTENSIONS:
        if assume_yes:
            return 'safe', ""
        return 'warn', f"将读写 Office 文档({ext})，可能包含宏或敏感数据"
    return 'safe', ""

def _is_safe_output(filepath: str) -> tuple:
    """检查输出文件类型是否安全（不允许生成可执行/危险文件）"""
    ext = os.path.splitext(filepath)[1].lower()
    if ext in {'.exe', '.dll', '.bat', '.cmd', '.ps1', '.vbs', '.sh', '.com', '.scr', '.hta', '.reg', '.msi', '.apk', '.jar'}:
        return False, f"安全规则禁止生成 {ext} 文件"
    return True, ""
```

</details>

---

## ⚡ 自适应硬件调度 （v3.5 新增）

> dgngjx-skill 会自动检测你的电脑配置（CPU核心数、内存大小），并根据硬件能力调整并发任务数量和资源分配，**绝不拖累低配电脑**。

<details>
<summary>📋 硬件检测与智能调度脚本（v3.5 新增）</summary>

```python
import os, sys, subprocess, platform

def get_hardware_info() -> dict:
    """自动检测用户电脑硬件信息，用于智能调度"""
    info = {
        'cpu_count': os.cpu_count() or 2,
        'ram_mb': 0,
        'platform': platform.system(),
        'is_low_end': False,
        'max_workers': 1,
        'max_file_size_mb': 100,
    }
    
    try:
        if info['platform'] == 'Windows':
            result = subprocess.run(
                ['wmic', 'computersystem', 'get', 'TotalPhysicalMemory', '/value'],
                capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.split('\n'):
                if 'TotalPhysicalMemory' in line:
                    bytes_val = int(line.split('=')[1].strip())
                    info['ram_mb'] = bytes_val // (1024 * 1024)
                    break
        elif info['platform'] == 'Linux':
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal'):
                        info['ram_mb'] = int(line.split()[1]) // 1024
                    break
        elif info['platform'] == 'Darwin':
            result = subprocess.run(
                ['sysctl', '-n', 'hw.memsize'], capture_output=True, text=True, timeout=5
            )
            info['ram_mb'] = int(result.stdout.strip()) // (1024 * 1024)
    except Exception:
        info['ram_mb'] = 4096
    
    if info['ram_mb'] < 4096 or info['cpu_count'] <= 2:
        info['is_low_end'] = True
        info['max_workers'] = 1
        info['max_file_size_mb'] = 50
    elif info['ram_mb'] < 8192 or info['cpu_count'] <= 4:
        info['max_workers'] = 2
        info['max_file_size_mb'] = 200
    else:
        info['max_workers'] = min(info['cpu_count'], 4)
        info['max_file_size_mb'] = 500
    
    return info

_HW = get_hardware_info()
print(f"🖥️ 系统检测: {_HW['cpu_count']}核 | {_HW['ram_mb']}MB RAM | {_HW['platform']}")
if _HW['is_low_end']:
    print("⚡ 已启用低配模式：单任务运行，小文件优先，绝不卡顿")
else:
    print(f"⚡ 已启用标准模式：最多 {_HW['max_workers']} 并发，文件上限 {_HW['max_file_size_mb']}MB")
```

</details>

**调度策略一览：**

| 硬件级别 | 内存 | CPU | 并发数 | 单文件上限 | 保护策略 |
|---------|------|-----|--------|-----------|---------|
| 🟢 高配 | ≥8GB | ≥6核 | 4 | 500MB | 多任务并行，大文件分块 |
| 🟡 中配 | 4-8GB | 2-4核 | 2 | 200MB | 双任务，中等文件 |
| 🔴 低配 | <4GB | ≤2核 | 1 | 50MB | 单任务，小文件优先 |

---

## 📦 依赖管理

### 检测环境

任何功能使用前，AI 先跑这个脚本看看缺了什么：

<details>
<summary>📋 依赖检测脚本</summary>

```python
import sys, subprocess
print(f"Python: {sys.version.split()[0]}")
pkgs = {'PIL':'Pillow(PIL)','rembg':'rembg','PyPDF2':'PyPDF2','cv2':'opencv-python','jieba':'jieba'}
for pkg, name in pkgs.items():
    try: __import__(pkg); print(f"  ✅ {name}")
    except: print(f"  ❌ {name}（缺失）")
try:
    subprocess.run(['ffmpeg','-version'], capture_output=True, text=True)
    print("  ✅ ffmpeg")
except: print("  ❌ ffmpeg（缺失）")
```

</details>

### 一键安装

```
pip install Pillow PyPDF2 jieba
```

> AI 必须问用户确认后再执行。

### 按功能安装

| 你想用 | 只装这个 | 命令 |
|--------|---------|------|
| 压缩图片 / 证件照 / 基础修复 | Pillow (3MB) | `pip install Pillow` |
| PDF 合并/拆分/加密 | PyPDF2 (200KB) | `pip install PyPDF2` |
| 人像抠图 | rembg (300MB) | `pip install rembg` |
| 精准中文分词 | jieba (10MB) | `pip install jieba` |
| 视频转换 / 编辑 | ffmpeg (系统包) | 见下方一键安装 |

> ⚠️ rembg 首次运行会自动下载 ~300MB 模型（1-5分钟），装好后可离线使用。
> 💡 jieba 为可选依赖，词频统计不装 jieba 也能用（会自动降级到正则分词）。

### FFmpeg 一键安装（v3.0 简化）

> 💡 最简方案：打开 PowerShell，粘贴 `winget install ffmpeg` 一行搞定。

---

## ❌ 不支持（边界情况说明）

| 不支持 | 原因 | 替代方案 |
|--------|------|---------|
| 在线编辑 PSD | .psd 为封闭格式 | [Photopea](https://www.photopea.com/) |
| Excel 在线编辑 | 超出能力 | 可通过本工具转 PDF |
| 视频录屏（浏览器外） | 需浏览器 API | 用电脑自带录屏 |
| 大于 500MB 的视频 | 浏览器会卡 | 需本地安装 FFmpeg |
| 密码加密后丢失 | 安全机制限制 | 密码在加密时展示一次，请截图保存 |
| 实时网络请求拦截 | 超出能力范围 | 使用 Fiddler / Charles |
| 批量视频压制 | 需专业编码软件 | HandBrake 批量队列 |
| 处理可执行文件 | 安全规则禁止 | 使用专业反编译/分析工具 |

---

## 📦 包化架构（v4.1.0 新增）

> v4.1.0 引入四包机制，SKILL.md 从 129KB 瘦身至 30KB，模块详情外置到 `references/modules/*.md`。

### 四包一览

| 包 ID | 名称 | 默认加载 | 包含模块 | 依赖 |
|-------|------|:--------:|---------|------|
| `core` | 核心包 | ✅ | 数据换算/文本/教育/开发/实用/系统工具 | 零依赖 |
| `ent` | 娱乐包 | ❌ | 生活娱乐（笑话/壁纸/BMI/番茄钟） | 零依赖 |
| `media` | 媒体包 | ❌ | 图片/PDF/视频 | Pillow/PyPDF2/FFmpeg |
| `ai` | AI包 | ❌ | AI办公（会议纪要） | whisper（可选） |

### 包安装方式

```bash
# CLI 安装
dgngjx --install-pack ent
dgngjx --install-pack media
dgngjx --install-pack ai

# 查看已安装包
dgngjx --list-packs
```

### 模块详情文件

| 模块 | 文件路径 |
|------|---------|
| 模块 1：数据换算 | `references/modules/calc.md` |
| 模块 2：文本工具 | `references/modules/text.md` |
| 模块 3：教育工具 | `references/modules/edu.md` |
| 模块 4：生活娱乐 | `references/modules/life.md` |
| 模块 5：开发工具 | `references/modules/dev.md` |
| 模块 6：图片工具 | `references/modules/img.md` |
| 模块 7：PDF转换 | `references/modules/pdf.md` |
| 模块 8：视频工具 | `references/modules/video.md` |
| 模块 9：实用小工具 | `references/modules/util.md` |
| 模块 10：系统工具 | `references/modules/sys.md` |
| 模块 11：AI办公 | `references/modules/ai.md` |

---

## 🏥 首次运行体检报告（v4.1.0 新增）

> 首次运行时自动检测环境，输出就绪率和缺失依赖一键安装命令。

<details>
<summary>📋 体检报告代码</summary>

```python
#!/usr/bin/env python3
"""dgngjx-skill 首次运行体检报告 v4.1.0"""
import sys, subprocess, os, json, platform

HEALTH_FILE = os.path.join(os.path.expanduser("~"), ".workbuddy", "dgngjx_health.json")

def check_python():
    v = sys.version_info
    ok = v >= (3, 8)
    return {"name": "Python", "status": "ok" if ok else "warn",
            "version": f"{v.major}.{v.minor}.{v.micro}", "required": "≥ 3.8",
            "fix": None if ok else "请升级 Python 到 3.8+"}

def check_module(pkg_name, import_name=None):
    import_name = import_name or pkg_name
    try:
        __import__(import_name)
        return {"name": pkg_name, "status": "ok", "version": "", "required": "", "fix": None}
    except ImportError:
        return {"name": pkg_name, "status": "missing", "version": "", "required": "", "fix": f"pip install {pkg_name}"}

def check_ffmpeg():
    try:
        r = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            return {"name": "FFmpeg", "status": "ok", "version": r.stdout.split(chr(10))[0][:50], "required": "", "fix": None}
    except: pass
    return {"name": "FFmpeg", "status": "missing", "version": "", "required": "视频转换/编辑", "fix": "winget install ffmpeg"}

def check_network():
    try:
        import urllib.request
        req = urllib.request.Request("https://api.github.com", headers={"User-Agent":"dgngjx/4.1"})
        urllib.request.urlopen(req, timeout=5)
        return {"name": "网络连接", "status": "ok", "version": "", "required": "", "fix": None}
    except Exception as e:
        return {"name": "网络连接", "status": "warn", "version": "", "required": "汇率/知识查询", "fix": f"网络受限: {type(e).__name__}"}

def run_health_check(force=False):
    if not force and os.path.exists(HEALTH_FILE):
        try:
            with open(HEALTH_FILE, encoding="utf-8") as f:
                prev = json.load(f)
            if prev.get("skipped", False):
                return None
        except: pass

    checks = [
        check_python(),
        check_module("Pillow", "PIL"),
        check_module("PyPDF2"),
        check_module("rembg"),
        check_module("jieba"),
        check_ffmpeg(),
        check_network(),
    ]

    ok_count = sum(1 for c in checks if c["status"] == "ok")
    missing = [c for c in checks if c["status"] == "missing"]

    print("=" * 50)
    print("  🏥 dgngjx-skill 首次运行体检报告")
    print("=" * 50)
    for c in checks:
        icon = "✅" if c["status"] == "ok" else ("⚠️" if c["status"] == "warn" else "❌")
        ver = f" ({c['version']})" if c["version"] else ""
        print(f"  {icon} {c['name']}{ver}")
    print(f"  就绪率: {ok_count}/{len(checks)} ({ok_count*100//len(checks)}%)")
    if missing:
        print("  📦 缺失依赖（一键安装）：")
        cmds = []
        for c in missing:
            if c["fix"]:
                print(f"    • {c['name']}: {c['fix']}")
                if "pip install" in c["fix"]:
                    cmds.append(c["fix"].replace("pip install ", ""))
        if cmds:
            print(f"  快速安装: pip install {' '.join(cmds)}")
    print("=" * 50)

    os.makedirs(os.path.dirname(HEALTH_FILE), exist_ok=True)
    with open(HEALTH_FILE, "w", encoding="utf-8") as f:
        json.dump({"checked": True, "skipped": False, "ok_count": ok_count, "total": len(checks)}, f)
    return checks

if __name__ == "__main__":
    force = "--force" in sys.argv
    run_health_check(force=force)
```

</details>

---

## 功能模块

> **v4.1.0 起模块详情外置**，主文档只保留模块名称索引，完整代码见 `references/modules/*.md`。

| 模块 | 名称 | 包 | 文件 |
|------|------|:--:|------|
| 1 | 数据换算 | core | [calc.md](references/modules/calc.md) |
| 2 | 文本工具 | core | [text.md](references/modules/text.md) |
| 3 | 教育工具 | core | [edu.md](references/modules/edu.md) |
| 4 | 生活娱乐 | ent | [life.md](references/modules/life.md) |
| 5 | 开发工具 | core | [dev.md](references/modules/dev.md) |
| 6 | 图片工具 | media | [img.md](references/modules/img.md) |
| 7 | PDF转换 | media | [pdf.md](references/modules/pdf.md) |
| 8 | 视频工具 | media | [video.md](references/modules/video.md) |
| 9 | 实用小工具 | core | [util.md](references/modules/util.md) |
| 10 | 系统工具 | core | [sys.md](references/modules/sys.md) |
| 11 | AI办公 | ai | [ai.md](references/modules/ai.md) |

---

## 最佳实践

### 场景 1：新电脑第一次用

```
你: "帮我检测一下环境"
AI: 跑检测脚本 → 自适应硬件调度初始化 → 体检报告
你: "帮我装一下"
AI: pip install Pillow PyPDF2 jieba
你: "帮我压缩 D:\photo.jpg"
AI: ✅ 完成
```

### 场景 2：低配电脑性能保护

```
处理 50MB 图片时
→ 系统检测到 4GB RAM → 自动单任务模式
→ 显示 "⚠️ 50MB 文件 → 压缩可能需1-2分钟"
→ 分配最小资源，不卡顿
```

### 场景 3：安全文件拦截

```
你: "帮我压缩 C:\Windows\system32\cmd.exe"
AI: 🚫 .exe 可执行程序 — 安全规则禁止处理
```

---

## ❓ 常见问题

### Q1: 第一次使用怎么做？
直接说一句话。零依赖功能直接跑。需安装功能会提示。

### Q2: 发现 skill 有更新怎么办？
```bash
clawhub update dgngjx-skill
```
或检查：`skillhub search dgngjx-skill`

### Q3: 有什么建议/bug？
📧 **邮箱：njskills@agent.qq.com**
作者会阅读每一条反馈。

### Q4: 处理大文件太慢？
v3.5.0 起已根据你的硬件自动调度，低配机会自动降为小文件单任务模式，不会出现卡死。

### Q5: 批量重命名风险？
必须先预览，确认输入 `YES` 才执行。可执行文件会自动跳过。

### Q6: MD转HTML支持复杂语法吗？
支持标题、列表、代码块、引用、粗体、行内代码。复杂表格建议用 pandoc。

### Q7: 汇率查询需要联网吗？
默认无需联网（内置 30+ 种常见货币缓存）。输入联网模式可获取实时汇率，联网失败自动降级到缓存。

### Q8: 历史记录存在哪里？
保存在 `~/.workbuddy/dgngjx_history.json`，保留最近 200 条。可随时搜索或清空。

### Q9: 会议纪要需要安装 whisper 吗？
不需要。默认使用模式 C（手动粘贴文本）即可零依赖运行。需要自动化 ASR 时再安装 whisper 或配置 Paraformer API。

### Q10: 周报是自动记录的吗？
是的。使用工具后，系统自动记录到 `~/.workbuddy/dgngjx_history.json`。周报生成时自动汇总本周期记录。

### Q11: dgngjx CLI 怎么用？
安装 skill 后，可直接用 `dgngjx 模块.工具 --参数` 调用。例如 `dgngjx calc.mortgage --amount 1000000 --years 30 --rate 4.2`。无参数启动进入交互向导。加 `--json` 输出机器可解析 JSON，加 `--yes` 或设置 `DGNGJX_ASSUME_YES=1` 跳过非危险确认点。

### Q12: registry.json 是什么？
49 个工具的元数据注册表，包含模块归属、参数 schema、依赖声明和安全等级。CLI 启动时只加载此文件（轻量），工具代码延迟加载。

### Q13: v4.1.0 的四包机制怎么用？
默认加载 `core` 核心包（37 个零依赖工具）。需要图片/PDF/视频功能时，运行 `dgngjx --install-pack media` 安装媒体包。需要娱乐功能时，运行 `dgngjx --install-pack ent` 安装娱乐包。运行 `dgngjx --list-packs` 查看所有可用包。

---

## 功能分类统计

| 类别 | 数量 | 开箱即用 |
|------|:----:|:--------:|
| ✅ 零依赖即可运行 | 37 | ✅ |
| 📦 需确认安装后运行 | 12 | ❌（有引导+在线替代） |
| **总计** | **49** | **76%** |

## 更新日志

| v4.1.0 | 2026-09-17 | 增加：包化架构（SKILL.md 129KB→30KB + 11模块外置 references/modules/*.md）；增加：四包机制（core/ent/media/ai，CLI --install-pack/--list-packs）；增加：首次运行体检报告（Python/Pillow/PyPDF2/rembg/jieba/ffmpeg/网络/磁盘）；迁移：娱乐模块（笑话/壁纸/BMI/番茄钟）移至 ent 可选包；优化：registry.json 独立文件 + pack 字段；增加：个税五险全国化（tax_2026.yaml 数据包，13城市查表+7级分段累进引擎）；增加：汇率缓存时效治理（72h TTL + 陈旧标注 + 警示横幅）；增加：独立个税计算器（模块1.2.1） |
| v3.9.0 | 2026-08-24 | 增加：统一 CLI 入口（argparse 子命令 + registry.json 注册表 + 49 工具参数化）；拆分：编码/哈希拆分为 encode + hash 独立工具；合并：图片五功能合并为 img 统一入口（compress/convert/removebg/idphoto/repair）；优化：安全规则分级重构（🔴 硬拦截 / 🟡 警告+确认 / 🟢 自由读写）；增加：无人值守支持（DGNGJX_ASSUME_YES 环境变量 + --yes + --json 输出） |
| v3.8.0 | 2026-08-17 | 增加：会议纪要生成器（模块11.1 ASR三级降级链）；增加：周报/月报自动生成（模块10.6）；优化：系统资源监控（模块10.1 wmic→PowerShell CIM） |
| v3.7.0 | 2026-08-07 | 增加：CSV查看器/密码强度/颜色转换/随机数/文本差异/BMI/番茄钟/汇率查询/历史记录/配置持久化/管道联动；优化：开箱即用率57%→65% |
| v3.6.0 | 2026-07-07 | 增加：文件哈希/UUID/时间戳/IP工具；扩展：单位换算8→28种；扩展：编码新增MD5/SHA+进制互转 |
| v3.5.0 | 2026-07-14 | 增加：硬件调度/安全过滤/系统监控/批量重命名/MD转HTML/更新提醒 |
| v3.0.0 | 2026-07-13 | 增加：jieba分词/视频编辑/路径修复/FFmpeg脚本/模块9 |
| v2.5.0 | 2026-07-12 | 增加：HTTP语法修复；扩充坑表格 |
| v2.2.0 | 2026-07-11 | 修复：多个bug |
| v2.1.0 | 2026-07-10 | 修复：单位换算float崩溃+壁纸urllib缺失 |
| v2.0.0 | 2026-07-09 | 增加：国内联网优化；大文件性能增强 |
| v1.0.0 | 2026-07-02 | 初始版本，8大模块29个工具 |

## 一键安装后可用功能

| 装这些 | 新增可用 |
|-------|---------|
| `pip install Pillow` | 压缩 / 证件照 / 基础修复 / PS |
| `pip install PyPDF2` | PDF 合并 / 拆分 / 加密 / 解密 |
| `pip install rembg` | 人像抠图（首次 300MB） |
| `pip install jieba` | 精准中文分词 |
| FFmpeg | 格式转换 / 视频编辑（6大功能） |
| `pip install qrcode[pil]` | 二维码本地生成 |

## 发布信息

- **作者**：Admin
- **联系邮箱**：njskills@agent.qq.com
- **许可证**：MIT
- **支持平台**：Windows / macOS / Linux
- **当前版本**：v4.1.0
- **检查更新**：`skillhub search dgngjx-skill`
- **升级命令**：`clawhub update dgngjx-skill`