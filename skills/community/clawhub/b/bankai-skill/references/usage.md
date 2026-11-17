# BankAI 使用与运维说明（references/usage.md）

> 给使用者和后续维护者的补充细节。SKILL.md 保持精简，详情在此。

## 1. 成本与计费
- 模型默认 `deepseek-chat`（DeepSeek 官方直连）。输出价约 **12 元 / 百万 tokens**；输入（system + user prompt）同样计费。
- 单次最长输出 `max_tokens = 8192`，约 0.1 元；叠加输入，单次实际约 **几分钱**。
- **高峰翻倍**：每日 **9–12 点、14–18 点** 价格翻倍（约 0.2 元/次）。非高峰调用更省，建议在闲时批量生成。

## 2. 合规与风险提示（重要）
- 输出为 **AI 生成草稿**，须 **人工核对** 后方可使用；不得直接提交未经审核的内容。
- Prompt 已要求"禁止编造数据、标注需人工核对"；但仍须使用者对关键数字、监管依据、文号负责。
- **数据出境**：云端 MVP 下，输入内容会发往 DeepSeek 公有云。涉及银行**敏感/涉密**文档时，务必走私有化（见 §4），不要经公有云。

## 3. 密钥
- 从 DeepSeek 开放平台获取 API Key，设为环境变量 `DEEPSEEK_API_KEY`。
- 可用 `--key-env <变量名>` 指定其它环境变量名。
- 不推荐复用网站的腾讯云函数代理（`deepseek-v4-flash` + `X-App-Token`）——该 token 是线上网站私有秘钥，Skill 不应依赖。

## 4. 私有化（BASE_URL，数据不出行）
- 设置环境变量 `BASE_URL` 指向自建 **OpenAI 兼容**端点（如 vLLM / Ollama 暴露的 `…/chat/completions`）。
- 调用时加 `--base-url $BASE_URL`，模型名用本地部署的模型（如 `deepseek-r1-distill` 等）。
- 此口子对应 feasibility 里的"私有化部署"诉求；v1 仅预留，不在云端 MVP 默认开启。

## 5. 调用参数
- `--type <id或名称>`：公文类型，可用 `scripts/bankai_write.mjs --list` 查看 59 种。
- `--input <JSON或@文件路径>`：各字段键值对（必填见 SKILL.md 分类说明）。
- `--output <文件>`：可选，写入文件而非打印。
- `--model`：默认 `deepseek-chat`，可覆盖。
- `--mock`：离线模拟，不真实调用（用于测试/演示）。
