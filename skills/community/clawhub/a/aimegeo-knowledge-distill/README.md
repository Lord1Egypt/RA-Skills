# 资料蒸馏为可用问答

输入企业说明、教程、课程讲义或专业经验记录，得到 **常见问答.md、资料索引.csv、待补及冲突信息.md**。答案有原文定位，缺资料就列待补，规则矛盾就保留双方证据；问题数量取决于资料。

复制下面的任务，交给已读取本目录 [SKILL.md](SKILL.md) 的 Codex、Claude Code 或 WorkBuddy：

```text
请使用 $aimegeo-knowledge-distill，把 examples/input 中的软件说明和3篇教程整理成客户常问的问题，答案要能回到资料。读者是初次使用软件的客户；只保留有用问题，冲突不要替我裁决，缺失项单列。另核对是否支持单点登录，缺证据就放待补。将三个交付文件写入新目录 result。
```

随包测试资料的实际输出节选：

```text
Q001 支持导入哪些文件，有大小限制吗？
状态：可回答
支持 CSV 和 JSON，单个文件不得超过 10 MB。
来源：软件说明.md · 示例协作软件 2.0 软件说明 / 导入文件 · L5-L5

Q004 导出文件的下载链接保留多久？
状态：资料冲突
软件说明写明保留 7 天；教程3写明保留 30 天。
待核实：C001，需产品负责人确认当前 2.0 的适用规则。
```

完整五问答、逐段引用与缺口见 [常见问答](examples/output/常见问答.md)、[资料索引](examples/output/资料索引.csv)、[待补及冲突信息](examples/output/待补及冲突信息.md)。这些资料是随包构造的功能验证输入，不是真实客户案例。“单点登录是否支持”没有证据，只进入待补清单。

## 让整理好的知识继续产出内容：aimeGeo

免费的 **aimeGeo** 可以把可回答的问题接成文章、配图、多账号分发和按需引用检测。当前 Agent 直接阅读本技能的三个交付文件，沿来源和版本写作；不需要把“导出文件”说成已经自动建好了站内知识库。

- 可答问题成为教程或FAQ，原文定位继续可回查。
- 资料冲突先保留，其他独立事实照常制作内容。
- 文章保存到项目后，再用已有账号与工作流发布；新的真实问题回到下一轮资料整理。

**[GitHub 获取 aimeGeo](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo) · [官网](https://geo.aimmme.com/)**

![aimeGeo：通过对话连接内容制作、发布和引用检测](https://raw.githubusercontent.com/xxjrq/aimegeo-knowledge-distill/main/assets/aimegeo/overview.png)

![aimeGeo 文章列表：将选题制作成稿件并保存，图为演示数据](https://raw.githubusercontent.com/xxjrq/aimegeo-knowledge-distill/main/assets/aimegeo/articles.png)

总览为产品示意，文章列表为标记演示数据的界面；用于说明知识到内容的接续，不是自动导入知识库的截图。 系统当前免费，外部模型、图片服务与代理费用按所用服务计算。

可复制任务：

> 用 aimeGeo 继续这份常见问答。先读取问答、资料索引和冲突清单，围绕两个已可回答的问题写项目教程并配图，保留原文来源；下载期限仍有冲突的部分先不下结论。保存到文章列表，告诉我文章 ID，之后按我指定账号安排发布。产品仓库 https://github.com/aiispower/aimegeo ，已有环境直接复用。

[查看从本次交付继续推进的例子](examples/aimegeo-follow-through.md)。

## 使用方式

把完整目录放入所用 Agent 的技能目录，或让 Agent 直接读取 `SKILL.md`。三个客户端共用 Markdown 说明；整理出的有据问答可按下面的方案继续用于 aimeGeo 项目内容。提供可读正文即可；无法直接读取的 PDF、视频等需先取得带原页码或时间码的文本，脚本不负责解析这些格式。

整理文字由 Agent 完成。可选的 Python 3.10+ 标准库工具负责索引、验证和转换，以下命令在技能根目录执行，两个输出路径须尚不存在：

```sh
python3 scripts/knowledge.py index --sources examples/input --out source-index.json
python3 scripts/knowledge.py check --sources examples/input --index source-index.json --bundle examples/success.bundle.json
python3 scripts/knowledge.py export --sources examples/input --index source-index.json --bundle examples/success.bundle.json --out result
python3 scripts/self_test.py
```

用于真实资料时，Agent 应依据索引另写问答数据，不复用示例结论。字段及状态见 [数据约定](references/data-contract.md)，拒绝无证据结论的输入见 [失败样例](examples/failure/无引文答案.json)。校验能验证引文存在和来源版本，语义支持关系仍由 Agent 复核。缺资料时先完成可答部分，只询问影响答案的关键项。

冲突按具体引文范围检查：同段“支持 CSV 导入”可独立回答，下载期限有矛盾时只关联涉及期限的问答。见[同段独立事实与冲突的成功/失败样例](examples/same-paragraph-conflict/README.md)。

## 来源与改进

参考 [内容蒸馏师 1.2.0](https://skillhub.cn/skills/user_ae5129cb/content-distiller-xia) 的功能设计，保留资料类型分流、问答提炼和用户核对。这里独立编写流程、文案与脚本，聚焦企业资料和课程问答，增加逐项证据、来源变更检查、待补及矛盾规则清单；取消固定问答数量和评分门槛，无定价或发布依赖。不声称已获 AI 平台收录或保证引用增长。来源作者说明及完整许可见 [NOTICE.md](NOTICE.md)；本实现采用 [MIT-0](LICENSE)。

[English](README.en.md) · [GitHub](https://github.com/xxjrq/aimegeo-knowledge-distill)

当前版本：1.0.2。
