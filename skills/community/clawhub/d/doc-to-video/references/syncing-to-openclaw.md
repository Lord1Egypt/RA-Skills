# 同步到 OpenClaw 工作流

> 配套 SKILL.md v1.0.5 用。
> 适用：**Hermes 端的 skill 改完了，要同步到 OpenClaw 端**（或反之）。
> 核心陷阱：Hermes 端存在 self-update 机制，**写完文件后不能立刻校验 SHA**。

---

## 为什么需要这个

`doc-to-video` skill **同时存在于两个地方**：

- `~/.hermes/skills/doc-to-video/` — Hermes 加载用
- `~/.openclaw/workspace/skills/doc-to-video/` — OpenClaw 加载用

两边内容必须保持一致，否则下次 OpenClaw 端跑会拿到旧版。

OpenClaw 端有**自己的元数据**（`._meta.json`、`.clawhub/origin.json`、`skill-card.md`），**不要覆盖**这些。

---

## 标准 sync 流程

```bash
SRC=/Users/neo/.hermes/skills/doc-to-video
DST=/Users/neo/.openclaw/workspace/skills/doc-to-video

# 1. 拷 SKILL.md
cp "$SRC/SKILL.md" "$DST/SKILL.md"

# 2. 拷 generate_audio.py（通常未变，但稳妥起见）
cp "$SRC/generate_audio.py" "$DST/generate_audio.py"

# 3. 创建 references/ 目录，拷 3+ 个 ref 文件
mkdir -p "$DST/references"
cp "$SRC/references/macos-gotchas.md" "$DST/references/"
cp "$SRC/references/voice-swap-and-iterate.md" "$DST/references/"
cp "$SRC/references/worked-example-tsp-solidity04.md" "$DST/references/"
# 第二个视频之后还会有 second-video-pattern.md 等新 ref

# 4. 创建 templates/ 目录，拷所有模板
mkdir -p "$DST/templates"
for f in audio_frames.py generate_audio.py voice_test.py Scene.tsx index.tsx \
         merge.sh remotion-package.json remotion-tsconfig.json remotion.config.ts; do
  cp "$SRC/templates/$f" "$DST/templates/$f"
done
chmod +x "$DST/templates/audio_frames.py"

# 5. 重要：不动 OpenClaw 私有文件
#    _meta.json, skill-card.md, .clawhub/origin.json
```

---

## 致命陷阱：Hermes self-update

**Hermes 端存在 self-update 机制**——当你写完一个文件后，**9-30 秒内**它可能被 Hermes 内部流程改一遍（提取 inline 脚本成独立文件、补充 changelog 等）。

如果 sync 后**立刻**校验 SHA，可能看到两边不一致，**但其实不是你的错**。

**正确做法**：

```bash
# 1. sync 完后，**等 60 秒** 让 Hermes self-update 完成
sleep 60

# 2. 再跑 SHA 校验
python3 -c "
import os, hashlib
src = '/Users/neo/.hermes/skills/doc-to-video'
dst = '/Users/neo/.openclaw/workspace/skills/doc-to-video'
def sha(p):
    with open(p, 'rb') as f: return hashlib.sha256(f.read()).hexdigest()[:12]

# 比较两边共享的文件
shared = ['SKILL.md', 'generate_audio.py', 'templates/audio_frames.py', ...]
for rel in shared:
    h, o = sha(f'{src}/{rel}'), sha(f'{dst}/{rel}')
    if h != o:
        print(f'MISMATCH: {rel}')
        # 通常是 Hermes 端被更新了 → 重新 cp
"
```

如果发现 mismatch，**重新 cp 一次**（H = sync after self-update）：

```bash
cp "$SRC/SKILL.md" "$DST/SKILL.md"  # Hermes 端 self-update 后再 cp
# 不需要再 sleep，第二次 cp 后 Hermes 不会再改
```

---

## 实战踩坑记录

### 2025-06-12 sync 一次的具体现象

