# 常见问题（FAQ）

> 本文件集中回答 ai-weekly 使用中最常遇到的问题。其它文档（SKILL.md / README / CHANGELOG）里的零散说明以本页为准。
> 找不到答案？多半在 [SKILL.md](SKILL.md) 的对应章节，或 [data_sources.md](data_sources.md) / [report_structure.md](report_structure.md)。

---

## 一、怎么用这个 Skill？（最常被问）

**直接说人话就能触发**，不用记命令。举几个真实对话：

- 「帮我生成一份本周 AI 行业新闻周报」→ 走完整模式，产出单文件 HTML 网站
- 「这周的 AI 新闻怎么样？给我看个简报就行」→ 走轻量模式，对话里直接出 Markdown 列表
- 「帮我把上周的周报推送到飞书」→ 读取 report.json，推飞书头条卡片
- 「生成 8 月最后一周的 AI 周报，时间范围 2026-08-25 到 2026-08-31」→ 你指定时间窗

如果你用的是 WorkBuddy 这类 Agent 平台，把 `ai-weekly` 技能装入后，上述任意一句都会自动激活全链路（抓取 → 生成 → 可选推送）。

### 想要「多轮真实对话」的完整示范？

上面是单轮触发。如果你想知道**遇到歧义 / 改需求 / 抓取失败 / 想复现历史周报**时该怎么说、技能会怎么回，
见 [SKILL.md § 1.1 真实对话场景](SKILL.md)——那里有 5 则完整多轮对话：

| 场景 | 你会这么问 | 技能会怎么做 |
|------|-----------|-------------|
| 时间窗有歧义 | 「这周的周报呢？」 | 先反问是 W37 还是 W38，不猜 |
| 中途改需求 | 「图表能去掉吗」 | 直说没有这个开关，给 3 个真选项 |
| 抓取失败 | 跑了但条数很少 | 先 `--check-feeds` 体检，再给重试/降级方案 |
| 复现历史周报 | 「重生成 8/24 那期」 | 先说清 RSS 只保留约 1 周，问你有没有快照 |
| 参数细化 | 「榜单多几条、标题别翻译」 | `--ranking-top 20 --no-translate-title` |

> ⚠️ **重生成历史周报必读**：一定要显式传 `--date <周期截止日>`。不传的话报告周期会被写成「今天−7 ~ 今天」，
> 历史周报会被悄悄改写成当期内容（文件名不变、内容变了）。

---

## 二、安装与配置

### Q1：依赖怎么装？
技能根目录有 `requirements.txt`（`feedparser` / `requests` / `beautifulsoup4` 等）。推荐用受管 venv：

```bash
# 建 venv（一次性）
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt

# 之后一律用统一启动器，它会自动探测并复用 venv
bash run_report.sh scripts/fetch_ai_news.py --output news.json
```

> 没 venv / 没依赖也能跑：用 WebSearch 手动搜集新闻写成同样结构的 JSON，再走 `--api-json` 消费。

### Q2：GitHub PAT 怎么生成？（仅用 GitHub Pages 部署时需要）
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 勾 `repo`（含 `public_repo`）权限
3. 复制 token，设为环境变量 `GITHUB_TOKEN`，或交给 `git` 凭据管理器
4. 推送 `gh-pages` 分支用：`git push origin gh-pages`

> **不想碰 GitHub？** 部署后端可换 `tencent-cos` / `vercel` / `netlify` / `cloudflare-pages` / `local`（见第六节），这些都不需要 GitHub PAT。

### Q3：`run_report.sh` 是什么？必须用吗？
是统一启动器，负责自动探测并复用 `aiweekly` venv，避免你手动选解释器。所有脚本都建议通过它跑：
```bash
bash run_report.sh scripts/<脚本>.py [参数]
```

---

## 三、首次使用

### Q4：第一次跑要做什么？
最小闭环（只生成网站，不部署、不推送）：
1. 抓新闻：`bash run_report.sh scripts/fetch_ai_news.py --output news.json`
2. （建议）用 WebSearch 拿市场/融资真实数据，记下数值与来源
3. 生成：`bash run_report.sh scripts/generate_site.py --api-json news.json --market-data <数值> --market-source "<来源>" -o AI_News_YYYY-MM-DD.html`
4. 校验：`bash run_report.sh scripts/validate_report.py --html AI_News_YYYY-MM-DD.html`
5. 展示：把 `AI_News_YYYY-MM-DD.html` 用 `present_files` 打开

