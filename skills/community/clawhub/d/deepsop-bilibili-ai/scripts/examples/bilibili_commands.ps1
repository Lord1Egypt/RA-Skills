# 假设 social-auto-upload 已 clone 到 $SAU_HOME，且已经跑过 `uv sync --python 3.12`。
$SAU_HOME = "$env:USERPROFILE\.openclaw\social-auto-upload"

# 登录
# 建议由用户自己在本地真实终端里执行。
# 如果终端二维码显示不完整，可以打开当前目录下的 qrcode.png 扫码。
$account = "account_a"
# account_name is user-defined. One account_name maps to one account file.
# You can prepare multiple account names and run them in parallel.

& uv run --project $SAU_HOME python sau_cli.py bilibili login --account $account

# 校验
& uv run --project $SAU_HOME python sau_cli.py bilibili check --account $account

# 上传视频
& uv run --project $SAU_HOME python sau_cli.py bilibili upload-video `
  --account $account `
  --file .\videos\demo.mp4 `
  --title "Bilibili CLI Demo" `
  --desc "Bilibili CLI Demo" `
  --tid 249 `
  --tags 足球,测试 `
  --schedule "2026-03-26 16:00"
