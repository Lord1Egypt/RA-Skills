# omni2docx 回归测试

把渲染引擎的"闭环"从本地 scratch 固化进仓库，任何人 clone 后都能复现验收。

## 运行

依赖：`python-docx`、`python-pptx`（仅验收器用；渲染脚本本身只依赖标准库）。

```bash
cd omni2docx
python3 tests/run_all.py
```

或单跑其一：

```bash
python3 tests/run_matrix_test.py     # docx 引擎：12 例真实语料 + XML 级断言
python3 tests/run_matrix_multi.py    # 三格式闭环：13 例 ×(HTML/PPTX) + 4 专项
```

整体非零退出即失败（CI 直接用 `run_all.py`）。

## 套件覆盖

- **docx 矩阵**（`run_matrix_test.py`）：12 例真实解析产物（xlsx/PDF 研报/债券书/HTML/音频/docx/PPTX/JPG OCR/千页/截断/边界×2），多 profile + 开关组合，`validate_docx.py` 保真校验，再做 XML 级断言：PAGE 域、emoji 剥离、引用块楷体、递归 inline。
- **三格式闭环**（`run_matrix_multi.py`）：13 例中间件 ×（展示 HTML / 汇报 PPTX），用随包 `validate_html.py`/`validate_pptx.py` 验收（回归同时覆盖验收器本身）；专项：多源合并、`--md` 直出、空 markdown、纯表格。

## 目录

```
tests/
├── run_all.py            # 总入口（CI）
├── run_matrix_test.py    # docx 矩阵
├── run_matrix_multi.py   # 三格式闭环
├── generate_fixtures.py  # 合成 fixture 生成器（可重生成）
├── fixtures/             # 24 个 fixture（13 中间件 JSON + 10 md + edge_case.md）
├── out/                  # 生成产物（gitignore，每次重跑覆盖）
└── .gitignore
```

## fixture 说明（合成语料）

`fixtures/` 全部为**合成占位语料**（`generate_fixtures.py` 生成，或手写的 `edge_case.md`），
与任何真实机构、个人及数据无关，可安全公开、对任意 clone 可复现。结构等价于真实语料，
保留断言锚点：引用块（楷体）、嵌套行内（code/链接/斜体）、emoji（剥离/保留）、表格、脚注、
截断、大规模文档、OCR 拆字。

若要改用你自己的真实文档做回归：把解析产物放进 `fixtures/`（建议加进 `.gitignore`，不要推公开仓库），
脚本按文件名识别；`generate_fixtures.py` 仅覆盖合成 fixture，不会动你新增的文件。
