# C 扩展使用说明

## 概述

AGI 进化模型包含两个 C 扩展模块：`personality_core`（马斯洛权重/大五人格算法）与
`core_perception_node`（工具调用接口 / trace_id）。分别提供：

- Linux/macOS 预编译：`personality_core.so` / `core_perception_node.so`（ELF 格式）
- Windows 预编译：`personality_core.pyd` / `core_perception_node.pyd`（PE/DLL 格式，2026-08-11 由本地 MinGW-w64 构建）

加载器 `scripts/c_ext_loader.py` 按平台自动选择 `.so` 或 `.pyd`，并带执行安全探针与纯 Python 自动降级。

## 部署说明

### 生产环境（推荐）

本 Skill 已包含双平台预编译的 C 扩展文件，部署时会自动加载：

- ✅ 无需编译
- ✅ 自动降级
- ✅ 功能完整

### 目录结构

C 扩展文件位于 `scripts/` 根目录（加载器搜索 `scripts/` 与 `scripts/personality_core/`）：

```
scripts/
├── personality_core.pyd          ← Windows 预编译（已构建）
├── core_perception_node.pyd      ← Windows 预编译（已构建）
├── personality_core.so           ← Linux/macOS 预编译
├── core_perception_node.so       ← Linux/macOS 预编译
└── c_ext_loader.py               ← 平台感知加载器
```

### 本地开发

如需重新编译 C 扩展，请参考以下步骤：

#### 1. 编译要求

- Linux/macOS: gcc 或 clang
- **Windows: 原生 MinGW-w64（如 `D:\Program Files\mingw64\bin\gcc.exe`，x86_64-w64-mingw32 目标）。实测 VS Build Tools 非必需。**
- Python 3.7+；本机管理版 Python 位于 `C:\Users\kiwif\.workbuddy\binaries\python\versions\3.13.12\`（含 `include/Python.h`、`libs/python3.lib`、`python3.dll`）

#### 2. Windows 编译步骤（稳定 ABI，跨 3.3+ 版本）

采用 `Py_LIMITED_API` 链接 `python3.lib`（-> `python3.dll`），产出的 `.pyd` 在 CPython 3.13 / 3.14 上均可加载：

```bash
GCC="D:/Program Files/mingw64/bin/gcc.exe"
INC="C:/Users/kiwif/.workbuddy/binaries/python/versions/3.13.12/include"
LIB="C:/Users/kiwif/.workbuddy/binaries/python/versions/3.13.12/libs"
OUT="C:/Users/kiwif/.workbuddy/skills/agi-evolution-model/scripts"

# personality_core：纯标准库 + Python.h，直接编译
"$GCC" -shared -std=c99 -O2 -D Py_LIMITED_API=0x03030000 -I"$INC" \
  so333/personality_core.c -o "$OUT/personality_core.pyd" -L"$LIB" -lpython3

# core_perception_node：用 getpid()，MinGW 需 force-include <process.h>
"$GCC" -shared -std=c99 -O2 -D Py_LIMITED_API=0x03030000 -include process.h -I"$INC" \
  so333/core_perception_node.c -o "$OUT/core_perception_node.pyd" -L"$LIB" -lpython3
```

产物须命名为 `personality_core.pyd` / `core_perception_node.pyd`（加载器按平台后缀查找）。

#### 3. 验证加载

```bash
cd scripts && python c_ext_loader.py
# 期望：personality_core: loaded=True / core_perception_node: loaded=True
```

## 性能对比

| 操作 | 纯Python | C扩展 | 提升 |
|------|----------|-------|------|
| 归一化权重 | 0.8ms | 0.05ms | **16倍** |
| 相似度计算 | 3.2ms | 0.12ms | **27倍** |
| 优先级计算 | 2.5ms | 0.09ms | **28倍** |
| 批量计算(1000) | 280ms | 12ms | **23倍** |

## 自动降级机制

如果 C 扩展加载失败，Skill 会自动降级到纯 Python 实现：

```python
from personality_layer_pure import PersonalityLayer

if PersonalityLayer.USE_C_EXT:
    print("使用 C 扩展加速")
else:
    print("使用纯 Python 实现（降级模式）")
```

**降级触发条件**：
- C 扩展文件不存在
- 平台不匹配（例如在 macOS 上使用 Linux 的 .so）
- Python 版本不兼容

## 平台支持

当前预编译版本支持：

| 平台 | 状态 | 文件名 |
|------|------|--------|
| Linux x64 | ✅ 预编译 | `personality_core.so` / `core_perception_node.so` |
| Windows x64 | ✅ 已预编译（2026-08-11） | `personality_core.pyd` / `core_perception_node.pyd` |
| macOS x64 | ⚠️ 需编译 | - |
| macOS ARM64 | ⚠️ 需编译 | - |

**其他平台**：需要手动编译 C 扩展。

## 故障排查

### C 扩展未加载

**症状**：日志显示 "使用纯 Python 实现（降级模式）"

**原因**：
1. 平台不匹配
2. Python 版本不兼容
3. 文件损坏

**解决方案**：
- 当前平台：降级到纯 Python（功能正常）
- 本地开发：重新编译对应平台的 C 扩展

### ImportError

**症状**：`ImportError: No module named 'personality_core'`

**解决方案**：无需处理，系统会自动降级到纯 Python 实现。

## 注意事项

1. **预编译文件**：Linux（`.so`）与 Windows（`.pyd`）均已提供；macOS 需自行编译
2. **跨平台**：未覆盖的平台自动降级到纯 Python 实现
3. **功能一致**：降级模式下功能完全正常，仅性能略低
4. **无需编译**：生产部署不需要编译，直接使用预编译文件
5. **Windows 构建约束**：`core_perception_node.c` 用了 `getpid()`，MinGW 编译须 `-include process.h`；两个模块均用 `Py_LIMITED_API` 稳定 ABI，链接 `python3.lib`，可跨 CPython 3.3+ 加载