### Q5：飞书推送目标怎么配置？
最简方式——跑交互式向导（免手动建文件）：
```bash
python scripts/init_feishu_config.py
```
它会引导你填群 chat_id 或私聊 user_id，自动生成 `delivery/feishu_target.json` 并校验。详情见第五节。

也可手动：把目标写进 `delivery/feishu_target.json`：
```json
{ "chat_id": "oc_xxxx" }
```
（该文件已被 `.gitignore` 忽略，不会入库。）

### Q6：新闻数据从哪来？要我自己搜吗？
默认全部来自 14 个 RSS 源（国内 7 + 国外 7），脚本自动抓。市场/融资图表需要你用 WebSearch 拿真实值注入（未注入时图表会标「示例/估算数据」，绝不伪造）。

---

## 四、常见问题（生成 / 内容）

### Q7：排行榜显示的是旧的 / 几周前的？
实时榜依赖运行环境的网络：
- 国内环境优先国内源（OpenCompass 司南 / SuperCLUE / ModelScope），但部分是 SPA，抓不到就回退随技能附带的 `cn_leaderboard_snapshot.json`（标注截止日，徽章显示「缓存快照」）。
- 国外源（LMArena / Artificial Analysis / Hugging Face）直连不稳时，会自动尝试国内可访问的公开镜像；镜像也失败再回退本地快照。
- 所有源都失败 → 显示「暂无实时数据」，绝不编造模型名。

可用 `bash run_report.sh scripts/leaderboard_diagnose.py` 看每个源的可达性和镜像回退命中。

### Q8：市场数据是估算的，怎么回事？
没注入真实 WebSearch 数据时，图表会标「示例/估算数据」。这是故意的——**绝不伪造实时数据**。想拿到真实值，用 `--market-data` / `--funding-data` 注入（参数里有 `--market-source` / `--funding-source` 署名）。

### Q9：英文报道我看不懂中文？
每条英文新闻在生成时强制带中文摘要（校验器查「英文报道中文总结」覆盖率，要求 100%）。若某条缺中文总结，是抓取异常，回报即可。

### Q10：「本周看点」三块内容（看点卡 / 给本周的你 / 关键词彩标）有时看不到？
这三块在**生成阶段服务端预渲染进静态 HTML**，即使禁用 JS 也可见。若重生成后仍看不到，先确认：① 输出路径就是打开的那个文件（别输出到 `-fixed`/`-static` 之类旁路名）；② 浏览器硬刷新（Ctrl/Shift+R）。

---

## 五、飞书推送

### Q11：飞书推送走什么通道？
推送统一走 **飞书连接器（connector）**：经 `lark-cli` 发送，密钥由连接器托管、不写进仓库（webhook 自定义机器人路径已移除）。适合 WorkBuddy 用户。
  ```bash
  python delivery/feishu_connector.py --report report.json --chat-id oc_xxxx
  python delivery/feishu_connector.py --report report.json --user-id ou_xxxx --as user   # 私聊给自己冒烟
  ```

### Q12：bot 身份和 user 身份有什么区别？
- `--as bot`（默认）：以应用机器人身份发，需机器人已加入目标群。
- `--as user`：以你本人身份发，需你对该会话有发消息权限（首次测试最省事，不用加机器人）。

### Q13：飞书配置能不能一键生成？
能。`scripts/init_feishu_config.py` 交互式引导，自动产出正确格式的 `feishu_target.json` 并做基础校验：
```bash
python scripts/init_feishu_config.py
# 填 chat_id（群）或 user_id（私聊）→ 写入 delivery/feishu_target.json
```

---

## 六、网页托管（部署）

