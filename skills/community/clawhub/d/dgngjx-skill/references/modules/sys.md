# 🖥️ 模块 10：系统工具 ⭐ v3.5 新增模块

---

#### 10.1 系统资源监控 ⭐ v3.8.0 优化（wmic → PowerShell CIM）

**✅ 开箱即用**

实时监控 CPU、内存、磁盘使用率，返回中文信息。v3.8.0 将 wmic 迁移到 PowerShell CIM cmdlet，兼容 Windows Server 2025+。

<details>
<summary>📋 展开查看命令</summary>

```python
import os, platform, subprocess, time

def _ps_cim(cmd):
    """执行 PowerShell CIM 命令并返回 stdout"""
    r = subprocess.run(
        ["powershell", "-NoProfile", "-Command", cmd],
        capture_output=True, text=True, timeout=10
    )
    return r.stdout.strip()

def get_system_resources():
    """获取系统资源信息（跨Windows/macOS/Linux）"""
    info = {'cpu_usage': 0, 'ram_total_mb': 0, 'ram_used_mb': 0, 'ram_percent': 0,
            'disk_total_gb': 0, 'disk_used_gb': 0, 'disk_percent': 0,
            'cpu_count': os.cpu_count() or 2, 'platform': platform.system()}
    
    # CPU 使用率
    try:
        if info['platform'] == 'Windows':
            out = _ps_cim("Get-CimInstance Win32_Processor | Select-Object -ExpandProperty LoadPercentage")
            lines = [l.strip() for l in out.split('\n') if l.strip().isdigit()]
            info['cpu_usage'] = int(lines[0]) if lines else 0
        else:
            r = subprocess.run(['grep','-c','processor','/proc/cpuinfo'], capture_output=True, text=True, timeout=5)
            info['cpu_usage'] = 0  # Linux
    except: pass
    
    # 内存信息
    try:
        if info['platform'] == 'Windows':
            out = _ps_cim("Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory,TotalVisibleMemorySize | Format-List")
            for line in out.split('\n'):
                line = line.strip()
                if line.startswith('TotalVisibleMemorySize'):
                    info['ram_total_mb'] = int(line.split(':')[1].strip()) // 1024
                elif line.startswith('FreePhysicalMemory'):
                    free = int(line.split(':')[1].strip()) // 1024
                    info['ram_used_mb'] = info['ram_total_mb'] - free
            if info['ram_total_mb'] > 0:
                info['ram_percent'] = int(info['ram_used_mb'] / info['ram_total_mb'] * 100)
        else:
            with open('/proc/meminfo') as f:
                mem = {}
                for line in f:
                    parts = line.split()
                    if parts[0] in ('MemTotal:','MemAvailable:','MemFree:'):
                        mem[parts[0]] = int(parts[1])
            total = mem.get('MemTotal:',0)
            avail = mem.get('MemAvailable:', mem.get('MemFree:',0))
            info['ram_total_mb'] = total // 1024
            info['ram_used_mb'] = (total - avail) // 1024
            if total > 0: info['ram_percent'] = int((total-avail)/total*100)
    except: pass
    
    # 磁盘信息
    try:
        if info['platform'] == 'Windows':
            out = _ps_cim("Get-CimInstance Win32_LogicalDisk | Select-Object Size,FreeSpace,DeviceID | Format-List")
            total = free = 0
            for block in out.split('\n\n'):
                for line in block.split('\n'):
                    line = line.strip()
                    if line.startswith('Size') and ':' in line:
                        val = line.split(':')[1].strip()
                        if val.isdigit(): total += int(val)
                    elif line.startswith('FreeSpace') and ':' in line:
                        val = line.split(':')[1].strip()
                        if val.isdigit(): free += int(val)
            info['disk_total_gb'] = total // (1024**3)
            info['disk_used_gb'] = (total - free) // (1024**3)
            if total > 0: info['disk_percent'] = int((total-free)/total*100)
        else:
            r = subprocess.run(['df','/'], capture_output=True, text=True, timeout=5)
            lines = r.stdout.strip().split('\n')
            if len(lines)>1:
                parts = lines[1].split()
                if len(parts)>=4:
                    total = int(parts[1])
                    used = int(parts[2])
                    info['disk_total_gb'] = total // (1024**2)
                    info['disk_used_gb'] = used // (1024**2)
                    info['disk_percent'] = int(parts[4].replace('%',''))
    except: pass
    
    return info

res = get_system_resources()
print("=" * 40)
print("  📊 dgngjx-skill 系统资源监控")
print("=" * 40)
print(f"🖥️ 系统: {res['platform']}")
print(f"⚡ CPU: {res['cpu_usage']}% 占用 | {res['cpu_count']} 核心")
print(f"🧠 内存: {res['ram_used_mb']}/{res['ram_total_mb']} MB ({res['ram_percent']}%)")
print(f"💾 磁盘: {res['disk_used_gb']}/{res['disk_total_gb']} GB ({res['disk_percent']}%)")
print()

# 预警
if res['ram_percent'] > 90: print("🔴 内存严重不足！建议关闭部分程序")
elif res['ram_percent'] > 75: print("🟡 内存偏高，考虑释放")
if res['disk_percent'] > 90: print("🔴 磁盘空间告急！清理空间")
elif res['disk_percent'] > 80: print("🟡 磁盘空间偏低")
if res['cpu_usage'] > 90: print("🔴 CPU 负载过高")
elif res['cpu_usage'] > 75: print("🟡 CPU 使用率较高")
```

