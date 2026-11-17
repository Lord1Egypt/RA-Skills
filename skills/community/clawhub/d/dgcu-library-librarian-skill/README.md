# 东莞城市学院图书馆 AI 馆员 Skill

让支持 Agent Skills 的 AI 助手远程调用图书馆服务，面向本校师生和社会读者公开使用。无需企业微信、学校账号或 API Key。

## 能做什么

- 咨询本馆借阅规则、图书馆资源和文献检索方法。
- 查询东莞城市学院实时纸质馆藏、索书号、馆藏地点和可借册数。
- 同时实时查询人民邮电出版社和电子工业出版社知阅电子书，返回可点击阅读链接。
- 查询东莞图书馆公开馆藏。

电子书检索直接查询两个官网，不使用导入书单。接口失败会明确报告，不把故障当成没有书。

## 安装

从 GitHub 下载或克隆本仓库，将包含 `SKILL.md` 的目录以 `dgcu-library-librarian` 为名放入所用 AI 助手的技能目录，然后重启/刷新技能列表。

```sh
git clone https://github.com/chenxianlong/dgcu-library-librarian-skill.git dgcu-library-librarian
```

例如 Codex 的个人技能目录为 `~/.codex/skills/`，Claude Code 为 `~/.claude/skills/`。也可以从腾讯 SkillHub 搜索技能名 `dgcu-library-librarian` 安装；能否搜索到以平台审核和收录状态为准。

对 AI 助手说：“使用 dgcu-library-librarian 帮我找 Claude Code 电子书，人民邮电和知阅都查。”

## 直接运行

需要 Python 3，只有标准库依赖，无需 `pip install`。

```sh
python scripts/librarian.py --action ebooks "Claude Code" --limit 6
python scripts/librarian.py --action catalog "人工智能" --limit 5
python scripts/librarian.py --action dongguan "三体" --limit 5
python scripts/librarian.py "东莞城市学院学生能借几本书？"
```

## 开放接口

`GET https://lib.dgcu.edu.cn/libai/api/public` 查看能力及限额。

向同一地址 POST JSON：

```json
{"action":"ebooks","query":"Claude Code","limit":6}
```

`action` 可选 `ask`（默认）、`catalog`、`ebooks`、`dongguan`。响应包含 `action`、`queriedAt` 和 `result`。检索最多返回 10 条；`ask` 最长 1000 字，其他检索词最长 100 字。

## 权限、隐私与服务限额

技能和查询接口面向社会公开；图书借阅、入馆及电子书全文阅读仍遵守相应机构的资格与访问规定。查询命中不代表获得阅读授权。

问题通过 HTTPS 发到图书馆服务器；智能咨询还会发送给图书馆配置的模型服务商。请勿发送密码、证件号、读者账号或敏感个人信息。公开接口不记录对话正文，反向代理保留常规访问日志。

当前限额：每来源 IP 每 10 分钟 20 次、每日 100 次；全局每日 1000 次，并发 3 个请求。共用公网出口的用户共用 IP 额度。429 请至少等待 10 分钟；故障时稍后再试。限额为服务端内存计数，服务重启会重置；服务不承诺全天候无故障。

本仓库仅包含技能说明和公开接口客户端，不含服务端密钥、企业微信配置、服务器登录信息或内部运维资料。

## 许可

技能说明及客户端代码使用 [MIT License](LICENSE.txt)。图书元数据、书籍及远程服务不因本许可获得再分发或访问授权。
