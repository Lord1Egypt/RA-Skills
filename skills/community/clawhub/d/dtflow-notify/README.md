# dtflow-notify（readme）

把钉钉接成你 agent 的**通知/私信通道**：工作通知、机器人单聊私信、以本人身份私信；支持 text/markdown/文件。

## 依赖
- `python3`、`requests`
- 钉钉**企业内部应用**（AppKey/AppSecret/AgentId）
- `dws`（仅 `--dm-self` 本人私信需要）

## 配置
写 `~/.dingtalk-skills/config`（键=值，逐行，见 `config.example.env`）或导出同名环境变量：
`DINGTALK_APP_KEY / DINGTALK_APP_SECRET / DINGTALK_AGENT_ID / DINGTALK_MY_USER_ID / DINGTALK_MY_NAME`

## 用法
```bash
python3 scripts/notify.py --text "内容"              # 工作通知
python3 scripts/notify.py --markdown "**内容**" --title "标题"
python3 scripts/notify.py --dm-self --text "内容"    # 以本人身份私信
python3 scripts/notify.py --file /abs/path.xlsx      # 文件
```

## 说明
这是「钉钉联动」能力族的**基座**。群消息→自动建待办、定时提醒→钉钉等工作流可按需扩展。

## License
MIT