### Q14：必须部署到 GitHub Pages 吗？
**不必。** `scripts/deploy.py` 支持多后端：
```bash
bash run_report.sh deploy --html AI_News_YYYY-MM-DD.html --deploy-to github-pages   # 默认
bash run_report.sh deploy --html AI_News_YYYY-MM-DD.html --deploy-to tencent-cos     # 国内最稳
bash run_report.sh deploy --html AI_News_YYYY-MM-DD.html --deploy-to vercel          # 海外免备案
```
- `github-pages`：需 PAT + push + 切 Pages 源（一次性）。
- `tencent-cos` / `vercel` / `netlify` / `cloudflare-pages` / `local`：**无需 GitHub**，按后端要求填密钥/基址即可（示例见 `delivery/deploy_config.example.json`）。
- 飞书卡片的 `view_url` 由后端自动推导，非 GitHub 后端也不会指向 github.io。

### Q15：GitHub Pages 怎么开？PAT 权限怎么设？
仓库 Settings → Pages → Source 选 `gh-pages / /root`（首次用 `run_report.sh deploy --switch-pages` 可自动切）。PAT 需 `repo` 权限（见第二节 Q2）。

### Q16：域名怎么绑？
GitHub Pages：仓库 Settings → Pages → Custom domain 填你的域名，去 DNS 加 CNAME。其它后端按各自平台绑自定义域名。

---

## 七、网络问题

### Q17：国外源（LMArena / HuggingFace / Artificial Analysis）连不上？
这是**预期内的降级路径**，不是故障：
- 技能已内置**国内可访问镜像回退**：主源失败自动试公开镜像（见 Q7）。
- 镜像也失败时回退到随技能附带的离线快照，报告标注「缓存快照」，**绝不编造**。
- 无需你做任何额外配置。

### Q18：`--proxy` 是做什么的？
`--proxy` / `HTTPS_PROXY` 是**标准的 HTTP 出站代理参数**，用于「企业内网要求所有出站流量经统一代理」这类网络架构。它是一项通用的网络配置能力，**不是**为了访问特定站点而设；本技能不提供、也不支持任何规避网络管理措施的做法。公网直连环境无需配置。

### Q19：排行榜源到底怎么选的？
优先级：`--ranking-json` 指定快照 > 多源池实时（按 `--region` 排序，国内优先国内源）> 国内快照 / 本地缓存 > 「暂无实时数据」。用 `leaderboard_diagnose.py` 可看实际探测结果。

---

## 八、模型数据

### Q20：排行榜里某些模型是假的吗？
不会。`model_profiles.json` 每条都带 `verified=true` 和真实来源锚点（官方公告 / Artificial Analysis / Hugging Face）。早期自动抓取、无来源核实的推测条目已被 `scripts/validate_models.py` 移到 `model_profiles_unverified.json`，**不参与排行榜、不回填**。

### Q21：怎么判断某个模型资料是否可信？
```bash
bash run_report.sh scripts/validate_models.py --check
```
输出会告诉你主表里有无未核实条目。要新增模型，先 WebSearch 核实、再写回 `model_profiles.json`（带 `source`）。

### Q22：snapshot / 缓存快照是什么意思？
实时抓取不到时用的兜底数据，随技能附带或本地缓存，文件里标注了数据截止日，页面徽章也会写明「缓存快照」，不会伪装成实时。

### Q23：排行榜是按什么排的？为什么和别家不一样？
综合榜用 LMArena / Artificial Analysis；开源榜用 Hugging Face / ModelScope。每个子榜头部有「实时·国内源 / 实时·国外源 / 缓存快照」徽章，页脚注明探测到的网络环境与选用策略——你始终知道数据从哪来。

---

## 九、排错速查

| 现象 | 先查 | 命令 |
|------|------|------|
| 某「本周看点」块看不到 | 输出路径 / 硬刷新 | 见 Q10 |
| 排行榜是旧的 | 网络 / 镜像回退 | `leaderboard_diagnose.py` |
| 市场图显示「示例/估算」 | 没注入真实数据 | `--market-data` + `--market-source` |
| 飞书推不动 | 配置 / 目标 | `init_feishu_config.py` 重生成；`--dry-run` 预览 |
| 模型档案有未核实项 | 数据治理 | `validate_models.py --check` |
| 部署失败 | 后端凭据 | `deploy.py --dry-run` 看计划 |
