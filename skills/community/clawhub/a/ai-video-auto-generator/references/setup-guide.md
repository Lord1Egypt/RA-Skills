# 视频流水线环境搭建指南

## 前置依赖

| 组件 | 版本要求 | 说明 |
|------|---------|------|
| Python | ≥3.13 | 宿主平台自动管理 |
| Node.js | ≥22 | 宿主平台自动管理 |
| FFmpeg | ≥6.0 | hyperframes 渲染必需（含 ffprobe） |
| hyperframes | ≥0.6 | 视频合成引擎（npm 包） |
| lark-cli | ≥1.0.56 | 飞书对接 |

依赖路径解析遵循**执行路径即身份**原则，不绑定宿主平台：
- Layer 1：Skill 包内路径（`scripts/_paths.py` — 通过 `__file__` + SKILL.md marker 自定位）
- Layer 2：运行时配置（`<project>/config/` → `<skill_root>/config/` 分层加载）
- Layer 3：用户项目（`--project <path>`）

详情见 `scripts/_paths.py` 和 `scripts/_shared_tools.py`。

---

## 一键安装（WorkBuddy 环境）

```bash
# 1. 安装 Python 依赖
pip install imageio-ffmpeg

# 2. 安装 hyperframes（Node.js 包）
#    hyperframes 路径由 _paths.py 的 resolve_node_modules() 解析：
#    <skill_root>/vendor/node/node_modules/ → <skill_root>/node_modules/ → 系统 npm root
cd node_modules
npx hyperframes --version    # 会自动安装

# 3. 设置 ffmpeg（从 imageio-ffmpeg 复制）
python3 -c "
import os, shutil
from imageio_ffmpeg import get_ffmpeg_exe
# ffmpeg 路径由 _paths.py 的 resolve_tool('ffmpeg', skill_root) 解析：
# <skill_root>/vendor/ffmpeg/ → config/tools.toml → 系统 PATH → legacy(仅标记)
# 安装到系统 PATH 上即可，_paths.py 会自动发现
src = get_ffmpeg_exe()
dst = os.path.dirname(src)
print(f'ffmpeg already available at: {src}')
"

# 4. 验证：用 _paths.py 确认工具可用
python3 -c "
import sys, os
sys.path.insert(0, 'scripts')
from _paths import resolve_skill_root, resolve_tool

root = resolve_skill_root()
print(f'Skill root: {root}')

for tool in ('ffmpeg', 'node'):
    exe = resolve_tool(tool, root)
    print(f'{tool}: {\"✅ \" + exe if exe else \"❌ not found\"}')

from _paths import resolve_node_modules
nm = resolve_node_modules(root)
hf = os.path.join(nm, 'hyperframes', 'dist', 'cli.js') if nm else ''
print(f'hyperframes CLI: {\"✅\" if hf and os.path.isfile(hf) else \"❌ not found\"}')"
```

---

## 自动路径解析（执行路径即身份）

`scripts/_paths.py` 的路径计算规则（不绑定任何宿主平台）：

```
resolve_skill_root(__file__)  # 从调用者向上找 SKILL.md → skill 根目录

find_config_files(skill_root, project)  # 分层配置，优先级：
  1. <project>/config/keys.env           ← 项目专属
  2. <project>/config/config.toml
  3. <skill_root>/config/keys.env        ← 当前平台这份 skill 专属
  4. <skill_root>/config/config.toml

resolve_tool(tool, skill_root)  # 工具路径：
  1. <skill_root>/vendor/<tool>/         ← 随 skill 打包
  2. <skill_root>/config/tools.toml      ← 这份 skill 声明的路径
  3. 系统 PATH                           ← 用户自己装的
  4. (仅 .legacy-workbuddy 标记) ~/.workbuddy/binaries/<tool>/
```

不依赖任何全局环境变量。三个平台同时跑三份 skill，各读各的 `skill_root/config/`。

---

## 跨 PC 检查清单

在新 PC 上跑流水线前，执行：

```bash
# Python
python3 -c "import imageio_ffmpeg; print('imageio_ffmpeg OK')"

# Node.js
node --version  # ≥22

# 工具检查（通过 _paths.py 确认）
python3 -c "
import sys, os
sys.path.insert(0, 'scripts')
from _paths import resolve_skill_root, resolve_tool, resolve_node_modules
root = resolve_skill_root()
for tool in ('ffmpeg', 'node'):
    exe = resolve_tool(tool, root)
    print(f'{tool}: {\"✅ \" + exe if exe else \"❌ not found\"}')
nm = resolve_node_modules(root)
hf = os.path.join(nm, 'hyperframes', 'dist', 'cli.js') if nm else ''
print(f'hyperframes CLI: {\"✅\" if hf and os.path.isfile(hf) else \"❌ not found\"}')
"

# lark-cli
lark-cli --version

# Feishu 配置
cat config/config.toml | grep feishu   # 或项目目录下的 project/config/config.toml
```

如果缺少任何组件，运行上面的一键安装命令。

---

## 常见问题

### FFmpeg not found

hyperframes 需要在 `PATH` 上找到 ffmpeg 和 ffprobe。`hyperframes_stitch.py` 会自动通过
`_paths.py` 的 `resolve_ffmpeg(skill_root)` 解析（优先级：vendor/ → tools.toml → PATH → legacy）。

如果仍然找不到，手动检查：
```bash
ffmpeg -version
which ffmpeg
```

### Composition not found

hyperframes 需要以下文件在项目根目录：
- `index.html` ← 由 `stitch` 子命令 / `hyperframes_stitch.py` 自动生成
- `hyperframes.json`
- `meta.json`

如果仍报错，用 `--composition` 显式指定合成文件路径。

### 飞书写入失败

Windows 下 lark-cli 输出中文时可能解码异常。
已在 `feishu.py` 的 `_lark()` 中设置 `encoding="utf-8", errors="replace"`。
数据会自动兜底写入本地缓存 `tasks/task_tracker.json`。
