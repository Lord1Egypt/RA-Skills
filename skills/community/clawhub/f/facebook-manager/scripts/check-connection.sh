#!/bin/bash
# Kiểm tra kết nối Facebook — cả Page Token và User Token
# Cách dùng: bash check-connection.sh

echo "🔍 Kiểm tra kết nối Facebook..."
echo "========================================="
echo ""

# Kiểm tra Page Token
if [ -n "$FACEBOOK_PAGE_TOKEN" ] && [ -n "$FACEBOOK_PAGE_ID" ]; then
  echo "📄 Chế độ PAGE TOKEN"
  echo "   Page ID: $FACEBOOK_PAGE_ID"
  echo "   Token: ${FACEBOOK_PAGE_TOKEN:0:20}..."
  RESP=$(curl -s "https://graph.facebook.com/v22.0/$FACEBOOK_PAGE_ID?fields=name,followers_count,fan_count" \
    -H "Authorization: Bearer $FACEBOOK_PAGE_TOKEN")
  if echo "$RESP" | grep -q '"error"'; then
    ERR=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('error',{}).get('message','?'))" 2>/dev/null)
    echo "   ❌ THẤT BẠI: $ERR"
  else
    NAME=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('name','?'))" 2>/dev/null)
    FANS=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('fan_count','?'))" 2>/dev/null)
    echo "   ✅ Fanpage: $NAME (${FANS} fans)"
  fi
  echo ""
else
  echo "⏭️  Page Token: chưa cấu hình (bỏ qua)"
  echo ""
fi

# Kiểm tra User Token
if [ -n "$FACEBOOK_USER_TOKEN" ]; then
  echo "👤 Chế độ USER TOKEN"
  echo "   Token: ${FACEBOOK_USER_TOKEN:0:20}..."
  RESP=$(curl -s "https://graph.facebook.com/v22.0/me?fields=id,name" \
    -H "Authorization: Bearer $FACEBOOK_USER_TOKEN")
  if echo "$RESP" | grep -q '"error"'; then
    ERR=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('error',{}).get('message','?'))" 2>/dev/null)
    echo "   ❌ THẤT BẠI: $ERR"
  else
    NAME=$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('name','?'))" 2>/dev/null)
    echo "   ✅ User: $NAME"
    # Test group access
    GROUPS=$(curl -s "https://graph.facebook.com/v22.0/me/groups?limit=3&fields=name" \
      -H "Authorization: Bearer $FACEBOOK_USER_TOKEN")
    if echo "$GROUPS" | grep -q '"data"'; then
      echo "   ✅ Quyền nhóm: OK"
    else
      echo "   ⚠️  Quyền nhóm: chưa có (thêm groups_access_member_info)"
    fi
  fi
  echo ""
else
  echo "⏭️  User Token: chưa cấu hình (bỏ qua)"
  echo ""
fi

echo "========================================="
echo "Xong!"