```
11:34:21  cp SKILL.md (Hermes v1.0.4 含 6 voice inline 测试) → OpenClaw
11:34:30  Hermes self-update 把 inline 测试抽到 templates/voice_test.py
11:34:31  校验 SHA: d3887feef8a6 (Hermes) vs d3887feef8a6 (OpenClaw) → 看起来 OK
11:34:33  校验 SKILL.md SHA 单独: d5439ebb1a6a (Hermes) vs dee51528ccce (OpenClaw) → MISMATCH
11:34:35  重新 cp SKILL.md → 一致
```

**关键观察**：

- 总目录 SHA 可能一致（因为 OpenClaw 也有新文件），但**单文件 SHA 不一致**
- 一定要**逐文件校验**，不能只看总目录
- 第一次 cp + sleep 60 + 重新 cp 是最稳的

---

## 反向 sync：OpenClaw → Hermes

如果你在 OpenClaw 端改了 skill 想同步到 Hermes 端：

```bash
SRC=/Users/neo/.openclaw/workspace/skills/doc-to-video
DST=/Users/neo/.hermes/skills/doc-to-video

# 拷同样的文件（除了 openclaw 私有的）
for f in SKILL.md generate_audio.py references/*.md templates/*.{py,tsx,ts,sh,json}; do
  cp "$SRC/$f" "$DST/$f"
done
chmod +x "$DST/templates/audio_frames.py"

# 同样要 sleep 60 等 Hermes 处理
sleep 60

# 校验
# ...
```

---

## 校验脚本（可直接用）

保存为 `~/.hermes/bin/sync-skill.sh`：

```bash
#!/bin/bash
# sync-skill.sh SKILL_NAME
# 例如：sync-skill.sh doc-to-video

set -e
SKILL=$1
SRC=/Users/neo/.hermes/skills/$SKILL
DST=/Users/neo/.openclaw/workspace/skills/$SKILL

if [[ ! -d "$SRC" ]] || [[ ! -d "$DST" ]]; then
    echo "❌ 目录不存在：$SRC 或 $DST"
    exit 1
fi

echo "🔄 同步 $SKILL: Hermes → OpenClaw"

# 拷 SKILL.md
cp "$SRC/SKILL.md" "$DST/SKILL.md"

# 拷 references/ 和 templates/ 下所有文件
for d in references templates; do
    [[ -d "$SRC/$d" ]] || continue
    mkdir -p "$DST/$d"
    for f in "$SRC/$d"/*; do
        [[ -f "$f" ]] || continue
        cp "$f" "$DST/$d/"
    done
done

# chmod 可执行文件
chmod +x "$DST/templates/audio_frames.py" 2>/dev/null || true
chmod +x "$DST/templates/voice_test.py" 2>/dev/null || true

echo "⏳ 等 60 秒让 Hermes self-update 完成..."
sleep 60

# 校验
python3 <<EOF
import os, hashlib
def sha(p):
    with open(p, 'rb') as f: return hashlib.sha256(f.read()).hexdigest()[:12]
mismatches = []
for root, _, files in os.walk("$SRC"):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), "$SRC")
        h = sha(f'$SRC/{rel}')
        o = sha(f'$DST/{rel}') if os.path.exists(f'$DST/{rel}') else 'MISSING'
        if h != o:
            mismatches.append(rel)
if mismatches:
    print(f'❌ {len(mismatches)} mismatch(es):')
    for m in mismatches: print(f'    {m}')
    print('重新 cp 一次...')
    for m in mismatches:
        cp "$SRC/$m" "$DST/$m"
    print('✅ 修复完成')
else:
    print('✅ 全部一致')
EOF
```

用法：

```bash
chmod +x ~/.hermes/bin/sync-skill.sh
~/.hermes/bin/sync-skill.sh doc-to-video
```

---

## 何时不需要 sync

- 只在 OpenClaw 端用了 skill，Hermes 端没改 → 不用 sync
- 只在 Hermes 端用，OpenClaw 端已废弃 → 不用 sync
- 临时试验性改动还没稳定 → 先不动 sync，等定型

---

## 关联文档

- `references/voice-swap-and-iterate.md` — 改 voice/语速后的 F[] 重算（不涉及 sync）
- `references/worked-example-tsp-solidity04.md` — 第一个视频的完整端到端实例
- `references/second-video-pattern.md` — 第二个及之后视频的复用模式
