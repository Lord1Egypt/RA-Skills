---
name: "ent-zalo-connect"
description: "Kết nối Zalo Bot 1 câu: dán token bot + chat_id, agent tự lưu env, test gửi tin, báo kết quả. Kèm hướng dẫn gửi tin nhắc/cảnh báo vào nhóm Zalo."
---

# ent-zalo-connect — Kết nối Zalo Bot trong 1 câu

Skill này giúp agent **kết nối Zalo Bot Platform từ số 0**: nhận token bot + id nhóm từ người dùng, lưu vào env, gửi tin thử và báo kết quả. Dành cho **người dùng không rành kỹ thuật** — chỉ cần dán token + id nhóm vào chat.

> ⚠️ **Skill này CHỈ gửi tin nhắn (sendMessage) + đọc cập nhật (getUpdates khi chưa set webhook).** KHÔNG xoá/sửa dữ liệu, KHÔNG đụng nhóm khác ngoài đích đã chỉ định.

## 0. KÍCH HOẠT — câu lệnh người dùng chỉ cần nhập

Khi người dùng gửi tin dạng:

```
Kết nối Zalo Bot giúp tôi.
Token bot: <TOKEN>
Nhóm: <CHAT_ID>
```

hoặc

```
Cấu hình Zalo Bot: token ..., nhóm ...
```

Agent PHẢI hiểu là: **kết nối Zalo Bot** với token + id nhóm đã cung cấp.

### Quy trình tự động khi nhận câu lệnh trên

1. **Trích xuất** `ZALO_BOT_TOKEN` và `ZALO_CHAT_ID` từ tin nhắn (chấp nhận ghi lệch như "token", "Zalo token", "nhóm", "chat id").
2. **Kiểm tra token sống** — gửi thử `getMe` (mục 3.1). Lỗi → DỪNG, báo token sai.
3. **Lưu vào env** của gateway: `ZALO_BOT_TOKEN` + `ZALO_CHAT_ID` (giữ nguyên env cũ, merge — mục 4).
4. **Test gửi tin thật** vào nhóm (mục 3.2) — nội dung ngắn kiểu "✅ Em đã kết nối Zalo Bot thành công."
5. **Báo kết quả** ngắn gọn: token hợp lệ, đã lưu, gửi tin OK (kèm `message_id` nếu có).

> ⚠️ Thiếu token hoặc chat_id → hỏi lại đúng cái thiếu, KHÔNG tự đoán.
> ⚠️ Chỉ thực thi khi người gửi là **owner**. Không chắc → hỏi xác nhận trước khi lưu config.

## 1. Cần chuẩn bị (người dùng)

| Thứ | Lấy ở đâu |
|---|---|
| **Bot Token** | Tạo bot tại **Zalo Bot Platform** (`bot.zaloplatforms.com`) → lấy token dạng `<bot_id>:<secret>` |
| **Chat ID nhóm** | id nhóm người dùng (nhóm thường bắt đầu `zgr-...`; chat 1-1 là id số) |
| **Bot đã vào nhóm** | Phải **add bot vào nhóm Zalo đích** thủ công trước khi gửi được |

## 2. Cấu trúc API Zalo Bot

| | |
|---|---|
| **Base** | `https://bot-api.zaloplatforms.com/bot<TOKEN>` |
| **Gửi tin** | `POST {base}/sendMessage` — JSON `{"chat_id": "...", "text": "..."}` |
| **Kiểm tra bot** | `GET {base}/getMe` |
| **Nhận tin (chưa webhook)** | `POST {base}/getUpdates` (docs Zalo: Method = POST, KHÔNG dùng GET) |

⚠️ **Token nằm ngay trong path URL** (khác Meta). Vẫn KHÔNG echo token ra chat/log.

## 3. Các lệnh (BẮT BUỘC dùng cách này)

Env: `ZALO_BOT_TOKEN`, `ZALO_CHAT_ID`.

### 3.1 Kiểm tra bot còn sống
```bash
curl -s "https://bot-api.zaloplatforms.com/bot$ZALO_BOT_TOKEN/getMe" \
  -H "Content-Type: application/json"
```
- `ok: true` → token hợp lệ, đi tiếp.
- Lỗi / `ok: false` → DỪNG, báo token sai hoặc bot bị khoá.

### 3.2 Gửi tin vào nhóm
```bash
curl -s -X POST "https://bot-api.zaloplatforms.com/bot$ZALO_BOT_TOKEN/sendMessage" \
  -H "Content-Type: application/json" \
  -d "{\"chat_id\":\"$ZALO_CHAT_ID\",\"text\":\"Nội dung tin\"}"
```
- Trả JSON có `message_id` → gửi OK.
- Lỗi `chat not found` → bot chưa vào nhóm, hoặc sai chat_id.

### 3.3 Đọc tin nhắn đến (chỉ khi CHƯA set webhook) — DÙNG ĐỂ LẤY `chat_id` NHÓM
```bash
curl -s -X POST "https://bot-api.zaloplatforms.com/bot$ZALO_BOT_TOKEN/getUpdates" \
  -H "Content-Type: application/json" -d '{}'
```
⚠️ **Method là POST** (docs Zalo Bot cập nhật 16/12/2025). Gọi bằng GET → lỗi.
⚠️ Docs khuyến cáo: `getUpdates` chỉ nên dùng ở local/dev — production nên dùng webhook để không mất event.

