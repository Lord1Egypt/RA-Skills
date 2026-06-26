#!/bin/bash
# 快速授权 Outlook 邮箱

cd "$(dirname "$0")"

python3 authorize.py outlook \
  --client-id "0360031a-ad0e-4bce-9d2f-0c53eda894b8" \
  --client-secret "914fb58f-4aea-4ddb-bb97-51d66581cfee" \
  --tenant-id "40a99b83-a343-41ca-b303-3e122965a6d8" \
  --name "outlook_live"

echo ""
echo "✅ 授权完成！现在可以使用 Outlook 邮箱了"
echo ""
echo "检查邮件:"
echo "  python3 email-pro.py --account outlook_live check --limit 10"
echo ""
echo "发送邮件:"
echo "  python3 email-pro.py --account outlook_live send --to 'recipient@example.com' --subject '主题' --body '内容'"
