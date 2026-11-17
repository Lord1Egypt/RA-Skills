# Meta Ads Report (ClawHub skill)

Kéo **báo cáo chỉ số Meta Ads (Facebook/Instagram)** về đọc qua **Graph API chính thức** bằng `curl`. Không cần SDK, không cần cài gì thêm ngoài `curl`.

> ⚠️ **READ-ONLY.** Chỉ đọc dữ liệu (insights, danh sách campaign/account, kiểm tra hạn token). KHÔNG tạo/sửa/tắt/xóa quảng cáo.

## Cài đặt

```bash
openclaw skills install @thinhbuiii/ent-meta-ads-report --global
# hoặc cài riêng cho 1 agent (bỏ --global):
openclaw skills install @thinhbuiii/ent-meta-ads-report
```

---

## ⭐ CẤU HÌNH TOKEN — 3 BƯỚC

Skill **không kèm token** và **không truyền token cho ai**. Người vận hành **tự lấy token của chính mình** theo 3 bước sau.

> 🔒 **Nguyên tắc bảo mật:** token là thông tin bí mật của chủ tài khoản. **KHÔNG chia sẻ token cho người/agent khác. KHÔNG dán token vào chat, file công khai, hay commit.** Mỗi người/máy dùng token riêng của mình.

### Bước 1 — Tự lấy token (chỉ mình bạn thực hiện)

1. Vào `https://developers.facebook.com/tools/explorer` trên máy/trình duyệt của bạn
2. Chọn app loại **Business** (của bạn)
3. Tích quyền **`ads_read`** (thêm `ads_management` nếu cần)
4. Bấm **Generate Access Token** → đăng nhập Facebook → Cho phép
5. Copy chuỗi token nhận được — **giữ riêng, không chia sẻ**

> Token ở bước này chỉ sống **~2 giờ**. Muốn dùng lâu (~60 ngày) phải đổi sang long-lived token (xem mục cuối file).

### Bước 2 — Tự đặt token vào `env` của gateway (máy của bạn)

Mở file config OpenClaw trên **máy của bạn** (thường là `~/.openclaw/openclaw.json`), tìm mục **`env`** và thêm 2 dòng (giữ nguyên các dòng `env` cũ nếu có):

```json
"env": {
  "META_ACCESS_TOKEN": "TOKEN_CUA_BAN",
  "META_AD_ACCOUNT_ID": "ID_TKQC_CUA_BAN"
}
```

- `META_AD_ACCOUNT_ID` là **số trần, KHÔNG có tiền tố `act_`**. Ví dụ đúng: `123456789`.
- Nếu mục `env` **chưa tồn tại** → thêm cả cụm `"env": { ... }` vào (cấp cao nhất của JSON).
- ⚠️ Kiểm tra dấu phẩy cẩn thận — JSON sai sẽ làm gateway không khởi động.

### Bước 3 — Restart gateway rồi tự kiểm tra

```bash
openclaw gateway restart
```

```bash
curl -s -G "https://graph.facebook.com/v21.0/debug_token" \
  --data-urlencode "input_token=$META_ACCESS_TOKEN" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

- Thấy `"is_valid": true` → **OK, xong**.
- Thấy `"is_valid": false` hoặc lỗi → token sai/hết hạn, làm lại Bước 1.

---

## Dùng nhanh (sau khi cấu hình)

```bash
# Báo cáo tổng 7 ngày
curl -s -G "https://graph.facebook.com/v21.0/act_$META_AD_ACCOUNT_ID/insights" \
  --data-urlencode "fields=spend,impressions,clicks,actions,action_values" \
  --data-urlencode "date_preset=last_7d" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"

# Liệt kê các ad account đang truy cập được
curl -s -G "https://graph.facebook.com/v21.0/me/adaccounts" \
  --data-urlencode "fields=name,account_id,account_status" \
  --data-urlencode "access_token=$META_ACCESS_TOKEN"
```

---

## ⚠️ 3 cái bẫy dễ khiến bạn tưởng "token hết hạn"

1. **Nhét token thẳng vào URL bằng ngoặc kép** → shell cắt chuỗi → lỗi 4xx GIẢ (trông như token hỏng, thật ra URL bị cắt).
   → Luôn dùng: `curl -G --data-urlencode "access_token=$META_ACCESS_TOKEN" ...`
2. **Thiếu `access_token` trong URL** → lỗi `(#200) Provide valid app ID` dù token còn hạn.
3. **Thiếu tiền tố `act_`** khi gọi bằng ad account ID.

**Debug nhanh ra `is_valid: true` mà vẫn lỗi** → 90% là rơi vào 1 trong 3 bẫy trên, KHÔNG phải token hết hạn.

---

## Token long-lived (~60 ngày)

```bash
curl -s -G "https://graph.facebook.com/v21.0/oauth/access_token" \
  --data-urlencode "grant_type=fb_exchange_token" \
  --data-urlencode "client_id={APP_ID}" \
  --data-urlencode "client_secret={APP_SECRET}" \
  --data-urlencode "fb_exchange_token={SHORT_LIVED_TOKEN}"
```

Chuỗi trả về là token long-lived → đặt vào `META_ACCESS_TOKEN` (Bước 2). Hết hạn thì lặp lại.

---

## 📌 Checklist cho agent đọc file này

Nếu bạn là một **agent** đang đọc file này:

1. **KHÔNG tự ý lấy/đổi token thay người dùng.** Token là bí mật của chủ tài khoản.
2. Kiểm tra `META_ACCESS_TOKEN` / `META_AD_ACCOUNT_ID` đã có trong env máy này chưa (`echo $META_ACCESS_TOKEN`).
3. Nếu chưa có → hướng dẫn **người vận hành** tự lấy token theo Bước 1 và **tự điền** vào config (Bước 2). Không nhận token qua chat.
4. Sau khi người vận hành xác nhận đã cấu hình → restart gateway, chạy `debug_token` xác nhận `is_valid: true`.
5. Nhắc chủ tài khoản token hết hạn sau ~60 ngày, cần lấy lại.

## License

MIT