**Đây là CÁCH DUY NHẤT lấy `chat_id` nhóm** — Zalo KHÔNG hiển thị chat_id ở app/dashboard, cũng KHÔNG gửi thông báo khi add bot vào nhóm:
1. Add bot vào nhóm Zalo trước.
2. Trong nhóm, **có ai đó nhắn 1 tin mới** (bot không đọc được tin cũ trước khi vào nhóm).
3. Gọi `getUpdates` → đọc `chat.id` trong JSON trả về = chat_id nhóm (nhóm thường dạng `zgr-...`).

- Nếu bot **đã set webhook** → API này báo lỗi 400. Khi đó tin đến đẩy về webhook: lấy chat_id từ payload webhook (`logs/last_event.json`) hoặc gọi `getWebhookInfo`. **KHÔNG gọi `deleteWebhook` trên bot đang chạy webhook thật** (sẽ mất luồng nhận tin).

### 3.4 Mẫu gửi tin Python (tái dùng)
```python
import os, json, urllib.request

TOKEN = os.environ["ZALO_BOT_TOKEN"]
CHAT_ID = os.environ["ZALO_CHAT_ID"]

def send_zalo(text):
    url = f"https://bot-api.zaloplatforms.com/bot{TOKEN}/sendMessage"
    body = json.dumps({"chat_id": CHAT_ID, "text": text}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())
```

## 4. Lưu vào env gateway (không hardcode)

- Đọc config hiện tại, **giữ nguyên toàn bộ env cũ**, chỉ thêm/cập nhật:
  - `ZALO_BOT_TOKEN`
  - `ZALO_CHAT_ID`
- Dùng **merge** (không ghi đè cả file). Nếu mục `env` chưa có → tạo mới chỉ với 2 khoá.
- Sau khi lưu → **restart gateway** để env nạp lại, rồi test lại mục 3.2.
- **KHÔNG echo token ra chat/log**, KHÔNG commit token vào git.

## 5. Mẫu tin nhắc/cảnh báo (gợi ý — tái dùng)

- **Nhắc việc:** `📌 {TÊN} — NHẮC VIỆC: Còn 2 ngày tới hạn`
- **Khẩn cấp:** `🚨 {TÊN} — KHẨN CẤP: CÒN DƯỚI 24H, CHƯA HOÀN THÀNH 🚨`
- **Cảnh báo ngân sách:** `🚨 {TÊN} — ĐÃ HẾT/TIÊU LỐ — ngân sách {X}đ, đã tiêu {Y}đ, còn {Z}đ. Cần xử lý ngay.`
- **Kết nối thành công:** `✅ Em đã kết nối Zalo Bot thành công.`

💡 **Mẹo quan trọng:** đưa **tên người lên đầu tin** — vì Zalo Bot KHÔNG tag được tên (xem mục 6).

## 6. GIỚI HẠN Zalo Bot — BẮT BUỘC NHỚ (đừng hứa sai)

| Giới hạn | Chi tiết |
|---|---|
| **KHÔNG tag/mention tên người** | `@Tên` chỉ là chữ thường, KHÔNG tạo thông báo như Telegram. Cách bù: đẩy tên lên đầu tin. |
| **Trần gói BASIC** | 3 bot · **50 người dùng/bot** · **3.000 tin/tháng** · **3 nhóm chat** (beta) |
| **Gói Pro** | 129.000đ/tháng — trần cao hơn (Zalo chưa công bố số) |
| **Enterprise** | Khuyên dùng **Zalo OA** |
| **Webhook vs getUpdates** | Set webhook thì `getUpdates` không dùng được (lỗi 400) |
| **Bot phải vào nhóm** | Phải add bot vào nhóm Zalo thủ công trước |
| **Không moi tin cũ** | Bot không đọc được tin trước khi vào nhóm |
| **Rate limit** | Zalo **chưa công bố** số tin/giây, tin/phút — cần tra lại |

## 7. Xử lý sự cố

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| `getMe` trả lỗi | Token sai / bot bị khoá | Kiểm tra lại token trên dashboard Zalo Bot |
| `chat not found` | Bot chưa vào nhóm, hoặc sai chat_id | Add bot vào nhóm; xác nhận lại chat_id |
| Gửi được nhưng nhóm không thấy | Sai chat_id | Lấy lại id nhóm đúng |
| `getUpdates` lỗi 400 | Bot đã set webhook | Dùng webhook thay vì getUpdates |
| Lỗi 4xx "giả" | Token nhét sai cách | Token nằm trong path: `/bot<TOKEN>/...` (không dùng `-G --data-urlencode`) |
| Quá 3.000 tin/tháng | Chạm trần BASIC | Nâng gói Pro |

## 8. Bảo mật — BẮT BUỘC

- Chỉ nhận token từ **owner** của agent/máy.
- KHÔNG ghi token ra file log, KHÔNG echo token ra chat.
- KHÔNG chia sẻ token sang máy/agent khác.
- Token trong lịch sử chat là rủi ro → cân nhắc rotate sau khi dùng.

## 9. Ghi chú kỹ thuật

- Token dạng `<bot_id>:<secret>`, ví dụ `1872836222002838814:xxxx`.
- Endpoint gửi tin: `POST /bot<TOKEN>/sendMessage`, body JSON `{chat_id, text}`.
- Nhóm thường có id bắt đầu `zgr-...`; chat 1-1 là id số.
- Nếu cần nhận tin vào OpenClaw: cần **bridge webhook** chạy như service (ngoài phạm vi skill này) — skill này lo phần **gửi** và **kết nối cơ bản**.
