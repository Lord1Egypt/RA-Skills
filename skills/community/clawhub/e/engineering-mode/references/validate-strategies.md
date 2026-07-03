# Validate Strategies

VERIFY 阶段的验证命令速查。按需加载。

## L1: Lint（每次编辑后必做，10s 超时）

| 语言 | 命令 | 备注 |
|---|---|---|
| JavaScript/JSX | `npx eslint <file>` | 单文件 lint |
| TypeScript/TSX | `npx eslint <file>` | 优先 lint，不做类型检查 |
| Python | `python3 -m flake8 <file>` | 或 `python3 -m py_compile <file>` 检查语法 |
| Shell/Bash | `shellcheck <file>` | |
| Rust | `cargo check -p <crate>` | 单 crate 检查 |
| JSON | `python3 -c "import json; json.load(open('<file>'))"` | 纯语法验证 |
| YAML | `python3 -c "import yaml; yaml.safe_load(open('<file>'))"` | 纯语法验证 |
| Markdown | 跳过（无语法风险） | |

**重要**：
- TypeScript **不用** `tsc --noEmit <file>` —— 跨文件依赖导致假阳性
- 类型检查退化到 L2 或依赖 agent 自身审查
- 项目无 linter 配置 → 退化为 `python3 -c "import py_compile"` / `node --check <file>`

## L2: 单元/集成（逻辑改动时，30s 超时）

| 语言 | 命令 | 备注 |
|---|---|---|
| Python | `python3 -m pytest tests/test_<module>.py -x -q` | `-x` 首失败即停 |
| JavaScript/TS | `npx jest <test-file> --no-coverage` | 单测试文件 |
| Rust | `cargo test <test_name> --quiet` | |
| Go | `go test ./path/to/package -run TestName` | |

原则：
- 只跑**相关**测试，不跑全量
- 超时 30s，超时视为失败

## L3: 全量（所有步骤完成后，120s 超时）

| 语言 | 命令 | 备注 |
|---|---|---|
| Python | `python3 -m pytest -x -q` | 全量测试 |
| JavaScript/TS | `npm run build 2>&1` | 全量构建 |
| Rust | `cargo build 2>&1` | debug build |
| Go | `go build ./...` | 全量编译 |
| 多语言项目 | 按项目 Makefile/脚本定义 | |

原则：
- 仅在**所有步骤完成后**执行一次
- 120s 超时，超时报告但不一定失败（大项目正常）

## 超时处理

所有验证命令必须带超时：
```bash
timeout 10 npx eslint src/file.ts 2>&1
timeout 30 python3 -m pytest tests/test_x.py -x -q 2>&1
timeout 120 npm run build 2>&1
```
