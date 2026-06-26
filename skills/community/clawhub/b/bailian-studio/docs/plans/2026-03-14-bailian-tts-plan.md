# Bailian Studio TTS 播报 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 增加百炼 TTS 播报（WAV + simpleaudio），支持默认配置与 env/secret 覆盖。

**Architecture:** 新增 `tts_speak.py` 作为独立 CLI，复用 `env.py` 读取配置，调用百炼 TTS API 生成 WAV，使用 simpleaudio 播放。

**Tech Stack:** Python 3, dashscope, simpleaudio.

---

### Task 1: 扩展配置读取（TTS 相关）

**Files:**
- Modify: `scripts/env.py`

**Step 1: Write the failing test**

在 `tests` 新增测试骨架（若暂无测试框架，可先写断言脚本并手动运行）：
```python
from scripts.env import get_tts_config
cfg = get_tts_config()
assert cfg["model"]
```
期待：当前缺少 `get_tts_config`，运行失败。

**Step 2: Run test to verify it fails**

Run: `python3 -c "from scripts.env import get_tts_config"`
Expected: ImportError 或 AttributeError。

**Step 3: Write minimal implementation**

在 `env.py` 增加：
```python
def get_tts_config(env_path: Optional[Path] = None) -> Dict[str, str]:
    return {
        "model": _get_value("BAILIAN_TTS_MODEL", env_path) or "<DEFAULT>",
        "voice": _get_value("BAILIAN_TTS_VOICE", env_path) or "<DEFAULT>",
        "sample_rate": _get_value("BAILIAN_TTS_SAMPLE_RATE", env_path) or "16000",
    }
```
默认值用百炼官方默认（实现时替换 `<DEFAULT>`）。

**Step 4: Run test to verify it passes**

Run: `python3 -c "from scripts.env import get_tts_config; print(get_tts_config())"`
Expected: 输出包含 model/voice/sample_rate。

**Step 5: Commit**

```bash
git add scripts/env.py
git commit -m "feat: add bailian tts config"
```

---

### Task 2: 新增 TTS 播报脚本

**Files:**
- Create: `scripts/tts_speak.py`

**Step 1: Write the failing test**

```bash
python3 scripts/tts_speak.py --text "测试"
```
Expected: 当前文件不存在，失败。

**Step 2: Write minimal implementation**

实现流程：
1. 读取 API Key / TTS 配置
2. 调用百炼 TTS API（WAV）
3. 将返回内容写入临时 wav
4. `simpleaudio` 播放并等待结束

**Step 3: Run test to verify it passes**

Run: `python3 scripts/tts_speak.py --text "测试"`
Expected: 播放声音（或在无 key 时给出清晰错误）。

**Step 4: Commit**

```bash
git add scripts/tts_speak.py
git commit -m "feat: add tts speak cli"
```

---

### Task 3: 文档更新

**Files:**
- Modify: `SKILL.md`

**Step 1: Update docs**

新增使用示例：
```bash
python3 {baseDir}/scripts/tts_speak.py --text "你好"
```
并说明依赖：`dashscope`, `simpleaudio`。

**Step 2: Commit**

```bash
git add SKILL.md
git commit -m "docs: add tts usage"
```

---

### Task 4: 验证与收尾

**Step 1: Run quick check**

- `python3 scripts/tts_speak.py --text "测试"`

**Step 2: Commit**

```bash
git status --short
```
确保干净。
