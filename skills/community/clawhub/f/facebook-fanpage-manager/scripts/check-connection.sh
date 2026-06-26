#!/bin/bash
# Kiểm tra kết nối Facebook Fanpage
# Cách dùng: bash check-connection.sh

echo "🔍 Kiểm tra kết nối Facebook Fanpage..."
echo "========================================="

# Kiểm tra biến môi trường
if [ -z "$FACEBOOK_PAGE_ID" ]; then
  echo "❌ Chưa cấu hình FACEBOOK_PAGE_ID"
  echo "   Thêm vào openclaw.json hoặc export FACEBOOK_PAGE_ID=..."
  exit 1
fi

if [ -z "$FACEBOOK_ACCESS_TOKEN" ]; then
  echo "❌ Chưa cấu hình FACEBOOK_ACCESS_TOKEN"
  echo "   Thêm vào openclaw.json hoặc export FACEBOOK_ACCESS_TOKEN=..."
  exit 1
fi

echo "📋 Page ID: $FACEBOOK_PAGE_ID"
echo "🔑 Token: ${FACEBOOK_ACCESS_TOKEN:0:20}...${FACEBOOK_ACCESS_TOKEN: -10}"
echo ""

# Gọi API kiểm tra
RESPONSE=$(curl -s "https://graph.facebook.com/v21.0/$FACEBOOK_PAGE_ID?fields=name,followers_count,fan_count" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN")

# Kiểm tra lỗi
if echo "$RESPONSE" | grep -q '"error"'; then
  echo "❌ Kết nối THẤT BẠI!"
  echo ""
  ERROR_MSG=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('error',{}).get('message','Unknown error'))" 2>/dev/null)
  echo "   Lỗi: $ERROR_MSG"
  echo ""
  echo "💡 Giải pháp:"
  echo "   1. Kiểm tra Page ID có đúng không"
  echo "   2. Kiểm tra Token còn hạn không (debug tại developers.facebook.com/tools/debug/accesstoken/)"
  echo "   3. Lấy token mới theo hướng dẫn trong references/setup-guide.md"
  exit 1
fi

# Thành công
PAGE_NAME=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('name','N/A'))" 2>/dev/null)
FOLLOWERS=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('followers_count','N/A'))" 2>/dev/null)
FANS=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('fan_count','N/A'))" 2>/dev/null)

echo "✅ Kết nối THÀNH CÔNG!"
echo ""
echo "   📄 Fanpage: $PAGE_NAME"
echo "   👥 Followers: $FOLLOWERS"
echo "   👍 Fans: $FANS"
echo ""
echo "========================================="
echo "Sẵn sàng sử dụng!"