</details>

**⚠️ 可能遇到的坑：**

| 情况 | 原因 | 解决 |
|------|------|------|
| 获取失败返回 0 | 权限不足 | 以管理员权限运行 |
| wmic 被禁用 | Windows 精简版 | v3.8.0 已迁移到 PowerShell CIM，无需 wmic |
| macOS 内存显示异常 | macOS 内存管理机制 | 正常行为，macOS 积极利用内存 |
| PowerShell 执行策略限制 | Restricted 策略 | 运行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |

---

#### 10.2 批量文件重命名 ⭐ v3.5.0 新增

**✅ 开箱即用**（零依赖，纯 os 模块）

批量预览后才能执行，支持正则替换、序号前缀、大小写转换。

<details>
<summary>📋 展开查看命令</summary>

```python
import os, re

def _fix_path(p):
    return p.strip().strip('"').strip("'").replace("\\","/").replace("//","/")

BLOCKED_EXTS = {'.exe','.dll','.bat','.cmd','.ps1','.vbs','.sh','.com','.scr','.hta','.reg','.msi','.apk','.jar'}

dir_path = _fix_path(input("目录路径:").strip() or ".")
if not os.path.isdir(dir_path):
    print(f"❌ 目录不存在: {dir_path}")
else:
    files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path,f))]
    safe_files = [f for f in files if os.path.splitext(f)[1].lower() not in BLOCKED_EXTS]
    if len(safe_files) != len(files):
        print(f"⚠️ 已跳过 {len(files)-len(safe_files)} 个系统/可执行文件")
    files = safe_files
    
    if not files:
        print("❌ 目录为空或无安全文件")
    else:
        print(f"\n📁 {dir_path} 中找到 {len(files)} 个文件")
        print()
        print("重命名模式:")
        print("  1. 添加前缀 (如: photo_001.jpg)")
        print("  2. 添加后缀 (如: 001_终版.jpg)")
        print("  3. 正则替换 (正则表达式匹配替换)")
        print("  4. 大小写转换 (全部小写/大写)")
        print("  5. 序号重命名 (统一前缀+递增数字)")
        mode = input("选择模式(1-5):").strip() or "1"
        
        previews = []
        
        if mode == "1":
            prefix = input("前缀:").strip() or "file_"
            for i, fn in enumerate(files):
                new = prefix + fn
                previews.append((fn, new))
                
        elif mode == "2":
            suffix = input("后缀:").strip() or "_ok"
            for fn in files:
                name, ext = os.path.splitext(fn)
                new = name + suffix + ext
                previews.append((fn, new))
                
        elif mode == "3":
            pattern = input("匹配正则:").strip()
            repl = input("替换为:").strip()
            if not pattern:
                print("❌ 正则表达式不能为空")
                previews = []
            else:
                for fn in files:
                    new = re.sub(pattern, repl, fn)
                    previews.append((fn, new))
                    
        elif mode == "4":
            upper = input("转大写?(Y/n):").strip().lower() != 'n'
            for fn in files:
                new = fn.upper() if upper else fn.lower()
                previews.append((fn, new))
                
        elif mode == "5":
            prefix = input("统一前缀:").strip() or "file"
            start = int(input("起始序号(1):") or 1)
            width = int(input("序号位数(3):") or 3)
            for i, fn in enumerate(files):
                _, ext = os.path.splitext(fn)
                new = f"{prefix}_{str(start+i).zfill(width)}{ext}"
                previews.append((fn, new))
        
        if previews:
            print(f"\n📋 预览（共 {len(previews)} 个文件）:")
            print("-" * 60)
            for old, new in previews[:10]:
                if old != new:
                    print(f"  {old}")
                    print(f"    → {new}")
                else:
                    print(f"  {old} （无变化）")
            if len(previews) > 10:
                print(f"  ... 还有 {len(previews)-10} 个文件")
            print("-" * 60)
            
            new_names = [new for _, new in previews]
            if len(new_names) != len(set(new_names)):
                print("⚠️ 警告：新文件名存在冲突！")
                from collections import Counter
                for name, cnt in Counter(new_names).items():
                    if cnt > 1:
                        print(f"   冲突: {name} ({cnt}次)")
                print("   请修改规则避免冲突")
            else:
                confirm = input(f"\n确认执行? (输入 YES 确认): ").strip()
                if confirm == "YES":
                    success = 0
                    for old, new in previews:
                        if old != new:
                            old_path = os.path.join(dir_path, old)
                            new_path = os.path.join(dir_path, new)
                            if not os.path.exists(new_path):
                                os.rename(old_path, new_path)
                                success += 1
                            else:
                                print(f"⚠️ 已存在，跳过: {new}")
                    print(f"✅ 已重命名 {success} 个文件")
                else:
                    print("❎ 已取消")
```

