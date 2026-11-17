# SkillHub MCP 广场提报文本（cite-holmes-mcp）

> 状态：**材料就绪，待提交**。MCP 广场为收录制（现网 27 条全部 publisherType=tencent，
> 无自助入口）——提交走官方评测问卷/建议反馈通道，以下为按现网条目 schema 备齐的字段。
> 署名：**SorSor**（SkillHub 发布者，uid 437178；cite-holmes/academic-figures 等技能作者）

| 字段 | 内容 |
|---|---|
| slug | `cite-holmes-mcp` |
| name | 引文核验 MCP（Cite Holmes） |
| publisher | SorSor |
| homepage | https://github.com/docsor1212/cite-holmes/tree/main/mcp |
| sourceUrl | https://github.com/docsor1212/cite-holmes |
| install | `uvx --from "git+https://github.com/docsor1212/cite-holmes#subdirectory=mcp" cite-holmes-mcp` |
| category | 学术科研（或按平台归"社区 MCP"） |

**summary（可直接粘贴）**：

> 通过 MCP Server 对论文/文稿引文做逐条机械核验（DOI/PMID/arXiv/URL 多源官方
> 注册库交叉：DOI.org、PubMed E-utilities、arXiv API、Crossref/Retraction Watch、
> Wayback），输出三级判定（verified/partial/unreachable/invalid）与 CiteScore
> 评分卡（0–100 + A–D 级）。tools 齐备：5 tools（v5.6 起）+ 2 resources + 1 工作流 prompt。
> 零密钥可用（可选学术 API key 增强），零遥测，本地优先；批量 ≤50/次、输出自动
> 截断（MCP 消息安全）。适配论文写作、投稿预检与 AI 幻觉引用检测场景。
> MCP 版本 mcp-v2.0.0（tag），随主仓 v3.5.0+ 分发。

**安装提示词（可直接粘贴）**：

> 安装 cite-holmes-mcp：uvx --from "git+https://github.com/docsor1212/cite-holmes#subdirectory=mcp" cite-holmes-mcp

## 完工证据链（随提报可引用）

| DoD | 证据 |
|---|---|
| G1 pyproject+入口 | `uvx --from <mcp/> cite-holmes-mcp --help` 正常输出（本地与干净环境 git 双通道） |
| G2 E2E | `mcp/tests/e2e_transcript.md`：in-memory 全原语（2026-10-04 v3.5.0 期历史记录：彼时 tools/list=2；真网络 3 claims：verified/invalid/verified，CiteScore 40/100）。当前工具面 5 tools 见 mcp/README.md 与 server.py @mcp.tool 注册 |
| G3 README | `mcp/README.md`：三安装通道+三客户端配置 JSON+边界说明 |
| G5 边界 | `mcp/tests/test_bounds.py` 6/6：批量 >50 拒、=50 收、长字段截断（结构保持）、总输出 <64KB |
| 落仓 | tag `mcp-v2.0.0`（git ls-remote 可查）+ 干净环境（env -i）git 拉取 uvx 通过 |
| npm | **跳过（声明）**：Python 包，uvx/git 为唯一主通道，README 已注明 |
