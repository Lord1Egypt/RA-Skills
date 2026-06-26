# Amazon Review Workbook Skill

这是一个可移植的 Amazon 评论抓取与表格交付 skill。

它可以完成这些事情：

- 通过已登录的 Chrome 会话抓取 Amazon 商品评论
- 导出固定 14 列的事实工作簿
- 可选接入 DeepLX 自动补全 `评论中文版`
- 生成轻量标注输入，交给模型补全语义字段
- 将模型标注结果合并回完整工作簿
- 在追加抓取前先做覆盖率检查
- 根据历史跑数自动调优关键词词表

## 仓库结构

- `README.md`：仓库使用说明
- `SKILL.md`：给 agent 环境使用的 skill 说明
- `references/`：配置、输出契约、标注规则
- `scripts/`：核心 CLI 和处理脚本
- `agents/openai.yaml`：默认 agent prompt 元数据
- `tests/`：轻量回归测试

## 环境要求

- Python 3.11 及以上
- 一个已经登录 Amazon 的 Chrome，会话开启远程调试端口 `9222`
- 需要的 Python 包：

```bash
pip install pandas openpyxl requests websocket-client
```

- 如果想先自动翻译，再做语义标注，可选配置 DeepLX

## 配置方法

### 1. 启动带远程调试的 Chrome

Windows：

```powershell
"$env:ProgramFiles\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="$env:LOCALAPPDATA\Google\Chrome\User Data"
```

启动后确认这个 Chrome 会话里已经登录了 Amazon。

### 2. 可选配置 DeepLX

把 `.env.example` 复制为本地 `.env`，或者直接设置环境变量：

```env
DEEPLX_API_URL=https://your-deeplx-host/translate
DEEPLX_API_KEY=your-optional-key
```

## 快速开始

### 健康检查

```bash
python scripts/amazon_review_workbook.py doctor --url "<amazon-url>"
```

### 抓取事实工作簿

```bash
python scripts/amazon_review_workbook.py intake --url "<amazon-url>" --output-dir "./amazon-review-output"
```

### 在继续追加抓取前先看覆盖率

```bash
python scripts/amazon_review_workbook.py coverage-check --url "<amazon-url>" --db-path "./amazon-review-output/amazon_review_cache.sqlite3"
```

### 可选：先补 `评论中文版`

```bash
python scripts/amazon_review_workbook.py translate --input-json "./amazon-review-output/amazon_<asin>_review_rows_factual.json" --output-dir "./amazon-review-output"
```

### 生成标注输入

```bash
python scripts/amazon_review_workbook.py taxonomy-bootstrap --input-json "./amazon-review-output/amazon_<asin>_review_rows_translated.json" --output-dir "./amazon-review-output"
python scripts/amazon_review_workbook.py prepare-tagging --input-json "./amazon-review-output/amazon_<asin>_review_rows_translated.json" --output-dir "./amazon-review-output"
```

### 合并标注结果，导出最终工作簿

```bash
python scripts/amazon_review_workbook.py merge-build --base-json "./amazon-review-output/amazon_<asin>_review_rows_translated.json" --labels-json "./amazon-review-output/amazon_<asin>_labels.json" --output-dir "./amazon-review-output" --taxonomy-version "v1" --strict
```

## 关键词策略

现在的关键词搜索已经做了收束和提速：

- `deep` 模式默认只跑 combo，不自动跑关键词
- 只有显式传 `--keywords` 才会进入关键词阶段
- `--keywords` 不带值时，会使用内置 profile
- 内置 profile：
  - `generic`
  - `electronics`
  - `dashcam`
- 默认复用策略是 `successful`
  - 历史上搜出过新增评论的关键词会被跳过
  - 近期 0 命中的关键词会临时抑制，避免短时间重复撞墙

示例：

```bash
python scripts/amazon_review_workbook.py intake --url "<amazon-url>" --output-dir "./amazon-review-output" --keywords --keyword-profile electronics
```

```bash
python scripts/amazon_review_workbook.py intake --url "<amazon-url>" --output-dir "./amazon-review-output" --keywords --keyword-profile dashcam --keyword-reuse-scope none
```

## 关键词自动调优

可以根据历史 SQLite 缓存和旧关键词实验报告，生成或刷新调优状态：

```bash
python scripts/amazon_review_workbook.py keyword-autotune --output-dir "./amazon-review-output" --db-path "./amazon-review-output/amazon_review_cache.sqlite3" --report-glob "./reports/*keywords*.json"
```

它会生成 `keyword_tuning_state.json`，之后关键词阶段会自动优先读取这个调优结果。

## 主要命令

- `doctor`
- `collect`
- `intake`
- `coverage-check`
- `keyword-autotune`
- `translate`
- `taxonomy-bootstrap`
- `prepare-tagging`
- `merge-build`
- `summary`

## 发布说明

这个仓库的定位是“可公开复用的 skill 源码仓库”，不是私有工作目录镜像。

### 发布边界

发布前请确认以下内容不会进入仓库：

- `.env`
- `amazon-review-output/`
- SQLite 缓存文件
- `label_cache.jsonl`
- 真实评论导出表格
- 一次性本地调试脚本或临时分析产物

### 推荐发布流程

1. 先跑测试：

```bash
python -m unittest discover -s tests -p "test_*.py"
```

2. 确认 `.gitignore` 已覆盖本地产物。

3. 检查 staged 文件，只保留这些类型：

- `README.md`
- `SKILL.md`
- `references/`
- `scripts/`
- `tests/`
- `agents/openai.yaml`
- `.env.example`
- `LICENSE`

4. 提交前重点检查：

- 是否有真实评论数据
- 是否有本机绝对路径
- 是否有 API Key / token / cookie
- 是否把 `amazon-review-output` 里的实际样本带进去了

5. 提交并推送：

```bash
git add .
git commit -m "your message"
git push origin main
```

### 版本建议

如果改动较大，建议按下面的粒度发版：

- `patch`：修 bug、改文档、小幅参数调整
- `minor`：新增命令、新增 profile、新增非破坏性能力
- `major`：改输出契约、改工作流主路径、移除旧参数

### 发布后建议检查

- 仓库首页 README 是否可直接教会新人配置
- `LICENSE` 是否存在
- `git clone` 后是否能按 README 跑通 `doctor --help`
- `SKILL.md`、CLI 参数、README 三者是否一致

## 输出契约

事实工作簿和最终工作簿都使用固定 14 列：

1. `序号`
2. `评论用户名`
3. `国家`
4. `星级评分`
5. `评论原文`
6. `评论中文版`
7. `评论概括`
8. `情感倾向`
9. `类别分类`
10. `标签`
11. `重点标记`
12. `评论链接网址`
13. `评论时间`
14. `评论点赞数`

详细字段规则见 [references/output-schema.md](references/output-schema.md)。

## 测试

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## 说明

- `.env`、SQLite 缓存、真实评论导出文件、本地输出产物默认都不会提交
- 这个仓库发布的是可复用 skill，不包含私有评论数据
