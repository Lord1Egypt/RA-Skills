# ai-news-poster 在 OpenClaw 的操作手册

这份手册用于你下次独立完成安装、验证、测试与日常出图。

## 1) 前置条件

- 已安装 OpenClaw CLI（命令 `openclaw` 可用）
- 已有 skill 源目录：`/Users/cyc-mac/skills/skills/ai-news-poster`
- Python 3 可用（命令 `python3` 可用）
- 首次使用如缺依赖，安装 `Pillow`

```bash
python3 -m pip install pillow
```

## 2) 安装到 OpenClaw

OpenClaw 的本地托管技能目录是：`~/.openclaw/skills`

```bash
mkdir -p ~/.openclaw/skills
cp -R /Users/cyc-mac/skills/skills/ai-news-poster ~/.openclaw/skills/ai-news-poster
```

## 3) 安装后验证

### 3.1 查看技能详情

```bash
openclaw skills info ai-news-poster
```

预期关键结果：
- `Source: openclaw-managed`
- `Path: ~/.openclaw/skills/ai-news-poster/SKILL.md`
- 状态为 `Ready`

### 3.2 全量健康检查

```bash
openclaw skills check
```

预期关键结果：
- `ai-news-poster` 出现在 `Ready to use` 列表里

## 4) 功能测试（推荐方式）

直接从 OpenClaw 安装目录运行渲染脚本，验证“真实安装副本”能出图。

```bash
python3 ~/.openclaw/skills/ai-news-poster/scripts/render.py \
  ~/.openclaw/skills/ai-news-poster/examples/input.sample.json \
  ~/.openclaw/skills/ai-news-poster/output/openclaw-test.png
```

预期输出：
- 终端显示 `Poster generated: .../openclaw-test.png`
- 文件存在：`~/.openclaw/skills/ai-news-poster/output/openclaw-test.png`

## 5) 日常使用（每天出图）

### 5.1 准备当天新闻 JSON

复制模板：

```bash
cp ~/.openclaw/skills/ai-news-poster/examples/input.sample.json \
  ~/.openclaw/skills/ai-news-poster/examples/input.today.json
```

然后编辑 `input.today.json`：
- `date` 改为当天日期
- `news` 必须 **恰好 5 条**
- 每条包含：`headline` / `summary` / `source` / `tag`
- `brand` 改成你的品牌名

### 5.2 生成当天海报

```bash
python3 ~/.openclaw/skills/ai-news-poster/scripts/render.py \
  ~/.openclaw/skills/ai-news-poster/examples/input.today.json \
  ~/.openclaw/skills/ai-news-poster/output/today.png
```

## 6) 更新 skill（你改了仓库里的版本后）

如果你在仓库里改了 `skills/ai-news-poster`，重新覆盖到 OpenClaw 托管目录：

```bash
rm -rf ~/.openclaw/skills/ai-news-poster
cp -R /Users/cyc-mac/skills/skills/ai-news-poster ~/.openclaw/skills/ai-news-poster
openclaw skills info ai-news-poster
```

## 7) 常见问题排障

### Q1: `openclaw skills info ai-news-poster` 找不到
- 检查目录是否存在：`ls ~/.openclaw/skills/ai-news-poster`
- 确认 `SKILL.md` 在该目录下
- 再执行一次复制安装命令

### Q2: 渲染时报 `Pillow is required`
- 安装依赖：`python3 -m pip install pillow`

### Q3: 报错 `'news' must contain exactly 5 items`
- 必须严格 5 条新闻，不能多不能少

### Q4: 中文字体显示异常
- 当前脚本会自动尝试 macOS 常见中文字体
- 若你本机缺字体，可安装中文字体后重试

## 8) 快速检查清单（30 秒）

- [ ] `openclaw skills info ai-news-poster` 显示 `Ready`
- [ ] 输入 JSON 是 5 条新闻
- [ ] `python3 .../render.py input.json output.png` 成功
- [ ] 输出 PNG 存在且可打开

