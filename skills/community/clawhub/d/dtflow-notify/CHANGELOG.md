# Changelog

## 0.1.1
- 新增：钉钉「文件」消息单文件 ≤20MB 上限守卫（超限拒绝并提示拆分/压缩）。

## 0.1.0
- 首个公开版：钉钉「工作通知 / 机器人私信 / 本人私信」统一发送出口（`scripts/notify.py`）。
- 凭证按环境变量或 `~/.dingtalk-skills/config` 读取；失败自动写日志。
- 附 `config.example.env` 与安装说明。