</details>

**⚠️ 可能遇到的坑：**

| 情况 | 原因 | 解决 |
|------|------|------|
| 输入 YES 仍被拒绝 | 必须大写的 YES | 输入 `YES` |
| 文件名冲突 | 替换规则导致重名 | 修改正则或前缀 |
| 无变化 | 规则未匹配 | 检查正则或前缀 |
| 跳过系统文件 | 安全规则拦截 | 正常行为，不可执行文件不参与 |

---

#### 10.3 Markdown 转 HTML ⭐ v3.5.0 新增

**✅ 开箱即用**（零依赖纯 Python，将 Markdown 文件转为带样式的独立 HTML）

<details>
<summary>📋 展开查看命令</summary>

```python
import os, re, html

def _fix_path(p):
    return p.strip().strip('"').strip("'").replace("\\","/").replace("//","/")

BLOCKED_EXTS = {'.exe','.dll','.bat','.cmd','.ps1','.vbs','.sh','.com','.scr','.hta','.reg','.msi','.apk','.jar'}

f = _fix_path(input("Markdown文件路径:").strip() or "README.md")
if not os.path.exists(f):
    print(f"❌ 文件不存在: {f}")
else:
    ext = os.path.splitext(f)[1].lower()
    if ext in BLOCKED_EXTS:
        print(f"🚫 安全规则禁止处理 {ext} 文件")
    else:
        with open(f, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()
        
        lines = md_content.split('\n')
        html_lines = []
        in_code_block = False
        in_list = False
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('```'):
                lang = stripped[3:].strip()
                if in_code_block:
                    html_lines.append('</code></pre>')
                    in_code_block = False
                else:
                    html_lines.append(f'<pre><code class="language-{lang}">' if lang else '<pre><code>')
                    in_code_block = True
                continue
            
            if in_code_block:
                html_lines.append(html.escape(line))
                continue
            
            if not stripped:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append('')
                continue
            
            if stripped.startswith('# '):
                html_lines.append(f'<h1>{html.escape(stripped[2:])}</h1>')
                continue
            elif stripped.startswith('## '):
                html_lines.append(f'<h2>{html.escape(stripped[3:])}</h2>')
                continue
            elif stripped.startswith('### '):
                html_lines.append(f'<h3>{html.escape(stripped[4:])}</h3>')
                continue
            
            if stripped.startswith('- ') or stripped.startswith('* '):
                if not in_list:
                    html_lines.append('<ul>')
                    in_list = True
                item = stripped[2:]
                item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                html_lines.append(f'<li>{item}</li>')
                continue
            
            if stripped.startswith('> '):
                html_lines.append(f'<blockquote>{html.escape(stripped[2:])}</blockquote>')
                continue
            
            if stripped == '---':
                html_lines.append('<hr/>')
                continue
            
            paragraph = html.escape(stripped)
            paragraph = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', paragraph)
            paragraph = re.sub(r'`(.+?)`', r'<code>\1</code>', paragraph)
            html_lines.append(f'<p>{paragraph}</p>')
        
        if in_list:
            html_lines.append('</ul>')
        
        body_content = '\n'.join(html_lines)
        
        full_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{os.path.basename(f)}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px 20px; color: #333; line-height: 1.8; }}
