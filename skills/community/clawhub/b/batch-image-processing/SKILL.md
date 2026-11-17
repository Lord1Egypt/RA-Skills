---
name: batch-image-processing
description: >-
  批量图片处理：压缩、格式转换、目录重组。触发词：压缩图片、图片瘦身、batch compress、格式转换。
  覆盖：Pillow JPEG 压缩质量阈值、jpegoptim vs Pillow 选择、远程服务器批量处理、断点续传。
version: 1.0.0
author: 尘天
license: MIT
---

# 批量图片处理

## 核心决策树

| 需求 | 方案 |
|------|------|
| 只压缩 JPG，原图质量高 (>85) | jpegoptim `--max70`，速度快 |
| 已经是中等质量 (~80) 的 JPG | Pillow 重压缩 q=60-65，jpegoptim 无效 |
| 格式混合 (webp/png/gif → 统一 JPG) | Pillow 全量处理，一步到位 |
| 大批量 (>1万张) | Pillow + ThreadPoolExecutor，按 CPU 核心数定线程 |

## Pillow JPEG 压缩质量阈值（实测数据）

**关键发现：对已压缩图片，Pillow 重压缩的压缩率与 quality 的关系：**

| quality | 原图q≈80-85 时的压缩率 | 画质影响 |
|---------|----------------------|---------|
| 85 | 103-116% (反而变大!) | 无 |
| 75 | 91-101% (基本持平) | 极小 |
| 70 | 88-97% | 小 |
| 65 | 87-95% | 可接受 |
| 60 | 80-89% | 有损但不明显 |
| 55 | 79-85% | 明显但可用 |

**经验规则：**
- 原图本身已压缩过 (q≈80) → q=75 几乎无效果，需要 q≤65 才有显著压缩
- jpegoptim `--max80` 对原图质量 ≤80 的图片完全无效（不会降质）
- 要显著压缩已压缩图片，必须用 Pillow 强制重压缩 + 降低 quality

## 脚本模板

```python
#!/usr/bin/env python3
"""批量图片压缩 v2：Pillow 统一处理，输出JPG，支持断点续传。"""
import os, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

SRC_DIR = "/path/to/source"
DST_DIR = "/path/to/output"
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tiff")
DEFAULT_QUALITY = 65
WORKERS = 4  # ⚠️ 见下方 CPU 线程建议

def process_one(src_path, dst_path, quality):
    src_size = os.path.getsize(src_path)
    if os.path.exists(dst_path) and os.path.getsize(dst_path) > 100:
        return src_size, os.path.getsize(dst_path), "skip"
    try:
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)  # ⚠️ 必须每文件建目录
        img = Image.open(src_path)
        if hasattr(img, "n_frames") and img.n_frames > 1:
            img.seek(0)
        # 透明通道 → 白底RGB
        if img.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P": img = img.convert("RGBA")
            if img.mode in ("RGBA", "LA"):
                bg.paste(img, mask=img.split()[-1])
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")
        img.save(dst_path, "JPEG", quality=quality, optimize=True)
        return src_size, os.path.getsize(dst_path), "ok"
    except Exception as e:
        return src_size, 0, f"fail:{e}"
```

## ⚠️ 常见陷阱

### 1. os.makedirs 只创建顶层目录
```python
# ❌ WRONG — 只创建 DST_DIR，子目录不存在导致 cp/save 失败
os.makedirs(DST_DIR, exist_ok=True)
# 后续操作 /data/software/xiunice_images/sub/file.jpg → 报错

# ✅ CORRECT — 每个文件处理前创建父目录
os.makedirs(os.path.dirname(dst_path), exist_ok=True)
```

### 2. jpegoptim 对已压缩图片无效
jpegoptim `--max80` 的含义是「如果原图质量 > 80 则降到 80，否则不动」。如果原图已经是 q≈80，完全不压缩。必须用 Pillow 重压缩。

### 3. CPU 线程数必须匹配服务器核心数
```bash
nproc  # 查看 CPU 核心数
```
| 服务器 | 建议线程数 | 说明 |
|--------|-----------|------|
| 4核 (N100等) | 2-3 | 留 1-2 核给系统服务 |
| 8核 | 4-6 | |
| 16核+ | 8-12 | |

