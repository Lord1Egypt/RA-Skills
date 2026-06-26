# fortune-telling-bazi

八字算命 skill，支持多人八字存储、激活当前用户、查看详情和联合分析。计算完全在本地完成，不依赖远程 API。

## 安装

### 通过 ClawHub 安装

1. 打开 ClawHub。
2. 搜索 `fortune-telling-bazi`。
3. 点击安装。
4. 安装完成后，在对话中说「开始算命」「看看八字」或「我的八字」即可启用。

### 本地检查

安装后，skill 目录中应包含：

```text
SKILL.md
README.md
scripts/
data/
```

所有 Python 文件都在 `scripts/` 下。无需额外安装第三方 Python 包。

## 使用方法

### 在对话中使用

常用触发词：

| 你可以说 | 作用 |
|---|---|
| `开始算命` / `算命` / `看看八字` / `我的八字` | 启用八字流程 |
| `添加八字` / `加个人` / `录入八字` | 添加一个新用户 |
| `查看用户` / `都有谁` | 查看已保存用户 |
| `联合分析` / `合盘` / `双人八字` | 分析多个人的八字关系 |
| `停止算命` / `不算了` / `退出算命` | 退出算命模式 |

首次启用时，系统会询问姓名、出生年月日、出生时间和性别。保存后，该用户会被激活，之后回复会自动带上八字摘要。

### 命令行使用

在 skill 根目录运行：

```bash
python3 scripts/main.py status
python3 scripts/main.py add 小明 1990 6 1 12:00 男
python3 scripts/main.py list
python3 scripts/main.py view 小明
python3 scripts/main.py active 小明
python3 scripts/main.py joint 小明,小红
python3 scripts/main.py remove 小明
```

时间参数支持：

```text
16
16:30
下午4
晚8
```

### 数据文件

用户数据保存在本地：

```text
data/users.json
data/active.json
```

这些文件包含个人出生信息，建议不要提交到公开仓库。

## 测试

运行单元测试：

```bash
python3 -m unittest scripts/test_lunar_core.py
```

测试包含 12 个固定八字样例，以及 128 个固定 seed 的随机日期 round-trip 检查。

---

# fortune-telling-bazi

A BaZi fortune-telling skill with local birth-chart calculation, multi-person storage, active-user context, detail views, and joint analysis. All calculations run locally and do not call a remote API.

## Installation

### Install from ClawHub

1. Open ClawHub.
2. Search for `fortune-telling-bazi`.
3. Click install.
4. After installation, say "开始算命", "看看八字", or "我的八字" in chat to start.

### Local Check

After installation, the skill directory should contain:

```text
SKILL.md
README.md
scripts/
data/
```

All Python files live under `scripts/`. No third-party Python packages are required.

## Usage

### Chat Usage

Common trigger phrases:

| Say | Action |
|---|---|
| `开始算命` / `算命` / `看看八字` / `我的八字` | Start the BaZi flow |
| `添加八字` / `加个人` / `录入八字` | Add a new person |
| `查看用户` / `都有谁` | List saved people |
| `联合分析` / `合盘` / `双人八字` | Run joint analysis |
| `停止算命` / `不算了` / `退出算命` | Exit fortune-telling mode |

On first use, the skill asks for name, birth date, birth time, and gender. After saving, the person becomes active, and future replies can include the BaZi summary automatically.

### Command Line Usage

Run from the skill root:

```bash
python3 scripts/main.py status
python3 scripts/main.py add Alice 1990 6 1 12:00 女
python3 scripts/main.py list
python3 scripts/main.py view Alice
python3 scripts/main.py active Alice
python3 scripts/main.py joint Alice,Bob
python3 scripts/main.py remove Alice
```

Supported time formats:

```text
16
16:30
下午4
晚8
```

### Data Files

User data is stored locally:

```text
data/users.json
data/active.json
```

These files may contain personal birth information. Avoid committing them to a public repository.

## Tests

Run:

```bash
python3 -m unittest scripts/test_lunar_core.py
```

The test suite includes 12 fixed BaZi examples and 128 deterministic random date round-trip checks.
