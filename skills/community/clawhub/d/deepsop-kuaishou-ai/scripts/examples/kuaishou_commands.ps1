# 假设 social-auto-upload 已 clone 到 $SAU_HOME，且已经跑过 `uv sync --python 3.12`。
$SAU_HOME = "$env:USERPROFILE\.openclaw\social-auto-upload"

# PowerShell examples for the installed sau CLI.

# account_name is user-defined. One account_name maps to one account file.
# You can prepare multiple account names and run them in parallel.
$account = "account_a"
$video = "videos/demo.mp4"
$thumbnail = "videos/demo.png"
$noteImages = @("videos/1.png", "videos/2.png", "videos/3.png")

& uv run --project $SAU_HOME python sau_cli.py kuaishou login --account $account
& uv run --project $SAU_HOME python sau_cli.py kuaishou check --account $account

& uv run --project $SAU_HOME python sau_cli.py kuaishou upload-video `
  --account $account `
  --file $video `
  --title "Kuaishou video from PowerShell" `
  --desc "Kuaishou video description from PowerShell" `
  --tags "cli,video" `
  --thumbnail $thumbnail `
  --headless

& uv run --project $SAU_HOME python sau_cli.py kuaishou upload-note `
  --account $account `
  --images $noteImages `
  --title "Kuaishou note title from PowerShell" `
  --note "Kuaishou note from PowerShell" `
  --tags "cli,note" `
  --headless