**用户明确纠正：8线程跑在4核N100上CPU拉满。** 这是硬限制，不是建议。

### 6. 爬虫下载的文件在宿主机上，不在容器里

爬虫（如 xiunice_xiuren_scraper.py）通过 SSH 在宿主机上运行，下载的文件保存在宿主机的 `/data/software/` 下。**容器内的 `/opt/data/` 和宿主机的 `/data/software/` 是不同的路径。**

```bash
# ❌ 在容器里找 — 找不到
ls /data/software/xiuren_images/  # No such file

# ✅ SSH 到宿主机找
ssh -i KEY root@172.17.0.1 "ls /data/software/xiuren_images/"
```

**排查步骤**：找不到文件时，先查 session_search 看是哪个 worker 执行的任务，确认脚本中的 `SAVE_DIR` 路径，然后 SSH 到对应机器查看。

### 7. 压缩任务输出目录规范

**每次压缩任务使用新的输出目录**，不要复用之前的目录。命名规则：`{原目录名}_compressed`。

```bash
# ✅ 新任务新目录
源: /data/software/xiuren_images/
目标: /data/software/xiuren_compressed/  # 新建

# ❌ 复用旧目录会导致混乱
目标: /data/software/xiunice_images/  # 这是另一个任务的
```

### 8. Pillow quality 选择实测

| quality | 原图q≈80时压缩率 | 适用场景 |
|---------|-----------------|---------|
| 60 | 35-40% | 平衡画质与体积 |
| 50 | 30-35% | 极限压缩，画质可接受 |
| 40 | 25-30% | 画质明显下降 |

**用户偏好**：quality=50 用于 xiuren 图片压缩（21GB → 7.4GB，节省 13.7GB）。

### 4. Pillow open 不释放内存
大批量处理时，每张图 open → save 后 PIL 对象应自然回收，但 for 循环中避免累积引用。ThreadPoolExecutor 4-8 workers 是安全范围。

### 5. 格式转换注意事项
- PNG 透明背景 → JPG：需要合成白底（模板中已包含）
- WebP 动画：`img.seek(0)` 只取第一帧
- 模式不匹配：`P` 模式（调色板）需先转 RGBA 再合成

## 远程服务器执行模式

```bash
# SCP 脚本到远程
scp -i /path/to/key script.py user@host:/data/script.py

# 后台执行（不阻塞对话）
terminal(
    command="ssh -i key user@host 'cd /data && python3 -u script.py 2>&1 | tee /data/compress.log'",
    background=True,
    notify_on_complete=True
)

# 检查进度
ssh -i key user@host "tail -5 /data/compress.log"
```

**断点续传**：输出文件已存在且 >100B 则跳过，支持中断后重跑。

### 6. SSH 首次连接需要 StrictHostKeyChecking

```bash
# ❌ WRONG — 首次 SSH 到新主机会卡在 yes/no 提示
ssh -i key root@172.17.0.1 "command"

# ✅ CORRECT — 跳过主机密钥验证（cron/自动化场景必需）
ssh -i key -o ConnectTimeout=5 -o StrictHostKeyChecking=no root@172.17.0.1 "command"
```

**注意**：`-o ConnectTimeout=5` 防止网络不通时无限等待；`-o StrictHostKeyChecking=no` 是自动化任务的硬性要求。

### 7. CLI 参数化压缩脚本（批量任务模板）

对于需要反复执行的压缩任务（不同源目录、不同目标目录），使用 CLI 参数化脚本：

```bash
# 用法
python3 compress_generic.py --input /data/software/src_dir --output /data/software/dst_dir

# 批量执行多个目录
for dir in dir1 dir2 dir3; do
  python3 compress_generic.py --input /data/software/$dir --output /data/software/${dir}_compressed
done
```

脚本位置：`scripts/compress_generic.py`（在 skill 目录下）
部署方式：SCP 到宿主机后执行，支持断点续传。

### 8. Cron 自主执行模式（无用户在场）