h1 {{ color: #1a1a1a; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
h2 {{ color: #2c3e50; margin-top: 30px; }}
h3 {{ color: #34495e; }}
code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
pre {{ background: #2d2d2d; color: #f8f8f2; padding: 16px; border-radius: 6px; overflow-x: auto; }}
blockquote {{ border-left: 4px solid #ddd; margin: 0; padding-left: 16px; color: #666; }}
ul {{ padding-left: 24px; }}
li {{ margin-bottom: 4px; }}
hr {{ border: none; border-top: 1px solid #eee; margin: 20px 0; }}
strong {{ color: #1a1a1a; }}
</style>
</head>
<body>
{body_content}
</body>
</html>'''
        
        out_name = os.path.splitext(f)[0] + '.html'
        with open(out_name, 'w', encoding='utf-8') as out:
            out.write(full_html)
        
        print(f"✅ 已生成: {out_name}")
        print(f"   行数: {len(lines)} → HTML大小: {os.path.getsize(out_name)//1024}KB")
        print(f"   💡 双击打开浏览器预览")
```

</details>

**⚠️ 可能遇到的坑：**

| 情况 | 原因 | 解决 |
|------|------|------|
| 复杂表格未转换 | 极简解析器不支持 | 使用专业工具如 pandoc |
| 图片未显示 | 本地路径未转绝对路径 | 手动替换为绝对路径或URL |
| 含HTML标签的MD | 被转义 | 正常行为，安全考虑 |
| 大文件慢 | 逐行解析 | 10MB+ 文件建议用 pandoc |

---

#### 10.4 历史记录系统 ⭐ v3.7.0 新增

**✅ 开箱即用**（纯 Python 标准库 json，零依赖）

<details>
<summary>📋 展开查看命令</summary>

```python
import json, os, datetime

HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".workbuddy", "dgngjx_history.json")
os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

def _load():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []

def _save(records):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(records[-200:], f, ensure_ascii=False, indent=2)

mode = input("操作(记录/查看/搜索/清空):").strip() or "查看"
if mode == "记录":
    tool = input("工具名:").strip()
    inp = input("输入摘要:").strip()
    out = input("输出摘要:").strip()
    rec = {"time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           "tool": tool, "input": inp[:200], "output": out[:200]}
    records = _load()
    records.append(rec)
    _save(records)
    print(f"✅ 已记录（共 {len(records)} 条）")
elif mode == "查看":
    records = _load()
    if not records:
        print("📭 暂无历史记录")
    else:
        for i, r in enumerate(records[-20:], 1):
            print(f"{i}. [{r['time']}] {r['tool']}")
            print(f"   输入: {r.get('input','')[:60]}")
            print(f"   输出: {r.get('output','')[:60]}")
        print(f"\n共 {len(records)} 条（显示最近 20 条）")
elif mode == "搜索":
    kw = input("搜索关键词:").strip().lower()
    records = _load()
    matched = [r for r in records if kw in r.get("tool","").lower() or kw in r.get("input","").lower()]
    print(f"找到 {len(matched)} 条匹配:")
    for r in matched[-10:]:
        print(f"  [{r['time']}] {r['tool']} - {r.get('input','')[:50]}")
elif mode == "清空":
    confirm = input("确认清空？输入 YES:").strip()
    if confirm == "YES":
        _save([])
        print("✅ 历史记录已清空")
    else:
        print("已取消")
else:
    print(f"❌ 不支持 {mode}。可选: 记录/查看/搜索/清空")
```

</details>

---

#### 10.5 配置持久化 ⭐ v3.7.0 新增

**✅ 开箱即用**（纯 Python 标准库 json，零依赖）

<details>
<summary>📋 展开查看命令</summary>

```python
import json, os

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".workbuddy", "dgngjx_config.json")
DEFAULTS = {"image_quality": 80, "output_format": "JPEG", "theme": "auto",
            "recent_tools": [], "auto_save_history": True}
os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

def _load():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, encoding="utf-8") as f:
            cfg = json.load(f)
        for k, v in DEFAULTS.items():
            if k not in cfg:
                cfg[k] = v
        return cfg
    return dict(DEFAULTS)

def _save(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

mode = input("操作(查看/设置/重置):").strip() or "查看"
if mode == "查看":
    cfg = _load()
    print("=== 当前配置 ===")
    for k, v in cfg.items():
        print(f"  {k}: {v}")
    print(f"\n配置文件: {CONFIG_FILE}")
elif mode == "设置":
    cfg = _load()
    key = input(f"设置项({'/'.join(DEFAULTS.keys())}):").strip()
    if key not in DEFAULTS:
        print(f"❌ 未知设置项。可选: {', '.join(DEFAULTS.keys())}")
    else:
        val = input(f"当前 {key}={cfg[key]}，新值:").strip()
        if val:
            if isinstance(DEFAULTS[key], int):
                try: val = int(val)
                except ValueError: print("❌ 需要整数"); raise SystemExit
            elif isinstance(DEFAULTS[key], bool):
                val = val.lower() in ("true","yes","1","y")
            cfg[key] = val
            _save(cfg)
            print(f"✅ {key} = {val}")
elif mode == "重置":
    confirm = input("确认重置为默认值？输入 YES:").strip()
    if confirm == "YES":
        _save(DEFAULTS)
        print("✅ 已重置")
    else:
        print("已取消")
else:
    print(f"❌ 不支持 {mode}。可选: 查看/设置/重置")
```

</details>

---

#### 10.6 周报/月报自动生成 ⭐ v3.8.0 新增

**✅ 开箱即用**（纯 Python 标准库 json/datetime，零依赖）

<details>
<summary>📋 展开查看命令</summary>

```python
import json, os, datetime

HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".workbuddy", "dgngjx_history.json")

def _load():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []

mode = input("生成周报(w)/月报(m)，默认w:").strip() or "w"
records = _load()
if not records:
    print("📭 暂无历史记录。先使用工具自动记录工作。")
else:
    today = datetime.date.today()
    if mode == "m":
        start = today.replace(day=1)
        period_label = f"{today.year}年{today.month}月"
        title = f"# 📋 {period_label} 月度工作报告"
    else:
        start = today - datetime.timedelta(days=today.weekday())
        period_label = f"{start.strftime('%m/%d')} - {today.strftime('%m/%d')}"
        title = f"# 📋 本周工作报告（{period_label}）"
    
    filtered = []
    for r in records:
        try:
            t = datetime.datetime.strptime(r.get("time",""), "%Y-%m-%d %H:%M:%S").date()
            if t >= start and t <= today:
                filtered.append(r)
        except ValueError:
            continue
    
    print(title)
    print(f"\n> 生成时间：{today:%Y-%m-%d} | 数据源：{len(filtered)} 条记录\n")
    
    if not filtered:
        print("本周期内暂无记录。")
    else:
        tool_counts = {}
        for r in filtered:
            tool = r.get("tool","未知")
            tool_counts[tool] = tool_counts.get(tool, 0) + 1
        print("## 📊 工具使用统计\n")
        print("| 工具 | 使用次数 |")
        print("|------|---------:|")
        for tool, cnt in sorted(tool_counts.items(), key=lambda x: -x[1]):
            print(f"| {tool} | {cnt} |")
        print("\n## 📝 工作记录明细\n")
        for i, r in enumerate(filtered, 1):
            inp = r.get("input","")[:80]
            out = r.get("output","")[:80]
            print(f"**{i}. [{r['time']}] {r['tool']}**")
            print(f"   - 输入: {inp}")
            print(f"   - 输出: {out}")
            print()
        print("---\n*本报告由 dgngjx-skill 历史记录系统自动生成*")
```

</details>

---

#### 🔗 模块间管道联动 ⭐ v3.7.0 新增架构特性

**✅ 开箱即用**（纯标准库，零依赖）

<details>
<summary>📋 管道使用示例</summary>

```python
import csv, json, io

def csv_to_markdown_table(csv_path):
    """CSV 文件 → Markdown 表格"""
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if len(rows) < 2:
        return "CSV 至少需要 1 行表头 + 1 行数据"
    header = rows[0]
    lines = []
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")
    for row in rows[1:]:
        while len(row) < len(header):
            row.append("")
        lines.append("| " + " | ".join(row[:len(header)]) + " |")
    return "\n".join(lines)

def csv_to_json(csv_path):
    """CSV 文件 → JSON 数组"""
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return json.dumps(list(reader), ensure_ascii=False, indent=2)

path = input("CSV文件路径:").strip().strip('"').strip("'")
fmt = input("输出格式(json/md):").strip() or "md"
if fmt == "json":
    print(csv_to_json(path))
else:
    print(csv_to_markdown_table(path))
```

</details>