当任务以 cron job 运行时，没有用户可交互，必须：
- 所有参数在任务描述中明确指定（路径、quality、threads）
- 后台执行 + notify_on_complete 等待完成
- 用 `tail` 读取日志获取最终结果
- 直接输出报告，不询问确认

## 目录重组（按元数据分组）

当图片/文件夹平铺在一个目录下，需要按元数据（人名、日期、类别等）重新分组时：

### 核心流程
1. **先 dry-run** — 打印分组统计和移动计划，确认无误再执行
2. **提取元数据** — 从文件夹名中用正则提取关键字段
3. **处理命名不一致** — 同一实体可能有多种命名格式，需要映射表
4. **执行移动** — `os.rename()` 原子操作，同一文件系统内无复制开销

### 人名提取模板（适用于 xiuren/xiunice 等写真站）

```python
import re

def extract_person_name(dirname):
    """从文件夹名提取人名，处理拼音+中文组合"""
    s = dirname
    # 移除常见前缀
    s = re.sub(r'^xiuren-uncensored-4k-', '', s)
    s = re.sub(r'^xiuren-uncensored-', '', s)
    
    # 匹配 "名字-r18-..." 或 "名字-秀人网..." 模式
    m = re.match(r'^([^\-]+(?:-[^\-]+)*?)(?:-r18|-秀人网|-内购|-私拍|...)', s)
    name = m.group(1).strip('-') if m else s.split('-')[0]
    
    # 处理拼音+中文: "chen-xiaohua-陈小花" → "陈小花"
    parts = name.split('-')
    if len(parts) >= 2:
        cn = [p for p in parts if re.search(r'[\u4e00-\u9fff]', p)]
        if cn:
            name = cn[0]  # 优先用中文名
    
    return name

# 手动映射表（解决提取不准的边界情况）
NAME_MAP = {
    "唐翩翩-秀人網-極品模特": "唐翩翩",
    "娜娜子-童顏巨乳": "娜娜子",
    "lin": None,  # 混了多人，需单独处理
}

# 需要合并的分组（同一人的不同命名）
MERGE_MAP = {
    "evelyn": "evelyn艾莉",
    "白洁bseeie": "白洁bessie",
}
```

### ⚠️ 关键陷阱

**0. os.rename 对长路径/同名目录会失败 (Errno 22)**
```python
# ❌ os.rename 在以下情况失败：
# 1. 路径过长（>255 bytes，中文字符占3字节）
# 2. 目标路径是源路径的子目录（自己移动到自己下面）
os.rename(src, dst)  # [Errno 22] Invalid argument

# ✅ 解决方案：用 subprocess 调 mv 命令（os.rename 对长路径会失败）
import subprocess
# 注意：subprocess 执行外部命令，仅当 os.rename 确实失败时使用
subprocess.run(["mv", src, dst], check=True)

# 或者先 dry-run 检查，失败的手动用 bash mv 处理
```

**实测案例**：310个文件夹重命名，27个因路径过长或同名目录失败。用 `mv` 命令全部修复。

**1. 必须先 dry-run**
```bash
python3 reorganize.py --dry-run  # 只打印，不移动
# 确认分组正确后再去掉 --dry-run 执行
```
第一次写的脚本几乎必然有提取错误（边界情况太多），dry-run 能快速发现问题。

**2. 双人合集保留原名**
如 `梨霜儿-金允希` 是双人作品，不应拆分到单人目录下。

**3. 同名不同分辨率版本**
同一作品可能有 `4k` 和非 `4k` 两个版本（文件夹名差 `-4k` 后缀），应归入同一人名目录。

## 并行任务路径隔离

**当多个任务同时处理同一数据源时，必须使用不同的输出目录。**

```bash
# ❌ WRONG — 两个任务写同一目录
老C压缩 → /data/software/xiunice_images
老B爬虫  → /data/software/xiunice_images  # 冲突！

# ✅ CORRECT — 路径分离
老C压缩 → /data/software/xiunice_images    # 压缩输出
老B爬虫  → /data/software/xiuren_images    # 爬虫输出
```
